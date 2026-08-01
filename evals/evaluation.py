"""Pure trace observation, deterministic scoring, and report generation."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


CRITICAL_FAILURE_TYPES = frozenset(
    {
        "invented-fact",
        "removed-constraint",
        "changed-instruction",
        "changed-certainty",
        "corrupted-protected-text",
        "broken-register",
    }
)


@dataclass(frozen=True)
class TraceObservation:
    automatic_activation: bool
    skill_loaded: bool
    activation_source: str
    final_output: str
    session_id: str | None


def _normalized_path(value: str | Path) -> str:
    return os.path.realpath(os.path.expanduser(str(value)))


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
                location = re.search(
                    r'<skill name="crystal-clear" location="([^"]+)">', text
                )
                if location and _normalized_path(location.group(1)) == expected_path:
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


def skill_hash_record(
    value: str | None, *, source: str
) -> dict[str, str | None]:
    return {
        "status": "present" if value is not None else "absent",
        "source": source,
        "sha256": value,
    }


def activation_record(
    observation: TraceObservation, *, skill_body_injected: bool
) -> dict[str, Any]:
    if skill_body_injected:
        return {
            "automatic": False,
            "skill_loaded": True,
            "source": "system-injection",
        }
    return {
        "automatic": observation.automatic_activation,
        "skill_loaded": observation.skill_loaded,
        "source": observation.activation_source,
    }


def parse_preservation_judgment(value: str) -> dict[str, Any]:
    """Parse the strict model judgment used by the development smoke suite."""
    text = value.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if len(lines) >= 3 and lines[-1].strip() == "```":
            text = "\n".join(lines[1:-1])
    try:
        judgment = json.loads(text)
    except json.JSONDecodeError as error:
        raise ValueError(f"preservation judgment is not valid JSON: {error}") from error

    expected = {
        "critical_preservation_failure",
        "critical_failure_types",
        "evidence",
    }
    if not isinstance(judgment, dict) or set(judgment) != expected:
        raise ValueError("preservation judgment has unexpected fields")
    failure_types = judgment["critical_failure_types"]
    if (
        not isinstance(judgment["critical_preservation_failure"], bool)
        or not isinstance(failure_types, list)
        or not all(
            isinstance(failure_type, str)
            and failure_type in CRITICAL_FAILURE_TYPES
            for failure_type in failure_types
        )
        or judgment["critical_preservation_failure"] != bool(failure_types)
        or not isinstance(judgment["evidence"], str)
    ):
        raise ValueError("preservation judgment is invalid")
    return judgment


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
    preservation_judgments = [
        row["preservation_judgment"]
        for row in rows
        if row.get("preservation_judgment") is not None
    ]
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
        "preservation_judgments": len(preservation_judgments),
        "critical_preservation_failures": sum(
            judgment["critical_preservation_failure"]
            for judgment in preservation_judgments
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
        (
            "- Critical preservation failures: "
            f"{summary['critical_preservation_failures']} "
            f"({summary['preservation_judgments']} judged behavior outputs)"
        ),
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
        judgment = row.get("preservation_judgment")
        if judgment is not None:
            checks.append(not judgment["critical_preservation_failure"])
        outcome = "harness-ok" if all(checks) else "harness-fail"
        trace = row["trace_file"]
        evidence = f"[Raw trace]({trace})"
        if row.get("preservation_judgment_file"):
            evidence += (
                f"; [preservation judgment]({row['preservation_judgment_file']})"
            )
        lines.append(
            "| {scenario} | {kind} | {arm} | {source} | {outcome} | "
            "{evidence} |".format(
                scenario=row["scenario_id"],
                kind=row["kind"],
                arm=row["arm"],
                source=row["activation"]["source"],
                outcome=outcome,
                evidence=evidence,
            )
        )
    return "\n".join(lines) + "\n"
