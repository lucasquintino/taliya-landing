# T012-022 Evidence - SDK Read-Only And Proposal-Only Tools

## Scope Completed

Implemented SDK-callable tools from the Spec 012 tool catalog:

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/tools.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/agents.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/__init__.py`
- `services/taliya-agent-runtime/tests/test_spec012_sdk_agents.py`

Read-only tools:

- `get_product_knowledge`
- `get_spec006_product_contracts`
- `get_diagnostic_ledger`
- `get_conversation_summary`
- `get_demo_waitlist_handoff_state`
- `get_approved_template_catalog`

Proposal-only tools:

- `propose_diagnostic_update`
- `propose_waitlist_update`
- `propose_demo_state_update`
- `propose_handoff`
- `propose_template_plan`
- `propose_sales_inbox_projection`

Commit tools exposed to SDK reasoning: none.

## Proof Type

Mocked/no-cost isolated spike.

## Tests And Checks

From `services/taliya-agent-runtime`:

```text
python -m pytest tests\test_spec012_sdk_agents.py tests\test_spec012_sdk_spike_isolation.py -q
..........                                                               [100%]
10 passed in 1.82s

python -m ruff check app\core\taliya_commercial_sdk tests\test_spec012_sdk_agents.py tests\test_spec012_sdk_spike_isolation.py
All checks passed!
```

## Tool Evidence

- Tools are declared with Agents SDK `function_tool`.
- Tool inputs use strict JSON-compatible schemas; open `dict[str, Any]` tool inputs were avoided.
- Read-only tools return envelopes with `side_effect_class="read_only"` and `commits_state=false`.
- Proposal-only tools return envelopes with `side_effect_class="proposal_only"`, `validation_required=true`, and `commit_after_validation_only=true`.
- Product facts come from official product knowledge and Spec 006 product contract builders.
- Template catalog reads metadata only and does not render final copy.
- Agent manifests now expose tool names, and real SDK `Agent` instances receive SDK tool objects.

## Anti-Determinism Review

No regex, token list, raw-text route parser, action compiler, or deterministic commercial shortcut was added. Tools do not parse lead text to decide price, demo, diagnostic, waitlist, pain-first, objection, or mixed intent. They only read official facts/snapshots or return non-committed proposals chosen by the SDK model.

## Protected Scope Review

No `/pilates`, landing visual, Sales Inbox UI, multi-tenant, client/studio WhatsApp, or checkout files were modified by this task.

## Paid-Call Status

No paid OpenAI call was run. Tools were instantiated and invoked locally through mocked/no-cost tests only; no `Runner.run` call was executed.

## Open Risks

T012-023 must define the strict `TaliyaTurnProposal` adapter so tool and run outputs cannot become direct customer-facing delivery. Runtime state reads are snapshot-based in the isolated spike; production state access remains blocked until later integration tasks.

## Next Task Lock

Next allowed task: T012-023 implement SDK output adapter to `TaliyaTurnProposal`.
