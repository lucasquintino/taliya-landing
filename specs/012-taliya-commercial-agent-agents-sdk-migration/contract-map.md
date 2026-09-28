# Contract Map - Spec 011 To Spec 012 SDK Architecture

Purpose: prevent Spec 012 from losing the behavior already defined by Spec 010/011.

## Mapping Rules

- Every preserved behavior must have exactly one primary owner and may have secondary enforcement.
- Agent instructions may express policy, but cannot be the only enforcement for P0/P1 requirements.
- Tools provide facts or proposals, not unchecked final authority.
- Validators remain required for hard business rules.
- Renderer remains required for approved customer-facing language.
- Evals remain required for behavior quality.

## Contract Mapping

| Preserved requirement | Primary Spec 012 owner | Secondary owner |
| --- | --- | --- |
| LLM-first commercial understanding | SDK agents and handoffs | static audit, evals |
| Direct question answered first | SDK agent instructions and output schema | validator, golden transcripts |
| Diagnostic ledger required keys | Diagnostic Agent and proposal tools | diagnostic validator, Sales Inbox projection |
| One diagnostic question at a time | Diagnostic Agent | validator, renderer gate |
| Accept simple answer like "120" | Diagnostic Agent | numeric/diagnostic validator |
| No repeated diagnostic question | Diagnostic Agent | diagnostic validator, state |
| Final diagnostic staged order | Diagnostic Agent proposal | renderer, diagnostic validator |
| Natural studio-owner language | agent instructions and templates | banned phrase validator, manual review |
| Price/product facts official only | product knowledge tools | product claim validator |
| 497 is price, not students | Product/Diagnostic Agents | numeric validator |
| WhatsApp scope answer | Product Agent | product knowledge validator |
| Demo/product-demo state | Product Agent and demo proposal | state persistence, renderer |
| Waitlist only after clear intent | Waitlist Agent | waitlist validator |
| Human request pauses AI | Handoff Agent | turn gate, runtime state |
| Internal labels not renderable | Context Builder | leak validator, renderer |
| Sales Inbox is projection | Persistence/projection | projection validator |
| Widget/WhatsApp same core | Runtime API/adapters | integration tests |
| No old TS fallback | static audit | endpoint tests |
| No `runtime/runner.py` brain | static audit | import graph tests |
| No free-form whole response variable | SDK output schema | template registry validator |
| No product facts in prompts/templates | product governance audit | static audit |
| Cost must include model usage | SDK trace/usage | eval report contract |
| Golden/do-not-do required | eval harness | manual approval |

## Current Spec 011 Elements To Preserve

Preserve as-is or adapt narrowly:

- regression fixtures;
- golden transcript scenario definitions;
- do-not-do fixture categories;
- product knowledge fixtures;
- template registry concept;
- renderer channel rules;
- Sales Inbox expected projection fields;
- trace/export report shape;
- static audit forbidden categories;
- protected `/pilates` no-drift gate;
- rollback rule that does not restore legacy commercial brain.

## Current Spec 011 Elements To Replace

Replace in the normal SDK path:

- `ConductorActionDecision` as the main model output;
- `TurnSituation.allowed_actions` as the central commercial constraint;
- `DecisionCompiler` as state/render brain;
- action-level repair as primary recovery;
- custom provider request/response wrappers as the main agent framework;
- simulated specialist role fields when SDK agents/handoffs can express real roles.

## Required New Contracts

Spec 012 needs these new contracts before implementation:

- `TaliyaTurnProposal` schema.
- SDK tool side-effect classification.
- SDK agent handoff graph.
- SDK trace-to-Taliya-trace mapping.
- SDK output validation adapter.
- SDK spike pass/fail rubric.
- SDK cost budget policy.
- SDK privacy/tracing policy.
