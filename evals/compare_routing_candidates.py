#!/usr/bin/env python3
"""Compare fixed metadata candidates using held-out Pi routing evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from evals.run_routing import (
    DEFAULT_CANDIDATES,
    DEFAULT_SCENARIOS,
    load_environment_results,
    load_routing_candidates,
    load_routing_scenarios,
    summarize_routing_results,
    validate_result_set,
)


THRESHOLDS = {
    "explicit_request_recall": 0.95,
    "complex_communication_recall": 0.85,
    "unrelated_control_false_positive_rate": 0.10,
}


def _boundary_accuracy(metric: dict[str, Any]) -> float | None:
    total = metric["positive_runs"] + metric["negative_runs"]
    if not total:
        return None
    correct = metric["true_positives"] + metric["negative_runs"] - metric["false_positives"]
    return round(correct / total, 4)


def assess_candidate(summary: dict[str, Any], *, description_length: int) -> dict[str, Any]:
    held = summary["category_splits"]
    explicit = held["explicit-request"]["held-out"]
    complex_ = held["complex-communication"]["held-out"]
    control = held["unrelated-control"]["held-out"]
    boundary = held["boundary"]["held-out"]
    checks = {
        "explicit_request_recall": explicit["recall"] >= THRESHOLDS["explicit_request_recall"],
        "complex_communication_recall": complex_["recall"] >= THRESHOLDS["complex_communication_recall"],
        "unrelated_control_false_positive_rate": control["false_positive_rate"] <= THRESHOLDS["unrelated_control_false_positive_rate"],
    }
    correct = (
        explicit["true_positives"]
        + complex_["true_positives"]
        + control["negative_runs"]
        - control["false_positives"]
    )
    return {
        "description_length": description_length,
        "passes": all(checks.values()),
        "checks": checks,
        "held_out_correct": correct,
        "held_out": {
            "explicit_request_recall": explicit["recall"],
            "complex_communication_recall": complex_["recall"],
            "unrelated_control_false_positive_rate": control["false_positive_rate"],
            "boundary": {
                "recall": boundary["recall"],
                "false_positive_rate": boundary["false_positive_rate"],
                "accuracy": _boundary_accuracy(boundary),
            },
        },
    }


def choose_candidate(candidates: list[dict[str, Any]]) -> dict[str, Any] | None:
    passing = [candidate for candidate in candidates if candidate["assessment"]["passes"]]
    if not passing:
        return None
    return max(
        passing,
        key=lambda candidate: (
            candidate["assessment"]["held_out_correct"],
            -len(candidate["description"]),
        ),
    )


def _delta(value: float | None, baseline: float | None) -> float | None:
    if value is None or baseline is None:
        return None
    return round(value - baseline, 4)


def _format_rate(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.1%}"


def _load_validated_results(
    output: Path,
    scenario_set: dict[str, Any],
    *,
    split: str = "all",
    expected_skill_ref: str | None = None,
) -> list[dict[str, Any]]:
    results = load_environment_results(output, "pinned")
    validate_result_set(
        output=output,
        environment="pinned",
        results=results,
        scenario_set=scenario_set,
        repeats=5,
        split=split,
    )
    if expected_skill_ref is not None and {
        row["skill_ref"] for row in results
    } != {expected_skill_ref}:
        raise ValueError(
            f"{output} does not contain only expected skill {expected_skill_ref}"
        )
    return results


def compare(
    candidate_file: Path,
    results_root: Path,
    baseline_output: Path,
    scenario_file: Path = DEFAULT_SCENARIOS,
    semantic_scenario_file: Path | None = None,
) -> dict[str, Any]:
    candidate_set = load_routing_candidates(candidate_file)
    scenario_set = load_routing_scenarios(scenario_file)
    baseline = summarize_routing_results(
        _load_validated_results(baseline_output, scenario_set)
    )
    rows = []
    for candidate in candidate_set["candidates"]:
        candidate_root = results_root / candidate["id"]
        expected_ref = f"{candidate_set['base_skill_ref']}+metadata:{candidate['id']}"
        results = []
        for split in ("train", "held-out"):
            results.extend(
                _load_validated_results(
                    candidate_root / split,
                    scenario_set,
                    split=split,
                    expected_skill_ref=expected_ref,
                )
            )
        summary = summarize_routing_results(results)
        assessment = assess_candidate(
            summary, description_length=len(candidate["description"])
        )
        baseline_held = baseline["category_splits"]
        held = assessment["held_out"]
        assessment["change_from_178eaf8"] = {
            "explicit_request_recall": _delta(
                held["explicit_request_recall"],
                baseline_held["explicit-request"]["held-out"]["recall"],
            ),
            "complex_communication_recall": _delta(
                held["complex_communication_recall"],
                baseline_held["complex-communication"]["held-out"]["recall"],
            ),
            "unrelated_control_false_positive_rate": _delta(
                held["unrelated_control_false_positive_rate"],
                baseline_held["unrelated-control"]["held-out"]["false_positive_rate"],
            ),
            "boundary_recall": _delta(
                held["boundary"]["recall"],
                baseline_held["boundary"]["held-out"]["recall"],
            ),
            "boundary_false_positive_rate": _delta(
                held["boundary"]["false_positive_rate"],
                baseline_held["boundary"]["held-out"]["false_positive_rate"],
            ),
        }
        rows.append({**candidate, "assessment": assessment, "summary": summary})
    selected = choose_candidate(rows)
    semantic_probe_summary = None
    if selected and semantic_scenario_file is not None:
        semantic_output = results_root / selected["id"] / "semantic-probes"
        if semantic_output.is_dir():
            semantic_set = load_routing_scenarios(
                semantic_scenario_file, frozen=False
            )
            semantic_results = _load_validated_results(
                semantic_output,
                semantic_set,
                expected_skill_ref=(
                    f"{candidate_set['base_skill_ref']}+metadata:{selected['id']}"
                ),
            )
            semantic_probe_summary = summarize_routing_results(semantic_results)
    return {
        "schema_version": 1,
        "candidate_version": candidate_set["version"],
        "base_skill_ref": candidate_set["base_skill_ref"],
        "selection_rule": "Among candidates passing all held-out thresholds, maximize correct held-out explicit, complex, and unrelated-control runs; break an exact tie by choosing the shorter description.",
        "thresholds": THRESHOLDS,
        "selected_candidate": selected["id"] if selected else None,
        "semantic_probe_summary": semantic_probe_summary,
        "candidates": rows,
    }


def render_markdown(comparison: dict[str, Any]) -> str:
    lines = [
        "# Automatic activation metadata comparison",
        "",
        f"- Candidate set: `{comparison['candidate_version']}`",
        f"- Unchanged skill body base: `{comparison['base_skill_ref']}`",
        "- Reference harness/model: Pi with `openai-codex/gpt-5.6-sol`",
        "- Metadata: English-only; every candidate is at most 1,024 characters",
        "- Tuning: candidates and the selection rule were frozen before held-out evaluation; no wording was changed after inspecting held-out evidence",
        f"- Selection rule: {comparison['selection_rule']}",
        "",
        "## Held-out acceptance and change from `178eaf8`",
        "",
        "| Candidate | Chars | Explicit recall | Delta | Complex recall | Delta | Unrelated FPR | Delta | Pass |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in comparison["candidates"]:
        a = row["assessment"]
        h = a["held_out"]
        d = a["change_from_178eaf8"]
        lines.append(
            f"| {row['id']} | {a['description_length']} | {_format_rate(h['explicit_request_recall'])} | "
            f"{_format_rate(d['explicit_request_recall'])} | {_format_rate(h['complex_communication_recall'])} | "
            f"{_format_rate(d['complex_communication_recall'])} | {_format_rate(h['unrelated_control_false_positive_rate'])} | "
            f"{_format_rate(d['unrelated_control_false_positive_rate'])} | {'yes' if a['passes'] else 'no'} |"
        )
    selected = comparison["selected_candidate"]
    lines.extend(["", "## Selection", ""])
    if selected:
        lines.append(f"Selected **`{selected}`** from the held-out evidence using the frozen rule above.")
    else:
        lines.append("**No candidate was selected.** Every failed candidate and its threshold trade-off remains published below.")
    lines.extend([
        "",
        "Direct invocation remains the guaranteed fallback in Pi: `/skill:crystal-clear`.",
        "",
        "## Boundary category (reported independently)",
        "",
        "| Candidate | Recall | Delta | False-positive rate | Delta | Accuracy |",
        "|---|---:|---:|---:|---:|---:|",
    ])
    for row in comparison["candidates"]:
        h = row["assessment"]["held_out"]["boundary"]
        d = row["assessment"]["change_from_178eaf8"]
        lines.append(
            f"| {row['id']} | {_format_rate(h['recall'])} | {_format_rate(d['boundary_recall'])} | "
            f"{_format_rate(h['false_positive_rate'])} | {_format_rate(d['boundary_false_positive_rate'])} | "
            f"{_format_rate(h['accuracy'])} |"
        )
    lines.extend(["", "## Candidate descriptions and evidence", ""])
    for row in comparison["candidates"]:
        lines.extend([
            f"### `{row['id']}` — {row['variant']}",
            "",
            f"> {row['description']}",
            "",
            f"- [Training raw run report]({row['id']}/train/pinned/SUMMARY.md)",
            f"- [Held-out raw run report]({row['id']}/held-out/pinned/SUMMARY.md)",
            f"- Training explicit recall: {_format_rate(row['summary']['category_splits']['explicit-request']['train']['recall'])}",
            f"- Training complex recall: {_format_rate(row['summary']['category_splits']['complex-communication']['train']['recall'])}",
            f"- Training unrelated-control FPR: {_format_rate(row['summary']['category_splits']['unrelated-control']['train']['false_positive_rate'])}",
            "",
        ])
    probes = comparison.get("semantic_probe_summary")
    if probes is not None:
        lines.extend([
            "## Supplemental semantic routing",
            "",
            "These non-English/non-Japanese probes are reported separately and do not affect candidate selection or frozen acceptance metrics.",
            "",
            "| Language | Runs | Recall |",
            "|---|---:|---:|",
        ])
        for language, metrics in probes["languages"].items():
            lines.append(
                f"| {language} | {metrics['runs']} | {_format_rate(metrics['recall'])} |"
            )
        lines.extend([
            "",
            f"- [Selected-candidate raw probe report]({selected}/semantic-probes/pinned/SUMMARY.md)",
            "",
        ])
    lines.extend([
        "## Reproduce",
        "",
        "```sh",
        "# Run training before held-out; do not revise routing-candidates.json between them.",
        "for candidate in concrete short; do",
        "  python3 -m evals.run_routing --skill-ref ac8f935 --candidate \"$candidate\" --split train --environment pinned --repeats 5 --output \"evals/results/routing/metadata-v1/$candidate/train\"",
        "  python3 -m evals.run_routing --skill-ref ac8f935 --candidate \"$candidate\" --split held-out --environment pinned --repeats 5 --output \"evals/results/routing/metadata-v1/$candidate/held-out\"",
        "done",
        "python3 -m evals.compare_routing_candidates --semantic-scenarios evals/routing-semantic-probes.json",
        "```",
    ])
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--results", type=Path, default=Path("evals/results/routing/metadata-v1"))
    parser.add_argument("--baseline", type=Path, default=Path("evals/results/routing/178eaf8"))
    parser.add_argument("--scenarios", type=Path, default=DEFAULT_SCENARIOS)
    parser.add_argument("--semantic-scenarios", type=Path)
    args = parser.parse_args()
    comparison = compare(
        args.candidates,
        args.results,
        args.baseline,
        args.scenarios,
        args.semantic_scenarios,
    )
    args.results.mkdir(parents=True, exist_ok=True)
    (args.results / "comparison.json").write_text(json.dumps(comparison, indent=2, ensure_ascii=False) + "\n")
    (args.results / "SUMMARY.md").write_text(render_markdown(comparison))
    print(args.results / "SUMMARY.md")


if __name__ == "__main__":
    main()
