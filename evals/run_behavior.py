#!/usr/bin/env python3
"""Run and report the frozen Crystal Clear clarity-behavior baseline."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import shutil
import sys
import tempfile
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any, Iterable

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from evals.evaluation import observe_trace, skill_hash_record
from evals.run_smoke import execute_pi, git_revision, pi_version, run_command, sha256


REPO_ROOT = Path(__file__).resolve().parent.parent
EVALS_ROOT = Path(__file__).resolve().parent
DEFAULT_SCENARIOS = EVALS_ROOT / "behavior-scenarios.json"
DEFAULT_OUTPUT = EVALS_ROOT / "results" / "behavior" / "178eaf8"
CATEGORIES = ("english", "japanese", "multilingual-core")
MULTILINGUAL_LANGUAGES = {"es", "zh-CN", "ar", "de", "mixed-ja-en"}
FAILURE_MODES = {
    "buried-answer", "ambiguous-referent", "detached-qualification",
    "terminology-drift", "register-mismatch", "accidental-certainty-change",
}
CHECK_KINDS = ("protected-string", "fact", "number", "constraint", "condition")
CRITICAL_FAILURE_TYPES = {
    "invented-fact", "removed-constraint", "changed-instruction",
    "changed-certainty", "corrupted-protected-text", "broken-register",
}
JUDGMENT_KEYS = {
    "critical_preservation_failure", "critical_failure_types", "preservation",
    "first_pass_understanding", "core_structure", "referent_scope_terminology",
    "register_preserved", "naturalness", "evidence",
}
_PRINT_LOCK = threading.Lock()


def load_behavior_scenarios(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text())
    rows = data.get("scenarios", [])
    if not data.get("version") or len(rows) != 15:
        raise ValueError("behavior fixture must define a version and exactly five scenarios per category")
    if len({row.get("id") for row in rows}) != 15:
        raise ValueError("behavior scenario ids must be unique")
    required = {"id", "category", "language", "failure_modes", "source_text", "output_contract", "prompt", "checks"}
    for row in rows:
        missing = required - row.keys()
        if missing:
            raise ValueError(f"scenario {row.get('id')} is missing {sorted(missing)}")
        if row["category"] not in CATEGORIES:
            raise ValueError(f"scenario {row['id']} has an unknown category")
        if not set(row["failure_modes"]) <= FAILURE_MODES:
            raise ValueError(f"scenario {row['id']} has an unknown failure mode")
        if row["source_text"] not in row["prompt"] or row["output_contract"] not in row["prompt"]:
            raise ValueError(f"scenario {row['id']} prompt must contain source and output contract")
        for check in row["checks"]:
            if set(check) != {"id", "kind", "values"} or check["kind"] not in CHECK_KINDS or not check["values"]:
                raise ValueError(f"scenario {row['id']} has an invalid deterministic check")
    if Counter(row["category"] for row in rows) != Counter({category: 5 for category in CATEGORIES}):
        raise ValueError("behavior fixture must contain exactly five scenarios per category")
    multi = {row["language"] for row in rows if row["category"] == "multilingual-core"}
    if multi != MULTILINGUAL_LANGUAGES:
        raise ValueError("multilingual-core coverage is incomplete")
    if {mode for row in rows for mode in row["failure_modes"]} != FAILURE_MODES:
        raise ValueError("behavior fixture must cover every required failure mode")
    if {check["kind"] for row in rows for check in row["checks"]} != set(CHECK_KINDS):
        raise ValueError("behavior fixture must cover every deterministic check kind")
    return data


def score_preservation(scenario: dict[str, Any], output: str) -> dict[str, Any]:
    checks = []
    failures: Counter[str] = Counter()
    for check in scenario["checks"]:
        missing = [value for value in check["values"] if value not in output]
        passed = not missing
        if not passed:
            failures[check["kind"]] += 1
        checks.append({**check, "missing": missing, "passed": passed})
    output_present = bool(output.strip())
    return {
        "output_present": output_present,
        "passed": output_present and not failures,
        "checks": checks,
        "failures_by_kind": dict(sorted(failures.items())),
    }


def assign_blind_pairs(pairs: list[tuple[str, int]], *, seed: int, skill_arm: str) -> list[dict[str, Any]]:
    """Seed both anonymous A/B orientation and presentation order, then balance A/B."""
    rng = random.Random(seed)
    assignments = []
    for scenario_id, repeat in pairs:
        skill_first = bool(rng.getrandbits(1))
        a_arm, b_arm = ((skill_arm, "no-skill") if skill_first else ("no-skill", skill_arm))
        assignments.append({
            "pair_id": f"{scenario_id}--r{repeat:02d}",
            "scenario_id": scenario_id,
            "repeat": repeat,
            "a_arm": a_arm,
            "b_arm": b_arm,
        })
    target_skill_a = len(assignments) // 2
    skill_a = [row for row in assignments if row["a_arm"] == skill_arm]
    if len(skill_a) > target_skill_a:
        for row in rng.sample(skill_a, len(skill_a) - target_skill_a):
            row["a_arm"], row["b_arm"] = row["b_arm"], row["a_arm"]
    elif len(skill_a) < target_skill_a:
        no_skill_a = [row for row in assignments if row["a_arm"] == "no-skill"]
        for row in rng.sample(no_skill_a, target_skill_a - len(skill_a)):
            row["a_arm"], row["b_arm"] = row["b_arm"], row["a_arm"]
    rng.shuffle(assignments)
    for index, assignment in enumerate(assignments, 1):
        assignment["presentation_index"] = index
    return assignments


def _strip_json_fence(value: str) -> str:
    text = value.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if len(lines) >= 3 and lines[-1].strip() == "```":
            text = "\n".join(lines[1:-1])
    return text


def parse_judgment(value: str, category: str) -> dict[str, Any]:
    try:
        data = json.loads(_strip_json_fence(value))
    except json.JSONDecodeError as error:
        raise ValueError(f"judge output is not valid JSON: {error}") from error
    if not isinstance(data, dict) or set(data) != {"output_a", "output_b", "preference", "preference_evidence"}:
        raise ValueError("judge output has unexpected top-level fields")
    if data["preference"] not in {"A", "B", "tie"} or not isinstance(data["preference_evidence"], str):
        raise ValueError("judge preference is invalid")
    for label in ("output_a", "output_b"):
        score = data[label]
        if not isinstance(score, dict) or set(score) != JUDGMENT_KEYS:
            raise ValueError(f"{label} has unexpected fields")
        if not isinstance(score["critical_preservation_failure"], bool):
            raise ValueError(f"{label} critical flag is invalid")
        failure_types = score["critical_failure_types"]
        if not isinstance(failure_types, list) or not set(failure_types) <= CRITICAL_FAILURE_TYPES:
            raise ValueError(f"{label} critical failure types are invalid")
        if score["critical_preservation_failure"] != bool(failure_types):
            raise ValueError(f"{label} critical flag and types disagree")
        scoped_fields = ("preservation", "core_structure") if category == "multilingual-core" else ("preservation", "first_pass_understanding", "core_structure", "referent_scope_terminology")
        for field in scoped_fields:
            if type(score[field]) is not int or not 1 <= score[field] <= 5:
                raise ValueError(f"{label} {field} must be an integer from 1 to 5")
        if category == "multilingual-core":
            if any(score[field] is not None for field in ("first_pass_understanding", "referent_scope_terminology", "register_preserved", "naturalness")):
                raise ValueError("multilingual-core out-of-scope scores and naturalness must be null")
        else:
            if not isinstance(score["register_preserved"], bool):
                raise ValueError(f"{label} register is invalid")
            naturalness = score["naturalness"]
            if type(naturalness) is not int or not 1 <= naturalness <= 5:
                raise ValueError(f"{label} naturalness must be an integer from 1 to 5")
        if not isinstance(score["evidence"], str):
            raise ValueError(f"{label} evidence is invalid")
    return data


def _mean(values: list[int | None]) -> float | None:
    scoped = [value for value in values if type(value) is int]
    return round(mean(scoped), 3) if scoped else None


def summarize_behavior(generations: Iterable[dict[str, Any]], judgments: Iterable[dict[str, Any]]) -> dict[str, Any]:
    generation_rows = list(generations)
    judgment_rows = list(judgments)
    summary: dict[str, Any] = {"categories": {}}
    for category in CATEGORIES:
        category_generations = [row for row in generation_rows if row["category"] == category]
        category_judgments = [row for row in judgment_rows if row["category"] == category]
        arms = sorted({row["arm"] for row in category_generations}, key=lambda value: (value != "no-skill", value))
        arm_metrics = {}
        for arm in arms:
            rows = [row for row in category_generations if row["arm"] == arm]
            failures: Counter[str] = Counter()
            for row in rows:
                failures.update(row["deterministic_score"]["failures_by_kind"])
            judged_outputs = []
            preference = Counter()
            for row in category_judgments:
                side = "output_a" if row["a_arm"] == arm else "output_b"
                judged_outputs.append(row["judgment"][side])
                preferred_arm = None
                if row["judgment"]["preference"] == "A": preferred_arm = row["a_arm"]
                elif row["judgment"]["preference"] == "B": preferred_arm = row["b_arm"]
                preference["wins" if preferred_arm == arm else "ties" if preferred_arm is None else "losses"] += 1
            arm_metrics[arm] = {
                "runs": len(rows),
                "missing_outputs": sum(not row["deterministic_score"]["output_present"] for row in rows),
                "deterministic_failures_by_kind": {kind: failures[kind] for kind in CHECK_KINDS},
                "gpt_judged": {
                    "outputs": len(judged_outputs),
                    "mean_preservation": _mean([row["preservation"] for row in judged_outputs]),
                    "mean_first_pass_understanding": _mean([row["first_pass_understanding"] for row in judged_outputs]),
                    "mean_core_structure": _mean([row["core_structure"] for row in judged_outputs]),
                    "critical_failures": sum(row["critical_preservation_failure"] for row in judged_outputs),
                    "critical_failure_types": dict(sorted(Counter(kind for row in judged_outputs for kind in row["critical_failure_types"]).items())),
                    "pair_preferences": {key: preference[key] for key in ("wins", "losses", "ties")},
                },
            }
        summary["categories"][category] = {"generations": len(category_generations), "judgments": len(category_judgments), "arms": arm_metrics}
    return summary


def _fmt(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.3f}"


def render_behavior_markdown(summary: dict[str, Any], generations: list[dict[str, Any]], judgments: list[dict[str, Any]], *, scenario_version: str, skill_ref: str, repeats: int) -> str:
    lines = [
        "# Clarity-behavior baseline", "",
        f"This injected-behavior baseline compares no skill with Crystal Clear revision `{skill_ref}`. It is not automatic-routing evidence.",
        f"Frozen scenarios: `{scenario_version}`; {repeats} repetitions per scenario and arm.", "",
        "English, Japanese, and multilingual-core evidence is reported separately; there is no pooled headline score.", "",
    ]
    labels = {"english": "English", "japanese": "Japanese", "multilingual-core": "Multilingual core"}
    for category in CATEGORIES:
        metrics = summary["categories"][category]
        lines.extend([f"## {labels[category]}", "", f"Generations: {metrics['generations']}; blind comparisons: {metrics['judgments']}.", "", "### Deterministic evidence", "", "Exact-literal checks provide preservation evidence only; they do not establish semantic correctness or clarity.", "", "| Arm | Runs | Missing outputs | Protected | Facts | Numbers | Constraints | Conditions |", "|---|---:|---:|---:|---:|---:|---:|---:|"])
        for arm, values in metrics["arms"].items():
            failures = values["deterministic_failures_by_kind"]
            lines.append(f"| {arm} | {values['runs']} | {values['missing_outputs']} | {failures['protected-string']} | {failures['fact']} | {failures['number']} | {failures['constraint']} | {failures['condition']} |")
        lines.extend(["", "### GPT-judged evidence", "", "Blind, seeded A/B judgments are model evidence and are separate from deterministic checks.", "", "| Arm | Preservation | First-pass understanding | Core structure | Critical failures | Wins | Losses | Ties |", "|---|---:|---:|---:|---:|---:|---:|---:|"])
        for arm, values in metrics["arms"].items():
            judged = values["gpt_judged"]
            prefs = judged["pair_preferences"]
            lines.append(f"| {arm} | {_fmt(judged['mean_preservation'])} | {_fmt(judged['mean_first_pass_understanding'])} | {_fmt(judged['mean_core_structure'])} | {judged['critical_failures']} | {prefs['wins']} | {prefs['losses']} | {prefs['ties']} |")
        if category == "multilingual-core":
            lines.extend(["", "Spanish, Simplified Chinese, Arabic, German, and mixed Japanese/English are assessed only for core structure and preservation. This report makes no native-naturalness claim and does not treat them as validated language profiles."])
        lines.append("")
    lines.extend(["## Human-reviewed evidence", "", "No human-reviewed evidence was collected for this baseline. Native-Japanese calibration is a later release step.", "", "## Raw evidence", "", "### Generations", "", "| Scenario | Category | Arm | Repeat | Deterministic | Result | Trace |", "|---|---|---|---:|---|---|---|"])
    for row in sorted(generations, key=lambda item: (item["scenario_id"], item["arm"], item["repeat"])):
        lines.append(f"| {row['scenario_id']} | {row['category']} | {row['arm']} | {row['repeat']} | {'pass' if row['deterministic_score']['passed'] else 'fail'} | [result]({row['result_file']}) | [trace]({row['trace_file']}) |")
    lines.extend(["", "### Blind GPT judgments", "", "| Pair | Category | Presented | Preference | Result | Trace |", "|---|---|---:|---|---|---|"])
    for row in sorted(judgments, key=lambda item: item["presentation_index"]):
        lines.append(f"| {row['pair_id']} | {row['category']} | {row['presentation_index']} | {row['judgment']['preference']} | [result]({row['result_file']}) | [trace]({row['trace_file']}) |")
    return "\n".join(lines) + "\n"


def _materialize_skill(ref: str, directory: Path) -> tuple[Path, dict[str, str]]:
    directory.mkdir(parents=True)
    hashes = {}
    for name in ("SKILL.md", "language-guides.md", "elements-of-style.md"):
        if ref == "worktree":
            content = (REPO_ROOT / name).read_text()
        else:
            content = run_command(["git", "show", f"{ref}:{name}"], cwd=REPO_ROOT) + "\n"
        path = directory / name
        path.write_text(content)
        hashes[name] = sha256(path)
    return directory / "SKILL.md", hashes


def _generation_run(*, scenario: dict[str, Any], arm: str, repeat: int, model: str, scenario_version: str, output: Path, pi_release: str, harness_revision: str) -> dict[str, Any]:
    stem = f"{scenario['id']}--{arm}--r{repeat:02d}"
    raw_dir = output / "raw" / "generations"
    raw_dir.mkdir(parents=True, exist_ok=True)
    trace_destination = raw_dir / f"{stem}.trace.jsonl"
    result_destination = raw_dir / f"{stem}.result.json"
    with tempfile.TemporaryDirectory(prefix="crystal-clear-behavior-") as tmp_value:
        root = Path(tmp_value)
        session_root = root / "pi"
        appended = None
        hashes = None
        resolved_ref = None
        if arm != "no-skill":
            resolved_ref = run_command(["git", "rev-parse", arm], cwd=REPO_ROOT) if arm != "worktree" else harness_revision
            skill, hashes = _materialize_skill(arm, session_root / "work")
            appended = root / "injected.md"
            appended.write_text("Apply the following writing skill silently to the user's task. Its relative references are available in the working directory.\n\n" + skill.read_text())
        started_at = datetime.now(timezone.utc).isoformat()
        start = time.monotonic()
        live_trace = execute_pi(prompt=scenario["prompt"], model=model, session_root=session_root, appended_instructions=appended)
        duration_ms = round((time.monotonic() - start) * 1000)
        shutil.copy2(live_trace, trace_destination)
        observation = observe_trace(trace_destination, Path("/__behavior_injection__/SKILL.md"))
    result = {
        "schema_version": 1, "scenario_version": scenario_version,
        "scenario_id": scenario["id"], "category": scenario["category"], "language": scenario["language"],
        "failure_modes": scenario["failure_modes"], "source_text": scenario["source_text"],
        "output_contract": scenario["output_contract"], "prompt": scenario["prompt"], "checks": scenario["checks"],
        "arm": arm, "repeat": repeat, "provider_model": model, "pi_version": pi_release,
        "skill_ref": None if arm == "no-skill" else arm, "skill_revision": resolved_ref,
        "skill_hash": skill_hash_record(None if hashes is None else hashes["SKILL.md"], source="none" if hashes is None else "system-injection"),
        "skill_artifact_hashes": hashes, "harness_git_revision": harness_revision,
        "started_at": started_at, "duration_ms": duration_ms,
        "random_seed": {"status": "unsupported-by-pi-cli-and-provider", "value": None},
        "system_configuration": {"thinking": "minimal", "context_files": False, "extensions": False, "prompt_templates": False, "automatic_skill_discovery": False, "tools": ["read"], "skill_body_injected": appended is not None},
        "skill_inventory": [], "session_id": observation.session_id, "final_output": observation.final_output,
        "trace_file": f"raw/generations/{trace_destination.name}", "result_file": f"raw/generations/{result_destination.name}",
    }
    result["deterministic_score"] = score_preservation(scenario, observation.final_output)
    result_destination.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    with _PRINT_LOCK: print(f"[generation] {stem}")
    return result


def _judge_prompt(scenario: dict[str, Any], output_a: str, output_b: str) -> str:
    if scenario["category"] == "multilingual-core":
        scope = "Assess only preservation and core structure. Set first_pass_understanding, referent_scope_terminology, register_preserved, and naturalness to null. Make no native-naturalness judgment."
        scoped_values = '"first_pass_understanding":null,"core_structure":1,"referent_scope_terminology":null,"register_preserved":null,"naturalness":null'
    else:
        scope = "Assess every field, including naturalness from 1 to 5."
        scoped_values = '"first_pass_understanding":1,"core_structure":1,"referent_scope_terminology":1,"register_preserved":true,"naturalness":1'
    output_shape = '{"critical_preservation_failure":false,"critical_failure_types":[],"preservation":1,' + scoped_values + ',"evidence":"concise evidence"}'
    return f'''You are a blind evaluator. Compare two anonymous revisions of the same source. Judge preservation before clarity. Do not infer which system produced either output.\n\nSOURCE:\n{scenario["source_text"]}\n\nOUTPUT CONTRACT:\n{scenario["output_contract"]}\n\nPRESERVATION REQUIREMENTS:\nPreserve facts, numbers, constraints, conditions, certainty, protected text, and requested register. {scope}\n\nOUTPUT A:\n{output_a}\n\nOUTPUT B:\n{output_b}\n\nReturn only JSON with exactly this shape:\n{{"output_a":{output_shape},"output_b":{output_shape},"preference":"A","preference_evidence":"concise evidence"}}\nAll scored fields are integers 1-5. preference is A, B, or tie. Allowed critical_failure_types: invented-fact, removed-constraint, changed-instruction, changed-certainty, corrupted-protected-text, broken-register. A critical flag is true exactly when its types list is nonempty.'''


def _judgment_run(*, assignment: dict[str, Any], scenario: dict[str, Any], by_key: dict[tuple[str, str, int], dict[str, Any]], model: str, output: Path, pi_release: str, harness_revision: str, judge_seed: int) -> dict[str, Any]:
    a = by_key[(scenario["id"], assignment["a_arm"], assignment["repeat"])]
    b = by_key[(scenario["id"], assignment["b_arm"], assignment["repeat"])]
    prompt = _judge_prompt(scenario, a["final_output"], b["final_output"])
    prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()
    stem = assignment["pair_id"]
    raw_dir = output / "raw" / "judgments"
    raw_dir.mkdir(parents=True, exist_ok=True)
    trace_destination = raw_dir / f"{stem}.trace.jsonl"
    result_destination = raw_dir / f"{stem}.result.json"
    with tempfile.TemporaryDirectory(prefix="crystal-clear-judge-") as tmp_value:
        started_at = datetime.now(timezone.utc).isoformat(); start = time.monotonic()
        live_trace = execute_pi(prompt=prompt, model=model, session_root=Path(tmp_value))
        duration_ms = round((time.monotonic() - start) * 1000)
        shutil.copy2(live_trace, trace_destination)
        observation = observe_trace(trace_destination, Path("/__judge__/SKILL.md"))
    judgment = parse_judgment(observation.final_output, scenario["category"])
    result = {
        "schema_version": 1, "scenario_version": a["scenario_version"], "pair_id": assignment["pair_id"],
        "scenario_id": scenario["id"], "category": scenario["category"], "language": scenario["language"], "repeat": assignment["repeat"],
        "presentation_index": assignment["presentation_index"], "judge_seed": judge_seed,
        "prompt_sha256": prompt_hash, "presented_output_a": a["final_output"], "presented_output_b": b["final_output"],
        "a_arm": assignment["a_arm"], "b_arm": assignment["b_arm"], "judgment": judgment,
        "raw_judge_output": observation.final_output, "provider_model": model, "pi_version": pi_release,
        "harness_git_revision": harness_revision, "started_at": started_at, "duration_ms": duration_ms,
        "system_configuration": {"thinking": "minimal", "context_files": False, "extensions": False, "prompt_templates": False, "automatic_skill_discovery": False, "tools": ["read"], "skill_body_injected": False},
        "session_id": observation.session_id, "trace_file": f"raw/judgments/{trace_destination.name}", "result_file": f"raw/judgments/{result_destination.name}",
    }
    result_destination.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    with _PRINT_LOCK: print(f"[judgment] {stem}")
    return result


def load_results(output: Path, kind: str) -> list[dict[str, Any]]:
    return [json.loads(path.read_text()) for path in sorted((output / "raw" / kind).glob("*.result.json"))]


def _retry(callable_, *, attempts: int = 3) -> dict[str, Any]:
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            return callable_()
        except Exception as error:
            last_error = error
            if attempt < attempts:
                with _PRINT_LOCK:
                    print(f"[retry {attempt}/{attempts}] {error}", file=sys.stderr)
                time.sleep(attempt)
    assert last_error is not None
    raise last_error


def _validate_trace(output: Path, row: dict[str, Any], output_field: str) -> None:
    trace = output / row["trace_file"]
    result = output / row["result_file"]
    if not trace.is_file() or not result.is_file():
        raise ValueError(f"{row.get('pair_id', row.get('scenario_id'))} has missing raw evidence")
    observation = observe_trace(trace, Path("/__validation__/SKILL.md"))
    if observation.final_output != row[output_field] or observation.session_id != row["session_id"]:
        raise ValueError(f"{row.get('pair_id', row.get('scenario_id'))} disagrees with its trace")


def validate_evidence(*, output: Path, scenario_set: dict[str, Any], generations: list[dict[str, Any]], judgments: list[dict[str, Any]], arms: list[str], repeats: int, judge_seed: int) -> None:
    scenarios = scenario_set["scenarios"]
    expected_generation = {(row["id"], arm, repeat) for row in scenarios for arm in arms for repeat in range(1, repeats + 1)}
    actual_generation = [(row["scenario_id"], row["arm"], row["repeat"]) for row in generations]
    if len(actual_generation) != len(set(actual_generation)) or set(actual_generation) != expected_generation:
        raise ValueError("generation result set is incomplete, duplicate, or stale")
    scenario_by_id = {row["id"]: row for row in scenarios}
    by_key = {(row["scenario_id"], row["arm"], row["repeat"]): row for row in generations}
    invariant_fields = ("provider_model", "pi_version", "harness_git_revision", "random_seed")
    for field in invariant_fields:
        if len({json.dumps(row[field], sort_keys=True) for row in generations}) != 1:
            raise ValueError(f"generation results mix {field}")
    skill_arm = [arm for arm in arms if arm != "no-skill"][0]
    expected_skill_revision = run_command(["git", "rev-parse", skill_arm], cwd=REPO_ROOT) if skill_arm != "worktree" else generations[0]["harness_git_revision"]
    with tempfile.TemporaryDirectory(prefix="crystal-clear-validation-") as tmp_value:
        _, expected_hashes = _materialize_skill(skill_arm, Path(tmp_value) / "skill")
    for row in generations:
        if row["scenario_version"] != scenario_set["version"]:
            raise ValueError(f"{row['scenario_id']} has stale scenario_version")
        scenario = scenario_by_id[row["scenario_id"]]
        for field in ("category", "language", "failure_modes", "source_text", "output_contract", "prompt", "checks"):
            if row[field] != scenario[field]: raise ValueError(f"{row['scenario_id']} has stale {field}")
        if row["deterministic_score"] != score_preservation(scenario, row["final_output"]):
            raise ValueError(f"{row['scenario_id']} has a stale deterministic score")
        if row["arm"] == "no-skill":
            if row["skill_ref"] is not None or row["skill_revision"] is not None or row["skill_artifact_hashes"] is not None or row["skill_hash"] != skill_hash_record(None, source="none"):
                raise ValueError(f"{row['scenario_id']} has invalid no-skill provenance")
        elif row["skill_ref"] != skill_arm or row["skill_revision"] != expected_skill_revision or row["skill_artifact_hashes"] != expected_hashes or row["skill_hash"] != skill_hash_record(expected_hashes["SKILL.md"], source="system-injection"):
            raise ValueError(f"{row['scenario_id']} has invalid skill provenance")
        _validate_trace(output, row, "final_output")
    for scenario in scenarios:
        for repeat in range(1, repeats + 1):
            prompts = {by_key[(scenario["id"], arm, repeat)]["prompt"] for arm in arms}
            contracts = {by_key[(scenario["id"], arm, repeat)]["output_contract"] for arm in arms}
            if len(prompts) != 1 or len(contracts) != 1: raise ValueError("behavior arms do not use identical prompts and contracts")
    expected_assignments = assign_blind_pairs([(row["id"], repeat) for row in scenarios for repeat in range(1, repeats + 1)], seed=judge_seed, skill_arm=[arm for arm in arms if arm != "no-skill"][0])
    expected_judgments = {(row["scenario_id"], row["repeat"]): row for row in expected_assignments}
    actual_judgments = [(row["scenario_id"], row["repeat"]) for row in judgments]
    if len(actual_judgments) != len(set(actual_judgments)) or set(actual_judgments) != set(expected_judgments):
        raise ValueError("judgment result set is incomplete, duplicate, or stale")
    judge_invariants = ("provider_model", "pi_version", "harness_git_revision", "system_configuration")
    for field in judge_invariants:
        if len({json.dumps(row[field], sort_keys=True) for row in judgments}) != 1:
            raise ValueError(f"judgments mix {field}")
    for row in judgments:
        assignment = expected_judgments[(row["scenario_id"], row["repeat"])]
        for field in ("pair_id", "presentation_index", "a_arm", "b_arm"):
            if row[field] != assignment[field]: raise ValueError(f"{row['pair_id']} has stale blind assignment")
        scenario = scenario_by_id[row["scenario_id"]]
        if row["scenario_version"] != scenario_set["version"] or row["category"] != scenario["category"] or row["language"] != scenario["language"] or row["judge_seed"] != judge_seed:
            raise ValueError(f"{row['pair_id']} has stale scenario or judge provenance")
        a = by_key[(row["scenario_id"], row["a_arm"], row["repeat"])]["final_output"]
        b = by_key[(row["scenario_id"], row["b_arm"], row["repeat"])]["final_output"]
        prompt = _judge_prompt(scenario, a, b)
        if row["presented_output_a"] != a or row["presented_output_b"] != b or row["prompt_sha256"] != hashlib.sha256(prompt.encode()).hexdigest():
            raise ValueError(f"{row['pair_id']} has stale presented evidence")
        if parse_judgment(row["raw_judge_output"], row["category"]) != row["judgment"]:
            raise ValueError(f"{row['pair_id']} has stale parsed judgment")
        trace_text = (output / row["trace_file"]).read_text()
        if any(identity in trace_text for identity in ("no-skill", skill_arm, "Crystal Clear")):
            raise ValueError(f"{row['pair_id']} judge trace exposes an arm identity")
        _validate_trace(output, row, "raw_judge_output")


def write_reports(output: Path, scenario_set: dict[str, Any], generations: list[dict[str, Any]], judgments: list[dict[str, Any]], *, arms: list[str], repeats: int, judge_seed: int) -> None:
    validate_evidence(output=output, scenario_set=scenario_set, generations=generations, judgments=judgments, arms=arms, repeats=repeats, judge_seed=judge_seed)
    summary = summarize_behavior(generations, judgments)
    summary["scenario_version"] = scenario_set["version"]; summary["arms"] = arms; summary["repeats"] = repeats; summary["judge_seed"] = judge_seed
    (output / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    (output / "SUMMARY.md").write_text(render_behavior_markdown(summary, generations, judgments, scenario_version=scenario_set["version"], skill_ref=[arm for arm in arms if arm != "no-skill"][0], repeats=repeats))


def run_behavior(args: argparse.Namespace) -> None:
    scenario_set = load_behavior_scenarios(args.scenarios)
    arms = args.arms.split(",")
    if len(arms) != 2 or "no-skill" not in arms: raise ValueError("behavior baseline requires no-skill and exactly one skill arm")
    if args.repeats != 5: raise ValueError("the frozen behavior baseline requires exactly five repeats")
    args.output.mkdir(parents=True, exist_ok=True)
    release = pi_version(); revision = git_revision(); futures = []
    generations = load_results(args.output, "generations")
    existing_generation_keys = {(row["scenario_id"], row["arm"], row["repeat"]) for row in generations}
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        for scenario in scenario_set["scenarios"]:
            for arm in arms:
                for repeat in range(1, args.repeats + 1):
                    if (scenario["id"], arm, repeat) in existing_generation_keys:
                        continue
                    futures.append(executor.submit(_retry, lambda scenario=scenario, arm=arm, repeat=repeat: _generation_run(scenario=scenario, arm=arm, repeat=repeat, model=args.model, scenario_version=scenario_set["version"], output=args.output, pi_release=release, harness_revision=revision)))
        generations.extend(future.result() for future in as_completed(futures))
    by_key = {(row["scenario_id"], row["arm"], row["repeat"]): row for row in generations}
    skill_arm = [arm for arm in arms if arm != "no-skill"][0]
    assignments = assign_blind_pairs([(row["id"], repeat) for row in scenario_set["scenarios"] for repeat in range(1, args.repeats + 1)], seed=args.judge_seed, skill_arm=skill_arm)
    scenario_by_id = {row["id"]: row for row in scenario_set["scenarios"]}; futures = []
    judgments = load_results(args.output, "judgments")
    existing_judgment_keys = {(row["scenario_id"], row["repeat"]) for row in judgments}
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        for assignment in assignments:
            if (assignment["scenario_id"], assignment["repeat"]) in existing_judgment_keys:
                continue
            futures.append(executor.submit(_retry, lambda assignment=assignment: _judgment_run(assignment=assignment, scenario=scenario_by_id[assignment["scenario_id"]], by_key=by_key, model=args.judge_model or args.model, output=args.output, pi_release=release, harness_revision=revision, judge_seed=args.judge_seed)))
        judgments.extend(future.result() for future in as_completed(futures))
    write_reports(args.output, scenario_set, generations, judgments, arms=arms, repeats=args.repeats, judge_seed=args.judge_seed)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenarios", type=Path, default=DEFAULT_SCENARIOS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--arms", default="no-skill,178eaf8")
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--judge-seed", type=int, default=178)
    parser.add_argument("--model", default="openai-codex/gpt-5.6-sol")
    parser.add_argument("--judge-model")
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--report-only", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args(); arms = args.arms.split(",")
    if args.report_only:
        scenario_set = load_behavior_scenarios(args.scenarios)
        write_reports(args.output, scenario_set, load_results(args.output, "generations"), load_results(args.output, "judgments"), arms=arms, repeats=args.repeats, judge_seed=args.judge_seed)
    else:
        run_behavior(args)
    print(args.output / "SUMMARY.md")


if __name__ == "__main__": main()
