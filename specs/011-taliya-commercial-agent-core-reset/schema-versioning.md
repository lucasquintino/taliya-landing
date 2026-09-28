# Schema Versioning: Spec 011 Taliya Commercial Core Reset

Status: binding governance note for `T011-026`.

Current conductor schema version: `011.0`

The machine-enforced version contract lives in
`services/taliya-agent-runtime/app/core/taliya_commercial/schema_versioning.py`.

## Rule

The conductor decision JSON is a production contract, not an internal detail.

Any change to fields, required fields, enum values, nested structures, variable
shape, semantic meaning, or trace/projection obligations requires:

- compatibility review;
- fixture updates;
- eval coverage;
- Sales Inbox projection review;
- schema fingerprint update;
- explicit version decision.

There is no silent migration. There is no automatic downgrade. Unsupported
versions must fail validation before rendering, persistence, delivery, or Sales
Inbox projection.

## Schema Fingerprint

The current schema fingerprint is:

```text
sha256:e093d16fc05f349b3ddc27389eabaa33544fc10366606b4323e3e9a92bef7bb4
```

The fingerprint is derived from `ConductorDecision.model_json_schema()` using a
canonical JSON encoding. If the fingerprint changes, the tests must fail until
the change is reviewed and this contract is intentionally updated.

## Reviewed Updates

- 2026-05-30 / T011-057: added required `language_policy` to
  `ConductorDecision` so the LLM must declare the practical studio-owner
  language register and whether `CRM` is avoided by default or allowed with
  reason/evidence. The external JSON field remains `language_policy.register`;
  the Python model uses an internal safe attribute name to avoid Pydantic method
  shadowing.
- 2026-05-30 / T011-058: added
  `demo.customer_facing_concept = commercial_product_demo` to `DemoDecision` so
  commercial demo and product demo stay one customer-facing concept in the
  conductor schema. OpenAI technical reference demos, video production, and
  visual demo assets remain out of scope.

## Version Policy

`011.0` is the only supported conductor schema version until implementation
evidence proves a new version is needed.

Version changes are classified as:

- patch-compatible: documentation wording, comments, or internal code that does
  not change `ConductorDecision.model_json_schema()`;
- minor-compatible: additive optional fields or enum values that old traces can
  ignore safely, after eval coverage and projection review;
- breaking: removed fields, renamed fields, required-field additions, type
  changes, meaning changes, trace/projection changes, or validator behavior that
  changes pass/fail semantics.

Minor-compatible and breaking changes require a new supported version entry and
explicit migration or rejection behavior. Until that exists, newer versions such
as `011.1` are unsupported.

## Migration Rules

The reset starts with no automatic migrations. This is deliberate.

If a future migration is added, it must:

- be deterministic and schema-only;
- never decide a commercial route;
- never invent facts, template variables, product claims, diagnostic answers, or
  Sales Inbox fields;
- preserve original payload and version in trace;
- record migration status in the validator/trace report;
- have before/after fixtures and eval coverage.

Migration code must not live in `runner.py` and must not become a commercial
repair path.

## Runtime Gate

Before a conductor decision can be accepted:

1. `schema_version` must exist.
2. The version must be in the supported version set.
3. The current schema fingerprint must match the reviewed fingerprint.
4. The payload must pass strict schema validation.
5. Validators still decide behavior correctness; version compatibility alone is
   never enough for PASS.

This keeps schema evolution explicit while preserving the LLM-first contract.
