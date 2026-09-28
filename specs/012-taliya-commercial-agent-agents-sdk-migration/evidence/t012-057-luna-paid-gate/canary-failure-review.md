# T012-057 Luna canary failure review

Date: 2026-08-04/05

## Paid attempt

- Model: `gpt-5.6-luna`
- Scenario: `luna-price-objection-context`
- Result: failed and stopped before the targeted or canonical suites
- Model operations: `5`
- Exact cost: `$0.016029`
- Cumulative approved ceiling: `$0.75`
- Remaining approved ceiling: `$0.733971`
- Complete evidence: `canary/20260805T002009Z/`

The first turn answered the official prices and offered the diagnostic. On the
second turn, Luna correctly interpreted `hmm, talvez fique pesado` as
`price_objection` plus `budget_concern` and selected
`answer_price_objection`. No customer-facing response was delivered because
the validator bridge blocked the compiled result with
`price_question_missing_diagnostic_offer`.

## Root cause

The action-first compiler already maps `answer_price_objection` to
`diagnostic_offered`. The legacy validator bridge did not translate that
action to `diagnostic.action=offer`, although the superseded compiler already
did so and the binding price-objection contract expects the diagnostic next
step to be preserved. The model interpretation, approved objection template,
and renderer were correct.

## No-cost correction

The bridge now maps entry/product `answer_price_objection` to
`diagnostic.action=offer`. The post-diagnostic action
`answer_price_objection_with_context` remains unchanged. No raw-text routing,
regex commercial decision, template copy change, or extra diagnostic message
was added.

The Markdown report writer now renders exchanges from every turn instead of
only committed transcript entries. Failed/suppressed turns retain the user
message and explicitly state that no assistant message was delivered, with the
turn status and issue codes. The original failed report was regenerated with
the complete second user message.

## Verification after correction

- Exact bridge regression: passed.
- Exact two-turn mocked canary through SDK runner/compiler/validators/renderer:
  passed with zero repairs and `$0` spend.
- Focused Ruff: passed.
- Full Spec 012: `285 passed / 718 deselected`.
- Active production gate: `517 passed`.
- Pinned Linux Docker image `taliya-agent-runtime:luna-canary-fix`: built.

No additional paid call was made after the failed canary. Targeted and
canonical suites remain blocked pending review of this checkpoint.
