# Tasks - Spec 012 Agents SDK Migration

These tasks are documentation and implementation planning tasks. They do not authorize production code changes until the user approves the migration plan.

## Phase 0 - Decision And Freeze

- [x] T012-000 Maintain Spec 012 implementation ledger, coverage map, and decision log as mandatory controls.
- [x] T012-001 Confirm OpenAI Agents SDK as the selected engine for the next Taliya commercial agent implementation.
- [x] T012-002 Freeze Spec 011 and preserved Spec 010 contracts as behavior source of truth.
- [x] T012-003 Confirm that current Spec 011 implementation is not the final motor and should not receive more tactical commercial patches except safety/rollback fixes.
- [x] T012-004 Confirm protected scope: no `/pilates` redesign, no multi-tenant, no client/studio WhatsApp, no checkout, no Sales Inbox UI redesign.
- [x] T012-005 Confirm SDK privacy/tracing policy before any production or externally stored traces.
- [x] T012-006 Record D-012-001 through D-012-007 in `decision-log.md` before SDK implementation code.

## Phase 1 - SDK Design Lock

- [x] T012-010 Define `TaliyaTurnProposal` schema.
- [x] T012-011 Define SDK agent topology and handoff graph.
- [x] T012-012 Define tool side-effect classes: read-only, proposal-only, commit-after-validation.
- [x] T012-013 Map every preserved Spec 010/011 behavior to agent/tool/guardrail/validator/renderer/eval owner.
- [x] T012-014 Define SDK trace-to-Taliya-trace mapping.
- [x] T012-015 Define SDK cost budget and max-turn policy.
- [x] T012-016 Define abort criteria for SDK spike.
- [x] T012-017 Update `coverage-map.md` with exact owners/evidence for all P0/P1 preserved behaviors before spike code.
- [x] T012-018 Define static anti-drift audit patterns before SDK implementation.
- [x] T012-019 Define explicit RAG/product knowledge policy before SDK implementation.

## Phase 2 - Isolated SDK Spike

- [x] T012-020 Create isolated SDK prototype path without public cutover.
- [x] T012-021 Implement minimal Taliya agents with instructions from behavior contracts.
- [x] T012-022 Implement read-only/proposal-only tools.
- [x] T012-023 Implement SDK output adapter to `TaliyaTurnProposal`.
- [x] T012-024 Reuse a focused validator/render path for spike output.
- [x] T012-025 Run no-cost/mocked SDK contract tests.
- [x] T012-026 Prepare paid spike approval packet.
- [x] T012-026B Build the no-cost real SDK runner harness and dry-run gate (strict output type, run-context state, tracing disabled, budget meter, frozen multi-turn inputs, report writer) so T012-027 has something safe to execute.
- [x] T012-027 Run approved paid SDK spike scenarios.
      Closed on 2026-06-16 as executed and superseded by the action-first
      architecture. Evidence:
      `evidence/t012-027-paid-spike-closure-action-first-superseded.md`, plus
      the existing `evidence/t012-027/attempt-*` reports,
      `evidence/t012-027/attempt-4-to-7-and-ideal-conversation-analysis.md`,
      and `evidence/t012-027/action-first-battery-summary.md`. The paid spike
      ran under explicit approvals, reached 15/15 structural pass on the
      original frozen scenarios, then exposed why the original template-first
      boundary must not be the production motor. D-012-012 superseded that
      boundary with action-first, and T012-028/T012-029 recorded the
      continue/adapt decision. No new paid call was made for this closure.
- [x] T012-028 Compare SDK spike to current Spec 011 path.
- [x] T012-029 Decide continue/adapt/abort based on spike evidence.

## Phase 3 - SDK Core Implementation (action-first per design-lock-v2)

Revised on 2026-06-10 by D-012-012: the production core follows
`011/action-contract.md` (Turn Situation Builder -> LLM
`ConductorActionDecision` -> Decision Compiler), not the spike's
LLM-selects-templates boundary. See `design-lock-v2-action-first.md`.

- [x] T012-030A Define strict `ConductorActionDecision` output schema (small
      action decision; no final template plan, no official-source variable
      values, no state transitions) and per-mode action menus.
- [x] T012-030B Build the Turn Situation Builder (deterministic board from
      persisted state: mode, pending_question_key, allowed_actions,
      eligible_template_groups, missing keys, forbidden actions). Absorbs the
      spike's state preamble and diagnostic-sequence guardrails.
- [x] T012-030C Build the Decision Compiler (state transition, ledger merge,
      staged final diagnostic sequence including deliver_hold, template group
      expansion, official-source variables, projection inputs, render plan).
- [x] T012-030D Rewire the SDK agents to the action-first contract (triage
      pure router preserved; specialists consume the action menu and return
      `ConductorActionDecision`).
- [x] T012-031 Integrate the action-first SDK runner behind a feature flag on
      the current endpoint (context builder, situation builder, compiler,
      validators, renderer, persistence, delivery).
- [x] T012-032 Port the FULL Spec 011 validator set plus the 010 voice rules
      (banned phrases, anti-parrot feedback, no-CRM-for-lay-lead,
      owner-language, repeated-greeting block, rejected final formats,
      thin-context "pelo que voce contou" block, answer-adequacy map).
- [x] T012-032B Add the delta-contract coverage: product knowledge keys
      (how_it_works, routine_areas, whatsapp_scope, integration_scope,
      comparison_*, security_and_data, availability_and_onboarding,
      out_of_profile), the 5 delta templates, post-diagnostic compact context,
      objection/refusal/resume/out-of-profile behavior, and the name policy.
- [x] T012-033 Adapt approved renderer to the compiler's render plan.
- [x] T012-034 Adapt trace store/export for SDK run items plus
      situation/decision/compiler records.
- [x] T012-035 Adapt Sales Inbox projection (persisted, verified end to end).
- [x] T012-036 Preserve runtime API/HMAC/idempotency/turn gate; add the
      per-conversation cost cap.
- [x] T012-037 Prove no old runner/TS v2 public fallback.
- [x] T012-032C Implement the SDK-path safety guardrails deferred by
      D-012-010: prompt injection, unsupported media, sensitive data, medical
      advice. Mandatory before shadow mode (Phase 5 cannot start without it).
- [x] T012-038 Port canonical fixtures: `011/regression-cases.md` and
      `011/do-not-do-static-fixtures.json` replace the 15 reconstructed spike
      scenarios as the paid-eval source of truth. The 3 open attempt-8
      regression failures are superseded by this task: those scenarios are
      re-validated under action-first against the canonical set.
- [x] T012-038B Extend fixtures with the uncovered conversational cells:
      interruption matrix (question types x phases), answer correction
      ("na verdade sao 80, nao 120"), multiple answers in one message,
      objection mid-diagnostic, resume after days, and messy real-world input
      (typos, abbreviations, slang, no punctuation - e.g. "qto fica?",
      "tem como ver ai mn").
- [x] T012-039 Build the Layer 3 quality-judge harness from
      `010/contracts/eval-contract.md` (P1 average >= 4.2, none below 4.0;
      structural pass is never the success measure).
- [x] T012-039B Fix the spike conversation-harness transcript assembly
      (duplicated rendered chunks, encoding glitch) so manual review reads
      clean transcripts. (Superseded: the action-first conversation runner
      builds clean transcripts by construction; proven by test.)

## Phase 4 - Verification

- [x] T012-040 Run static audit.
- [x] T012-041 Run SDK contract tests.
- [x] T012-042 Run mocked SDK run-item fixtures.
- [x] T012-043 Run real-model golden transcripts.
      Paid test approved on 2026-06-15. First attempt was blocked before any
      OpenAI call because the runtime did not load `.env.local`; after explicit
      approval to reuse the existing key, the real-model runner executed the
      canonical 9-scenario Spec 011 golden set multiple times while no-cost
      fixes were applied between reruns. Latest full run:
      `evidence/t012-043-real-model-golden-transcripts/20260615T211155Z/`
      executed 9/9, passed 9/9, 32 model ops, `$0.087127`, not aborted.
      Total recorded T012-043 paid spend in reports is `$1.205769`. The prior
      failed `final-price-first` case was confirmed in isolation:
      `evidence/t012-043-real-model-golden-transcripts/20260615T204145Z/`
      passed 1/1, 2 model ops, `$0.004265`. The previous residual failure was
      `step3g-long-conversation`: waitlist turn 12 declared `how_it_works` plus
      `availability_and_onboarding`, but rendered `waitlist.current_path_explained`
      instead of required `product.how_it_works_direct`. This was fixed no-cost
      by prioritizing how-it-works answers before waitlist missing-detail
      continuation, then confirmed by the automated 9/9 full rerun. Manual
      review after the 9/9 run rejected closure because the customer-facing
      transcripts still contained quality/safety issues: leaked internal policy
      text ("Nao prometa..."), third-person internal summary copy in waitlist,
      duplicated diagnostic feedback chunks, confusing report check
      explanations, and a template mismatch around waitlist/product-question
      continuation. These were fixed no-cost on 2026-06-15 with final
      customer-visible guardrails, approved public copy for WhatsApp/waitlist/
      diagnostic/price/handoff, and report-check cleanup. Encoding/mojibake
      was reviewed as item 1 and mapped as a false
      positive caused by reading UTF-8 evidence through the Windows default
      encoding; the saved transcript files are UTF-8 and do not require runtime
      correction. Latest no-cost Spec 012 validation after these fixes:
      `270 passed / 716 deselected`; focused ruff passed. Consolidated
      evidence: `evidence/t012-043-real-model-golden-reruns-20260615.md` and
      `evidence/t012-043-golden-failure-fixes-nocost-20260615.md`. Do not
      advance to T012-044 until a paid rerun is explicitly approved/executed/
      reviewed after the manual-review fixes. New approved paid rerun on
      2026-06-16:
      `evidence/t012-043-real-model-golden-transcripts/20260616T001941Z/`
      executed 9/9, passed 7/9, failed `final-price-plus-pain` and
      `step3g-long-conversation`, 32 model ops, `$0.089871`, not aborted.
      No-cost follow-up fixed `final-price-plus-pain` expectation to match the
      approved generic contextual hook and tightened agent/repair instructions
      so pain-first and diagnostic `answer_feedback` use a practical reading
      instead of echoing the lead. Verification: preflight-only passed, Spec
      012 suite `270 passed / 716 deselected`, focused ruff clean, paid calls
      `$0` for this follow-up. Additional no-cost fix before the next paid
      round: diagnostic answer feedback is now compiler-owned fixed copy per
      captured question, final diagnostic agent recommendation no longer
      renders free `agent_pain_resolved`, and stale `price_objection` is
      filtered from the legacy validator bridge when the accepted action is
      waitlist. Verification: focused fixes `6 passed`, full Spec 012 suite
      `271 passed / 716 deselected`, focused ruff clean, golden preflight-only
      passed, paid calls `$0` for this follow-up. Additional PT-BR/punctuation
      hardening before the next paid round: the renderer now normalizes common
      customer-facing unaccented Portuguese outside URLs, the action-first
      prompt requires Brazilian Portuguese with correct accents and punctuation
      for human composition variables, and Spec 012 text contracts were updated
      to assert the accented public output. Verification: full Spec 012 suite
      `271 passed / 716 deselected`, focused ruff clean, SDK preflight `6
      passed`, paid calls `$0` for this follow-up. The approved paid rerun
      after PT-BR source cleanup is saved at
      `evidence/t012-043-real-model-golden-transcripts/20260616T112913Z/`:
      9/9 executed, 7/9 passed, failed `final-price-first` and
      `final-demo-request`, 34 model ops, `$0.089745`, not aborted. No-cost
      follow-up fixed both blockers by correcting action FORM from the LLM's
      structured fields only (`prices`/`price_question` and
      `demo_intent=requested`/`demo`), preserving the raw LLM decision in trace;
      price-objection copy was also corrected from `E`/`não e` to `É`/`não é`.
      Verification after the no-cost fix: full Spec 012 suite `273 passed /
      716 deselected`, focused ruff clean, golden preflight-only passed, paid
      calls `$0` for this follow-up. The explicitly approved paid confirmation
      after that fix is saved at
      `evidence/t012-043-real-model-golden-transcripts/20260616T120633Z/`:
      9/9 executed, 8/9 passed, failed only `step3g-long-conversation`, 32
      model ops, `$0.085023`, not aborted. It confirmed `final-price-first`
      and `final-demo-request` fixed. Remaining failure was turn 12 during
      waitlist: `answer_question_then_continue_waitlist` lacked a product fact
      key and fell back to `product.overview_short`, whose official fact
      contained internal marker `Não prometa...`; validator correctly blocked
      it as `customer_visible_internal_text_leak`. No-cost follow-up fixed the
      waitlist contract-info path to render `waitlist.current_path_explained`
      when the LLM declares `waitlist_intent=contract_intent` without product
      fact keys. Verification after this fix: focused waitlist tests `2
      passed`, full Spec 012 suite `274 passed / 716 deselected`, focused ruff
      clean, golden preflight-only passed, paid calls `$0` for this follow-up.
      Final paid confirmation is saved at
      `evidence/t012-043-real-model-golden-transcripts/20260616T121413Z/`:
      9/9 executed, 9/9 passed, 0 failed, 33 model ops, `$0.087158`, not
      aborted. Manual transcript spot-review after the run found the nine
      flows coherent enough for the automated T012-043 closure: price,
      price+pain, pain-first, Instagram/source, WhatsApp scope, long
      conversation, waitlist joined, human handoff pause, and demo request.
      No public cutover is implied by this closure.
- [x] T012-044 Run do-not-do fixtures.
      Closed on 2026-06-16 for the Spec 012 action-first SDK/no-cost gate.
      Evidence: `evidence/t012-044-do-not-do-fixtures.md`. Verification:
      canonical do-not-do + safety `19 passed`; canonical port + do-not-do +
      safety `23 passed`; full Spec 012 suite `274 passed / 716 deselected`;
      focused ruff passed. No paid OpenAI calls. A broad exploratory selector
      that also reached legacy Spec 011 reported one Spec 011 adapter fixture
      failure; it is documented as out of scope for T012-044 because AGENTS.md
      forbids implementing Spec 011 and the equivalent Spec 012 SDK fixture
      passed.
- [x] T012-045 Export mandatory trace evidence.
      Closed on 2026-06-16 using the approved T012-043 real-model 9/9 report
      as source. Evidence:
      `evidence/t012-045-mandatory-trace-evidence/summary.md` and
      `evidence/t012-045-mandatory-trace-evidence/summary.json`, plus one
      `012.action_trace_export.v1` package per golden scenario. Result: 9
      scenarios, 22 turns, 21 required traces, all required trace sections
      complete, no missing trace turns, no incomplete traces. The one
      non-traced turn is the expected post-handoff suppressed turn. External
      provider trace export remains disabled by D-012-007/D-012-009. No public
      delivery, outbox reservation, endpoint cutover, `/pilates`, checkout,
      Sales Inbox UI, multi-tenant, or client/studio WhatsApp work.
      Verification: action trace export + contract gate `4 passed`; full Spec
      012 suite `274 passed / 716 deselected`; focused ruff passed.
- [x] T012-046 Export Sales Inbox projection evidence.
      Closed on 2026-06-16 using the approved T012-043 real-model 9/9 report
      as source. Evidence:
      `evidence/t012-046-sales-inbox-projection-evidence/summary.md` and
      `evidence/t012-046-sales-inbox-projection-evidence/summary.json`, plus
      one `012.sales_inbox_projection_export.v1` package per golden scenario.
      Result: 9 scenarios, 22 turns, 21 required projections, all projections
      complete, no missing required fields, no missing projection turns. The
      one non-projected turn is the expected post-handoff suppressed turn. This
      is local projection evidence only: no Sales Inbox UI, persistence commit
      behavior, public delivery, endpoint cutover, `/pilates`, checkout,
      multi-tenant, or client/studio WhatsApp work. Verification: Sales Inbox
      projection + contract gate `7 passed`; full Spec 012 suite `274 passed /
      716 deselected`; focused ruff passed.
- [x] T012-047 Prepare manual transcript review package.
      Closed on 2026-06-16 using the approved T012-043 real-model 9/9 report.
      Evidence:
      `evidence/t012-047-manual-transcript-review-package/summary.md` and
      `evidence/t012-047-manual-transcript-review-package/summary.json`, plus
      one `012.manual_transcript_review.v1` package per golden scenario. The
      package contains all 9 transcripts, 22 turns, 21 delivered turns, 1
      expected post-handoff suppressed turn, trace/projection presence flags,
      source check results, and a product-owner checklist. Review status remains
      `pending_manual_review`; manual decision remains `pending`. Verification:
      manual review package + contract gate `3 passed`; full Spec 012 suite
      `274 passed / 716 deselected`; focused ruff passed.
- [x] T012-048 Get explicit product-owner approval.
      Closed on 2026-06-16 as limited approval for technical advance to
      simulated/no-cost shadow mode only. Evidence:
      `evidence/t012-048-product-owner-approval-limited-shadow-simulation.md`.
      User clarified there are no real production leads yet and approved the
      narrower wording: advance to shadow/simulation without real leads, without
      public activation, and without automatic paid cost. This does not approve
      real lead traffic shadowing, public activation, paid OpenAI calls,
      external trace export, `/pilates`, Sales Inbox UI, checkout, multi-tenant,
      or client/studio WhatsApp work.

## Phase 5 - Shadow And Cutover

- [x] T012-050 Run SDK path in shadow mode.
      Closed on 2026-06-16 for simulated/no-cost shadow mode under the limited
      T012-048 approval. Evidence:
      `evidence/t012-050-simulated-shadow-mode.md`. The Spec 012 runtime
      adapter now honors explicit `metadata.spec012_shadow_mode.enabled=true`,
      runs the action-first pipeline with an injected no-cost SDK model,
      suppresses public messages, records local trace/projection/usage evidence,
      and does not mutate live runtime state. Verification: runtime adapter +
      contract gate `6 passed`; full Spec 012 suite `275 passed / 716
      deselected`; focused ruff passed. Real production lead traffic shadowing
      remains unapproved and unnecessary while there are no real leads.
- [x] T012-051 Compare SDK shadow output against golden/manual samples.
      Closed on 2026-06-16 in simulated/no-real-leads mode. Evidence:
      `evidence/t012-051-simulated-shadow-comparison/summary.md` and
      `evidence/t012-051-simulated-shadow-comparison/summary.json`. The
      comparison covered all 9 approved T012-043 scenarios against the T012-047
      manual package, T012-045 trace completeness, T012-046 projection
      completeness, and T012-050 simulated shadow invariant. Result: 9/9
      compared scenarios passed, no failures, no real lead traffic, no public
      activation, no paid OpenAI call for this task.
- [x] T012-052 Prove rollback disables SDK without old deterministic commercial brain.
      Closed on 2026-06-16. Evidence:
      `evidence/t012-052-rollback-no-old-brain.md`. Runtime flags prove the
      desired behavior: with Spec 012 enabled, the API routes to the SDK
      adapter; with OpenAI provider and no paid approval, paid calls are blocked;
      with Spec 012 disabled and Spec 011 commercial core disabled, the API
      returns `spec011_core_disabled` instead of invoking the old core; the
      legacy `/v1/agent-runs` route remains quarantined. Verification:
      API/settings/static/contract tests `28 passed`; focused ruff passed. No
      paid OpenAI calls and no public activation.
- [x] T012-053 Prepare production preflight.
      Closed on 2026-06-16 as local/no-real-leads production preflight
      preparation, matching the user's clarification that production currently
      has no real leads. Evidence:
      `evidence/t012-053-production-preflight-local-no-real-leads.md`.
      Verification: SDK preflight + paid harness dry-run + static audit +
      contract gate `35 passed`; real-model golden runner `--preflight-only`
      loaded all 9 canonical scenarios and reported
      `paid_call_status: not_attempted_preflight_only`. No paid OpenAI call,
      no real traffic shadowing, no public activation, and no protected-scope
      work.
- [x] T012-054 Prepare first-hours emergency watch.
      Closed on 2026-06-16 as a local/no-real-leads emergency watch runbook.
      Evidence:
      `evidence/t012-054-first-hours-emergency-watch-local-no-real-leads.md`.
      The watch defines first-check timing, two-hour active watch, stop
      conditions, and evidence sources for any future activation, but does not
      activate the SDK path or monitor real traffic. No paid OpenAI call, no
      real traffic shadowing, no public activation, and no protected-scope
      work.
- [x] T012-055 Activate only after explicit approval.
      Approved on 2026-06-16 by the user instruction to remove the extra
      paid-approval flag, remove the docs that mention it, and put the agent
      live. Evidence:
      `evidence/t012-055-public-activation-direct.md`. Production now routes
      `/v1/taliya-commercial/turn` to the Spec 012 action-first SDK runtime
      when `TALIYA_AGENT_RUNTIME_ENV=production` and
      `TALIYA_AGENT_PROVIDER=openai`. Deploy/smoke verification completed on
      2026-06-16: Supabase project `pxvabrsngfhebytdqxth` was active/healthy,
      runtime schema and RLS migrations were applied, public health passed, and
      paid production smoke `req_spec012_public_smoke_1781620949` returned
      HTTP 200 with runtime status `succeeded`.

## Phase 6 - Luna Production Migration

- [x] T012-056 Prepare the no-cost Luna migration preflight.
      Closed on 2026-08-04. The public runtime no longer imports or falls back
      to the old Spec 011 commercial engine; runtime failures and empty/invalid
      responses produce a safe operational reply instead of a silent widget.
      Action agents use `gpt-5.6-luna` with `reasoning.effort=none`; pricing,
      cached-token accounting, repairs, latency, SDK versions, and build/model
      health metadata are recorded. Direct dependencies are pinned and the
      Linux lock built successfully in Docker. Added a neutral
      `pause_waitlist_decision` action so hesitation does not force data
      collection, joining, or decline. Evidence:
      `evidence/t012-056-luna-migration-preflight.md` and
      `evidence/luna-migration-targeted/`. Verification: Spec 012 `283 passed`;
      active production gate `514 passed`; widget adapter `10/10`; delivery
      audit `34/34`; zero-cost aggregate `6/6`; TypeScript, ESLint, focused Ruff,
      and the Next.js production build passed; Linux Docker image and
      `/healthz` passed. Official Luna pricing was verified and corrected to
      `$1.00` input / `$0.10` cached input / `$1.25` cache-write input / `$6.00`
      output per million tokens. Cache-write usage is extracted, persisted,
      traced, and included in the hard cap. Post-correction verification:
      focused `71 passed`, Spec 012 `283 passed`, production gate `515 passed`,
      and rebuilt Docker health passed.
      Paid-call status: `$0`.
- [x] T012-057 Run the explicitly approved Luna real-model gate. Completed
      after explicit user approval on 2026-08-04 with a cumulative hard ceiling
      of `$0.75` and a user-reported available balance of `$1.03`.
      Required order: one targeted canary; all 3 targeted migration scenarios;
      the canonical 9-scenario set three consecutive times. Compare against the
      archived approved `gpt-5.4-mini` 9/9 evidence. Save complete transcripts,
      selected actions, templates, traces, token usage, latency, repairs, and
      cost for every turn. Stop on the first runtime/model-access failure,
      safety/internal leak, silent successful turn, or budget cap. Approval is
      recorded in D-012-017. A single cumulative ledger must cover
      every phase; separate per-command budgets must not reset the ceiling.
      First canary attempt stopped on its first failed scenario after `5` model
      operations and `$0.016029`. Luna correctly selected the price-objection
      action, but the Spec 011 validator bridge omitted the compiler's
      `diagnostic_offered` action mapping and blocked delivery with
      `price_question_missing_diagnostic_offer`. The no-cost parity fix and an
      exact two-turn mocked regression now pass; Spec 012 is `285 passed` and
      the active production gate is `517 passed`. The transcript reporter now
      retains failed inbound turns. Evidence:
      `evidence/t012-057-luna-paid-gate/canary-failure-review.md`. The exact
      canary rerun passed and brought reported cumulative spend to `$0.027981`.
      The targeted phase then passed its first scenario and stopped before the
      second transcript was returned because its initial completed-diagnostic
      fixture lacked the required projection fields. After the no-cost fixture
      correction and whole-batch preflight, isolated reruns closed the targeted
      gate at `3/3`: price objection `$0.011370`, waitlist hesitation
      `$0.007805`, and diagnostic acceptance without regreeting `$0.005308`.
      Canonical round 1 then completed at `6/9` and `$0.118506`. The three
      failures were: pain acknowledgement lost the concrete `WhatsApp` anchor;
      Instagram interest selected a generic action and invented a fact key;
      waitlist capture extracted both pending fields but asked for one again.
      Paid execution stopped for no-cost correction. The schema now constrains
      product fact keys, the LLM prompts preserve concrete context and select
      the source-specific action, the compiler consumes newly captured waitlist
      slots before choosing the next operation, and the paid runner is proven
      fail-fast. Verification after correction: focused `103 passed`, Spec 012
      `293 passed / 718 deselected`, active production gate `525 passed`, focused
      Ruff and `git diff --check` passed, and the pinned Luna Docker image passed
      `/healthz`. Reported cumulative spend is `$0.170970`; the conservative
      unreconciled reserve remains `$0.020000`, for `$0.190970` operationally
      accounted. No paid call was made after the failed canonical round.
      Evidence: `evidence/t012-057-luna-paid-gate/targeted-stop-review.md` and
      `evidence/t012-057-luna-paid-gate/canonical-round-1-stop-review.md`.
      Final closure: after isolated recovery of the three first-round failures,
      Luna completed three consecutive canonical `9/9` rounds with full human
      transcript review. A later automated 9/9 was correctly rejected by human
      review for a redundant WhatsApp answer; answer-adequacy was fixed at zero
      cost, the isolated case passed, and the recovery round passed 9/9. Total
      reported spend: `$0.685395`; operationally accounted with reserve:
      `$0.705395`, below the approved `$0.75` ceiling. Compared with the
      `gpt-5.4-mini` baseline, accepted Luna rounds had equal 9/9 structural
      stability and repairs, about 41.7% higher cost and 25.7% higher wall time.
      Evidence: `evidence/t012-057-luna-paid-gate/closeout.md`.
- [x] T012-058 Deploy the compatibility build while preserving the current
      production model, then verify build/model/SDK health metadata and the
      public widget operational fallback.
      Completed on Railway deployment
      `65201fcd-0848-4d66-9208-0f753f00261d`: health passed in production with
      model `gpt-5.4-mini`, reasoning none, OpenAI `2.44.0`, and Agents SDK
      `0.18.0`. No paid call or model switch occurred. Evidence:
      `evidence/t012-058-compatibility-deployment.md`.
- [x] T012-059 Switch Railway `TALIYA_AGENT_MODEL` to `gpt-5.6-luna`, deploy,
      and run the approved paid production smoke through the public widget/API.
      Roll back to the previous Railway deployment/model if any stop condition
      is hit; never restore the legacy commercial brain.
      Attempt 1 stopped before model execution: deployment
      `7cf61829-aaec-4fdb-b444-d062f2de0873` was healthy on Luna, but the public
      smoke returned `runtime_database_unavailable` because Supabase project
      `pxvabrsngfhebytdqxth` was `INACTIVE`. Railway was rolled back to
      `gpt-5.4-mini` in successful deployment
      `fb31d45d-245f-4d72-97ce-1f581766575a`. No OpenAI usage was reported and
      the approved budget ledger is unchanged. The existing Supabase project
      is being restored before any new paid smoke. Evidence:
      `evidence/t012-059-luna-switch-attempt-1.md`.
      Completed after restoration and no-cost database proof. Production smoke
      `t012059_luna_prod_smoke_2_1785894540` succeeded on Luna with 2 model
      operations, 0 repairs, and `$0.006091`. Human review accepted the full
      three-message WhatsApp answer. Two defects exposed by the smoke were
      corrected without another paid turn: direct WhatsApp answers no longer
      claim `diagnostic_offered` unless the rendered response actually offers
      it, and public assistant IDs are stable across idempotent replays. Full
      gates and both Railway/Vercel production builds passed. Final active
      Railway: `48ae1d84-63db-4633-8288-b8af40246e0f`; final active Vercel:
      `dpl_E7EPTbJoKiXuf5ekNq27W33PEcSB`; source/build SHA:
      `5c15aed6a68a2907789e34843d7c4efd152cf927`. Evidence:
      `evidence/t012-059-luna-production-switch.md`.
- [x] T012-060 Complete the first-hours watch and close the Luna migration with
      production transcripts, persistence/usage evidence, final cost, and the
      exact active Railway deployment/build SHA.
      Closed on 2026-08-05 under the previously approved no-real-leads scope.
      The post-activation watch found no new real runs, no additional model
      cost, and no Railway/Vercel 5xx. Supabase remained `ACTIVE_HEALTHY`; the
      paid smoke transcript, persisted run/trace, exact usage, stable public
      replay IDs, deployment IDs, image digest, and Git SHA were verified.
      Reported cumulative spend is `$0.691486`; with the conservative
      `$0.020000` reserve, `$0.711486` is operationally accounted and
      `$0.038514` remains under the approved ceiling. No synthetic paid traffic
      was generated merely to extend an empty watch window. Evidence:
      `evidence/t012-060-luna-first-hours-watch-closeout.md`.

## Task Closure Requirements

Each task must close with:

- scope confirmation;
- files changed;
- evidence path;
- tests/evals run;
- whether proof is design, mocked, isolated spike, integration, shadow, or production-path;
- anti-determinism review;
- protected-scope diff result;
- paid-call status and cost, when applicable;
- next task lock.

If any of these are missing, the task remains open.
