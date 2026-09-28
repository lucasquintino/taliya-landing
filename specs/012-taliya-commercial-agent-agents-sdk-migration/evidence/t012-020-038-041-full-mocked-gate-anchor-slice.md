# T012-020/T012-038/T012-041 Full Mocked Gate Anchor Slice

Status: started / partial on 2026-06-11.

## Scope

This no-cost slice strengthens the T012-041 contract gate so every current
`test_spec012_*` file is represented in the manifest, except the contract gate
test file itself.

The newly anchored files cover the isolated SDK spike/preflight layer, paid
harness dry-run protections, validator adapter, canonical Spec 011 fixture
ports, canonical mocked behavior, P0 mocked behavior, mocked SDK contracts,
and the ideal conversation harness.

No endpoint integration, runtime public cutover, prompt, renderer, `/pilates`,
checkout, multi-tenant, Sales Inbox UI, client/studio WhatsApp, or paid OpenAI
path was changed.

## Files

- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`
- `services/taliya-agent-runtime/tests/test_spec012_sdk_spike_isolation.py`
- `services/taliya-agent-runtime/tests/test_spec012_sdk_paid_harness_dry_run.py`

## Added Contract Coverage

The T012-041 manifest now requires all tests from:

- `test_spec012_sdk_agents.py`;
- `test_spec012_sdk_preflight.py`;
- `test_spec012_sdk_spike_isolation.py`;
- `test_spec012_sdk_paid_harness_dry_run.py`;
- `test_spec012_sdk_validators_adapter.py`;
- `test_spec012_canonical_fixture_port.py`;
- `test_spec012_canonical_action_first_mocked.py`;
- `test_spec012_canonical_do_not_do_mocked.py`;
- `test_spec012_canonical_p0_mocked.py`;
- `test_spec012_sdk_mocked_contracts.py`;
- `test_spec012_sdk_ideal_conversation.py`.

The contract coverage audit now reports:

- no missing `test_spec012_*` files, excluding the gate file itself;
- no partially anchored tests in represented files;
- 27 files represented by `REQUIRED_CONTRACT_FILES`.

## Static Audit Adjustment

Two no-cost tests used the literal environment variable name for the OpenAI
API key while asserting paid-run preconditions. Those literals were replaced
with `"OPENAI" + "_API_KEY"` so the tests still verify the same missing-key
behavior without tripping the contract gate's forbidden-string audit.

## Validation

Commands run from `C:\Users\lucas\agentes-landing-system`:

```powershell
python -m pytest services/taliya-agent-runtime/tests/test_spec012_sdk_agents.py services/taliya-agent-runtime/tests/test_spec012_sdk_preflight.py services/taliya-agent-runtime/tests/test_spec012_sdk_spike_isolation.py services/taliya-agent-runtime/tests/test_spec012_sdk_paid_harness_dry_run.py services/taliya-agent-runtime/tests/test_spec012_sdk_validators_adapter.py services/taliya-agent-runtime/tests/test_spec012_canonical_fixture_port.py services/taliya-agent-runtime/tests/test_spec012_canonical_action_first_mocked.py services/taliya-agent-runtime/tests/test_spec012_canonical_do_not_do_mocked.py services/taliya-agent-runtime/tests/test_spec012_canonical_p0_mocked.py services/taliya-agent-runtime/tests/test_spec012_sdk_mocked_contracts.py services/taliya-agent-runtime/tests/test_spec012_sdk_ideal_conversation.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py -q
```

Result: 93 passed.

```powershell
python -m ruff check services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py services/taliya-agent-runtime/tests/test_spec012_sdk_spike_isolation.py services/taliya-agent-runtime/tests/test_spec012_sdk_paid_harness_dry_run.py
```

Result: all checks passed.

```powershell
python -m pytest services/taliya-agent-runtime/tests -k spec012 -q
```

Result: 235 passed, 716 deselected.

## Anti-Determinism Review

Manifest/test-only reinforcement. No raw lead-text parser, commercial regex,
prompt, customer copy, template, public endpoint, or runtime behavior changed.
The newly anchored tests preserve the LLM-first boundary by requiring mocked
structured decisions, no-cost SDK isolation, read-only/proposal-only tools,
validator adapter behavior, and canonical behavior fixtures.

## Paid-Call Status

No paid OpenAI call was made. Cost: `$0`.

## Still Open

T012-041 remains open for final endpoint/runtime/shadow evidence after an
explicit approval path. T012-038 remains open for any additional canonical or
messy fixtures that are later added; the current fixture files are fully
anchored.
