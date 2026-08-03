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

These tests cover trace observation, deterministic scoring, report generation, recursive skill-artifact materialization, and the generated *Elements of Style* index. They do not call a model. `reference-loading-scenarios.json` freezes focused policy expectations: short tasks read no reference, targeted tasks read the index and no more than two selected files, and comprehensive English passes read the canonical source.

Validate the generated reference directly with:

```sh
python3 scripts/generate_elements_of_style.py --check
python3 -m unittest evals.tests.test_elements_of_style -v
```

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

## Compare automatic-activation metadata candidates

`routing-candidates.json` freezes the agreed concrete English-only description and a shorter English-only variant. Both keep the skill body at `ac8f935`, use the unchanged frozen scenarios, and run five repeats in the formal pinned inventory. Candidate wording and the selection rule were fixed before held-out evidence was inspected.

```sh
# Finish both training runs before held-out; do not revise candidates between phases.
for candidate in concrete short; do
  python3 -m evals.run_routing \
    --skill-ref ac8f935 --candidate "$candidate" --split train \
    --environment pinned --repeats 5 \
    --output "evals/results/routing/metadata-v1/$candidate/train"
done
for candidate in concrete short; do
  python3 -m evals.run_routing \
    --skill-ref ac8f935 --candidate "$candidate" --split held-out \
    --environment pinned --repeats 5 \
    --output "evals/results/routing/metadata-v1/$candidate/held-out"
done
python3 -m evals.compare_routing_candidates
selected=$(python3 -c 'import json; print(json.load(open("evals/results/routing/metadata-v1/comparison.json"))["selected_candidate"])')
python3 -m evals.run_routing \
  --skill-ref ac8f935 --candidate "$selected" --supplemental \
  --scenarios evals/routing-semantic-probes.json --environment pinned --repeats 5 \
  --output "evals/results/routing/metadata-v1/$selected/semantic-probes"
python3 -m evals.compare_routing_candidates \
  --semantic-scenarios evals/routing-semantic-probes.json
```

The generated comparison at `results/routing/metadata-v1/SUMMARY.md` reports training and held-out evidence separately, validates each result matrix and trace before comparison, checks the precommitted held-out thresholds, reports boundary cases independently, and shows deltas from `178eaf8`. Japanese and mixed-language prompts test the frozen set. Separate Spanish, Simplified Chinese, Arabic, and German probes test semantic routing without placing literal non-English triggers in metadata; these probes do not affect selection. If every candidate fails, the comparison selects none and publishes each trade-off.

## Run the frozen clarity-behavior baseline

The behavior benchmark freezes 15 scenarios in `behavior-scenarios.json`: five English, five Japanese, and five multilingual-core scenarios. The multilingual-core set covers Spanish, Simplified Chinese, Arabic, German, and mixed Japanese/English. These languages are assessed only for core structure and preservation; the benchmark makes no native-naturalness claim for them.

Run every scenario five times with no skill and with the unmodified skill at revision `178eaf8`, then create 75 blind GPT comparisons:

```sh
python3 -m evals.run_behavior \
  --arms no-skill,178eaf8 --repeats 5 \
  --output evals/results/behavior/178eaf8 \
  --judge-seed 178 --jobs 4
```

Both arms use the exact same user prompt and output contract through the headless Pi seam. Skill discovery is disabled. The no-skill arm has no injected instructions; the other arm injects `SKILL.md` from `178eaf8` and materializes that revision's relative references. Materialization discovers `references/` recursively for current revisions and retains historical compatibility at the evaluation boundary for refs such as `178eaf8`, whose skill links to a root `elements-of-style.md`. The current skill itself has no root-path compatibility adapter. Completed raw records are retained, so rerunning the command resumes a partial live run. Individual failed calls are retried up to three times.

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

### Run the Japanese speech-act regression

The release review found that a report (`〜すると伝えた`) was sometimes rewritten as an instruction (`〜するよう伝えた`). This focused live check runs the exact behavior seam five times and also rejects speaker/addressee reversal, expanded attributed content, and invented approval ordering:

```sh
python3 -m evals.run_japanese_regression --repeats 5
```

A passing run reports zero meaning-change regressions. It is a fast regression check, not a substitute for the full release matrix.

The English modality regression found during the `320739c` release evaluation has its own focused live check. It rejects rewriting a recommendation as a bare approval directive while also checking the frozen deadline, availability, and security constraint:

```sh
python3 -m evals.run_semantic_regression --repeats 5
```

The terminology regressions have focused checks for both sides of the editorial/content boundary:

```sh
python3 -m evals.run_terminology_regression --repeats 5
python3 -m evals.run_terminology_regression --team-sync --repeats 5
```

The first rejects turning “keep the product term … throughout” into an invented instruction to keep the product enabled. The second preserves a genuine constraint on the product's UI name rather than discarding it as a rewrite instruction. Both also check the frozen behavior and scope facts.

The temporal regression preserves an event-relative deadline and a present access state while resolving an English referent:

```sh
python3 -m evals.run_temporal_regression --repeats 5
python3 -m evals.run_temporal_regression --minimal-wording --repeats 5
```

It rejects replacing `before then` with the potentially stricter `before Friday` boundary or shifting `Maya retains access` into a future prediction.

The remaining Japanese preference checks cover restrained business politeness, limiter attachment, and natural reuse of an introduced product term:

```sh
python3 -m evals.run_japanese_preference_regression --repeats 5
```

Focused English and German preference checks cover a natural exclusive-subject construction and terminology-only replacement that retains the original behavior verbs:

```sh
python3 -m evals.run_wording_preference_regression --repeats 5
```

The Arabic exclusivity regression checks that a Pro-plan-only eligibility restriction keeps its explicit restrictive force alongside the 14-day condition and uncertain 24-hour duration:

```sh
python3 -m evals.run_arabic_exclusivity_regression --repeats 5
```

The Simplified Chinese role regression checks that resolving a pronoun does not invent an actor for an agentless review, turn a separate final-confirmation responsibility into an ordering constraint, or narrow a shared Friday deadline to ticket closure alone:

```sh
python3 -m evals.run_chinese_role_regression --repeats 5
python3 -m evals.run_chinese_role_regression --minimal --repeats 5
```

The Spanish scope regression checks that leading with Ana's personal approval action does not narrow the separate general migration prohibition to Ana:

```sh
python3 -m evals.run_spanish_scope_regression --scope-only --repeats 5
python3 -m evals.run_spanish_scope_regression --review-fact-only --repeats 5
python3 -m evals.run_spanish_scope_regression --minimal-review --repeats 5
python3 -m evals.run_spanish_scope_regression --repeats 5  # also checks all frozen facts
```

The already-clear English procedure regression separates the critical review-versus-execution boundary from harmless but unnecessary copyedits:

```sh
python3 -m evals.run_procedure_boundary_regression --critical-only --repeats 5
python3 -m evals.run_procedure_boundary_regression --repeats 5  # also requires exact unchanged output
```

## Run the release-candidate evaluation

Release evaluation uses an immutable commit, not `worktree`, and requires a clean tracked worktree before live execution. The core matrix is exactly 425 generations: 200 formal pinned-inventory routing runs plus 225 behavior generations (15 scenarios × no skill/current/candidate × five repeats). The 75 blind behavior comparisons present only revision `178eaf8` and the candidate; the unjudged no-skill arm remains generation evidence and receives no inferred judgment scores.

```sh
candidate=$(git rev-parse HEAD)
python3 -m evals.run_release \
  --candidate-ref "$candidate" \
  --output "evals/results/release/$candidate"
```

This also runs the separately labeled `already-clear-v1-post-candidate` supplement. Its four English/Japanese cases run five times each. Exact equality is deterministic; every changed output receives a strict semantic-equivalence judgment. The supplement is not pooled into the 425 generations, and its post-candidate design limitation is disclosed in its report.

The first command ends with `pending-human-review` when all automated gates pass and writes two different Japanese-review artifacts:

- `japanese-review.packet.json` contains 12 deterministic, randomized anonymous pairs, the frozen calibration policy, and a Japanese rubric. It contains no condition identities, GPT scores, or preferences.
- `japanese-review.packet.sha256` contains the public packet hash needed in the response.
- `japanese-review.response-template.json` is the form the project owner fills in.
- `japanese-review.assignment-key.json` contains the condition mapping and automated scores. Keep it hidden from the reviewer until scoring is complete.

The owner returns a JSON response with the packet hash and exactly 12 reviews:

```json
{
  "packet_sha256": "copy from japanese-review.packet.sha256",
  "reviewer_role": "project-owner",
  "owner_attestation": true,
  "reviews": [
    {
      "review_id": "JP-01",
      "output_a": {
        "first_pass_understanding": 5,
        "naturalness": 5,
        "preservation": 5,
        "critical_meaning_change": false
      },
      "output_b": {
        "first_pass_understanding": 4,
        "naturalness": 4,
        "preservation": 5,
        "critical_meaning_change": false
      },
      "preference": "A",
      "notes": "任意の短い根拠"
    }
  ]
}
```

After all 12 rows are complete, incorporate and freeze the native-Japanese calibration:

```sh
python3 -m evals.run_release \
  --candidate-ref "$candidate" \
  --output "evals/results/release/$candidate" \
  --human-response owner-japanese-response.json \
  --report-only
```

Report-only mode revalidates every routing, behavior, boundary, provenance, packet, and response record, preserves the hashed raw owner response, and checks the owner attestation. For each shared rubric item (first-pass understanding, naturalness, preservation, critical preservation, and pair preference), it compares pairwise automated and human candidate-regression classifications. More than 20% disagreement removes that automated item from acceptance while retaining it as labeled non-gating evidence. Deterministic protected-string gates and human critical-meaning gates can never be removed. A pair counts as a candidate regression when any owner score is lower, the candidate alone has a critical meaning change, or the owner prefers the current output. Candidate regressions must remain at or below 10%, and any candidate critical meaning change fails release.

The generated `RELEASE.md` keeps routing, English, Japanese, multilingual-core, supplemental-boundary, and human evidence separate. Every failed threshold remains visible. The decision is `fail` on any gating failure, `pending-human-review` without a valid owner response, and `pass` only when every remaining gate passes.

Verify the reference-loading policy through four live headless Pi traces (short, targeted English, targeted Spanish, and comprehensive English):

```sh
python3 -m evals.run_reference_loading --output /tmp/crystal-clear-reference-loading
```

The command fails if observed Elements read paths differ from the frozen policy, if a targeted task reads more than two selected files, or if a targeted task reads the full source.

The lower-level behavior command remains available. Its historical two-arm defaults are unchanged; a release run uses explicit comparison arms:

```sh
python3 -m evals.run_behavior \
  --arms "no-skill,178eaf8,$candidate" \
  --compare-arms "178eaf8,$candidate" \
  --repeats 5 --output /tmp/crystal-clear-behavior-release
```

## Override the smoke model or output location

```sh
python3 -m evals.run_smoke \
  --model openai-codex/gpt-5.6-sol \
  --output /tmp/crystal-clear-smoke
```

Every result records the actual model and Pi version. Do not combine results from different configurations without reporting them separately.
