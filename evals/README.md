# Evaluation harness

The harness tests Crystal Clear at one external seam: a headless Pi run. Each run preserves the compact Pi session trace, final output, activation observation, and execution provenance.

The smoke suite is a harness check, not an activation or quality benchmark. The full baseline scenario sets belong to later tickets.

## Prerequisites

- Pi is installed and authenticated for `openai-codex/gpt-5.6-sol`.
- Run commands from the repository root.
- The current Git revision contains `SKILL.md`.

## Test deterministic logic

```sh
python3 -m unittest discover -s evals/tests -v
```

These tests cover trace observation, deterministic scoring, and report generation. They do not call a model.

## Run the live smoke suite

```sh
python3 -m evals.run_smoke
```

The command runs:

- one positive automatic-routing scenario;
- one negative automatic-routing scenario;
- one direct invocation, which validates that direct loading is distinct from automatic activation; and
- one behavior scenario under no-skill, current-skill, and candidate-skill arms.

Routing scenarios use Pi's normal skill discovery. By default, the harness expects the installed skill at `~/.pi/agent/skills/crystal-clear/SKILL.md`; override this with `--discovered-skill` when needed. Before generation, the harness uses Pi's own package and skill loaders to record the complete enabled inventory that can influence routing. Automatic activation means that the model called `read` with the resolved installed path. A `/skill:crystal-clear` command injects the skill directly, so the report records it as `direct-invocation`, not `automatic-read`.

The behavior arms use an identical user prompt and return contract. The skill arms inject the selected skill body into the system prompt, which isolates post-loading behavior from automatic routing. Their activation source is `system-injection`.

A `harness-ok` result means only that the expected activation, non-empty output, and smoke fixture's protected strings passed. It is not a complete preservation or clarity verdict. Every result carries a structured skill-hash record. The no-skill arm uses `status: absent`, `source: none`, and a null hash rather than omitting provenance.

Results are written under `evals/results/smoke/`:

- `raw/*.trace.jsonl` — compact Pi session traces;
- `raw/*.result.json` — normalized results and provenance;
- `summary.json` — deterministic counts; and
- `SUMMARY.md` — the human-readable result index.

## Regenerate the report without calling Pi

```sh
python3 -m evals.run_smoke --report-only
```

This command rebuilds both summaries from the checked-in normalized result records. It does not call a model or rewrite the raw traces.

## Override the model or output location

```sh
python3 -m evals.run_smoke \
  --model openai-codex/gpt-5.6-sol \
  --output /tmp/crystal-clear-smoke
```

Every result records the actual model and Pi version. Do not combine results from different configurations without reporting them separately.
