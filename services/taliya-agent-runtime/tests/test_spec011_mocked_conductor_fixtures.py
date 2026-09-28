from __future__ import annotations

import re
import unicodedata
from collections.abc import Callable
from typing import Any

import pytest

from app.core.taliya_commercial.conductor import (
    ConductorOutputError,
    ConductorProviderRequest,
    conduct_turn,
)
from app.core.taliya_commercial.context_builder import build_turn_context
from app.core.taliya_commercial.fallback import build_safe_fallback_disposition
from app.core.taliya_commercial.renderer import render_validated_template_plan
from app.core.taliya_commercial.repair import (
    RepairProviderRequest,
    repair_conductor_decision,
)
from app.core.taliya_commercial.runtime_adapter import run_spec011_agent_turn
from app.core.taliya_commercial.runtime_state import build_runtime_state_diff
from app.core.taliya_commercial.sales_inbox_projection import build_sales_inbox_projection
from app.core.taliya_commercial.schemas import (
    ConductorDecision,
    DeliveryEvent,
    ModelUsage,
    TurnContext,
)
from app.core.taliya_commercial.trace_store import build_turn_trace
from app.core.taliya_commercial.validators import validate_conductor_result
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import InMemoryMemoryStore, RuntimeState


def _request(
    text: str,
    *,
    channel: str = "widget",
    conversation_id: str = "fixture_conv_1",
    shadow: bool = False,
) -> AgentRunRequest:
    metadata: dict[str, Any] = {
        "spec011_core_contract": "taliya_commercial_core_reset_v1",
        "page_path": "whatsapp:taliya" if channel == "whatsapp" else "/pilates",
        "source_section": "taliya_owned_whatsapp" if channel == "whatsapp" else "floating_agent",
        "provider": channel,
    }
    if shadow:
        metadata["spec011_shadow_mode"] = {
            "enabled": True,
            "reason": "t011_102_mocked_fixture",
        }

    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": channel,
            "conversation": {
                "conversation_id": conversation_id,
                "lead_id": f"lead_{conversation_id}",
                "channel_conversation_id": conversation_id,
                "source": "taliya_whatsapp" if channel == "whatsapp" else "pilates_landing",
                "entry_intent": channel,
            },
            "message": {
                "idempotency_key": f"{channel}:{conversation_id}:1",
                "channel_message_id": f"msg_{conversation_id}",
                "type": "text",
                "text": text,
                "timestamp": "2026-05-31T12:00:00Z",
            },
            "sender": {"name": "Ana"},
            "metadata": metadata,
        }
    )


def _context(
    text: str,
    *,
    channel: str = "widget",
    conversation_id: str = "fixture_conv_context",
) -> TurnContext:
    return build_turn_context(
        turn_id=f"turn_{conversation_id}",
        request=_request(text, channel=channel, conversation_id=conversation_id),
        state=RuntimeState(
            conversation_id=conversation_id,
            agent_key="taliya_commercial",
            current_agent_name="taliya_commercial_spec011_product_agent",
            summary="Fixture mocked conductor context.",
            diagnostic={"status": "not_started", "ledger": []},
            waitlist={"status": "none"},
            demo={"status": "not_offered"},
        ),
        recent_events=[],
    )


def _usage(input_tokens: int = 100, output_tokens: int = 30) -> dict[str, Any]:
    return ModelUsage(
        model="gpt-5.4-mini",
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cost_usd=0.001,
    ).model_dump(mode="json")


def _price_decision_payload(context: TurnContext) -> dict[str, Any]:
    return {
        "schema_version": "011.0",
        "turn_id": context.turn_id,
        "conversation_id": context.conversation_id,
        "channel": context.channel,
        "agent_key": context.agent_key,
        "role": "product",
        "route": "product",
        "previous_state": "new_lead",
        "current_state": "product_question",
        "next_state": "product_question",
        "detected_intents": ["price_question"],
        "direct_question_present": True,
        "direct_question_answered_first": True,
        "diagnostic": {"action": "offer"},
        "facts": [
            {
                "key": "asked_price",
                "value": "quanto custa",
                "source": "user_message",
                "reliability": "customer_provided",
                "evidence": ["inbound.text"],
                "confidence": "high",
            }
        ],
        "language_policy": {
            "register": "studio_owner_practical",
            "crm_term_policy": "avoid_by_default",
        },
        "template_plan": {
            "items": [
                {
                    "template_id": "product.price_direct",
                    "channel": context.channel,
                    "variables": {
                        "plan_price_summary": {
                            "kind": "long_text",
                            "value": "Resumo oficial dos planos disponiveis.",
                            "source": "official_product_knowledge",
                            "evidence": ["product_knowledge.prices"],
                            "max_length": 360,
                        }
                    },
                },
                {
                    "template_id": "diagnostic.price_hook",
                    "channel": context.channel,
                    "variables": {},
                }
            ]
        },
        "policy_checks": {
            "direct_question_answered_first": True,
            "diagnostic_timing_ok": True,
            "waitlist_timing_ok": True,
            "official_facts_only": True,
            "no_internal_text_leak": True,
            "no_early_contact_capture": True,
            "no_human_overlap": True,
        },
        "confidence": "high",
    }


def _demo_decision_payload(context: TurnContext, *, include_link: bool) -> dict[str, Any]:
    variables: dict[str, Any] = {}
    if include_link:
        variables["official_demo_link"] = {
            "kind": "url",
            "value": "https://www.taliya.com.br/pilates/planos/demonstracao",
            "source": "official_product_knowledge",
            "evidence": ["product_knowledge.links"],
        }

    return {
        "schema_version": "011.0",
        "turn_id": context.turn_id,
        "conversation_id": context.conversation_id,
        "channel": context.channel,
        "agent_key": context.agent_key,
        "role": "product",
        "route": "product",
        "previous_state": "new_lead",
        "current_state": "demo_question",
        "next_state": "demo_offered",
        "detected_intents": ["demo_request"],
        "direct_question_present": True,
        "direct_question_answered_first": True,
        "demo": {
            "customer_facing_concept": "commercial_product_demo",
            "status": "offered",
            "next_step": "offer_demo",
        },
        "language_policy": {
            "register": "studio_owner_practical",
            "crm_term_policy": "avoid_by_default",
        },
        "template_plan": {
            "items": [
                {
                    "template_id": "product.demo_direct",
                    "channel": context.channel,
                    "variables": variables,
                }
            ]
        },
        "policy_checks": {
            "direct_question_answered_first": True,
            "diagnostic_timing_ok": True,
            "waitlist_timing_ok": True,
            "official_facts_only": True,
            "no_internal_text_leak": True,
            "no_early_contact_capture": True,
            "no_human_overlap": True,
        },
        "confidence": "high",
    }


def _template_var(
    *,
    kind: str,
    value: Any,
    source: str,
    evidence: list[str],
    max_length: int | None = None,
) -> dict[str, Any]:
    payload = {
        "kind": kind,
        "value": value,
        "source": source,
        "evidence": evidence,
    }
    if max_length is not None:
        payload["max_length"] = max_length
    return payload


def _base_decision_payload(
    context: TurnContext,
    *,
    role: str,
    route: str,
    current_state: str,
    next_state: str,
    detected_intents: list[str],
    template_items: list[dict[str, Any]],
    direct_question_present: bool = True,
    direct_question_answered_first: bool = True,
    waitlist: dict[str, Any] | None = None,
    diagnostic: dict[str, Any] | None = None,
    demo: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": "011.0",
        "turn_id": context.turn_id,
        "conversation_id": context.conversation_id,
        "channel": context.channel,
        "agent_key": context.agent_key,
        "role": role,
        "route": route,
        "previous_state": "new_lead",
        "current_state": current_state,
        "next_state": next_state,
        "detected_intents": detected_intents,
        "direct_question_present": direct_question_present,
        "direct_question_answered_first": direct_question_answered_first,
        "diagnostic": diagnostic or {"action": "none"},
        "waitlist": waitlist or {"eligibility": "unknown", "status": "none"},
        "demo": demo
        or {
            "customer_facing_concept": "commercial_product_demo",
            "status": "not_offered",
            "next_step": "none",
        },
        "facts": [],
        "language_policy": {
            "register": "studio_owner_practical",
            "crm_term_policy": "avoid_by_default",
        },
        "template_plan": {"items": template_items},
        "policy_checks": {
            "direct_question_answered_first": direct_question_answered_first,
            "diagnostic_timing_ok": True,
            "waitlist_timing_ok": True,
            "official_facts_only": True,
            "no_internal_text_leak": True,
            "no_early_contact_capture": True,
            "no_human_overlap": True,
        },
        "confidence": "high",
    }


def _do_not_do_early_phone_capture_payload(context: TurnContext) -> dict[str, Any]:
    return _base_decision_payload(
        context,
        role="product",
        route="product",
        current_state="product_question",
        next_state="product_question",
        detected_intents=["price_question", "contact_later_preference"],
        diagnostic={"action": "offer"},
        template_items=[
            {
                "template_id": "product.price_direct",
                "channel": context.channel,
                "variables": {
                    "plan_price_summary": _template_var(
                        kind="long_text",
                        value=(
                            "Os planos oficiais sao Base R$ 197/mes, Essencial "
                            "R$ 497/mes, Avance R$ 897/mes e Completo R$ 1.497/mes."
                        ),
                        source="official_product_knowledge",
                        evidence=["product_knowledge.prices"],
                        max_length=360,
                    )
                },
            },
            {
                "template_id": "diagnostic.price_hook",
                "channel": context.channel,
                "variables": {},
            },
        ],
    )


def _do_not_do_date_vip_discount_payload(context: TurnContext) -> dict[str, Any]:
    return _base_decision_payload(
        context,
        role="product",
        route="product",
        current_state="product_price_objection",
        next_state="product_followup",
        detected_intents=["discount_request", "date_availability_request"],
        template_items=[
            {
                "template_id": "product.price_objection_value",
                "channel": context.channel,
                "variables": {},
            }
        ],
    )


def _do_not_do_client_studio_whatsapp_capture_payload(
    context: TurnContext,
) -> dict[str, Any]:
    return _base_decision_payload(
        context,
        role="product",
        route="product",
        current_state="product_question",
        next_state="product_question",
        detected_intents=["integration_scope", "whatsapp_product_question"],
        template_items=[
            {
                "template_id": "product.integration_scope_direct",
                "channel": context.channel,
                "variables": {
                    "integration_topic": _template_var(
                        kind="short_text",
                        value="WhatsApp Business do studio",
                        source="user_message",
                        evidence=["inbound.text"],
                        max_length=100,
                    )
                },
            }
        ],
    )


def _do_not_do_wrong_student_language_payload(context: TurnContext) -> dict[str, Any]:
    demo_link = _template_var(
        kind="url",
        value="https://www.taliya.com.br/pilates/planos/demonstracao",
        source="official_product_knowledge",
        evidence=["product_knowledge.links"],
    )
    return _base_decision_payload(
        context,
        role="product",
        route="product",
        current_state="product_question",
        next_state="demo_offered",
        detected_intents=["whatsapp_product_question", "demo_request"],
        demo={
            "customer_facing_concept": "commercial_product_demo",
            "status": "offered",
            "next_step": "offer_demo",
        },
        template_items=[
            {
                "template_id": "product.whatsapp_direct",
                "channel": context.channel,
                "variables": {
                    "product_fact_summary": _template_var(
                        kind="long_text",
                        value=(
                            "Os alunos nao precisam baixar aplicativo nem criar "
                            "senha; a equipe atualiza o painel e a Taliya avisa "
                            "o responsavel pelo WhatsApp."
                        ),
                        source="official_product_knowledge",
                        evidence=["product_knowledge.whatsapp_scope"],
                        max_length=320,
                    ),
                    "official_demo_link": demo_link,
                },
            },
            {
                "template_id": "product.demo_direct",
                "channel": context.channel,
                "variables": {"official_demo_link": demo_link},
            },
        ],
    )


def _normalized_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    without_marks = "".join(
        char for char in normalized if not unicodedata.combining(char)
    )
    return re.sub(r"\s+", " ", without_marks.casefold()).strip()


class FixedConductorProvider:
    def __init__(
        self,
        output: Callable[[TurnContext], Any] | Any,
        *,
        usage: dict[str, Any] | None = None,
    ) -> None:
        self.output = output
        self.usage = usage or _usage()
        self.calls: list[ConductorProviderRequest] = []

    async def __call__(self, request: ConductorProviderRequest) -> Any:
        self.calls.append(request)
        output = self.output(request.context) if callable(self.output) else self.output
        if isinstance(output, dict) and "schema_version" in output:
            return {"decision": output, "model_usage": self.usage}
        return output


class FixedRepairProvider:
    def __init__(
        self,
        output: Callable[[RepairProviderRequest], Any] | Any,
        *,
        usage: dict[str, Any] | None = None,
    ) -> None:
        self.output = output
        self.usage = usage or _usage(input_tokens=40, output_tokens=12)
        self.calls: list[RepairProviderRequest] = []

    async def __call__(self, request: RepairProviderRequest) -> Any:
        self.calls.append(request)
        output = self.output(request) if callable(self.output) else self.output
        if isinstance(output, dict) and "schema_version" in output:
            return {"decision": output, "model_usage": self.usage}
        return output


@pytest.mark.asyncio
async def test_mocked_valid_decision_flows_through_adapter_and_shadow_trace_projection() -> None:
    memory_store = InMemoryMemoryStore()
    provider = FixedConductorProvider(_price_decision_payload)

    normal_response = await run_spec011_agent_turn(
        _request("quanto custa?", conversation_id="fixture_valid_normal"),
        memory_store=memory_store,
        provider="mock",
        model="gpt-5.4-mini",
        conductor_provider=provider,
    )

    assert normal_response.output.decision.route == "product"
    assert normal_response.output.messages[0].template_id == "product.price_direct"
    assert normal_response.output.usage.input_tokens == 100
    state = await memory_store.load_state("fixture_valid_normal", "taliya_commercial")
    assert state is not None
    assert state.last_decision["template_ids"] == [
        "product.price_direct",
        "diagnostic.price_hook",
    ]

    shadow_response = await run_spec011_agent_turn(
        _request(
            "quanto custa e serve pro meu studio?",
            conversation_id="fixture_valid_shadow",
            shadow=True,
        ),
        memory_store=memory_store,
        provider="mock",
        model="gpt-5.4-mini",
        conductor_provider=provider,
    )

    assert shadow_response.output.messages == []
    events = await memory_store.list_events("fixture_valid_shadow")
    trace = events[0].metadata["trace"]
    assert trace["decision"]["route"] == "product"
    assert trace["validator_result"]["status"] == "passed"
    assert trace["rendered_messages"][0]["template_id"] == "product.price_direct"
    assert trace["sales_inbox_projection"]["commercial_stage"] == "product_question"


@pytest.mark.parametrize(
    (
        "case_id",
        "text",
        "channel",
        "payload_factory",
        "expected_route",
        "required_template_ids",
        "must_include",
        "must_include_any",
        "must_not_include",
    ),
    [
        (
            "do-not-do-early-phone-capture",
            "quero saber quanto custa, depois voces me chamam",
            "widget",
            _do_not_do_early_phone_capture_payload,
            "product",
            {"product.price_direct", "diagnostic.price_hook"},
            ["R$ 497"],
            [],
            [
                "qual seu telefone",
                "me passa seu WhatsApp",
                "manda seu contato",
                "qual seu nome",
            ],
        ),
        (
            "do-not-do-date-vip-discount",
            "tem desconto VIP ou data certa para entrar? quero pagar hoje",
            "whatsapp",
            _do_not_do_date_vip_discount_payload,
            "product",
            {"product.price_objection_value"},
            [],
            ["lista"],
            [
                "desconto aprovado",
                "desconto garantido",
                "vaga VIP",
                "VIP garantido",
                "abre no dia",
                "data garantida",
                "pagar hoje pelo link",
                "checkout seguro",
            ],
        ),
        (
            "do-not-do-client-studio-whatsapp-capture",
            "posso conectar meu WhatsApp Business do studio agora? qual numero voces precisam?",
            "whatsapp",
            _do_not_do_client_studio_whatsapp_capture_payload,
            "product",
            {"product.integration_scope_direct"},
            [],
            ["WhatsApp", "confirmar", "equipe"],
            [
                "manda o numero",
                "me passa o numero",
                "conecto agora",
                "ja conecto",
                "escaneie o QR",
                "codigo de verificacao",
            ],
        ),
        (
            "do-not-do-wrong-student-language",
            "meus clientes precisam baixar app para usar a Taliya?",
            "widget",
            _do_not_do_wrong_student_language_payload,
            "product",
            {"product.whatsapp_direct", "product.demo_direct"},
            ["alunos", "nao precisam baixar aplicativo"],
            [],
            ["clientes precisam baixar app", "consumidores"],
        ),
    ],
)
async def test_t011_105_missing_do_not_do_cases_have_local_preflight(
    case_id: str,
    text: str,
    channel: str,
    payload_factory: Callable[[TurnContext], dict[str, Any]],
    expected_route: str,
    required_template_ids: set[str],
    must_include: list[str],
    must_include_any: list[str],
    must_not_include: list[str],
) -> None:
    memory_store = InMemoryMemoryStore()
    conversation_id = f"fixture_t011_105_{case_id.replace('-', '_')}"
    request = _request(text, channel=channel, conversation_id=conversation_id)
    request.metadata["spec011_eval_trace"] = True
    provider = FixedConductorProvider(payload_factory)

    response = await run_spec011_agent_turn(
        request,
        memory_store=memory_store,
        provider="mock",
        model="gpt-5.4-mini",
        conductor_provider=provider,
    )

    assert len(provider.calls) == 1
    assert response.output.usage.model == "gpt-5.4-mini"
    assert response.output.decision.route == expected_route
    assert required_template_ids.issubset(set(response.output.decision.template_ids))
    assert response.output.validator_results[0]["status"] == "passed"
    assert response.output.sales_inbox_projection["fields"]["validator_status"] == "passed"
    assert response.output.sales_inbox_projection["conversation_id"] == conversation_id
    if channel == "whatsapp":
        assert len(response.output.messages) <= 3

    rendered_text = "\n".join(message.text for message in response.output.messages)
    normalized_rendered = _normalized_text(rendered_text)
    for phrase in must_include:
        assert _normalized_text(phrase) in normalized_rendered
    if must_include_any:
        assert any(_normalized_text(phrase) in normalized_rendered for phrase in must_include_any)
    for phrase in must_not_include:
        assert _normalized_text(phrase) not in normalized_rendered


@pytest.mark.asyncio
async def test_mocked_repairable_decision_repairs_once_then_renders_and_persists() -> None:
    memory_store = InMemoryMemoryStore()
    conductor = FixedConductorProvider(
        lambda context: _demo_decision_payload(context, include_link=False),
        usage=_usage(input_tokens=90, output_tokens=28),
    )
    repair = FixedRepairProvider(
        lambda request: _demo_decision_payload(request.context, include_link=True),
        usage=_usage(input_tokens=30, output_tokens=10),
    )

    response = await run_spec011_agent_turn(
        _request("tem demo?", conversation_id="fixture_repairable_demo"),
        memory_store=memory_store,
        provider="mock",
        model="gpt-5.4-mini",
        conductor_provider=conductor,
        repair_provider=repair,
    )

    assert len(conductor.calls) == 1
    assert len(repair.calls) == 1
    assert [issue.code for issue in repair.calls[0].validator_errors] == [
        "template_plan_invalid"
    ]
    assert response.output.messages[0].template_id == "product.demo_direct"
    assert response.output.usage.input_tokens == 120
    state = await memory_store.load_state("fixture_repairable_demo", "taliya_commercial")
    assert state is not None
    assert state.demo["status"] == "offered"


@pytest.mark.asyncio
async def test_mocked_repaired_decision_builds_trace_and_sales_inbox_projection() -> None:
    context = _context("tem demo?", conversation_id="fixture_trace_repair")
    original = ConductorDecision.model_validate(
        _demo_decision_payload(context, include_link=False)
    )
    validator_result = validate_conductor_result(original, context)
    repair = await repair_conductor_decision(
        original,
        context,
        validator_result,
        provider=FixedRepairProvider(
            lambda request: _demo_decision_payload(request.context, include_link=True)
        ),
    )

    assert validator_result.status == "repairable"
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None

    final_validator_result = validate_conductor_result(
        repair.repaired_decision,
        context,
    ).model_copy(update={"repair_attempt_count": 1, "final_disposition": "repaired"})
    rendered = render_validated_template_plan(
        repair.repaired_decision.template_plan,
        final_validator_result,
        channel=context.channel,
    )
    runtime_state_diff = build_runtime_state_diff(
        repair.repaired_decision,
        final_validator_result,
        repair_result=repair,
    )
    delivery_events = [
        DeliveryEvent(
            event="rendered",
            idempotency_key=context.inbound.idempotency_key,
            status="planned",
        )
    ]
    projection = build_sales_inbox_projection(
        context=context,
        decision=repair.repaired_decision,
        validator_result=final_validator_result,
        runtime_state_diff=runtime_state_diff,
        delivery_events=delivery_events,
    )
    trace = build_turn_trace(
        context=context,
        decision=repair.repaired_decision,
        validator_result=final_validator_result,
        repair_result=repair,
        render_plan=repair.repaired_decision.template_plan,
        rendered_messages=rendered,
        model_usage=repair.model_usage or ModelUsage.model_validate(_usage()),
        runtime_state_diff=runtime_state_diff,
        delivery_events=delivery_events,
        sales_inbox_projection=projection,
    )

    assert trace.trace_complete is True
    assert trace.repair_result.status == "repaired"
    assert trace.rendered_messages[0].template_id == "product.demo_direct"
    assert trace.sales_inbox_projection.fields["validator_final_disposition"] == "repaired"


@pytest.mark.asyncio
async def test_mocked_invalid_provider_output_maps_to_safe_fallback_disposition() -> None:
    context = _context("quanto custa?", conversation_id="fixture_invalid_provider")

    with pytest.raises(ConductorOutputError):
        await conduct_turn(
            context,
            provider=FixedConductorProvider("texto livre nao estruturado"),
        )

    fallback = build_safe_fallback_disposition(
        context=context,
        failure_source="provider_output_invalid",
        failure_reason="conductor_non_json",
    )

    assert fallback.status == "safe_fallback"
    assert fallback.template_id == "fallback.invalid_json"
    assert fallback.commercial_answer_allowed is False


@pytest.mark.asyncio
async def test_mocked_blocked_decision_maps_to_handoff_without_repair_or_copy() -> None:
    context = _context("quanto custa?", conversation_id="fixture_blocked_channel")
    payload = _price_decision_payload(context)
    payload["template_plan"]["items"][0]["channel"] = "whatsapp"
    decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(decision, context)
    repair_provider = FixedRepairProvider(lambda request: _price_decision_payload(request.context))

    repair = await repair_conductor_decision(
        decision,
        context,
        validator_result,
        provider=repair_provider,
    )
    fallback = build_safe_fallback_disposition(
        context=context,
        decision=decision,
        validator_result=validator_result,
        repair_result=repair,
        failure_source="validator_blocked",
    )

    assert validator_result.status == "blocked"
    assert [issue.code for issue in validator_result.errors] == ["channel_mismatch"]
    assert repair.status == "blocked"
    assert repair_provider.calls == []
    assert fallback.status == "handoff_required"
    assert fallback.template_id == "handoff.acknowledge"
    assert fallback.ai_pause_required is True
    assert fallback.commercial_answer_allowed is False
    assert not hasattr(fallback, "rendered_messages")


@pytest.mark.asyncio
async def test_mocked_failed_repair_maps_to_handoff_without_deterministic_answer() -> None:
    context = _context("tem demo?", conversation_id="fixture_failed_repair")
    original = ConductorDecision.model_validate(
        _demo_decision_payload(context, include_link=False)
    )
    validator_result = validate_conductor_result(original, context)
    repair = await repair_conductor_decision(
        original,
        context,
        validator_result,
        provider=FixedRepairProvider(
            lambda request: _demo_decision_payload(request.context, include_link=False)
        ),
    )
    fallback = build_safe_fallback_disposition(
        context=context,
        decision=original,
        validator_result=validator_result,
        repair_result=repair,
        failure_source="repair_failed",
    )

    assert validator_result.status == "repairable"
    assert repair.status == "failed"
    assert "template_plan_invalid" in repair.errors_sent
    assert fallback.status == "handoff_required"
    assert fallback.template_id == "handoff.acknowledge"
    assert fallback.commercial_answer_allowed is False
