#!/usr/bin/env python3
"""Run the live regression for Spanish prohibition-scope preservation."""
from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from evals.evaluation import observe_trace
from evals.run_behavior import _materialize_skill
from evals.run_smoke import execute_pi

PROMPT = """Reescribe el SOURCE para que la acción principal aparezca primero. Devuelve solo una solicitud clara y concisa en español. Conserva hechos, nombres, fecha y condición. SOURCE: Hemos revisado varias opciones durante dos semanas. El sistema anterior seguirá disponible. Necesitamos que Ana apruebe Proyecto Faro antes del 3 de mayo. No se debe iniciar la migración sin la aprobación de Seguridad."""
MINIMAL_REVIEW_PROMPT = """Reescribe el SOURCE para que la acción principal aparezca primero. Devuelve solo una solicitud concisa en español y conserva todos los hechos. SOURCE: Hemos revisado varias opciones durante dos semanas. Necesitamos que Ana apruebe Proyecto Faro."""


def scope_narrowing_reasons(output: str) -> list[str]:
    """Return failures for the prohibition-scope bug, independent of other facts."""
    text = " ".join(output.split())
    security_approval = r"(?:(?:la|el)\s+)?(?:aprobación|visto bueno)\s+de\s+Seguridad"
    general_patterns = (
        rf"no\s+se\s+(?:debe|deberá|puede|podrá)\s+iniciar\s+la\s+migración\s+sin\s+{security_approval}",
        rf"la\s+migración\s+no\s+(?:debe|deberá|puede|podrá)\s+iniciarse\s+sin\s+{security_approval}",
        rf"no\s+(?:debe|deberá|puede|podrá)\s+iniciarse\s+la\s+migración\s+sin\s+{security_approval}",
        rf"(?:^|[.!?;]\s*)no\s+iniciar\s+la\s+migración\s+sin\s+{security_approval}",
        rf"la\s+migración\s+no\s+se\s+iniciará\s+sin\s+{security_approval}",
        rf"la\s+migración\s+(?:solo|únicamente)\s+(?:puede|podrá)\s+iniciarse\s+con\s+{security_approval}",
        rf"la\s+migración\s+(?:solo|únicamente)\s+se\s+iniciará\s+con\s+{security_approval}",
        rf"(?:solo|únicamente)\s+se\s+(?:puede|podrá)\s+iniciar\s+la\s+migración\s+con\s+{security_approval}",
        rf"tras\s+{security_approval},?\s+(?:puede|podrá)\s+iniciarse\s+la\s+migración",
        rf"después\s+de\s+{security_approval},?\s+(?:puede|podrá)\s+iniciarse\s+la\s+migración",
    )
    general_prohibition = any(re.search(pattern, text, re.I) for pattern in general_patterns)
    reasons = []
    if not general_prohibition:
        reasons.append("missing-general-security-prohibition")
    if re.search(
        r"(?:Ana,?\s*)?(?:no\s+inicies|no\s+inicie|no\s+debes\s+iniciar|no\s+debe\s+iniciar)\s+la\s+migración|"
        r"Ana\s+no\s+(?:puede|podrá|debe)\s+iniciar\s+la\s+migración|"
        r"Ana[^.!?;]{0,45}(?:aprueba|apruebe|debe\s+aprobar)[^.!?;]{0,45}\by\s+no\s+iniciar\s+la\s+migración",
        text,
        re.I,
    ):
        reasons.append("general-prohibition-narrowed-to-ana")
    return reasons


def invented_approval_order_reasons(output: str) -> list[str]:
    """Reject making Ana's approval an unstated prerequisite for migration."""
    text = " ".join(output.split())
    patterns = (
        r"Ana[^.!?;]{0,70}(?:apruebe|aprueba|debe aprobar)[^.!?;]{0,60}[;.]?\s*"
        r"(?:después|luego|a continuación)\s*,[^.!?;]{0,70}migración",
        r"migración[^.!?;]{0,55}(?:después|luego|tras|una vez|hasta)\s+(?:de\s+)?(?:que\s+)?"
        r"Ana[^.!?;]{0,20}(?:apruebe|aprueba|haya aprobado)",
        r"(?:aprobación|visto bueno)\s+de\s+Ana[^.!?;]{0,35}(?:necesari[ao]|requisito|condición)"
        r"[^.!?;]{0,35}(?:iniciar|inicio)\s+la\s+migración",
        r"(?:iniciar|inicio)\s+la\s+migración[^.!?;]{0,35}(?:requiere|necesita|depende de)"
        r"[^.!?;]{0,25}(?:aprobación|visto bueno)\s+de\s+Ana",
    )
    return ["invented-ana-approval-before-migration"] if any(re.search(pattern, text, re.I) for pattern in patterns) else []


def review_fact_reasons(output: str) -> list[str]:
    """Return failures for the two-week options-review fact only."""
    text = " ".join(output.split())
    patterns = (
        r"(?:hemos\s+)?revis\w*\s+(?:varias\s+)?opciones\s+durante\s+dos\s+semanas",
        r"(?:^|[.!?;]\s*)durante\s+dos\s+semanas,?\s+(?:hemos\s+(?:estado\s+revisando|revisado)|revisamos|revisando)\s+(?:varias\s+)?opciones",
        r"tras\s+dos\s+semanas\s+(?:de\s+revisión\s+de|revisando|de\s+revisar)\s+(?:varias\s+)?opciones",
        r"tras\s+(?:haber\s+)?revis\w*\s+(?:varias\s+)?opciones\s+durante\s+dos\s+semanas",
        r"después\s+de\s+haber\s+revis\w*\s+(?:varias\s+)?opciones\s+durante\s+dos\s+semanas",
    )
    for pattern in patterns:
        match = re.search(pattern, text, re.I)
        if match is None:
            continue
        window = text[max(0, match.start() - 20) : match.end()]
        if not re.search(r"\b(?:no|sin|nunca)\b", window, re.I):
            return []
    return ["missing-two-week-review"]


def scope_change_reasons(output: str) -> list[str]:
    """Return all deterministic failures for the frozen Spanish scenario."""
    text = " ".join(output.split())
    lower = text.lower()
    ana_approval = bool(
        re.search(r"(?:necesitamos\s+que\s+)?Ana\s+(?:apruebe|debe aprobar)|(?:por favor,?\s*)?Ana,?\s+(?:aprueba|necesitamos\s+que\s+apruebes)", text, re.I)
    ) and not bool(re.search(r"\bno\s+(?:necesitamos\s+que\s+)?Ana\s+(?:apruebe|debe aprobar)", text, re.I))
    review_preserved = not review_fact_reasons(output)
    old_system_available = (
        "sistema anterior" in lower
        and bool(re.search(r"(?:seguirá|permanece(?:rá)?|continuará)\s+disponible", text, re.I))
        and not bool(re.search(r"sistema anterior[^.!?;]{0,25}\bno\s+(?:seguirá|permanecerá|continuará)\s+disponible", text, re.I))
    )
    reasons = scope_narrowing_reasons(output)
    reasons.extend(invented_approval_order_reasons(output))
    required = {
        "missing-ana-approval": ana_approval,
        "missing-project": "Proyecto Faro" in text,
        "missing-deadline": "3 de mayo" in text,
        "missing-two-week-review": review_preserved,
        "missing-old-system-availability": old_system_available,
    }
    reasons.extend(name for name, passed in required.items() if not passed)
    return reasons


def run_once(repeat: int, model: str, *, minimal_review: bool) -> tuple[int, str]:
    with tempfile.TemporaryDirectory(prefix="crystal-clear-spanish-scope-regression-") as tmp:
        root = Path(tmp)
        session_root = root / "pi"
        skill, _ = _materialize_skill("worktree", session_root / "work")
        instructions = root / "instructions.md"
        instructions.write_text(
            "Apply the following writing skill silently to the user's task. "
            "Its relative references are available in the working directory.\n\n"
            + skill.read_text()
        )
        live_trace = execute_pi(
            prompt=MINIMAL_REVIEW_PROMPT if minimal_review else PROMPT,
            model=model,
            session_root=session_root,
            appended_instructions=instructions,
        )
        saved_trace = root / "trace.jsonl"
        shutil.copy2(live_trace, saved_trace)
        output = observe_trace(saved_trace, Path("/__regression__/SKILL.md")).final_output
    return repeat, output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="openai-codex/gpt-5.6-sol")
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--scope-only", action="store_true")
    parser.add_argument("--review-fact-only", action="store_true")
    parser.add_argument("--minimal-review", action="store_true")
    args = parser.parse_args()
    if args.repeats < 1:
        raise ValueError("--repeats must be positive")

    rows: list[tuple[int, str]] = []
    with ThreadPoolExecutor(max_workers=args.repeats) as executor:
        futures = [
            executor.submit(run_once, repeat, args.model, minimal_review=args.minimal_review)
            for repeat in range(1, args.repeats + 1)
        ]
        rows.extend(future.result() for future in as_completed(futures))

    regressions = 0
    for repeat, output in sorted(rows):
        if args.scope_only:
            reasons = scope_narrowing_reasons(output)
        elif args.review_fact_only or args.minimal_review:
            reasons = review_fact_reasons(output)
        else:
            reasons = scope_change_reasons(output)
        regressions += bool(reasons)
        suffix = f" ({', '.join(reasons)})" if reasons else ""
        print(f"[{repeat}] {'REGRESSION' if reasons else 'preserved'}{suffix}: {output}")
    print(f"Spanish scope regressions: {regressions}/{args.repeats}")
    if regressions:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
