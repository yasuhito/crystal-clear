from __future__ import annotations

import unittest

from evals.run_spanish_scope_regression import (
    review_fact_reasons,
    scope_change_reasons,
    scope_narrowing_reasons,
)


class SpanishScopePreservationTests(unittest.TestCase):
    def test_accepts_general_migration_prohibition(self) -> None:
        output = (
            "Ana, aprueba Proyecto Faro antes del 3 de mayo. Hemos revisado varias opciones durante dos semanas y el "
            "sistema anterior seguirá disponible. No se debe iniciar la migración sin la aprobación de Seguridad."
        )
        self.assertEqual(scope_change_reasons(output), [])

    def test_accepts_natural_impersonal_paraphrases(self) -> None:
        outputs = (
            "Necesitamos que Ana apruebe Proyecto Faro antes del 3 de mayo. Tras revisar opciones durante dos semanas, "
            "el sistema anterior permanecerá disponible. La migración no debe iniciarse sin el visto bueno de Seguridad.",
            "Ana debe aprobar Proyecto Faro antes del 3 de mayo. Revisamos opciones durante dos semanas y el sistema "
            "anterior continuará disponible. La migración solo puede iniciarse con la aprobación de Seguridad.",
            "Solicitamos que Ana apruebe Proyecto Faro antes del 3 de mayo. Tras revisar opciones durante dos semanas, "
            "el sistema anterior seguirá disponible y la migración no deberá iniciarse sin la aprobación de Seguridad.",
            "Ana debe aprobar Proyecto Faro antes del 3 de mayo. Revisamos opciones durante dos semanas y el sistema "
            "anterior seguirá disponible. Tras la aprobación de Seguridad, podrá iniciarse la migración.",
            "Necesitamos que Ana apruebe Proyecto Faro antes del 3 de mayo. No se puede iniciar la migración sin la "
            "aprobación de Seguridad. Revisamos opciones durante dos semanas y el sistema anterior seguirá disponible.",
            "Ana debe aprobar Proyecto Faro antes del 3 de mayo. Revisamos opciones durante dos semanas y el sistema "
            "anterior seguirá disponible. Solo se puede iniciar la migración con la aprobación de Seguridad.",
            "Ana debe aprobar Proyecto Faro antes del 3 de mayo. Revisamos opciones durante dos semanas y el sistema "
            "anterior seguirá disponible. La migración solo se iniciará con la aprobación de Seguridad.",
        )
        for output in outputs:
            with self.subTest(output=output):
                self.assertEqual(scope_change_reasons(output), [])

    def test_rejects_reversed_or_negated_frozen_facts(self) -> None:
        outputs = (
            "No necesitamos que Ana apruebe Proyecto Faro antes del 3 de mayo. No se debe iniciar la migración sin la aprobación de Seguridad. No hemos revisado opciones durante dos semanas. El sistema anterior no seguirá disponible.",
            "Ana debe aprobar Proyecto Faro antes del 3 de mayo. La migración solo puede iniciarse sin la aprobación de Seguridad. Revisamos opciones durante dos semanas. El sistema anterior seguirá disponible.",
        )
        for output in outputs:
            with self.subTest(output=output):
                self.assertTrue(scope_change_reasons(output))

    def test_review_fact_oracle_requires_duration_action_and_object(self) -> None:
        valid_outputs = (
            "Tras dos semanas revisando varias opciones, seguimos adelante.",
            "Durante dos semanas hemos revisado varias opciones.",
            "Durante dos semanas, hemos estado revisando varias opciones.",
        )
        invalid = (
            "Tras dos semanas de revisión, seguimos adelante.",
            "Revisamos varias opciones, seguimos adelante.",
            "No hemos revisado opciones durante dos semanas.",
            "No se revisaron opciones durante dos semanas.",
            "Revisamos el sistema anterior durante dos semanas. Había varias opciones.",
            "Revisamos opciones. El sistema anterior estuvo disponible dos semanas.",
            "Durante dos semanas el sistema anterior seguirá disponible. Revisamos opciones.",
            "Tras dos semanas sin revisar opciones, seguimos adelante.",
            "Durante dos semanas esperamos, revisamos opciones.",
            "Revisamos el sistema durante dos semanas y luego revisamos opciones.",
            "El sistema estuvo disponible durante dos semanas, revisamos opciones.",
        )
        for output in valid_outputs:
            with self.subTest(output=output):
                self.assertEqual(review_fact_reasons(output), [])
        for output in invalid:
            with self.subTest(output=output):
                self.assertIn("missing-two-week-review", review_fact_reasons(output))

    def test_scope_oracle_ignores_unrelated_fact_omission(self) -> None:
        output = (
            "Ana debe aprobar Proyecto Faro antes del 3 de mayo. "
            "La migración no debe iniciarse sin la aprobación de Seguridad."
        )
        self.assertEqual(scope_narrowing_reasons(output), [])
        self.assertIn("missing-two-week-review", scope_change_reasons(output))

    def test_rejects_observed_prohibition_narrowing(self) -> None:
        output = (
            "Ana, aprueba Proyecto Faro antes del 3 de mayo; no inicies la migración sin la aprobación de Seguridad. "
            "El sistema anterior seguirá disponible tras dos semanas de revisión de varias opciones."
        )
        reasons = scope_change_reasons(output)
        self.assertIn("general-prohibition-narrowed-to-ana", reasons)
        self.assertIn("missing-general-security-prohibition", reasons)

    def test_rejects_equivalent_ana_specific_prohibitions(self) -> None:
        endings = (
            "Ana no debe iniciar la migración sin la aprobación de Seguridad.",
            "Ana no puede iniciar la migración sin la aprobación de Seguridad.",
            "No inicie la migración sin la aprobación de Seguridad.",
            "Ana debe aprobar Proyecto Faro antes del 3 de mayo y no iniciar la migración sin la aprobación de Seguridad.",
        )
        prefix = (
            "Ana debe aprobar Proyecto Faro antes del 3 de mayo. Revisamos opciones durante dos semanas y el sistema "
            "anterior seguirá disponible. "
        )
        for ending in endings:
            with self.subTest(ending=ending):
                self.assertIn("general-prohibition-narrowed-to-ana", scope_change_reasons(prefix + ending))


if __name__ == "__main__":
    unittest.main()
