from __future__ import annotations

from app.core.taliya_commercial.governance import validate_governance_metadata


def _valid_payload() -> dict[str, object]:
    return {
        "change_id": "gov_011_087_001",
        "date": "2026-05-30",
        "owner": "product-owner",
        "artifact_type": "template",
        "affected_artifacts": ["template_registry.product.demo_direct"],
        "reason": "Ajustar texto aprovado para demonstracao comercial.",
        "expected_impact": "Melhorar clareza sem mudar decisao do conductor.",
        "transcript_diff_reference": (
            "specs/011-taliya-commercial-agent-core-reset/eval-reports/demo-diff.md"
        ),
        "eval_before_reference": (
            "specs/011-taliya-commercial-agent-core-reset/eval-reports/before.json"
        ),
        "eval_after_reference": (
            "specs/011-taliya-commercial-agent-core-reset/eval-reports/after.json"
        ),
        "approval_evidence": ["approval-log:2026-05-30:taliya-commercial"],
        "sensitive_change": True,
        "product_fact_sources": [
            {
                "key": "demo_link",
                "source": "official_product_knowledge",
                "reference": "product_knowledge.links.demo",
            }
        ],
    }


def test_governance_metadata_accepts_complete_review_record() -> None:
    result = validate_governance_metadata(_valid_payload())

    assert result.status == "passed"
    assert result.final_disposition == "accepted"
    assert result.errors == []


def test_governance_metadata_blocks_missing_review_evidence() -> None:
    payload = _valid_payload()
    payload["reason"] = ""
    payload["transcript_diff_reference"] = ""
    payload["eval_after_reference"] = ""
    payload["approval_evidence"] = []

    result = validate_governance_metadata(payload)

    assert result.status == "blocked"
    assert {error.code for error in result.errors} >= {
        "governance_reason_missing",
        "governance_transcript_diff_missing",
        "governance_eval_reference_missing",
        "governance_approval_missing",
    }


def test_governance_metadata_blocks_product_facts_outside_official_sources() -> None:
    payload = _valid_payload()
    payload["artifact_type"] = "prompt"
    payload["product_fact_sources"] = [
        {
            "key": "monthly_price",
            "source": "prompt",
            "reference": "system_prompt.price_copy",
        }
    ]

    result = validate_governance_metadata(payload)

    assert result.status == "blocked"
    assert {error.code for error in result.errors} == {
        "governance_product_fact_source_invalid"
    }
