#!/usr/bin/env python3
"""Run or re-report the end-to-end headless Pi smoke evaluation."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from evals.evaluation import (
    CRITICAL_FAILURE_TYPES,
    activation_record,
    observe_trace,
    parse_preservation_judgment,
    render_markdown,
    score_result,
    skill_hash_record,
    summarize_results,
)
from evals.skill_artifacts import materialize_skill_artifacts


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SCENARIOS = Path(__file__).resolve().parent / "smoke-scenarios.json"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "results" / "smoke"
CURRENT_SKILL_REF = "178eaf8"
AGENT_DIR = Path.home() / ".pi" / "agent"
DEFAULT_DISCOVERED_SKILL = (
    AGENT_DIR / "skills" / "crystal-clear" / "SKILL.md"
)


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


def find_pi_module_index() -> Path:
    pi_executable = shutil.which("pi")
    if pi_executable is None:
        raise FileNotFoundError("pi executable not found")
    adjacent = Path(pi_executable).resolve().parent / "index.js"
    if adjacent.is_file():
        return adjacent
    npm_root = Path(run_command(["npm", "root", "-g"]))
    installed = npm_root / "@earendil-works" / "pi-coding-agent" / "dist" / "index.js"
    if installed.is_file():
        return installed
    raise FileNotFoundError("could not locate the installed Pi module index")


def normal_skill_inventory(
    cwd: Path,
    agent_dir: Path = AGENT_DIR,
    home_dir: Path | None = None,
) -> list[dict[str, Any]]:
    pi_index = find_pi_module_index()
    script = Path(__file__).resolve().parent / "list_pi_skills.mjs"
    environment = os.environ.copy()
    if home_dir is not None:
        home_dir.mkdir(parents=True, exist_ok=True)
        environment["HOME"] = str(home_dir)
    completed = subprocess.run(
        [
            "node",
            str(script),
            str(pi_index),
            str(cwd),
            str(agent_dir),
        ],
        check=True,
        capture_output=True,
        text=True,
        env=environment,
    )
    return json.loads(completed.stdout)


def materialize_skill(ref: str, destination: Path) -> Path:
    skill, _ = materialize_skill_artifacts(ref, destination)
    return skill


def load_scenarios(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text())
    if not data.get("version") or not data.get("routing") or not data.get("behavior"):
        raise ValueError("scenario file must define version, routing, and behavior")
    if any(not scenario.get("source_text") for scenario in data["behavior"]):
        raise ValueError("every behavior smoke scenario must define source_text")
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
    appended_instructions: Path | None = None,
    normal_skill_discovery: bool = False,
    agent_dir: Path | None = None,
) -> Path:
    provider, model_id = split_model(model)
    sessions = session_root / "sessions"
    work = session_root / "work"
    sessions.mkdir(parents=True, exist_ok=True)
    work.mkdir(parents=True, exist_ok=True)
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
    ]
    if not normal_skill_discovery:
        command.append("--no-skills")
    command.extend(["--tools", "read"])
    if appended_instructions is not None:
        command.extend(["--append-system-prompt", str(appended_instructions)])

    environment = os.environ.copy()
    if agent_dir is not None:
        isolated_home = agent_dir / ".isolated-home"
        isolated_home.mkdir(parents=True, exist_ok=True)
        environment["PI_CODING_AGENT_DIR"] = str(agent_dir)
        environment["HOME"] = str(isolated_home)
    completed = subprocess.run(
        [*command, prompt],
        cwd=work,
        env=environment,
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
    discovered_skill_path: Path,
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
        appended_instructions: Path | None = None
        injected_skill: dict[str, Any] | None = None
        normal_skill_discovery = kind == "routing"
        observed_skill_path = (
            discovered_skill_path if kind == "routing" else worktree_skill
        )
        session_root = tmp / "pi"
        pi_cwd = session_root / "work"
        pi_cwd.mkdir(parents=True)
        skill_inventory = (
            normal_skill_inventory(pi_cwd) if normal_skill_discovery else []
        )

        if kind == "routing":
            if scenario["invocation"] == "direct":
                prompt = f"/skill:crystal-clear {prompt}"
        elif arm != "no-skill":
            ref = CURRENT_SKILL_REF if arm == "current-skill" else "worktree"
            source, artifact_hashes = materialize_skill_artifacts(ref, pi_cwd)
            appended_instructions = tmp / f"{arm}-system-prompt.md"
            appended_instructions.write_text(
                "Apply the following writing skill to the user's task. Its relative references are available in the working directory.\n\n"
                + source.read_text()
            )
            injected_skill = {
                "condition": arm,
                "source_ref": ref,
                "sha256": sha256(source),
                "artifact_hashes": artifact_hashes,
            }

        started_at = datetime.now(timezone.utc).isoformat()
        start = time.monotonic()
        live_trace = execute_pi(
            prompt=prompt,
            model=model,
            session_root=session_root,
            appended_instructions=appended_instructions,
            normal_skill_discovery=normal_skill_discovery,
        )
        duration_ms = round((time.monotonic() - start) * 1000)
        shutil.copy2(live_trace, trace_destination)
        observation = observe_trace(trace_destination, observed_skill_path)

    loaded_skill_hash = (
        injected_skill["sha256"]
        if injected_skill is not None
        else (sha256(discovered_skill_path) if kind == "routing" else None)
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
            "automatic_skill_discovery": normal_skill_discovery,
            "tools": ["read"],
            "skill_body_injected": appended_instructions is not None,
        },
        "skill_inventory": skill_inventory,
        "skill_hash": skill_hash_record(
            loaded_skill_hash,
            source=(
                "system-injection"
                if injected_skill is not None
                else ("normal-discovery" if kind == "routing" else "none")
            ),
        ),
        "injected_skill": injected_skill,
        "session_id": observation.session_id,
        "activation": activation_record(
            observation, skill_body_injected=appended_instructions is not None
        ),
        "final_output": observation.final_output,
        "trace_file": relative_trace_path(output, trace_destination),
    }
    result["score"] = score_result(result)
    result_destination.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    return result


def judge_candidate_preservation(
    *,
    scenario: dict[str, Any],
    candidate: dict[str, Any],
    model: str,
    output: Path,
    pi_release: str,
    revision: str,
) -> dict[str, Any]:
    """Judge critical preservation separately from deterministic string checks."""
    prompt = f'''Judge whether the revision has a critical preservation failure. A critical failure invents or removes a fact, changes a constraint or instruction, strengthens or weakens certainty, corrupts protected text, or breaks the requested register. Judge preservation only, not writing quality.

REQUEST:
{scenario["prompt"]}

SOURCE:
{scenario["source_text"]}

REVISION:
{candidate["final_output"]}

Return only JSON with exactly this shape:
{{"critical_preservation_failure":false,"critical_failure_types":[],"evidence":"concise evidence"}}
Allowed failure types: {", ".join(sorted(CRITICAL_FAILURE_TYPES))}. The flag must be true exactly when the list is nonempty.'''
    raw_dir = output / "raw"
    trace_destination = raw_dir / f"{scenario['id']}--candidate-skill.judgment.trace.jsonl"
    judgment_destination = raw_dir / f"{scenario['id']}--candidate-skill.judgment.json"
    with tempfile.TemporaryDirectory(prefix="crystal-clear-smoke-judge-") as tmp_value:
        started_at = datetime.now(timezone.utc).isoformat()
        start = time.monotonic()
        live_trace = execute_pi(
            prompt=prompt,
            model=model,
            session_root=Path(tmp_value),
        )
        duration_ms = round((time.monotonic() - start) * 1000)
        shutil.copy2(live_trace, trace_destination)
        observation = observe_trace(trace_destination, Path("/__smoke_judge__/SKILL.md"))
    judgment = parse_preservation_judgment(observation.final_output)
    record = {
        "schema_version": 1,
        "scenario_version": candidate["scenario_version"],
        "scenario_id": scenario["id"],
        "kind": "preservation-judgment",
        "arm": "candidate-skill",
        "provider_model": model,
        "pi_version": pi_release,
        "git_revision": revision,
        "started_at": started_at,
        "duration_ms": duration_ms,
        "session_id": observation.session_id,
        "judgment": judgment,
        "raw_judge_output": observation.final_output,
        "trace_file": relative_trace_path(output, trace_destination),
    }
    judgment_destination.write_text(
        json.dumps(record, indent=2, ensure_ascii=False) + "\n"
    )
    candidate["preservation_judgment"] = judgment
    candidate["preservation_judgment_file"] = relative_trace_path(
        output, judgment_destination
    )
    candidate["preservation_judgment_trace_file"] = relative_trace_path(
        output, trace_destination
    )
    candidate_path = raw_dir / f"{scenario['id']}--candidate-skill.result.json"
    candidate_path.write_text(json.dumps(candidate, indent=2, ensure_ascii=False) + "\n")
    return candidate


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


def run_smoke(
    scenarios_path: Path,
    output: Path,
    model: str,
) -> list[dict[str, Any]]:
    scenarios = load_scenarios(scenarios_path)
    discovered_skill_path = DEFAULT_DISCOVERED_SKILL
    if not discovered_skill_path.is_file():
        raise FileNotFoundError(
            "normal Pi discovery requires an installed crystal-clear skill at "
            f"{discovered_skill_path}"
        )
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
                discovered_skill_path=discovered_skill_path,
            )
        )
    behavior = scenarios["behavior"][0]
    candidate: dict[str, Any] | None = None
    for arm in ("no-skill", "current-skill", "candidate-skill"):
        result = run_one(
            scenario=behavior,
            kind="behavior",
            arm=arm,
            model=model,
            scenario_version=scenarios["version"],
            output=output,
            pi_release=release,
            revision=revision,
            discovered_skill_path=discovered_skill_path,
        )
        results.append(result)
        if arm == "candidate-skill":
            candidate = result
    assert candidate is not None
    judge_candidate_preservation(
        scenario=behavior,
        candidate=candidate,
        model=model,
        output=output,
        pi_release=release,
        revision=revision,
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
