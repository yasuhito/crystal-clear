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
- one behavior scenario under no-skill, current-skill, and candidate-skill arms; and
- one preservation-only model judgment of the candidate behavior output.

Routing scenarios use Pi's normal skill discovery and the installed skill at `~/.pi/agent/skills/crystal-clear/SKILL.md`. Before each routing generation, the harness uses Pi's own package and skill loaders with the exact run directory to record the complete enabled inventory that can influence routing. Automatic activation means that the model called `read` with the resolved installed path. A `/skill:crystal-clear` command injects the skill directly, so the report records it as `direct-invocation`, not `automatic-read`.

The behavior arms use an identical user prompt and return contract. The skill arms inject the selected skill body into the system prompt, which isolates post-loading behavior from automatic routing. Their activation source is `system-injection`.

A `harness-ok` result means only that the expected activation, non-empty output, smoke fixture's protected strings, and—where present—the preservation judgment passed. The strict preservation judgment checks critical failures separately from deterministic protected-string evidence; it remains model evidence, not a complete semantic or clarity verdict. Every result carries a structured skill-hash record. The no-skill arm uses `status: absent`, `source: none`, and a null hash rather than omitting provenance.

Results are written under `evals/results/smoke/`:

- `raw/*.trace.jsonl` — compact Pi session traces;
- `raw/*.result.json` — normalized results and provenance;
- `raw/*.judgment.json` and matching traces — preservation-only model evidence;
- `summary.json` — deterministic and preservation-judgment counts; and
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

## Run the frozen clarity-behavior baseline

The behavior benchmark freezes 15 scenarios in `behavior-scenarios.json`: five English, five Japanese, and five multilingual-core scenarios. The multilingual-core set covers Spanish, Simplified Chinese, Arabic, German, and mixed Japanese/English. These languages are assessed only for core structure and preservation; the benchmark makes no native-naturalness claim for them.

Run every scenario five times with no skill and with the unmodified skill at revision `178eaf8`, then create 75 blind GPT comparisons:

```sh
python3 -m evals.run_behavior \
  --arms no-skill,178eaf8 --repeats 5 \
  --output evals/results/behavior/178eaf8 \
  --judge-seed 178 --jobs 4
```

Both arms use the exact same user prompt and output contract through the headless Pi seam. Skill discovery is disabled. The no-skill arm has no injected instructions; the other arm injects `SKILL.md` from `178eaf8` and materializes that revision's relative references. Completed raw records are retained, so rerunning the command resumes a partial live run. Individual failed calls are retried up to three times.

The 75 comparisons pair the two arms at the same scenario and repeat. The seed reproduces shuffled presentation order and balanced anonymous A/B placement; it does not seed provider generation, which the current Pi/provider seam does not support. Judge prompts contain the source, output contract, preservation scope, and anonymous outputs—not arm identities. Strict JSON judgments score preservation and core structure. English and Japanese also receive first-pass-understanding, referent/scope/terminology, register, and naturalness scores. Multilingual-core fields outside its limited scope must be null.

Evidence is labeled in three separate layers:

- **Deterministic evidence** checks exact protected strings and required fact, number, constraint, and condition anchors. Literal presence cannot establish semantic correctness or clarity.
- **GPT-judged evidence** is blind, pairwise model judgment and remains model evidence.
- **Human-reviewed evidence** is not collected in this baseline; native-Japanese calibration is a later release step.

Raw generation and judgment traces and normalized records are written under `results/behavior/178eaf8/raw/`. The category-separated published report is `results/behavior/178eaf8/SUMMARY.md`.

Regenerate the summaries from checked-in evidence without calling Pi:

```sh
python3 -m evals.run_behavior \
  --arms no-skill,178eaf8 --repeats 5 \
  --output evals/results/behavior/178eaf8 \
  --judge-seed 178 --report-only
```

Report-only mode validates the complete generation and judgment matrices, scenario data, prompt equality, skill provenance, deterministic scores, blind assignments, parsed judgments, and trace observations before publishing any number.

## Override the smoke model or output location

```sh
python3 -m evals.run_smoke \
  --model openai-codex/gpt-5.6-sol \
  --output /tmp/crystal-clear-smoke
```

Every result records the actual model and Pi version. Do not combine results from different configurations without reporting them separately.
