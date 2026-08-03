#!/usr/bin/env python3
"""Generate the indexed Elements of Style reference from its canonical source.

The budget checks use ``ceil(character_count / 4)`` as a deterministic English
Markdown token estimate. This is reproducible without an external tokenizer and
is deliberately documented as an estimate, not an exact model token count.
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ROOT = REPO_ROOT / "references" / "elements-of-style"
DEFAULT_SOURCE = DEFAULT_ROOT / "source.md"
RULE_PATTERN = re.compile(r"^### Rule (\d+)\. (.+)$", re.MULTILINE)
TERM_PATTERN = re.compile(r"^\*\*(.+?)\.\*\*", re.MULTILINE)
SECTION_V_PATTERN = re.compile(r"^## V\. Words And Expressions Commonly Misused$", re.MULTILINE)
WORD_GROUPS = (("A-F", "A", "F"), ("G-M", "G", "M"), ("N-S", "N", "S"), ("T-Z", "T", "Z"))
GENERATED_PATHS = (
    "index.md",
    *(f"rules/rule-{number:02d}.md" for number in range(1, 19)),
    "words/index.md",
    "words/a-f.md",
    "words/g-m.md",
    "words/n-s.md",
    "words/t-z.md",
)

RULE_TAGS = {
    1: "English-specific",
    2: "English-specific",
    3: "English-specific",
    4: "English-specific",
    5: "English-specific",
    6: "English-specific",
    7: "English-specific",
    8: "Transferable composition principle",
    9: "Transferable with caution",
    10: "Transferable with caution",
    11: "Transferable with caution",
    12: "Transferable composition principle",
    13: "Transferable composition principle",
    14: "Transferable with caution",
    15: "Transferable composition principle",
    16: "Transferable composition principle",
    17: "Transferable with caution",
    18: "Transferable with caution",
}

ROUTER = (
    ("English possessives", (1,)),
    ("English lists and serial commas", (2,)),
    ("Parenthetic or restrictive expressions", (3,)),
    ("Comma before a conjunction joining clauses", (4,)),
    ("Comma splice between independent clauses", (5,)),
    ("Unintentional sentence fragment", (6,)),
    ("Dangling introductory phrases", (7,)),
    ("Paragraph unity, opening, or ending", (8, 9)),
    ("Passive voice or an unclear actor", (10,)),
    ("Weak negatives or vague language", (11, 12)),
    ("Wordiness or repetitive sentence patterns", (13, 14)),
    ("Broken parallelism or separated modifiers", (15, 16)),
    ("Summary tense", (17,)),
    ("Emphasis and information order", (18,)),
)


@dataclass(frozen=True)
class ParsedSource:
    rules: dict[int, str]
    rule_titles: dict[int, str]
    section_v: str
    terms: list[str]
    term_groups: dict[str, list[str]]
    word_chunks: dict[str, str]


def estimate_tokens(text: str) -> int:
    """Estimate English Markdown tokens as ceil(characters / 4)."""
    return math.ceil(len(text) / 4)


def _term_initial(term: str) -> str:
    match = re.search(r"[A-Za-z]", term)
    if match is None:
        raise ValueError(f"word-usage term has no Latin initial: {term!r}")
    return match.group().upper()


def parse_source(source: str) -> ParsedSource:
    rule_matches = list(RULE_PATTERN.finditer(source))
    numbers = [int(match.group(1)) for match in rule_matches]
    if numbers != list(range(1, 19)):
        raise ValueError(f"expected Rules 1-18 exactly once, found {numbers}")
    section_v_match = SECTION_V_PATTERN.search(source)
    if section_v_match is None:
        raise ValueError("source is missing Section V")
    rules: dict[int, str] = {}
    titles: dict[int, str] = {}
    for index, match in enumerate(rule_matches):
        end = rule_matches[index + 1].start() if index + 1 < len(rule_matches) else section_v_match.start()
        number = int(match.group(1))
        rules[number] = source[match.start():end]
        titles[number] = match.group(2)

    section_v = source[section_v_match.start():]
    term_matches = list(TERM_PATTERN.finditer(section_v))
    if not term_matches:
        raise ValueError("Section V contains no word-usage terms")
    terms = [match.group(1) for match in term_matches]
    if len(terms) != len(set(terms)):
        raise ValueError("Section V contains duplicate word-usage terms")

    term_groups: dict[str, list[str]] = {}
    word_chunks: dict[str, str] = {}
    previous_end = 0
    for index, (group, low, high) in enumerate(WORD_GROUPS):
        selected = [position for position, term in enumerate(terms) if low <= _term_initial(term) <= high]
        if not selected:
            raise ValueError(f"Section V has no terms for {group}")
        if selected != list(range(selected[0], selected[-1] + 1)):
            raise ValueError(f"Section V terms are not ordered for {group}")
        start = 0 if index == 0 else term_matches[selected[0]].start()
        end = term_matches[selected[-1] + 1].start() if selected[-1] + 1 < len(term_matches) else len(section_v)
        if start != previous_end:
            raise ValueError("word chunk boundaries do not cover Section V continuously")
        previous_end = end
        term_groups[group] = [terms[position] for position in selected]
        word_chunks[group] = section_v[start:end]
    if previous_end != len(section_v) or sum(term_groups.values(), []) != terms:
        raise ValueError("word chunks do not cover every Section V term exactly once")
    return ParsedSource(rules, titles, section_v, terms, term_groups, word_chunks)


def _rule_links(numbers: tuple[int, ...]) -> str:
    return ", ".join(f"[Rule {number}](rules/rule-{number:02d}.md)" for number in numbers)


def render_index(parsed: ParsedSource) -> str:
    lines = [
        "# The Elements of Style: indexed reference",
        "",
        "Use this index as the interface for targeted consultation. The generated rule and word files reproduce the canonical 1918 source verbatim; they do not summarize or modernize it.",
        "",
        "## Access policy",
        "",
        "Every language may consult this same index. Apply a rule only when it is natural and useful in the target language. Target-language grammar, convention, information structure, and the applicable language guide override this reference; do not transplant English forms directly. Treat historical usage advice cautiously.",
        "",
        "- **Short task:** use the skill core only; load no Elements reference.",
        "- **Targeted substantial writing or revision:** read this index, then at most one or two relevant rule or word-chunk files.",
        "- **Comprehensive English copyedit or explicit full Strunk pass:** read [`source.md`](source.md).",
        "- **Comprehensive work in another language:** continue to use this index and targeted files; do not import the full English grammar wholesale.",
        "",
        "## Task and symptom router",
        "",
        "| Need or symptom | Consult |",
        "|---|---|",
    ]
    lines.extend(f"| {symptom} | {_rule_links(numbers)} |" for symptom, numbers in ROUTER)
    lines.extend(
        [
            "| A particular English word or expression | [Section V word index](words/index.md) |",
            "",
            "## Complete rule index",
            "",
            "Tags describe transferability once; they are not language-specific branching instructions.",
            "",
            "| Rule | Classification |",
            "|---|---|",
        ]
    )
    for number in range(1, 19):
        lines.append(
            f"| [Rule {number}. {parsed.rule_titles[number]}](rules/rule-{number:02d}.md) | {RULE_TAGS[number]} |"
        )
    lines.extend(
        [
            "",
            "## Word usage",
            "",
            "Use the [Section V word index](words/index.md) to select one alphabetic chunk. Current usage, audience needs, and house style take precedence over the 1918 advice.",
            "",
            "## Full source",
            "",
            "The canonical, unchanged source is [`source.md`](source.md).",
            "",
        ]
    )
    return "\n".join(lines)


def render_words_index(parsed: ParsedSource) -> str:
    lines = [
        "# Section V word index",
        "",
        "Select the single chunk containing the term in question. The chunk bodies reproduce Section V verbatim.",
        "",
        "| Term | Chunk |",
        "|---|---|",
    ]
    for group, _, _ in WORD_GROUPS:
        path = group.lower() + ".md"
        lines.extend(f"| {term} | [{group}]({path}) |" for term in parsed.term_groups[group])
    lines.append("")
    return "\n".join(lines)


def generated_documents(source: str) -> dict[str, str]:
    parsed = parse_source(source)
    documents = {"index.md": render_index(parsed), "words/index.md": render_words_index(parsed)}
    documents.update({f"rules/rule-{number:02d}.md": body for number, body in parsed.rules.items()})
    documents.update({f"words/{group.lower()}.md": body for group, body in parsed.word_chunks.items()})
    if set(documents) != set(GENERATED_PATHS):
        raise AssertionError("generated document inventory is incomplete")
    return documents


def write_documents(documents: dict[str, str], output_root: Path, *, check: bool) -> bool:
    differences: list[str] = []
    expected_paths = {Path(relative) for relative in GENERATED_PATHS}
    managed_existing = {
        path.relative_to(output_root)
        for root in (output_root / "rules", output_root / "words")
        if root.is_dir()
        for path in root.rglob("*.md")
    }
    if (output_root / "index.md").is_file():
        managed_existing.add(Path("index.md"))
    extras = sorted(managed_existing - expected_paths)
    differences.extend(f"extra:{path.as_posix()}" for path in extras)
    if not check:
        for relative in extras:
            (output_root / relative).unlink()
    for relative in GENERATED_PATHS:
        destination = output_root / relative
        expected = documents[relative].encode()
        if not destination.is_file() or destination.read_bytes() != expected:
            differences.append(relative)
            if not check:
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(expected)
    if differences and check:
        print("generated Elements outputs are stale: " + ", ".join(differences), file=sys.stderr)
        return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--check", action="store_true", help="fail instead of rewriting stale outputs")
    args = parser.parse_args()
    documents = generated_documents(args.source.read_text())
    if not write_documents(documents, args.output_root, check=args.check):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
