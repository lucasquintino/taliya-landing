# Requirements Evidence Matrix

Date: 2026-05-22

Update: Product-owner review added final diagnostic/demo/name correction requirements after this matrix was originally generated. Rows marked **Verified** below are historical for the prior T158-T204 gate unless they explicitly reference T206-T226 evidence. Production approval requires new evidence for FR-034A-D and SC-030-SC-035.

Status legend:

- **Verified**: current repository evidence proves the requirement in local/runtime/real-OpenAI scope.
- **Pending external gate**: implementation support exists, but completion requires product-owner approval, production deploy, production env configuration, or live WhatsApp smoke.
- **Out of scope enforced**: requirement is satisfied by explicit rejection, naming, docs, or tests that prevent scope expansion.

## Functional Requirements

| ID | Status | Primary evidence |
| --- | --- | --- |
| FR-001 | Pending external gate | Official Next routes are wired to `runtime-client.ts`; production cutover still blocked by T211-T226, T132-T135, and T205 approval. |
| FR-002 | Verified | Real OpenAI matrix `28/28`; `agent-runtime-invariants.json`; `test_reference_structure.py`. |
| FR-003 | Verified | `reference-map.md`; `services/taliya-agent-runtime/app/domains/taliya_commercial/agents.py`; runner/tool/guardrail tests. |
| FR-004 | Verified | `reference-map.md`. |
| FR-005 | Verified | `services/taliya-agent-runtime/README.md`; `railway.toml`; naming eval. |
| FR-006 | Verified | `test_agent_registry.py`; real OpenAI payloads use `agent_key: taliya_commercial`. |
| FR-007 | Verified | `/v1/agent-runs` contract tests and `app/runtime/registry.py`. |
| FR-008 | Verified | Unknown/future agent registry tests. |
| FR-009 | Verified | Runtime schema tests for `agent_family`, `owner_scope`, nullable `tenant_id`; future-agent docs. |
| FR-010 | Out of scope enforced | `rollout-and-deploy.md`; no client studio WhatsApp integration tasks. |
| FR-011 | Out of scope enforced | Future studio operation agents are reserved/rejected only. |
| FR-012 | Verified | Protected `/pilates` baseline docs; no intentional landing redesign in 010 changes. |
| FR-013 | Verified | `baseline.md` and protected landing baseline folder. |
| FR-014 | Verified | Task T004 complete; route edits are limited to runtime integration. |
| FR-015 | Verified | Next routes and Sales Inbox remain in `app/`, `lib/`, `components/`; runtime is separate service. |
| FR-016 | Pending external gate | Railway config and deploy preflight checks exist; actual Railway deploy T132 is intentionally pending. |
| FR-017 | Verified | `test_hmac_auth.py`; `runtime-client.ts`; runtime HMAC verifier. |
| FR-018 | Verified | HMAC stale/signature/body contract tests. |
| FR-019 | Verified | `GET /healthz`; local health check returned OK; production healthcheck returns `503` when required config is incomplete. |
| FR-020 | Verified | Structured response schema tests and real OpenAI payloads. |
| FR-021 | Verified | `app/runtime/schemas.py`; real OpenAI transcript payloads; Sales Inbox projection tests. |
| FR-022 | Verified | Output guardrail tests and runtime validators. |
| FR-023 | Verified | Tool registration/idempotency tests; side effects are tool-mediated; misconfigured production run endpoint blocks without idempotent side effect. |
| FR-024 | Verified | Product knowledge eval and real transcript source versions. |
| FR-025 | Verified | Real OpenAI direct price/product scenarios. |
| FR-026 | Verified | Product knowledge invariant tests and no-invented-link checks. |
| FR-027 | Verified | Product source version tests and Sales Inbox source projection. |
| FR-028 | Verified | Real OpenAI direct-question checks; quality judge directness dimension. |
| FR-029 | Verified | Real behavior matrix includes ambiguous/mixed/out-of-order scenarios. |
| FR-030 | Verified | Diagnostic ledger tests for prior volunteered facts. |
| FR-031 | Verified | Diagnostic ledger/completion tests and real thin diagnostic scenario. |
| FR-032 | Verified | Diagnostic schema, Postgres-backed persistence tests, and Sales Inbox projection. |
| FR-033 | Verified | Behavior matrix covers diagnostic offer timing. |
| FR-034 | Verified | Waitlist contract tests and clear-contract-intent scenarios. |
| FR-034A | Pending correction implementation | New staged final diagnostic requirement added after product-owner review; covered by tasks T211-T224. |
| FR-034B | Pending correction implementation | New demo-state branch requirement added after product-owner review; covered by tasks T214, T217, T224. |
| FR-034C | Pending correction implementation | New WhatsApp/widget name timing requirement added after product-owner review; covered by tasks T215, T221, T224. |
| FR-034D | Pending correction implementation | New diagnostic feedback cadence requirement added after product-owner review; covered by tasks T211, T220, T224. |
| FR-035 | Verified | Waitlist idempotency tests. |
| FR-036 | Verified | Waitlist tool/store tests and Sales Inbox waitlist projection. |
| FR-037 | Verified | No-phone-request invariants and real cold/direct scenarios. |
| FR-038 | Verified | Widget contact capture is gated by runtime/client behavior and evals. |
| FR-039 | Verified | Human handoff tests and real handoff scenario. |
| FR-040 | Verified | WhatsApp webhook local HTTP harness `10/10`. |
| FR-041 | Verified | Sales Inbox handoff route and handoff evals. |
| FR-042 | Verified | Real handoff second-turn silence and `human_paused` payload. |
| FR-043 | Verified | Runner events, usage, tool summaries, guardrail fields, Sales Inbox projection tests. |
| FR-044 | Verified | Model usage tests and real provider usage in reports. |
| FR-045 | Verified | Cost cap tests and cost eval. |
| FR-046 | Verified | Template registry/renderer tests; real transcripts include `template_ids`. |
| FR-047 | Verified | Runtime path uses `runtime-client.ts`; old v2 quarantined from official path. |
| FR-048 | Verified | No legacy conversational fallback in runtime client; release readiness records this. |
| FR-049 | Verified | Safe fallback, unsupported media, cost cap, and handoff tests. |
| FR-050 | Verified | Local WhatsApp webhook harness `10/10`; delivery matrix `20/20`. |
| FR-051 | Verified | Widget adapter reused; no visual redesign. |
| FR-052 | Verified | Existing lead/Sales Inbox store extended; Sales Inbox eval `14/14`. |
| FR-053 | Verified | Naming eval; migration uses `agent_runtime_*`. |
| FR-054 | Verified | Runtime schema scope tests. |
| FR-055 | Verified | Real OpenAI payloads show `taliya` family/scope and `tenant_id: null`. |
| FR-056 | Verified | Runtime eval suite includes invariants, transcripts, and quality judge. |
| FR-057 | Verified | Quality judge now scores real transcripts and can fail naturalness/usefulness. |
| FR-058 | Verified | Blocking failures alias and quality judge report are separate artifacts. |
| FR-059 | Pending external gate | Manual widget/local HTTP WhatsApp documented; live WhatsApp production smoke T135 pending. |
| FR-060 | Pending external gate | Final production gate requires T211-T226 evidence, T205 approval, and T132-T135 rollout. |
| FR-061 | Verified | Redaction validators and output guardrail tests. |
| FR-062 | Verified | Behavior contract imported into prompts/policy; tasks T139-T180 complete. |
| FR-063 | Verified | Agent topology in `agents.py` and real payload `current_agent` values. |
| FR-064 | Verified | Real matrix usage shows one model operation per normal turn except handoff silence. |
| FR-065 | Verified | Structured schema and real decision payloads include required fields. |
| FR-066 | Verified | Real `oi`/`bom dia` scenarios. |
| FR-067 | Verified | Real widget/site/Instagram/diagnostic CTA scenarios. |
| FR-068 | Verified | Diagnostic offer timing covered in behavior matrix and quality judge. |
| FR-069 | Verified | Cold greeting, unresolved/safety/handoff/waitlist scenarios block diagnostic where required. |
| FR-070 | Verified | Name policy tests and reliable/unreliable profile scenarios. |
| FR-071 | Verified | Output guardrail tests and repair/fallback tests. |
| FR-072 | Verified | Real OpenAI final behavior matrix `28/28` with saved transcripts. |
| FR-073 | Verified | Pricing table/cost tests and cost report. |
| FR-074 | Verified | Conversation state contract tests plus SQL state round-trip coverage. |
| FR-075 | Verified | LLM-first/template-controlled behavior validated by real transcripts and invariants. |
| FR-076 | Verified | Renderer tests and delivery eval. |
| FR-077 | Verified | Channel adapter/delivery tests. |
| FR-078 | Verified | Delivery matrix `20/20`; runtime delivery eval `10/10`. |
| FR-079 | Verified | Diagnostic ledger/progression tests. |
| FR-080 | Verified | Diagnostic no-repeat tests. |
| FR-081 | Verified | Invalid JSON repair/no-state-advance test. |
| FR-082 | Verified | Idempotency tests and WhatsApp duplicate webhook harness. |
| FR-083 | Verified | Conversation ordering test. |
| FR-084 | Verified | Handoff tests, Sales Inbox handoff route, real second-turn silence. |
| FR-085 | Verified | Product source version/key persistence checks. |
| FR-086 | Verified | Safety/prompt-injection/sensitive/unsupported media real scenarios and templates. |
| FR-087 | Verified | Sales Inbox completeness eval `14/14`; contract projection fields. |
| FR-088 | Verified | Zero-cost gates `6/6` plus underlying Python/eval/completion-evidence/build tests. |
| FR-089 | Verified | Real OpenAI runner caps for scenarios/model calls/cost/dry-run/stop-on-failure. |
| FR-090 | Pending external gate | Product-owner transcript review T205 is pending and can only approve after T211-T226 evidence is available. |
| FR-091 | Verified | Product follow-up delta implemented without reopening protected flows; regression tests and real delta matrix passed. |
| FR-092 | Verified | `product.how_it_works_direct`, runtime contract tests, and real OpenAI `product-delta-how-it-works` pass. |
| FR-093 | Verified | `test_product_knowledge.py` covers all added product knowledge keys. |
| FR-094 | Verified | `_product_knowledge_keys_for_prompt` selective retrieval tests and real source-key reports. |
| FR-095 | Verified | Runtime prompt compaction includes `post_diagnostic_context`; regression tests cover saved context use. |
| FR-096 | Verified | Post-diagnostic follow-up regression test verifies no diagnostic restart/repeat. |
| FR-097 | Verified | Runtime contract maps new LLM-selected normalized intents to product-followup templates and source keys. |
| FR-098 | Verified | Product-followup behavior remains LLM-first; deterministic code is limited to contract repair/guardrails after LLM output. |
| FR-099 | Verified | Template registry, renderer, and real delta reports cover all new product-followup templates. |
| FR-100 | Verified | Output guardrails and quality checks block lay-lead CRM wording where not directly asked. |
| FR-101 | Verified | Integration/WhatsApp scope template and real OpenAI integration scenario avoid unsupported setup/integration promises. |
| FR-102 | Verified | Security/data template, validator fixes, and real OpenAI security scenario avoid unsupported LGPD/security claims and sensitive-data capture. |
| FR-103 | Verified | Out-of-profile template and real OpenAI student scenario qualify gently without diagnostic/waitlist. |
| FR-104 | Verified | Diagnostic-refusal contract and real OpenAI refusal scenario answer price without reoffering diagnostic. |
| FR-105 | Verified | Full runtime tests, delivery eval, Sales Inbox eval, invariants, and zero-cost gates passed after the delta. |
| FR-106 | Verified | Product-followup templates and guardrails enforce Pilates-studio-owner language and block technical SaaS language. |
| FR-107 | Verified | Real OpenAI product-followup delta report includes model usage/cost for all six commercial scenarios. |

## Success Criteria

| ID | Status | Primary evidence |
| --- | --- | --- |
| SC-001 | Verified | `agent-runtime-invariants.json`; real OpenAI matrix uses runtime/model decisions. |
| SC-002 | Verified | Product knowledge eval and real product transcripts. |
| SC-003 | Verified | Invariant/product evals and real behavior matrix. |
| SC-004 | Verified | Quality judge directness; real direct-question scenarios. |
| SC-005 | Verified | Transcript quality judge `32/32`, matrix average `4.96/5`. |
| SC-006 | Verified | Thin diagnostic and no-fake-certainty tests. |
| SC-007 | Verified | Handoff evals and real second-turn silence. |
| SC-008 | Verified | Idempotency tests and local WhatsApp webhook harness. |
| SC-009 | Verified | Waitlist tests and Sales Inbox projection. |
| SC-010 | Verified | Cost eval and cost cap tests. |
| SC-011 | Verified | Sales Inbox completeness eval `14/14`. |
| SC-012 | Verified | `/pilates` baseline docs and no intentional visual changes. |
| SC-013 | Pending external gate | Local HTTP WhatsApp smoke passed and deploy preflight is documented; live Meta/Dualhook smoke T135 pending. |
| SC-014 | Pending external gate | Product-owner decision is pending in `product-owner-transcript-review.md`. |
| SC-015 | Verified | Redaction/output guardrail tests. |
| SC-016 | Verified | Real OpenAI behavior matrix `28/28`. |
| SC-017 | Verified | Real cold greeting scenarios. |
| SC-018 | Verified | Direct-question checks in real matrix and quality judge. |
| SC-019 | Verified | Real-provider reports contain visible transcripts, route, policy checks, usage/cost. |
| SC-020 | Verified | Quality judge `32/32`, average `4.96/5`, no scenario below `4.0`, blocking failures `0`. |
| SC-021 | Verified | Template IDs in real transcripts and template registry tests. |
| SC-022 | Verified | Delivery eval and message delivery matrix. |
| SC-023 | Verified | Diagnostic ledger/completion tests. |
| SC-024 | Verified | Diagnostic no-repeat tests. |
| SC-025 | Verified | Waitlist contract/timing tests and real scenarios. |
| SC-026 | Verified | Name policy tests and reliable/unreliable profile scenarios. |
| SC-027 | Verified | LLM output repair test. |
| SC-028 | Verified | Idempotency/order tests and duplicate webhook harness. |
| SC-029 | Verified | Sales Inbox completeness eval `14/14`. |
| SC-030 | Pending correction implementation | New final diagnostic staged-shape criterion; covered by tasks T212, T218, T219, T224. |
| SC-031 | Pending correction implementation | New blocked-old-copy criterion; covered by tasks T213, T218, T224. |
| SC-032 | Pending correction implementation | New diagnostic feedback criterion; covered by tasks T211, T220, T224. |
| SC-033 | Pending correction implementation | New demo-history branch criterion; covered by tasks T214, T217, T224. |
| SC-034 | Pending correction implementation | New name-timing criterion; covered by tasks T215, T221, T224. |
| SC-035 | Verified historically | Real OpenAI dry-run/caps and final cost under `US$0.30`; must be rerun for the correction matrix before production approval. |
| SC-036 | Verified | Real OpenAI `product-delta-how-it-works` pass and regression tests treat "como funciona" as product route. |
| SC-037 | Verified | Post-diagnostic saved-context regression test passes without restarting diagnostic. |
| SC-038 | Verified | `no_crm_lay_copy` checks and output guardrails pass in product-followup delta. |
| SC-039 | Verified | Real OpenAI comparison scenario passes with no current-tool attack or unsupported migration promise. |
| SC-040 | Verified | Real OpenAI integration scenario passes and uses `product.integration_scope_direct`. |
| SC-041 | Verified | Real OpenAI security/data scenario passes and uses conservative official-fact copy. |
| SC-042 | Verified | Real OpenAI out-of-profile scenario passes without diagnostic or buyer treatment. |
| SC-043 | Verified | Real OpenAI diagnostic-refusal scenario passes with direct price answer and no diagnostic offer. |
| SC-044 | Verified | Protected tests, delivery, Sales Inbox, build, and delta cost cap passed after implementation. |
| SC-045 | Verified | Product-followup output guardrails block technical SaaS terms in lay-lead templates. |
| SC-046 | Verified | Real OpenAI product-followup delta JSON contains model usage/cost for all six non-operational product-followup scenarios. |

## Open Completion Gates

The requirements not fully complete now include both new correction implementation and external gates:

- Product Explanation And Follow-Up Delta implementation and retest: FR-091-FR-107, SC-036-SC-046, T232-T259 completed with real OpenAI delta `6/6`.
- Final diagnostic/demo/name correction implementation and retest: FR-034A-D, SC-030-SC-034, T211-T226.
- Product-owner transcript approval: FR-090, SC-014, T211-T226 evidence, T205, T157, T137.
- Production deploy/cutover: FR-016, FR-060, T132-T134.
- Live production WhatsApp smoke: FR-059, SC-013, T135.

These gates must remain open until the corresponding approval/deploy/smoke action actually happens.
