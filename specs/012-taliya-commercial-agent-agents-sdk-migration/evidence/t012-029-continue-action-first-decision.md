# T012-029 Continue/Adapt/Abort Decision

Status: completed locally on 2026-06-15.

## Decision

Continue, with the action-first adaptation already adopted by D-012-012.

The migration should continue only on the Spec 012 action-first Agents SDK
path:

`Turn Situation Builder -> LLM ConductorActionDecision -> Decision Compiler -> validators -> renderer -> commit/delivery`.

The original template-first SDK spike boundary remains superseded and must not
be revived as the production target.

## Basis

This decision is based on `evidence/t012-028-sdk-vs-spec011-comparison.md` and
the current implementation ledger.

Key reasons:

- the original SDK spike proved SDK orchestration and model understanding but
  repeated the known T011-105 failure mode;
- action-first real-model validation delivered the staged final diagnostic
  that the template-first spike failed to deliver;
- the no-cost contract gate now anchors every current `test_spec012_*` file
  except the gate itself;
- remaining gaps are endpoint/runtime, persistence, real-model/shadow and
  approval gates, not a reason to abort the SDK migration.

## Authorized Next Work

The user's 2026-06-15 instruction, "pode seguir com autonomia maxima ate a
parte de custo pago", authorizes continuing no-cost implementation work until a
paid OpenAI call or another explicit approval gate is reached.

Allowed next:

- no-cost endpoint/runtime integration work behind a feature flag;
- local tests and static audits;
- local trace/projection/manual-review packages;
- docs, ledgers, and decision artifacts.

Still blocked without explicit approval:

- paid OpenAI runs;
- public cutover;
- shadow mode against production traffic;
- external trace export containing lead text;
- `/pilates` visual/layout/copy changes;
- Sales Inbox UI redesign;
- checkout, multi-tenant, or client/studio WhatsApp scope expansion.

## Next Task Lock

Proceed to T012-031/T012-036 in the narrowest no-cost form:

- integrate the action-first runner behind an off-by-default feature flag;
- prove current public behavior remains unchanged when the flag is off;
- prove HMAC/idempotency/turn-gate behavior is preserved;
- do not route real traffic to the SDK path;
- do not run paid OpenAI calls.

## Anti-Determinism Review

The decision does not authorize deterministic commercial routing. The
commercial brain remains the LLM returning structured action decisions. Runtime
code may only provide operational boundaries, official facts, compiler
expansion, validation, rendering, persistence, delivery, trace and cost control.

## Paid-Call Status

No paid OpenAI call was made. Cost: `$0`.
