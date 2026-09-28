# T012-028 SDK vs Spec 011 Comparison

Status: completed locally on 2026-06-15.

## Scope

This no-cost comparison decides whether the Spec 012 Agents SDK path should
continue after the isolated spike and action-first correction, using only local
evidence already present in the repository.

No OpenAI call was made for this comparison. No endpoint, `/pilates`, checkout,
Sales Inbox UI, multi-tenant, client/studio WhatsApp, or public cutover file was
changed.

## Compared Paths

| Path | Role in this comparison | Current verdict |
| --- | --- | --- |
| Spec 011 public/runtime path | Binding behavior source and current fallback baseline, not the final motor | Preserve contracts, validators, renderer and fixtures; do not keep as the new commercial brain. |
| Spec 012 original SDK spike | Proved SDK orchestration and model understanding, but used the wrong LLM-template boundary | Superseded by action-first because it repeated the T011-105 failure mode. |
| Spec 012 action-first SDK path | Target production architecture | Continue implementation behind feature flag; it matches the binding `011/action-contract.md` shape. |

## Executive Result

Continue the Spec 012 migration, but only on the action-first architecture:

`Turn Situation Builder -> LLM ConductorActionDecision -> Decision Compiler -> validators -> renderer -> commit/delivery`.

The comparison does not approve public cutover, shadow mode, endpoint activation
without a feature flag, or paid runs. Those remain separately gated.

## Evidence Used

| Evidence | What it proves |
| --- | --- |
| `conformidade-contratos-binding-2026-06-10.pt-BR.md` | The original SDK spike reproduced the known failed boundary where the LLM selects final template plans and variables. The binding fix is action-first. |
| `design-lock-v2-action-first.md` | The production target is the Spec 011 action contract, not the template-first spike output. |
| `evidence/t012-027/action-first-battery-summary.md` | Real-model action-first validation: canary 3/3; 15 frozen scenarios delivered after no-cost fixes; staged final diagnostic delivered on the real model; known-state turns reach one model operation. |
| `evidence/t012-020-038-041-full-mocked-gate-anchor-slice.md` | Every current `test_spec012_*` file except the gate itself is represented in the no-cost contract manifest; canonical mocked behavior and dry-run protections are mandatory. |
| `evidence/t012-041-sdk-contract-gate-slice.md` plus later T012-041 anchor slices | Contract gate enforces strict structured decisions, no free-form SDK delivery, no public imports in the isolated test contract, validators, safety, trace, projection, run-items and static audits. |
| `implementation-ledger.md` | Task-by-task closure notes with protected-scope review, paid-call status and remaining locks. |

## Behavior Comparison

| Requirement | Spec 011 baseline | Original SDK spike | Action-first SDK status | Result |
| --- | --- | --- | --- | --- |
| LLM-first commercial understanding | Existing motor intended to preserve LLM judgment, with mature validators and templates | SDK agents interpreted turns but were asked to choose final templates/variables | LLM chooses compact action and captured semantics; code handles state/template/official facts | Action-first preserves LLM-first without template-first drift. |
| No deterministic commercial regex brain | Spec 011 validators/templates exist; risk is keeping/patching old motor | Spike avoided regex, but repair burden rose because output boundary was too large | Static audit blocks regex-as-brain and public old-runner fallback in SDK core | Action-first is safer and audited. |
| Direct question answered first | Baseline contract requires it | Spike needed validators/repair and had mixed-intent failures early | Validator adequacy map, compiler facts, and mocked/real fixtures cover price/product interruptions | Continue; final real-model golden repetition still required. |
| Diagnostic sequence | Spec 011 defines six-key order and staged final | Spike failed staged final in all 15 spike runs | Compiler derives staged final; real-model battery delivered staged final in Portuguese | Action-first materially beats the original spike and aligns with Spec 011. |
| State ownership | Spec 011 action contract requires board/state before LLM | Original spike let LLM carry too much state/template burden | Turn Situation Builder has no lead-text parameter and computes mode/pending/actions from state | Action-first aligns with binding architecture. |
| Official facts/prices/demo links | Spec 011 validators block invented facts | Spike grounded facts but sometimes needed repair | Compiler resolves official facts; validators block invented price/demo/security/checkout claims | Continue; final runtime persistence proof remains. |
| Product delta (`how_it_works`, WhatsApp scope, security, integration, availability, out-of-profile) | Delta exists as binding requirement, not fully in old public motor | Original spike did not close the full delta | T012-032B slices and fixtures cover the delta in mocked/isolated paths | Partial until real-model and endpoint evidence. |
| Safety boundaries | Required before shadow/cutover | Deferred in original spike by D-012-010 | T012-032C blocks prompt injection, unsupported media, sensitive data and medical advice without LLM calls | Closed for isolated path; final endpoint proof remains. |
| Sales Inbox consistency | Existing projection contracts are preserved | Spike had proposal/evidence only | Action-first projection package derives from validated state/events; no Sales Inbox UI change | Partial until persisted endpoint/runtime proof. |
| Trace/evidence | Spec 011 has reporting expectations | Spike local traces existed | Action-first trace package maps situation, decision, compiler, delivery and SDK run-items | Partial until runtime trace-store/export proof. |
| Cost | Existing path cost/routing differs | Spike proved SDK can run but repair/tool ops were a risk | Action-first known-state turn can run in one model operation; cost cap exists | Continue; real production cost needs shadow. |
| Release gate | Spec 010/011 require eval/manual quality | Spike structural pass was not enough | Quality judge harness exists and blocks mocked proof from release | Not final until real judge/transcripts. |

## What Improved Over The Original SDK Spike

- The LLM no longer has to remember or emit the final template plan.
- The final diagnostic staged sequence is derived by the compiler, making the
  central spike failure class structurally impossible.
- Known-state turns can start directly at the specialist, reducing SDK handoff
  operations without replacing semantic judgment with regex.
- Official variables such as prices, plan summaries and demo links are compiler
  owned, not model-invented.
- Validator repair is now a safety net, not the main way to make the model obey
  the template plan.

## What Spec 011 Still Contributes

- Binding behavior contracts.
- Canonical regression/do-not-do fixtures.
- Mature validator rules.
- Renderer/template discipline.
- Sales Inbox projection expectations.
- Release bar: real transcripts, quality judge and manual review.

The migration should preserve these assets, not reimplement them as prompt-only
behavior.

## Gaps Before Public Activation

The following are not proven by T012-028:

- endpoint/runtime integration behind a feature flag (T012-031);
- persisted trace-store/export proof (T012-034);
- persisted Sales Inbox projection proof (T012-035/T012-046);
- HMAC/idempotency/turn-gate proof in the SDK path (T012-036);
- no public old-runner fallback after feature-flag integration (T012-037);
- real-model golden and do-not-do repetitions after the action-first fixes
  (T012-043/T012-044);
- real quality judge and product-owner/manual review (T012-039/T012-047/T012-048);
- shadow, rollback, preflight, first-hours watch and cutover approval
  (T012-050..T012-055).

## Recommendation For T012-029

Decision: continue, with adaptation already applied.

Meaning:

- continue implementing Spec 012 on the action-first SDK path;
- do not resurrect the original template-first spike boundary;
- do not patch Spec 011 as the final motor;
- proceed next with no-cost feature-flagged endpoint/runtime integration
  planning and tests;
- keep paid real-model validation, shadow mode and public activation blocked
  until explicit approval.

## Validation

This comparison is documentation/evidence only. The current no-cost contract
gate should remain the mechanical proof for the isolated SDK state:

```powershell
python -m pytest services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py -q
```

Most recent local result before this file was written: 2 passed.

## Anti-Determinism Review

No runtime behavior changed. The recommendation explicitly preserves the
LLM-first action-first boundary: the model performs commercial interpretation
and returns structured action decisions; deterministic code remains limited to
state board construction, official facts, compiler expansion, validation,
rendering, persistence, delivery, safety and cost controls.

## Paid-Call Status

No paid OpenAI call was made. Cost: `$0`.
