# Governance Metadata Contract

Prompt, policy, template, and product-knowledge changes must carry review
metadata before they are allowed to affect the Taliya commercial agent.

Required fields:

- `change_id`
- `date`
- `owner`
- `artifact_type`
- `affected_artifacts`
- `reason`
- `expected_impact`
- `transcript_diff_reference`
- `eval_before_reference`
- `eval_after_reference`
- `approval_evidence`
- `sensitive_change`
- `product_fact_sources`

Product facts may reference only:

- `official_product_knowledge`
- `spec_006_product_contract`

This contract is control-plane only. It must not change runtime prompts,
template wording, product facts, routing, adapters, Sales Inbox UI, `/pilates`,
or `runtime/runner.py`.
