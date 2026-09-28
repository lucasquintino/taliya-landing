# Tool Catalog - Spec 012

Revision 2026-06-10 (spike evidence): state-read tools take no model-supplied
arguments - they read the snapshot from the SDK local run context
(`RunContextWrapper`), so the model never echoes state JSON.
`get_approved_template_catalog` returns full variable specs (kind, max_length,
allowed sources). The triage agent has NO tools (`tool_choice=required` pure
router). Under design-lock-v2, proposal tools become optional reasoning notes:
the final output carries the decision.

Purpose: prevent SDK tools from becoming hidden routers or unvalidated state mutators.

## Tool Classes

### Read-Only

Callable during SDK reasoning. Must not mutate state.

| Tool | Purpose | Allowed input | Forbidden behavior |
| --- | --- | --- | --- |
| `get_product_knowledge` | Read official product facts | fact keys, topic hints | invent facts, choose route from raw text |
| `get_spec006_product_contracts` | Read product contract constraints | contract keys | create new offers, dates, discounts |
| `get_diagnostic_ledger` | Read current diagnostic state | conversation id | mark fields complete |
| `get_conversation_summary` | Read compact memory | conversation id | promote inferred facts to reliable facts |
| `get_demo_waitlist_handoff_state` | Read operational state | conversation id | commit demo/waitlist/handoff |
| `get_approved_template_catalog` | Read available response families | route/family hint | render final response |

### Proposal-Only

Callable during SDK reasoning. May propose changes with evidence. Runtime commits only after validation.

| Tool | Purpose | Required evidence | Commit owner |
| --- | --- | --- | --- |
| `propose_diagnostic_update` | Propose ledger field update | lead message excerpt or state evidence | diagnostic commit layer |
| `propose_waitlist_update` | Propose waitlist status/details | explicit buying/next-step intent evidence | waitlist commit layer |
| `propose_demo_state_update` | Propose demo interest/status | explicit demo/product-demo signal | demo commit layer |
| `propose_handoff` | Propose human pause/escalation | lead request or policy reason | turn gate/runtime state |
| `propose_template_plan` | Propose approved template ids/variables | answer obligations and refs | renderer |
| `propose_sales_inbox_projection` | Propose projection fields | validated state/proposal refs | Sales Inbox projection |

### Commit-After-Validation

Not exposed to free SDK reasoning on normal commercial turns.

| Operation | Owner | Precondition |
| --- | --- | --- |
| commit diagnostic ledger | runtime persistence | proposal plus diagnostic validator pass |
| commit waitlist state | runtime persistence | proposal plus waitlist validator pass |
| commit demo state | runtime persistence | proposal plus product/demo validator pass |
| commit human pause/resume | turn gate/runtime controls | handoff validator or explicit runtime-control event |
| commit Sales Inbox projection | projection layer | validated state/event source |
| reserve delivery/outbox | delivery layer | render and state commit pass |

## Tool Invariants

- No tool may parse raw lead text with regex to decide price, demo, diagnostic, waitlist, pain-first, objection, or mixed intent.
- No tool may return a whole customer-facing response.
- Product retrieval tools must return fact refs/source ids for customer-facing product claims.
- No tool may ask for client/studio WhatsApp numbers.
- No tool may invent checkout links, discounts, launch dates, VIP access, or availability.
- No tool may mark inferred/channel metadata as reliable lead facts without evidence.
- Every proposal tool output must include evidence and uncertainty.
