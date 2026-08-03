from __future__ import annotations

import unittest

from evals.run_arabic_exclusivity_regression import exclusivity_reasons


class ArabicExclusivityTests(unittest.TestCase):
    def test_accepts_natural_exclusive_plan_phrasings(self) -> None:
        outputs = (
            "في خطة Pro فقط، يمكن استعادة الملفات المحذوفة إذا قُدِّم الطلب خلال 14 يومًا، وقد تستغرق الاستعادة حتى 24 ساعة.",
            "لا تتوفر استعادة الملفات المحذوفة إلا في خطة Pro إذا قُدِّم الطلب خلال 14 يومًا، وقد تستغرق عملية الاستعادة حتى 24 ساعة.",
            "لا يمكن استعادة الملفات المحذوفة إلا في خطة Pro إذا قُدِّم الطلب خلال 14 يومًا، وقد تستغرق الاستعادة حتى 24 ساعة.",
            "تقتصر استعادة الملفات المحذوفة على خطة Pro، بشرط تقديم الطلب خلال 14 يومًا، وقد تستغرق الاستعادة حتى 24 ساعة.",
        )
        for output in outputs:
            with self.subTest(output=output):
                self.assertEqual(exclusivity_reasons(output), [])

    def test_rejects_omitted_or_broadened_exclusivity(self) -> None:
        outputs = (
            "في خطة Pro، يمكن استعادة الملفات المحذوفة إذا قُدِّم الطلب خلال 14 يومًا، وقد تستغرق الاستعادة حتى 24 ساعة.",
            "يمكن استعادة الملفات المحذوفة، وليس فقط في خطة Pro، إذا قُدِّم الطلب خلال 14 يومًا، وقد تستغرق الاستعادة حتى 24 ساعة.",
            "يمكن استعادة الملفات المحذوفة في خطة Pro وغيرها إذا قُدِّم الطلب خلال 14 يومًا، وقد تستغرق الاستعادة حتى 24 ساعة.",
            "يمكن استعادة الملفات المحذوفة في خطة Pro فقط، وكذلك في خطة Enterprise، إذا قُدِّم الطلب خلال 14 يومًا، وقد تستغرق الاستعادة حتى 24 ساعة.",
        )
        for output in outputs:
            with self.subTest(output=output):
                self.assertIn("missing-pro-plan-exclusivity", exclusivity_reasons(output))

    def test_rejects_polarity_scope_and_uncertainty_changes(self) -> None:
        outputs = (
            "في خطة Pro فقط، لا يمكن استعادة الملفات المحذوفة إذا قُدِّم الطلب خلال 14 يومًا، وقد تستغرق الاستعادة حتى 24 ساعة.",
            "في خطة Pro فقط، يمكن استعادة الملفات المحذوفة إذا لم يُقدَّم الطلب خلال 14 يومًا، وقد تستغرق الاستعادة حتى 24 ساعة.",
            "في خطة Pro فقط، يمكن استعادة الملفات المحذوفة إذا قُدِّم الطلب بعد 14 يومًا، وقد تستغرق الاستعادة حتى 24 ساعة.",
            "في خطة Pro فقط، يمكن استعادة الملفات المحذوفة إذا قُدِّم الطلب خلال 14 يومًا، وستستغرق الاستعادة 24 ساعة.",
            "في خطة Pro فقط، يمكن استعادة الملفات المحذوفة إذا رُفض الطلب خلال 14 يومًا، وقد تستغرق الاستعادة حتى 24 ساعة.",
            "في خطة Pro فقط، يمكن استعادة الملفات المحذوفة إذا استغرقت الاستعادة 14 يومًا، وقد يُقدَّم الطلب خلال 24 ساعة.",
            "في خطة Pro فقط، يمكن استعادة الملفات المحذوفة إذا قُدِّم الطلب خلال 14 يومًا، وقد تستغرق الاستعادة أكثر من 24 ساعة.",
        )
        for output in outputs:
            with self.subTest(output=output):
                self.assertTrue(exclusivity_reasons(output))


if __name__ == "__main__":
    unittest.main()
