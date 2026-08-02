# Automatic activation metadata comparison

- Candidate set: `routing-metadata-candidates-v1`
- Unchanged skill body base: `ac8f935`
- Reference harness/model: Pi with `openai-codex/gpt-5.6-sol`
- Metadata: English-only; every candidate is at most 1,024 characters
- Tuning: candidates and the selection rule were frozen before held-out evaluation; no wording was changed after inspecting held-out evidence
- Selection rule: Among candidates passing all held-out thresholds, maximize correct held-out explicit, complex, and unrelated-control runs; break an exact tie by choosing the shorter description.

## Held-out acceptance and change from `178eaf8`

| Candidate | Chars | Explicit recall | Delta | Complex recall | Delta | Unrelated FPR | Delta | Pass |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| concrete | 688 | 100.0% | 13.3% | 100.0% | 0.0% | 0.0% | 0.0% | yes |
| short | 561 | 100.0% | 13.3% | 100.0% | 0.0% | 0.0% | 0.0% | yes |

## Selection

Selected **`short`** from the held-out evidence using the frozen rule above.

Direct invocation remains the guaranteed fallback in Pi: `/skill:crystal-clear`.

## Boundary category (reported independently)

| Candidate | Recall | Delta | False-positive rate | Delta | Accuracy |
|---|---:|---:|---:|---:|---:|
| concrete | 100.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| short | 100.0% | 0.0% | 0.0% | 0.0% | 100.0% |

## Candidate descriptions and evidence

### `concrete` — agreed-concrete-description

> Write, rewrite, edit, proofread, or structure text and instructions for first-pass understanding. Use when communication quality is the primary task: explicit requests to clarify, simplify, make concise, readable, natural, or unambiguous, improve wording, tone, or structure, polish, rewrite, or copyedit; and complex explanations, documentation, READMEs, procedures, reports, proposals, emails, UI or error messages, summaries, prompts, agent instructions, and localized or multilingual text. Applies core clarity rules to any language, with validated language guidance for English and Japanese. Preserve facts, constraints, uncertainty, terminology, protected text, and requested voice.

- [Training raw run report](concrete/train/pinned/SUMMARY.md)
- [Held-out raw run report](concrete/held-out/pinned/SUMMARY.md)
- Training explicit recall: 100.0%
- Training complex recall: 100.0%
- Training unrelated-control FPR: 0.0%

### `short` — shorter-description

> Write or improve text and instructions for first-pass understanding. Use for explicit requests to clarify, simplify, polish, rewrite, edit, or proofread, and when communication quality is primary in complex explanations, documentation, READMEs, procedures, reports, proposals, emails, UI and error messages, summaries, prompts, agent instructions, or localized and multilingual text. Apply core clarity rules in any language and validated English and Japanese guidance. Preserve facts, constraints, uncertainty, terminology, protected text, and requested voice.

- [Training raw run report](short/train/pinned/SUMMARY.md)
- [Held-out raw run report](short/held-out/pinned/SUMMARY.md)
- Training explicit recall: 94.3%
- Training complex recall: 100.0%
- Training unrelated-control FPR: 0.0%

## Supplemental semantic routing

These non-English/non-Japanese probes are reported separately and do not affect candidate selection or frozen acceptance metrics.

| Language | Runs | Recall |
|---|---:|---:|
| ar | 5 | 100.0% |
| de | 5 | 100.0% |
| es | 5 | 100.0% |
| zh-Hans | 5 | 100.0% |

- [Selected-candidate raw probe report](short/semantic-probes/pinned/SUMMARY.md)

## Reproduce

```sh
# Finish both training runs before held-out; do not revise candidates between phases.
for candidate in concrete short; do
  python3 -m evals.run_routing --skill-ref ac8f935 --candidate "$candidate" --split train --environment pinned --repeats 5 --output "evals/results/routing/metadata-v1/$candidate/train"
done
for candidate in concrete short; do
  python3 -m evals.run_routing --skill-ref ac8f935 --candidate "$candidate" --split held-out --environment pinned --repeats 5 --output "evals/results/routing/metadata-v1/$candidate/held-out"
done
python3 -m evals.compare_routing_candidates
selected=$(python3 -c 'import json; print(json.load(open("evals/results/routing/metadata-v1/comparison.json"))["selected_candidate"])')
python3 -m evals.run_routing --skill-ref ac8f935 --candidate "$selected" --supplemental --scenarios evals/routing-semantic-probes.json --environment pinned --repeats 5 --output "evals/results/routing/metadata-v1/$selected/semantic-probes"
python3 -m evals.compare_routing_candidates --semantic-scenarios evals/routing-semantic-probes.json
```
