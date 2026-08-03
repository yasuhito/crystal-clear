from __future__ import annotations

import unittest

from evals.run_semantic_regression import modality_change_reasons


class RecommendationModalityTests(unittest.TestCase):
    def test_accepts_preserved_recommendation_and_constraints(self) -> None:
        output = (
            "After several weeks of discussion and a risk review, we recommend approving Project Northstar by 14 June. "
            "The legacy exporter remains available, and rollout must not begin until security signs off."
        )
        self.assertEqual(modality_change_reasons(output), [])

    def test_accepts_valid_recommendation_paraphrase(self) -> None:
        outputs = (
            "After several weeks of discussion and a risk review, our advice is to approve Project Northstar "
            "by 14 June. The legacy exporter is available, and rollout can begin only after security signs off.",
            "After several weeks of discussion and a review of the risks, we recommend approving Project Northstar "
            "by 14 June, provided that rollout does not begin until security signs off; the legacy exporter remains available.",
        )
        for output in outputs:
            with self.subTest(output=output):
                self.assertEqual(modality_change_reasons(output), [])

    def test_rejects_observed_recommendation_to_directive_change(self) -> None:
        output = (
            "Approve Project Northstar by 14 June, following several weeks of discussion and a risk review; "
            "however, rollout must not begin before security signs off, and the legacy exporter remains available."
        )
        reasons = modality_change_reasons(output)
        self.assertIn("missing-positive-approval-recommendation", reasons)
        self.assertIn("recommendation-became-directive", reasons)

    def test_rejects_negated_recommendation(self) -> None:
        shared = (
            " Project Northstar by 14 June after several weeks of discussion and a risk review. "
            "The legacy exporter remains available, and rollout must not begin until security signs off."
        )
        for opening in (
            "We do not recommend approving",
            "Our advice is not to approve",
            "We cannot recommend approving",
            "We can't recommend approving",
            "We never recommend approving",
            "We don't recommend approving",
        ):
            with self.subTest(opening=opening):
                self.assertIn(
                    "missing-positive-approval-recommendation",
                    modality_change_reasons(opening + shared),
                )

    def test_rejects_recommendation_detached_from_later_approval(self) -> None:
        output = (
            "After several weeks of discussion and a risk review, we recommend waiting; the board will later approve "
            "Project Northstar by 14 June. The legacy exporter remains available, and rollout must not begin until "
            "security signs off."
        )
        self.assertIn("missing-positive-approval-recommendation", modality_change_reasons(output))

    def test_rejects_detached_recommendation_token(self) -> None:
        output = (
            "Project Northstar: Approve by 14 June after several weeks of discussion and a risk review. "
            "This recommendation is concise. The legacy exporter remains available, and rollout must not begin until security signs off."
        )
        reasons = modality_change_reasons(output)
        self.assertIn("missing-positive-approval-recommendation", reasons)

    def test_rejects_reversed_availability_and_security_meaning(self) -> None:
        outputs = (
            "The legacy exporter is unavailable, and security must not sign off before rollout begins.",
            "No legacy exporter remains available, and rollout must not begin until security refuses to sign off.",
        )
        prefix = (
            "After several weeks of discussion and a risk review, we recommend approving Project Northstar by 14 June. "
        )
        for ending in outputs:
            with self.subTest(ending=ending):
                reasons = modality_change_reasons(prefix + ending)
                self.assertIn("legacy-exporter-not-available", reasons)
                self.assertIn("missing-rollout-security-condition", reasons)

    def test_rejects_omitted_or_negated_discussion_and_risk_review(self) -> None:
        details = (
            "",
            "The migration was not discussed for several weeks, and its risks were not reviewed. ",
            "The migration hasn't been discussed for several weeks, and its risks were not reviewed. ",
            "There has never been a discussion of the migration over several weeks, and its risks were not reviewed. ",
        )
        for detail in details:
            with self.subTest(detail=detail):
                output = (
                    detail
                    + "We recommend approving Project Northstar by 14 June. "
                    "The legacy exporter remains available, and rollout must not begin until security signs off."
                )
                reasons = modality_change_reasons(output)
                self.assertIn("missing-discussion-duration", reasons)
                self.assertIn("missing-risk-review", reasons)


if __name__ == "__main__":
    unittest.main()
