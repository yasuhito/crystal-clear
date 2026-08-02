import json
import re
import unittest
from collections import defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES_PATH = REPO_ROOT / "evals" / "use-case-fixtures.json"
RECIPES_PATH = REPO_ROOT / "references" / "use-cases.md"
SKILL_PATH = REPO_ROOT / "SKILL.md"

EXPECTED_RECIPES = {
    "direct-answers": "Direct answers",
    "documentation-and-procedures": "Documentation and procedures",
    "errors-and-support": "Errors and support",
    "incidents-and-status-updates": "Incidents and status updates",
    "proposals-and-decision-memos": "Proposals and decision memos",
    "emails-and-requests": "Emails and requests",
    "japanese-business-prose": "Japanese business prose",
    "bilingual-and-localized-text": "Bilingual and localized text",
    "agent-facing-instructions": "Agent-facing instructions",
    "voice-sensitive-creative-text": "Voice-sensitive creative text",
}


class UseCaseFixtureTests(unittest.TestCase):
    def test_each_published_recipe_has_positive_and_preservation_coverage(self):
        document = json.loads(FIXTURES_PATH.read_text())
        fixtures = document["fixtures"]
        coverage = defaultdict(set)
        ids = []

        for fixture in fixtures:
            ids.append(fixture["id"])
            coverage[fixture["recipe"]].add(fixture["kind"])
            self.assertTrue(fixture["prompt"])
            self.assertTrue(fixture["expected_properties"])
            self.assertTrue(fixture["preserve"])

        self.assertEqual(document["version"], "use-cases-v1")
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(set(coverage), set(EXPECTED_RECIPES))
        for recipe, kinds in coverage.items():
            self.assertIn("positive", kinds, recipe)
            self.assertTrue(kinds & {"preservation", "boundary"}, recipe)

    def test_fixture_recipes_match_reference_sections(self):
        headings = set(re.findall(r"^## (.+)$", RECIPES_PATH.read_text(), re.MULTILINE))
        self.assertEqual(headings, set(EXPECTED_RECIPES.values()))

    def test_core_keeps_short_tasks_out_of_genre_reference(self):
        skill = SKILL_PATH.read_text()
        self.assertIn("The core is sufficient for short tasks", skill)
        self.assertIn("Do not load the recipes for a short task", skill)


if __name__ == "__main__":
    unittest.main()
