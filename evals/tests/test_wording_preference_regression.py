from __future__ import annotations

import unittest

from evals.run_wording_preference_regression import english_qualification_reasons, german_terminology_reasons


class WordingPreferenceTests(unittest.TestCase):
    def test_accepts_natural_english_exclusive_subject(self) -> None:
        outputs = (
            "Only customers with Enterprise accounts created after January 1, 2025, can restore archived workspaces. Restoration may take up to 48 hours.",
            "Only customers whose Enterprise accounts were created after 1 January 2025 can restore archived workspaces. Recovery can take as long as 48 hours.",
        )
        for output in outputs:
            with self.subTest(output=output):
                self.assertEqual(english_qualification_reasons(output), [])

    def test_rejects_awkward_or_semantically_changed_english_qualification(self) -> None:
        outputs = (
            "Customers can restore archived workspaces only for Enterprise accounts created after January 1, 2025. Recovery may take up to 48 hours.",
            "Only customers with Enterprise accounts created before January 1, 2025, can restore archived workspaces. Restoration may take up to 48 hours.",
            "Only customers with Enterprise accounts created after January 1, 2025, can restore archived workspaces. Restoration takes 48 hours.",
            "Only customers with Enterprise accounts created after January 1, 2025, can restore archived workspaces. Restoration may take up to 48 hours, but it will always take exactly 48 hours.",
            "Only customers with Enterprise accounts created after January 1, 2025, can restore archived workspaces. Recovery may take up to 48 hours only for deleted files.",
        )
        for output in outputs:
            with self.subTest(output=output):
                self.assertTrue(english_qualification_reasons(output))

    def test_accepts_german_term_unification_without_behavior_rewrite(self) -> None:
        outputs = (
            "Aktivieren Sie die Datenprüfung in den Einstellungen. Die Datenprüfung untersucht neue Uploads. Die Datenprüfung prüft keine vorhandenen Dateien.",
            "Aktivieren Sie in den Einstellungen die Datenprüfung. Neue Uploads untersucht die Datenprüfung. Vorhandene Dateien prüft die Datenprüfung nicht.",
        )
        for output in outputs:
            with self.subTest(output=output):
                self.assertEqual(german_terminology_reasons(output), [])

    def test_rejects_added_instruction_or_changed_german_polarity(self) -> None:
        outputs = (
            "Aktivieren Sie die Datenprüfung in den Einstellungen. Die Datenprüfung untersucht neue Uploads. Beachten Sie, dass die Datenprüfung keine vorhandenen Dateien untersucht.",
            "Aktivieren Sie die Datenprüfung in den Einstellungen. Die Datenprüfung untersucht keine neuen Uploads. Die Datenprüfung prüft keine vorhandenen Dateien.",
            "Aktivieren Sie die Datenprüfung in den Einstellungen. Die Datenprüfung untersucht neue Uploads. Die Datenprüfung prüft vorhandene Dateien.",
            "Aktivieren Sie die Datenprüfung nicht in den Einstellungen. Die Datenprüfung untersucht neue Uploads. Die Datenprüfung prüft keine vorhandenen Dateien.",
            "Aktivieren Sie die Datenprüfung in den Einstellungen. Die Datenprüfung untersucht neue Uploads nicht. Die Datenprüfung prüft keine vorhandenen Dateien.",
            "Aktivieren Sie die Datenprüfung in den Einstellungen. Das Prüfwerkzeug untersucht neue Uploads. Der Scanner prüft keine vorhandenen Dateien.",
        )
        for output in outputs:
            with self.subTest(output=output):
                self.assertTrue(german_terminology_reasons(output))


if __name__ == "__main__":
    unittest.main()
