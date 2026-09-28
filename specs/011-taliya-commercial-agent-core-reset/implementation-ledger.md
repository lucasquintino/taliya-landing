# Implementation Ledger - Taliya Commercial Agent Core Reset

Purpose: this is the execution control panel for Spec 011. It does not replace `spec.md`, `tasks.md`, or `coverage-map.md`; it keeps the implementation from drifting after long sessions, compaction, interruptions, or pressure to ship.

## Resume Protocol

Before continuing any implementation step:

1. Read `AGENTS.md`.
2. Read `.agents/skills/taliya-llm-first-agent/SKILL.md`.
3. Read this ledger.
4. Read the active task row in `tasks.md`.
5. Read the matching coverage rows in `coverage-map.md`.
6. Continue only from `Current Task Lock`.

If these files disagree, stop and reconcile the docs before changing runtime code.

## Current Status

| Field | Value |
| --- | --- |
| Current phase | Phase 10 - Verification And Approval |
| Last completed implementation task | T011-104A - action-first conductor correction, full action coverage gate, and readiness closure |
| Last completed control task | T011-009A/T011-009B - coverage-map gate and implementation anti-drift ledger |
| Current task lock | T011-105 paid golden/do-not-do evidence - blocked until explicit user approval for capped paid rerun |
| Public runtime status | Widget/web and Taliya-owned WhatsApp commercial turn paths are wired in code to the Spec 011 endpoint. Public old TS v2 commercial fallback reachability is blocked. The runtime API shell no longer imports/calls `runtime/runner.py`; legacy `/v1/agent-runs` rejects Taliya commercial turns and allows only zero-token `runtime_control` handoff operations. Old runner tests/evals/docs are explicitly labeled as legacy reference only, and real OpenAI production-path evals post to `/v1/taliya-commercial/turn`. T011-095 proved the widget cutover produced no `/pilates` protected source diff and no visual/layout drift after manual review of strict screenshot deltas. T011-096 added explicit shadow mode that runs the Spec 011 core, records trace/projection evidence, suppresses public delivery, and does not mutate live state. T011-097 added a replayable shadow comparison package: widget price/plan-fit and Taliya-owned WhatsApp diagnostic samples passed 110/110 assertions with public delivery suppressed and trace/projection evidence complete. T011-098 added and proved the explicit `TALIYA_SPEC011_COMMERCIAL_CORE_ENABLED` rollback flag: disabled-core traffic returns controlled operational fallback/error before public `fetch` or Python core execution and does not reactivate old TS v2 or Python runner commercial answering. T011-099 added and proved the first-hours emergency watch-readiness package for 100% cutover, with monitor fields, abort criteria, owners, operator actions, and Phase 10 activation block. T011-100 upgraded and passed the active-path static audit, and removed an active TS adapter fallback that inferred unsupported product-fact requests from user text instead of structured runtime output. T011-101 added and passed a replayable unit/contract gate over full runtime pytest, focused API/settings/widget/shadow tests, widget/WhatsApp Node adapter tests, TypeScript, static audit, runner/fallback/rollback guards, and protected source diff. T011-102 added and passed a replayable mocked conductor fixture gate; it also fixed an active repair-boundary gap so structurally valid conductor JSON with template-plan registry errors reaches validators/repair instead of dying before repair. T011-103 passed the P0 real-model observed-bug gate against `/v1/taliya-commercial/turn`: real OpenAI P0 fixture 9/9, report contract 41/41, delivery duplicate/interleaving gate 7/7, and gate wrapper 8/8. T011-104 closed the full required real-model suite. T011-105 golden/do-not-do is in progress; trace/projection exports, manual approval, rollback rehearsal, production preflight, and approval log remain incomplete. |
| Phase 3 status | Passed for isolated core only. Widget/WhatsApp adapter verification remains Phase 9. |
| Phase 4 status | Passed for isolated core only. Context snapshots are local eval/debug artifacts, not production traces. |
| Phase 5 status | Passed for isolated core and P0 real-model observed-bug gate. Full real-model/golden transcript validation remains Phase 10. |
| Phase 7 status | Passed for isolated core only. Adapter and production-path rendering remain Phase 9/10. |
| Phase 8 status | Passed for isolated core only. Adapter and production-path persistence/projection remain Phase 9/10. |
| Phase 8A status | Passed for isolated control-plane only. Production approval/cutover evidence remains Phase 10. |
| Phase 9 status | Passed for Phase 9 readiness: T011-090/T011-099 passed for widget and Taliya-owned WhatsApp adapter wiring, public old TS v2 fallback blocking, public runtime runner quarantine, legacy evidence labeling, `/pilates` no-drift evidence, technical shadow-mode plumbing, manual-sample shadow comparison, rollback proof, and first-hours emergency watch readiness. Final production activation is still blocked by Phase 10. |
| Last full focused validation | Latest no-cost fix after the paid pain-first context failure passed: targeted pain-first action/compile/adapter tests 16/16, action/compiler/conductor/widget focused suite 68/68, full runtime pytest 716/716, Ruff over touched action-first files, readiness script syntax check, T011-105 readiness 13/13 with `ready_for_paid_batch`, protected diff empty, and T011-105 closure 2/11 with expected `fail_missing_or_failed_paid_evidence`. The current readiness source fingerprint is `e458fcec6bb36bed281b3b7437582554e9b02d89d958d3bb4f216f95b4ef6987`. |
| Current T011-105 validation status | Paused, not closed. The latest paid T011-105 attempt on fingerprint `b6bc712960ac06a93f80eff575a732cfb7e3d86f22cc0e7a6cbfce54fe159c9b` spent US$0.005045 and stopped after `final-pain-first` failed because the rendered pain context did not reuse lead terms `whatsapp` and `interessado`. Local no-cost fix is green on fingerprint `e458fcec6bb36bed281b3b7437582554e9b02d89d958d3bb4f216f95b4ef6987`; fresh paid pain-first, long-conversation, and four do-not-do scenarios have not run on this fingerprint. |
| Next allowed action | Do not spend OpenAI credits without new explicit user approval. The next action is to request/receive approval for the exact capped paid command, then run T011-105 paid evidence. If not approved, stop at this no-cost ready state. |

## No-Cost Reconciliation - 2026-06-04

This reconciliation did not advance the task lock and did not spend OpenAI credits. It aligned the control docs with the real implementation state: `spec.md` now says implementation is in progress and blocked at T011-105, `tasks.md` keeps T011-008/T011-011 open as governance/evidence debt, and `coverage-map.md` no longer labels the already implemented core-schema contracts as merely planned.

Added `worktree-audit.md` as the current dirty-worktree risk register. The audit confirms the protected source diff is empty for `/pilates`, landing components/data, `lib/landing/floating-agent.ts`, and `components/internal/SalesInboxClient.tsx`; it also records the existing dirty one-line `runtime/runner.py` diff as a final-closure risk even though active-path static audit says the public Spec 011 runtime does not import or call runner.

Superseded by the action-first correction: current task lock is now T011-105 paid evidence. T011-105 remains blocked until the user explicitly approves a capped paid rerun on the action-first fingerprint.

## Paid Batch Attempt - 2026-06-04

The user explicitly approved one capped T011-105 paid batch with `--approval-token T011-105-US0.36 --approved-budget-usd 0.36`. The runner spent estimated US$0.108970 and stopped correctly after the first paid failure. Readiness passed first on fingerprint `b818ed2356dcc3f52456cabdae2c95de740d30186fe935f1a10ec63ffcc8e9d8`; `final-pain-first` passed 1/1; `step3g-long-conversation` failed 0/1 with HTTP 500 on turns 9, 11, 12, and 13; the four missing do-not-do scenarios did not run because the wrapper stops on first paid failure.

Concrete failures from the paid long conversation:

- Turn 9 `quero resolver agora`: final diagnostic repair still allowed a too-long `recommended_plan_or_range` plus missing/invalid final diagnostic staging to surface as HTTP 500.
- Turn 11 `achei caro`: price-objection repair incorrectly tried to attach `plan_price_summary` to `product.price_objection_value`, creating `template_plan_invalid` instead of structurally marking the diagnostic hook as an offer.
- Turn 12 `quero comecar, me coloca na lista`: provider JSON returned a non-boolean fact `renderable`, which failed Pydantic before validators/repair.
- Turn 13 `como funciona mesmo?`: renderer saw missing `contextual_next_step` after the earlier failed state cascade.

Local no-cost fixes after the paid failure stayed LLM-first: provider payload normalization now coerces non-boolean fact `renderable` to `false`, and price-objection repair preserves `product.price_objection_value` without adding an unsupported price-summary variable. Test hardening added a regression for non-boolean `renderable`, a regression for pending-diagnostic price objection repair, and a stronger long-conversation preflight fixture with an overlong plan recommendation.

Historical validation after that local fix passed with no additional paid spend on fingerprint `65d09c6969023d33cb720b42287adeee3cc712b0c4517f969679e35a2cfdd9b6`; this was superseded by the action-first correction and the current action-coverage fingerprint recorded in `Current Status`.

This paid-failure checkpoint is superseded: T011-104A and the later action-coverage hardening are complete. The current lock is T011-105 paid evidence, still requiring fresh explicit approval before any paid batch.

## Action-First Correction - 2026-06-04

The post-paid audit concluded that Spec 011's intended "LLM-first controlled" model was only partially implemented. The current conductor still asks the LLM to assemble too much of the final runtime shape: route, state, diagnostic action, template plan, variables, render order, and self-checks. Validators and repair correctly block many bad outputs, but the repeated paid failures show this creates a reactive loop where paid evals discover new invalid combinations.

Spec 011 now adds `action-contract.md` as a binding contract. The next work must introduce a Turn Situation Builder, a smaller LLM `ConductorActionDecision`, and a Decision Compiler. Deterministic code may compute state-derived allowed actions, obligations, and eligible template groups, but it must not infer commercial meaning from raw lead text or choose commercial actions/templates from keywords. The LLM remains the conversation brain by interpreting the inbound message and choosing one allowed action.

New task lock at that checkpoint: T011-104A. Phase 5B later passed with no-cost evidence; T011-105 paid golden/do-not-do remains blocked until readiness is regenerated on the new action-first source fingerprint.

## T011-058A Completion - 2026-06-04

Implemented `TurnSituation` schema and builder in `services/taliya-agent-runtime/app/core/taliya_commercial/turn_situation.py`. The builder derives mode, pending diagnostic question, completed/missing diagnostic keys, allowed actions, obligations, eligible template groups, official fact keys, state constraints, and forbidden actions from typed context and persisted state only.

Anti-determinism review: the builder does not inspect inbound text for commercial keywords and does not map words such as demo, caro, agora, WhatsApp, Instagram, dor, alunos, or lista into actions. A regression test proves diagnostic-mode action menus are identical across those raw-text variants.

Validation passed with no paid OpenAI spend:

- `python -m pytest services\taliya-agent-runtime\tests\test_spec011_turn_situation.py -q` = 5 passed.
- `python -m ruff check services\taliya-agent-runtime\app\core\taliya_commercial\turn_situation.py services\taliya-agent-runtime\tests\test_spec011_turn_situation.py` = passed.

Next task lock moved forward after this checkpoint; see T011-058B..T011-058F completion below. T011-105 paid rerun remains blocked.

## T011-058B/T011-058C Partial Evidence - 2026-06-04

Implemented the first no-cost action-first bridge:

- `ConductorActionDecision` and action-conductor request/schema tests now prove the LLM-facing normal-turn output is smaller and excludes route, state, template, render, and whole-response fields.
- `DecisionCompiler` now compiles the tested action subset into the existing `ConductorDecision` contract for validators/rendering:
  - direct product/price question -> official price template plus diagnostic offer;
  - pending diagnostic answer capture -> ledger update plus next diagnostic question;
  - final urgency capture -> staged final diagnostic render plan.
- Static compiler test proves the compiler does not read `context.inbound.text`, does not lowercase/casefold lead text, and does not import regex for commercial matching.

Validation passed with no paid OpenAI spend:

- `python -m pytest services\taliya-agent-runtime\tests\test_spec011_decision_compiler.py services\taliya-agent-runtime\tests\test_spec011_conductor_boundary.py services\taliya-agent-runtime\tests\test_spec011_turn_situation.py -q` = 40 passed.
- `python -m ruff check services\taliya-agent-runtime\app\core\taliya_commercial\decision_compiler.py services\taliya-agent-runtime\tests\test_spec011_decision_compiler.py services\taliya-agent-runtime\app\core\taliya_commercial\conductor.py services\taliya-agent-runtime\app\core\taliya_commercial\schemas.py services\taliya-agent-runtime\app\core\taliya_commercial\turn_situation.py` = passed.

Review conclusion: this was the correct direction, but this partial checkpoint did not close T011-058B/T011-058C yet. The next checkpoint below closes Phase 5B with adapter integration and long-conversation preflight evidence.

## T011-058B..T011-058F Completion - 2026-06-04

Completed the action-first conductor correction for no-cost Phase 5B:

- `runtime_adapter.py` now prefers `conduct_action_turn -> compile_action_decision -> validate/render/persist` when no legacy test provider is explicitly injected.
- `OpenAIActionConductorProvider` sends the compact action payload/schema to OpenAI for normal production turns instead of asking the model to produce the full route/state/template/render plan.
- Existing legacy `conductor_provider` injection remains supported only for older no-cost fixtures while the rest of the suite migrates.
- `DecisionCompiler` now covers:
  - official price answer plus diagnostic hook;
  - pending diagnostic capture and next question;
  - final urgency capture and staged diagnostic delivery;
  - post-diagnostic demo request;
  - post-diagnostic product/how-it-works follow-up;
  - post-diagnostic price objection;
  - waitlist offer after eligible intent/context.
- Static audit tests prove `TurnSituation` and `DecisionCompiler` do not read raw inbound text, lowercase/casefold lead text, import regex, or carry state/template fields in `ConductorActionDecision`.
- Mode matrix tests prove entry, diagnostic, post-diagnostic, waitlist, and handoff modes produce bounded allowed-action menus.
- A no-cost long-conversation preflight now covers the paid-failure path: pending urgency -> final diagnostic -> demo -> price objection -> post-diagnostic how-it-works -> waitlist offer.

Validation passed with no paid OpenAI spend:

- `python -m pytest services\taliya-agent-runtime\tests\test_spec011_action_mode_matrix.py services\taliya-agent-runtime\tests\test_spec011_action_first_static_audit.py services\taliya-agent-runtime\tests\test_spec011_decision_compiler.py services\taliya-agent-runtime\tests\test_spec011_conductor_boundary.py services\taliya-agent-runtime\tests\test_spec011_turn_situation.py services\taliya-agent-runtime\tests\test_spec011_widget_runtime_adapter.py -q` = 70 passed.
- `python -m ruff check services\taliya-agent-runtime\tests\test_spec011_action_mode_matrix.py services\taliya-agent-runtime\tests\test_spec011_action_first_static_audit.py services\taliya-agent-runtime\app\core\taliya_commercial\runtime_adapter.py services\taliya-agent-runtime\app\core\taliya_commercial\decision_compiler.py services\taliya-agent-runtime\tests\test_spec011_widget_runtime_adapter.py services\taliya-agent-runtime\tests\test_spec011_decision_compiler.py services\taliya-agent-runtime\app\core\taliya_commercial\conductor.py services\taliya-agent-runtime\app\core\taliya_commercial\schemas.py services\taliya-agent-runtime\app\core\taliya_commercial\turn_situation.py` = passed.

Review conclusion: we are back on the original proposal and no longer asking the LLM to assemble the whole monster object for normal turns. The remaining T011-104A closure work is to decide whether action-level repair is mandatory before paid evidence, regenerate readiness/source fingerprint, and only then ask for explicit approval for a capped T011-105 paid rerun.

Next task lock: T011-104A closure/readiness. T011-105 paid rerun remains blocked.

## T011-104A Completion - 2026-06-04

Completed the remaining T011-104A closure work:

- Added a single action-level repair retry in `runtime_adapter.py`. If the first `ConductorActionDecision` is structurally invalid or selects an action outside `TurnSituation.allowed_actions`, the runtime makes one corrected action-conductor call with explicit repair instructions. It does not choose a commercial action deterministically.
- Added no-cost coverage proving invalid action repair retries once and then compiles through the normal validator/render path.
- Regenerated T011-105 readiness on the action-first source fingerprint.
- Ran no-cost T011-105 closure to confirm the only remaining blocker is missing/failed paid evidence.

Validation passed with no paid OpenAI spend:

- `python -m pytest services\taliya-agent-runtime\tests\test_spec011_widget_runtime_adapter.py::test_runtime_adapter_repairs_invalid_action_decision_once services\taliya-agent-runtime\tests\test_spec011_action_mode_matrix.py services\taliya-agent-runtime\tests\test_spec011_action_first_static_audit.py services\taliya-agent-runtime\tests\test_spec011_decision_compiler.py services\taliya-agent-runtime\tests\test_spec011_conductor_boundary.py services\taliya-agent-runtime\tests\test_spec011_turn_situation.py services\taliya-agent-runtime\tests\test_spec011_widget_runtime_adapter.py -q` = 71 passed.
- `python -m ruff check services\taliya-agent-runtime\app\core\taliya_commercial\runtime_adapter.py services\taliya-agent-runtime\tests\test_spec011_widget_runtime_adapter.py` = passed.
- Initial T011-104A readiness passed with source fingerprint `08c269b903cf934e5bf79825c1e5a3d6abb7948236f24d338b161d20ac6b5782`; later action-coverage hardening superseded this with current fingerprint `b6bc712960ac06a93f80eff575a732cfb7e3d86f22cc0e7a6cbfce54fe159c9b`.
- `node scripts\eval-agent-runtime-spec011-t011-105-closure.mjs` = 4/11 passed, expected release gate `fail_missing_or_failed_paid_evidence`.

Review conclusion: the action-first correction is complete enough for the next paid T011-105 attempt. The system is not released; it is only ready to ask for explicit approval for the capped paid evidence run.

Next task lock: T011-105 paid golden/do-not-do evidence. Do not spend OpenAI credits without explicit user approval.

## T011-104A Action Coverage Hardening - 2026-06-04

Added a no-cost action coverage release gate after the first action-first closure. The gate requires every `TurnAction` exposed to the LLM to be explicitly classified as compiled or operationally handled; it no longer allows a silent "pending before release" bucket. This prevents the action menu from growing while the compiler still lacks a validated state/render/projection path.

Implementation changes stayed within the LLM-first boundary:

- `TurnSituation` still derives mode and allowed actions from persisted state/context only, not raw lead text.
- The LLM still selects the commercial action from the bounded menu.
- `DecisionCompiler` now covers entry openings, pain-first diagnostic offer/start, handoff request, diagnostic direct-question continuation, completion/clarification/refusal, product follow-ups, WhatsApp scope, integration scope, plan-fit, price objection, diagnostic offer after answer, and waitlist offer/missing-details/join/decline/continue.
- Operational handoff-active actions remain outside the compiler and are covered by runtime handoff pause/resume/suppression tests.
- Trace output now includes `turn_situation`, `action_decision`, and `action_repair_attempt_count` so eval/debug evidence can show what the LLM chose and what the compiler rendered.

Validation passed with no paid OpenAI spend:

- `python -m pytest services\taliya-agent-runtime\tests\test_spec011_action_coverage_contract.py services\taliya-agent-runtime\tests\test_spec011_decision_compiler.py -q` = 34 passed.
- Focused action trace/repair adapter tests = 2 passed.
- `python -m pytest tests -q` from `services/taliya-agent-runtime` = 713 passed.
- `python -m ruff check ...` over touched action-first files = passed.
- `node scripts\eval-agent-runtime-spec011-t011-105-readiness.mjs` = 13/13 passed, release gate `ready_for_paid_batch`, paid spend US$0, source fingerprint `b6bc712960ac06a93f80eff575a732cfb7e3d86f22cc0e7a6cbfce54fe159c9b`, protected diff empty.
- `node scripts\eval-agent-runtime-spec011-t011-105-closure.mjs` = 4/11, expected `fail_missing_or_failed_paid_evidence`.

Review conclusion: this closes the no-cost gap that could have let the LLM choose an action the compiler could not safely execute. T011-105 is still not complete; the only allowed next step is an explicitly approved capped paid evidence batch on the current fingerprint.

## Paid Pain-First Context Failure - 2026-06-04

The user approved the capped T011-105 paid batch. The runner behaved correctly and stopped after the first paid failure.

- Paid batch fingerprint: `b6bc712960ac06a93f80eff575a732cfb7e3d86f22cc0e7a6cbfce54fe159c9b`.
- Paid spend: US$0.005045.
- Paid commands started: 1.
- Failed scenario: `final-pain-first`.
- Failure: rendered response did not reuse lead context terms `whatsapp` and `interessado`.
- Runtime status: HTTP 200 succeeded; this was a quality/eval failure, not a 500.

Root cause: the action-first LLM selected `offer_diagnostic_from_pain`, but omitted `diagnostic_intent.details.pain_context_human`. The compiler accepted a generic fallback sentence, so validators/repair never got a chance to recover customer-facing context.

Local no-cost fix keeps the agent LLM-first:

- action-conductor instructions now require `pain_context_human` for `offer_diagnostic_from_pain`, grounded in latest inbound and reusing concrete lead terms;
- action-conductor validation rejects `offer_diagnostic_from_pain` without `diagnostic_intent.details.pain_context_human`, triggering the single action-level repair attempt;
- compiler now rejects missing pain context instead of rendering a generic fallback;
- pain-first compiler output includes approved `opening.cold_greeting`, `diagnostic.offer_soft`, and `diagnostic.ask_active_students` from state-derived missing diagnostic keys.

Validation passed with no further paid spend:

- targeted pain-first action/compile/adapter tests = 16 passed;
- action coverage/compiler/conductor/widget focused suite = 68 passed;
- full runtime pytest = 716 passed;
- Ruff over touched action-first files = passed;
- T011-105 readiness = 13/13 `ready_for_paid_batch`;
- T011-105 closure = 2/11 expected `fail_missing_or_failed_paid_evidence`;
- current readiness fingerprint = `e458fcec6bb36bed281b3b7437582554e9b02d89d958d3bb4f216f95b4ef6987`.

Review conclusion: the next paid batch must be freshly approved and rerun on fingerprint `e458fcec6bb36bed281b3b7437582554e9b02d89d958d3bb4f216f95b4ef6987`; previous pain-first paid evidence is stale and failed.

## Non-Negotiables

- One implementation task at a time.
- No `/pilates` layout, styling, copy, animation, section, hierarchy, or visual redesign changes.
- No multi-tenant work.
- No client/studio WhatsApp connection work.
- No checkout/payment work.
- No Sales Inbox UI redesign.
- No new commercial brain inside `services/taliya-agent-runtime/app/runtime/runner.py`.
- No fallback to the old TS v2 public commercial responder.
- No deterministic commercial routing for price, demo, plan-fit, pain-first, diagnostic, waitlist, product questions, source/social openings, or mixed intent.
- Templates are approved language after decision. They are not conversation logic.
- Product facts must come from official product knowledge or Spec 006-derived product contracts, not prompts, templates, fallbacks, or test-only literals.
- Normal commercial turns must require model usage after the conductor exists. Low cost is suspicious if it means the agent stopped thinking.

## Current Task Lock

### T011-104A - Completed Action-First Conductor Correction

Goal: implement the corrected action-first/state-aware conductor contract before any additional paid T011-105 evidence. This task exists because repeated paid long-conversation failures showed the current conductor contract is too broad and the repair layer is absorbing too much structural responsibility.

Expected behavior:

- The core builds `TurnSituation` from persisted state and typed context.
- The LLM receives allowed actions and chooses exactly one action.
- The LLM still interprets all commercial meaning; deterministic code does not map raw text keywords to price, demo, objection, diagnostic, waitlist, handoff, or source actions.
- The compiler derives state/render/projection from the selected action.
- Static audit and tests prove the anti-determinism boundary.
- Long-conversation preflight proves pending urgency, demo after diagnostic, price objection after diagnostic, waitlist intent, and post-diagnostic how-it-works before any paid rerun.

Likely allowed:

- `specs/011-taliya-commercial-agent-core-reset/action-contract.md`
- `services/taliya-agent-runtime/app/core/taliya_commercial/turn_situation.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial/conductor.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial/schemas.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial/decision_compiler.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial/validators.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial/repair.py`
- focused tests and static audit scripts

Forbidden:

- Adding raw-text keyword routing for price, demo, caro, agora, WhatsApp, Instagram, dor, alunos, waitlist, or handoff.
- Replacing LLM commercial interpretation with deterministic slot capture.
- Weakening validators or renderer requirements to make the old full-plan conductor pass.
- Running paid T011-105 before T011-104A is green.

### T011-105 - Current Lock: Run Golden Transcripts And "Do Not Do" Fixtures

Goal: prove versioned golden transcripts and forbidden-behavior fixtures on the Spec 011 production path. T011-105 is broader than unit, mocked, static, and isolated local preflight evidence; it cannot close without real production-path golden/do-not-do proof.

Current continuation, 2026-06-01:

- Latest paid golden long-conversation report `agent-runtime-spec011-golden-long-conversation-16` failed 0/1 at estimated cost US$0.293154.
- The two concrete failures were: final handoff output lost `diagnostic.status=completed`, and the price objection response missed the approved value language.
- Local fixes now preserve completed diagnostic output from persisted context/projection on later product and handoff turns.
- Local fixes also add approved `product.price_objection_value` language through template registry, renderer, validator, repair, and conductor instructions. This remains LLM-first because the LLM still conducts the turn and structured intent/template plan; deterministic code only validates, repairs, and renders approved language.
- Added a no-cost adapter preflight that simulates completed diagnostic -> `achei caro` -> human handoff and verifies the evaluator-sensitive conditions: approved value-language terms, operations terms, handoff request, and completed diagnostic ledger in the final output.
- No-cost validation passed: targeted preflight 1/1, expanded local pytest 186/186, Ruff over touched core/test files, mocked conductor gate 6/6, `node --check` for golden/do-not-do and coverage gate scripts, and protected `/pilates`/landing/floating-agent/Sales Inbox UI source diff empty.
- No OpenAI spend was made in this continuation.
- Follow-up no-cost aggregation previously showed golden evidence at 7/8. The fixture inventory then exposed that a dedicated pain-first golden was missing from T011-019.
- Added `final-pain-first` to the versioned golden suite and added RC-011-053A for the pure pain-first opening. Existing paid evidence now fails this stronger golden because customer-facing `answer_feedback` leaked English translation text (`lead loses`, `interested leads`, `team takes too long`).
- Local validator/repair fixes now flag `diagnostic_feedback_language_leak` and repair the feedback from the lead's own evidence. This stays LLM-first because it validates and repairs a renderable variable after the structured decision, not a commercial route from raw user text.
- Current golden evidence is 7/9. The remaining golden gaps are `final-pain-first` and `step3g-long-conversation`.
- Follow-up no-cost aggregation showed current do-not-do evidence is 4/8 passing. The remaining gaps are missing real-model evidence for early phone capture, invented date/VIP/discount, client/studio WhatsApp capture, and wrong student/client language.
- Initial dry-run budget planning recorded the missing pain-first golden as 1 estimated model call under US$0.03, the long conversation rerun as 14 estimated model calls under US$0.30, and the missing do-not-do subset as 4 estimated model calls under US$0.08. After later context/provider-input optimizations, the current paid batch cap is US$0.36 / 19 model calls, with the long-conversation cap reduced to US$0.25.
- Added a no-cost T011-105 preflight in `test_spec011_mocked_conductor_fixtures.py` for the four do-not-do gaps. It uses mocked structured conductor JSON, not deterministic user-text routing, and verifies model usage, passed validators, rendered template ids, Sales Inbox projection, WhatsApp <=3 chunks where applicable, required approved text, and absence of forbidden phrases.
- Hardened `eval-agent-runtime-spec011-golden-do-not-do.mjs` so a scenario can have multiple candidate evidence reports. The gate now evaluates all passing runtime candidates against fixture expectations and selects a fixture-satisfying candidate, while recording rejected evidence. This prevents report-order artifacts from hiding the fixed `final-demo-request` evidence or creating a false extra failure.
- Added `eval-agent-runtime-spec011-fixture-inventory.mjs`, a no-cost fixture inventory gate. It passed 8/8 and proves the versioned golden suite covers price, price-plus-pain, pain-first, Instagram/source, WhatsApp product, diagnostic/long conversation, waitlist, human handoff, and product demo; it also proves the do-not-do suite covers all required forbidden-behavior categories and that fixture case IDs map to unique regression-case IDs.
- Added `eval-agent-runtime-spec011-t011-105-readiness.mjs`, a no-cost pre-paid readiness gate. It reruns the fixture inventory, T011-105 paid-batch safety audit, local preflights, mocked conductor gate, existing-evidence golden/do-not-do aggregations, budget dry-runs, paid-runner refusal checks, and protected source diff. The report `agent-runtime-spec011-t011-105-readiness` passed 10/10 with `ready_for_paid_batch` and confirms the only remaining T011-105 blocker is approved paid evidence, not local readiness.
- Added `eval-agent-runtime-spec011-t011-105-paid-batch.mjs`, a paid-runner safety wrapper that requires an exact approval token and approved budget as explicit command-line arguments before any paid OpenAI eval can start. It reruns readiness first, stops after any paid failure, and aggregates golden/do-not-do evidence only from the capped reports. Validated refusal paths: no token, wrong budget, env-var-only approval, and `--continue-on-failure` all exit before paid commands. The current post-optimization approval token/budget is `--approval-token T011-105-US0.36 --approved-budget-usd 0.36`.
- The first approved T011-105 paid batch ran and stopped safely after the first paid failure. `final-pain-first` passed 1/1 at estimated cost US$0.015606. `step3g-long-conversation` failed 0/1 at estimated cost US$0.255610 because later product/handoff turns exposed stale `missing` diagnostic ledger entries after the diagnostic had already completed. The four missing do-not-do scenarios were not run because the batch runner intentionally stops on first paid failure.
- Fixed the local cause without adding deterministic commercial routing: diagnostic ledgers are now canonicalized as current state by `question_key`, stale weaker statuses do not overwrite answered/inferred values, context/output can recover from already-dirty persisted ledgers, and subsequent turns clean dirty persisted ledgers.
- Fixed `eval-agent-runtime-spec011-t011-105-paid-batch.mjs` cost accounting so a paid command that fails but writes a fresh report still contributes its scenario cost. The reconciled paid batch report now records US$0.271216 from the fresh pain-first and failed long-conversation reports, still under the US$0.41 approved cap.
- Latest no-cost validation after local hardening: targeted pytest 30/30 for ledger/context/adapter, focused failing-contract suite 28/28, full `test_spec011_*.py` sweep 404/404, Ruff over touched core/test files, paid-batch script syntax check, unit/contract gate 7/7, T011-105 safety audit 11/11, mocked conductor gate 6/6, active-path static audit 8/8, focused T011-105 preflight 5/5, T011-105 readiness 12/12 with `ready_for_paid_batch`, protected source diff empty, and T011-105 closure 4/11 with `fail_missing_or_failed_paid_evidence`.
- Local contract hardening from the broad sweep: missing/partial `policy_checks` now remain a conductor-boundary error instead of being silently normalized to false; `product.plan_fit_with_diagnostic`, `product.comparison_current_tool`, and `product.integration_scope_direct` require grounded variables before rendering; and validator acceptance fixtures now reflect the current stronger contracts for price answers and completed diagnostic delivery.
- Added source fingerprinting for T011-105 evidence. Readiness records a SHA-256 fingerprint over the current Spec 011 core/runtime/eval/fixture sources and the no-cost gate scripts that prove readiness, the paid runner refuses to start if the readiness fingerprint does not match the current code, checks the same fingerprint after readiness and between paid phases before continuing, and the closure gate requires readiness and paid-batch evidence to match the current source fingerprint. The fingerprint now covers 46 files, including the fingerprint helper itself, `eval-agent-runtime-spec011-unit-contract.mjs`, `eval-agent-runtime-spec011-t011-105-safety-audit.mjs`, fixture inventory, mocked conductor, static audit, rollback, quarantine, and widget-adapter gates. This prevents closing T011-105 with paid reports generated for a different local code or gate state, and prevents spending the next paid phase after source/gate drift is detected mid-batch.
- Added `eval-agent-runtime-spec011-t011-105-closure.mjs`, a no-cost post-paid closure gate. It cannot pass from readiness alone; it requires the paid batch report, the new paid pain-first report, the new paid long-conversation report, the new four-case do-not-do report, golden 9/9 aggregation, do-not-do 8/8 aggregation, exact budget/token evidence, fresh report timestamps relative to the approved batch start, paid batch cost equal to the sum of fresh scenario report costs, source-fingerprint match, and empty protected source diff. Current report `agent-runtime-spec011-t011-105-closure` correctly fails 4/11 because the paid batch stopped after the long-conversation failure and fresh passing long/do-not-do/aggregation evidence does not exist yet.
- Added a no-cost runtime context optimization before the next paid T011-105 attempt. `run_spec011_agent_turn` now uses a `RuntimeContextProfile` that keeps the LLM as the commercial brain while reducing prompt input by selecting only the official product/Spec 006 source refs needed for the current turn. The selector returns source keys and transcript budget only; it does not return route, intent, template, copy, or state decisions. Generic diagnostic context keeps core product facts and `spec006.product_positioning`/`spec006.plan_entitlements`; extra comparison, security, commercial-policy, setup/access, operating-mode, and out-of-profile refs are retrieved only as additional official source material.
- No-cost budget proxy for the optimized runtime context: default context JSON was 38,724 chars / 26 refs; runtime context is 16,249 chars / 16 refs, a 58.0% context reduction, with the diagnostic ledger, compact memory, and Sales Inbox inputs preserved. This is not a paid-cost claim yet; the next real OpenAI evidence must prove the actual token/cost reduction.
- Latest no-cost validation after the context optimization: focused context/runtime pytest 25/25, mocked conductor gate 6/6, active-path static audit 8/8, T011-105 readiness 12/12 with `ready_for_paid_batch`, protected source diff empty, and readiness source fingerprint `69f8a88fe93ab272c274d0b9fa98527cdc719ba5f13bd9703c84014430042627` over 47 files.
- Second approved paid batch after the optimization spent US$0.210999 in reported estimated runtime cost and stopped after golden aggregation failure. Fresh `final-pain-first` passed individually at US$0.013065, and fresh `step3g-long-conversation` passed individually at US$0.197934 for 14 turns. The long-conversation lead cost is now 22.56% lower than the previous US$0.255610 run. Aggregation still failed because `final-pain-first` asked `diagnostic.ask_urgency` before `diagnostic.ask_active_students`, so the four do-not-do paid scenarios were not run.
- Local no-cost fix after that paid batch: validator/repair now blocks a pain-first `diagnostic.offer_soft` turn from asking another diagnostic question before `active_students_or_size`; repair preserves the approved offer copy and asks `diagnostic.ask_active_students`. Validation passed: focused diagnostic/repair/widget/context pytest 87/87, Ruff over touched files, mocked conductor gate 6/6, static audit 8/8, and T011-105 readiness 12/12 with current source fingerprint `2c5c65934e2c00059c9b5923a773f4ad8f815828991b1da148571c0996a3a5b2`. Closure remains red 5/11 until fresh paid evidence is rerun on this fingerprint.
- Second no-cost cost optimization before any further paid evidence: OpenAI provider input now uses compact JSON separators, keeps static `specialist_policy`/requirements before dynamic context, sends product/Spec006 refs to the model as compact source refs with `excerpt`/`evidence` and no full `value`, preserves full ref values in the local `TurnContext` for validators/repair/renderer, and compresses the template/variable catalog into a schema-preserving array format that keeps required/optional variables, kind, allowed sources, max length, and validation rules. Product plan excerpts were tightened so the model still sees all configured plan names/prices, including `Completo` / `R$ 1.497/mes`, after full `value` removal. No paid calls were made. Validation passed: focused conductor/product/context pytest 31/31, full Spec 011 pytest sweep 415/415, Ruff over touched files, mocked conductor gate 6/6, static audit 8/8, T011-105 readiness 12/12, protected source diff empty, and closure remains red 5/11 as expected. No-cost representative proxy: provider input 24,986 -> 18,617 chars (-25.49%), model context 17,404 -> 11,806 chars (-32.17%), combined request proxy ~50.5k -> ~41.7k chars (-17.3%). Follow-up no-cost cap hardening lowered the next paid-batch approval ceiling from US$0.41 to US$0.36 and the long-conversation cap from US$0.30 to US$0.25 without removing scenarios or model-call coverage. Current readiness fingerprint is `26aca5379ed81145988952338c6e0153e405b76aa2f07b17f990995914fc4de9`.
- Third conservative no-cost optimization before any further paid evidence: model-facing OpenAI schema now keeps the root `ConductorDecision` title but strips repeated nested `title` fields; model-facing product refs omit source versions and false `missing` flags while preserving key, source, evidence, and excerpts; and duplicated `specialist_policy.global_rules` are replaced in the model input by `global_rules_ref` because the same rules remain in the conductor instructions. The full specialist policy and full product refs still exist in the local provider request/context for validators, repair, renderer, trace, and source reporting. No paid calls were made. Validation passed: focused conductor/product/context pytest 31/31, full Spec 011 pytest sweep 415/415, Ruff over touched files, mocked conductor gate 6/6, static audit 8/8, T011-105 safety audit 11/11, T011-105 readiness 12/12, protected source diff empty, and closure remains red 5/11 as expected. No-cost representative proxy: provider input 18,617 -> 15,487 chars (-16.81% vs the second optimization), model context 11,806 -> 9,874 chars (-16.36%), response schema 9,225 -> 7,341 chars (-20.73%), combined request proxy ~41.7k -> ~36.7k chars (-12.02%). The approval ceiling remains US$0.36 until fresh paid evidence proves the new exact scenario cost. Current readiness fingerprint is `133bbcb45feecbede9225bc9a672530bc935fb552c27e2187710c60b0083e8e9`.
- Approved T011-105 paid batch on fingerprint `133bbcb45feecbede9225bc9a672530bc935fb552c27e2187710c60b0083e8e9` stopped after `final-pain-first` returned HTTP 500. The batch started 1 paid scenario and reported estimated runtime cost US$0.00 because no model usage was recorded in the failed response. The failure exposed that the model could emit the response schema name as `schema_version=011.conductor_decision.v1`; validators correctly rejected it, but deterministic repair did not normalize that known alias before applying the existing pain-first active-students/greeting repair. Local no-cost fix: response schema now pins `schema_version` to `011.0`, and repair normalizes only the known alias `011.conductor_decision.v1` to the current version before continuing through validators; unknown or silent versions remain rejected by schema-versioning tests. Validation passed: focused conductor/repair/schema-versioning pytest 83/83, full Spec 011 pytest sweep 415/415, Ruff over touched files, mocked conductor gate 6/6, static audit 8/8, T011-105 safety audit 11/11, T011-105 readiness 12/12, protected source diff empty, and closure remains red 3/11 as expected because fresh paid evidence does not exist on the new fingerprint. Current readiness fingerprint is `ba682023809d82e0a730969494b3e134ba85bad774956e9f7ccfb7004e2ee863`.
- Approved T011-105 paid batch on fingerprint `ba682023809d82e0a730969494b3e134ba85bad774956e9f7ccfb7004e2ee863` stopped after `final-pain-first` returned `decision.route=product` for a first-turn pain-first diagnostic offer. The batch started 1 paid scenario and reported exact estimated cost US$0.00956. Local no-cost fix: validators now reject first-turn pain-first diagnostic offers that are misrouted as product without a direct product question and require `diagnostic.ask_active_students`; structural repair converts the LLM decision to the diagnostic route, preserves the approved pain offer, and asks active students. T011-105 readiness now includes a fake-provider adapter reproduction of this exact failure, so the next paid attempt cannot start unless this local guard is green. Validation passed: focused validator/adapter/repair pytest 86/86, full Spec 011 pytest sweep 418/418, Ruff over touched Python files, `node --check` for readiness, unit/contract gate 7/7, protected source diff empty, T011-105 readiness 12/12, and closure 3/11 with expected `fail_missing_or_failed_paid_evidence`. Current readiness fingerprint is `79f9cd80f744b1601d372da2338476c4091e7fed82ae10a05d67cfe7cf73c687`.
- Approved T011-105 paid batch on fingerprint `79f9cd80f744b1601d372da2338476c4091e7fed82ae10a05d67cfe7cf73c687` passed `final-pain-first` 1/1 at US$0.010208, then failed `step3g-long-conversation` 0/1 at US$0.141368 with HTTP 500 on turn 11 (`achei caro`). Exact batch cost was US$0.151576. The failure exposed a stale demo/diagnostic-follow-up repair gap: the real model reused `product.demo_direct` and completed-diagnostic delivery state when the current inbound was a value objection, validators correctly blocked it (`diagnostic_final_demo_stage_missing`, `diagnostic_final_staged_order_invalid`, `stale_demo_direct_without_current_request`, `demo_direct_question_flags_missing`), but repair fell through to failure/final-diagnostic redelivery instead of producing the approved value-objection answer.
- Local no-cost fix after that paid batch: stale completed-diagnostic demo follow-up repair now wins over generic completed-diagnostic redelivery, treats demo as current only when the inbound actually asks for demo, removes stale `product.demo_direct`, drops partial `diagnostic.deliver_*` items on product follow-up, and repairs explicit value objections to `product.price_direct` + `product.price_objection_value` with official price sourcing. This is a narrow post-LLM validator/repair guard after an invalid structured decision; it does not pre-route normal commercial turns or replace the conductor.
- Validation after the stale-demo/value-objection fix passed: focused repair pytest 4/4, focused repair/adapter regression pytest 8/8, Ruff over touched files, unit/contract gate 7/7, T011-105 readiness 12/12 with `ready_for_paid_batch`, protected source diff empty, and closure 4/11 with expected `fail_missing_or_failed_paid_evidence`. Closure now also proves the previous paid batch fingerprint `79f9cd80f744b1601d372da2338476c4091e7fed82ae10a05d67cfe7cf73c687` is stale against current fingerprint `f8aa524d898d7d192402ba6e609714b2666225f37f96f963e4c49c25fd82cb8d`, so fresh paid evidence is required before T011-105 can close.
- Approved T011-105 paid batch on fingerprint `f8aa524d898d7d192402ba6e609714b2666225f37f96f963e4c49c25fd82cb8d` passed `final-pain-first` 1/1 at US$0.009933, then failed `step3g-long-conversation` 0/1 at US$0.113069. Exact batch cost was US$0.123002. The failure exposed two operational guardrail gaps: the real model returned invalid diagnostic `next_question_key` JSON with invalid `answer_feedback` source on the pending urgency answer (`quero resolver agora`), and a later human handoff exposed Sales Inbox `diagnostic_status` mismatch.
- Local no-cost fix after that paid batch: `diagnostic_next_question_invalid` is now LLM-repairable under the existing one-call repair cap, with repair instructions to choose a mandatory diagnostic key or complete the diagnostic when the current inbound answers the final pending field. Context builder, Sales Inbox projection, and Sales Inbox validation now derive diagnostic status from the canonical diagnostic ledger when persisted status is stale, and runtime-state diff ignores a stray `next_question_key` when `diagnostic.action=none` so neutral product/handoff turns cannot reset diagnostic state. These changes are state/validation/projection hardening after structured model output; they do not add raw-message commercial routing, template-first decisions, or regex shortcuts.
- Validation after the invalid-next-question/Sales-Inbox-status fix passed: targeted regressions 4/4, focused repair/context/runtime-state/Sales Inbox suite 95/95, adapter long preflight/handoff regressions 2/2, full Spec 011 pytest sweep 423/423, mocked conductor gate 6/6, T011-105 safety audit 11/11, active-path static audit 8/8, Ruff over touched files, unit/contract gate 7/7, T011-105 readiness 12/12 with `ready_for_paid_batch`, `/pilates`/floating-agent/Sales Inbox UI protected source diff empty, and closure 4/11 with expected `fail_missing_or_failed_paid_evidence`. Closure now proves the previous paid batch fingerprint `f8aa524d898d7d192402ba6e609714b2666225f37f96f963e4c49c25fd82cb8d` is stale against current fingerprint `6ab09be27860075c621a3cc316d388ee770f5eb655fe9e0518bebd64ea3b6a83`, so fresh paid evidence is required before T011-105 can close. `services/taliya-agent-runtime/app/runtime/runner.py` remains dirty from an existing one-line diff and was not edited in this continuation.
- Approved T011-105 paid batch on fingerprint `6ab09be27860075c621a3cc316d388ee770f5eb655fe9e0518bebd64ea3b6a83` passed `final-pain-first` 1/1, then failed `step3g-long-conversation` 0/1 with HTTP 500 on turn 9 (`quero resolver agora`). Exact batch cost was US$0.134766. The failure exposed a narrower repair-boundary gap: validators correctly blocked `diagnostic_urgency_answer_not_captured` when the current inbound answered the final pending urgency question, but the blocked-result repair allowlist did not let that validator code reach the one-call LLM repair path.
- Local no-cost fix after that paid batch: `diagnostic_urgency_answer_not_captured` is now LLM-repairable under the existing one-call repair cap, and repair instructions require capturing the current inbound as the urgency answer with `user_message` evidence and completing the diagnostic when urgency is the final pending mandatory field. This remains post-LLM validation/repair hardening; it does not pre-classify urgency from raw lead text for normal turns.
- Validation after the pending-urgency capture fix passed: exact repair regression 2/2, focused repair/diagnostic/long-adapter suite 75/75, Ruff over touched files, mocked conductor gate 6/6, active-path static audit 8/8, `/pilates`/floating-agent/Sales Inbox UI protected source diff empty, T011-105 readiness 12/12 with `ready_for_paid_batch`, and closure 4/11 with expected `fail_missing_or_failed_paid_evidence`. Closure now proves the paid batch fingerprint `6ab09be27860075c621a3cc316d388ee770f5eb655fe9e0518bebd64ea3b6a83` is stale against current fingerprint `213490a61b217e3657b414447a42624a0fa1a14de5fd6c9f86bdca619c1033f5`, so fresh paid evidence is required before T011-105 can close.
- Approved T011-105 paid batch on fingerprint `213490a61b217e3657b414447a42624a0fa1a14de5fd6c9f86bdca619c1033f5` stopped after `final-pain-first` failed 0/1 with HTTP 500 before model usage was recorded. Exact reported batch cost was US$0. The failure exposed that structural pain-first repair produced the approved diagnostic offer but omitted the mandatory first diagnostic question, leaving `pain_first_must_offer_diagnostic` unrepaired.
- Local no-cost fix after that paid batch: structural pain-first repair now sets `diagnostic.next_question_key=active_students_or_size` and renders `opening.cold_greeting`, `diagnostic.offer_soft`, and `diagnostic.ask_active_students` together. This is still a validator/repair guard after invalid structured model output; normal pain-first understanding remains LLM-first.
- Validation after the pain-first first-question fix passed: exact pain-first repair regression and related pain-first adapter/repair tests 3/3, focused repair + pain-first/long-adapter suite 62/62, Ruff over touched files, mocked conductor gate 6/6, active-path static audit 8/8, `/pilates`/floating-agent/Sales Inbox UI protected source diff empty, T011-105 readiness 12/12 with `ready_for_paid_batch`, and closure 2/11 with expected `fail_missing_or_failed_paid_evidence`. Closure now proves the paid batch fingerprint `213490a61b217e3657b414447a42624a0fa1a14de5fd6c9f86bdca619c1033f5` is stale against current fingerprint `02afedc6c47ef7cf836623f7152154bc65881bd4e483bdfa8df7949923d4941b`, so fresh paid evidence is required before T011-105 can close.
- Added a no-cost known-validator recovery gate before any further paid rerun. `agent-runtime-spec011-known-validator-recovery` proves 6/6 recovery paths with US$0 spend for the known recent validator failures: pain-first offer missing first question, schema alias plus diagnostic start question, pain-first product-route misroute, pending urgency capture, invalid diagnostic next question, stale demo/current request, and Sales Inbox diagnostic-status mismatch. Readiness now requires this gate and passed 13/13 on fingerprint `4749feb1c718f59c906a8e44c8c76a6d651f8a528c1f112a559433ab04b627ba`; full Spec 011 pytest passed 425/425; active-path static audit passed 8/8; T011-105 safety audit passed 12/12; closure remains red 2/11 only because fresh paid evidence on the current fingerprint does not exist.
- Approved T011-105 paid batch on fingerprint `4749feb1c718f59c906a8e44c8c76a6d651f8a528c1f112a559433ab04b627ba` spent US$0.126241, passed `final-pain-first` at US$0.009578, and failed `step3g-long-conversation` at US$0.116663 with HTTP 500 on turn 9 (`quero resolver agora`) and turn 10 (`me manda demo`). The failure exposed two post-LLM repair-boundary gaps: a final urgency answer could leave stale `diagnostic.next_question_key=urgency` while trying to deliver the final diagnostic, and a current direct demo request could keep a stale price intent and trigger price validators.
- Local no-cost fix after that paid batch: final-diagnostic structural repair now completes the diagnostic, clears stale `next_question_key`, and renders the approved staged final diagnostic sequence when all mandatory answers are complete; current demo direct structural repair removes stale price intents only when the LLM already selected `product.demo_direct` for a current demo request. The known-validator recovery gate now covers 9/9 cases and 15 validator codes, including the two new paid failures, with one adapter-level sequential preflight that reproduces the latest paid turn-9/turn-10 failure through persisted state. Validation passed: exact new repair regressions 2/2, focused repair/adapter suite 77/77, Ruff passed, known-validator recovery 9/9, full Spec 011 pytest sweep 428/428, active-path static audit 8/8, T011-105 safety audit 12/12, T011-105 readiness 13/13 on fingerprint `b818ed2356dcc3f52456cabdae2c95de740d30186fe935f1a10ec63ffcc8e9d8`, protected source diff empty, and closure 4/11 with expected `fail_missing_or_failed_paid_evidence`.

Expected behavior:

- Run golden/do-not-do evidence against `/v1/taliya-commercial/turn`, not legacy `/v1/agent-runs` or `runtime/runner.py`.
- Real-model golden reports must include transcript/input, channel/source metadata, structured decision JSON, validator/repair result, rendered messages, model usage/cost, runtime-state diff, Sales Inbox projection where applicable, delivery evidence, and pass/fail reason.
- Do-not-do aggregation must compare passing report evidence against `scripts/fixtures/agent-runtime/spec-011-golden-transcripts.json` and `scripts/fixtures/agent-runtime/spec-011-do-not-do-runtime.json` as applicable.
- A local/mock preflight is only a budget guard. It is not T011-105 closure evidence.
- If the next paid rerun fails, fix the concrete cause locally and stop before any second paid rerun unless the user explicitly approves more spend.
- Do not weaken validators, trace/projection requirements, pass criteria, or report assertions to make a weak transcript pass.
- Do not mark T011-105 complete unless `node scripts\eval-agent-runtime-spec011-t011-105-closure.mjs` passes after the approved paid batch.

Likely allowed:

- `specs/011-taliya-commercial-agent-core-reset/action-contract.md`
- `services/taliya-agent-runtime/app/core/taliya_commercial/turn_situation.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial/decision_compiler.py`
- action-first conductor/schema/static-audit/test changes needed for T011-104A
- `scripts/fixtures/agent-runtime/spec-011-golden-transcripts.json`
- `scripts/fixtures/agent-runtime/spec-011-do-not-do-runtime.json`
- `scripts/eval-agent-runtime-spec011.py`
- `scripts/eval-agent-runtime-spec011-golden-do-not-do.mjs`
- narrowly scoped conductor/policy/schema/validator/repair/template/renderer/core fixes for action-first T011-104A and proven T011-105 failures
- eval reports under `specs/011-taliya-commercial-agent-core-reset/eval-reports/`
- `specs/011-taliya-commercial-agent-core-reset/tasks.md`
- `specs/011-taliya-commercial-agent-core-reset/coverage-map.md`
- this ledger

Forbidden:

- `/pilates`, `components/landing`, `data/landing`, `lib/landing/floating-agent.ts`, and `components/internal/SalesInboxClient.tsx` unless only read for protected-diff verification.
- `services/taliya-agent-runtime/app/runtime/runner.py`
- old TypeScript commercial fallback modules as public responders or rollback targets
- customer/studio WhatsApp adapter files or account-connection code
- deterministic commercial routing from user text for price, demo, plan-fit, pain-first, diagnostic, waitlist, product questions, source/social openings, or mixed intent

Next allowed action:

- Implement T011-104A with no paid OpenAI spend: `TurnSituation`, smaller `ConductorActionDecision`, `DecisionCompiler`, action-level repair, static anti-determinism audit, and long-conversation action preflight.
- After T011-104A passes, regenerate readiness on the new fingerprint. Only then may the user be asked to approve another capped T011-105 paid batch.

## Stop Rules

Stop before editing if any of these become true:

- A proposed change needs `/pilates` visual/layout/copy movement.
- A proposed change adds `if`, regex, token lists, or templates as the primary decider for commercial meaning.
- A proposed change puts product facts into prompts/templates/fallbacks instead of official sources.
- A proposed change makes `runner.py` smarter commercially instead of quarantining it later.
- A normal commercial turn can pass without structured decision JSON once Phase 5 begins.
- A validator failure would be handled by deterministic commercial copy instead of repair or safe fallback/handoff.
- A manual validation is vague and cannot be replayed from inputs, state, expected result, and observed output.
- A phase is marked complete without updating `coverage-map.md` and this ledger.
- A green eval only proves string matching while the transcript is commercially bad.

## Phase Gates

| Phase | Gate |
| --- | --- |
| Phase 4 | Cannot finish until T011-041..T011-045 have tests, evidence rows, and at least one concrete context snapshot report. |
| Phase 5 | Cannot start until context includes memory, official product facts, Spec 006 summaries, internal/non-renderable labels, reliability labels, and snapshot persistence. |
| Phase 6 | Cannot start until conductor output is strict JSON, model usage is logged, and mocked conductor fixtures exist. |
| Phase 7 | Cannot start until validators can reject unsafe or incomplete template plans. |
| Phase 8 | Cannot finish until trace and Sales Inbox projection are generated from validated state/events. |
| Phase 9 | Cannot start until behavior gates pass outside public traffic. |
| Phase 10 | Cannot pass until static, unit, mocked, real-model, golden, do-not-do, trace, projection, manual review, rollback, and approval evidence all exist. |

Production note: the user approved eventual full production cutover instead of a canary because the current production behavior is bad. That does not remove the Phase 9/10 proof requirements. It means the cutover can be 100% only after rollback, monitoring, and manual approval are proven.

## Required Closure Checklist For Every Task

Before marking any task done:

- State the exact task id closed.
- Confirm the implementation stayed inside the allowed scope.
- Link the regression or requirement rows covered.
- Run the focused tests.
- Run the nearest relevant suite.
- Run static audit or a targeted static review when LLM-first risk exists.
- Add or update a manual/eval report when behavior cannot be proven by unit tests alone.
- Update `coverage-map.md` with evidence.
- Update this ledger with the new last completed task and next task lock.
- Explain whether the proof is isolated-core, adapter-level, or production-path proof.

## Last Known Validation

After T011-103:

```powershell
python -m pytest services\taliya-agent-runtime\tests\test_spec011_conductor_boundary.py services\taliya-agent-runtime\tests\test_spec011_repair_loop.py services\taliya-agent-runtime\tests\test_spec011_validators_diagnostic.py services\taliya-agent-runtime\tests\test_spec011_validators_core.py -q
python -m ruff check services\taliya-agent-runtime\app\core\taliya_commercial\conductor.py services\taliya-agent-runtime\app\core\taliya_commercial\repair.py services\taliya-agent-runtime\app\core\taliya_commercial\validators.py services\taliya-agent-runtime\tests\test_spec011_conductor_boundary.py services\taliya-agent-runtime\tests\test_spec011_repair_loop.py
node scripts\eval-agent-runtime-spec011-p0-real-model-gate.mjs
git -c safe.directory=C:/Users/lucas/agentes-landing-system diff --name-only -- app/pilates components/landing data/landing lib/landing/floating-agent.ts components/internal/SalesInboxClient.tsx
```

Results:

- Focused conductor/repair/validator suite: 63 passed.
- Focused Ruff check: passed.
- P0 real-model gate wrapper: 8/8 passed.
- Real OpenAI P0 report: 9/9 passed, release gate `pass`, estimated cost US$0.159867.
- Mandatory report contract over the green P0 report: 41/41 passed.
- RC-011-010/011 delivery duplicate/interleaving gate: 7/7 passed.
- Protected source diff command returned no files.

Static review result:

- No source diff in `app/pilates`, `components/landing`, `data/landing`, `lib/landing/floating-agent.ts`, or `components/internal/SalesInboxClient.tsx`.
- T011-103 fixed only proven P0 real-model failures with structural LLM-first guardrails: provider JSON normalization for registered variables and misplaced decision fields, price-hook/feedback repair, diagnostic retarget repair, urgency evidence validation, final diagnostic staged repair, and WhatsApp staged coalescing.
- The full P0 gate had earlier red reruns that exposed real stochastic/model-output failures; those failures were fixed and the final gate reran green 8/8.
- T011-103 is P0 observed-bug real-model proof, not full real-model/golden/manual/final production approval.
- No `/pilates` layout, copy, animation, section, or visual component file was edited.
- No Sales Inbox UI or `floating-agent` source was edited.
- No `runtime/runner.py` edit was made for T011-103; an existing unrelated dirty diff remains in the worktree and is not part of this closure.

Manual report:

- T011-103 runtime/core changes:
  - `services/taliya-agent-runtime/app/core/taliya_commercial/conductor.py`
  - `services/taliya-agent-runtime/app/core/taliya_commercial/repair.py`
  - `services/taliya-agent-runtime/app/core/taliya_commercial/validators.py`
  - `services/taliya-agent-runtime/app/core/taliya_commercial/renderer.py`
- T011-103 tests and harnesses:
  - `services/taliya-agent-runtime/tests/test_spec011_conductor_boundary.py`
  - `services/taliya-agent-runtime/tests/test_spec011_repair_loop.py`
  - `services/taliya-agent-runtime/tests/test_spec011_renderer_channel_rules.py`
  - `services/taliya-agent-runtime/tests/test_spec011_renderer_final_diagnostic.py`
  - `scripts/eval-agent-runtime-real-openai.py`
  - `scripts/eval-agent-runtime-spec011-p0-real-model-gate.mjs`
  - `scripts/eval-agent-runtime-spec011-report-contract.mjs`
  - `scripts/eval-agent-runtime-spec011-delivery-turn-gate.mjs`
  - `scripts/fixtures/agent-runtime/spec-011-real-openai-p0.json`
- T011-103 generated reports:
  - `specs/011-taliya-commercial-agent-core-reset/eval-reports/agent-runtime-spec011-p0-real-model-gate.json`
  - `specs/011-taliya-commercial-agent-core-reset/eval-reports/agent-runtime-spec011-p0-real-model-gate.md`
  - `specs/011-taliya-commercial-agent-core-reset/eval-reports/agent-runtime-spec011-p0-real-model.json`
  - `specs/011-taliya-commercial-agent-core-reset/eval-reports/agent-runtime-spec011-p0-real-model.md`
  - `specs/011-taliya-commercial-agent-core-reset/eval-reports/agent-runtime-spec011-report-contract.json`
  - `specs/011-taliya-commercial-agent-core-reset/eval-reports/agent-runtime-spec011-delivery-turn-gate.json`
- T011-103 closure docs:
  - `specs/011-taliya-commercial-agent-core-reset/tasks.md`
  - `specs/011-taliya-commercial-agent-core-reset/coverage-map.md`
  - `specs/011-taliya-commercial-agent-core-reset/implementation-ledger.md`

## Last Known Validation After T011-104

T011-104 is closed. The next task lock is T011-105 only: golden transcripts and "do not do" fixtures.

Scope confirmation:

- No `/pilates` layout/copy/visual file was edited.
- No Sales Inbox UI, `lib/landing/floating-agent.ts`, multi-tenant, client/studio WhatsApp, checkout, old TypeScript fallback responder, or `runtime/runner.py` source was edited.
- Commercial understanding stayed LLM-first. The new deterministic logic is validator/repair only, keyed from structured LLM decision intents, not from user-text regex as a conversation brain.

Fixes made during T011-104 real-model closure:

- Direct integration/current-system questions must use `product.integration_scope_direct` before any human confirmation/handoff.
- Diagnostic refusal must be respected: when the LLM marks `diagnostic_refusal`, validators reject diagnostic hooks/offers in that same turn and repair removes the diagnostic offer while preserving the direct price answer.
- Added a budget-safe coverage gate so partial real OpenAI reports can be combined by scenario id without rerunning already-green scenarios.

Validation run:

```powershell
python -m pytest services\taliya-agent-runtime\tests\test_spec011_validators_core.py services\taliya-agent-runtime\tests\test_spec011_validators_product_claims.py services\taliya-agent-runtime\tests\test_spec011_repair_loop.py -q
python -m ruff check services\taliya-agent-runtime\app\core\taliya_commercial\validators.py services\taliya-agent-runtime\app\core\taliya_commercial\repair.py services\taliya-agent-runtime\app\core\taliya_commercial\conductor.py services\taliya-agent-runtime\app\core\taliya_commercial\conductor_policy.py services\taliya-agent-runtime\tests\test_spec011_validators_core.py services\taliya-agent-runtime\tests\test_spec011_validators_product_claims.py services\taliya-agent-runtime\tests\test_spec011_repair_loop.py
python -m pytest services\taliya-agent-runtime\tests\test_runtime_behavior_regressions.py -k "diagnostic_refusal or integration_scope or product_followup or how_it_works" -q
node scripts\eval-agent-runtime-spec011-static-audit.mjs
node scripts\eval-agent-runtime-spec011-report-contract.mjs specs\011-taliya-commercial-agent-core-reset\eval-reports\agent-runtime-spec011-full-required-product-delta-integration-fixed-1.json
node scripts\eval-agent-runtime-spec011-report-contract.mjs specs\011-taliya-commercial-agent-core-reset\eval-reports\agent-runtime-spec011-full-required-product-delta-diagnostic-refusal-fixed-1.json
node scripts\eval-agent-runtime-spec011-coverage-gate.mjs --fixture scripts\fixtures\agent-runtime\product-followup-delta-real-openai.json --report specs\011-taliya-commercial-agent-core-reset\eval-reports\agent-runtime-spec011-full-required-product-delta-budgeted-1.json --report specs\011-taliya-commercial-agent-core-reset\eval-reports\agent-runtime-spec011-full-required-product-delta-integration-fixed-1.json --report specs\011-taliya-commercial-agent-core-reset\eval-reports\agent-runtime-spec011-full-required-product-delta-remaining-budgeted-1.json --report specs\011-taliya-commercial-agent-core-reset\eval-reports\agent-runtime-spec011-full-required-product-delta-diagnostic-refusal-fixed-1.json --name agent-runtime-spec011-full-required-product-delta-coverage-1
node scripts\eval-agent-runtime-spec011-coverage-gate.mjs --fixture scripts\fixtures\agent-runtime\final-behavior-matrix.json --report specs\011-taliya-commercial-agent-core-reset\eval-reports\agent-runtime-spec011-full-required-final-matrix-budgeted-1.json --report specs\011-taliya-commercial-agent-core-reset\eval-reports\agent-runtime-spec011-full-required-remaining-budgeted-1.json --name agent-runtime-spec011-full-required-final-matrix-coverage-1
git -c safe.directory=C:/Users/lucas/agentes-landing-system diff --name-only -- app/pilates components/landing data/landing lib/landing/floating-agent.ts components/internal/SalesInboxClient.tsx
```

Results:

- Focused validator/repair/product-claim suite: 63 passed.
- Focused runtime behavior regression suite: 9 passed, 85 deselected.
- Ruff: passed.
- Static audit: 8/8 passed.
- Report contract for fixed integration real-model report: 7/7 passed.
- Report contract for fixed diagnostic-refusal real-model report: 7/7 passed.
- Product-followup delta coverage gate: 6/6 passed, selected pass-evidence cost US$0.085131.
- Final behavior matrix coverage gate: 29/29 passed, selected pass-evidence cost US$0.533415.
- New real OpenAI calls made during this closure cost US$0.070573 total: integration fixed US$0.014003, remaining product-delta run US$0.042342, diagnostic-refusal fixed US$0.014228.
- Protected source diff command returned no files.

T011-104 changed:

- `services/taliya-agent-runtime/app/core/taliya_commercial/conductor.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial/conductor_policy.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial/validators.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial/repair.py`
- `services/taliya-agent-runtime/tests/test_spec011_validators_core.py`
- `services/taliya-agent-runtime/tests/test_spec011_validators_product_claims.py`
- `services/taliya-agent-runtime/tests/test_spec011_repair_loop.py`
- `scripts/eval-agent-runtime-spec011-coverage-gate.mjs`
- `specs/011-taliya-commercial-agent-core-reset/tasks.md`
- `specs/011-taliya-commercial-agent-core-reset/coverage-map.md`
- `specs/011-taliya-commercial-agent-core-reset/implementation-ledger.md`
- T011-104 eval reports under `specs/011-taliya-commercial-agent-core-reset/eval-reports/`

Remaining after T011-104:

- T011-105 golden transcripts and do-not-do fixtures.
- T011-106 Sales Inbox projection export.
- T011-107 mandatory trace export.
- T011-108 manual transcript package.
- T011-109 explicit product-owner approval.
- T011-110 production preflight/cutover plan.
- T011-111 rollback proof immediately before production activation.
- T011-112 approval log.

## Anti-Drift Review Questions

Ask these before and after each task:

- Did the LLM remain the owner of commercial understanding?
- Did deterministic code stay limited to operation, safety, validation, rendering, persistence, delivery, handoff, idempotency, and pure empty cold greeting?
- Did the change make the core smaller and more typed, or did it create another hidden brain?
- Could the same bug return because the proof only checked strings and not state, trace, usage, and projection?
- Is every customer-facing claim grounded in official product knowledge or Spec 006?
- Is Sales Inbox a projection of validated state/events, not a second interpretation engine?
- Did we label isolated-core proof honestly instead of implying production is already safe?
