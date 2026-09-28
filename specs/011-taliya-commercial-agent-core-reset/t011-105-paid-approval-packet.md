# T011-105 Paid Approval Packet

Date: 2026-06-04

Purpose: approve exactly one capped paid evidence batch for T011-105 after the current no-cost readiness gates are green.

## Current State

- Current task lock: T011-105 - run golden transcripts and "do not do" fixtures.
- Current source fingerprint: `e458fcec6bb36bed281b3b7437582554e9b02d89d958d3bb4f216f95b4ef6987`.
- Readiness gate: `agent-runtime-spec011-t011-105-readiness` passed 13/13 with `ready_for_paid_batch`.
- Closure gate: `agent-runtime-spec011-t011-105-closure` is intentionally red at 2/11 with `fail_missing_or_failed_paid_evidence`.
- Latest paid batch spend already consumed: US$0.005045.
- No paid OpenAI command may run without fresh explicit approval.

## Last Paid Failure

The latest paid batch ran on stale fingerprint `b6bc712960ac06a93f80eff575a732cfb7e3d86f22cc0e7a6cbfce54fe159c9b`.

- `final-pain-first`: failed 0/1 after HTTP 200 because the response did not reuse lead context terms `whatsapp` and `interessado`.
- `step3g-long-conversation`: not run.
- Four missing "do not do" scenarios did not run because the batch stops on first paid failure.

Failure shape:

- `final-pain-first`: the action-first LLM selected `offer_diagnostic_from_pain` but omitted `diagnostic_intent.details.pain_context_human`; the compiler rendered a generic fallback, so the output lost the lead's concrete WhatsApp/interested-lead context.

Local fix is no-cost validated and remains LLM-first:

- The action-first correction now asks the LLM for a compact `ConductorActionDecision` instead of the full route/state/template/render object.
- The compiler derives state/render/projection from the LLM-selected action and validators still enforce product facts, diagnostics, Sales Inbox, waitlist, demo, and handoff contracts.
- Every exposed `TurnAction` is now either compiled or operationally handled by a release gate; no pending action bucket remains before paid readiness.
- Pain-first action validation now rejects `offer_diagnostic_from_pain` without LLM-provided `pain_context_human`; the compiler no longer renders a generic pain-first fallback.
- Normal commercial understanding remains LLM-first; deterministic code compiles and validates the selected action instead of choosing commercial intent from raw text.

## No-Cost Evidence Before Approval

Latest no-cost evidence on current fingerprint:

- Known critical validator recovery gate: 9/9 passed with US$0 spend, covering `pain_first_must_offer_diagnostic`, `unsupported_schema_version`, `diagnostic_start_must_ask_active_students`, `pain_first_diagnostic_offer_must_use_diagnostic_route`, `diagnostic_urgency_answer_not_captured`, `diagnostic_next_question_invalid`, `diagnostic_next_question_not_missing`, `diagnostic_final_demo_stage_missing`, `diagnostic_final_staged_order_invalid`, `price_question_missing_price_answer`, `price_question_missing_diagnostic_hook`, `price_question_missing_diagnostic_offer`, `demo_direct_question_flags_missing`, `stale_demo_direct_without_current_request`, and `sales_inbox_diagnostic_status_mismatch`.
- Targeted pain-first action/compile/adapter tests: 16/16 passed.
- Action coverage + compiler/conductor/widget focused tests: 68/68 passed.
- Action trace/repair adapter focused tests: 2/2 passed.
- Full runtime pytest sweep: 716/716 passed.
- Mocked conductor gate: 6/6 passed.
- Active-path static audit: 8/8 passed.
- T011-105 safety audit: 12/12 passed.
- T011-105 readiness: 13/13 passed.
- Protected `/pilates`, `floating-agent`, and Sales Inbox UI source diff: empty.

## Exact Approved Command

Only this command shape is allowed after explicit approval:

```powershell
node scripts\eval-agent-runtime-spec011-t011-105-paid-batch.mjs --approval-token T011-105-US0.36 --approved-budget-usd 0.36
```

The runner must refuse:

- missing approval token;
- wrong approval token;
- env-var-only approval;
- `--continue-on-failure`;
- source fingerprint drift before or between paid phases.

## Budget And Stop Rules

Approved ceiling for one batch: US$0.36.

Internal caps:

- `final-pain-first`: max 1 model call, max US$0.03.
- `step3g-long-conversation`: max 14 model calls, max US$0.25.
- four missing "do not do" scenarios: max 4 model calls, max US$0.08.

The runner must stop after any paid failure. If it fails, inspect and fix locally before any new paid rerun.

## Closure Criteria

T011-105 can close only after:

- paid batch report passes on the current source fingerprint;
- paid pain-first report passes;
- paid long-conversation report passes;
- paid four-case "do not do" report passes;
- golden aggregation passes 9/9 and selects fresh evidence;
- do-not-do aggregation passes 8/8 and selects fresh evidence;
- closure gate passes 11/11;
- `tasks.md`, `coverage-map.md`, and `implementation-ledger.md` are updated after the passing closure.

## Not Allowed

- Do not weaken validators, closure checks, fixture expectations, or source-fingerprint checks to pass.
- Do not add deterministic commercial routing from lead text.
- Do not touch `/pilates`, `floating-agent`, Sales Inbox UI, multi-tenant, client/studio WhatsApp, checkout, or `runtime/runner.py`.
