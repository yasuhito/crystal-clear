# Automatic activation baseline — pinned

- Inventory role: **formal**
- Inventory snapshot: `pinned-routing-inventory-v1`
- Frozen scenarios: `routing-v1-frozen-2026-03-24` (40 scenarios; 12 held-out)
- Baseline skill revision: `ac8f935+metadata:short`
- Runs: 60
- Recall across expected-positive runs: 100.0% (35/35)
- Precision: 100.0%
- False-positive rate across all expected-negative runs: 0.0% (0/25)
- Unrelated-control false-positive rate: 0.0% (0/15)

This pinned inventory is the only result eligible for later pass/fail comparison.

## Category results

| Category | Runs | Recall | Precision | False-positive rate | Activation rate |
|---|---:|---:|---:|---:|---:|
| boundary | 15 | 100.0% | 100.0% | 0.0% | 33.3% |
| complex-communication | 15 | 100.0% | 100.0% | n/a | 100.0% |
| explicit-request | 15 | 100.0% | 100.0% | n/a | 100.0% |
| unrelated-control | 15 | n/a | n/a | 0.0% | 0.0% |

## Frozen split results

| Split | Runs | Recall | False-positive rate |
|---|---:|---:|---:|
| train | 0 | n/a | n/a |
| held-out | 60 | 100.0% | 0.0% |

## Selection outcomes

`not-selected` means Crystal Clear was not read. `selected-with-little-visible-change` means it was read but the final output was identical or at least 98% similar to the supplied source text. Generated outputs without a source text are reported as `selected-effect-not-deterministically-assessed`; the report does not infer a behavioral effect merely from selection.

- not-selected: 25
- selected-with-little-visible-change: 0
- selected-with-visible-change: 15
- selected-effect-not-deterministically-assessed: 20

## Raw runs

| Scenario | Category | Split | Repeat | Expected | Observed | Outcome | Trace | Result |
|---|---|---|---:|---|---|---|---|---|
| boundary-code-doc-held | boundary | held-out | 1 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/boundary-code-doc-held--r01.trace.jsonl) | [result](raw/boundary-code-doc-held--r01.result.json) |
| boundary-code-doc-held | boundary | held-out | 2 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/boundary-code-doc-held--r02.trace.jsonl) | [result](raw/boundary-code-doc-held--r02.result.json) |
| boundary-code-doc-held | boundary | held-out | 3 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/boundary-code-doc-held--r03.trace.jsonl) | [result](raw/boundary-code-doc-held--r03.result.json) |
| boundary-code-doc-held | boundary | held-out | 4 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/boundary-code-doc-held--r04.trace.jsonl) | [result](raw/boundary-code-doc-held--r04.result.json) |
| boundary-code-doc-held | boundary | held-out | 5 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/boundary-code-doc-held--r05.trace.jsonl) | [result](raw/boundary-code-doc-held--r05.result.json) |
| boundary-code-only-held | boundary | held-out | 1 | false | false | not-selected | [trace](raw/boundary-code-only-held--r01.trace.jsonl) | [result](raw/boundary-code-only-held--r01.result.json) |
| boundary-code-only-held | boundary | held-out | 2 | false | false | not-selected | [trace](raw/boundary-code-only-held--r02.trace.jsonl) | [result](raw/boundary-code-only-held--r02.result.json) |
| boundary-code-only-held | boundary | held-out | 3 | false | false | not-selected | [trace](raw/boundary-code-only-held--r03.trace.jsonl) | [result](raw/boundary-code-only-held--r03.result.json) |
| boundary-code-only-held | boundary | held-out | 4 | false | false | not-selected | [trace](raw/boundary-code-only-held--r04.trace.jsonl) | [result](raw/boundary-code-only-held--r04.result.json) |
| boundary-code-only-held | boundary | held-out | 5 | false | false | not-selected | [trace](raw/boundary-code-only-held--r05.trace.jsonl) | [result](raw/boundary-code-only-held--r05.result.json) |
| boundary-ja-data-held | boundary | held-out | 1 | false | false | not-selected | [trace](raw/boundary-ja-data-held--r01.trace.jsonl) | [result](raw/boundary-ja-data-held--r01.result.json) |
| boundary-ja-data-held | boundary | held-out | 2 | false | false | not-selected | [trace](raw/boundary-ja-data-held--r02.trace.jsonl) | [result](raw/boundary-ja-data-held--r02.result.json) |
| boundary-ja-data-held | boundary | held-out | 3 | false | false | not-selected | [trace](raw/boundary-ja-data-held--r03.trace.jsonl) | [result](raw/boundary-ja-data-held--r03.result.json) |
| boundary-ja-data-held | boundary | held-out | 4 | false | false | not-selected | [trace](raw/boundary-ja-data-held--r04.trace.jsonl) | [result](raw/boundary-ja-data-held--r04.result.json) |
| boundary-ja-data-held | boundary | held-out | 5 | false | false | not-selected | [trace](raw/boundary-ja-data-held--r05.trace.jsonl) | [result](raw/boundary-ja-data-held--r05.result.json) |
| complex-en-report-held | complex-communication | held-out | 1 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-report-held--r01.trace.jsonl) | [result](raw/complex-en-report-held--r01.result.json) |
| complex-en-report-held | complex-communication | held-out | 2 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-report-held--r02.trace.jsonl) | [result](raw/complex-en-report-held--r02.result.json) |
| complex-en-report-held | complex-communication | held-out | 3 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-report-held--r03.trace.jsonl) | [result](raw/complex-en-report-held--r03.result.json) |
| complex-en-report-held | complex-communication | held-out | 4 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-report-held--r04.trace.jsonl) | [result](raw/complex-en-report-held--r04.result.json) |
| complex-en-report-held | complex-communication | held-out | 5 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-report-held--r05.trace.jsonl) | [result](raw/complex-en-report-held--r05.result.json) |
| complex-en-skill-held | complex-communication | held-out | 1 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-skill-held--r01.trace.jsonl) | [result](raw/complex-en-skill-held--r01.result.json) |
| complex-en-skill-held | complex-communication | held-out | 2 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-skill-held--r02.trace.jsonl) | [result](raw/complex-en-skill-held--r02.result.json) |
| complex-en-skill-held | complex-communication | held-out | 3 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-skill-held--r03.trace.jsonl) | [result](raw/complex-en-skill-held--r03.result.json) |
| complex-en-skill-held | complex-communication | held-out | 4 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-skill-held--r04.trace.jsonl) | [result](raw/complex-en-skill-held--r04.result.json) |
| complex-en-skill-held | complex-communication | held-out | 5 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-skill-held--r05.trace.jsonl) | [result](raw/complex-en-skill-held--r05.result.json) |
| complex-ja-procedure-held | complex-communication | held-out | 1 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-ja-procedure-held--r01.trace.jsonl) | [result](raw/complex-ja-procedure-held--r01.result.json) |
| complex-ja-procedure-held | complex-communication | held-out | 2 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-ja-procedure-held--r02.trace.jsonl) | [result](raw/complex-ja-procedure-held--r02.result.json) |
| complex-ja-procedure-held | complex-communication | held-out | 3 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-ja-procedure-held--r03.trace.jsonl) | [result](raw/complex-ja-procedure-held--r03.result.json) |
| complex-ja-procedure-held | complex-communication | held-out | 4 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-ja-procedure-held--r04.trace.jsonl) | [result](raw/complex-ja-procedure-held--r04.result.json) |
| complex-ja-procedure-held | complex-communication | held-out | 5 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-ja-procedure-held--r05.trace.jsonl) | [result](raw/complex-ja-procedure-held--r05.result.json) |
| control-code-held | unrelated-control | held-out | 1 | false | false | not-selected | [trace](raw/control-code-held--r01.trace.jsonl) | [result](raw/control-code-held--r01.result.json) |
| control-code-held | unrelated-control | held-out | 2 | false | false | not-selected | [trace](raw/control-code-held--r02.trace.jsonl) | [result](raw/control-code-held--r02.result.json) |
| control-code-held | unrelated-control | held-out | 3 | false | false | not-selected | [trace](raw/control-code-held--r03.trace.jsonl) | [result](raw/control-code-held--r03.result.json) |
| control-code-held | unrelated-control | held-out | 4 | false | false | not-selected | [trace](raw/control-code-held--r04.trace.jsonl) | [result](raw/control-code-held--r04.result.json) |
| control-code-held | unrelated-control | held-out | 5 | false | false | not-selected | [trace](raw/control-code-held--r05.trace.jsonl) | [result](raw/control-code-held--r05.result.json) |
| control-debug-held | unrelated-control | held-out | 1 | false | false | not-selected | [trace](raw/control-debug-held--r01.trace.jsonl) | [result](raw/control-debug-held--r01.result.json) |
| control-debug-held | unrelated-control | held-out | 2 | false | false | not-selected | [trace](raw/control-debug-held--r02.trace.jsonl) | [result](raw/control-debug-held--r02.result.json) |
| control-debug-held | unrelated-control | held-out | 3 | false | false | not-selected | [trace](raw/control-debug-held--r03.trace.jsonl) | [result](raw/control-debug-held--r03.result.json) |
| control-debug-held | unrelated-control | held-out | 4 | false | false | not-selected | [trace](raw/control-debug-held--r04.trace.jsonl) | [result](raw/control-debug-held--r04.result.json) |
| control-debug-held | unrelated-control | held-out | 5 | false | false | not-selected | [trace](raw/control-debug-held--r05.trace.jsonl) | [result](raw/control-debug-held--r05.result.json) |
| control-lookup-held | unrelated-control | held-out | 1 | false | false | not-selected | [trace](raw/control-lookup-held--r01.trace.jsonl) | [result](raw/control-lookup-held--r01.result.json) |
| control-lookup-held | unrelated-control | held-out | 2 | false | false | not-selected | [trace](raw/control-lookup-held--r02.trace.jsonl) | [result](raw/control-lookup-held--r02.result.json) |
| control-lookup-held | unrelated-control | held-out | 3 | false | false | not-selected | [trace](raw/control-lookup-held--r03.trace.jsonl) | [result](raw/control-lookup-held--r03.result.json) |
| control-lookup-held | unrelated-control | held-out | 4 | false | false | not-selected | [trace](raw/control-lookup-held--r04.trace.jsonl) | [result](raw/control-lookup-held--r04.result.json) |
| control-lookup-held | unrelated-control | held-out | 5 | false | false | not-selected | [trace](raw/control-lookup-held--r05.trace.jsonl) | [result](raw/control-lookup-held--r05.result.json) |
| explicit-en-clarify-status-held | explicit-request | held-out | 1 | true | true | selected-with-visible-change | [trace](raw/explicit-en-clarify-status-held--r01.trace.jsonl) | [result](raw/explicit-en-clarify-status-held--r01.result.json) |
| explicit-en-clarify-status-held | explicit-request | held-out | 2 | true | true | selected-with-visible-change | [trace](raw/explicit-en-clarify-status-held--r02.trace.jsonl) | [result](raw/explicit-en-clarify-status-held--r02.result.json) |
| explicit-en-clarify-status-held | explicit-request | held-out | 3 | true | true | selected-with-visible-change | [trace](raw/explicit-en-clarify-status-held--r03.trace.jsonl) | [result](raw/explicit-en-clarify-status-held--r03.result.json) |
| explicit-en-clarify-status-held | explicit-request | held-out | 4 | true | true | selected-with-visible-change | [trace](raw/explicit-en-clarify-status-held--r04.trace.jsonl) | [result](raw/explicit-en-clarify-status-held--r04.result.json) |
| explicit-en-clarify-status-held | explicit-request | held-out | 5 | true | true | selected-with-visible-change | [trace](raw/explicit-en-clarify-status-held--r05.trace.jsonl) | [result](raw/explicit-en-clarify-status-held--r05.result.json) |
| explicit-ja-bunshou-held | explicit-request | held-out | 1 | true | true | selected-with-visible-change | [trace](raw/explicit-ja-bunshou-held--r01.trace.jsonl) | [result](raw/explicit-ja-bunshou-held--r01.result.json) |
| explicit-ja-bunshou-held | explicit-request | held-out | 2 | true | true | selected-with-visible-change | [trace](raw/explicit-ja-bunshou-held--r02.trace.jsonl) | [result](raw/explicit-ja-bunshou-held--r02.result.json) |
| explicit-ja-bunshou-held | explicit-request | held-out | 3 | true | true | selected-with-visible-change | [trace](raw/explicit-ja-bunshou-held--r03.trace.jsonl) | [result](raw/explicit-ja-bunshou-held--r03.result.json) |
| explicit-ja-bunshou-held | explicit-request | held-out | 4 | true | true | selected-with-visible-change | [trace](raw/explicit-ja-bunshou-held--r04.trace.jsonl) | [result](raw/explicit-ja-bunshou-held--r04.result.json) |
| explicit-ja-bunshou-held | explicit-request | held-out | 5 | true | true | selected-with-visible-change | [trace](raw/explicit-ja-bunshou-held--r05.trace.jsonl) | [result](raw/explicit-ja-bunshou-held--r05.result.json) |
| explicit-ja-suikou-held | explicit-request | held-out | 1 | true | true | selected-with-visible-change | [trace](raw/explicit-ja-suikou-held--r01.trace.jsonl) | [result](raw/explicit-ja-suikou-held--r01.result.json) |
| explicit-ja-suikou-held | explicit-request | held-out | 2 | true | true | selected-with-visible-change | [trace](raw/explicit-ja-suikou-held--r02.trace.jsonl) | [result](raw/explicit-ja-suikou-held--r02.result.json) |
| explicit-ja-suikou-held | explicit-request | held-out | 3 | true | true | selected-with-visible-change | [trace](raw/explicit-ja-suikou-held--r03.trace.jsonl) | [result](raw/explicit-ja-suikou-held--r03.result.json) |
| explicit-ja-suikou-held | explicit-request | held-out | 4 | true | true | selected-with-visible-change | [trace](raw/explicit-ja-suikou-held--r04.trace.jsonl) | [result](raw/explicit-ja-suikou-held--r04.result.json) |
| explicit-ja-suikou-held | explicit-request | held-out | 5 | true | true | selected-with-visible-change | [trace](raw/explicit-ja-suikou-held--r05.trace.jsonl) | [result](raw/explicit-ja-suikou-held--r05.result.json) |
