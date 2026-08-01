# Headless Pi smoke results

- Runs: 6
- Routing expectations met: 2/2
- Missing final outputs: 0
- Protected-string failures: 0

| Scenario | Kind | Arm | Activation | Result | Evidence |
|---|---|---|---|---|---|
| behavior-rewrite | behavior | candidate-skill | none | pass | [Raw trace](raw/behavior-rewrite--candidate-skill.trace.jsonl) |
| behavior-rewrite | behavior | current-skill | none | pass | [Raw trace](raw/behavior-rewrite--current-skill.trace.jsonl) |
| behavior-rewrite | behavior | no-skill | none | pass | [Raw trace](raw/behavior-rewrite--no-skill.trace.jsonl) |
| routing-direct | routing | direct | direct-invocation | pass | [Raw trace](raw/routing-direct--direct.trace.jsonl) |
| routing-negative | routing | automatic | none | pass | [Raw trace](raw/routing-negative--automatic.trace.jsonl) |
| routing-positive | routing | automatic | automatic-read | pass | [Raw trace](raw/routing-positive--automatic.trace.jsonl) |
