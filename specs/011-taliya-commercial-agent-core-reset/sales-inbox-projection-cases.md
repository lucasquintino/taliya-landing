# Sales Inbox Projection Cases: Spec 011 Taliya Commercial Core Reset

Status: binding projection contract for `T011-028`.

The machine-readable contract lives in
`sales-inbox-projection-cases.json`.

## Purpose

Sales Inbox is a projection. It is not a second conversation brain.

The current Sales Inbox work is useful and should not be thrown away. Existing
fields such as `LeadRecord`, `QualificationDraft`, `agentRuntime`,
`crmAgentDiagnostic`, `commercialStage`, `diagnosticStatus`, `waitlistStatus`,
`demoStatus`, `summary`, and `nextAction` are treated as the seed projection.

The reset adds a stricter rule: for each commercial case family, the projection
must say which current_field is reused, what source_of_truth owns the value, and
whether the current field is enough.

## Status Values

- `reuse`: the current field can be kept as-is for the case contract.
- `reuse_with_validator`: the current field is useful, but must be populated from
  validated runtime state, conductor decision, trace, ledger, product knowledge,
  or operator state.
- `missing`: the current projection does not expose enough structured evidence
  yet; implementation must add or derive it later.

The default expectation is reuse with stricter validation. New fields are added
only when the current projection cannot prove correctness.

## Source Of Truth

Allowed source owners are:

- `turn_gate`
- `validated_conductor_decision`
- `validated_runtime_state`
- `diagnostic_ledger`
- `official_product_knowledge`
- `spec_006_product_contract`
- `delivery_outbox`
- `trace_store`
- `operator_state`
- `channel_metadata`
- `none_forbidden`

`none_forbidden` is used for things Sales Inbox must not project, such as a price
being saved as student count, internal source labels leaking to customer-facing
text, or a waitlist state appearing without clear intent.

## Current Reuse Policy

The current agent projection does serve as a base:

- `LeadRecord` remains the operator-facing aggregate.
- `QualificationDraft` remains a compatibility layer while the new projection is
  introduced.
- `agentRuntime` remains the compatibility home for runtime trace fields.
- `SalesInboxClient` can continue displaying existing fields.

But these fields cannot be trusted blindly:

- adapter inference cannot become reliable memory without source/confidence
  labels;
- string fields such as `agentRuntime.templateIds` or
  `agentRuntime.productSourceKeys` need validator-backed trace evidence;
- completed diagnostic requires per-key ledger evidence, not just a status;
- waitlist requires intent evidence;
- product claims require official product knowledge or Spec 006;
- every meaningful turn needs trace/model/validator/projection evidence before
  eval PASS.

## Case Families

The JSON contract covers the families required by `sales-inbox-contract.md` and
Spec 011 regression cases:

- cold greeting;
- source opening;
- price and plan-fit;
- pain-first;
- diagnostic in progress and completed;
- demo states;
- post-diagnostic follow-up;
- buying intent and waitlist states;
- handoff and human pause;
- duplicate webhook/deferred inbound;
- invalid JSON/provider fallback;
- unsupported media;
- product how-it-works;
- comparison/current tool;
- WhatsApp and integration scope;
- security/data;
- out of profile;
- diagnostic refusal.

Future projection implementation must satisfy this matrix. A transcript that
looks good but fails this projection contract is not green.
