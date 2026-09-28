# Contract: Product Knowledge

## Purpose

Product knowledge is the only official source for commercial claims.

## Required Scope

Initial scope:

```text
scope = taliya_commercial
```

## Required Fields

- `source_key`
- `version`
- `last_reviewed_at`
- `plans`
- `prices`
- `plan_comparison`
- `links`
- `demo_status`
- `waitlist_status`
- `checkout_status`
- `availability`
- `cancellation_or_guarantee_policy`
- `privacy_or_data_notes`
- `unsupported_claims`

Product-followup delta required fields:

- `how_it_works`
- `routine_areas`
- `whatsapp_scope`
- `integration_scope`
- `comparison_spreadsheet`
- `comparison_management_system`
- `security_and_data`
- `availability_and_onboarding`
- `out_of_profile`

## Provisional Official Links

Until product owner changes the source:

- Plans page: `/pilates/planos`
- Demo/commercial page path: `/pilates/planos/demonstracao`
- Demo/commercial absolute URL for WhatsApp: `https://www.taliya.com.br/pilates/planos/demonstracao`
- Waitlist: internal database action, no invented public link
- Checkout: unavailable unless explicitly added to product knowledge

## Tool Behavior

`get_product_knowledge` must:

- accept a query or requested keys
- return only official facts
- return missing facts explicitly
- include `source_version`
- include unsupported claims when relevant
- support selective retrieval for product explanation, post-diagnostic follow-up, comparison, integration/scope, security/data, availability/onboarding, and out-of-profile questions
- avoid returning all product-followup fact groups on unrelated turns

## Guardrail Behavior

Output validation must block delivery when:

- a product claim lacks source version
- a price differs from official source
- a link is not present in official source
- checkout is implied while unavailable
- the agent promises availability that is not official
- an integration, setup, migration, mass-message, security, LGPD, certification, encryption, audit, or data-access claim is not present in official product knowledge
- "CRM" is used as lay-lead persuasion outside the allowed cases defined in `product-followup-delta-contract.md`

## Review Policy

Any pricing, link, availability, or demo change must update product knowledge before prompts, tools, eval fixtures, or UI copy depend on it.

Any claim about how Taliya works, WhatsApp Business scope, routine areas, integrations, comparison with current tools, security/data, onboarding, or out-of-profile fit must also be added to product knowledge before prompts, templates, or eval fixtures depend on it.
