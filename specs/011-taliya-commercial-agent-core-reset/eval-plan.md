# Eval Plan - Taliya Commercial Agent Core Reset

The eval plan exists to prevent another structurally green but behaviorally bad release. It measures the transcript, the structured decision, validation, persistence, Sales Inbox projection, delivery behavior, and model usage together.

## Principles

- PASS means the user-facing conversation is acceptable, not only that JSON parsed.
- Every commercial answer must be traceable to a conductor decision.
- Every product fact must be traceable to official product knowledge and, where product surface/access/setup/agent/mode behavior is involved, Spec 006 product contracts.
- Every diagnostic conclusion must be traceable to ledger evidence.
- Every rendered message must be traceable to approved templates or approved safety fallback.
- Sales Inbox consistency is part of correctness.
- Skipped or missing evidence is FAIL.
- PASS is never automatic. Judge review can help triage quality, but it cannot override deterministic failures, missing trace, missing model usage, or incomplete Sales Inbox projection.

## Eval Layers

### Layer 1 - Static Contract Audit

Run before behavior tests:

- Search for commercial regex/if/template-first paths outside allowed operational/safety modules.
- Search for old v2 fallback usage in public widget/WhatsApp paths.
- Search for commercial logic added to `runtime/runner.py` or any equivalent orchestration brain.
- Search for customer-facing internal labels and banned phrases.
- Search for semantic renderer defaults.
- Search for generic whole-message template variables and unregistered customer-facing prose variables.
- Search for adapter/Sales Inbox inferred facts being promoted to reliable memory without source/confidence labels.
- Search for product facts hardcoded in prompts, templates, tests, fallbacks, or route logic when they belong in official product knowledge or Spec 006.
- Search for deterministic routing terms such as price/price equivalents, plan, demo, diagnostic, waitlist, "como funciona", Instagram/source opening, pain/dor, WhatsApp product questions, student counts, plan fit, objections, and mixed intent.
- Verify new modules follow one-responsibility ownership.

Blocking examples:

- `if "preco" in text` selecting a customer-facing price template.
- `route_from_text` deciding product/diagnostic/waitlist route.
- Renderer filling missing `pain_context_human` with generic copy.
- Adapter falling back to `agent-v2-response-generator`.
- Prompt or template embedding plan limits, checkout behavior, launch promises, or integration promises outside official product sources.
- Any `runner.py` change that chooses a commercial route or response for price, demo, diagnostic, waitlist, product explanation, pain-first, or source-opening turns.

### Layer 2 - Unit And Contract Tests

Test deterministic components:

- Turn Gate idempotency, locks, pause, outbox sequence, deferred inbound handling, and no parallel replies while a response is being delivered.
- Context Builder separates internal metadata from customer-visible facts.
- Product knowledge retrieval returns facts but does not decide behavior.
- Schema validation for conductor output.
- Validators for direct question, diagnostic ledger, waitlist/demo gating, product facts, internal leaks, price/student-count disambiguation, Sales Inbox completeness.
- Renderer rejects missing semantic variables and renders approved chunks.
- Persistence/projection writes runtime and Sales Inbox state consistently.
- Projection inference never re-enters conductor context as reliable customer-provided fact unless validated.
- Trace schema is complete for normal commercial turns.
- Product claim validators enforce official product knowledge and Spec 006 product contracts.
- Human handoff pause/resume is stateful and audited.
- `/pilates` desktop/mobile baseline exists before widget cutover work and no visual/layout drift is introduced.

### Layer 3 - Mocked Conductor Fixtures

Use fixed conductor JSON fixtures to test:

- Valid decisions render/persist correctly.
- Invalid decisions fail for the right reason.
- Repair loop receives precise validation errors.
- Blocked cases produce safe operational fallback/handoff.

These tests should not call OpenAI.

### Layer 3A - Golden Transcript And Do-Not-Do Fixtures

Run versioned fixtures before real model suites:

- Golden transcripts for price, price-plus-pain, pain-first, Instagram/source opening, WhatsApp product question, product demo, diagnostic, waitlist, human handoff, post-demo/product-demo, and long conversation.
- "Do not do" fixtures for early phone capture, invented checkout/payment, invented discount/date/VIP status, invented integrations/certifications, collecting client/studio WhatsApp numbers, wrong student/customer language, and interpreting `497` as active students.

Reports must show transcript diff, conductor JSON diff, rendered-message diff, validator diff, usage diff, and Sales Inbox projection diff.

### Layer 4 - Real Model Regression Suite

Run quota-limited real OpenAI scenarios from `regression-cases.md`.

Minimum required groups:

- Cold/opening.
- Direct price and price-plus-pain.
- Product follow-up: how it works, WhatsApp, integration, security, comparison, out-of-profile.
- Diagnostic start, short answers, mixed side questions, mandatory urgency, final diagnostic.
- Waitlist before and after fit.
- Handoff/pause/resume.
- Delivery concurrency/chunks.
- Sales Inbox projection.
- Mandatory trace completeness.

Every scenario report must include:

- Input transcript.
- Channel/source metadata.
- Context snapshot.
- Conductor raw JSON.
- Validator report.
- Repair report if any.
- Rendered outbound messages.
- Model usage and cost.
- Runtime state diff.
- Sales Inbox projection diff.
- Delivery/outbox events.
- Pass/fail reason.

### Layer 5 - Judge / Quality Review

Use a judge only after deterministic checks pass.

Judge rubric:

- Answers direct question first.
- Uses natural Taliya voice.
- Avoids internal/technical language.
- Does not invent facts.
- Does not over-sell waitlist/demo.
- Keeps diagnostic practical and staged.
- Does not repeat or skip diagnostic questions.
- Handles mixed intent gracefully.

Judge PASS cannot override deterministic FAIL.

### Layer 6 - Manual Product-Owner Review

Required before production cutover:

- Final diagnostic transcript set.
- Product follow-up transcript set.
- Price/plan/demo transcript set.
- Waitlist transcript set.
- WhatsApp chunking/concurrency transcript set.
- Sales Inbox screenshots or data export proving completeness.
- Trace samples proving input/context/decision/render/usage/projection chain.
- Approval log entries for sensitive decisions and approved transcript groups.

### Layer 7 - Shadow Mode, Rollback, And Full Cutover

Required before customer-facing activation:

- Shadow mode runs the new core in parallel without responding to the lead.
- Shadow reports compare conductor decision, validators, render plan, trace, model usage, and Sales Inbox projection against golden transcripts and manual review samples.
- Feature flag rollback is tested and proves disabling the new core does not re-enable the old deterministic commercial brain as public responder.
- Full production cutover runs with first-hours emergency monitoring for trace quality, handoff pause, Sales Inbox completeness, fallback rate, model usage, duplicate/interleaved delivery, P0 behavior, and cost.

## Failure Severity

- P0: unsafe, internal leak, wrong product fact, wrong numeric grounding, diagnostic final wrong/skipped, duplicate outbound, human pause violation, Sales Inbox missing, false PASS.
- P1: user-facing quality issue, weak diagnostic language, unnecessary repeat, missing useful steering, channel awkwardness.
- P2: minor wording, trace metadata gap, non-blocking report readability issue.

Release requires:

- 0 P0.
- 0 unresolved P1 in required flows.
- Static audit clean.
- Mandatory trace complete for all sampled normal commercial turns.
- Shadow mode approved.
- Rollback proof approved.
- First-hours emergency watch criteria and abort path approved before full activation.
- Product-owner approval for manual transcript groups.

## PASS Invalidators

Mark FAIL automatically if:

- Scenario has no transcript.
- Scenario has no rendered output when output is expected.
- Commercial output has no model usage.
- Mandatory trace fields are missing.
- Decision JSON missing required fields.
- Validator did not run.
- Sales Inbox projection missing or inconsistent.
- Unregistered free-form template variable is rendered.
- Adapter/Sales Inbox inferred data is reused as reliable fact without source/confidence.
- Product fact appears in prompt/template/test/fallback instead of official product knowledge or Spec 006 source where applicable.
- `runner.py` or old TS v2 public paths answer/route a commercial turn.
- Widget/landing-affecting cutover runs without `/pilates` baseline/no-drift evidence.
- Internal text appears in customer message.
- Official product facts are contradicted.
- Diagnostic ledger completes without all mandatory keys.
- Urgency is skipped before final diagnostic.
- A simple pending diagnostic answer like "120" is rejected without evidence.
- Eval says PASS based only on structural JSON.
- Real bug regression case did not fail against the current system before the fix.
- Shadow mode, rollback proof, or first-hours emergency watch readiness is missing for production activation.

## Reporting Format

Each eval report should include:

- `scenario_id`
- `status`: PASS/FAIL
- `severity`
- `channel`
- `input_messages`
- `rendered_messages`
- `decision_json`
- `validator_results`
- `repair_attempts`
- `model_usage`
- `runtime_state`
- `sales_inbox_projection`
- `delivery_events`
- `trace_complete`
- `schema_version`
- `golden_transcript_diff`
- `assertions`
- `failure_reason`
- `artifact_paths`

## Cost And Model Policy

- Normal turns should use one conductor model call.
- Repair allows one extra model call.
- Low-confidence complex diagnostic may use one extra specialist/reasoning call only when logged with reason.
- Eval judge calls are separate from runtime behavior and must be labeled as eval-only.
- Cost optimization must happen through prompt/context/retrieval/model choice before any commercial deterministic shortcut is considered.
- Cost optimization fails if it removes model usage from normal commercial turns or degrades golden transcript outcomes without explicit product-owner approval.

## Release Sequence

1. Static audit passes.
2. Unit/contract tests pass.
3. Mocked conductor fixture tests pass.
4. Golden transcripts and do-not-do fixtures pass or approved diffs are recorded.
5. Real model P0 regression suite passes.
6. Full required real model suite passes within budget.
7. Sales Inbox projection export reviewed.
8. Mandatory trace export reviewed.
9. `/pilates` baseline/no-drift evidence reviewed for widget cutover work.
10. Manual product-owner transcript review approves.
11. Shadow mode passes.
12. Feature flag rollback proof passes.
13. First-hours emergency watch criteria, abort path, and monitoring fields are approved.
14. Production preflight is prepared separately.
