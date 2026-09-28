# T012-040/T012-041 Tool Commit Static Audit Slice

Status: started / partial on 2026-06-12.

## Scope

This no-cost slice strengthens the SDK static audit and contract gate for the
OpenAI Agents SDK tool boundary.

The covered invariant is:

- SDK `@function_tool` functions exposed during model reasoning must remain
  read-only or proposal-only.
- They must not commit, persist, deliver, enqueue, publish, or otherwise mutate
  production state during reasoning.
- Commit remains a validator/runtime operation after structured LLM action,
  validation, rendering, and trace creation.

This does not add public endpoint integration, public delivery, Sales Inbox UI,
checkout, multi-tenant behavior, `/pilates` changes, or paid OpenAI calls.

## Files

- `services/taliya-agent-runtime/tests/test_spec012_static_audit.py`
- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`

## Added Coverage

`test_t012_040_sdk_tools_cannot_commit_or_deliver_during_reasoning` parses
`tools.py` with Python AST and asserts:

- every `@function_tool` exposure is exactly one of the approved `get_*` or
  `propose_*` SDK tools;
- all exposed tool names start with `get_` or `propose_`;
- exposed tool bodies do not call explicit commit/persist/state-write or
  delivery functions such as `commit_state`, `persist_state`, `send_message`,
  `deliver_message`, `enqueue_message`, or `publish_message`.

The T012-041 contract gate now requires this audit anchor so the invariant does
not live only as an unanchored static test.

The same slice also tightened the T012-041 manifest so all current T012-040
static audit anchors are mandatory contract checks:

- commercial regex-brain block;
- SDK tools read-only/proposal-only boundary;
- SDK tools no commit/delivery during reasoning;
- no direct free-text SDK delivery fields;
- no isolated old-runner/public-fallback path;
- no public app import before flag/cutover;
- no hardcoded unsafe checkout, discount, availability, integration, security,
  or migration promises;
- external tracing disabled;
- trace export cannot claim public delivery.

## Validation

Commands run from `C:\Users\lucas\agentes-landing-system`:

```powershell
python -m pytest services/taliya-agent-runtime/tests/test_spec012_static_audit.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py -q
```

Result: 11 passed.

```powershell
python -m pytest services/taliya-agent-runtime/tests -k spec012 -q
```

Result: 232 passed, 716 deselected.

```powershell
python -m ruff check services/taliya-agent-runtime/tests/test_spec012_static_audit.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py
```

Result: all checks passed.

## Anti-Determinism Review

This slice is static contract enforcement only. It does not inspect lead text,
route commercial meaning, add keyword/regex intent shortcuts, choose prices,
choose demo/waitlist/diagnostic behavior, or render customer copy.

The LLM-first action contract remains unchanged: the LLM selects the structured
commercial action; deterministic code validates, resolves official facts,
renders approved templates, traces, and commits only after validation.

## Paid-Call Status

No paid OpenAI call was made. Cost: `$0`.

## Still Open

T012-040 and T012-041 remain open overall until final endpoint/runtime
integration, real-model golden transcripts, shadow/cutover evidence, and
product-owner approval are available.
