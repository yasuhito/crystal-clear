import json
import tempfile
import unittest
from pathlib import Path

from evals.run_behavior import _materialize_skill
from evals.run_boundary import load_boundary_scenarios, parse_equivalence
from evals.run_release import (
    build_japanese_packet,
    evaluate_release,
    human_response_template,
    import_human_response,
)


BOUNDARY = Path(__file__).resolve().parents[1] / "already-clear-scenarios.json"


def judged(score, *, critical=False):
    return {
        "critical_preservation_failure": critical,
        "critical_failure_types": ["changed-certainty"] if critical else [],
        "preservation": score,
        "first_pass_understanding": score,
        "core_structure": score,
        "referent_scope_terminology": score,
        "register_preserved": True,
        "naturalness": score,
        "evidence": "evidence",
    }


def behavior_summary(candidate="b" , *, critical=0, protected=0, wins=20, losses=2):
    categories = {}
    for category in ("english", "japanese", "multilingual-core"):
        categories[category] = {"generations": 75, "judgments": 25, "arms": {
            "no-skill": {"runs": 25, "deterministic_failures_by_kind": {}},
            "178eaf8": {"runs": 25, "deterministic_failures_by_kind": {}},
            candidate: {"runs": 25, "deterministic_failures_by_kind": {"protected-string": protected}, "gpt_judged": {
                "outputs": 25, "mean_preservation": 4.8, "mean_noncritical_preservation": 4.8, "critical_failures": critical,
                "pair_preferences": {"wins": wins, "losses": losses, "ties": 25-wins-losses},
            }},
        }}
    return {"arms": ["no-skill", "178eaf8", candidate], "compare_arms": ["178eaf8", candidate], "repeats": 5, "categories": categories}


class SkillArtifactTests(unittest.TestCase):
    def test_materializes_referenced_recipe_when_present_and_tolerates_old_ref(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, candidate_hashes = _materialize_skill("1691ba0", root / "candidate")
            _, baseline_hashes = _materialize_skill("178eaf8", root / "baseline")
            self.assertIn("references/use-cases.md", candidate_hashes)
            self.assertTrue((root / "candidate" / "references" / "use-cases.md").is_file())
            self.assertNotIn("references/use-cases.md", baseline_hashes)


class BoundaryTests(unittest.TestCase):
    def test_fixture_is_versioned_and_balanced(self):
        data = load_boundary_scenarios(BOUNDARY)
        self.assertEqual(len(data["scenarios"]), 4)
        self.assertEqual({row["language"] for row in data["scenarios"]}, {"en", "ja"})

    def test_equivalence_parser_is_strict(self):
        self.assertTrue(parse_equivalence('{"equivalent":true,"critical_meaning_change":false,"evidence":"same"}')["equivalent"])
        with self.assertRaises(ValueError):
            parse_equivalence('{"equivalent":true,"critical_meaning_change":false,"evidence":"same","arm":"candidate"}')


class ReleaseGateTests(unittest.TestCase):
    def test_release_stays_pending_until_human_response(self):
        report = evaluate_release(
            candidate_revision="b" * 40,
            routing={"runs": 200, "categories": {
                "explicit-request": {"recall": .96}, "complex-communication": {"recall": .88},
                "unrelated-control": {"false_positive_rate": .1}}},
            behavior=behavior_summary("b" * 40),
            boundary={"post_candidate_fixture": True, "languages": {"en": {"equivalent_rate": 1}, "ja": {"equivalent_rate": .9}}},
            human=None,
        )
        self.assertEqual(report["decision"], "pending-human-review")
        self.assertEqual(report["core_generations"], 425)

    def test_calibration_can_remove_only_the_disagreed_gpt_item(self):
        candidate = "b" * 40
        behavior = behavior_summary(candidate)
        for category in behavior["categories"].values():
            category["arms"][candidate]["gpt_judged"]["mean_noncritical_preservation"] = 4.4
        human = {"valid": True, "candidate_regression_rate": 0, "candidate_critical_changes": 0, "calibration": {"preservation": {"automated_acceptance": False}}}
        report = evaluate_release(
            candidate_revision=candidate,
            routing={"runs": 200, "categories": {"explicit-request": {"recall": .96}, "complex-communication": {"recall": .88}, "unrelated-control": {"false_positive_rate": .1}}},
            behavior=behavior,
            boundary={"post_candidate_fixture": True, "languages": {"en": {"equivalent_rate": 1}, "ja": {"equivalent_rate": 1}}},
            human=human,
        )
        preservation = [gate for gate in report["gates"] if "mean-noncritical-preservation" in gate["id"]]
        self.assertTrue(all(not gate["passed"] and not gate["gating"] for gate in preservation))
        self.assertEqual(report["decision"], "pass")

    def test_failed_language_gate_remains_visible_and_fails(self):
        human = {"valid": True, "candidate_regressions": 0, "candidate_regression_rate": 0, "pairs": 12, "candidate_critical_changes": 0, "calibration": {}}
        report = evaluate_release(
            candidate_revision="b" * 40,
            routing={"runs": 200, "categories": {
                "explicit-request": {"recall": .96}, "complex-communication": {"recall": .88},
                "unrelated-control": {"false_positive_rate": .1}}},
            behavior=behavior_summary("b" * 40, critical=1),
            boundary={"post_candidate_fixture": True, "languages": {"en": {"equivalent_rate": 1}, "ja": {"equivalent_rate": 1}}},
            human=human,
        )
        self.assertEqual(report["decision"], "fail")
        self.assertTrue(any(not gate["passed"] and "critical" in gate["id"] for gate in report["gates"]))


class JapanesePacketTests(unittest.TestCase):
    def _judgments(self):
        rows = []
        for i in range(25):
            rows.append({
                "pair_id": f"ja-{i // 5}--r{i % 5 + 1:02}", "scenario_id": f"ja-{i // 5}",
                "category": "japanese", "repeat": i % 5 + 1,
                "a_arm": "178eaf8", "b_arm": "c" * 40,
                "presented_output_a": f"現行{i}", "presented_output_b": f"候補{i}",
                "judgment": {"output_a": judged(4), "output_b": judged(5), "preference": "B", "preference_evidence": ""},
            })
        return rows

    def test_packet_is_deterministic_anonymous_and_has_separate_key(self):
        scenarios = {f"ja-{i}": {"source_text": f"原文{i}", "output_contract": "本文のみ"} for i in range(5)}
        packet, key = build_japanese_packet(self._judgments(), scenarios, candidate_revision="c" * 40, seed=808, count=12)
        packet2, key2 = build_japanese_packet(self._judgments(), scenarios, candidate_revision="c" * 40, seed=808, count=12)
        self.assertEqual((packet, key), (packet2, key2))
        self.assertEqual(len(packet["pairs"]), 12)
        public = json.dumps(packet, ensure_ascii=False)
        self.assertNotIn("candidate", public.lower())
        self.assertNotIn("current", public.lower())
        self.assertNotIn("gpt", public.lower())
        template = human_response_template(packet)
        self.assertEqual(template["reviewer_role"], "project-owner")
        self.assertEqual(len(template["reviews"]), 12)
        self.assertIsNone(template["reviews"][0]["preference"])

    def test_score_regression_counts_even_when_preference_is_tie(self):
        scenarios = {f"ja-{i}": {"source_text": f"原文{i}", "output_contract": "本文のみ"} for i in range(5)}
        packet, key = build_japanese_packet(self._judgments(), scenarios, candidate_revision="c" * 40, seed=808, count=12)
        response = human_response_template(packet)
        for review, assignment in zip(response["reviews"], key["pairs"]):
            candidate_key = "output_" + assignment["candidate_label"].lower()
            current_key = "output_" + assignment["current_label"].lower()
            review[candidate_key] = {"first_pass_understanding": 4, "naturalness": 5, "preservation": 5, "critical_meaning_change": False}
            review[current_key] = {"first_pass_understanding": 5, "naturalness": 5, "preservation": 5, "critical_meaning_change": False}
            review["preference"] = "tie"
        imported = import_human_response(packet, key, response)
        self.assertEqual(imported["candidate_regressions"], 12)
        self.assertEqual(imported["candidate_regression_rate"], 1.0)
        self.assertIn("critical_preservation", imported["calibration"])

    def test_import_rejects_missing_pairs(self):
        scenarios = {f"ja-{i}": {"source_text": f"原文{i}", "output_contract": "本文のみ"} for i in range(5)}
        packet, key = build_japanese_packet(self._judgments(), scenarios, candidate_revision="c" * 40, seed=808, count=12)
        response = {"packet_sha256": key["packet_sha256"], "reviewer_role": "project-owner", "owner_attestation": True, "reviews": []}
        with self.assertRaisesRegex(ValueError, "exactly"):
            import_human_response(packet, key, response)
        with self.assertRaisesRegex(ValueError, "top-level"):
            import_human_response(packet, key, {**response, "condition": "candidate"})
        with self.assertRaisesRegex(ValueError, "attestation"):
            import_human_response(packet, key, {**response, "owner_attestation": False})


if __name__ == "__main__":
    unittest.main()
