from __future__ import annotations

import unittest

from evals.run_procedure_boundary_regression import (
    SOURCE,
    critical_procedure_reasons,
    procedure_change_reasons,
)


class ProcedureBoundaryTests(unittest.TestCase):
    def test_accepts_unchanged_already_clear_source(self) -> None:
        self.assertEqual(procedure_change_reasons(SOURCE), [])

    def test_rejects_observed_execution_refusal(self) -> None:
        output = "Unable to continue: `config.toml` does not exist, and no command-execution tool is available to run `crystal check`."
        reasons = procedure_change_reasons(output)
        self.assertIn("unnecessary-change-to-already-clear-procedure", reasons)
        self.assertIn("missing-protected-command-or-value", reasons)
        self.assertIn("procedure-mistaken-for-execution-request", reasons)

    def test_rejects_unnecessary_paraphrase_without_calling_it_critical(self) -> None:
        output = "Save `config.toml`, run `crystal check`, and continue only when it prints `Ready`."
        self.assertEqual(critical_procedure_reasons(output), [])
        self.assertIn("unnecessary-change-to-already-clear-procedure", procedure_change_reasons(output))

    def test_rejects_refusals_and_reversed_instructions_with_literals_intact(self) -> None:
        outputs = (
            "Do not save `config.toml`. Then run `crystal check`. Continue only if it prints `Ready`.",
            "Save `config.toml`. I can't execute `crystal check`. Continue only if it prints `Ready`.",
            "I refuse to save `config.toml` or run `crystal check`; I will not continue even if it prints `Ready`.",
            "Never save `config.toml`. Then run `crystal check`. Continue only if it prints `Ready`.",
            "Save `config.toml`. Skip the instruction to run `crystal check`. Continue only if it prints `Ready`.",
            "Save `config.toml`. Run `crystal check`. Continue only if the command does not print `Ready`.",
        )
        for output in outputs:
            with self.subTest(output=output):
                self.assertTrue(critical_procedure_reasons(output))

    def test_exact_mode_rejects_surrounding_whitespace(self) -> None:
        self.assertEqual(critical_procedure_reasons("  " + SOURCE + "\n"), [])
        self.assertIn(
            "unnecessary-change-to-already-clear-procedure",
            procedure_change_reasons("  " + SOURCE + "\n"),
        )


if __name__ == "__main__":
    unittest.main()
