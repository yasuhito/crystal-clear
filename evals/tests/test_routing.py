import json
import tempfile
import unittest
from pathlib import Path

from evals.run_routing import (
    classify_selection_outcome,
    load_routing_scenarios,
    render_routing_markdown,
    summarize_routing_results,
    validate_result_set,
)


SCENARIOS = Path(__file__).resolve().parents[1] / "routing-scenarios.json"


class FrozenScenarioTests(unittest.TestCase):
    def test_frozen_set_has_required_shape_and_split(self) -> None:
        scenario_set = load_routing_scenarios(SCENARIOS)
        scenarios = scenario_set["scenarios"]

        self.assertEqual(len(scenarios), 40)
        self.assertEqual(
            {category: sum(row["category"] == category for row in scenarios) for category in {
                "explicit-request",
                "complex-communication",
                "unrelated-control",
                "boundary",
            }},
            {
                "explicit-request": 10,
                "complex-communication": 10,
                "unrelated-control": 10,
                "boundary": 10,
            },
        )
        self.assertEqual(sum(row["split"] == "held-out" for row in scenarios), 12)
        self.assertEqual(sum(row["split"] == "train" for row in scenarios), 28)
        self.assertEqual(len({row["id"] for row in scenarios}), 40)
        required = {
            "id",
            "language",
            "category",
            "split",
            "expected_activation",
            "rationale",
            "prompt",
        }
        for scenario in scenarios:
            self.assertFalse(required - scenario.keys(), scenario["id"])
            if scenario["split"] == "held-out":
                self.assertIn("paraphrase_of", scenario)

    def test_report_rejects_a_partial_result_set(self) -> None:
        scenario_set = load_routing_scenarios(SCENARIOS)
        with self.assertRaisesRegex(ValueError, "incomplete or stale"):
            validate_result_set(
                output=Path("/tmp/missing"),
                environment="pinned",
                results=[],
                scenario_set=scenario_set,
                repeats=5,
            )

    def test_rejects_an_invalid_frozen_set(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "invalid.json"
            path.write_text(json.dumps({"version": "v1", "scenarios": []}))
            with self.assertRaisesRegex(ValueError, "exactly 40"):
                load_routing_scenarios(path)


class RoutingReportTests(unittest.TestCase):
    def result(
        self,
        *,
        scenario_id: str,
        category: str,
        expected: bool,
        activated: bool,
        split: str = "train",
        repeat: int = 1,
        environment: str = "pinned",
    ) -> dict:
        return {
            "scenario_id": scenario_id,
            "category": category,
            "split": split,
            "language": "en",
            "repeat": repeat,
            "environment": environment,
            "expected_activation": expected,
            "activation": {"automatic": activated},
            "selection_outcome": "selected-with-visible-change" if activated else "not-selected",
            "trace_file": f"raw/{scenario_id}-{repeat}.trace.jsonl",
        }

    def test_summary_reports_recall_false_positives_categories_and_splits(self) -> None:
        results = [
            self.result(
                scenario_id="explicit-a",
                category="explicit-request",
                expected=True,
                activated=True,
            ),
            self.result(
                scenario_id="complex-a",
                category="complex-communication",
                expected=True,
                activated=False,
                split="held-out",
            ),
            self.result(
                scenario_id="control-a",
                category="unrelated-control",
                expected=False,
                activated=True,
            ),
            self.result(
                scenario_id="boundary-a",
                category="boundary",
                expected=False,
                activated=False,
                split="held-out",
            ),
        ]

        summary = summarize_routing_results(results)

        self.assertEqual(summary["overall"]["recall"], 0.5)
        self.assertEqual(summary["overall"]["precision"], 0.5)
        self.assertEqual(summary["overall"]["false_positive_rate"], 0.5)
        self.assertEqual(summary["categories"]["explicit-request"]["recall"], 1.0)
        self.assertEqual(summary["categories"]["unrelated-control"]["false_positive_rate"], 1.0)
        self.assertEqual(summary["splits"]["held-out"]["runs"], 2)
        self.assertEqual(summary["selection_outcomes"]["not-selected"], 2)

    def test_report_labels_formal_inventory_and_links_raw_evidence(self) -> None:
        result = self.result(
            scenario_id="explicit-a",
            category="explicit-request",
            expected=True,
            activated=True,
        )
        result["result_file"] = "raw/explicit-a-1.result.json"
        report = render_routing_markdown(
            summary=summarize_routing_results([result]),
            results=[result],
            environment="pinned",
            inventory_role="formal",
            scenario_version="routing-v1",
            skill_ref="178eaf8",
            inventory_snapshot="pinned-v1",
        )

        self.assertIn("only result eligible", report)
        self.assertIn("Precision: 100.0%", report)
        self.assertIn("[trace](raw/explicit-a-1.trace.jsonl)", report)
        self.assertIn("[result](raw/explicit-a-1.result.json)", report)

    def test_selection_outcome_distinguishes_unchanged_selected_output(self) -> None:
        self.assertEqual(
            classify_selection_outcome(False, "source", "source"),
            "not-selected",
        )
        self.assertEqual(
            classify_selection_outcome(True, "Same sentence.", "Same sentence."),
            "selected-with-little-visible-change",
        )
        self.assertEqual(
            classify_selection_outcome(True, "Same sentence.", "A clearer sentence."),
            "selected-with-visible-change",
        )
        self.assertEqual(
            classify_selection_outcome(True, None, "A generated answer."),
            "selected-effect-not-deterministically-assessed",
        )


if __name__ == "__main__":
    unittest.main()
