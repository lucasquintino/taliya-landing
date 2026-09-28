# Implementation Source Discipline - Spec 012

Purpose: prevent drift while implementing the Taliya commercial agent migration.

This file is mandatory working discipline for every remaining Spec 012
implementation slice.

## Core Rule

No source, no implementation.

Every behavior change must cite at least one authoritative source before code
changes are accepted:

- Spec 010 binding contract;
- Spec 011 binding contract;
- `conformity-matrix.pt-BR.md`;
- existing Spec 011 test or fixture;
- official template registry / renderer contract;
- existing runtime validator behavior;
- explicit product-owner decision recorded in Spec 012.

If no source exists, record the item as a gap or pending decision. Do not encode
it as product truth.

## Required Per-Slice Checklist

Before editing code:

1. Identify the task id, e.g. `T012-032`.
2. Identify the exact behavior being ported.
3. Identify the source file and rule/test/fixture proving the behavior.
4. Confirm the change stays inside the allowed scope.
5. Confirm it does not reintroduce regex/state-machine/template-first
   commercial routing.

During implementation:

1. Add or update a Spec 012 test that fails without the port.
2. Keep deterministic code limited to form, validation, compilation,
   official-fact grounding, state, safety, delivery, cost, or trace boundaries.
3. Do not make deterministic code infer commercial meaning from raw lead text.
4. Do not alter `/pilates`, landing visuals, Sales Inbox UI, checkout,
   multi-tenant, or client/studio WhatsApp.
5. Do not run paid OpenAI calls without explicit approval and budget.

Before closing a slice:

1. Run the relevant focused tests.
2. Run `python -m pytest tests\ -k spec012 -q`.
3. Run `python -m ruff check app\core\taliya_commercial_sdk` and include any
   new Spec 012 tests in the ruff target if needed.
4. Write evidence under `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/`.
5. Update `implementation-ledger.md` with:
   - source references;
   - files changed;
   - tests run;
   - proof type;
   - anti-determinism review;
   - protected-scope result;
   - paid-call status;
   - next task lock.

## Explicit Non-Goals

Do not use this discipline to freeze useful engineering judgment. It prevents
inventing product behavior; it does not prevent:

- adapting an existing validator to the action-first shape;
- adding tests that prove an existing rule in the new architecture;
- refactoring glue code when behavior is preserved;
- adding operational/safety boundaries already allowed by AGENTS.md and
  `taliya-llm-first-agent`.

## Ambiguity Handling

When a behavior is plausible but not sourced:

1. Add it to the evidence file or ledger as `pending product-owner decision`.
2. Do not implement it as a hard validator.
3. If needed for local experimentation, keep it behind test-only fixtures or
   comments clearly marked non-binding.

Known pending decisions include:

- official plan recommendation derivation from diagnostic facts;
- whether "como funciona o diagnostico?" after acceptance starts diagnostic or
  answers a product/process question.

## Review Question

Every final summary for implementation work should be able to answer:

> Which source made each behavior change legitimate?

If the answer is unclear, the slice is not closed.
