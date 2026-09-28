# T012-033 Slice - Renderer Over Compiler Render Plans

Date: 2026-06-11

## Scope

Advanced T012-033 with no-cost proof that the approved renderer accepts
compiler-owned render plans after action-first validation.

Covered:

- diagnostic-entry name question from compiler -> validator -> renderer;
- `product.how_it_works_direct` with compiler-owned `contextual_next_step`
  enum variable;
- staged final diagnostic render plan with compiler-owned official facts,
  diagnostic compositions, and WhatsApp chunk policy.

This is isolated-core proof. It does not add public endpoint cutover.

## Sources

- `specs/012-taliya-commercial-agent-agents-sdk-migration/tasks.md`
  - T012-033 adapts the approved renderer to the compiler's render plan.
- `specs/012-taliya-commercial-agent-agents-sdk-migration/spec.md`
  - FR-012-043/044 require bounded template variables and renderer failure
    instead of generic semantic defaults.
- `specs/012-taliya-commercial-agent-agents-sdk-migration/conformity-matrix.pt-BR.md`
  - maps channel chunking and renderer rules to T012-033.
- `.agents/skills/taliya-llm-first-agent/SKILL.md`
  - renderer is a guardrail/rendering layer after the LLM chooses the action.

## Files Changed

- `services/taliya-agent-runtime/tests/test_spec012_renderer_compiler.py`

## Behavior Proved

The new tests compile structured `ConductorActionDecision` objects and then
validate/render the resulting `CompiledTurn` through `validate_compiled_turn`.

Proof points:

- `ask_name_at_diagnostic_entry` renders exactly the approved
  `diagnostic.ask_name_at_entry` copy;
- `answer_how_it_works` renders `product.how_it_works_direct` with the
  compiler-owned enum `contextual_next_step`;
- `complete_diagnostic` renders the staged final diagnostic with
  `staged_diagnostic` chunk policy and no renderer-level generic fallback.

## Tests

Run from `services/taliya-agent-runtime`:

- `python -m pytest tests\test_spec012_renderer_compiler.py -q`
  - result: 3 passed
- `python -m pytest tests\ -k spec012 -q`
  - result: 206 passed, 716 deselected
- `python -m ruff check tests\test_spec012_renderer_compiler.py`
  - result: all checks passed

## Anti-Determinism Review

No lead-text parser, regex, routing shortcut, or new customer-facing runtime
branch was added. Tests feed mocked structured decisions to the compiler and
prove the renderer accepts only the validated compiler plan.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout, multi-tenant, public
endpoint, or client/studio WhatsApp files were edited.

## Paid Calls

None.

## Still Open

T012-033 can be considered closed for the isolated core, but endpoint/channel
delivery integration still belongs to T012-031/T012-036 and final verification
belongs to Phase 4.
