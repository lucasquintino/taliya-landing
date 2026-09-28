# Coverage Map - Spec 012

Purpose: prove that every planned behavior and architecture guarantee has an owner, task, and evidence requirement.

No task may be considered done if it leaves a P0/P1 requirement without evidence.

## Coverage Rules

- Every preserved Spec 010/011 contract must map to an SDK agent, tool, guardrail, validator, renderer, persistence rule, eval, or manual review.
- Agent instructions can guide behavior, but P0/P1 rules also need validator, renderer, static audit, eval, or trace evidence.
- Every implementation task must update this map when it creates, removes, or changes an owner.
- A release gate cannot pass with missing owner, missing evidence, or `Not covered`.

## Revision 2026-06-10 (D-012-012) - New Owners And Rows

Architecture owners added by the action-first revision:

| Requirement | Primary owner | Required task | Evidence required |
| --- | --- | --- | --- |
| Deterministic board before the model | Turn Situation Builder | T012-030B | Situation record in trace: mode, pending key, allowed actions. |
| Model returns only ConductorActionDecision | Strict output schema | T012-030A | Schema rejects template plans/state/official variables. |
| Staged delivery and official variables derived by code | Decision Compiler | T012-030C | Compiler tests: full staged sequence from a single completed-diagnostic action. |
| Composition variables validated (action rejected without them) | Validators | T012-032 | T011-105 lesson: action without pain_context_human must fail, not fallback. |

Behavioral rows previously missing:

| Behavior | Primary owner | Secondary owner | Required evidence |
| --- | --- | --- | --- |
| Answer adequacy (price answer contains the price) | Validator (port `price_question_missing_price_answer`) | judge eval | Price question answered with a priced template, mid-diagnostic included. |
| Conversation-state tracking owned by code | Situation Builder/ledger | stale-question scrub | Model never re-raises answered questions (spike: 5 resurrections). |
| Answer correction ("na verdade sao 80") | Diagnostic ledger merge (compiler) | fixtures T012-038B | Ledger updates, no re-ask, no contradiction. |
| Multiple answers in one message | LLM captured_slots + compiler merge | fixtures T012-038B | Both slots recorded in one turn. |
| Messy real-world input | LLM interpretation | fixtures T012-038B | Typos/slang/abbreviations interpreted correctly. |
| Voice rules (anti-parrot, no repeated greeting, banned phrases) | Voice validators | judge eval | T012-032 checks block; judge confirms naturalness. |

## Architecture Coverage

| Requirement | Primary owner | Required task | Evidence required |
| --- | --- | --- | --- |
| Agents SDK owns orchestration | SDK runner/agents | T012-020, T012-030 | SDK run trace shows agent path/handoffs/tools. |
| No custom action-first conductor | Static audit/import graph | T012-037, T012-040 | Audit blocks old conductor/DecisionCompiler as public SDK brain. |
| Structured proposal before validation | SDK output adapter | T012-010, T012-023, T012-032 | Contract tests reject free-form direct response. |
| Validators after SDK | Validator adapter | T012-024, T012-032 | Mocked failures block render/persist/delivery. |
| Approved renderer only | Renderer adapter | T012-024, T012-033 | Tests prove no direct SDK text delivery. |
| Proposal-only state updates | Tool catalog/runtime commit layer | T012-012, T012-022, T012-036 | Tool classification tests and trace show no reasoning-time commits. |
| Explicit RAG/product knowledge layer | RAG policy and product tools | T012-019, T012-022 | Product claims map to fact refs/source ids and retrieval does not route commercial turns. |
| Sales Inbox as projection | Projection adapter | T012-035, T012-046 | Projection export matches validated state/events. |
| Widget/WhatsApp shared core | Runtime adapters | T012-031, T012-036 | Integration tests use same SDK core with channel formatting only. |
| No protected `/pilates` drift | Git diff/static review | Every task | Protected diff check is recorded in ledger. |

## Behavioral Coverage

| Behavior | Primary owner | Secondary owner | Required evidence |
| --- | --- | --- | --- |
| Direct question first | Product/Diagnostic agents | validator, golden eval | Real-model and mocked scenarios show answer before steering. |
| Pain-first context reuse | Triage/Product agents | manual review, golden eval | Lead terms are reused naturally without internal labels. |
| Price/student separation | Product/Diagnostic agents | product/numeric validator | `497` is price, not student count. |
| Diagnostic required fields | Diagnostic agent | diagnostic validator | Urgency and other mandatory keys are complete before final diagnostic. |
| One diagnostic question at a time | Diagnostic agent | renderer/validator | Eval rejects multi-question diagnostic turns. |
| Accept simple numeric answers | Diagnostic agent | diagnostic ledger validator | `120` updates student count and continues. |
| No repeated questions | Diagnostic agent | state/validator | Long diagnostic transcript proves ledger-aware next question. |
| Final diagnostic quality | Diagnostic agent | approved renderer/manual review | Final output is complete, practical, and not cut off. |
| WhatsApp product scope | Product agent | product knowledge validator | Official answer states Taliya-owned scope without client/studio connection. |
| Demo request handling | Product agent | demo proposal/state | Demo interest is persisted and answered naturally. |
| Waitlist only after clear intent | Waitlist agent | waitlist validator | Curiosity does not become waitlist; clear buying intent can. |
| Human handoff pauses AI | Handoff agent | turn gate/runtime state | Automation suppresses replies until explicit resume. |
| Delivery concurrency | Turn gate/outbox | mocked integration | Inbound during chunks is deferred behind current response. |
| No internal leaks | Context/output adapter | leak validator | Phrases like internal source/profile labels are blocked. |
| Sales Inbox consistency | Projection adapter | projection validator | Inbox fields match validated conversation state. |

## Release Coverage

| Gate | Required before | Evidence |
| --- | --- | --- |
| Phase 0 decisions recorded | Any SDK code | `decision-log.md` |
| Design lock complete | Isolated spike | `design-lock.md`, `tool-catalog.md`, `trace-map.md`, `coverage-map.md`, `static-anti-drift-audit.md`, `rag-policy.md` |
| Mocked spike green | Paid spike | mocked contract report |
| Paid spike approved and passed | SDK core implementation | paid run report with usage/cost |
| Static audit green | Shadow mode | audit report |
| Golden/do-not-do green | Public activation | eval report |
| Shadow mode green | Public activation | shadow comparison report |
| Rollback proof green | Public activation | rollback evidence |
| Product-owner approval | Public activation | approval log entry |
