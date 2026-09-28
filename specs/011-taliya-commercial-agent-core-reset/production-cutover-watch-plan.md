# Production Cutover Watch Plan - Spec 011

Task: T011-099

This is the first-hours emergency watch package for the Taliya commercial agent reset. It prepares the 100 percent production cutover path the user approved, but it does not itself approve production activation.

Do not activate without Phase 10 approval.

## Scope

- Traffic: 100 percent of Taliya-owned commercial leads from the widget and Taliya-owned WhatsApp after approval.
- Not canary: the plan intentionally avoids staged canary because the current production behavior is considered worse than the reset risk.
- Rollback: `TALIYA_SPEC011_COMMERCIAL_CORE_ENABLED=false`.
- Rollback behavior: operational fallback or retryable `spec011_core_disabled`, never the old TS v2 commercial responder and never `runtime/runner.py` commercial answering.
- First watch window: 240 minutes.
- First check: within 5 minutes.
- Cadence: every 15 minutes by default, every 30 minutes for aggregate cost review.

## Required Evidence Before Activation Review

- Shadow mode report passes.
- Shadow comparison against manual samples passes.
- Rollback report passes.
- Runner quarantine report passes.
- Public fallback quarantine report passes.
- `/pilates` no-drift report passes with manual visual review.
- Phase 10 release gates still remain separate: static, unit, mocked, real-model, golden, do-not-do, Sales Inbox export, trace export, manual product-owner review, production preflight, and approval log.

## Monitors

1. Trace quality
   - Check `trace_id`, input, context, decision, validator, repair, render plan, rendered messages, model usage, runtime diff, delivery events, Sales Inbox projection, and `trace_complete`.
   - Abort if any normal commercial turn lacks trace evidence or references legacy runner/TS v2 commercial answering.

2. Human handoff behavior
   - Check handoff status, reason, delivery control, runtime diff, projection, and message count.
   - Abort if AI replies while human is active or resumes without explicit event/state evidence.

3. Sales Inbox completeness
   - Check projection for stage, summary, case-family fields, operator next action, diagnostic/waitlist/handoff state, and source labels.
   - Abort if projection is missing, mismatched, incomplete, or promotes inferred facts as reliable.

4. Model usage
   - Check model, input tokens, output tokens, and cost on every normal commercial turn.
   - Abort if commercial understanding happens without model usage.

5. Cost
   - Check aggregate first-hours cost, per-turn cost, retry/repair spikes, and model usage.
   - Abort if cost exceeds approved budget or low cost means conductor bypass.

6. Fallback and error rate
   - Check status, fallback reason, error code, retryability, channel, and conversation scope.
   - Abort if fallback/error rate reaches 5 percent or if any fallback generates deterministic commercial answer copy.

7. Duplicate and interleaved delivery
   - Check idempotency keys, provider message ids, delivery events, outbox status, deferred inbound, and message count.
   - Abort on duplicate public replies or processing an inbound during active outbound delivery as a fresh commercial intent.

8. P0 behavior
   - Check sampled transcripts/traces for internal leaks, wrong product facts, wrong numeric grounding, skipped diagnostic urgency, repeated answered diagnostic question, duplicate delivery, Sales Inbox gaps, and false PASS.
   - Abort on a single P0.

9. Rollback readiness
   - Check rollback, runner quarantine, public fallback quarantine, and protected source diff.
   - Abort if rollback cannot be executed within 5 minutes or if it would reactivate an old commercial brain.

## Abort Criteria

Abort criteria are binding for the first-hours watch.

Abort immediately if any of these occurs:

- Internal/source/debug text leaks into rendered output.
- Product fact, price, plan, checkout, launch date, discount, VIP, integration, certification, demo availability, or capability is invented or misstated.
- Numeric grounding is wrong, especially `497` as student count or a student count as price.
- Diagnostic completes while a mandatory question, especially urgency, is missing.
- Same inbound produces duplicate public replies.
- Lead message during chunks is processed before current outbound delivery finishes.
- AI sends any commercial reply while human handoff is active.
- Sales Inbox projection is missing, wrong, incomplete, or promotes inferred facts as reliable.
- Eval/report says PASS while transcript, trace, model usage, validator result, delivery event, or Sales Inbox projection evidence is missing or contradictory.
- Public path can reach old TS v2 or `runtime/runner.py` commercial answering.

## Operator Actions

- Pre-activation: rerun static, rollback, quarantine, shadow, watch-readiness, TypeScript, and focused runtime suites.
- First 5 minutes: sample widget and Taliya-owned WhatsApp turns for trace id, model usage, delivery events, and Sales Inbox projection.
- Every 15 minutes: review trace quality, handoff, Sales Inbox, fallback/errors, duplicate/interleaved delivery, and P0 behavior.
- Every 30 minutes: review aggregate cost and token usage.
- Abort: set `TALIYA_SPEC011_COMMERCIAL_CORE_ENABLED=false`, preserve reports/traces/transcripts, stop activation review, and open a red-first regression task.

## Closure Status

This plan is watch-readiness evidence for T011-099 only. It does not close Phase 10, does not approve production activation, and does not replace the separate production preflight/cutover plan required by T011-110.
