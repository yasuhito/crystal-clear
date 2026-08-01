#!/usr/bin/env python3
"""Run and report the frozen Crystal Clear automatic-routing baseline."""

from __future__ import annotations

import argparse
import json
import re
import sys
import shutil
import subprocess
import tempfile
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterable

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from evals.evaluation import activation_record, observe_trace, skill_hash_record
from evals.run_smoke import (
    AGENT_DIR,
    execute_pi,
    git_revision,
    normal_skill_inventory,
    pi_version,
    run_command,
    sha256,
)


REPO_ROOT = Path(__file__).resolve().parent.parent
EVALS_ROOT = Path(__file__).resolve().parent
DEFAULT_SCENARIOS = EVALS_ROOT / "routing-scenarios.json"
DEFAULT_MANIFEST = EVALS_ROOT / "fixtures" / "skills-manifest.json"
DEFAULT_OUTPUT = EVALS_ROOT / "results" / "routing" / "178eaf8"
REQUIRED_CATEGORIES = {
    "explicit-request",
    "complex-communication",
    "unrelated-control",
    "boundary",
}
_PRINT_LOCK = threading.Lock()


@dataclass(frozen=True)
class RoutingEnvironment:
    agent_dir: Path
    inventory: list[dict[str, Any]]
    snapshot: str
    role: str


def load_routing_scenarios(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text())
    scenarios = data.get("scenarios", [])
    if len(scenarios) != 40:
        raise ValueError("routing scenario set must contain exactly 40 scenarios")
    required = {
        "id",
        "language",
        "category",
        "split",
        "expected_activation",
        "rationale",
        "prompt",
    }
    if len({row.get("id") for row in scenarios}) != 40:
        raise ValueError("routing scenario ids must be unique")
    for row in scenarios:
        missing = required - row.keys()
        if missing:
            raise ValueError(f"scenario {row.get('id')} is missing {sorted(missing)}")
        if row["category"] not in REQUIRED_CATEGORIES:
            raise ValueError(f"scenario {row['id']} has an unknown category")
        if row["split"] not in {"train", "held-out"}:
            raise ValueError(f"scenario {row['id']} has an unknown split")
        if not isinstance(row["expected_activation"], bool):
            raise ValueError(f"scenario {row['id']} must declare boolean activation")
        if row["split"] == "held-out" and not row.get("paraphrase_of"):
            raise ValueError(f"held-out scenario {row['id']} must name its source paraphrase")
    category_counts = Counter(row["category"] for row in scenarios)
    if category_counts != Counter({category: 10 for category in REQUIRED_CATEGORIES}):
        raise ValueError("routing scenario set must contain 10 scenarios per category")
    if sum(row["split"] == "held-out" for row in scenarios) != 12:
        raise ValueError("routing scenario set must reserve exactly 30% held out")
    return data


def _copy_auth(agent_dir: Path) -> None:
    agent_dir.mkdir(parents=True, exist_ok=True)
    auth = AGENT_DIR / "auth.json"
    if auth.exists():
        (agent_dir / "auth.json").symlink_to(auth)


def _materialize_baseline_skill(skill_ref: str, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for name in ("SKILL.md", "language-guides.md", "elements-of-style.md"):
        content = run_command(["git", "show", f"{skill_ref}:{name}"], cwd=REPO_ROOT)
        (destination / name).write_text(content + "\n")


def _safe_skill_name(name: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip("-")
    if not value:
        raise ValueError(f"cannot materialize skill name {name!r}")
    return value


def build_pinned_agent(
    destination: Path, *, skill_ref: str, manifest_path: Path
) -> tuple[list[dict[str, Any]], str]:
    _copy_auth(destination)
    skills_root = destination / "skills"
    skills_root.mkdir()
    manifest = json.loads(manifest_path.read_text())
    for entry in manifest["skills"]:
        target = skills_root / _safe_skill_name(entry["name"])
        if entry["source"] == "git-ref":
            _materialize_baseline_skill(skill_ref, target)
        else:
            source = manifest_path.parent / entry["path"]
            shutil.copytree(source.parent, target)
    inventory = normal_skill_inventory(
        destination / "work", destination, destination / ".isolated-home"
    )
    expected = sorted(entry["name"] for entry in manifest["skills"])
    actual = sorted(item["name"] for item in inventory)
    if actual != expected:
        raise RuntimeError(f"pinned inventory mismatch: expected {expected}, got {actual}")
    return inventory, manifest["version"]


def build_installed_agent(
    destination: Path, *, skill_ref: str
) -> tuple[list[dict[str, Any]], str]:
    """Snapshot the owner's enabled inventory, replacing Crystal Clear with skill_ref."""
    _copy_auth(destination)
    source_work = destination.parent / "installed-inventory-work"
    source_work.mkdir()
    source_inventory = normal_skill_inventory(source_work, AGENT_DIR)
    skills_root = destination / "skills"
    skills_root.mkdir()
    seen: set[str] = set()
    for item in source_inventory:
        name = item["name"]
        if name in seen:
            raise RuntimeError(f"resolved installed inventory contains duplicate {name!r}")
        seen.add(name)
        target = skills_root / _safe_skill_name(name)
        if name == "crystal-clear":
            _materialize_baseline_skill(skill_ref, target)
        else:
            shutil.copytree(Path(item["path"]).resolve().parent, target)
    executed_inventory = normal_skill_inventory(
        destination / "work", destination, destination / ".isolated-home"
    )
    expected = sorted(item["name"] for item in source_inventory)
    actual = sorted(item["name"] for item in executed_inventory)
    if actual != expected:
        raise RuntimeError(f"installed inventory mismatch: expected {expected}, got {actual}")
    snapshot_inventory = []
    executed_by_name = {item["name"]: item for item in executed_inventory}
    for item in source_inventory:
        recorded = dict(item)
        executed = executed_by_name[item["name"]]
        recorded["sha256"] = executed["sha256"]
        if item["name"] == "crystal-clear":
            recorded["path"] = f"git:{skill_ref}:SKILL.md"
        snapshot_inventory.append(recorded)
    snapshot_id = "installed-" + inventory_sha256(snapshot_inventory)[:12]
    return snapshot_inventory, snapshot_id


def inventory_sha256(inventory: list[dict[str, Any]]) -> str:
    import hashlib

    canonical = json.dumps(inventory, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(canonical).hexdigest()


def _normalized_text(value: str) -> str:
    return " ".join(value.casefold().split())


def classify_selection_outcome(
    activated: bool, input_text: str | None, final_output: str
) -> str:
    if not activated:
        return "not-selected"
    if input_text is None:
        return "selected-effect-not-deterministically-assessed"
    source = _normalized_text(input_text)
    output = _normalized_text(final_output)
    similarity = SequenceMatcher(None, source, output).ratio()
    if source == output or similarity >= 0.98:
        return "selected-with-little-visible-change"
    return "selected-with-visible-change"


def _rate(numerator: int, denominator: int) -> float | None:
    return round(numerator / denominator, 4) if denominator else None


def _metric_group(rows: list[dict[str, Any]]) -> dict[str, Any]:
    positives = [row for row in rows if row["expected_activation"]]
    negatives = [row for row in rows if not row["expected_activation"]]
    true_positives = sum(row["activation"]["automatic"] for row in positives)
    false_positives = sum(row["activation"]["automatic"] for row in negatives)
    selected = true_positives + false_positives
    return {
        "runs": len(rows),
        "positive_runs": len(positives),
        "negative_runs": len(negatives),
        "true_positives": true_positives,
        "false_positives": false_positives,
        "recall": _rate(true_positives, len(positives)),
        "precision": _rate(true_positives, selected),
        "false_positive_rate": _rate(false_positives, len(negatives)),
        "activation_rate": _rate(
            sum(row["activation"]["automatic"] for row in rows), len(rows)
        ),
    }


def summarize_routing_results(results: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = list(results)
    return {
        "runs": len(rows),
        "overall": _metric_group(rows),
        "categories": {
            category: _metric_group([row for row in rows if row["category"] == category])
            for category in sorted(REQUIRED_CATEGORIES)
        },
        "splits": {
            split: _metric_group([row for row in rows if row["split"] == split])
            for split in ("train", "held-out")
        },
        "languages": {
            language: _metric_group([row for row in rows if row["language"] == language])
            for language in sorted({row["language"] for row in rows})
        },
        "selection_outcomes": dict(
            sorted(Counter(row["selection_outcome"] for row in rows).items())
        ),
    }


def _format_rate(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.1%}"


def render_routing_markdown(
    *,
    summary: dict[str, Any],
    results: list[dict[str, Any]],
    environment: str,
    inventory_role: str,
    scenario_version: str,
    skill_ref: str,
    inventory_snapshot: str,
) -> str:
    overall = summary["overall"]
    lines = [
        f"# Automatic activation baseline — {environment}",
        "",
        f"- Inventory role: **{inventory_role}**",
        f"- Inventory snapshot: `{inventory_snapshot}`",
        f"- Frozen scenarios: `{scenario_version}` (40 scenarios; 12 held-out)",
        f"- Baseline skill revision: `{skill_ref}`",
        f"- Runs: {summary['runs']}",
        f"- Recall across expected-positive runs: {_format_rate(overall['recall'])} ({overall['true_positives']}/{overall['positive_runs']})",
        f"- Precision: {_format_rate(overall['precision'])}",
        f"- False-positive rate across all expected-negative runs: {_format_rate(overall['false_positive_rate'])} ({overall['false_positives']}/{overall['negative_runs']})",
        (
            "- Unrelated-control false-positive rate: "
            f"{_format_rate(summary['categories']['unrelated-control']['false_positive_rate'])} "
            f"({summary['categories']['unrelated-control']['false_positives']}/"
            f"{summary['categories']['unrelated-control']['negative_runs']})"
        ),
        "",
    ]
    if inventory_role == "formal":
        lines.append("This pinned inventory is the only result eligible for later pass/fail comparison.")
    else:
        lines.append("This complete installed inventory is ecological reference only and is not eligible for pass/fail comparison.")
    lines.extend([
        "",
        "## Category results",
        "",
        "| Category | Runs | Recall | Precision | False-positive rate | Activation rate |",
        "|---|---:|---:|---:|---:|---:|",
    ])
    for category, metrics in summary["categories"].items():
        lines.append(
            f"| {category} | {metrics['runs']} | {_format_rate(metrics['recall'])} | "
            f"{_format_rate(metrics['precision'])} | {_format_rate(metrics['false_positive_rate'])} | "
            f"{_format_rate(metrics['activation_rate'])} |"
        )
    lines.extend([
        "",
        "## Frozen split results",
        "",
        "| Split | Runs | Recall | False-positive rate |",
        "|---|---:|---:|---:|",
    ])
    for split, metrics in summary["splits"].items():
        lines.append(
            f"| {split} | {metrics['runs']} | {_format_rate(metrics['recall'])} | "
            f"{_format_rate(metrics['false_positive_rate'])} |"
        )
    lines.extend([
        "",
        "## Selection outcomes",
        "",
        "`not-selected` means Crystal Clear was not read. `selected-with-little-visible-change` means it was read but the final output was identical or at least 98% similar to the supplied source text. Generated outputs without a source text are reported as `selected-effect-not-deterministically-assessed`; the report does not infer a behavioral effect merely from selection.",
        "",
    ])
    for outcome, count in summary["selection_outcomes"].items():
        lines.append(f"- {outcome}: {count}")
    lines.extend([
        "",
        "## Raw runs",
        "",
        "| Scenario | Category | Split | Repeat | Expected | Observed | Outcome | Trace | Result |",
        "|---|---|---|---:|---|---|---|---|---|",
    ])
    for row in sorted(results, key=lambda item: (item["scenario_id"], item["repeat"])):
        trace = row["trace_file"]
        result = row["result_file"]
        lines.append(
            f"| {row['scenario_id']} | {row['category']} | {row['split']} | {row['repeat']} | "
            f"{str(row['expected_activation']).lower()} | {str(row['activation']['automatic']).lower()} | "
            f"{row['selection_outcome']} | [trace]({trace}) | [result]({result}) |"
        )
    return "\n".join(lines) + "\n"


def _run_one(
    *,
    scenario: dict[str, Any],
    repeat: int,
    environment: str,
    inventory_role: str,
    inventory_snapshot: str,
    inventory: list[dict[str, Any]],
    agent_dir: Path,
    model: str,
    skill_ref: str,
    skill_revision: str,
    scenario_version: str,
    output: Path,
    pi_release: str,
    harness_revision: str,
) -> dict[str, Any]:
    run_stem = f"{scenario['id']}--r{repeat:02d}"
    environment_output = output / environment
    raw_dir = environment_output / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    trace_destination = raw_dir / f"{run_stem}.trace.jsonl"
    result_destination = raw_dir / f"{run_stem}.result.json"
    with tempfile.TemporaryDirectory(prefix=f"crystal-clear-{environment}-") as tmp_value:
        session_root = Path(tmp_value)
        started_at = datetime.now(timezone.utc).isoformat()
        start = time.monotonic()
        live_trace = execute_pi(
            prompt=scenario["prompt"],
            model=model,
            session_root=session_root,
            normal_skill_discovery=True,
            agent_dir=agent_dir,
        )
        duration_ms = round((time.monotonic() - start) * 1000)
        shutil.copy2(live_trace, trace_destination)
        observed_skill = agent_dir / "skills" / "crystal-clear" / "SKILL.md"
        observation = observe_trace(trace_destination, observed_skill)
    result: dict[str, Any] = {
        "schema_version": 1,
        "scenario_version": scenario_version,
        "scenario_id": scenario["id"],
        "language": scenario["language"],
        "category": scenario["category"],
        "split": scenario["split"],
        "paraphrase_of": scenario.get("paraphrase_of"),
        "rationale": scenario["rationale"],
        "expected_activation": scenario["expected_activation"],
        "prompt": scenario["prompt"],
        "input_text": scenario.get("input_text"),
        "repeat": repeat,
        "environment": environment,
        "inventory_role": inventory_role,
        "inventory_snapshot": inventory_snapshot,
        "provider_model": model,
        "pi_version": pi_release,
        "skill_ref": skill_ref,
        "skill_revision": skill_revision,
        "skill_hash": skill_hash_record(sha256(observed_skill), source="git-ref"),
        "harness_git_revision": harness_revision,
        "started_at": started_at,
        "duration_ms": duration_ms,
        "random_seed": {
            "status": "unsupported-by-pi-cli-and-provider",
            "value": None,
        },
        "system_prompt": {
            "status": "pi-generated-not-exported",
            "reconstruction_inputs": [
                "pi_version",
                "provider_model",
                "system_configuration",
                "skill_inventory",
            ],
        },
        "system_configuration": {
            "thinking": "minimal",
            "context_files": False,
            "extensions": False,
            "prompt_templates": False,
            "automatic_skill_discovery": True,
            "tools": ["read"],
            "skill_body_injected": False,
            "agent_directory_isolated": True,
        },
        "skill_inventory": inventory,
        "session_id": observation.session_id,
        "activation": activation_record(observation, skill_body_injected=False),
        "final_output": observation.final_output,
        "trace_file": f"raw/{trace_destination.name}",
        "result_file": f"raw/{result_destination.name}",
    }
    result["selection_outcome"] = classify_selection_outcome(
        observation.automatic_activation,
        scenario.get("input_text"),
        observation.final_output,
    )
    result_destination.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    with _PRINT_LOCK:
        print(
            f"[{environment}] {scenario['id']} repeat {repeat}: "
            f"{result['activation']['source']}"
        )
    return result


def load_environment_results(output: Path, environment: str) -> list[dict[str, Any]]:
    return [
        json.loads(path.read_text())
        for path in sorted((output / environment / "raw").glob("*.result.json"))
    ]


def _trace_reads_crystal_clear(trace_path: Path) -> bool:
    suffix = "/skills/crystal-clear/SKILL.md"
    for line in trace_path.read_text().splitlines():
        if not line.strip():
            continue
        message = json.loads(line).get("message")
        if not isinstance(message, dict) or message.get("role") != "assistant":
            continue
        for part in message.get("content", []):
            if not isinstance(part, dict):
                continue
            arguments = part.get("arguments", {})
            if (
                part.get("type") == "toolCall"
                and part.get("name") == "read"
                and isinstance(arguments, dict)
                and str(arguments.get("path", "")).endswith(suffix)
            ):
                return True
    return False


def validate_result_set(
    *,
    output: Path,
    environment: str,
    results: list[dict[str, Any]],
    scenario_set: dict[str, Any],
    repeats: int,
) -> None:
    scenarios = scenario_set["scenarios"]
    expected_keys = {
        (scenario["id"], repeat)
        for scenario in scenarios
        for repeat in range(1, repeats + 1)
    }
    actual_keys = [(row["scenario_id"], row["repeat"]) for row in results]
    if len(actual_keys) != len(set(actual_keys)):
        raise ValueError(f"{environment} results contain duplicate scenario repeats")
    if set(actual_keys) != expected_keys:
        missing = sorted(expected_keys - set(actual_keys))
        extra = sorted(set(actual_keys) - expected_keys)
        raise ValueError(
            f"{environment} result set is incomplete or stale; missing={missing}, extra={extra}"
        )
    invariant_fields = (
        "scenario_version",
        "environment",
        "inventory_role",
        "inventory_snapshot",
        "provider_model",
        "pi_version",
        "skill_ref",
        "skill_revision",
        "skill_hash",
        "harness_git_revision",
        "random_seed",
        "system_prompt",
        "system_configuration",
        "skill_inventory",
    )
    for field in invariant_fields:
        values = {json.dumps(row[field], sort_keys=True) for row in results}
        if len(values) != 1:
            raise ValueError(f"{environment} results mix incompatible {field} values")
    if results[0]["scenario_version"] != scenario_set["version"]:
        raise ValueError(f"{environment} results use a stale scenario version")
    if any(row["environment"] != environment for row in results):
        raise ValueError(f"{environment} results contain another environment")
    scenario_by_id = {scenario["id"]: scenario for scenario in scenarios}
    scenario_fields = (
        "language",
        "category",
        "split",
        "paraphrase_of",
        "rationale",
        "expected_activation",
        "prompt",
        "input_text",
    )
    for row in results:
        scenario = scenario_by_id[row["scenario_id"]]
        for field in scenario_fields:
            if row.get(field) != scenario.get(field):
                raise ValueError(
                    f"{row['scenario_id']} result uses stale scenario field {field}"
                )
        for link_field in ("trace_file", "result_file"):
            if not (output / environment / row[link_field]).is_file():
                raise ValueError(
                    f"{row['scenario_id']} repeat {row['repeat']} has no {link_field}"
                )
        trace_path = output / environment / row["trace_file"]
        trace_observation = observe_trace(trace_path, Path("/__not_a_skill__/SKILL.md"))
        trace_activated = _trace_reads_crystal_clear(trace_path)
        if row["activation"]["automatic"] != trace_activated:
            raise ValueError(
                f"{row['scenario_id']} repeat {row['repeat']} activation disagrees with trace"
            )
        if row["final_output"] != trace_observation.final_output:
            raise ValueError(
                f"{row['scenario_id']} repeat {row['repeat']} output disagrees with trace"
            )
        if row["session_id"] != trace_observation.session_id:
            raise ValueError(
                f"{row['scenario_id']} repeat {row['repeat']} session disagrees with trace"
            )
        expected_outcome = classify_selection_outcome(
            trace_activated, scenario.get("input_text"), trace_observation.final_output
        )
        if row["selection_outcome"] != expected_outcome:
            raise ValueError(
                f"{row['scenario_id']} repeat {row['repeat']} outcome disagrees with trace"
            )


def write_environment_report(
    output: Path,
    environment: str,
    results: list[dict[str, Any]],
    scenario_set: dict[str, Any],
    repeats: int,
) -> None:
    if not results:
        raise ValueError(f"no {environment} results to report")
    validate_result_set(
        output=output,
        environment=environment,
        results=results,
        scenario_set=scenario_set,
        repeats=repeats,
    )
    summary = summarize_routing_results(results)
    environment_output = output / environment
    (environment_output / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n"
    )
    first = results[0]
    (environment_output / "SUMMARY.md").write_text(
        render_routing_markdown(
            summary=summary,
            results=results,
            environment=environment,
            inventory_role=first["inventory_role"],
            scenario_version=first["scenario_version"],
            skill_ref=first["skill_ref"],
            inventory_snapshot=first["inventory_snapshot"],
        )
    )


def write_index(output: Path, environments: list[str]) -> None:
    lines = [
        "# Crystal Clear automatic-activation baseline",
        "",
        "The pinned and installed inventories are intentionally reported separately.",
        "Only the pinned inventory is eligible for later pass/fail comparison; the owner's complete installed inventory is ecological reference.",
        "",
    ]
    for environment in environments:
        lines.append(f"- [{environment} inventory report]({environment}/SUMMARY.md)")
    lines.extend([
        "",
        "The activation signal was validated by the issue #2 smoke evidence: direct invocation is recorded separately from an automatic skill read, and a known negative has no activation.",
    ])
    (output / "SUMMARY.md").write_text("\n".join(lines) + "\n")


def run_routing(args: argparse.Namespace) -> None:
    scenario_set = load_routing_scenarios(args.scenarios)
    if args.repeats != 5:
        raise ValueError("the frozen baseline must run exactly five repeats")
    skill_revision = run_command(["git", "rev-parse", args.skill_ref], cwd=REPO_ROOT)
    release = pi_version()
    harness_revision = git_revision()
    environments = ["pinned", "installed"] if args.environment == "both" else [args.environment]
    args.output.mkdir(parents=True, exist_ok=True)
    for environment in environments:
        shutil.rmtree(args.output / environment, ignore_errors=True)
    with tempfile.TemporaryDirectory(prefix="crystal-clear-routing-inventories-") as tmp_value:
        root = Path(tmp_value)
        configurations: dict[str, RoutingEnvironment] = {}
        if "pinned" in environments:
            agent_dir = root / "pinned-agent"
            inventory, snapshot = build_pinned_agent(
                agent_dir, skill_ref=args.skill_ref, manifest_path=args.manifest
            )
            configurations["pinned"] = RoutingEnvironment(
                agent_dir, inventory, snapshot, "formal"
            )
        if "installed" in environments:
            agent_dir = root / "installed-agent"
            inventory, snapshot = build_installed_agent(agent_dir, skill_ref=args.skill_ref)
            configurations["installed"] = RoutingEnvironment(
                agent_dir, inventory, snapshot, "ecological-reference"
            )
        futures = []
        with ThreadPoolExecutor(max_workers=args.jobs) as executor:
            for environment in environments:
                configuration = configurations[environment]
                for scenario in scenario_set["scenarios"]:
                    for repeat in range(1, args.repeats + 1):
                        futures.append(
                            executor.submit(
                                _run_one,
                                scenario=scenario,
                                repeat=repeat,
                                environment=environment,
                                inventory_role=configuration.role,
                                inventory_snapshot=configuration.snapshot,
                                inventory=configuration.inventory,
                                agent_dir=configuration.agent_dir,
                                model=args.model,
                                skill_ref=args.skill_ref,
                                skill_revision=skill_revision,
                                scenario_version=scenario_set["version"],
                                output=args.output,
                                pi_release=release,
                                harness_revision=harness_revision,
                            )
                        )
            for future in as_completed(futures):
                future.result()
    for environment in environments:
        write_environment_report(
            args.output,
            environment,
            load_environment_results(args.output, environment),
            scenario_set,
            args.repeats,
        )
    write_index(args.output, environments)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-ref", default="178eaf8")
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--scenarios", type=Path, default=DEFAULT_SCENARIOS)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--model", default="openai-codex/gpt-5.6-sol")
    parser.add_argument("--environment", choices=("both", "pinned", "installed"), default="both")
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--report-only", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    environments = ["pinned", "installed"] if args.environment == "both" else [args.environment]
    if args.report_only:
        scenario_set = load_routing_scenarios(args.scenarios)
        for environment in environments:
            write_environment_report(
                args.output,
                environment,
                load_environment_results(args.output, environment),
                scenario_set,
                args.repeats,
            )
        write_index(args.output, environments)
    else:
        run_routing(args)
    print(args.output / "SUMMARY.md")


if __name__ == "__main__":
    main()
