# T012-027 Attempts 4-7 And Ideal-Conversation Series - 2026-06-10

User approval: iteration runs until the 15/15 structural pass bar plus the
ideal-conversation round, cumulative hard ceiling `$2.00`, no public cutover.

## Frozen-Scenario Iterations (Attempts 4-7)

- Attempt 4 (repair enabled): 11/15, `$0.098629`. Remaining failures were all
  the self-attested `answered_before_steering` flag with no repair headroom.
- Fix: replaced the self-attested boolean with `answering_template_id` - the
  model names which template answers the obligation and the adapter derives
  the flag by deterministic plan membership. Self-attestation removed.
- Attempt 5: 13/15, `$0.096869`. Left: ungrounded plan recommendation source
  and one max_turns from sequential tool reads.
- Fix: deterministic state preamble injected into the input (the pipeline's
  "load compact memory" step), so the model stops spending turns rediscovering
  state; grounding instruction for the final diagnostic (must read official
  plan facts before delivering).
- Attempt 6: 14/15, `$0.079732`. Left: scenario 7 honest `model_decision`
  label on an ungrounded plan recommendation - correct validator block.
- Attempt 7 (after grounding probe): **15/15 passed_structural**, 27
  operations, `$0.069680`, 1 repair. One transient OpenAI 403 occurred before
  the successful run; the harness now records provider errors per scenario
  instead of crashing.

## Ideal-Conversation Series (12-turn full funnel, state committed between turns)

New no-cost harness: `ideal_conversation.py` runs the golden funnel script
turn by turn, committing state deterministically from each validated proposal
(runtime's commit-after-validation rule) and carrying the rendered transcript.

- Run 1: 12/12 "structural" but conversationally broken - triage answered
  every turn itself with opening templates ("Oi, tudo bem?" mid-conversation),
  never asked a diagnostic question. Root cause: triage self-answering plus
  narrow opening catalog; the "finalize directly" cost guidance made it worse.
  Key lesson: structural validity alone hides wrong-template-for-the-moment.
- Run 2: instruction-only fixes failed again (triage answered price with an
  empty variable). Prompting was not enough.
- Structural fix (SDK-native): triage became a pure router - no tools,
  `tool_choice="required"`, so its only possible action is one handoff; the
  specialist choice remains the model's semantic decision. Test
  `test_spec012_sdk_agents.py` updated accordingly (spike-evidence design
  revision).
- Run 3: routing correct, 7/12, but sticky product agent absorbed the
  diagnostic and conducted it badly. Fixes: sticky state only for flow owners
  (diagnostic in progress, handoff paused); product instructed to hand the
  diagnostic to the diagnostic agent; new deterministic validator rule
  `sdk_template_not_owned_by_agent` (an agent may only propose templates from
  its own catalog) plus `sdk_router_cannot_finalize`.
- Run 4: routing perfect (entry, entry, product, diagnostic) but routed turns
  had no repair headroom under 3 ops. Conversation runs now use 4 ops per
  turn (handoff + read + final + repair), consistent with the design-lock
  "triage plus specialist plus one repair".
- Run 5: **10/12 structural, routing and role boundaries all correct**, repair
  recovering failures mid-conversation. Honest content reading: gpt-5.4-mini
  conducts the multi-turn diagnostic poorly - skipped the active-students
  question, repeated deliver/plan-recommendation templates across turns 7-10,
  declared the diagnostic complete with 2 of 6 mandatory keys, and the sticky
  diagnostic agent answered the demo request (turn 11) instead of routing.

## Consolidated Finding For T012-028/029

Solved and proven on real calls: strict structured output, grounding of
price/plan claims, routing via forced-handoff router, role boundaries via
validators, repair loop, budget/tracing/abort controls, state-preamble
context, single-turn behavior (15/15).

Genuine open gap: multi-turn diagnostic conduct quality on `gpt-5.4-mini`
(question sequencing, no-repeat discipline, premature completion). This is a
model-capability boundary, not an architecture failure - the skill's cost
rule anticipates it ("use the configured low-cost model for normal turns",
strong model where needed). The natural next probe is the diagnostic agent on
a stronger model (`TALIYA_AGENT_STRONG_MODEL`, currently unset), which needs a
user decision on model and pricing.

Sticky-agent release on diagnostic completion is also pending (the diagnostic
agent kept turns after completion).

## Spend

- Attempts 4-7: `$0.344910` total.
- Ideal-conversation runs 1-5: `$0.273387` total.
- This approval cycle: ~`$0.636` of `$2.00`. All-time spike total: ~`$1.10`.
