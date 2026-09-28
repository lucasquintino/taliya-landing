# Template Variable Registry: Spec 011 Taliya Commercial Core Reset

Status: binding governance note for `T011-025`.

The machine-enforced registry lives in
`services/taliya-agent-runtime/app/core/taliya_commercial/template_registry.py`.
This document explains the rule it enforces.

## Rule

Templates are approved voice. Variables are not a loophole for free-form
assistant responses.

Every customer-facing variable must have:

- a registered name;
- a declared kind;
- allowed grounding sources;
- a maximum length or an enum/url shape;
- a validation rule;
- an approved template id where it can appear.

Any unregistered template id, unregistered variable, wrong variable kind, wrong
source, or over-broad max length must fail before rendering.

## Important Choices

- `contextual_next_step` is registered as an `enum`, not as long text. The
  renderer should own the approved copy for each allowed meaning.
- `first_name` may use `channel_metadata` only as a typed variable with evidence
  that it is a verified real person first name. Internal reliability labels,
  studio names, handles, phone numbers, and random profile values remain
  non-renderable.
- `plan_price_summary`, `recommended_plan_or_range`, `official_demo_link`, and
  `product_fact_summary` may only come from official product knowledge or Spec
  006 product contracts.
- Diagnostic final variables must be grounded in the diagnostic ledger and/or
  official product contracts. They cannot be hidden whole-message summaries.
- `product.general_objection_response` remains intentionally unregistered until
  eval evidence proves it is needed and product-owner review approves it.

## Validator Contract

The registry currently exposes:

- `TEMPLATE_REGISTRY`
- `VARIABLE_REGISTRY`
- `validate_template_registry()`
- `validate_render_plan_item_variables()`

Future renderer work must call registry validation before substituting customer
text. Future conductor work must produce `RenderPlanItem.variables` that conform
to this registry.

## Known Gaps

This closes the variable registry definition, not the renderer.

- `T011-070..T011-074` still need to implement rendering and channel chunk rules.
- Conditional variable rules still need validator implementation, for example
  `product.how_it_works_direct` with a diagnostic-delivered next-step variant
  must also include `recommended_area`.
- Template copy bodies are still governed by the preserved Spec 010 contracts
  and later renderer implementation.
