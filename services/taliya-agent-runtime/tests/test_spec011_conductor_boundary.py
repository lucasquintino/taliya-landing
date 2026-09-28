from __future__ import annotations

import json
from typing import Any

import pytest

from app.core.taliya_commercial.conductor import (
    ActionConductorProviderRequest,
    ActionConductorTurnResult,
    ConductorDecisionValidationError,
    ConductorOutputError,
    ConductorProviderRequest,
    ConductorTurnResult,
    _format_registered_template_catalog,
    build_action_conductor_model_input_payload,
    build_action_conductor_response_schema,
    build_conductor_model_input_payload,
    conduct_action_turn,
    conduct_turn,
)
from app.core.taliya_commercial.context_builder import build_turn_context
from app.core.taliya_commercial.context_snapshot import build_context_snapshot
from app.core.taliya_commercial.schemas import TurnContext
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import RuntimeState


def _request(text: str = "Quanto custa e tenho 120 alunos?") -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {
                "conversation_id": "conv_conductor_1",
                "lead_id": "lead_conductor_1",
                "channel_conversation_id": "wa_conductor_1",
                "source": "pilates_landing",
            },
            "message": {
                "idempotency_key": "wa:conv_conductor_1:1",
                "channel_message_id": "wamid_conductor_1",
                "type": "text",
                "text": text,
            },
            "sender": {
                "name": "Ana",
                "whatsapp_phone": "+5511999999999",
            },
            "metadata": {"page_path": "/pilates"},
        }
    )


def _state() -> RuntimeState:
    return RuntimeState(
        conversation_id="conv_conductor_1",
        agent_key="taliya_commercial",
        current_agent_name="taliya_commercial_product_agent",
        summary="Lead perguntou preco e mencionou tamanho do studio.",
        lead_facts=[
            {
                "key": "active_students_or_size",
                "value": "120",
                "source": "memory",
                "reliability": "customer_provided",
                "confidence": "high",
                "evidence": ["message:m1"],
            }
        ],
        diagnostic={"status": "not_started", "ledger": []},
        waitlist={"status": "none"},
        demo={"status": "not_offered"},
    )


def _context(text: str = "Quanto custa e tenho 120 alunos?") -> TurnContext:
    return build_turn_context(
        turn_id="turn_conductor_1",
        request=_request(text),
        state=_state(),
        recent_events=[],
        product_knowledge_keys=["prices"],
        spec006_contract_keys=["product_positioning"],
    )


def _valid_decision_payload(context: TurnContext) -> dict[str, Any]:
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
        "detected_intents": ["price_question", "student_count_fact"],
        "direct_question_present": True,
        "direct_question_answered_first": True,
        "language_policy": {
            "register": "studio_owner_practical",
            "crm_term_policy": "avoid_by_default",
        },
        "numeric_interpretations": [
            {
                "raw_text": "120",
                "kind": "student_count",
                "value": 120,
                "evidence": ["Quanto custa e tenho 120 alunos?"],
                "confidence": "high",
            }
        ],
        "template_plan": {
            "items": [
                {
                    "template_id": "product.price_direct",
                    "variables": {
                        "plan_price_summary": {
                            "kind": "long_text",
                            "value": "Resumo de preco vindo de conhecimento oficial.",
                            "source": "official_product_knowledge",
                            "evidence": ["product_knowledge.prices"],
                            "max_length": 360,
                        }
                    },
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


def _model_usage() -> dict[str, Any]:
    return {
        "model": "gpt-5.4-mini",
        "input_tokens": 120,
        "output_tokens": 32,
        "cost_usd": 0.001,
    }


def _provider_result(decision: dict[str, Any]) -> dict[str, Any]:
    return {"decision": decision, "model_usage": _model_usage()}


def _object_schemas(schema: Any) -> list[dict[str, Any]]:
    if isinstance(schema, list):
        return [
            item
            for value in schema
            for item in _object_schemas(value)
        ]
    if not isinstance(schema, dict):
        return []
    nested = [
        item
        for value in schema.values()
        for item in _object_schemas(value)
    ]
    if isinstance(schema.get("properties"), dict):
        return [schema, *nested]
    return nested


def _has_key(schema: Any, key: str) -> bool:
    if isinstance(schema, list):
        return any(_has_key(item, key) for item in schema)
    if not isinstance(schema, dict):
        return False
    return key in schema or any(_has_key(item, key) for item in schema.values())


class FakeConductorProvider:
    def __init__(self, output: Any) -> None:
        self.output = output
        self.calls: list[ConductorProviderRequest] = []

    async def __call__(self, request: ConductorProviderRequest) -> Any:
        self.calls.append(request)
        if isinstance(self.output, dict) and "schema_version" in self.output:
            return _provider_result(self.output)
        return self.output


class FakeActionConductorProvider:
    def __init__(self, output: Any) -> None:
        self.output = output
        self.calls: list[ActionConductorProviderRequest] = []

    async def __call__(self, request: ActionConductorProviderRequest) -> Any:
        self.calls.append(request)
        return self.output


def _valid_action_decision_payload(
    context: TurnContext,
    *,
    selected_action: str = "answer_direct_product_question",
) -> dict[str, Any]:
    return {
        "schema_version": "011.action_decision.v1",
        "turn_id": context.turn_id,
        "conversation_id": context.conversation_id,
        "channel": context.channel,
        "agent_key": context.agent_key,
        "selected_action": selected_action,
        "interpreted_intents": ["price_question"],
        "direct_question": {
            "present": True,
            "answered_first": True,
            "answer_obligations": ["answer_price_from_official_facts"],
        },
        "captured_slots": [],
        "product_fact_keys_used": ["prices"],
        "numeric_interpretations": [],
        "diagnostic_intent": {"status": "offer_after_answer"},
        "demo_intent": {"status": "none"},
        "waitlist_intent": {"status": "none"},
        "handoff_intent": {"status": "none"},
        "reply_goal": "answer the price question and offer diagnostic without pressure",
        "confidence": "high",
        "evidence": ["Quanto custa?"],
        "needs_clarification": False,
        "repair_hints": [],
    }


@pytest.mark.asyncio
async def test_conductor_calls_provider_once_with_context_snapshot_and_accepts_decision() -> None:
    context = _context("Quanto custa e tenho 120 alunos?")
    provider = FakeConductorProvider(_valid_decision_payload(context))

    result = await conduct_turn(context, provider=provider)

    assert isinstance(result, ConductorTurnResult)
    assert result.decision.route == "product"
    assert result.decision.role == "product"
    assert result.model_usage.input_tokens > 0
    assert len(provider.calls) == 1
    request = provider.calls[0]
    assert request.context == context
    assert request.response_schema["title"] == "ConductorDecision"
    assert request.response_schema["properties"]["schema_version"]["const"] == "011.0"
    assert "title" not in json.dumps(request.response_schema.get("$defs", {}))
    assert len(json.dumps(request.response_schema, separators=(",", ":"))) < 7600
    assert "product_knowledge" in request.context_snapshot_json
    assert "spec006.product_positioning" in request.context_snapshot_json
    assert request.llm_must_decide is True


@pytest.mark.asyncio
async def test_action_conductor_calls_provider_with_turn_situation_and_small_schema() -> None:
    context = _context("Quanto custa?")
    provider = FakeActionConductorProvider(
        {
            "decision": _valid_action_decision_payload(context),
            "model_usage": _model_usage(),
        }
    )

    result = await conduct_action_turn(context, provider=provider)

    assert isinstance(result, ActionConductorTurnResult)
    assert result.decision.selected_action == "answer_direct_product_question"
    assert result.decision.reply_goal
    assert len(provider.calls) == 1
    request = provider.calls[0]
    assert request.request_schema_version == "011.action_conductor_request.v1"
    assert request.turn_situation.mode == "entry"
    assert "answer_direct_product_question" in request.turn_situation.allowed_actions
    assert "answer_price" not in request.turn_situation.allowed_actions


def test_action_conductor_response_schema_excludes_full_plan_and_state_fields() -> None:
    schema = build_action_conductor_response_schema()
    serialized = json.dumps(schema, separators=(",", ":"))

    assert schema["title"] == "ConductorActionDecision"
    assert schema["properties"]["schema_version"]["const"] == "011.action_decision.v1"
    assert "selected_action" in schema["properties"]
    assert "template_plan" not in serialized
    assert "render_plan" not in serialized
    assert "previous_state" not in serialized
    assert "current_state" not in serialized
    assert "next_state" not in serialized
    assert "route" not in schema["properties"]


def test_action_conductor_model_input_includes_allowed_actions_not_template_catalog() -> None:
    context = _context("Quanto custa?")
    provider = FakeActionConductorProvider(
        {
            "decision": _valid_action_decision_payload(
                context,
                selected_action="answer_direct_product_question",
            ),
            "model_usage": _model_usage(),
        }
    )

    # Build through the provider request so this test stays aligned with production input.
    import asyncio

    asyncio.run(conduct_action_turn(context, provider=provider))
    payload = build_action_conductor_model_input_payload(provider.calls[0])

    assert "turn_situation" in payload
    assert "allowed_actions" in payload["turn_situation"]
    assert "answer_direct_product_question" in payload["turn_situation"]["allowed_actions"]
    assert "templates" not in json.dumps(payload.get("turn_situation"), separators=(",", ":"))


@pytest.mark.asyncio
async def test_action_conductor_rejects_action_outside_turn_situation_menu() -> None:
    context = _context("Quanto custa?")
    provider = FakeActionConductorProvider(
        {
            "decision": _valid_action_decision_payload(
                context,
                selected_action="answer_price",
            ),
            "model_usage": _model_usage(),
        }
    )

    with pytest.raises(ConductorDecisionValidationError) as exc_info:
        await conduct_action_turn(context, provider=provider)

    assert "selected_action" in str(exc_info.value)


@pytest.mark.asyncio
async def test_action_conductor_rejects_unavailable_product_fact_key() -> None:
    context = _context("Quanto custa?")
    decision = _valid_action_decision_payload(
        context,
        selected_action="answer_direct_product_question",
    )
    decision["product_fact_keys_used"] = ["made_up_product_key"]
    provider = FakeActionConductorProvider(
        {"decision": decision, "model_usage": _model_usage()}
    )

    with pytest.raises(ConductorDecisionValidationError) as exc_info:
        await conduct_action_turn(context, provider=provider)

    assert "product_fact_keys_used" in str(exc_info.value)


@pytest.mark.asyncio
async def test_action_conductor_rejects_pain_first_without_human_context() -> None:
    context = _context(
        "perco muitos interessados no WhatsApp porque a equipe demora para responder"
    )
    decision = _valid_action_decision_payload(
        context,
        selected_action="offer_diagnostic_from_pain",
    )
    decision["interpreted_intents"] = ["pain_statement", "interest_in_solutions"]
    decision["direct_question"] = {
        "present": False,
        "answered_first": False,
        "answer_obligations": [],
    }
    decision["product_fact_keys_used"] = []
    decision["diagnostic_intent"] = {"status": "offer", "details": {}}
    provider = FakeActionConductorProvider(
        {"decision": decision, "model_usage": _model_usage()}
    )

    with pytest.raises(ConductorDecisionValidationError) as exc_info:
        await conduct_action_turn(context, provider=provider)

    assert "diagnostic_intent.details.pain_context_human" in str(exc_info.value)


@pytest.mark.asyncio
async def test_conductor_accepts_legacy_render_plan_alias_from_provider() -> None:
    context = _context("Quanto custa?")
    decision = _valid_decision_payload(context)
    decision["render_plan"] = decision.pop("template_plan")
    provider = FakeConductorProvider(_provider_result(decision))

    result = await conduct_turn(context, provider=provider)

    assert result.decision.template_plan.items[0].template_id == "product.price_direct"
    assert not hasattr(result.decision, "render_plan")


@pytest.mark.asyncio
async def test_conductor_normalizes_malformed_diagnostic_object_to_default() -> None:
    context = _context("como funciona?")
    decision = _valid_decision_payload(context)
    decision.update(
        {
            "current_state": "product_how_it_works",
            "next_state": "product_question_answered",
            "detected_intents": ["how_it_works", "product_overview"],
            "diagnostic": "complete",
            "template_plan": {
                "items": [
                    {
                        "template_id": "product.how_it_works_direct",
                        "variables": {
                            "contextual_next_step": {
                                "kind": "enum",
                                "value": "diagnostic_offer_generic",
                                "source": "model_decision",
                                "evidence": ["detected_intents.how_it_works"],
                            }
                        },
                    }
                ]
            },
        }
    )
    provider = FakeConductorProvider(_provider_result(decision))

    result = await conduct_turn(context, provider=provider)

    assert result.decision.diagnostic.action == "none"
    assert [
        item.template_id for item in result.decision.template_plan.items
    ] == ["product.how_it_works_direct"]


@pytest.mark.asyncio
async def test_conductor_normalizes_incompatible_fact_reliability_pairs() -> None:
    context = _context("Quanto custa?")
    decision = _valid_decision_payload(context)
    decision["facts"] = [
        {
            "key": "profile_name",
            "value": "Ana",
            "source": "channel_metadata",
            "reliability": "customer_provided",
            "evidence": ["sender.name"],
        }
    ]
    provider = FakeConductorProvider(_provider_result(decision))

    result = await conduct_turn(context, provider=provider)

    assert result.decision.facts[0].source == "channel_metadata"
    assert result.decision.facts[0].reliability == "channel_provided"


@pytest.mark.asyncio
async def test_conductor_normalizes_runtime_state_fact_source_alias() -> None:
    context = _context("sim")
    decision = _valid_decision_payload(context)
    decision["facts"] = [
        {
            "key": "waitlist_confirmation",
            "value": "sim",
            "source": "runtime_state",
            "reliability": "inferred",
            "evidence": ["waitlist.pending_details"],
        }
    ]
    provider = FakeConductorProvider(_provider_result(decision))

    result = await conduct_turn(context, provider=provider)

    assert result.decision.facts[0].source == "memory"
    assert result.decision.facts[0].reliability == "inferred"


@pytest.mark.asyncio
async def test_conductor_normalizes_internal_facts_as_non_renderable() -> None:
    context = _context("Quanto custa?")
    decision = _valid_decision_payload(context)
    decision["facts"] = [
        {
            "key": "profile_name",
            "value": "Ana",
            "source": "channel_metadata",
            "reliability": "channel_provided",
            "renderable": True,
            "confidence": "certain",
            "evidence": ["sender.name"],
        }
    ]
    provider = FakeConductorProvider(_provider_result(decision))

    result = await conduct_turn(context, provider=provider)

    assert result.decision.facts[0].renderable is False
    assert result.decision.facts[0].confidence == "medium"


@pytest.mark.asyncio
async def test_conductor_normalizes_non_boolean_fact_renderable_before_validation() -> None:
    context = _context("quero comecar, me coloca na lista")
    decision = _valid_decision_payload(context)
    decision["facts"] = [
        {
            "key": "waitlist_interest",
            "value": "quer comecar",
            "source": "user_message",
            "reliability": "customer_provided",
            "renderable": "no",
            "confidence": "high",
            "evidence": ["quero comecar, me coloca na lista"],
        }
    ]
    provider = FakeConductorProvider(_provider_result(decision))

    result = await conduct_turn(context, provider=provider)

    assert result.decision.facts[0].renderable is False


@pytest.mark.asyncio
async def test_conductor_normalizes_provider_schema_noise_before_validation() -> None:
    context = _context("Quanto custa?")
    decision = _valid_decision_payload(context)
    decision["diagnostic"] = {
        "action": "none",
        "answer_value": "extra field from model",
    }
    decision["template_plan"]["items"][0]["variables"]["plan_price_summary"][
        "evidence"
    ] = ["product_knowledge.prices"]
    decision["template_plan"]["items"].append(
        {
            "template_id": "diagnostic.deliver_demo_not_offered",
            "variables": {
                "demo_status": {
                    "kind": "enum",
                    "value": "not_offered",
                    "source": "runtime_state",
                }
            },
        }
    )
    provider = FakeConductorProvider(_provider_result(decision))

    result = await conduct_turn(context, provider=provider)

    assert result.decision.diagnostic.action == "none"
    demo_variable = result.decision.template_plan.items[1].variables["demo_status"]
    assert demo_variable.evidence == ["runtime_state"]


@pytest.mark.asyncio
async def test_conductor_normalizes_waitlist_status_alias_before_schema_validation() -> None:
    context = _context("quero resolver agora")
    decision = _valid_decision_payload(context)
    decision["waitlist"] = {
        "eligibility": "eligible",
        "status": "interested",
        "missing_details": [],
    }
    provider = FakeConductorProvider(_provider_result(decision))

    result = await conduct_turn(context, provider=provider)

    assert result.decision.waitlist.status == "offered"


@pytest.mark.asyncio
async def test_conductor_fills_registered_variable_max_length_before_validation() -> None:
    context = _context("Quanto custa?")
    decision = _valid_decision_payload(context)
    decision["template_plan"]["items"][0]["variables"]["plan_price_summary"].pop(
        "max_length"
    )
    provider = FakeConductorProvider(_provider_result(decision))

    result = await conduct_turn(context, provider=provider)

    variable = result.decision.template_plan.items[0].variables["plan_price_summary"]
    assert variable.max_length == 360


@pytest.mark.asyncio
async def test_conductor_wraps_registered_primitive_template_variables() -> None:
    context = _context("Quanto custa?")
    decision = _valid_decision_payload(context)
    decision["template_plan"]["items"][0]["variables"]["plan_price_summary"] = (
        "Base: R$ 197/mes. Essencial: R$ 497/mes."
    )
    provider = FakeConductorProvider(_provider_result(decision))

    result = await conduct_turn(context, provider=provider)

    variable = result.decision.template_plan.items[0].variables["plan_price_summary"]
    assert variable.kind == "long_text"
    assert variable.source == "official_product_knowledge"
    assert variable.evidence == ["product_knowledge.prices"]
    assert variable.max_length == 360


@pytest.mark.asyncio
async def test_conductor_hoists_decision_fields_from_template_item_noise() -> None:
    context = _context("Quanto custa?")
    decision = _valid_decision_payload(context)
    policy_checks = decision.pop("policy_checks")
    first_item = decision["template_plan"]["items"][0]
    first_item["policy_checks"] = policy_checks
    first_item["confidence"] = "high"
    first_item["repair_hints"] = []
    first_item[":{"] = {"malformed": "provider noise"}
    provider = FakeConductorProvider(_provider_result(decision))

    result = await conduct_turn(context, provider=provider)

    assert result.decision.policy_checks.official_facts_only is True
    assert result.decision.confidence == "high"
    assert result.decision.template_plan.items[0].template_id == "product.price_direct"


@pytest.mark.asyncio
async def test_conductor_normalizes_string_template_items() -> None:
    context = _context("Quanto custa?")
    decision = _valid_decision_payload(context)
    decision["template_plan"]["items"] = ["product.price_direct"]
    provider = FakeConductorProvider(_provider_result(decision))

    result = await conduct_turn(context, provider=provider)

    assert result.decision.template_plan.items[0].template_id == "product.price_direct"
    assert result.decision.policy_checks.official_facts_only is True
    assert result.decision.policy_checks.no_internal_text_leak is True


@pytest.mark.asyncio
async def test_conductor_drops_output_only_decision_fields_before_validation() -> None:
    context = _context("95 alunos ativos")
    decision = _valid_decision_payload(context)
    decision["diagnostic_status"] = "in_progress"
    decision["diagnostic_allowed_now"] = True
    decision["waitlist_allowed_now"] = False
    decision["template_ids"] = ["product.price_direct"]
    provider = FakeConductorProvider(_provider_result(decision))

    result = await conduct_turn(context, provider=provider)

    assert result.decision.route == "product"
    assert not hasattr(result.decision, "diagnostic_status")


@pytest.mark.asyncio
async def test_conductor_request_does_not_tell_llm_to_emit_usage_envelope() -> None:
    context = _context("Quanto custa?")
    provider = FakeConductorProvider(_valid_decision_payload(context))

    await conduct_turn(context, provider=provider)

    provider_requirements = " ".join(provider.calls[0].provider_requirements).lower()
    assert "only the conductordecision json" in provider_requirements
    assert "do not include model_usage" in provider_requirements
    assert "conductorturnresult" not in provider_requirements
    assert "envelope with decision and model_usage" not in provider_requirements
    policy = str(provider.calls[0].specialist_policy.model_dump(mode="json"))
    assert "diagnostic.price_hook for generic price questions" in policy
    assert "plan_fit_context is grounded" in policy
    assert "not a plan-fit question by themselves" in policy
    assert "For price-only turns, leave demo.status=not_offered" in policy


@pytest.mark.asyncio
async def test_conductor_request_includes_registered_template_catalog() -> None:
    context = _context("Quanto custa?")
    provider = FakeConductorProvider(_valid_decision_payload(context))

    await conduct_turn(context, provider=provider)

    instructions = " ".join(provider.calls[0].instructions)
    assert "Use only template ids from this registered catalog" in instructions
    assert "product.price_direct" in instructions
    assert "diagnostic.deliver_hold" in instructions
    assert '"diagnostic.deliver":' not in instructions
    assert "Never use the legacy exact template id diagnostic.deliver" in instructions
    assert "plan_price_summary" in instructions
    assert "price_list_brief" not in instructions


def test_registered_template_catalog_is_compact_without_losing_rules() -> None:
    catalog = json.loads(_format_registered_template_catalog())

    assert catalog["template_format"] == "id:[required_variables,optional_variables]"
    assert catalog["variable_format"] == (
        "name:[kind,allowed_sources,max_length,validation_rule]"
    )
    assert catalog["templates"]["product.price_direct"] == [
        ["plan_price_summary"],
        ["plan_fit_context"],
    ]
    assert "diagnostic.deliver" not in catalog["templates"]
    price_variable = catalog["variables"]["plan_price_summary"]
    assert price_variable[0] == "long_text"
    assert "official_product_knowledge" in price_variable[1]
    assert price_variable[2] == 360
    assert "Official price/plan summary" in price_variable[3]
    assert len(_format_registered_template_catalog()) < 9000


@pytest.mark.asyncio
async def test_conductor_model_input_uses_compact_context_for_openai() -> None:
    context = build_turn_context(
        turn_id="turn_conductor_model_input",
        request=_request("Quanto custa e qual plano serve para 120 alunos?"),
        state=_state(),
        recent_events=[],
        product_knowledge_keys=["plans", "prices", "links"],
        spec006_contract_keys=["product_positioning", "plan_entitlements"],
    )
    provider = FakeConductorProvider(_valid_decision_payload(context))

    await conduct_turn(context, provider=provider)

    request = provider.calls[0]
    payload = build_conductor_model_input_payload(request)
    assert list(payload) == ["specialist_policy", "provider_requirements", "context"]
    assert "global_rules" not in payload["specialist_policy"]
    assert payload["specialist_policy"]["global_rules_ref"] == "see_conductor_instructions"
    assert payload["specialist_policy"]["roles"]
    model_refs = payload["context"]["product_knowledge"]
    assert model_refs
    assert all("value" not in ref for ref in model_refs)
    assert all("version" not in ref for ref in model_refs)
    assert all(ref.get("missing") is True or "missing" not in ref for ref in model_refs)
    assert all("excerpt" in ref or ref["missing"] is True for ref in model_refs)
    assert any(ref["key"] == "plans" for ref in model_refs)
    assert any(ref["key"] == "prices" for ref in model_refs)
    assert any(
        ref["key"] == "plans" and "Completo" in ref["excerpt"]
        for ref in model_refs
    )
    assert any(
        ref["key"] == "plans" and "R$ 1.497/mes" in ref["excerpt"]
        for ref in model_refs
    )
    assert any(ref.value is not None for ref in request.context.product_knowledge)


@pytest.mark.asyncio
async def test_conductor_request_explains_fact_source_reliability_rules() -> None:
    context = _context("Quanto custa?")
    provider = FakeConductorProvider(_valid_decision_payload(context))

    await conduct_turn(context, provider=provider)

    instructions = " ".join(provider.calls[0].instructions)
    assert "Allowed fact source/reliability pairs" in instructions
    assert '"official_product_knowledge":["internal"]' in instructions
    assert "Do not store official product prices" in instructions


@pytest.mark.asyncio
async def test_conductor_request_explains_top_level_json_shape() -> None:
    context = _context("Quanto custa?")
    provider = FakeConductorProvider(_valid_decision_payload(context))

    await conduct_turn(context, provider=provider)

    instructions = " ".join(provider.calls[0].instructions)
    assert "Return a flat ConductorDecision object" in instructions
    assert "top-level siblings of diagnostic" in instructions
    assert "Never nest those fields under diagnostic" in instructions
    assert "For price-only turns, leave demo.status=not_offered" in instructions


@pytest.mark.asyncio
async def test_conductor_request_schema_declares_required_fields_without_defaults() -> None:
    context = _context("Quanto custa e tenho 120 alunos?")
    provider = FakeConductorProvider(_valid_decision_payload(context))

    await conduct_turn(context, provider=provider)

    schema = provider.calls[0].response_schema
    demo_schema = schema["$defs"]["DemoDecision"]
    assert not _has_key(schema, "default")
    assert "customer_facing_concept" in demo_schema["required"]
    for object_schema in _object_schemas(schema):
        properties = object_schema["properties"]
        assert set(object_schema.get("required", [])) == set(properties)


@pytest.mark.asyncio
async def test_conductor_accepts_replayed_context_snapshot_as_input() -> None:
    context = _context()
    snapshot = build_context_snapshot(context, snapshot_id="snapshot_conductor_1")
    provider = FakeConductorProvider(_valid_decision_payload(context))

    result = await conduct_turn(snapshot, provider=provider)

    assert result.decision.turn_id == context.turn_id
    assert provider.calls[0].context == context


@pytest.mark.asyncio
async def test_conductor_rejects_freeform_text_without_customer_facing_fallback() -> None:
    context = _context()
    provider = FakeConductorProvider("Oi, consigo te explicar os planos por aqui.")

    with pytest.raises(ConductorOutputError):
        await conduct_turn(context, provider=provider)

    assert len(provider.calls) == 1


@pytest.mark.asyncio
async def test_conductor_rejects_invalid_json_without_repair_or_fallback() -> None:
    context = _context()
    provider = FakeConductorProvider({"message_text": "Hoje custa a partir de..."})

    with pytest.raises(ConductorDecisionValidationError):
        await conduct_turn(context, provider=provider)

    assert len(provider.calls) == 1


@pytest.mark.asyncio
async def test_conductor_rejects_decision_that_does_not_match_turn_context() -> None:
    context = _context()
    payload = _valid_decision_payload(context)
    payload["turn_id"] = "turn_from_other_context"
    provider = FakeConductorProvider(payload)

    with pytest.raises(ConductorDecisionValidationError):
        await conduct_turn(context, provider=provider)

    assert len(provider.calls) == 1
