from __future__ import annotations

from pathlib import Path

from app.core.taliya_commercial.context_builder import build_turn_context
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import RuntimeState


def _repo_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "specs" / "006-crm-operational-core").exists():
            return parent
    raise AssertionError("repo root not found")


def _request(text: str) -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {
                "conversation_id": "conv_spec006_1",
                "lead_id": "lead_spec006_1",
                "source": "pilates_landing",
            },
            "message": {
                "idempotency_key": "wa:conv_spec006_1:1",
                "type": "text",
                "text": text,
            },
            "sender": {},
            "metadata": {"page_path": "/pilates"},
        }
    )


def _state() -> RuntimeState:
    return RuntimeState(
        conversation_id="conv_spec006_1",
        agent_key="taliya_commercial",
        current_agent_name="taliya_commercial_product_agent",
        summary="Lead quer entender produto, setup e acesso.",
        diagnostic={"status": "not_started", "ledger": []},
        waitlist={"status": "none"},
        demo={"status": "not_offered"},
    )


def test_context_builder_retrieves_spec006_contract_refs_as_context() -> None:
    context = build_turn_context(
        turn_id="turn_spec006",
        request=_request("como funciona depois de assinar?"),
        state=_state(),
        recent_events=[],
        spec006_contract_keys=[
            "product_positioning",
            "plan_entitlements",
            "operating_modes",
            "setup_scope",
            "access_subscription",
            "navigation_routes",
        ],
    )

    refs = {
        ref.key: ref
        for ref in context.product_knowledge
        if ref.source == "spec_006_product_contract"
    }

    assert set(refs) == {
        "spec006.product_positioning",
        "spec006.plan_entitlements",
        "spec006.operating_modes",
        "spec006.setup_scope",
        "spec006.access_subscription",
        "spec006.navigation_routes",
    }
    positioning = refs["spec006.product_positioning"]
    assert positioning.version is not None
    assert positioning.version.startswith("spec006-")
    assert positioning.missing is False
    assert positioning.value["source_path"] == "specs/006-crm-operational-core/spec.md"
    assert positioning.value["heading"] == "Product Positioning"
    assert positioning.evidence == [
        "specs/006-crm-operational-core/spec.md#Product Positioning"
    ]
    source_text = (
        _repo_root() / "specs" / "006-crm-operational-core" / "spec.md"
    ).read_text(encoding="utf-8")
    assert positioning.value["excerpt"] in source_text


def test_context_builder_records_missing_spec006_contract_refs_explicitly() -> None:
    context = build_turn_context(
        turn_id="turn_spec006_missing",
        request=_request("tem agenda externa viva?"),
        state=_state(),
        recent_events=[],
        spec006_contract_keys=["calendar_live_write"],
    )

    spec_refs = [
        ref for ref in context.product_knowledge if ref.source == "spec_006_product_contract"
    ]

    assert len(spec_refs) == 1
    missing_ref = spec_refs[0]
    assert missing_ref.key == "spec006.calendar_live_write"
    assert missing_ref.missing is True
    assert missing_ref.value is None
    assert missing_ref.excerpt is None


def test_default_spec006_context_is_stable_not_commercial_routing() -> None:
    price_context = build_turn_context(
        turn_id="turn_price",
        request=_request("quanto custa?"),
        state=_state(),
        recent_events=[],
    )
    pain_context = build_turn_context(
        turn_id="turn_pain",
        request=_request("tenho faltas e vendas baguncadas"),
        state=_state(),
        recent_events=[],
    )

    price_spec_keys = [
        ref.key
        for ref in price_context.product_knowledge
        if ref.source == "spec_006_product_contract"
    ]
    pain_spec_keys = [
        ref.key
        for ref in pain_context.product_knowledge
        if ref.source == "spec_006_product_contract"
    ]

    assert price_spec_keys == pain_spec_keys
    assert "spec006.product_positioning" in price_spec_keys
    assert "spec006.plan_entitlements" in price_spec_keys
    assert price_context.diagnostic_ledger == pain_context.diagnostic_ledger
    assert price_context.waitlist_state == pain_context.waitlist_state
    assert price_context.demo_state == pain_context.demo_state
    assert price_context.handoff_state == pain_context.handoff_state
    assert not any(
        hasattr(ref, "route") or hasattr(ref, "template_id")
        for ref in price_context.product_knowledge
    )

