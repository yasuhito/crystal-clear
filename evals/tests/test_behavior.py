import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from evals.run_japanese_regression import has_meaning_change, meaning_change_reasons
from evals.run_behavior import (
    _judge_prompt,
    assign_blind_pairs,
    load_behavior_scenarios,
    parse_judgment,
    render_behavior_markdown,
    score_preservation,
    summarize_behavior,
)


FIXTURE = Path(__file__).resolve().parents[1] / "behavior-scenarios.json"


class BehaviorScenarioTests(unittest.TestCase):
    def test_frozen_fixture_has_required_coverage(self) -> None:
        data = load_behavior_scenarios(FIXTURE)
        rows = data["scenarios"]
        self.assertEqual(Counter(row["category"] for row in rows), {
            "english": 5, "japanese": 5, "multilingual-core": 5
        })
        self.assertEqual(
            {row["language"] for row in rows if row["category"] == "multilingual-core"},
            {"es", "zh-CN", "ar", "de", "mixed-ja-en"},
        )
        self.assertEqual(
            {mode for row in rows for mode in row["failure_modes"]},
            {"buried-answer", "ambiguous-referent", "detached-qualification", "terminology-drift", "register-mismatch", "accidental-certainty-change"},
        )
        self.assertEqual(
            {check["kind"] for row in rows for check in row["checks"]},
            {"protected-string", "fact", "number", "constraint", "condition"},
        )
        for row in rows:
            self.assertIn(row["source_text"], row["prompt"])
            self.assertIn(row["output_contract"], row["prompt"])

    def test_rejects_wrong_category_count(self) -> None:
        data = json.loads(FIXTURE.read_text())
        data["scenarios"].pop()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, "five scenarios"):
                load_behavior_scenarios(path)


class MeaningChangeReproTests(unittest.TestCase):
    SAFE = "佐藤さんは鈴木さんに、『レビュー後に鈴木さんが案件ID JP-42の報告書を送る』と伝えました。佐藤さんは承認を担当します。"

    def test_detects_observed_and_adversarial_meaning_changes(self) -> None:
        cases = {
            "instruction": self.SAFE.replace("送る』と", "送るよう』と"),
            "reversed attribution": self.SAFE.replace("佐藤さんは鈴木さんに", "鈴木さんは佐藤さんに"),
            "expanded attribution": "佐藤さんは鈴木さんに、『レビュー後に鈴木さんが案件ID JP-42の報告書を送り、佐藤さんが承認する』と伝えました。",
            "invented order": self.SAFE.replace("レビュー後に", "佐藤さんの承認後に"),
            "missing id": self.SAFE.replace("案件ID JP-42の", ""),
            "missing timing": self.SAFE.replace("レビュー後に", ""),
            "bare assertion": "レビュー後に鈴木さんが案件ID JP-42の報告書を送ります。佐藤さんは承認を担当します。",
        }
        for label, output in cases.items():
            with self.subTest(label=label):
                self.assertTrue(meaning_change_reasons(output))

    def test_accepts_report_that_preserves_all_invariants(self) -> None:
        outputs = (
            self.SAFE,
            "佐藤さんは鈴木さんに、『レビュー後に鈴木さんが案件ID JP-42の報告書を送る』と伝えました。佐藤さんによる承認のタイミングは明記されていません。",
        )
        for output in outputs:
            with self.subTest(output=output):
                self.assertFalse(has_meaning_change(output))


class DeterministicScoringTests(unittest.TestCase):
    def test_scores_each_required_literal_and_kind(self) -> None:
        scenario = {
            "checks": [
                {"id": "id", "kind": "protected-string", "values": ["API-17"]},
                {"id": "condition", "kind": "condition", "values": ["only if", "Friday"]},
            ]
        }
        score = score_preservation(scenario, "API-17 applies only if approved.")
        self.assertTrue(score["output_present"])
        self.assertFalse(score["passed"])
        self.assertEqual(score["failures_by_kind"], {"condition": 1})
        self.assertEqual(score["checks"][1]["missing"], ["Friday"])

    def test_relational_fact_check_rejects_reversed_roles(self) -> None:
        scenario = {
            "checks": [{
                "id": "roles", "kind": "fact",
                "values": ["Priya must export the audit log", "Maya retains access"],
            }]
        }
        score = score_preservation(
            scenario,
            "Maya must export the audit log. Priya retains access.",
        )
        self.assertFalse(score["passed"])
        self.assertEqual(score["failures_by_kind"], {"fact": 1})


class BlindJudgmentTests(unittest.TestCase):
    def test_assignment_is_seeded_and_balanced(self) -> None:
        pairs = [(f"s{i:02}", repeat) for i in range(15) for repeat in range(1, 6)]
        first = assign_blind_pairs(pairs, seed=178, skill_arm="178eaf8")
        second = assign_blind_pairs(pairs, seed=178, skill_arm="178eaf8")
        self.assertEqual(first, second)
        self.assertNotEqual(first, assign_blind_pairs(pairs, seed=179, skill_arm="178eaf8"))
        self.assertLessEqual(abs(Counter(row["a_arm"] for row in first)["178eaf8"] - Counter(row["b_arm"] for row in first)["178eaf8"]), 1)

    def test_parses_strict_judgment_and_disallows_multilingual_naturalness(self) -> None:
        payload = {
            "output_a": {"critical_preservation_failure": False, "critical_failure_types": [], "preservation": 5, "first_pass_understanding": None, "core_structure": 4, "referent_scope_terminology": None, "register_preserved": None, "naturalness": None, "evidence": "Preserves the stated condition."},
            "output_b": {"critical_preservation_failure": True, "critical_failure_types": ["changed-certainty"], "preservation": 2, "first_pass_understanding": None, "core_structure": 5, "referent_scope_terminology": None, "register_preserved": None, "naturalness": None, "evidence": "Turns possibility into certainty."},
            "preference": "A",
            "preference_evidence": "A preserves meaning.",
        }
        self.assertEqual(parse_judgment(json.dumps(payload), "multilingual-core"), payload)
        payload["output_a"]["naturalness"] = 4
        with self.assertRaisesRegex(ValueError, "naturalness"):
            parse_judgment(json.dumps(payload), "multilingual-core")

    def test_judge_prompt_matches_each_category_schema(self) -> None:
        english = {"category": "english", "source_text": "source", "output_contract": "contract"}
        multilingual = {"category": "multilingual-core", "source_text": "source", "output_contract": "contract"}
        self.assertIn('"naturalness":1', _judge_prompt(english, "A", "B"))
        self.assertIn('"first_pass_understanding":null', _judge_prompt(multilingual, "A", "B"))


class BehaviorReportTests(unittest.TestCase):
    def test_three_arm_summary_does_not_attribute_judgment_to_uncompared_arm(self) -> None:
        score = {"critical_preservation_failure": False, "critical_failure_types": [], "preservation": 5, "first_pass_understanding": 5, "core_structure": 5, "referent_scope_terminology": 5, "register_preserved": True, "naturalness": 5, "evidence": "ok"}
        generations = [
            {"scenario_id": "s", "category": "english", "arm": arm, "repeat": 1, "deterministic_score": {"output_present": True, "failures_by_kind": {}}}
            for arm in ("no-skill", "current", "candidate")
        ]
        judgments = [{"category": "english", "a_arm": "current", "b_arm": "candidate", "judgment": {"output_a": score, "output_b": score, "preference": "tie"}}]
        summary = summarize_behavior(generations, judgments)
        self.assertEqual(summary["categories"]["english"]["arms"]["no-skill"]["gpt_judged"]["outputs"], 0)
        self.assertEqual(summary["categories"]["english"]["arms"]["current"]["gpt_judged"]["outputs"], 1)
        self.assertEqual(summary["categories"]["english"]["arms"]["candidate"]["gpt_judged"]["outputs"], 1)

    def test_summary_and_report_separate_evidence_and_categories(self) -> None:
        rows = []
        judgments = []
        for index, category in enumerate(("english", "japanese", "multilingual-core"), 1):
            for arm in ("no-skill", "178eaf8"):
                rows.append({"scenario_id": f"s{index}", "category": category, "arm": arm, "repeat": 1, "result_file": "generation.json", "trace_file": "generation.jsonl", "deterministic_score": {"output_present": True, "passed": True, "checks": [], "failures_by_kind": {}}})
            judgments.append({
                "pair_id": f"s{index}--r01", "presentation_index": index,
                "category": category, "result_file": "judgment.json", "trace_file": "judgment.jsonl",
                "a_arm": "no-skill", "b_arm": "178eaf8",
                "judgment": {
                    "output_a": {"critical_preservation_failure": False, "critical_failure_types": [], "preservation": 4, "first_pass_understanding": 3, "core_structure": 3, "referent_scope_terminology": 4, "register_preserved": True, "naturalness": None if category == "multilingual-core" else 4, "evidence": "ok"},
                    "output_b": {"critical_preservation_failure": False, "critical_failure_types": [], "preservation": 5, "first_pass_understanding": 4, "core_structure": 4, "referent_scope_terminology": 5, "register_preserved": True, "naturalness": None if category == "multilingual-core" else 4, "evidence": "clear"},
                    "preference": "B", "preference_evidence": "clearer"
                }
            })
        summary = summarize_behavior(rows, judgments)
        markdown = render_behavior_markdown(summary, rows, judgments, scenario_version="behavior-v1", skill_ref="178eaf8", repeats=5)
        self.assertEqual(set(summary["categories"]), {"english", "japanese", "multilingual-core"})
        self.assertIn("Deterministic evidence", markdown)
        self.assertIn("GPT-judged evidence", markdown)
        self.assertIn("Human-reviewed evidence", markdown)
        self.assertIn("no native-naturalness claim", markdown)
        self.assertNotIn("Overall score", markdown)


if __name__ == "__main__":
    unittest.main()
