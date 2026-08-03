#!/usr/bin/env python3
"""Run focused English and German wording-preference regressions."""
from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from evals.evaluation import observe_trace
from evals.run_behavior import _materialize_skill
from evals.run_smoke import execute_pi

SCENARIOS = {
    "english": "Rewrite the SOURCE so each qualification is attached to the claim it limits. Return only a clear customer-facing explanation in English. Do not strengthen possibility into certainty. SOURCE: Customers can restore archived workspaces. This applies only to Enterprise accounts created after 1 January 2025, and recovery may take up to 48 hours.",
    "german": "Überarbeiten Sie SOURCE mit einem einheitlichen Produktbegriff. Geben Sie nur eine formelle dreisätzige Anleitung auf Deutsch zurück. Bewahren Sie die Einschränkung. SOURCE: Aktivieren Sie Datenprüfung in den Einstellungen. Das Prüfwerkzeug untersucht neue Uploads. Dieser Scanner prüft keine vorhandenen Dateien. Verwenden Sie durchgehend den Produktnamen Datenprüfung.",
}


def english_qualification_reasons(output: str) -> list[str]:
    sentences = [part.strip() for part in re.findall(r"[^.!?]+[.!?](?:\s|$)", output)]
    first = sentences[0] if sentences else ""
    second = sentences[1] if len(sentences) > 1 else ""
    natural_exclusive_subject = bool(
        re.fullmatch(
            r"Only customers (?:with Enterprise accounts|whose Enterprise accounts were) created after "
            r"(?:1 January|January 1,?) 2025,? can restore archived workspaces\.",
            first,
            re.I,
        )
    )
    uncertain_duration = bool(
        re.fullmatch(
            r"(?:Restoration|Recovery) (?:may take up to|can take as long as|may require up to) 48 hours\.",
            second,
            re.I,
        )
    )
    required = {
        "wrong-sentence-count": len(sentences) == 2,
        "unnatural-exclusive-qualification": natural_exclusive_subject,
        "missing-uncertain-48-hour-duration": uncertain_duration,
    }
    return [name for name, passed in required.items() if not passed]


def german_terminology_reasons(output: str) -> list[str]:
    sentences = [part.strip() for part in re.findall(r"[^.!?]+[.!?](?:\s|$)", output)]
    activation_sentences = [s for s in sentences if "Einstellungen" in s and "Datenprüfung" in s]
    activation = any(re.search(r"\bAktivieren Sie\b", s, re.I) and not re.search(r"\bnicht\b", s, re.I) for s in activation_sentences)
    upload_sentences = [s for s in sentences if re.search(r"neue Uploads", s, re.I) and "Datenprüfung" in s]
    new_uploads = any(
        re.search(r"\buntersucht\b", s, re.I) and not re.search(r"\b(?:nicht|keine)\b", s, re.I)
        for s in upload_sentences
    )
    existing_sentences = [s for s in sentences if re.search(r"vorhandene(?:n)? Dateien", s, re.I) and "Datenprüfung" in s]
    existing_limit = any(
        re.search(r"\bprüft\b", s, re.I)
        and re.search(r"\b(?:nicht|keine)\b", s, re.I)
        and not re.search(r"\bnicht\s+keine\b", s, re.I)
        for s in existing_sentences
    )
    required = {
        "wrong-sentence-count": len(sentences) == 3,
        "missing-activation": activation,
        "changed-new-upload-behavior": new_uploads,
        "changed-existing-file-limitation": existing_limit,
        "inconsistent-product-term": output.count("Datenprüfung") >= 3 and not re.search(r"\b(?:Scanner|Prüfwerkzeug)\b", output, re.I),
    }
    reasons = [name for name, passed in required.items() if not passed]
    if re.search(r"Beachten Sie", output, re.I):
        reasons.append("invented-attention-instruction")
    return reasons


CHECKERS: dict[str, Callable[[str], list[str]]] = {
    "english": english_qualification_reasons,
    "german": german_terminology_reasons,
}


def run_once(scenario: str, repeat: int, model: str) -> tuple[str, int, str]:
    with tempfile.TemporaryDirectory(prefix="crystal-clear-wording-preference-") as tmp:
        root = Path(tmp)
        session_root = root / "pi"
        skill, _ = _materialize_skill("worktree", session_root / "work")
        instructions = root / "instructions.md"
        instructions.write_text(
            "Apply the following writing skill silently to the user's task. "
            "Its relative references are available in the working directory.\n\n" + skill.read_text()
        )
        trace = execute_pi(
            prompt=SCENARIOS[scenario], model=model, session_root=session_root, appended_instructions=instructions
        )
        saved_trace = root / "trace.jsonl"
        shutil.copy2(trace, saved_trace)
        output = observe_trace(saved_trace, Path("/__regression__/SKILL.md")).final_output
    return scenario, repeat, output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="openai-codex/gpt-5.6-sol")
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--scenario", choices=["all", *SCENARIOS], default="all")
    args = parser.parse_args()
    names = list(SCENARIOS) if args.scenario == "all" else [args.scenario]
    if args.repeats < 1:
        raise ValueError("--repeats must be positive")

    rows: list[tuple[str, int, str]] = []
    with ThreadPoolExecutor(max_workers=len(names) * args.repeats) as executor:
        futures = [executor.submit(run_once, name, repeat, args.model) for name in names for repeat in range(1, args.repeats + 1)]
        rows.extend(future.result() for future in as_completed(futures))

    regressions = 0
    for name, repeat, output in sorted(rows):
        reasons = CHECKERS[name](output)
        regressions += bool(reasons)
        suffix = f" ({', '.join(reasons)})" if reasons else ""
        print(f"[{name} {repeat}] {'REGRESSION' if reasons else 'preserved'}{suffix}: {output}")
    print(f"wording preference regressions: {regressions}/{len(rows)}")
    if regressions:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
