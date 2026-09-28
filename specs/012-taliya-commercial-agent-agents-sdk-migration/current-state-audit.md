# Current-State Audit - Before Spec 012 Implementation

This audit documents why Spec 012 should replace the current conversation motor rather than continue patching it.

## What Is Working

- Public Taliya commercial turns are routed to `/v1/taliya-commercial/turn`.
- The legacy `/v1/agent-runs` path rejects public Taliya commercial turns.
- Runtime API has HMAC, idempotency, feature flag, and registry boundaries.
- The repo already depends on `openai-agents`.
- Spec 011 produced strong contracts, fixtures, validators, renderer boundaries, trace expectations, Sales Inbox projection expectations, and protected `/pilates` gates.
- Existing docs preserve the right commercial behavior and should be reused.

## What Is Not Working As The Final Motor

The current Spec 011 core has become a custom agent framework:

- `conductor.py` handles provider calls and conductor prompting.
- `turn_situation.py` constrains allowed actions.
- `decision_compiler.py` maps model actions into state/render decisions.
- `repair.py` contains extensive repair behavior.
- `validators.py` is very large and mixes many contract families.
- `runtime_adapter.py` orchestrates the entire custom pipeline.

This structure prevents old deterministic routing from returning, but it does not fully solve commercial understanding. The model can choose a valid action while still producing weak or generic context understanding.

## Key Failure Signal

The latest T011-105 paid evidence failed because a pain-first response did not reuse concrete lead terms such as WhatsApp/interested leads. That is a conversational understanding failure, not just a schema failure.

The local fix forced a required field and validator behavior, but continuing that pattern risks growing a larger repair/field framework instead of making the agent better.

## Main Risk If We Continue Spec 011 As-Is

- More validators and repair branches.
- More schema fields to compensate for model weakness.
- More action/compile logic.
- More locally green tests with weak conversation quality.
- Another large core that is safer than the old runner but still not a truly capable agent.

## Main Risk If We Move To Agents SDK

- SDK handoffs may increase cost.
- SDK final text may be tempting to deliver directly.
- SDK tools can mutate state if not constrained.
- Agent instructions can become product-fact hiding places.
- Tracing/privacy must be reviewed before production.
- A bad migration can recreate a new monster around the SDK.

## Recommendation

Proceed with Spec 012 documentation and an isolated Agents SDK spike.

Do not implement public cutover until the spike proves better commercial understanding than the current Spec 011 path on the critical scenarios.
