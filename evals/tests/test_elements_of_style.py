import hashlib
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from evals.run_reference_loading import elements_read_paths, validate_policy_result
from evals.skill_artifacts import discover_skill_artifacts, materialize_skill_artifacts
from scripts.generate_elements_of_style import (
    GENERATED_PATHS,
    estimate_tokens,
    parse_source,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
REFERENCE_ROOT = REPO_ROOT / "references" / "elements-of-style"
SOURCE = REFERENCE_ROOT / "source.md"
INDEX = REFERENCE_ROOT / "index.md"
LOADING_FIXTURE = REPO_ROOT / "evals" / "reference-loading-scenarios.json"
SOURCE_SHA256 = "d0edf854b5d39e22da68793603830e5bbdddb9266d272007993bcb821ba2799d"


class ElementsGeneratorTests(unittest.TestCase):
    def test_checked_in_outputs_are_reproducible_and_idempotent(self) -> None:
        command = [sys.executable, "scripts/generate_elements_of_style.py", "--check"]
        first = subprocess.run(command, cwd=REPO_ROOT, capture_output=True, text=True)
        self.assertEqual(first.returncode, 0, first.stderr)
        with tempfile.TemporaryDirectory() as tmp:
            generated = Path(tmp) / "elements-of-style"
            subprocess.run(
                [sys.executable, "scripts/generate_elements_of_style.py", "--output-root", str(generated)],
                cwd=REPO_ROOT,
                check=True,
            )
            before = {path.relative_to(generated): path.read_bytes() for path in generated.rglob("*.md")}
            subprocess.run(
                [sys.executable, "scripts/generate_elements_of_style.py", "--output-root", str(generated)],
                cwd=REPO_ROOT,
                check=True,
            )
            after = {path.relative_to(generated): path.read_bytes() for path in generated.rglob("*.md")}
            self.assertEqual(before, after)
            self.assertEqual(set(before), {Path(path) for path in GENERATED_PATHS})
            for relative, content in before.items():
                self.assertEqual(content, (REFERENCE_ROOT / relative).read_bytes())

    def test_check_rejects_and_generation_removes_stale_managed_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            generated = Path(tmp) / "elements-of-style"
            subprocess.run(
                [sys.executable, "scripts/generate_elements_of_style.py", "--output-root", str(generated)],
                cwd=REPO_ROOT,
                check=True,
            )
            stale = generated / "rules/stale.md"
            stale.write_text("stale")
            checked = subprocess.run(
                [sys.executable, "scripts/generate_elements_of_style.py", "--output-root", str(generated), "--check"],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(checked.returncode, 0)
            self.assertIn("extra:rules/stale.md", checked.stderr)
            subprocess.run(
                [sys.executable, "scripts/generate_elements_of_style.py", "--output-root", str(generated)],
                cwd=REPO_ROOT,
                check=True,
            )
            self.assertFalse(stale.exists())

    def test_source_moved_without_content_change_and_extracts_verbatim(self) -> None:
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest(), SOURCE_SHA256)
        parsed = parse_source(SOURCE.read_text())
        self.assertEqual(sorted(parsed.rules), list(range(1, 19)))
        self.assertEqual("".join(parsed.word_chunks.values()), parsed.section_v)
        for number, body in parsed.rules.items():
            self.assertEqual((REFERENCE_ROOT / f"rules/rule-{number:02d}.md").read_text(), body)
        for group, body in parsed.word_chunks.items():
            self.assertEqual((REFERENCE_ROOT / f"words/{group.lower()}.md").read_text(), body)

    def test_rules_and_section_v_terms_occur_exactly_once(self) -> None:
        generated_rules = "".join(
            (REFERENCE_ROOT / f"rules/rule-{number:02d}.md").read_text()
            for number in range(1, 19)
        )
        self.assertEqual(
            [int(value) for value in re.findall(r"^### Rule (\d+)\.", generated_rules, re.MULTILINE)],
            list(range(1, 19)),
        )
        parsed = parse_source(SOURCE.read_text())
        generated_words = "".join(
            (REFERENCE_ROOT / f"words/{group.lower()}.md").read_text()
            for group in ("A-F", "G-M", "N-S", "T-Z")
        )
        generated_terms = re.findall(r"^\*\*(.+?)\.\*\*", generated_words, re.MULTILINE)
        self.assertEqual(generated_terms, parsed.terms)
        self.assertEqual(len(generated_terms), len(set(generated_terms)))
        complete_index = INDEX.read_text().split("## Complete rule index", 1)[1].split("## Word usage", 1)[0]
        self.assertEqual(len(re.findall(r"^\| \[Rule \d+\.", complete_index, re.MULTILINE)), 18)
        self.assertEqual(
            sum(complete_index.count(tag) for tag in (
                "English-specific",
                "Transferable composition principle",
                "Transferable with caution",
            )),
            18,
        )

    def test_markdown_links_are_valid(self) -> None:
        link_pattern = re.compile(r"\[[^]]*\]\(([^)]+)\)")
        for document in [REPO_ROOT / "README.md", REPO_ROOT / "SKILL.md", *REFERENCE_ROOT.rglob("*.md")]:
            for target in link_pattern.findall(document.read_text()):
                if "://" in target or target.startswith("#"):
                    continue
                path_text = target.split("#", 1)[0]
                if path_text:
                    self.assertTrue((document.parent / path_text).resolve().exists(), f"broken link in {document}: {target}")

    def test_reference_budgets(self) -> None:
        source_tokens = estimate_tokens(SOURCE.read_text())
        index_tokens = estimate_tokens(INDEX.read_text())
        self.assertLessEqual(index_tokens, 1500)
        rule_tokens = [
            estimate_tokens((REFERENCE_ROOT / f"rules/rule-{number:02d}.md").read_text())
            for number in range(1, 19)
        ]
        self.assertTrue(all(tokens <= 1500 for tokens in rule_tokens))
        chunk_tokens = [
            estimate_tokens((REFERENCE_ROOT / f"words/{group}.md").read_text())
            for group in ("a-f", "g-m", "n-s", "t-z")
        ]
        selectable_tokens = [*rule_tokens, *chunk_tokens, estimate_tokens((REFERENCE_ROOT / "words/index.md").read_text())]
        worst_targeted = index_tokens + sum(sorted(selectable_tokens, reverse=True)[:2])
        self.assertLessEqual(worst_targeted, source_tokens * 0.30)
        managed = {
            path.relative_to(REFERENCE_ROOT).as_posix()
            for root in (REFERENCE_ROOT / "rules", REFERENCE_ROOT / "words")
            for path in root.rglob("*.md")
        }
        managed.add("index.md")
        self.assertEqual(managed, set(GENERATED_PATHS))


class ReferenceLoadingPolicyTests(unittest.TestCase):
    def test_trace_parser_and_policy_validation_use_observed_read_paths(self) -> None:
        scenario = {
            "id": "targeted",
            "mode": "targeted",
            "expected_reference_reads": [
                "references/elements-of-style/index.md",
                "references/elements-of-style/rules/rule-07.md",
            ],
        }
        events = [
            {"message": {"role": "assistant", "content": [
                {"type": "toolCall", "name": "read", "arguments": {"path": "/tmp/work/references/elements-of-style/index.md"}},
                {"type": "toolCall", "name": "read", "arguments": {"path": "/tmp/work/references/elements-of-style/rules/rule-07.md"}},
            ]}},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            trace = Path(tmp) / "trace.jsonl"
            trace.write_text("".join(json.dumps(event) + "\n" for event in events))
            reads = elements_read_paths(trace)
        self.assertEqual(reads, scenario["expected_reference_reads"])
        validate_policy_result(scenario, reads)
        with self.assertRaisesRegex(ValueError, "expected"):
            validate_policy_result(scenario, ["references/elements-of-style/source.md"])


    def test_fixture_covers_short_targeted_and_comprehensive_policy(self) -> None:
        fixture = json.loads(LOADING_FIXTURE.read_text())
        self.assertEqual(fixture["version"], "reference-loading-v1")
        by_mode = {row["mode"]: row for row in fixture["scenarios"]}
        self.assertEqual(set(by_mode), {"short", "targeted", "targeted-other-language", "comprehensive-english"})
        self.assertEqual(by_mode["short"]["expected_reference_reads"], [])
        targeted = by_mode["targeted"]["expected_reference_reads"]
        self.assertEqual(targeted[0], "references/elements-of-style/index.md")
        self.assertLessEqual(len(targeted[1:]), 2)
        other_language = by_mode["targeted-other-language"]["expected_reference_reads"]
        self.assertEqual(other_language[0], "references/elements-of-style/index.md")
        self.assertLessEqual(len(other_language[1:]), 2)
        self.assertEqual(
            by_mode["comprehensive-english"]["expected_reference_reads"],
            ["references/elements-of-style/source.md"],
        )
        skill = (REPO_ROOT / "SKILL.md").read_text()
        for required in ("Short tasks", "at most two", "source.md", "every language"):
            self.assertIn(required, skill)

    def test_recursive_materialization_supports_worktree_and_historical_root(self) -> None:
        worktree_paths = discover_skill_artifacts("worktree")
        self.assertIn("references/elements-of-style/index.md", worktree_paths)
        self.assertIn("references/elements-of-style/source.md", worktree_paths)
        self.assertNotIn("elements-of-style.md", worktree_paths)
        historical_paths = discover_skill_artifacts("178eaf8")
        self.assertIn("elements-of-style.md", historical_paths)
        with tempfile.TemporaryDirectory() as tmp:
            _, hashes = materialize_skill_artifacts("worktree", Path(tmp) / "current")
            self.assertEqual(set(hashes), set(worktree_paths))
            self.assertTrue((Path(tmp) / "current/references/elements-of-style/rules/rule-18.md").is_file())
            _, old_hashes = materialize_skill_artifacts("178eaf8", Path(tmp) / "old")
            self.assertIn("elements-of-style.md", old_hashes)
            self.assertTrue((Path(tmp) / "old/elements-of-style.md").is_file())


if __name__ == "__main__":
    unittest.main()
