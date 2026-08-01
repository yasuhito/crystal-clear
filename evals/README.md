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

Routing scenarios use Pi's normal skill discovery and the installed skill at `~/.pi/agent/skills/crystal-clear/SKILL.md`. Before each routing generation, the harness uses Pi's own package and skill loaders with the exact run directory to record the complete enabled inventory that can influence routing. Automatic activation means that the model called `read` with the resolved installed path. A `/skill:crystal-clear` command injects the skill directly, so the report records it as `direct-invocation`, not `automatic-read`.

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

## Run the frozen automatic-activation baseline

The routing benchmark freezes 40 designed pressure tests in `routing-scenarios.json`: 10 explicit requests, 10 complex communication tasks, 10 unrelated controls, and 10 boundary cases. Twelve scenarios (30%) are precommitted held-out paraphrases. Each record declares its language, category, expected activation, rationale, and split.

Run all 40 scenarios five times in both inventories:

```sh
python3 -m evals.run_routing \
  --skill-ref 178eaf8 --repeats 5 \
  --output evals/results/routing/178eaf8
```

The command produces two separate 200-run reports:

- `pinned/` is the formal inventory from `fixtures/skills-manifest.json`. Only this result is eligible for later pass/fail comparison.
- `installed/` snapshots the project owner's complete enabled inventory and replaces only Crystal Clear with the requested git revision. This result is ecological reference, not a release gate.

Both arms use normal Pi discovery in an isolated agent directory. No skill body is injected. Every normalized result records the exact skill revision and hash, inventory snapshot, provider/model, Pi version, harness revision, system configuration, repeat, final output, and raw trace link. Reports include recall, false-positive rate, category and split metrics, and separate selection-effect labels.

Regenerate reports from checked-in results without calling Pi:

```sh
python3 -m evals.run_routing \
  --skill-ref 178eaf8 --repeats 5 \
  --output evals/results/routing/178eaf8 \
  --report-only
```

The frozen baseline is published at `results/routing/178eaf8/SUMMARY.md`. Do not edit `routing-scenarios.json` after testing candidate metadata; create a new version instead.

## Override the smoke model or output location

```sh
python3 -m evals.run_smoke \
  --model openai-codex/gpt-5.6-sol \
  --output /tmp/crystal-clear-smoke
```

Every result records the actual model and Pi version. Do not combine results from different configurations without reporting them separately.
