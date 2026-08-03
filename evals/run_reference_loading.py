#!/usr/bin/env python3
"""Verify Elements of Style loading policy through live headless Pi traces."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from evals.evaluation import observe_trace
from evals.run_behavior import _materialize_skill
from evals.run_smoke import execute_pi, git_revision, pi_version

EVALS_ROOT = Path(__file__).resolve().parent
DEFAULT_SCENARIOS = EVALS_ROOT / "reference-loading-scenarios.json"
ELEMENTS_PREFIX = "references/elements-of-style/"


def elements_read_paths(trace: Path) -> list[str]:
    paths: list[str] = []
    for line in trace.read_text().splitlines():
        event = json.loads(line)
        message = event.get("message")
        if not isinstance(message, dict) or message.get("role") != "assistant":
            continue
        for part in message.get("content", []):
            if not isinstance(part, dict) or part.get("type") != "toolCall" or part.get("name") != "read":
                continue
            value = str(part.get("arguments", {}).get("path", "")).replace("\\", "/")
            marker = value.find(ELEMENTS_PREFIX)
            if marker >= 0:
                relative = value[marker:]
                if relative not in paths:
                    paths.append(relative)
    return paths


def validate_policy_result(scenario: dict[str, Any], reads: list[str]) -> None:
    expected = scenario["expected_reference_reads"]
    if reads != expected:
        raise ValueError(f"{scenario['id']} read {reads}, expected {expected}")
    if scenario["mode"].startswith("targeted"):
        selected = [path for path in reads if path != f"{ELEMENTS_PREFIX}index.md"]
        if len(selected) > 2 or f"{ELEMENTS_PREFIX}source.md" in reads:
            raise ValueError(f"{scenario['id']} violated targeted loading limits")


def run_scenario(
    scenario: dict[str, Any], *, scenario_version: str, model: str, output: Path
) -> dict[str, Any]:
    raw = output / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    trace_path = raw / f"{scenario['id']}.trace.jsonl"
    result_path = raw / f"{scenario['id']}.result.json"
    with tempfile.TemporaryDirectory(prefix="crystal-clear-reference-loading-") as tmp:
        root = Path(tmp)
        session_root = root / "pi"
        skill, hashes = _materialize_skill("worktree", session_root / "work")
        instructions = root / "instructions.md"
        instructions.write_text(
            "Apply the following writing skill silently to the user's task. Its relative references are available in the working directory.\n\n"
            + skill.read_text()
        )
        live = execute_pi(
            prompt=scenario["prompt"],
            model=model,
            session_root=session_root,
            appended_instructions=instructions,
        )
        shutil.copy2(live, trace_path)
        observation = observe_trace(trace_path, Path("/__reference_loading__/SKILL.md"))
    reads = elements_read_paths(trace_path)
    validate_policy_result(scenario, reads)
    result = {
        "schema_version": 1,
        "scenario_version": scenario_version,
        "scenario_id": scenario["id"],
        "mode": scenario["mode"],
        "language": scenario["language"],
        "prompt": scenario["prompt"],
        "expected_reference_reads": scenario["expected_reference_reads"],
        "observed_reference_reads": reads,
        "final_output": observation.final_output,
        "provider_model": model,
        "pi_version": pi_version(),
        "harness_git_revision": git_revision(),
        "skill_artifact_hashes": hashes,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "trace_file": f"raw/{trace_path.name}",
    }
    result_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenarios", type=Path, default=DEFAULT_SCENARIOS)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default="openai-codex/gpt-5.6-sol")
    args = parser.parse_args()
    fixture = json.loads(args.scenarios.read_text())
    scenario_version = fixture.get("version")
    if not isinstance(scenario_version, str) or not scenario_version:
        raise ValueError("reference-loading fixture must declare a version")
    results = [
        run_scenario(
            row,
            scenario_version=scenario_version,
            model=args.model,
            output=args.output,
        )
        for row in fixture["scenarios"]
    ]
    summary = {
        "schema_version": 1,
        "scenario_version": scenario_version,
        "runs": len(results),
        "passed": len(results),
        "results": [row["scenario_id"] for row in results],
    }
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(args.output / "summary.json")


if __name__ == "__main__":
    main()
