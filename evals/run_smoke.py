#!/usr/bin/env python3
"""Run or re-report the end-to-end headless Pi smoke evaluation."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from evals.evaluation import (
    observe_trace,
    render_markdown,
    score_result,
    summarize_results,
)


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SCENARIOS = Path(__file__).resolve().parent / "smoke-scenarios.json"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "results" / "smoke"
CURRENT_SKILL_REF = "178eaf8"


def run_command(command: list[str], cwd: Path | None = None) -> str:
    completed = subprocess.run(
        command,
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def materialize_skill(ref: str, destination: Path) -> Path:
    if ref == "worktree":
        source = REPO_ROOT / "SKILL.md"
        shutil.copy2(source, destination)
        return destination
    content = run_command(["git", "show", f"{ref}:SKILL.md"], cwd=REPO_ROOT)
    destination.write_text(content + "\n")
    return destination


def load_scenarios(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text())
    if not data.get("version") or not data.get("routing") or not data.get("behavior"):
        raise ValueError("scenario file must define version, routing, and behavior")
    return data


def pi_version() -> str:
    return run_command(["pi", "--version"])


def git_revision() -> str:
    return run_command(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT)


def split_model(value: str) -> tuple[str, str]:
    if "/" not in value:
        raise ValueError("model must use provider/model format")
    return tuple(value.split("/", 1))  # type: ignore[return-value]


def execute_pi(
    *,
    prompt: str,
    model: str,
    session_root: Path,
    skill_path: Path | None = None,
    appended_instructions: Path | None = None,
) -> Path:
    provider, model_id = split_model(model)
    sessions = session_root / "sessions"
    work = session_root / "work"
    sessions.mkdir(parents=True)
    work.mkdir(parents=True)
    command = [
        "pi",
        "--mode",
        "json",
        "--print",
        "--provider",
        provider,
        "--model",
        model_id,
        "--thinking",
        "minimal",
        "--session-dir",
        str(sessions),
        "--no-context-files",
        "--no-extensions",
        "--no-prompt-templates",
        "--no-skills",
        "--tools",
        "read",
    ]
    if skill_path is not None:
        command.extend(["--skill", str(skill_path)])
    if appended_instructions is not None:
        command.extend(["--append-system-prompt", str(appended_instructions)])

    completed = subprocess.run(
        [*command, prompt],
        cwd=work,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.returncode:
        raise RuntimeError(f"Pi failed ({completed.returncode}): {completed.stderr.strip()}")
    traces = sorted(sessions.glob("*.jsonl"))
    if len(traces) != 1:
        raise RuntimeError(f"expected one Pi session trace, found {len(traces)}")
    return traces[0]


def relative_trace_path(output: Path, trace: Path) -> str:
    return trace.relative_to(output).as_posix()


def run_one(
    *,
    scenario: dict[str, Any],
    kind: str,
    arm: str,
    model: str,
    scenario_version: str,
    output: Path,
    pi_release: str,
    revision: str,
) -> dict[str, Any]:
    run_id = f"{scenario['id']}--{arm}"
    raw_dir = output / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    trace_destination = raw_dir / f"{run_id}.trace.jsonl"
    result_destination = raw_dir / f"{run_id}.result.json"

    with tempfile.TemporaryDirectory(prefix="crystal-clear-smoke-") as tmp_value:
        tmp = Path(tmp_value)
        worktree_skill = REPO_ROOT / "SKILL.md"
        prompt = scenario["prompt"]
        skill_path: Path | None = None
        appended_instructions: Path | None = None
        injected_skill: dict[str, Any] | None = None

        if kind == "routing":
            skill_path = worktree_skill
            if scenario["invocation"] == "direct":
                prompt = f"/skill:crystal-clear {prompt}"
        elif arm != "no-skill":
            ref = CURRENT_SKILL_REF if arm == "current-skill" else "worktree"
            source = materialize_skill(ref, tmp / f"{arm}.md")
            appended_instructions = tmp / f"{arm}-system-prompt.md"
            appended_instructions.write_text(
                "Apply the following writing skill to the user's task.\n\n"
                + source.read_text()
            )
            injected_skill = {
                "condition": arm,
                "source_ref": ref,
                "sha256": sha256(source),
            }

        started_at = datetime.now(timezone.utc).isoformat()
        start = time.monotonic()
        live_trace = execute_pi(
            prompt=prompt,
            model=model,
            session_root=tmp / "pi",
            skill_path=skill_path,
            appended_instructions=appended_instructions,
        )
        duration_ms = round((time.monotonic() - start) * 1000)
        shutil.copy2(live_trace, trace_destination)
        observation = observe_trace(trace_destination, worktree_skill)

    skill_inventory = []
    if kind == "routing":
        skill_inventory.append(
            {
                "name": "crystal-clear",
                "path": str(worktree_skill.resolve()),
                "sha256": sha256(worktree_skill),
            }
        )

    result: dict[str, Any] = {
        "schema_version": 1,
        "scenario_version": scenario_version,
        "scenario_id": scenario["id"],
        "kind": kind,
        "arm": arm,
        "repeat": 1,
        "prompt": scenario["prompt"],
        "expected_activation": scenario.get("expected_activation"),
        "protected_strings": scenario.get("protected_strings", []),
        "provider_model": model,
        "pi_version": pi_release,
        "git_revision": revision,
        "started_at": started_at,
        "duration_ms": duration_ms,
        "system_configuration": {
            "thinking": "minimal",
            "context_files": False,
            "extensions": False,
            "prompt_templates": False,
            "automatic_skill_discovery": False,
            "tools": ["read"],
            "skill_body_injected": appended_instructions is not None,
        },
        "skill_inventory": skill_inventory,
        "injected_skill": injected_skill,
        "session_id": observation.session_id,
        "activation": {
            "automatic": observation.automatic_activation,
            "skill_loaded": observation.skill_loaded,
            "source": observation.activation_source,
        },
        "final_output": observation.final_output,
        "trace_file": relative_trace_path(output, trace_destination),
    }
    result["score"] = score_result(result)
    result_destination.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    return result


def load_raw_results(output: Path) -> list[dict[str, Any]]:
    return [
        json.loads(path.read_text())
        for path in sorted((output / "raw").glob("*.result.json"))
    ]


def write_reports(output: Path, results: list[dict[str, Any]]) -> None:
    output.mkdir(parents=True, exist_ok=True)
    summary = summarize_results(results)
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (output / "SUMMARY.md").write_text(render_markdown(summary, results))


def run_smoke(scenarios_path: Path, output: Path, model: str) -> list[dict[str, Any]]:
    scenarios = load_scenarios(scenarios_path)
    release = pi_version()
    revision = git_revision()
    results: list[dict[str, Any]] = []
    for scenario in scenarios["routing"]:
        results.append(
            run_one(
                scenario=scenario,
                kind="routing",
                arm=scenario["invocation"],
                model=model,
                scenario_version=scenarios["version"],
                output=output,
                pi_release=release,
                revision=revision,
            )
        )
    behavior = scenarios["behavior"][0]
    for arm in ("no-skill", "current-skill", "candidate-skill"):
        results.append(
            run_one(
                scenario=behavior,
                kind="behavior",
                arm=arm,
                model=model,
                scenario_version=scenarios["version"],
                output=output,
                pi_release=release,
                revision=revision,
            )
        )
    write_reports(output, results)
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenarios", type=Path, default=DEFAULT_SCENARIOS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--model", default="openai-codex/gpt-5.6-sol")
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="regenerate summaries from existing raw result records",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.report_only:
        results = load_raw_results(args.output)
        if not results:
            raise SystemExit(f"no raw result records under {args.output / 'raw'}")
        write_reports(args.output, results)
    else:
        run_smoke(args.scenarios, args.output, args.model)
    print(args.output / "SUMMARY.md")


if __name__ == "__main__":
    main()
