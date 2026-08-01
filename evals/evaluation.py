"""Pure trace observation, deterministic scoring, and report generation."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class TraceObservation:
    automatic_activation: bool
    skill_loaded: bool
    activation_source: str
    final_output: str
    session_id: str | None


def _normalized_path(value: str | Path) -> str:
    return os.path.abspath(os.path.expanduser(str(value)))


def _text_content(message: dict[str, Any]) -> list[str]:
    content = message.get("content", [])
    if isinstance(content, str):
        return [content]
    return [
        part.get("text", "")
        for part in content
        if isinstance(part, dict) and part.get("type") == "text"
    ]


def observe_trace(trace_path: Path, skill_path: Path) -> TraceObservation:
    """Observe skill loading and final output from a compact Pi session trace."""
    expected_path = _normalized_path(skill_path)
    automatic_activation = False
    direct_invocation = False
    final_output = ""
    session_id: str | None = None

    for raw_line in trace_path.read_text().splitlines():
        if not raw_line.strip():
            continue
        event = json.loads(raw_line)
        if event.get("type") == "session":
            session_id = event.get("id")
        message = event.get("message")
        if not isinstance(message, dict):
            continue

        role = message.get("role")
        if role == "user":
            for text in _text_content(message):
                if (
                    '<skill name="crystal-clear"' in text
                    and f'location="{expected_path}"' in text
                ):
                    direct_invocation = True

        if role != "assistant":
            continue
        for part in message.get("content", []):
            if not isinstance(part, dict):
                continue
            if part.get("type") == "toolCall" and part.get("name") == "read":
                arguments = part.get("arguments", {})
                if isinstance(arguments, dict) and arguments.get("path"):
                    if _normalized_path(arguments["path"]) == expected_path:
                        automatic_activation = True
            if part.get("type") == "text" and part.get("text", "").strip():
                final_output = part["text"].strip()

    if automatic_activation:
        source = "automatic-read"
    elif direct_invocation:
        source = "direct-invocation"
    else:
        source = "none"

    return TraceObservation(
        automatic_activation=automatic_activation,
        skill_loaded=automatic_activation or direct_invocation,
        activation_source=source,
        final_output=final_output,
        session_id=session_id,
    )


def score_result(result: dict[str, Any]) -> dict[str, Any]:
    expected = result.get("expected_activation")
    activation_matches = None
    if expected is not None:
        activation_matches = result["activation"]["automatic"] is bool(expected)

    output = result.get("final_output", "")
    protected = result.get("protected_strings", [])
    missing = [value for value in protected if value not in output]
    return {
        "activation_matches_expectation": activation_matches,
        "final_output_present": bool(output.strip()),
        "protected_strings_preserved": not missing,
        "missing_protected_strings": missing,
    }


def summarize_results(results: Iterable[dict[str, Any]]) -> dict[str, int]:
    rows = list(results)
    routing_scores = [
        row["score"]["activation_matches_expectation"]
        for row in rows
        if row["score"]["activation_matches_expectation"] is not None
    ]
    return {
        "runs": len(rows),
        "routing_runs": len(routing_scores),
        "routing_expectations_met": sum(value is True for value in routing_scores),
        "missing_final_outputs": sum(
            not row["score"]["final_output_present"] for row in rows
        ),
        "protected_string_failures": sum(
            not row["score"]["protected_strings_preserved"] for row in rows
        ),
    }


def render_markdown(
    summary: dict[str, int], results: Iterable[dict[str, Any]]
) -> str:
    rows = list(results)
    lines = [
        "# Headless Pi smoke results",
        "",
        f"- Runs: {summary['runs']}",
        (
            "- Routing expectations met: "
            f"{summary['routing_expectations_met']}/{summary['routing_runs']}"
        ),
        f"- Missing final outputs: {summary['missing_final_outputs']}",
        f"- Protected-string failures: {summary['protected_string_failures']}",
        "",
        "| Scenario | Kind | Arm | Activation | Result | Evidence |",
        "|---|---|---|---|---|---|",
    ]
    for row in sorted(rows, key=lambda item: (item["scenario_id"], item["arm"])):
        score = row["score"]
        checks = [
            score["final_output_present"],
            score["protected_strings_preserved"],
        ]
        if score["activation_matches_expectation"] is not None:
            checks.append(score["activation_matches_expectation"])
        outcome = "pass" if all(checks) else "fail"
        trace = row["trace_file"]
        lines.append(
            "| {scenario} | {kind} | {arm} | {source} | {outcome} | "
            "[Raw trace]({trace}) |".format(
                scenario=row["scenario_id"],
                kind=row["kind"],
                arm=row["arm"],
                source=row["activation"]["source"],
                outcome=outcome,
                trace=trace,
            )
        )
    return "\n".join(lines) + "\n"
