import unittest

from evals.compare_routing_candidates import assess_candidate, choose_candidate


def metric(*, recall=None, false_positive_rate=None, true_positives=0, false_positives=0, positive_runs=0, negative_runs=0):
    return {
        "recall": recall,
        "false_positive_rate": false_positive_rate,
        "true_positives": true_positives,
        "false_positives": false_positives,
        "positive_runs": positive_runs,
        "negative_runs": negative_runs,
    }


def summary(explicit_recall, complex_recall, control_fpr, boundary):
    return {
        "category_splits": {
            "explicit-request": {"held-out": metric(recall=explicit_recall, true_positives=15, positive_runs=15)},
            "complex-communication": {"held-out": metric(recall=complex_recall, true_positives=13, positive_runs=15)},
            "unrelated-control": {"held-out": metric(false_positive_rate=control_fpr, false_positives=1, negative_runs=15)},
            "boundary": {"held-out": boundary},
        }
    }


class CandidateAcceptanceTests(unittest.TestCase):
    def test_assessment_applies_only_precommitted_held_out_thresholds(self) -> None:
        result = assess_candidate(
            summary(1.0, 0.8667, 0.0667, metric(recall=1.0, false_positive_rate=0.1)),
            description_length=600,
        )
        self.assertTrue(result["passes"])
        self.assertEqual(result["held_out"]["explicit_request_recall"], 1.0)
        self.assertIn("boundary", result["held_out"])

    def test_failed_candidate_is_not_silently_selected(self) -> None:
        candidates = [
            {"id": "concrete", "description": "x" * 600, "assessment": {"passes": False, "held_out_correct": 44}},
            {"id": "short", "description": "x" * 500, "assessment": {"passes": False, "held_out_correct": 45}},
        ]
        self.assertIsNone(choose_candidate(candidates))

    def test_selection_uses_held_out_correct_runs_then_shorter_tie_breaker(self) -> None:
        candidates = [
            {"id": "concrete", "description": "x" * 600, "assessment": {"passes": True, "held_out_correct": 44}},
            {"id": "short", "description": "x" * 500, "assessment": {"passes": True, "held_out_correct": 45}},
        ]
        self.assertEqual(choose_candidate(candidates)["id"], "short")

        candidates[0]["assessment"]["held_out_correct"] = 45
        self.assertEqual(choose_candidate(candidates)["id"], "short")


if __name__ == "__main__":
    unittest.main()
