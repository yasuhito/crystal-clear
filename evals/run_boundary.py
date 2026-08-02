#!/usr/bin/env python3
"""Run the supplemental, post-candidate already-clear boundary check."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import tempfile
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from evals.evaluation import observe_trace, skill_hash_record
from evals.run_behavior import _materialize_skill, _retry
from evals.run_smoke import execute_pi, git_revision, pi_version, run_command

EVALS_ROOT = Path(__file__).resolve().parent
REPO_ROOT = EVALS_ROOT.parent
DEFAULT_SCENARIOS = EVALS_ROOT / "already-clear-scenarios.json"


def load_boundary_scenarios(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text())
    rows = data.get("scenarios", [])
    if not data.get("version") or data.get("status") != "supplemental-post-candidate":
        raise ValueError("boundary fixture must be versioned and labeled post-candidate")
    if len(rows) < 4 or len({row.get("id") for row in rows}) != len(rows):
        raise ValueError("boundary fixture must contain unique English and Japanese cases")
    required = {"id", "language", "source_text", "output_contract", "prompt"}
    for row in rows:
        if set(row) != required or row["language"] not in {"en", "ja"}:
            raise ValueError(f"invalid boundary scenario {row.get('id')}")
        if row["source_text"] not in row["prompt"] or row["output_contract"] not in row["prompt"]:
            raise ValueError(f"boundary scenario {row['id']} must embed source and contract")
    counts = Counter(row["language"] for row in rows)
    if counts["en"] != counts["ja"]:
        raise ValueError("boundary fixture must balance English and Japanese")
    return data


def parse_equivalence(value: str) -> dict[str, Any]:
    text = value.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if len(lines) >= 3 and lines[-1].strip() == "```": text = "\n".join(lines[1:-1])
    try: data = json.loads(text)
    except json.JSONDecodeError as error: raise ValueError(f"equivalence output is not JSON: {error}") from error
    if not isinstance(data, dict) or set(data) != {"equivalent", "critical_meaning_change", "evidence"}:
        raise ValueError("equivalence output has unexpected fields")
    if not isinstance(data["equivalent"], bool) or not isinstance(data["critical_meaning_change"], bool) or not isinstance(data["evidence"], str):
        raise ValueError("equivalence output has invalid values")
    if data["critical_meaning_change"] and data["equivalent"]:
        raise ValueError("a critical meaning change cannot be equivalent")
    return data


def _judge_prompt(source: str, output: str, language: str) -> str:
    return f'''You are a strict semantic-equivalence evaluator for an already-clear {language} passage. Determine whether the revision is unchanged in meaning, certainty, instructions, register, protected strings, and practical reading effect. Stylistic differences count as equivalent only when no meaning or clarity regression exists.\n\nSOURCE:\n{source}\n\nREVISION:\n{output}\n\nReturn only JSON: {{"equivalent":true,"critical_meaning_change":false,"evidence":"concise evidence"}}'''


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    result = {"post_candidate_fixture": True, "runs": len(rows), "languages": {}}
    for language in ("en", "ja"):
        scoped = [row for row in rows if row["language"] == language]
        equivalent = sum(row["unchanged"] or row["equivalence"]["equivalent"] for row in scoped)
        result["languages"][language] = {
            "runs": len(scoped), "unchanged": sum(row["unchanged"] for row in scoped),
            "equivalent": equivalent, "equivalent_rate": round(equivalent / len(scoped), 4) if scoped else None,
            "critical_meaning_changes": sum(row["equivalence"]["critical_meaning_change"] for row in scoped),
        }
    return result


def render(summary: dict[str, Any], rows: list[dict[str, Any]], version: str, revision: str) -> str:
    lines = ["# Already-clear supplemental boundary check", "", "This fixture was frozen after the candidate was authored. It is supplemental and is not part of the 425-generation core matrix.", "", f"Fixture: `{version}`; candidate: `{revision}`; five repeats per case.", "", "| Language | Runs | Exact unchanged | Unchanged/equivalent | Rate | Critical changes |", "|---|---:|---:|---:|---:|---:|"]
    for language in ("en", "ja"):
        item = summary["languages"][language]
        lines.append(f"| {language} | {item['runs']} | {item['unchanged']} | {item['equivalent']} | {item['equivalent_rate']:.1%} | {item['critical_meaning_changes']} |")
    lines += ["", "Every changed output receives a strict GPT semantic-equivalence judgment; exact equality is deterministic. Results remain separated by language.", "", "| Scenario | Language | Repeat | Result | Evidence |", "|---|---|---:|---|---|"]
    for row in sorted(rows, key=lambda x: (x["scenario_id"], x["repeat"])):
        status = "unchanged" if row["unchanged"] else "equivalent" if row["equivalence"]["equivalent"] else "changed"
        lines.append(f"| {row['scenario_id']} | {row['language']} | {row['repeat']} | {status} | [result]({row['result_file']}) |")
    return "\n".join(lines) + "\n"


def _run_one(scenario: dict[str, Any], repeat: int, candidate: str, model: str, output: Path, fixture_version: str, release: str, harness: str) -> dict[str, Any]:
    stem = f"{scenario['id']}--r{repeat:02}"
    raw = output / "raw"; raw.mkdir(parents=True, exist_ok=True)
    result_path, trace_path = raw / f"{stem}.result.json", raw / f"{stem}.trace.jsonl"
    with tempfile.TemporaryDirectory(prefix="crystal-clear-boundary-") as tmp:
        root = Path(tmp); session_root = root / "pi"
        skill, hashes = _materialize_skill(candidate, session_root / "work")
        appended = root / "injected.md"; appended.write_text("Apply this skill silently.\n\n" + skill.read_text())
        started = datetime.now(timezone.utc).isoformat(); start = time.monotonic()
        live = execute_pi(prompt=scenario["prompt"], model=model, session_root=session_root, appended_instructions=appended)
        duration = round((time.monotonic() - start) * 1000); shutil.copy2(live, trace_path)
        observation = observe_trace(trace_path, Path("/__boundary__/SKILL.md"))
    unchanged = observation.final_output == scenario["source_text"]
    if unchanged:
        equivalence = {"equivalent": True, "critical_meaning_change": False, "evidence": "Exact string equality."}
        judgment_trace = None
    else:
        prompt = _judge_prompt(scenario["source_text"], observation.final_output, scenario["language"])
        with tempfile.TemporaryDirectory(prefix="crystal-clear-boundary-judge-") as tmp:
            judge_live = execute_pi(prompt=prompt, model=model, session_root=Path(tmp))
            judge_trace_path = raw / f"{stem}.judgment.trace.jsonl"; shutil.copy2(judge_live, judge_trace_path)
            judged = observe_trace(judge_trace_path, Path("/__boundary_judge__/SKILL.md"))
        equivalence = parse_equivalence(judged.final_output); judgment_trace = f"raw/{judge_trace_path.name}"
        judgment_output = judged.final_output; judgment_prompt_sha256 = hashlib.sha256(prompt.encode()).hexdigest()
    row = {
        "schema_version": 1, "fixture_version": fixture_version, "fixture_status": "supplemental-post-candidate",
        "scenario_id": scenario["id"], "language": scenario["language"], "source_text": scenario["source_text"], "prompt": scenario["prompt"],
        "repeat": repeat, "candidate_ref": candidate, "candidate_revision": run_command(["git", "rev-parse", candidate], cwd=REPO_ROOT),
        "skill_hash": skill_hash_record(hashes["SKILL.md"], source="system-injection"), "skill_artifact_hashes": hashes,
        "provider_model": model, "pi_version": release, "harness_git_revision": harness, "started_at": started, "duration_ms": duration,
        "final_output": observation.final_output, "session_id": observation.session_id, "unchanged": unchanged, "equivalence": equivalence, "judgment_trace_file": judgment_trace,
        "raw_judgment_output": None if unchanged else judgment_output, "judgment_prompt_sha256": None if unchanged else judgment_prompt_sha256,
        "trace_file": f"raw/{trace_path.name}", "result_file": f"raw/{result_path.name}",
    }
    result_path.write_text(json.dumps(row, indent=2, ensure_ascii=False) + "\n"); print(f"[boundary] {stem}")
    return row


def load_results(output: Path) -> list[dict[str, Any]]:
    return [json.loads(path.read_text()) for path in sorted((output / "raw").glob("*.result.json"))]


def validate(data: dict[str, Any], rows: list[dict[str, Any]], candidate: str, repeats: int, output: Path | None = None) -> None:
    expected = {(s["id"], r) for s in data["scenarios"] for r in range(1, repeats + 1)}
    actual = [(r["scenario_id"], r["repeat"]) for r in rows]
    if len(actual) != len(set(actual)) or set(actual) != expected: raise ValueError("boundary evidence matrix is incomplete, duplicate, or stale")
    revision = run_command(["git", "rev-parse", candidate], cwd=REPO_ROOT)
    for field in ("provider_model", "pi_version", "harness_git_revision"):
        if len({row[field] for row in rows}) != 1:
            raise ValueError(f"boundary evidence mixes {field}")
    scenario_by_id = {row["id"]: row for row in data["scenarios"]}
    with tempfile.TemporaryDirectory(prefix="crystal-clear-boundary-validation-") as tmp:
        _, expected_hashes = _materialize_skill(candidate, Path(tmp) / "skill")
    for row in rows:
        scenario = scenario_by_id[row["scenario_id"]]
        if row["candidate_revision"] != revision or row["fixture_version"] != data["version"] or row["fixture_status"] != data["status"]:
            raise ValueError("boundary evidence has stale provenance")
        if row["source_text"] != scenario["source_text"] or row["prompt"] != scenario["prompt"] or row["language"] != scenario["language"]:
            raise ValueError(f"boundary evidence for {row['scenario_id']} has stale scenario content")
        if row["skill_artifact_hashes"] != expected_hashes or row["skill_hash"] != skill_hash_record(expected_hashes["SKILL.md"], source="system-injection"):
            raise ValueError(f"boundary evidence for {row['scenario_id']} has stale skill hashes")
        if row["unchanged"] != (row["final_output"] == row["source_text"]):
            raise ValueError(f"boundary evidence for {row['scenario_id']} has stale equality result")
        if row["unchanged"]:
            expected_equivalence = {"equivalent": True, "critical_meaning_change": False, "evidence": "Exact string equality."}
            if row["equivalence"] != expected_equivalence or row["judgment_trace_file"] is not None or row["raw_judgment_output"] is not None or row["judgment_prompt_sha256"] is not None:
                raise ValueError(f"unchanged boundary evidence for {row['scenario_id']} has a spurious judgment")
        else:
            prompt = _judge_prompt(row["source_text"], row["final_output"], row["language"])
            if row["equivalence"] != parse_equivalence(row["raw_judgment_output"]) or row["judgment_prompt_sha256"] != hashlib.sha256(prompt.encode()).hexdigest():
                raise ValueError(f"boundary judgment for {row['scenario_id']} is stale")
        if output is not None:
            trace = output / row["trace_file"]
            result = output / row["result_file"]
            if not trace.is_file() or not result.is_file(): raise ValueError(f"boundary evidence for {row['scenario_id']} is missing raw files")
            observed = observe_trace(trace, Path("/__boundary_validation__/SKILL.md"))
            if observed.final_output != row["final_output"] or observed.session_id != row["session_id"]: raise ValueError(f"boundary trace for {row['scenario_id']} disagrees with its record")
            if not row["unchanged"]:
                judge_trace = output / row["judgment_trace_file"]
                if not judge_trace.is_file() or observe_trace(judge_trace, Path("/__boundary_judge_validation__/SKILL.md")).final_output != row["raw_judgment_output"]:
                    raise ValueError(f"boundary judgment trace for {row['scenario_id']} disagrees with its record")


def write_report(output: Path, data: dict[str, Any], rows: list[dict[str, Any]], candidate: str, repeats: int) -> None:
    validate(data, rows, candidate, repeats, output); summary = summarize(rows)
    summary.update({"fixture_version": data["version"], "candidate_revision": run_command(["git", "rev-parse", candidate], cwd=REPO_ROOT), "repeats": repeats})
    (output / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    (output / "SUMMARY.md").write_text(render(summary, rows, data["version"], summary["candidate_revision"]))


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--candidate-ref", required=True); parser.add_argument("--scenarios", type=Path, default=DEFAULT_SCENARIOS); parser.add_argument("--output", type=Path, required=True); parser.add_argument("--repeats", type=int, default=5); parser.add_argument("--model", default="openai-codex/gpt-5.6-sol"); parser.add_argument("--report-only", action="store_true")
    args = parser.parse_args()
    if args.candidate_ref == "worktree": raise ValueError("boundary release evidence requires an immutable candidate ref")
    if args.repeats != 5: raise ValueError("boundary release evidence requires five repeats")
    data = load_boundary_scenarios(args.scenarios); args.output.mkdir(parents=True, exist_ok=True); rows = load_results(args.output)
    if not args.report_only:
        existing = {(r["scenario_id"], r["repeat"]) for r in rows}; release, harness = pi_version(), git_revision()
        for scenario in data["scenarios"]:
            for repeat in range(1, 6):
                if (scenario["id"], repeat) not in existing:
                    rows.append(_retry(lambda scenario=scenario, repeat=repeat: _run_one(scenario, repeat, args.candidate_ref, args.model, args.output, data["version"], release, harness)))
    write_report(args.output, data, rows, args.candidate_ref, args.repeats); print(args.output / "SUMMARY.md")


if __name__ == "__main__": main()
