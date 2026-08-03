#!/usr/bin/env python3
"""Orchestrate and gate the Crystal Clear release-candidate evaluation."""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import subprocess
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from evals.run_behavior import load_behavior_scenarios
from evals.run_smoke import run_command

REPO_ROOT = Path(__file__).resolve().parent.parent
EVALS_ROOT = Path(__file__).resolve().parent
CURRENT_REF = "178eaf8"
RUBRIC_ITEMS = ("first_pass_understanding", "naturalness", "preservation")
CRITICAL_CALIBRATION_ITEM = "critical_preservation"
CALIBRATION_ITEMS = (*RUBRIC_ITEMS, CRITICAL_CALIBRATION_ITEM, "preference")
CALIBRATION_POLICY = {
    "version": "automated-owner-regression-v1",
    "material_disagreement_threshold": 0.20,
    "rule": "Remove an automated item from acceptance when the automated review and project owner disagree on whether one condition regresses in more than 20% of reviewed pairs.",
}


def _canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n").encode()


def _score_for_arm(row: dict[str, Any], arm: str) -> dict[str, Any]:
    if row["a_arm"] == arm: return row["judgment"]["output_a"]
    if row["b_arm"] == arm: return row["judgment"]["output_b"]
    raise ValueError(f"pair {row['pair_id']} does not contain arm {arm}")


def build_japanese_packet(judgments: list[dict[str, Any]], scenarios: dict[str, dict[str, Any]], *, candidate_revision: str, seed: int = 808, count: int = 12, harness_revision: str | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    japanese = sorted((row for row in judgments if row["category"] == "japanese"), key=lambda row: row["pair_id"])
    if len(japanese) != 25 or count not in range(10, 16):
        raise ValueError("Japanese packet requires 10-15 selections from exactly 25 Japanese pairs")
    if any(candidate_revision not in {row["a_arm"], row["b_arm"]} or CURRENT_REF not in {row["a_arm"], row["b_arm"]} for row in japanese):
        raise ValueError("Japanese judgments must compare current and candidate arms")
    rng = random.Random(seed); selected = rng.sample(japanese, count)
    orientations = ["A"] * (count // 2) + ["B"] * (count - count // 2); rng.shuffle(orientations)
    public_pairs, key_pairs = [], []
    for index, (row, candidate_label) in enumerate(zip(selected, orientations), 1):
        review_id = f"JP-{index:02d}"; current_label = "B" if candidate_label == "A" else "A"
        outputs_by_arm = {row["a_arm"]: row["presented_output_a"], row["b_arm"]: row["presented_output_b"]}
        output_a = outputs_by_arm[candidate_revision] if candidate_label == "A" else outputs_by_arm[CURRENT_REF]
        output_b = outputs_by_arm[candidate_revision] if candidate_label == "B" else outputs_by_arm[CURRENT_REF]
        scenario = scenarios[row["scenario_id"]]
        public_pairs.append({"review_id": review_id, "source_text": scenario["source_text"], "output_contract": scenario["output_contract"], "output_a": output_a, "output_b": output_b})
        key_pairs.append({
            "review_id": review_id, "pair_id": row["pair_id"], "candidate_label": candidate_label, "current_label": current_label,
            "scores": {
                "candidate": {
                    **{item: _score_for_arm(row, candidate_revision)[item] for item in RUBRIC_ITEMS},
                    CRITICAL_CALIBRATION_ITEM: _score_for_arm(row, candidate_revision)["critical_preservation_failure"],
                },
                "current": {
                    **{item: _score_for_arm(row, CURRENT_REF)[item] for item in RUBRIC_ITEMS},
                    CRITICAL_CALIBRATION_ITEM: _score_for_arm(row, CURRENT_REF)["critical_preservation_failure"],
                },
            },
            "gpt_preference": row["judgment"]["preference"],
            "gpt_candidate_label": "A" if row["a_arm"] == candidate_revision else "B",
        })
    packet = {
        "schema_version": 1, "packet_version": "japanese-blind-review-v1", "seed": seed,
        "harness_revision": harness_revision or run_command(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT),
        "calibration_policy": CALIBRATION_POLICY,
        "instructions_ja": "各案を独立に評価してください。A/Bそれぞれについて、初読理解・自然さ・意味保存を1（低い）〜5（高い）で採点し、重大な意味変更の有無を記録してください。最後にA、B、同等のいずれかを選んでください。条件名を推測しないでください。",
        "rubric": {"first_pass_understanding": "初読理解 1〜5", "naturalness": "自然さ 1〜5", "preservation": "意味保存 1〜5", "critical_meaning_change": "重大な意味変更 true/false", "preference": "A/B/tie"},
        "pairs": public_pairs,
    }
    packet_sha = hashlib.sha256(_canonical(packet)).hexdigest()
    key = {"schema_version": 1, "packet_sha256": packet_sha, "candidate_revision": candidate_revision, "current_revision": run_command(["git", "rev-parse", CURRENT_REF], cwd=REPO_ROOT), "pairs": key_pairs}
    return packet, key


def human_response_template(packet: dict[str, Any]) -> dict[str, Any]:
    blank_scores = {
        "first_pass_understanding": None,
        "naturalness": None,
        "preservation": None,
        "critical_meaning_change": None,
    }
    return {
        "packet_sha256": hashlib.sha256(_canonical(packet)).hexdigest(),
        "reviewer_role": "project-owner",
        "owner_attestation": True,
        "reviews": [
            {
                "review_id": pair["review_id"],
                "output_a": dict(blank_scores),
                "output_b": dict(blank_scores),
                "preference": None,
                "notes": "",
            }
            for pair in packet["pairs"]
        ],
    }


def import_human_response(packet: dict[str, Any], key: dict[str, Any], response: dict[str, Any]) -> dict[str, Any]:
    expected_top = {"packet_sha256", "reviewer_role", "owner_attestation", "reviews"}
    if not isinstance(response, dict) or set(response) != expected_top:
        raise ValueError("human response has unexpected top-level fields")
    if response["reviewer_role"] != "project-owner" or response["owner_attestation"] is not True:
        raise ValueError("human response requires project-owner attestation")
    packet_sha = hashlib.sha256(_canonical(packet)).hexdigest()
    if key.get("packet_sha256") != packet_sha or response.get("packet_sha256") != packet_sha:
        raise ValueError("human response packet hash does not match the frozen packet")
    reviews = response.get("reviews")
    expected_ids = {row["review_id"] for row in packet["pairs"]}
    if not isinstance(reviews, list) or len(reviews) != len(expected_ids):
        raise ValueError(f"human response must contain exactly {len(expected_ids)} reviews")
    if {row.get("review_id") for row in reviews} != expected_ids:
        raise ValueError("human response review ids are missing, duplicate, or unknown")
    expected_fields = {"review_id", "output_a", "output_b", "preference", "notes"}
    score_fields = set(RUBRIC_ITEMS) | {"critical_meaning_change"}
    by_id = {row["review_id"]: row for row in reviews}; key_by_id = {row["review_id"]: row for row in key["pairs"]}
    regressions = critical = 0; comparisons = {item: {"disagreements": 0, "pairs": len(reviews)} for item in CALIBRATION_ITEMS}
    for review_id in sorted(expected_ids):
        review, assignment = by_id[review_id], key_by_id[review_id]
        if set(review) != expected_fields or review["preference"] not in {"A", "B", "tie"} or not isinstance(review["notes"], str):
            raise ValueError(f"review {review_id} has invalid fields")
        for label in ("output_a", "output_b"):
            score = review[label]
            if not isinstance(score, dict) or set(score) != score_fields or not isinstance(score["critical_meaning_change"], bool):
                raise ValueError(f"review {review_id} {label} is invalid")
            if any(type(score[item]) is not int or not 1 <= score[item] <= 5 for item in RUBRIC_ITEMS):
                raise ValueError(f"review {review_id} scores must be integers from 1 to 5")
        candidate_key = "output_" + assignment["candidate_label"].lower(); current_key = "output_" + assignment["current_label"].lower()
        candidate_critical = review[candidate_key]["critical_meaning_change"]
        current_critical = review[current_key]["critical_meaning_change"]
        score_regression = any(review[candidate_key][item] < review[current_key][item] for item in RUBRIC_ITEMS)
        critical_regression = candidate_critical and not current_critical
        preference_regression = review["preference"] == assignment["current_label"]
        regressions += int(score_regression or critical_regression or preference_regression)
        critical += int(candidate_critical)
        for item in RUBRIC_ITEMS:
            human_regression = review[candidate_key][item] < review[current_key][item]
            gpt_regression = assignment["scores"]["candidate"][item] < assignment["scores"]["current"][item]
            comparisons[item]["disagreements"] += human_regression != gpt_regression
        gpt_critical_regression = assignment["scores"]["candidate"][CRITICAL_CALIBRATION_ITEM] and not assignment["scores"]["current"][CRITICAL_CALIBRATION_ITEM]
        comparisons[CRITICAL_CALIBRATION_ITEM]["disagreements"] += critical_regression != gpt_critical_regression
        gpt_preference_regression = assignment["gpt_preference"] != "tie" and assignment["gpt_preference"] != assignment["gpt_candidate_label"]
        comparisons["preference"]["disagreements"] += preference_regression != gpt_preference_regression
    calibration = {}
    threshold = packet["calibration_policy"]["material_disagreement_threshold"]
    for item, values in comparisons.items():
        rate = values["disagreements"] / values["pairs"]
        calibration[item] = {**values, "disagreement_rate": round(rate, 4), "automated_acceptance": rate <= threshold}
    return {
        "valid": True, "pairs": len(reviews), "candidate_regressions": regressions,
        "candidate_regression_rate": round(regressions / len(reviews), 4),
        "candidate_critical_changes": critical, "calibration": calibration,
        "calibration_policy": packet["calibration_policy"],
        "reviewer_role": response["reviewer_role"],
        "owner_attestation": response["owner_attestation"],
        "raw_response_sha256": hashlib.sha256(_canonical(response)).hexdigest(),
        "reviews": reviews,
    }


def _gate(identifier: str, passed: bool, actual: Any, threshold: str, *, group: str, gating: bool = True) -> dict[str, Any]:
    return {"id": identifier, "group": group, "passed": bool(passed), "actual": actual, "threshold": threshold, "gating": gating}


def evaluate_release(*, candidate_revision: str, routing: dict[str, Any], behavior: dict[str, Any], boundary: dict[str, Any], human: dict[str, Any] | None) -> dict[str, Any]:
    behavior_runs = sum(category["generations"] for category in behavior["categories"].values())
    core = routing.get("runs", 0) + behavior_runs; gates = [_gate("core-generation-matrix", core == 425 and routing.get("runs") == 200 and behavior_runs == 225, core, "exactly 200 routing + 225 behavior = 425", group="provenance")]
    gates += [
        _gate("routing-explicit-recall", routing["categories"]["explicit-request"]["recall"] >= .95, routing["categories"]["explicit-request"]["recall"], ">= 0.95", group="routing"),
        _gate("routing-complex-recall", routing["categories"]["complex-communication"]["recall"] >= .85, routing["categories"]["complex-communication"]["recall"], ">= 0.85", group="routing"),
        _gate("routing-unrelated-fpr", routing["categories"]["unrelated-control"]["false_positive_rate"] <= .10, routing["categories"]["unrelated-control"]["false_positive_rate"], "<= 0.10", group="routing"),
    ]
    if behavior.get("arms") != ["no-skill", CURRENT_REF, candidate_revision] or behavior.get("compare_arms") != [CURRENT_REF, candidate_revision] or behavior.get("repeats") != 5:
        gates.append(_gate("behavior-arm-provenance", False, {"arms": behavior.get("arms"), "compare_arms": behavior.get("compare_arms")}, "exact release arms and comparison", group="provenance"))
    else: gates.append(_gate("behavior-arm-provenance", True, behavior["arms"], "exact release arms and comparison", group="provenance"))
    excluded = {item for item, value in (human or {}).get("calibration", {}).items() if not value.get("automated_acceptance", True)}
    for category in ("english", "japanese", "multilingual-core"):
        arm = behavior["categories"][category]["arms"][candidate_revision]; judged = arm["gpt_judged"]; prefs = judged["pair_preferences"]; pairs = sum(prefs.values())
        preservation_gating = "preservation" not in excluded
        critical_gating = CRITICAL_CALIBRATION_ITEM not in excluded
        preference_gating = "preference" not in excluded
        noncritical_preservation = judged["mean_noncritical_preservation"]
        gates += [
            _gate(f"{category}-mean-noncritical-preservation", noncritical_preservation >= 4.5, noncritical_preservation, ">= 4.5", group="behavior", gating=preservation_gating),
            _gate(f"{category}-critical-failures", judged["critical_failures"] == 0, judged["critical_failures"], "= 0", group="behavior", gating=critical_gating),
            _gate(f"{category}-protected-string-changes", arm["deterministic_failures_by_kind"]["protected-string"] == 0, arm["deterministic_failures_by_kind"]["protected-string"], "= 0", group="behavior"),
            _gate(f"{category}-candidate-win-rate", prefs["wins"] / pairs >= .5, round(prefs["wins"] / pairs, 4), ">= 0.50", group="behavior", gating=preference_gating),
            _gate(f"{category}-candidate-loss-rate", prefs["losses"] / pairs <= .1, round(prefs["losses"] / pairs, 4), "<= 0.10", group="behavior", gating=preference_gating),
        ]
    for language in ("en", "ja"):
        item = boundary["languages"][language]
        gates += [_gate(f"boundary-{language}-equivalent", item["equivalent_rate"] >= .9, item["equivalent_rate"], ">= 0.90", group="boundary"), _gate(f"boundary-{language}-critical-changes", item.get("critical_meaning_changes", 0) == 0, item.get("critical_meaning_changes", 0), "= 0", group="boundary")]
    gates.append(_gate("boundary-post-candidate-disclosure", boundary.get("post_candidate_fixture") is True, boundary.get("post_candidate_fixture"), "must disclose post-candidate fixture", group="boundary"))
    if human:
        gates += [_gate("human-candidate-regressions", human["candidate_regression_rate"] <= .1, human["candidate_regression_rate"], "<= 0.10", group="human"), _gate("human-critical-meaning-changes", human["candidate_critical_changes"] == 0, human["candidate_critical_changes"], "= 0", group="human")]
    gating_failures = [gate for gate in gates if gate["gating"] and not gate["passed"]]
    decision = "fail" if gating_failures else "pass" if human else "pending-human-review"
    return {"schema_version": 1, "candidate_revision": candidate_revision, "core_generations": core, "decision": decision, "gates": gates, "removed_automated_rubric_items": sorted(excluded), "human_review": human, "language_results_are_separate": True}


def _read(path: Path) -> Any: return json.loads(path.read_text())


def candidate_artifact_hashes(revision: str) -> dict[str, str]:
    hashes = {}
    for name in ("SKILL.md", "language-guides.md", "elements-of-style.md", "references/use-cases.md"):
        content = run_command(["git", "show", f"{revision}:{name}"], cwd=REPO_ROOT) + "\n"
        hashes[name] = hashlib.sha256(content.encode()).hexdigest()
    return hashes


def validate_routing_candidate_provenance(routing_dir: Path, revision: str, expected_skill_hash: str) -> None:
    rows = [_read(path) for path in sorted((routing_dir / "pinned" / "raw").glob("*.result.json"))]
    if len(rows) != 200:
        raise ValueError("release routing evidence must contain exactly 200 raw results")
    if any(row.get("skill_ref") != revision or row.get("skill_revision") != revision for row in rows):
        raise ValueError("release routing evidence does not use the exact immutable candidate revision")
    if any(row.get("skill_hash", {}).get("sha256") != expected_skill_hash for row in rows):
        raise ValueError("release routing evidence does not use the recorded candidate SKILL.md hash")


def validate_clean_tracked_worktree() -> None:
    result = subprocess.run(
        ["git", "diff-index", "--quiet", "HEAD", "--"], cwd=REPO_ROOT
    )
    if result.returncode:
        raise ValueError("live release evaluation requires a clean tracked worktree")


def validate_cross_suite_provenance(routing_dir: Path, behavior_dir: Path, boundary_dir: Path) -> dict[str, str]:
    paths = [
        next(iter(sorted((routing_dir / "pinned" / "raw").glob("*.result.json"))), None),
        next(iter(sorted((behavior_dir / "raw" / "generations").glob("*.result.json"))), None),
        next(iter(sorted((boundary_dir / "raw").glob("*.result.json"))), None),
    ]
    if any(path is None for path in paths):
        raise ValueError("release suites are missing raw provenance records")
    rows = [_read(path) for path in paths]
    provenance = {field: {row[field] for row in rows} for field in ("provider_model", "pi_version", "harness_git_revision")}
    mixed = [field for field, values in provenance.items() if len(values) != 1]
    if mixed:
        raise ValueError(f"release suites mix provenance: {', '.join(mixed)}")
    return {field: next(iter(values)) for field, values in provenance.items()}


def _run(command: list[str]) -> None:
    subprocess.run(command, cwd=REPO_ROOT, check=True)


def render_release(report: dict[str, Any]) -> str:
    lines = ["# Release-candidate decision", "", f"Decision: **{report['decision']}**", "", f"Candidate revision: `{report['candidate_revision']}`", f"Core matrix: {report['core_generations']} generations (routing and behavior only).", "", "English, Japanese, and multilingual-core results are kept separate. Failed and non-gating checks remain visible.", "", "| Gate | Group | Result | Actual | Threshold | Gating |", "|---|---|---|---|---|---|"]
    for gate in report["gates"]: lines.append(f"| {gate['id']} | {gate['group']} | {'pass' if gate['passed'] else 'fail'} | {gate['actual']} | {gate['threshold']} | {'yes' if gate['gating'] else 'removed after calibration'} |")
    lines += ["", "The already-clear fixture was designed after candidate authorship and is supplemental; it is excluded from the 425-generation matrix.", "", f"Removed GPT rubric items: {', '.join(report['removed_automated_rubric_items']) or 'none'}."]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--candidate-ref", required=True); parser.add_argument("--output", type=Path, required=True); parser.add_argument("--model", default="openai-codex/gpt-5.6-sol"); parser.add_argument("--judge-seed", type=int, default=808); parser.add_argument("--human-response", type=Path); parser.add_argument("--report-only", action="store_true")
    args = parser.parse_args()
    if args.candidate_ref == "worktree": raise ValueError("release candidate must be an immutable git commit")
    revision = run_command(["git", "rev-parse", "--verify", f"{args.candidate_ref}^{{commit}}"], cwd=REPO_ROOT)
    current = run_command(["git", "rev-parse", CURRENT_REF], cwd=REPO_ROOT)
    args.output.mkdir(parents=True, exist_ok=True); routing_dir, behavior_dir, boundary_dir = args.output / "routing", args.output / "behavior", args.output / "already-clear"
    python = sys.executable
    if not args.report_only:
        validate_clean_tracked_worktree()
        _run([python, "-m", "evals.run_routing", "--skill-ref", revision, "--environment", "pinned", "--repeats", "5", "--output", str(routing_dir), "--model", args.model])
        _run([python, "-m", "evals.run_behavior", "--arms", f"no-skill,{CURRENT_REF},{revision}", "--compare-arms", f"{CURRENT_REF},{revision}", "--repeats", "5", "--judge-seed", str(args.judge_seed), "--output", str(behavior_dir), "--model", args.model])
        _run([python, "-m", "evals.run_boundary", "--candidate-ref", revision, "--output", str(boundary_dir), "--model", args.model])
    else:
        _run([python, "-m", "evals.run_routing", "--skill-ref", revision, "--environment", "pinned", "--repeats", "5", "--output", str(routing_dir), "--report-only"])
        _run([python, "-m", "evals.run_behavior", "--arms", f"no-skill,{CURRENT_REF},{revision}", "--compare-arms", f"{CURRENT_REF},{revision}", "--repeats", "5", "--judge-seed", str(args.judge_seed), "--output", str(behavior_dir), "--report-only"])
        _run([python, "-m", "evals.run_boundary", "--candidate-ref", revision, "--output", str(boundary_dir), "--report-only"])
    artifact_hashes = candidate_artifact_hashes(revision)
    validate_routing_candidate_provenance(routing_dir, revision, artifact_hashes["SKILL.md"])
    judgments = [json.loads(path.read_text()) for path in sorted((behavior_dir / "raw" / "judgments").glob("*.result.json"))]
    scenario_data = load_behavior_scenarios(EVALS_ROOT / "behavior-scenarios.json")
    provenance = validate_cross_suite_provenance(routing_dir, behavior_dir, boundary_dir)
    packet, key = build_japanese_packet(
        judgments, {row["id"]: row for row in scenario_data["scenarios"]},
        candidate_revision=revision, seed=args.judge_seed, count=12,
        harness_revision=provenance["harness_git_revision"],
    )
    packet_path, key_path = args.output / "japanese-review.packet.json", args.output / "japanese-review.assignment-key.json"
    template_path = args.output / "japanese-review.response-template.json"
    packet_path.write_bytes(_canonical(packet)); key_path.write_text(json.dumps(key, indent=2, ensure_ascii=False) + "\n")
    template_path.write_text(json.dumps(human_response_template(packet), indent=2, ensure_ascii=False) + "\n")
    packet_hash_path = args.output / "japanese-review.packet.sha256"
    packet_hash_path.write_text(key["packet_sha256"] + "  " + packet_path.name + "\n")
    human = None
    response_artifact = None
    if args.human_response:
        response = _read(args.human_response)
        human = import_human_response(packet, key, response)
        response_artifact = args.output / "japanese-review.response.json"
        response_artifact.write_bytes(_canonical(response))
    routing, behavior, boundary = _read(routing_dir / "pinned" / "summary.json"), _read(behavior_dir / "summary.json"), _read(boundary_dir / "summary.json")
    report = evaluate_release(candidate_revision=revision, routing=routing, behavior=behavior, boundary=boundary, human=human)
    report["current_revision"] = current; report["candidate_artifact_hashes"] = artifact_hashes; report["execution_provenance"] = provenance
    report["artifacts"] = {"routing": "routing/pinned/SUMMARY.md", "behavior": "behavior/SUMMARY.md", "boundary": "already-clear/SUMMARY.md", "japanese_packet": packet_path.name, "japanese_packet_hash": packet_hash_path.name, "response_template": template_path.name, "assignment_key": key_path.name, "owner_response": None if response_artifact is None else response_artifact.name}
    (args.output / "release.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n"); (args.output / "RELEASE.md").write_text(render_release(report)); print(args.output / "RELEASE.md")


if __name__ == "__main__": main()
