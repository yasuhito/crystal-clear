# Automatic activation baseline — pinned

- Inventory role: **formal**
- Inventory snapshot: `pinned-routing-inventory-v1`
- Supplemental scenarios: `routing-semantic-probes-v1` (4 scenarios; outside frozen acceptance metrics)
- Baseline skill revision: `ac8f935+metadata:short`
- Runs: 20
- Recall across expected-positive runs: 100.0% (20/20)
- Precision: 100.0%
- False-positive rate across all expected-negative runs: n/a (0/0)
- Unrelated-control false-positive rate: n/a (0/0)

This pinned-inventory result is supplemental semantic evidence only and is not eligible for candidate selection or pass/fail comparison.

## Category results

| Category | Runs | Recall | Precision | False-positive rate | Activation rate |
|---|---:|---:|---:|---:|---:|
| boundary | 0 | n/a | n/a | n/a | n/a |
| complex-communication | 10 | 100.0% | 100.0% | n/a | 100.0% |
| explicit-request | 10 | 100.0% | 100.0% | n/a | 100.0% |
| unrelated-control | 0 | n/a | n/a | n/a | n/a |

## Frozen split results

| Split | Runs | Recall | False-positive rate |
|---|---:|---:|---:|
| train | 0 | n/a | n/a |
| held-out | 20 | 100.0% | n/a |

## Selection outcomes

`not-selected` means Crystal Clear was not read. `selected-with-little-visible-change` means it was read but the final output was identical or at least 98% similar to the supplied source text. Generated outputs without a source text are reported as `selected-effect-not-deterministically-assessed`; the report does not infer a behavioral effect merely from selection.

- not-selected: 0
- selected-with-little-visible-change: 0
- selected-with-visible-change: 0
- selected-effect-not-deterministically-assessed: 20

## Raw runs

| Scenario | Category | Split | Repeat | Expected | Observed | Outcome | Trace | Result |
|---|---|---|---:|---|---|---|---|---|
| semantic-ar-procedure | complex-communication | held-out | 1 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/semantic-ar-procedure--r01.trace.jsonl) | [result](raw/semantic-ar-procedure--r01.result.json) |
| semantic-ar-procedure | complex-communication | held-out | 2 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/semantic-ar-procedure--r02.trace.jsonl) | [result](raw/semantic-ar-procedure--r02.result.json) |
| semantic-ar-procedure | complex-communication | held-out | 3 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/semantic-ar-procedure--r03.trace.jsonl) | [result](raw/semantic-ar-procedure--r03.result.json) |
| semantic-ar-procedure | complex-communication | held-out | 4 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/semantic-ar-procedure--r04.trace.jsonl) | [result](raw/semantic-ar-procedure--r04.result.json) |
| semantic-ar-procedure | complex-communication | held-out | 5 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/semantic-ar-procedure--r05.trace.jsonl) | [result](raw/semantic-ar-procedure--r05.result.json) |
| semantic-de-proofread | explicit-request | held-out | 1 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/semantic-de-proofread--r01.trace.jsonl) | [result](raw/semantic-de-proofread--r01.result.json) |
| semantic-de-proofread | explicit-request | held-out | 2 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/semantic-de-proofread--r02.trace.jsonl) | [result](raw/semantic-de-proofread--r02.result.json) |
| semantic-de-proofread | explicit-request | held-out | 3 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/semantic-de-proofread--r03.trace.jsonl) | [result](raw/semantic-de-proofread--r03.result.json) |
| semantic-de-proofread | explicit-request | held-out | 4 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/semantic-de-proofread--r04.trace.jsonl) | [result](raw/semantic-de-proofread--r04.result.json) |
| semantic-de-proofread | explicit-request | held-out | 5 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/semantic-de-proofread--r05.trace.jsonl) | [result](raw/semantic-de-proofread--r05.result.json) |
| semantic-es-rewrite | explicit-request | held-out | 1 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/semantic-es-rewrite--r01.trace.jsonl) | [result](raw/semantic-es-rewrite--r01.result.json) |
| semantic-es-rewrite | explicit-request | held-out | 2 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/semantic-es-rewrite--r02.trace.jsonl) | [result](raw/semantic-es-rewrite--r02.result.json) |
| semantic-es-rewrite | explicit-request | held-out | 3 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/semantic-es-rewrite--r03.trace.jsonl) | [result](raw/semantic-es-rewrite--r03.result.json) |
| semantic-es-rewrite | explicit-request | held-out | 4 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/semantic-es-rewrite--r04.trace.jsonl) | [result](raw/semantic-es-rewrite--r04.result.json) |
| semantic-es-rewrite | explicit-request | held-out | 5 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/semantic-es-rewrite--r05.trace.jsonl) | [result](raw/semantic-es-rewrite--r05.result.json) |
| semantic-zh-instructions | complex-communication | held-out | 1 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/semantic-zh-instructions--r01.trace.jsonl) | [result](raw/semantic-zh-instructions--r01.result.json) |
| semantic-zh-instructions | complex-communication | held-out | 2 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/semantic-zh-instructions--r02.trace.jsonl) | [result](raw/semantic-zh-instructions--r02.result.json) |
| semantic-zh-instructions | complex-communication | held-out | 3 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/semantic-zh-instructions--r03.trace.jsonl) | [result](raw/semantic-zh-instructions--r03.result.json) |
| semantic-zh-instructions | complex-communication | held-out | 4 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/semantic-zh-instructions--r04.trace.jsonl) | [result](raw/semantic-zh-instructions--r04.result.json) |
| semantic-zh-instructions | complex-communication | held-out | 5 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/semantic-zh-instructions--r05.trace.jsonl) | [result](raw/semantic-zh-instructions--r05.result.json) |
