# Release-candidate decision

Decision: **fail**

Candidate revision: `5b834f6f50117324e2eebf3932ef01fe86527bef`
Core matrix: 425 generations (routing and behavior only).

English, Japanese, and multilingual-core results are kept separate. Failed and non-gating checks remain visible.

| Gate | Group | Result | Actual | Threshold | Gating |
|---|---|---|---|---|---|
| core-generation-matrix | provenance | pass | 425 | exactly 200 routing + 225 behavior = 425 | yes |
| routing-explicit-recall | routing | pass | 1.0 | >= 0.95 | yes |
| routing-complex-recall | routing | pass | 1.0 | >= 0.85 | yes |
| routing-unrelated-fpr | routing | pass | 0.0 | <= 0.10 | yes |
| behavior-arm-provenance | provenance | pass | ['no-skill', '178eaf8', '5b834f6f50117324e2eebf3932ef01fe86527bef'] | exact release arms and comparison | yes |
| english-mean-noncritical-preservation | behavior | pass | 4.947 | >= 4.5 | yes |
| english-critical-failures | behavior | fail | 6 | = 0 | yes |
| english-protected-string-changes | behavior | pass | 0 | = 0 | yes |
| english-candidate-win-rate | behavior | fail | 0.32 | >= 0.50 | removed after calibration |
| english-candidate-loss-rate | behavior | fail | 0.2 | <= 0.10 | removed after calibration |
| japanese-mean-noncritical-preservation | behavior | pass | 4.952 | >= 4.5 | yes |
| japanese-critical-failures | behavior | fail | 4 | = 0 | yes |
| japanese-protected-string-changes | behavior | pass | 0 | = 0 | yes |
| japanese-candidate-win-rate | behavior | fail | 0.4 | >= 0.50 | removed after calibration |
| japanese-candidate-loss-rate | behavior | fail | 0.32 | <= 0.10 | removed after calibration |
| multilingual-core-mean-noncritical-preservation | behavior | pass | 4.857 | >= 4.5 | yes |
| multilingual-core-critical-failures | behavior | fail | 4 | = 0 | yes |
| multilingual-core-protected-string-changes | behavior | pass | 0 | = 0 | yes |
| multilingual-core-candidate-win-rate | behavior | fail | 0.48 | >= 0.50 | removed after calibration |
| multilingual-core-candidate-loss-rate | behavior | fail | 0.28 | <= 0.10 | removed after calibration |
| boundary-en-equivalent | boundary | fail | 0.8 | >= 0.90 | yes |
| boundary-en-critical-changes | boundary | fail | 2 | = 0 | yes |
| boundary-ja-equivalent | boundary | pass | 1.0 | >= 0.90 | yes |
| boundary-ja-critical-changes | boundary | pass | 0 | = 0 | yes |
| boundary-post-candidate-disclosure | boundary | pass | True | must disclose post-candidate fixture | yes |
| human-candidate-regressions | human | fail | 0.75 | <= 0.10 | yes |
| human-critical-meaning-changes | human | fail | 2 | = 0 | yes |

The already-clear fixture was designed after candidate authorship and is supplemental; it is excluded from the 425-generation matrix.

Removed GPT rubric items: first_pass_understanding, naturalness, preference.
