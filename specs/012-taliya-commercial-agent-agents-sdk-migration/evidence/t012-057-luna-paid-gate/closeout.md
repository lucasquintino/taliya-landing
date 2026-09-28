# T012-057 Luna paid gate closeout

## Decision

T012-057 passed. `gpt-5.6-luna` completed three consecutive canonical rounds
at `9/9`, and every transcript was reviewed manually. The targeted migration
set also passed `3/3`. Production was not switched during this task.

## Consecutive canonical rounds

| Round | Result | Operations | Repairs | Cost | Wall time |
| --- | ---: | ---: | ---: | ---: | ---: |
| Success 1 | 9/9 | 33 | 3 | `$0.124465` | 89.070 s |
| Success 2 | 9/9 | 33 | 3 | `$0.123919` | 90.534 s |
| Success 3 recovery | 9/9 | 33 | 3 | `$0.122070` | 108.791 s |

The automated 9/9 attempt between success rounds 2 and 3 was rejected during
human review because the WhatsApp answer contained redundant specific and
generic product blocks. Its cost remains in the cumulative ledger. A no-cost
answer-adequacy correction and isolated paid retest passed before the final
round.

## Baseline comparison

The archived approved `gpt-5.4-mini` baseline was 9/9, 33 operations, 3
repairs, `$0.087158`, and 76.495 seconds. The three accepted Luna rounds
averaged `$0.123485` and 96.132 seconds: about 41.7% higher cost and 25.7%
higher wall time in this harness. Structural stability was equal across the
accepted samples. Luna preserved the approved behavior and handled the new
structured contracts, but this gate does not claim a cost or latency advantage.

## Cumulative budget

- User-reported balance before the gate: `$1.03`.
- Approved hard ceiling: `$0.75`.
- Reported paid spend: `$0.685395`.
- Conservative unreconciled reserve: `$0.020000`.
- Operationally accounted spend: `$0.705395`.
- Remaining approved ceiling: `$0.044605`.

## No-cost verification

- Focused answer-adequacy regression set: `82 passed`.
- Full Spec 012: `294 passed / 718 deselected`.
- Active production gate: `526 passed`.
- Focused Ruff and `git diff --check`: passed.
- Pinned Docker health: passed with Luna, OpenAI `2.44.0`, and Agents SDK
  `0.18.0`.

## Next gate

T012-058 may deploy the compatibility build while preserving the current
production model. The Luna model switch remains T012-059 and must retain the
rollback and monitoring conditions.
