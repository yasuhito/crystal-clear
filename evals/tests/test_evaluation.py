import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from evals.evaluation import (
    activation_record,
    observe_trace,
    parse_preservation_judgment,
    render_markdown,
    score_result,
    skill_hash_record,
    summarize_results,
)


SKILL_PATH = Path("/repo/crystal-clear/SKILL.md")


def write_trace(directory: Path, events: list[dict]) -> Path:
    path = directory / "trace.jsonl"
    path.write_text("".join(json.dumps(event) + "\n" for event in events))
    return path


class ObserveTraceTests(unittest.TestCase):
    def test_observes_automatic_activation_from_skill_read(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            trace = write_trace(
                Path(tmp),
                [
                    {
                        "type": "message",
                        "message": {
                            "role": "assistant",
                            "content": [
                                {
                                    "type": "toolCall",
                                    "name": "read",
                                    "arguments": {"path": str(SKILL_PATH)},
                                }
                            ],
                        },
                    },
                    {
                        "type": "message",
                        "message": {
                            "role": "assistant",
                            "content": [{"type": "text", "text": "Clear output."}],
                        },
                    },
                ],
            )

            observation = observe_trace(trace, SKILL_PATH)

            self.assertEqual(observation.activation_source, "automatic-read")
            self.assertTrue(observation.automatic_activation)
            self.assertEqual(observation.final_output, "Clear output.")

    def test_distinguishes_direct_invocation_from_automatic_activation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            trace = write_trace(
                Path(tmp),
                [
                    {
                        "type": "message",
                        "message": {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": (
                                        '<skill name="crystal-clear" '
                                        f'location="{SKILL_PATH}">instructions</skill>'
                                    ),
                                }
                            ],
                        },
                    },
                    {
                        "type": "message",
                        "message": {
                            "role": "assistant",
                            "content": [{"type": "text", "text": "Clear output."}],
                        },
                    },
                ],
            )

            observation = observe_trace(trace, SKILL_PATH)

            self.assertEqual(observation.activation_source, "direct-invocation")
            self.assertFalse(observation.automatic_activation)
            self.assertTrue(observation.skill_loaded)

    def test_resolves_symlinks_when_matching_direct_invocation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            real_skill = root / "installed" / "SKILL.md"
            real_skill.parent.mkdir()
            real_skill.write_text("skill")
            linked_directory = root / "linked-skill"
            linked_directory.symlink_to(real_skill.parent, target_is_directory=True)
            linked_skill = linked_directory / "SKILL.md"
            trace = write_trace(
                root,
                [
                    {
                        "type": "message",
                        "message": {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": (
                                        '<skill name="crystal-clear" '
                                        f'location="{linked_skill}">instructions</skill>'
                                    ),
                                }
                            ],
                        },
                    }
                ],
            )

            observation = observe_trace(trace, real_skill)

            self.assertEqual(observation.activation_source, "direct-invocation")

    def test_known_negative_has_no_activation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            trace = write_trace(
                Path(tmp),
                [
                    {
                        "type": "message",
                        "message": {
                            "role": "assistant",
                            "content": [{"type": "text", "text": "323"}],
                        },
                    }
                ],
            )

            observation = observe_trace(trace, SKILL_PATH)

            self.assertEqual(observation.activation_source, "none")
            self.assertFalse(observation.skill_loaded)
            self.assertEqual(observation.final_output, "323")

    def test_records_system_injection_as_loaded_but_not_automatic(self) -> None:
        observation = observe_trace(
            write_trace(
                Path(self.enterContext(tempfile.TemporaryDirectory())),
                [
                    {
                        "type": "message",
                        "message": {
                            "role": "assistant",
                            "content": [{"type": "text", "text": "Clear output."}],
                        },
                    }
                ],
            ),
            SKILL_PATH,
        )

        record = activation_record(observation, skill_body_injected=True)

        self.assertEqual(
            record,
            {
                "automatic": False,
                "skill_loaded": True,
                "source": "system-injection",
            },
        )


class PiInventoryBridgeTests(unittest.TestCase):
    def test_uses_enabled_paths_without_rescanning_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            enabled = root / "enabled.md"
            disabled = root / "disabled.md"
            enabled.write_text("enabled")
            disabled.write_text("disabled")
            fake_module = root / "fake-pi.mjs"
            fake_module.write_text(
                f'''\nexport class SettingsManager {{\n  static create(cwd, agentDir) {{ return {{ cwd, agentDir }}; }}\n}}\nexport class DefaultPackageManager {{\n  constructor(options) {{ this.options = options; }}\n  async resolve() {{\n    return {{ skills: [\n      {{ enabled: true, path: {json.dumps(str(enabled))} }},\n      {{ enabled: false, path: {json.dumps(str(disabled))} }}\n    ] }};\n  }}\n}}\nexport function loadSkills(options) {{\n  if (options.includeDefaults !== false) throw new Error("rescanned defaults");\n  if (options.skillPaths.length !== 1 || options.skillPaths[0] !== {json.dumps(str(enabled))}) {{\n    throw new Error("disabled path was not filtered");\n  }}\n  return {{ skills: [{{\n    name: "collision-winner",\n    filePath: options.skillPaths[0],\n    disableModelInvocation: false\n  }}] }};\n}}\n'''
            )
            script = Path(__file__).resolve().parents[1] / "list_pi_skills.mjs"

            completed = subprocess.run(
                ["node", str(script), str(fake_module), str(root), str(root / "agent")],
                check=True,
                capture_output=True,
                text=True,
            )
            inventory = json.loads(completed.stdout)

            self.assertEqual([item["name"] for item in inventory], ["collision-winner"])
            self.assertEqual(inventory[0]["path"], str(enabled))


class ScoreAndReportTests(unittest.TestCase):
    def test_parses_smoke_preservation_judgment(self) -> None:
        judgment = parse_preservation_judgment(
            '{"critical_preservation_failure":false,'
            '"critical_failure_types":[],"evidence":"Meaning is intact."}'
        )

        self.assertEqual(
            judgment,
            {
                "critical_preservation_failure": False,
                "critical_failure_types": [],
                "evidence": "Meaning is intact.",
            },
        )

    def test_rejects_non_string_preservation_failure_type(self) -> None:
        with self.assertRaises(ValueError):
            parse_preservation_judgment(
                '{"critical_preservation_failure":true,'
                '"critical_failure_types":[{}],"evidence":"bad value"}'
            )

    def test_no_skill_hash_has_schema_defined_absence(self) -> None:
        self.assertEqual(
            skill_hash_record(None, source="none"),
            {"status": "absent", "source": "none", "sha256": None},
        )

    def test_scores_expected_activation_and_protected_strings(self) -> None:
        result = {
            "kind": "routing",
            "expected_activation": True,
            "activation": {"automatic": True, "skill_loaded": True},
            "final_output": "API-17 remains unavailable.",
            "protected_strings": ["API-17"],
        }

        score = score_result(result)

        self.assertEqual(
            score,
            {
                "activation_matches_expectation": True,
                "final_output_present": True,
                "protected_strings_preserved": True,
                "missing_protected_strings": [],
            },
        )

    def test_summary_and_markdown_are_deterministic(self) -> None:
        results = [
            {
                "scenario_id": "routing-positive",
                "kind": "routing",
                "arm": "auto",
                "activation": {
                    "automatic": True,
                    "skill_loaded": True,
                    "source": "automatic-read",
                },
                "score": {
                    "activation_matches_expectation": True,
                    "final_output_present": True,
                    "protected_strings_preserved": True,
                    "missing_protected_strings": [],
                },
                "final_output": "Clear output.",
                "trace_file": "raw/routing-positive.jsonl",
            },
            {
                "scenario_id": "behavior-rewrite",
                "kind": "behavior",
                "arm": "no-skill",
                "activation": {
                    "automatic": False,
                    "skill_loaded": False,
                    "source": "none",
                },
                "score": {
                    "activation_matches_expectation": None,
                    "final_output_present": True,
                    "protected_strings_preserved": True,
                    "missing_protected_strings": [],
                },
                "final_output": "API-17 is unavailable.",
                "trace_file": "raw/behavior-rewrite--no-skill.jsonl",
            },
        ]

        summary = summarize_results(results)
        markdown = render_markdown(summary, results)

        self.assertEqual(summary["runs"], 2)
        self.assertEqual(summary["routing_expectations_met"], 1)
        self.assertEqual(summary["protected_string_failures"], 0)
        self.assertEqual(summary["critical_preservation_failures"], 0)
        self.assertIn("Critical preservation failures: 0", markdown)
        self.assertIn(
            "| routing-positive | routing | auto | automatic-read | harness-ok |",
            markdown,
        )
        self.assertIn("Raw trace", markdown)


if __name__ == "__main__":
    unittest.main()
