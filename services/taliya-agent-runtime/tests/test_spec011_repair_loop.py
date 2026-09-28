from __future__ import annotations

from typing import Any

import pytest

from app.core.taliya_commercial.context_builder import build_turn_context
from app.core.taliya_commercial.repair import (
    RepairProviderRequest,
    repair_conductor_decision,
)
from app.core.taliya_commercial.schemas import (
    ConductorDecision,
    TurnContext,
)
from app.core.taliya_commercial.validators import validate_conductor_result
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import RuntimeState

PAIN_FIRST_TEXT = "perco muitos interessados no WhatsApp porque a equipe demora para responder"


def _request(text: str = "tem demo?", *, sender_name: str = "Ana") -> AgentRunRequest:
    return AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "whatsapp",
            "conversation": {
                "conversation_id": "conv_repair_1",
                "lead_id": "lead_repair_1",
                "channel_conversation_id": "wa_repair_1",
                "source": "pilates_landing",
            },
            "message": {
                "idempotency_key": "wa:conv_repair_1:1",
                "channel_message_id": "wamid_repair_1",
                "type": "text",
                "text": text,
            },
            "sender": {"name": sender_name},
            "metadata": {"page_path": "/pilates"},
        }
    )


def _context(
    text: str = "tem demo?",
    *,
    product_knowledge_keys: list[str] | None = None,
) -> TurnContext:
    return build_turn_context(
        turn_id="turn_repair_1",
        request=_request(text),
        state=RuntimeState(
            conversation_id="conv_repair_1",
            agent_key="taliya_commercial",
            current_agent_name="taliya_commercial_product_agent",
            summary="Lead pediu demonstracao do produto.",
            diagnostic={"status": "not_started", "ledger": []},
            waitlist={"status": "none"},
            demo={"status": "not_offered"},
        ),
        recent_events=[],
        product_knowledge_keys=product_knowledge_keys or ["links", "prices", "plans"],
        spec006_contract_keys=["product_positioning"],
    )


def _fresh_context(text: str, *, sender_name: str = "Ana") -> TurnContext:
    return build_turn_context(
        turn_id="turn_repair_fresh",
        request=_request(text, sender_name=sender_name),
        state=None,
        recent_events=[],
        product_knowledge_keys=["links", "prices", "plans", "whatsapp_scope"],
        spec006_contract_keys=["product_positioning"],
    )


def _completed_diagnostic_context(text: str) -> TurnContext:
    completed_ledger = [
        {
            "question_key": "active_students_or_size",
            "status": "answered",
            "answer_value": "95 alunos",
            "evidence": ["95 alunos ativos"],
            "confidence": "high",
            "may_ask_again": False,
        },
        {
            "question_key": "main_pain",
            "status": "answered",
            "answer_value": "perde interessados no whatsapp",
            "evidence": ["perco interessados no whatsapp"],
            "confidence": "high",
            "may_ask_again": False,
        },
        {
            "question_key": "pain_detail",
            "status": "inferred_from_prior_message",
            "answer_value": "interessados se perdem no atendimento e follow-up",
            "evidence": ["perco interessados no whatsapp"],
            "confidence": "high",
            "may_ask_again": False,
        },
        {
            "question_key": "current_process",
            "status": "answered",
            "answer_value": "planilha e whatsapp",
            "evidence": ["hoje fica em planilha e whatsapp"],
            "confidence": "high",
            "may_ask_again": False,
        },
        {
            "question_key": "priority",
            "status": "answered",
            "answer_value": "vendas primeiro",
            "evidence": ["prioridade e vendas primeiro"],
            "confidence": "high",
            "may_ask_again": False,
        },
        {
            "question_key": "urgency",
            "status": "answered",
            "answer_value": "resolver agora",
            "evidence": ["quero resolver agora"],
            "confidence": "high",
            "may_ask_again": False,
        },
    ]
    return build_turn_context(
        turn_id="turn_repair_completed_diagnostic",
        request=_request(text),
        state=RuntimeState(
            conversation_id="conv_repair_1",
            agent_key="taliya_commercial",
            current_agent_name="taliya_commercial_diagnostic_agent",
            summary="Diagnostico concluido para studio com 95 alunos.",
            diagnostic={"status": "completed", "ledger": completed_ledger},
            waitlist={"status": "none"},
            demo={"status": "not_offered"},
        ),
        recent_events=[],
        product_knowledge_keys=["links", "prices", "plans"],
        spec006_contract_keys=["product_positioning"],
    )


def _pending_urgency_context(text: str) -> TurnContext:
    pending_ledger = [
        {
            "question_key": "active_students_or_size",
            "status": "answered",
            "answer_value": "95 alunos",
            "evidence": ["95 alunos ativos"],
            "confidence": "high",
            "may_ask_again": False,
        },
        {
            "question_key": "main_pain",
            "status": "answered",
            "answer_value": "perde interessados no whatsapp",
            "evidence": ["perco interessados no whatsapp"],
            "confidence": "high",
            "may_ask_again": False,
        },
        {
            "question_key": "pain_detail",
            "status": "inferred_from_prior_message",
            "answer_value": "interessados se perdem no atendimento e follow-up",
            "evidence": ["perco interessados no whatsapp"],
            "confidence": "high",
            "may_ask_again": False,
        },
        {
            "question_key": "current_process",
            "status": "answered",
            "answer_value": "planilha e whatsapp",
            "evidence": ["hoje fica em planilha e whatsapp"],
            "confidence": "high",
            "may_ask_again": False,
        },
        {
            "question_key": "priority",
            "status": "answered",
            "answer_value": "vendas primeiro",
            "evidence": ["prioridade e vendas primeiro"],
            "confidence": "high",
            "may_ask_again": False,
        },
        {
            "question_key": "urgency",
            "status": "missing",
            "evidence": ["Voces estao buscando resolver isso agora?"],
            "confidence": "high",
            "may_ask_again": True,
        },
    ]
    return build_turn_context(
        turn_id="turn_repair_pending_urgency",
        request=_request(text),
        state=RuntimeState(
            conversation_id="conv_repair_1",
            agent_key="taliya_commercial",
            current_agent_name="taliya_commercial_diagnostic_agent",
            summary="Diagnostico aguardando urgencia.",
            diagnostic={"status": "in_progress", "ledger": pending_ledger},
            waitlist={"status": "none"},
            demo={"status": "not_offered"},
        ),
        recent_events=[],
        product_knowledge_keys=["links", "prices", "plans"],
        spec006_contract_keys=["product_positioning"],
    )


def _widget_empty_context() -> TurnContext:
    request = AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "widget",
            "conversation": {
                "conversation_id": "conv_repair_widget_empty",
                "lead_id": "lead_repair_widget_empty",
                "channel_conversation_id": "browser_repair_widget_empty",
                "source": "pilates_landing",
                "entry_intent": "widget",
            },
            "message": {
                "idempotency_key": "widget:repair-empty:1",
                "channel_message_id": "web_repair_empty_1",
                "type": "text",
                "text": "",
            },
            "sender": {},
            "metadata": {"page_path": "/pilates", "source_section": "floating_agent"},
        }
    )
    return build_turn_context(
        turn_id="turn_repair_widget_empty",
        request=request,
        state=None,
        recent_events=[],
        product_knowledge_keys=["links", "prices", "plans"],
        spec006_contract_keys=["product_positioning"],
    )


def _diagnostic_cta_context() -> TurnContext:
    request = AgentRunRequest.model_validate(
        {
            "agent_key": "taliya_commercial",
            "channel": "widget",
            "conversation": {
                "conversation_id": "conv_repair_diagnostic_cta",
                "lead_id": "lead_repair_diagnostic_cta",
                "channel_conversation_id": "browser_repair_diagnostic_cta",
                "source": "pilates_landing",
                "entry_intent": "diagnostic_cta",
            },
            "message": {
                "idempotency_key": "widget:repair-diagnostic-cta:1",
                "channel_message_id": "web_repair_diagnostic_cta_1",
                "type": "text",
                "text": "pode fazer meu diagnostico?",
            },
            "sender": {},
            "metadata": {"page_path": "/pilates", "source_section": "diagnostic_cta"},
        }
    )
    return build_turn_context(
        turn_id="turn_repair_diagnostic_cta",
        request=request,
        state=None,
        recent_events=[],
        product_knowledge_keys=["links", "prices", "plans"],
        spec006_contract_keys=["product_positioning"],
    )


def _decision_payload(
    context: TurnContext,
    *,
    include_demo_link: bool,
) -> dict[str, Any]:
    variables: dict[str, Any] = {}
    if include_demo_link:
        variables["official_demo_link"] = {
            "kind": "url",
            "value": "https://www.taliya.com.br/pilates/planos/demonstracao",
            "source": "official_product_knowledge",
            "evidence": ["product_knowledge.links.demonstration"],
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


def _decision(context: TurnContext, *, include_demo_link: bool) -> ConductorDecision:
    return ConductorDecision.model_validate(
        _decision_payload(context, include_demo_link=include_demo_link)
    )


def _price_decision_payload(
    context: TurnContext,
    *,
    include_price_hook: bool,
    diagnostic_action: str = "offer",
) -> dict[str, Any]:
    plan_price_summary = {
        "kind": "long_text",
        "value": "Base R$ 197/mes; Essencial R$ 497/mes; Avance R$ 897/mes; Completo R$ 1.497/mes.",
        "source": "official_product_knowledge",
        "evidence": ["product_knowledge.prices"],
        "max_length": 360,
    }
    items: list[dict[str, Any]] = [
        {
            "template_id": "product.price_direct",
            "variables": {"plan_price_summary": plan_price_summary},
        }
    ]
    if include_price_hook:
        items.append({"template_id": "diagnostic.price_hook", "variables": {}})
    return {
        "schema_version": "011.0",
        "turn_id": context.turn_id,
        "conversation_id": context.conversation_id,
        "channel": context.channel,
        "agent_key": context.agent_key,
        "role": "product",
        "route": "product",
        "previous_state": "new_lead",
        "current_state": "price_question",
        "next_state": "diagnostic_offered",
        "detected_intents": ["price_question"],
        "direct_question_present": True,
        "direct_question_answered_first": True,
        "diagnostic": {"action": diagnostic_action},
        "language_policy": {
            "register": "studio_owner_practical",
            "crm_term_policy": "avoid_by_default",
        },
        "template_plan": {"items": items},
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


def _bad_price_decision_payload(context: TurnContext) -> dict[str, Any]:
    payload = _price_decision_payload(context, include_price_hook=False)
    payload["template_plan"]["items"][0]["variables"]["plan_price_summary"]["value"] = (
        "Plano inventado R$ 297/mes."
    )
    return payload


def _how_it_works_decision_payload(context: TurnContext) -> dict[str, Any]:
    payload = _price_decision_payload(context, include_price_hook=True)
    payload.update(
        {
            "current_state": "answering_product_question",
            "next_state": "diagnostic_offer",
            "detected_intents": ["how_it_works", "product_overview"],
            "diagnostic": {"action": "offer"},
            "template_plan": {
                "items": [
                    {
                        "template_id": "product.overview_short",
                        "variables": {
                            "product_fact_summary": {
                                "kind": "long_text",
                                "value": "Taliya organiza a rotina do studio.",
                                "source": "official_product_knowledge",
                                "evidence": ["product_knowledge.plans"],
                                "max_length": 320,
                            }
                        },
                    }
                ]
            },
        }
    )
    return payload


def _how_it_works_redundant_decision_payload(context: TurnContext) -> dict[str, Any]:
    payload = _how_it_works_decision_payload(context)
    payload["template_plan"] = {
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
            },
            {
                "template_id": "diagnostic.offer_soft",
                "variables": {
                    "pain_context_human": {
                        "kind": "long_text",
                        "value": "Voce quer entender como a Taliya funciona na pratica.",
                        "source": "diagnostic_ledger",
                        "evidence": ["user_message"],
                        "max_length": 320,
                    }
                },
            },
        ]
    }
    return payload


def _integration_handoff_decision_payload(context: TurnContext) -> dict[str, Any]:
    inbound_text = context.inbound.text or "integra com Instagram e com meu sistema atual?"
    return {
        "schema_version": "011.0",
        "turn_id": context.turn_id,
        "conversation_id": context.conversation_id,
        "channel": context.channel,
        "agent_key": context.agent_key,
        "role": "handoff",
        "route": "handoff",
        "previous_state": "new_lead",
        "current_state": "handoff_requested",
        "next_state": "handoff_requested",
        "detected_intents": [
            "integration_question",
            "current_system_question",
            "instagram_integration_question",
        ],
        "direct_question_present": True,
        "direct_question_answered_first": False,
        "handoff": {
            "status": "requested",
            "reason": "confirmar integracao com Instagram e sistema atual",
        },
        "language_policy": {
            "register": "studio_owner_practical",
            "crm_term_policy": "avoid_by_default",
        },
        "template_plan": {
            "items": [
                {
                    "template_id": "handoff.acknowledge",
                    "variables": {
                        "handoff_reason": {
                            "kind": "short_text",
                            "value": "confirmar integracao com Instagram e sistema atual",
                            "source": "user_message",
                            "evidence": [inbound_text],
                            "max_length": 120,
                        }
                    },
                }
            ]
        },
        "policy_checks": {
            "direct_question_answered_first": False,
            "diagnostic_timing_ok": True,
            "waitlist_timing_ok": True,
            "official_facts_only": True,
            "no_internal_text_leak": True,
            "no_early_contact_capture": True,
            "no_human_overlap": True,
        },
        "confidence": "medium",
    }


def _cold_greeting_bad_diagnostic_payload(context: TurnContext) -> dict[str, Any]:
    payload = _price_decision_payload(context, include_price_hook=False)
    payload.update(
        {
            "role": "diagnostic",
            "route": "diagnostic",
            "current_state": "diagnostic_started",
            "next_state": "diagnostic_in_progress",
            "detected_intents": ["greeting", "diagnostic"],
            "direct_question_present": False,
            "direct_question_answered_first": True,
            "demo": {
                "customer_facing_concept": "commercial_product_demo",
                "status": "not_offered",
                "next_step": "none",
            },
            "diagnostic": {
                "action": "ask_next",
                "next_question_key": "active_students_or_size",
            },
            "template_plan": {
                "items": [{"template_id": "diagnostic.ask_active_students"}]
            },
        }
    )
    return payload


def _plan_fit_bad_source_payload(context: TurnContext) -> dict[str, Any]:
    payload = _price_decision_payload(context, include_price_hook=True)
    payload.update(
        {
            "current_state": "plan_fit_question",
            "next_state": "diagnostic_offered",
            "detected_intents": ["plan_fit_question"],
            "diagnostic": {"action": "offer"},
            "template_plan": {
                "items": [
                    {
                        "template_id": "product.plan_fit_with_diagnostic",
                        "variables": {
                            "plan_fit_context": {
                                "kind": "short_text",
                                "value": "Voce quer entender se a Taliya serve pro seu studio.",
                                "source": "runtime_state",
                                "evidence": ["runtime_state.plan_fit_context"],
                                "max_length": 180,
                            }
                        },
                    }
                ]
            },
        }
    )
    return payload


def _plan_fit_missing_answer_payload(context: TurnContext) -> dict[str, Any]:
    payload = _price_decision_payload(context, include_price_hook=False)
    payload.update(
        {
            "role": "product",
            "route": "product",
            "current_state": "plan_fit_question",
            "next_state": "diagnostic_offered",
            "detected_intents": ["plan_recommendation", "pricing_fit"],
            "direct_question_present": True,
            "direct_question_answered_first": True,
            "demo": {
                "customer_facing_concept": "commercial_product_demo",
                "status": "not_offered",
                "next_step": "none",
            },
            "diagnostic": {"action": "offer", "next_question_key": "main_pain"},
            "template_plan": {"items": [{"template_id": "diagnostic.ask_main_pain"}]},
        }
    )
    return payload


def _whatsapp_incomplete_payload(context: TurnContext) -> dict[str, Any]:
    payload = _price_decision_payload(context, include_price_hook=False)
    payload.update(
        {
            "current_state": "whatsapp_question",
            "next_state": "product_question",
            "detected_intents": ["product_question", "whatsapp_product_question"],
            "direct_question_present": True,
            "direct_question_answered_first": True,
            "diagnostic": {"action": "none"},
            "template_plan": {
                "items": [
                    {
                        "template_id": "product.whatsapp_direct",
                        "variables": {
                            "product_fact_summary": {
                                "kind": "long_text",
                                "value": "Os alunos nao precisam baixar app nem criar senha.",
                                "source": "official_product_knowledge",
                                "evidence": ["product_knowledge.whatsapp_scope"],
                                "max_length": 320,
                            }
                        },
                    }
                ]
            },
        }
    )
    return payload


def _widget_empty_bad_site_cta_payload(context: TurnContext) -> dict[str, Any]:
    payload = _price_decision_payload(context, include_price_hook=False)
    payload.update(
        {
            "role": "entry",
            "route": "entry",
            "current_state": "site_opening",
            "next_state": "diagnostic_offered",
            "detected_intents": ["site_cta"],
            "direct_question_present": False,
            "direct_question_answered_first": True,
            "demo": {
                "customer_facing_concept": "commercial_product_demo",
                "status": "not_offered",
                "next_step": "none",
            },
            "diagnostic": {"action": "offer"},
            "template_plan": {"items": [{"template_id": "opening.site_cta"}]},
        }
    )
    return payload


def _sensitive_data_bad_handoff_payload(context: TurnContext) -> dict[str, Any]:
    payload = _price_decision_payload(context, include_price_hook=False)
    payload.update(
        {
            "role": "safety",
            "route": "safe_fallback",
            "current_state": "sensitive_data",
            "next_state": "sensitive_data",
            "detected_intents": ["sensitive_data", "cpf_provided"],
            "direct_question_present": True,
            "direct_question_answered_first": True,
            "diagnostic": {"action": "none"},
            "waitlist": {"eligibility": "unknown", "status": "none"},
            "handoff": {"status": "requested", "reason": "sensitive_data_provided"},
            "template_plan": {"items": [{"template_id": "safety.sensitive_data"}]},
        }
    )
    return payload


def _diagnostic_question_without_feedback_payload(context: TurnContext) -> dict[str, Any]:
    payload = _price_decision_payload(context, include_price_hook=True)
    payload.update(
        {
            "role": "diagnostic",
            "route": "diagnostic",
            "current_state": "diagnostic_in_progress",
            "next_state": "diagnostic_in_progress",
            "detected_intents": ["diagnostic", "pain_mention"],
            "direct_question_present": False,
            "direct_question_answered_first": True,
            "diagnostic": {
                "action": "ask_next",
                "next_question_key": "current_process",
                "ledger_updates": [
                    {
                        "question_key": "main_pain",
                        "status": "answered",
                        "answer_value": "reposicao baguncada no studio",
                        "evidence": ["user_message"],
                        "confidence": "high",
                        "may_ask_again": False,
                    },
                    {
                        "question_key": "current_process",
                        "status": "missing",
                        "evidence": ["user_message"],
                        "confidence": "medium",
                        "may_ask_again": True,
                    },
                ],
            },
            "template_plan": {
                "items": [
                    {
                        "template_id": "diagnostic.ask_current_process",
                        "variables": {},
                    }
                ]
            },
        }
    )
    return payload


def _diagnostic_complete_missing_urgency_payload(context: TurnContext) -> dict[str, Any]:
    payload = _diagnostic_question_without_feedback_payload(context)
    payload.update(
        {
            "current_state": "diagnostic_ready",
            "next_state": "diagnostic_delivered",
            "diagnostic": {
                "action": "complete",
                "next_question_key": None,
                "ledger_updates": [
                    {
                        "question_key": "active_students_or_size",
                        "status": "answered",
                        "answer_value": "120 alunos",
                        "evidence": ["user_message"],
                        "confidence": "high",
                        "may_ask_again": False,
                    },
                    {
                        "question_key": "main_pain",
                        "status": "answered",
                        "answer_value": "atendimento e follow-up",
                        "evidence": ["user_message"],
                        "confidence": "high",
                        "may_ask_again": False,
                    },
                    {
                        "question_key": "pain_detail",
                        "status": "answered",
                        "answer_value": "perde interessados no WhatsApp",
                        "evidence": ["user_message"],
                        "confidence": "high",
                        "may_ask_again": False,
                    },
                    {
                        "question_key": "current_process",
                        "status": "answered",
                        "answer_value": "planilha",
                        "evidence": ["user_message"],
                        "confidence": "high",
                        "may_ask_again": False,
                    },
                    {
                        "question_key": "priority",
                        "status": "answered",
                        "answer_value": "vendas",
                        "evidence": ["user_message"],
                        "confidence": "high",
                        "may_ask_again": False,
                    },
                    {
                        "question_key": "urgency",
                        "status": "missing",
                        "evidence": ["user_message"],
                        "confidence": "low",
                        "may_ask_again": True,
                    },
                ],
                "final_fields": {"recommended_plan_or_range": "Completo"},
            },
            "template_plan": {"items": [{"template_id": "diagnostic.deliver_hold"}]},
        }
    )
    return payload


def _diagnostic_complete_missing_pain_detail_bad_plan_evidence_payload(
    context: TurnContext,
) -> dict[str, Any]:
    payload = _diagnostic_complete_missing_urgency_payload(context)
    payload["diagnostic"]["ledger_updates"] = [
        {
            "question_key": "active_students_or_size",
            "status": "answered",
            "answer_value": "120 alunos",
            "evidence": ["user_message"],
            "confidence": "high",
            "may_ask_again": False,
        },
        {
            "question_key": "main_pain",
            "status": "answered",
            "answer_value": "atendimento e follow-up",
            "evidence": ["user_message"],
            "confidence": "high",
            "may_ask_again": False,
        },
        {
            "question_key": "pain_detail",
            "status": "missing",
            "evidence": ["user_message"],
            "confidence": "low",
            "may_ask_again": True,
        },
        {
            "question_key": "current_process",
            "status": "answered",
            "answer_value": "planilha",
            "evidence": ["user_message"],
            "confidence": "high",
            "may_ask_again": False,
        },
        {
            "question_key": "priority",
            "status": "answered",
            "answer_value": "vendas",
            "evidence": ["user_message"],
            "confidence": "high",
            "may_ask_again": False,
        },
        {
            "question_key": "urgency",
            "status": "answered",
            "answer_value": "resolver nesse mes",
            "evidence": ["user_message"],
            "confidence": "high",
            "may_ask_again": False,
        },
    ]
    payload["template_plan"] = {
        "items": [
            {
                "template_id": "diagnostic.deliver_plan_recommendation",
                "variables": {
                    "recommended_plan_or_range": {
                        "kind": "short_text",
                        "value": "Completo",
                        "source": "official_product_knowledge",
                        "evidence": ["product_knowledge.unknown_plan_hint"],
                        "max_length": 90,
                    }
                },
            }
        ]
    }
    return payload


def _diagnostic_complete_repaired_payload(context: TurnContext) -> dict[str, Any]:
    payload = _diagnostic_complete_missing_pain_detail_bad_plan_evidence_payload(context)
    for update in payload["diagnostic"]["ledger_updates"]:
        if update["question_key"] == "pain_detail":
            update.update(
                {
                    "status": "inferred_from_prior_message",
                    "answer_value": "perde interessados no WhatsApp",
                    "confidence": "high",
                    "may_ask_again": False,
                }
            )
    payload["template_plan"] = {
        "items": [
            {"template_id": "diagnostic.deliver_hold"},
            {
                "template_id": "diagnostic.deliver_plan_recommendation",
                "variables": {
                    "recommended_plan_or_range": {
                        "kind": "short_text",
                        "value": "Taliya completa",
                        "source": "official_product_knowledge",
                        "evidence": ["product_knowledge.unknown_plan_hint"],
                        "max_length": 90,
                    }
                },
            },
            {
                "template_id": "diagnostic.deliver_context",
                "variables": {
                    "pain_context_human": {
                        "kind": "long_text",
                        "value": (
                            "Pelo que voce contou, o peso principal esta em perder "
                            "interessados no WhatsApp e deixar follow-ups dependentes "
                            "de planilha, memoria da equipe e retorno manual."
                        ),
                        "source": "diagnostic_ledger",
                        "evidence": ["user_message"],
                        "max_length": 320,
                    }
                },
            },
            {
                "template_id": "diagnostic.deliver_agent_recommendation",
                "variables": {
                    "agent_name": {
                        "kind": "short_text",
                        "value": "Atendimento",
                        "source": "official_product_knowledge",
                        "evidence": ["product_knowledge.agents"],
                        "max_length": 60,
                    },
                    "agent_fit_phrase": {
                        "kind": "enum",
                        "value": "faria sentido primeiro",
                        "source": "model_decision",
                        "evidence": ["model_decision"],
                    },
                    "agent_pain_resolved": {
                        "kind": "long_text",
                        "value": "interessados que ficam sem resposta",
                        "source": "diagnostic_ledger",
                        "evidence": ["user_message"],
                        "max_length": 180,
                    },
                    "agent_recommendation_reason": {
                        "kind": "long_text",
                        "value": "essa foi a dor comercial mais clara",
                        "source": "spec_006_product_contract",
                        "evidence": ["spec006.unknown_agents"],
                        "max_length": 220,
                    },
                    "agent_practical_action": {
                        "kind": "long_text",
                        "value": "ele organiza respostas, contexto e chamada para humano",
                        "source": "diagnostic_ledger",
                        "evidence": ["user_message"],
                        "max_length": 220,
                    },
                },
            },
        ]
    }
    return payload


def _usage() -> dict[str, Any]:
    return {
        "model": "gpt-5.4-mini",
        "input_tokens": 80,
        "output_tokens": 24,
        "cost_usd": 0.0009,
    }


class FakeRepairProvider:
    def __init__(self, output: Any) -> None:
        self.output = output
        self.calls: list[RepairProviderRequest] = []

    async def __call__(self, request: RepairProviderRequest) -> Any:
        self.calls.append(request)
        return self.output


@pytest.mark.asyncio
async def test_repair_loop_returns_not_needed_without_provider_call_when_valid() -> None:
    context = _context()
    decision = _decision(context, include_demo_link=True)
    validator_result = validate_conductor_result(decision, context)
    provider = FakeRepairProvider({})

    repair = await repair_conductor_decision(
        decision,
        context,
        validator_result,
        provider=provider,
    )

    assert repair.status == "not_needed"
    assert repair.attempted is False
    assert repair.attempt_count == 0
    assert provider.calls == []


@pytest.mark.asyncio
async def test_repair_loop_does_not_repair_blocked_p0_validator_result() -> None:
    context = _context()
    decision = _decision(context, include_demo_link=True).model_copy(
        update={"conversation_id": "conv_other"}
    )
    validator_result = validate_conductor_result(decision, context)
    provider = FakeRepairProvider({})

    repair = await repair_conductor_decision(
        decision,
        context,
        validator_result,
        provider=provider,
    )

    assert validator_result.status == "blocked"
    assert repair.status == "blocked"
    assert repair.attempted is False
    assert provider.calls == []


@pytest.mark.asyncio
async def test_repair_loop_calls_provider_once_and_revalidates_repaired_decision() -> None:
    context = _context()
    original_decision = _decision(context, include_demo_link=False)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider(
        {
            "decision": _decision_payload(context, include_demo_link=True),
            "model_usage": _usage(),
        }
    )

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert validator_result.status == "repairable"
    assert len(provider.calls) == 1
    request = provider.calls[0]
    assert request.context == context
    assert request.original_decision == original_decision
    assert request.validator_errors == validator_result.errors
    assert request.response_schema["title"] == "ConductorDecision"
    assert request.max_attempts == 1
    instructions = " ".join(request.instructions)
    assert "Return a flat ConductorDecision object" in instructions
    assert "product.price_direct" in instructions
    assert "diagnostic.price_hook for generic price questions" in instructions
    assert "For price-only turns, repair demo.status to not_offered" in instructions
    assert "diagnostic_inferable_pain_detail_should_complete" in instructions
    assert "diagnostic.deliver_hold" in instructions
    assert '"diagnostic.deliver":' not in instructions
    assert "Never use the legacy exact template id diagnostic.deliver" in instructions
    assert "Allowed fact source/reliability pairs" in instructions
    assert repair.status == "repaired"
    assert repair.attempted is True
    assert repair.attempt_count == 1
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.template_plan.items[0].variables
    assert repair.model_usage is not None
    assert repair.model_usage.input_tokens == 80
    assert not hasattr(repair, "rendered_messages")


@pytest.mark.asyncio
async def test_repair_loop_applies_structural_price_hook_without_provider_call() -> None:
    context = _context("quanto custa?")
    original_decision = ConductorDecision.model_validate(
        _price_decision_payload(context, include_price_hook=False)
    )
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert validator_result.status == "repairable"
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    assert repair.model_usage is None
    template_ids = [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ]
    assert template_ids == ["product.price_direct", "diagnostic.price_hook"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_sets_demo_direct_question_flags() -> None:
    context = _context("quero ver uma demonstracao")
    payload = _decision_payload(context, include_demo_link=True)
    payload["direct_question_present"] = False
    payload["direct_question_answered_first"] = False
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "demo_direct_question_flags_missing" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.direct_question_present is True
    assert repair.repaired_decision.direct_question_answered_first is True
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_clears_stale_price_intent_for_current_demo_request() -> None:
    context = _pending_urgency_context("me manda demo")
    payload = _decision_payload(context, include_demo_link=True)
    payload["detected_intents"] = ["price_question", "demo_request"]
    payload["direct_question_present"] = False
    payload["direct_question_answered_first"] = False
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert {
        "price_question_missing_price_answer",
        "price_question_missing_diagnostic_hook",
        "price_question_missing_diagnostic_offer",
        "demo_direct_question_flags_missing",
    }.issubset({error.code for error in validator_result.errors})
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.direct_question_present is True
    assert repair.repaired_decision.direct_question_answered_first is True
    assert repair.repaired_decision.detected_intents == ["demo_request"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_turns_post_diagnostic_demo_redelivery_into_demo_direct() -> None:
    context = _completed_diagnostic_context("me manda demo")
    payload = _diagnostic_complete_repaired_payload(context)
    payload["detected_intents"] = ["demo_request", "diagnostic_continuation"]
    payload["demo"] = {
        "customer_facing_concept": "commercial_product_demo",
        "status": "viewed_or_asked",
        "next_step": "offer_demo",
    }
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "post_diagnostic_demo_request_redelivered_diagnostic" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.route == "product"
    assert repair.repaired_decision.diagnostic.action == "none"
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["product.demo_direct"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_turns_incomplete_diagnostic_demo_request_into_demo_direct() -> None:
    context = _context("me manda demo")
    payload = _diagnostic_complete_missing_urgency_payload(context)
    payload["detected_intents"] = ["demo_request", "diagnostic_continuation"]
    payload["demo"] = {
        "customer_facing_concept": "commercial_product_demo",
        "status": "viewed_or_asked",
        "next_step": "offer_demo",
    }
    payload["template_plan"] = {"items": [{"template_id": "diagnostic.deliver_hold"}]}
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "diagnostic_final_demo_stage_missing" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.route == "product"
    assert repair.repaired_decision.diagnostic.action == "none"
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["product.demo_direct"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_turns_post_diagnostic_redelivery_order_error_into_demo_direct() -> None:
    context = _completed_diagnostic_context("me manda demo")
    payload = _diagnostic_complete_missing_urgency_payload(context)
    for update in payload["diagnostic"]["ledger_updates"]:
        if update["question_key"] == "urgency":
            update.update(
                {
                    "status": "answered",
                    "answer_value": "quero resolver agora",
                    "evidence": ["quero resolver agora"],
                    "confidence": "high",
                    "may_ask_again": False,
                }
            )
    payload.update(
        {
            "detected_intents": ["demo_request"],
            "demo": {
                "customer_facing_concept": "commercial_product_demo",
                "status": "viewed_or_asked",
                "next_step": "offer_demo",
            },
            "waitlist": {
                "eligibility": "eligible",
                "status": "pending_details",
                "missing_details": [],
            },
            "template_plan": {
                "items": [
                    {"template_id": "diagnostic.deliver_context"},
                    {"template_id": "diagnostic.deliver_hold"},
                ]
            },
        }
    )
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert {
        "diagnostic_final_staged_order_invalid",
        "post_diagnostic_demo_request_redelivered_diagnostic",
    }.issubset({error.code for error in validator_result.errors})
    assert provider.calls == []
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.route == "product"
    assert repair.repaired_decision.waitlist.status == "none"
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["product.demo_direct"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_removes_price_hook_after_diagnostic_refusal() -> None:
    context = _context("nao quero diagnostico agora, so me fala o preco")
    payload = _price_decision_payload(context, include_price_hook=True)
    payload["detected_intents"] = ["price_question", "diagnostic_refusal"]
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "diagnostic_refusal_not_respected" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.diagnostic.action == "none"
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["product.price_direct"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_adds_official_price_answer_before_price_hook() -> None:
    context = _context("quanto custa?")
    payload = _price_decision_payload(context, include_price_hook=True)
    payload["template_plan"]["items"] = [
        {"template_id": "diagnostic.price_hook", "variables": {}}
    ]
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "price_question_missing_price_answer" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["product.price_direct", "diagnostic.price_hook"]
    assert (
        repair.repaired_decision.template_plan.items[0]
        .variables["plan_price_summary"]
        .source
    ) == "official_product_knowledge"
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_replaces_unsupported_price_with_official_summary() -> None:
    context = _context("Vi o plano de 497 e tenho reposicao baguncada no studio")
    original_decision = ConductorDecision.model_validate(
        _bad_price_decision_payload(context)
    )
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert validator_result.status == "blocked"
    assert "unsupported_price_value" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    price_item = repair.repaired_decision.template_plan.items[0]
    assert price_item.variables["plan_price_summary"].value == (
        "Base: R$ 197/mes; Essencial: R$ 497/mes; "
        "Avance: R$ 897/mes; Completo: R$ 1.497/mes."
    )
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_replaces_unsupported_plan_direct_price() -> None:
    context = _context("quanto custa o Completo?")
    payload = _bad_price_decision_payload(context)
    payload["template_plan"]["items"][0]["template_id"] = "product.plan_direct"
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    template_ids = [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ]
    assert template_ids == ["product.plan_direct", "diagnostic.price_hook"]
    assert repair.repaired_decision.diagnostic.action == "offer"
    assert (
        repair.repaired_decision.template_plan.items[0]
        .variables["plan_price_summary"]
        .value
    ) == "O plano Completo custa R$ 1.497/mes."
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_adds_grounded_diagnostic_answer_feedback() -> None:
    context = _context("Vi o plano de 497 e tenho reposicao baguncada no studio")
    original_decision = ConductorDecision.model_validate(
        _diagnostic_question_without_feedback_payload(context)
    )
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "diagnostic_question_missing_answer_feedback" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.repaired_decision is not None
    variables = repair.repaired_decision.template_plan.items[0].variables
    assert variables["answer_feedback"].value == (
        "Entendi: reposicao baguncada no studio."
    )
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_replaces_english_diagnostic_feedback_leak() -> None:
    context = _context(
        "perco muitos interessados no WhatsApp porque a equipe demora para responder"
    )
    payload = _diagnostic_question_without_feedback_payload(context)
    payload["diagnostic"]["ledger_updates"][0].update(
        {
            "answer_value": (
                "lead loses many interested leads because the team takes too long "
                "to reply"
            ),
            "evidence": [
                "perco muitos interessados no WhatsApp porque a equipe demora para responder"
            ],
        }
    )
    payload["template_plan"]["items"][0]["variables"]["answer_feedback"] = {
        "kind": "short_text",
        "value": (
            "Entendi: lead loses many interested leads because the team takes too "
            "long to reply."
        ),
        "source": "diagnostic_ledger",
        "evidence": [
            "perco muitos interessados no WhatsApp porque a equipe demora para responder"
        ],
        "max_length": 180,
    }
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "diagnostic_feedback_language_leak" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    feedback = repair.repaired_decision.template_plan.items[0].variables[
        "answer_feedback"
    ]
    assert feedback.value == (
        "Entendi: perco muitos interessados no WhatsApp porque a equipe demora "
        "para responder."
    )
    assert "lead loses" not in feedback.value
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_adds_price_answer_before_diagnostic_question() -> None:
    context = _context("Vi o plano de 497 e tenho reposicao baguncada no studio")
    payload = _diagnostic_question_without_feedback_payload(context)
    payload["detected_intents"].append("price_question")
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert {
        "price_question_missing_price_answer",
        "diagnostic_question_missing_answer_feedback",
    }.issubset({error.code for error in validator_result.errors})
    assert provider.calls == []
    assert repair.repaired_decision is not None
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == [
        "product.price_direct",
        "diagnostic.price_hook",
        "diagnostic.ask_current_process",
    ]
    question_variables = repair.repaired_decision.template_plan.items[2].variables
    assert question_variables["answer_feedback"].source == "diagnostic_ledger"
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_removes_product_route_question_after_price_plus_pain() -> None:
    context = _context("tenho reposicao baguncada na agenda e queria saber preco")
    payload = _price_decision_payload(context, include_price_hook=False)
    payload.update(
        {
            "detected_intents": ["price_question", "pain_statement"],
            "diagnostic": {
                "action": "ask_next",
                "next_question_key": "current_process",
                "ledger_updates": [
                    {
                        "question_key": "main_pain",
                        "status": "answered",
                        "answer_value": "reposicao baguncada na agenda",
                        "evidence": ["user_message"],
                        "confidence": "high",
                        "may_ask_again": False,
                    }
                ],
            },
            "template_plan": {
                "items": [
                    payload["template_plan"]["items"][0],
                    {
                        "template_id": "diagnostic.price_hook_with_context",
                        "variables": {
                            "plan_fit_context": {
                                "kind": "short_text",
                                "value": (
                                    "Voce comentou que a reposicao esta baguncada "
                                    "na agenda."
                                ),
                                "source": "user_message",
                                "evidence": [
                                    "tenho reposicao baguncada na agenda e queria saber preco"
                                ],
                                "max_length": 180,
                            }
                        },
                    },
                    {"template_id": "diagnostic.ask_current_process", "variables": {}},
                ]
            },
        }
    )
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "product_route_must_not_ask_diagnostic_question" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.diagnostic.action == "offer"
    assert repair.repaired_decision.diagnostic.next_question_key is None
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["product.price_direct", "diagnostic.price_hook_with_context"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_replaces_invalid_diagnostic_feedback_source() -> None:
    context = _context("Vi o plano de 497 e tenho reposicao baguncada no studio")
    payload = _diagnostic_question_without_feedback_payload(context)
    payload["template_plan"]["items"][0]["variables"]["answer_feedback"] = {
        "kind": "short_text",
        "value": "Entendi.",
        "source": "model_decision",
        "evidence": ["model_decision"],
        "max_length": 180,
    }
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "template_plan_invalid" in [error.code for error in validator_result.errors]
    assert provider.calls == []
    assert repair.repaired_decision is not None
    repaired_feedback = repair.repaired_decision.template_plan.items[0].variables[
        "answer_feedback"
    ]
    assert repaired_feedback.source == "diagnostic_ledger"
    assert repaired_feedback.value == "Entendi: reposicao baguncada no studio."
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_retargets_diagnostic_question_that_is_not_missing() -> None:
    context = _context("agenda e reposicoes")
    payload = _diagnostic_question_without_feedback_payload(context)
    for update in payload["diagnostic"]["ledger_updates"]:
        if update["question_key"] == "current_process":
            update["status"] = "answered"
            update["answer_value"] = "planilha"
            update["confidence"] = "high"
            update["may_ask_again"] = False
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "diagnostic_next_question_not_missing" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.diagnostic.next_question_key == (
        "active_students_or_size"
    )
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["diagnostic.ask_active_students"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_turns_incomplete_final_diagnostic_into_missing_question() -> None:
    context = _context("quero diagnostico gratuito com vendas")
    original_decision = ConductorDecision.model_validate(
        _diagnostic_complete_missing_urgency_payload(context)
    )
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert validator_result.status == "blocked"
    assert "diagnostic_required_field_missing" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.diagnostic.action == "ask_next"
    assert repair.repaired_decision.diagnostic.next_question_key == "urgency"
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["diagnostic.ask_urgency"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_answers_price_before_reopening_missing_urgency() -> None:
    context = _context("achei caro")
    payload = _diagnostic_complete_missing_urgency_payload(context)
    payload.update(
        {
            "detected_intents": ["price_objection"],
            "direct_question_present": True,
            "direct_question_answered_first": False,
            "policy_checks": {
                **payload["policy_checks"],
                "direct_question_answered_first": False,
            },
        }
    )
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert {
        "diagnostic_required_field_missing",
        "diagnostic_urgency_must_be_next",
    }.issubset({error.code for error in validator_result.errors})
    assert provider.calls == []
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.direct_question_answered_first is True
    assert repair.repaired_decision.diagnostic.action == "ask_next"
    assert repair.repaired_decision.diagnostic.next_question_key == "urgency"
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["product.price_direct", "product.price_objection_value", "diagnostic.ask_urgency"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_reopens_urgency_when_priority_evidence_was_used() -> None:
    context = _context("quero diagnostico gratuito com vendas")
    payload = _diagnostic_complete_missing_urgency_payload(context)
    for update in payload["diagnostic"]["ledger_updates"]:
        if update["question_key"] == "priority":
            update["evidence"] = ["a prioridade agora e vendas"]
        if update["question_key"] == "urgency":
            update["status"] = "answered"
            update["answer_value"] = "agora"
            update["evidence"] = ["a prioridade agora e vendas"]
            update["confidence"] = "medium"
            update["may_ask_again"] = False
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "diagnostic_urgency_evidence_is_priority" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.diagnostic.action == "ask_next"
    assert repair.repaired_decision.diagnostic.next_question_key == "urgency"
    urgency_update = next(
        item
        for item in repair.repaired_decision.diagnostic.ledger_updates
        if item.question_key == "urgency"
    )
    assert urgency_update.status == "missing"
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["diagnostic.ask_urgency"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_starts_diagnostic_with_active_students_question() -> None:
    context = _context("pode fazer diagnostico")
    payload = _price_decision_payload(context, include_price_hook=False)
    payload.update(
        {
            "role": "diagnostic",
            "route": "diagnostic",
            "current_state": "diagnostic_started",
            "next_state": "diagnostic_in_progress",
            "detected_intents": ["diagnostic_acceptance"],
            "direct_question_present": False,
            "direct_question_answered_first": True,
            "diagnostic": {
                "action": "start",
                "next_question_key": "priority",
                "ledger_updates": [],
            },
            "demo": {
                "customer_facing_concept": "commercial_product_demo",
                "status": "not_offered",
                "next_step": "none",
            },
            "template_plan": {"items": [{"template_id": "diagnostic.ask_priority"}]},
        }
    )
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "diagnostic_start_must_ask_active_students" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.diagnostic.next_question_key == (
        "active_students_or_size"
    )
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["diagnostic.ask_active_students"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_preserves_pain_first_offer_before_active_students_question() -> None:
    context = _fresh_context(PAIN_FIRST_TEXT)
    payload = _price_decision_payload(context, include_price_hook=False)
    payload.update(
        {
            "schema_version": "011.conductor_decision.v1",
            "role": "diagnostic",
            "route": "diagnostic",
            "current_state": "diagnostic_offered",
            "next_state": "diagnostic_waiting_acceptance",
            "detected_intents": ["pain_statement", "diagnostic_relevant"],
            "direct_question_present": False,
            "direct_question_answered_first": True,
            "diagnostic": {
                "action": "offer",
                "next_question_key": "urgency",
                "ledger_updates": [
                    {
                        "question_key": "main_pain",
                        "status": "answered",
                        "answer_value": "perco interessados no WhatsApp",
                        "evidence": [PAIN_FIRST_TEXT],
                        "confidence": "high",
                    }
                ],
            },
            "demo": {
                "customer_facing_concept": "commercial_product_demo",
                "status": "not_offered",
                "next_step": "none",
            },
            "template_plan": {
                "items": [
                    {
                        "template_id": "diagnostic.offer_soft",
                        "variables": {
                            "pain_context_human": {
                                "kind": "long_text",
                                "value": (
                                    "Você está perdendo interessados porque o "
                                    "atendimento no WhatsApp demora."
                                ),
                                "source": "user_message",
                                "evidence": [PAIN_FIRST_TEXT],
                                "max_length": 420,
                            }
                        },
                    },
                    {"template_id": "diagnostic.ask_urgency", "variables": {}},
                ]
            },
        }
    )
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "diagnostic_start_must_ask_active_students" in [
        error.code for error in validator_result.errors
    ]
    assert "unsupported_schema_version" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.schema_version == "011.0"
    assert repair.repaired_decision.diagnostic.next_question_key == (
        "active_students_or_size"
    )
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == [
        "opening.cold_greeting",
        "diagnostic.offer_soft",
        "diagnostic.ask_active_students",
    ]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_adds_pain_first_offer_before_first_question() -> None:
    context = _fresh_context(PAIN_FIRST_TEXT)
    payload = _price_decision_payload(context, include_price_hook=False)
    payload.update(
        {
            "role": "diagnostic",
            "route": "diagnostic",
            "current_state": "diagnostic_asked_active_students",
            "next_state": "diagnostic_in_progress",
            "detected_intents": ["pain_statement", "diagnostic_relevant"],
            "direct_question_present": False,
            "direct_question_answered_first": True,
            "diagnostic": {
                "action": "ask_next",
                "next_question_key": "active_students_or_size",
                "ledger_updates": [
                    {
                        "question_key": "main_pain",
                        "status": "answered",
                        "answer_value": "perco interessados no WhatsApp",
                        "evidence": [PAIN_FIRST_TEXT],
                        "confidence": "high",
                    }
                ],
            },
            "demo": {
                "customer_facing_concept": "commercial_product_demo",
                "status": "not_offered",
                "next_step": "none",
            },
            "template_plan": {
                "items": [
                    {"template_id": "diagnostic.ask_active_students", "variables": {}}
                ]
            },
        }
    )
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "pain_first_must_offer_diagnostic" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.diagnostic.next_question_key == (
        "active_students_or_size"
    )
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == [
        "opening.cold_greeting",
        "diagnostic.offer_soft",
        "diagnostic.ask_active_students",
    ]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_reopens_urgency_when_assistant_prompt_was_used() -> None:
    assistant_prompt = (
        "Voces estao buscando resolver isso agora ou so pesquisando por enquanto?"
    )
    context = _context("meu foco principal e vendas")
    context = context.model_copy(
        update={
            "recent_transcript": [
                {
                    "role": "assistant",
                    "content": assistant_prompt,
                    "source": "runtime_state",
                }
            ]
        }
    )
    payload = _diagnostic_complete_missing_urgency_payload(context)
    for update in payload["diagnostic"]["ledger_updates"]:
        if update["question_key"] == "urgency":
            update["status"] = "answered"
            update["answer_value"] = "agora"
            update["evidence"] = [assistant_prompt]
            update["confidence"] = "medium"
            update["may_ask_again"] = False
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "diagnostic_urgency_evidence_is_assistant_prompt" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.diagnostic.next_question_key == "urgency"
    urgency_update = next(
        item
        for item in repair.repaired_decision.diagnostic.ledger_updates
        if item.question_key == "urgency"
    )
    assert urgency_update.status == "missing"
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["diagnostic.ask_urgency"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_reopens_urgency_when_evidence_has_no_timing() -> None:
    context = _context("quero diagnostico gratuito com vendas")
    payload = _diagnostic_complete_missing_urgency_payload(context)
    for update in payload["diagnostic"]["ledger_updates"]:
        if update["question_key"] == "urgency":
            update["status"] = "answered"
            update["answer_value"] = "quer comparar o plano Completo agora"
            update["evidence"] = ["Quero comparar plano para a Taliya completa"]
            update["confidence"] = "medium"
            update["may_ask_again"] = False
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "diagnostic_urgency_evidence_not_timing" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.diagnostic.next_question_key == "urgency"
    urgency_update = next(
        item
        for item in repair.repaired_decision.diagnostic.ledger_updates
        if item.question_key == "urgency"
    )
    assert urgency_update.status == "missing"
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["diagnostic.ask_urgency"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_reopens_urgency_before_final_stage_repairs() -> None:
    context = _context("hoje fica em planilha e whatsapp")
    payload = _diagnostic_complete_missing_urgency_payload(context)
    payload["diagnostic"]["ledger_updates"][-1] = {
        "question_key": "urgency",
        "status": "missing",
        "answer_value": None,
        "evidence": [],
        "confidence": "low",
        "may_ask_again": True,
    }
    payload["demo"] = {
        "customer_facing_concept": "commercial_product_demo",
        "status": "viewed_or_asked",
        "next_step": "offer_demo",
    }
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "diagnostic_required_field_missing" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.diagnostic.action == "ask_next"
    assert repair.repaired_decision.diagnostic.next_question_key == "urgency"
    assert repair.repaired_decision.demo.next_step == "none"
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_clears_stale_completed_diagnostic_on_waitlist_followup() -> None:
    context = _completed_diagnostic_context("quero comecar, me coloca na lista")
    payload = _decision_payload(context, include_demo_link=False)
    payload.update(
        {
            "role": "waitlist",
            "route": "waitlist",
            "current_state": "waitlist_offered",
            "next_state": "waitlist_offered",
            "detected_intents": ["waitlist_interest"],
            "direct_question_present": False,
            "direct_question_answered_first": True,
            "diagnostic": {"action": "complete"},
            "waitlist": {
                "eligibility": "eligible",
                "status": "offered",
                "missing_details": [],
            },
            "template_plan": {
                "items": [
                    {
                        "template_id": "waitlist.offer_after_contract_intent",
                        "variables": {
                            "waitlist_context_summary": {
                                "kind": "long_text",
                                "value": "Lead quer entrar na lista depois do diagnostico.",
                                "source": "runtime_state",
                                "evidence": ["runtime_state.diagnostic.status"],
                                "max_length": 220,
                            }
                        },
                    }
                ]
            },
        }
    )
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "diagnostic_final_demo_stage_missing" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.diagnostic.action == "none"
    assert repair.repaired_decision.route == "waitlist"
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_prioritizes_handoff_over_incomplete_diagnostic() -> None:
    context = _completed_diagnostic_context("quero falar com alguem")
    payload = _diagnostic_complete_missing_urgency_payload(context)
    payload.update(
        {
            "detected_intents": ["request_human"],
            "handoff": {
                "status": "requested",
                "reason": "quero falar com alguem",
            },
            "template_plan": {"items": [{"template_id": "diagnostic.deliver_hold"}]},
        }
    )
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert provider.calls == []
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.route == "handoff"
    assert repair.repaired_decision.handoff.status == "requested"
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["handoff.acknowledge"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_clears_stale_demo_offer_on_price_followup() -> None:
    context = _completed_diagnostic_context("achei caro")
    payload = _price_decision_payload(context, include_price_hook=False)
    payload.update(
        {
            "previous_state": "diagnostic_completed_demo_viewed_or_asked",
            "current_state": "product_price_objection",
            "next_state": "product_followup",
            "detected_intents": ["price_objection"],
            "diagnostic": {"action": "complete"},
            "demo": {
                "customer_facing_concept": "commercial_product_demo",
                "status": "viewed_or_asked",
                "next_step": "offer_demo",
            },
        }
    )
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "demo_offer_template_missing" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.diagnostic.action == "none"
    assert repair.repaired_decision.demo.next_step == "none"
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["product.price_direct", "product.price_objection_value"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_rebuilds_price_objection_from_stale_demo_direct() -> None:
    context = _completed_diagnostic_context("achei caro")
    payload = _decision_payload(context, include_demo_link=True)
    payload.update(
        {
            "previous_state": "diagnostic_completed_demo_viewed_or_asked",
            "current_state": "demo_question",
            "next_state": "demo_offered",
            "detected_intents": ["price_objection", "demo_followup"],
            "diagnostic": {"action": "none"},
            "demo": {
                "customer_facing_concept": "commercial_product_demo",
                "status": "viewed_or_asked",
                "next_step": "offer_demo",
            },
        }
    )
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert {
        "price_question_missing_price_answer",
        "stale_demo_direct_without_current_request",
    }.issubset({error.code for error in validator_result.errors})
    assert provider.calls == []
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.diagnostic.action == "none"
    assert repair.repaired_decision.demo.next_step == "none"
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["product.price_direct", "product.price_objection_value"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_recovers_value_objection_when_model_reuses_stale_demo() -> None:
    context = _completed_diagnostic_context("achei caro")
    payload = _decision_payload(context, include_demo_link=True)
    payload.update(
        {
            "previous_state": "diagnostic_completed_demo_viewed_or_asked",
            "current_state": "demo_question",
            "next_state": "demo_offered",
            "detected_intents": ["demo_followup"],
            "direct_question_present": False,
            "direct_question_answered_first": False,
            "diagnostic": {
                "action": "complete",
                "ledger_updates": context.diagnostic_ledger,
                "final_fields": {"recommended_plan_or_range": "Essencial"},
            },
            "demo": {
                "customer_facing_concept": "commercial_product_demo",
                "status": "viewed_or_asked",
                "next_step": "offer_demo",
            },
            "template_plan": {
                "items": [
                    payload["template_plan"]["items"][0],
                    {"template_id": "diagnostic.deliver_plan_recommendation"},
                ]
            },
            "policy_checks": {
                **payload["policy_checks"],
                "direct_question_answered_first": False,
            },
        }
    )
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert {
        "diagnostic_final_demo_stage_missing",
        "diagnostic_final_staged_order_invalid",
        "stale_demo_direct_without_current_request",
        "demo_direct_question_flags_missing",
    }.issubset({error.code for error in validator_result.errors})
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.route == "product"
    assert repair.repaired_decision.detected_intents == ["price_objection"]
    assert repair.repaired_decision.diagnostic.action == "none"
    assert repair.repaired_decision.demo.next_step == "none"
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["product.price_direct", "product.price_objection_value"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_rebuilds_waitlist_intent_from_stale_demo_direct() -> None:
    context = _completed_diagnostic_context("quero comecar, me coloca na lista")
    payload = _decision_payload(context, include_demo_link=True)
    payload.update(
        {
            "previous_state": "diagnostic_completed_demo_viewed_or_asked",
            "current_state": "demo_question",
            "next_state": "demo_offered",
            "detected_intents": ["contract_intent", "waitlist_intent", "demo_followup"],
            "diagnostic": {"action": "none"},
            "demo": {
                "customer_facing_concept": "commercial_product_demo",
                "status": "viewed_or_asked",
                "next_step": "offer_demo",
            },
        }
    )
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert {
        "waitlist_contract_intent_missing_offer",
        "stale_demo_direct_without_current_request",
    }.issubset({error.code for error in validator_result.errors})
    assert provider.calls == []
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.route == "waitlist"
    assert repair.repaired_decision.demo.next_step == "none"
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["waitlist.offer_after_contract_intent"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_rebuilds_price_answer_when_template_variable_is_invalid() -> None:
    context = _context("quanto custa?")
    payload = _price_decision_payload(context, include_price_hook=False)
    payload["template_plan"] = {
        "items": [
            {
                "template_id": "diagnostic.price_hook",
                "variables": {
                    "plan_price_summary": {
                        "kind": "long_text",
                        "value": "Base R$ 197/mes.",
                        "source": "official_product_knowledge",
                        "evidence": ["product_knowledge.prices"],
                        "max_length": 360,
                    }
                },
            }
        ]
    }
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert {"template_plan_invalid", "price_question_missing_price_answer"}.issubset(
        {error.code for error in validator_result.errors}
    )
    assert provider.calls == []
    assert repair.repaired_decision is not None
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["product.price_direct", "diagnostic.price_hook"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_sets_price_diagnostic_offer_after_deduping_offer_templates() -> None:
    context = _context("quanto custa?")
    payload = _price_decision_payload(
        context,
        include_price_hook=True,
        diagnostic_action="none",
    )
    payload["template_plan"]["items"].append(
        {"template_id": "diagnostic.offer_soft", "variables": {}}
    )
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    expected_errors = {
        "price_question_missing_diagnostic_offer",
        "duplicate_diagnostic_offer_templates",
    }
    assert expected_errors.issubset(
        {error.code for error in validator_result.errors}
    )
    assert provider.calls == []
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.diagnostic.action == "offer"
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["product.price_direct", "diagnostic.price_hook"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_marks_price_objection_hook_as_diagnostic_offer_when_pending() -> None:
    context = _pending_urgency_context("achei caro")
    payload = _price_decision_payload(context, include_price_hook=False)
    payload.update(
        {
            "detected_intents": ["price_question", "price_objection"],
            "diagnostic": {"action": "none"},
            "template_plan": {
                "items": [
                    {
                        "template_id": "product.price_objection_value",
                        "variables": {},
                    }
                ]
            },
        }
    )
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "price_question_missing_diagnostic_offer" in {
        error.code for error in validator_result.errors
    }
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.diagnostic.action == "offer"
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_sends_pending_urgency_answer_to_llm_repair() -> None:
    context = _pending_urgency_context("quero resolver agora")
    payload = _diagnostic_complete_missing_urgency_payload(context)
    payload["diagnostic"]["action"] = "ask_next"
    payload["diagnostic"]["next_question_key"] = "urgency"
    payload["template_plan"] = {
        "items": [{"template_id": "diagnostic.ask_urgency", "variables": {}}]
    }
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider(
        {
            "decision": _diagnostic_complete_repaired_payload(context),
            "model_usage": _usage(),
        }
    )

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "diagnostic_urgency_answer_not_captured" in [
        error.code for error in validator_result.errors
    ]
    assert len(provider.calls) == 1
    assert "diagnostic_urgency_answer_not_captured" in [
        error.code for error in provider.calls[0].validator_errors
    ]
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.diagnostic.action == "complete"
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_sends_invalid_diagnostic_next_question_to_llm_repair() -> None:
    context = _pending_urgency_context("quero resolver agora")
    payload = _diagnostic_complete_missing_urgency_payload(context)
    payload["diagnostic"]["action"] = "ask_next"
    payload["diagnostic"]["next_question_key"] = "plan_fit_context"
    payload["template_plan"] = {
        "items": [
            {
                "template_id": "diagnostic.ask_urgency",
                "variables": {
                    "answer_feedback": {
                        "kind": "short_text",
                        "value": "Entendi.",
                        "source": "model_decision",
                        "evidence": ["model_decision"],
                        "max_length": 180,
                    }
                },
            }
        ]
    }
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider(
        {
            "decision": _diagnostic_complete_repaired_payload(context),
            "model_usage": _usage(),
        }
    )

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "diagnostic_next_question_invalid" in [
        error.code for error in validator_result.errors
    ]
    assert "template_plan_invalid" in [
        error.code for error in validator_result.errors
    ]
    assert len(provider.calls) == 1
    assert "diagnostic_next_question_invalid" in [
        error.code for error in provider.calls[0].validator_errors
    ]
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.diagnostic.action == "complete"
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_allows_llm_repair_for_inferable_pain_detail_and_evidence() -> None:
    context = _context(
        "quero diagnostico. Tenho 120 alunos, perco interessados no WhatsApp, "
        "uso planilha, prioridade vendas e e urgente nesse mes."
    )
    original_decision = ConductorDecision.model_validate(
        _diagnostic_complete_missing_pain_detail_bad_plan_evidence_payload(context)
    )
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider(
        {
            "decision": _diagnostic_complete_repaired_payload(context),
            "model_usage": _usage(),
        }
    )

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert validator_result.status == "blocked"
    assert "diagnostic_inferable_pain_detail_should_complete" in [
        error.code for error in validator_result.errors
    ]
    assert "product_claim_source_missing" in [
        error.code for error in validator_result.errors
    ]
    assert len(provider.calls) == 1
    instructions = " ".join(provider.calls[0].instructions)
    assert "product_claim_source_missing" in instructions
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    template_ids = [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ]
    assert template_ids[:4] == [
        "diagnostic.deliver_hold",
        "diagnostic.deliver_context",
        "diagnostic.deliver_crm_base",
        "diagnostic.deliver_operational_step",
    ]
    assert any(
        template_id.startswith("diagnostic.deliver_agent_recommendation")
        for template_id in template_ids[4:-2]
    )
    assert template_ids[-2:] == [
        "diagnostic.deliver_plan_recommendation",
        "diagnostic.deliver_demo_not_offered",
    ]
    plan_item = repair.repaired_decision.template_plan.items[-2]
    plan_variables = plan_item.variables
    assert plan_variables["recommended_plan_or_range"].value == "Completo"
    assert plan_variables["recommended_plan_or_range"].evidence == [
        "product_knowledge.plans"
    ]
    agent_variables = repair.repaired_decision.template_plan.items[4].variables
    assert agent_variables["agent_name"].evidence == ["product_knowledge.plans"]
    assert agent_variables["agent_recommendation_reason"].source == "diagnostic_ledger"
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_normalizes_final_diagnostic_plan_source_and_stages() -> None:
    context = _context(
        "tenho 120 alunos, perco interessados no WhatsApp, uso planilha, "
        "prioridade vendas e e urgente agora"
    )
    payload = _diagnostic_complete_missing_urgency_payload(context)
    for update in payload["diagnostic"]["ledger_updates"]:
        if update["question_key"] == "urgency":
            update.update(
                {
                    "status": "answered",
                    "answer_value": "urgente agora",
                    "evidence": ["e urgente agora"],
                    "confidence": "high",
                    "may_ask_again": False,
                }
            )
    payload["template_plan"] = {
        "items": [
            {
                "template_id": "diagnostic.deliver_plan_recommendation",
                "variables": {
                    "recommended_plan_or_range": {
                        "kind": "short_text",
                        "value": "Essencial",
                        "source": "diagnostic_ledger",
                        "evidence": ["priority vendas"],
                        "max_length": 90,
                    }
                },
            }
        ]
    }
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert {
        "product_claim_source_invalid",
        "diagnostic_final_demo_stage_missing",
        "diagnostic_final_staged_order_invalid",
    }.issubset({error.code for error in validator_result.errors})
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    template_ids = [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ]
    assert template_ids[:4] == [
        "diagnostic.deliver_hold",
        "diagnostic.deliver_context",
        "diagnostic.deliver_crm_base",
        "diagnostic.deliver_operational_step",
    ]
    assert any(
        template_id.startswith("diagnostic.deliver_agent_recommendation")
        for template_id in template_ids[4:-2]
    )
    assert template_ids[-2:] == [
        "diagnostic.deliver_plan_recommendation",
        "diagnostic.deliver_demo_not_offered",
    ]
    plan_item = repair.repaired_decision.template_plan.items[-2]
    plan_variables = plan_item.variables
    assert plan_variables["recommended_plan_or_range"].source == (
        "official_product_knowledge"
    )
    assert plan_variables["recommended_plan_or_range"].evidence == [
        "product_knowledge.plans"
    ]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_uses_ledger_for_unresolved_final_diagnostic_plan() -> None:
    context = _completed_diagnostic_context("quero resolver agora")
    payload = _diagnostic_complete_missing_urgency_payload(context)
    payload["diagnostic"]["ledger_updates"] = context.diagnostic_ledger
    payload["diagnostic"]["final_fields"] = {"recommended_plan_or_range": "Essencial"}
    payload["template_plan"] = {
        "items": [
            {
                "template_id": "diagnostic.deliver_plan_recommendation",
                "variables": {
                    "recommended_plan_or_range": {
                        "kind": "short_text",
                        "value": "Essencial",
                        "source": "official_product_knowledge",
                        "evidence": ["product_knowledge.unknown_plan_hint"],
                        "max_length": 90,
                    }
                },
            }
        ]
    }
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert {
        "unresolved_product_evidence",
        "product_claim_source_missing",
        "diagnostic_final_demo_stage_missing",
        "diagnostic_final_staged_order_invalid",
    }.issubset({error.code for error in validator_result.errors})
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    template_ids = [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ]
    assert template_ids[:4] == [
        "diagnostic.deliver_hold",
        "diagnostic.deliver_context",
        "diagnostic.deliver_crm_base",
        "diagnostic.deliver_operational_step",
    ]
    assert any(
        template_id.startswith("diagnostic.deliver_agent_recommendation")
        for template_id in template_ids[4:-2]
    )
    assert template_ids[-2:] == [
        "diagnostic.deliver_plan_recommendation",
        "diagnostic.deliver_demo_not_offered",
    ]
    plan_item = repair.repaired_decision.template_plan.items[-2]
    plan_variables = plan_item.variables
    assert plan_variables["recommended_plan_or_range"].evidence == [
        "product_knowledge.plans"
    ]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_normalizes_final_diagnostic_sources_and_demo_stage() -> None:
    context = _context(
        "tenho 95 alunos, perco interessados no WhatsApp, uso planilha, "
        "prioridade vendas e e urgente agora"
    )
    payload = _diagnostic_complete_repaired_payload(context)
    payload["template_plan"]["items"] = [
        item
        for item in payload["template_plan"]["items"]
        if item["template_id"] != "diagnostic.deliver_demo_not_offered"
    ]
    agent_variables = payload["template_plan"]["items"][3]["variables"]
    for variable_name in ("agent_pain_resolved", "agent_practical_action"):
        agent_variables[variable_name]["source"] = "official_product_knowledge"
        agent_variables[variable_name]["evidence"] = ["product_knowledge.plans"]
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert {
        "template_plan_invalid",
        "diagnostic_final_demo_stage_missing",
    }.issubset({error.code for error in validator_result.errors})
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    repaired_agent_variables = repair.repaired_decision.template_plan.items[4].variables
    assert repaired_agent_variables["agent_pain_resolved"].source == "diagnostic_ledger"
    assert repaired_agent_variables["agent_practical_action"].source == "diagnostic_ledger"
    assert repair.repaired_decision.template_plan.items[-1].template_id == (
        "diagnostic.deliver_demo_not_offered"
    )
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_completes_final_diagnostic_when_last_pending_answer_captured() -> None:
    context = _pending_urgency_context("quero resolver agora")
    payload = _diagnostic_complete_missing_urgency_payload(context)
    payload["diagnostic"]["action"] = "ask_next"
    payload["diagnostic"]["next_question_key"] = "urgency"
    for update in payload["diagnostic"]["ledger_updates"]:
        if update["question_key"] == "urgency":
            update.update(
                {
                    "status": "answered",
                    "answer_value": "quero resolver agora",
                    "evidence": ["quero resolver agora"],
                    "confidence": "high",
                    "may_ask_again": False,
                }
            )
    payload["template_plan"] = {"items": [{"template_id": "diagnostic.deliver_hold"}]}
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert {
        "diagnostic_next_question_not_missing",
        "diagnostic_final_demo_stage_missing",
        "diagnostic_final_staged_order_invalid",
    }.issubset({error.code for error in validator_result.errors})
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.diagnostic.action == "complete"
    assert repair.repaired_decision.diagnostic.next_question_key is None
    template_ids = [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ]
    assert template_ids[:4] == [
        "diagnostic.deliver_hold",
        "diagnostic.deliver_context",
        "diagnostic.deliver_crm_base",
        "diagnostic.deliver_operational_step",
    ]
    assert template_ids[-1] == "diagnostic.deliver_demo_not_offered"
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_applies_structural_how_it_works_template() -> None:
    context = _context("como funciona a Taliya na pratica?")
    original_decision = ConductorDecision.model_validate(
        _how_it_works_decision_payload(context)
    )
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert validator_result.status == "repairable"
    assert "how_it_works_template_missing" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    template_ids = [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ]
    assert template_ids == ["product.how_it_works_direct"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_rebuilds_invalid_how_it_works_without_completing_diagnostic() -> None:
    context = _completed_diagnostic_context("como funciona mesmo?")
    payload = _diagnostic_complete_missing_urgency_payload(context)
    payload.update(
        {
            "role": "product",
            "route": "product",
            "detected_intents": ["how_it_works_question"],
            "direct_question_present": True,
            "direct_question_answered_first": True,
            "demo": {
                "customer_facing_concept": "commercial_product_demo",
                "status": "viewed_or_asked",
                "next_step": "offer_demo",
            },
            "waitlist": {
                "eligibility": "eligible",
                "status": "pending_details",
                "missing_details": [],
            },
            "template_plan": {
                "items": [
                    {
                        "template_id": "product.how_it_works_direct",
                        "variables": {
                            "product_fact_summary": {
                                "kind": "long_text",
                                "value": "A Taliya organiza a rotina do studio.",
                                "source": "official_product_knowledge",
                                "evidence": ["product_knowledge.how_it_works"],
                                "max_length": 320,
                            }
                        },
                    }
                ]
            },
        }
    )
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "template_plan_invalid" in [error.code for error in validator_result.errors]
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.diagnostic.action == "none"
    assert repair.repaired_decision.demo.next_step == "none"
    assert repair.repaired_decision.waitlist.status == "none"
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["product.how_it_works_direct"]
    variables = repair.repaired_decision.template_plan.items[0].variables
    assert set(variables) == {"contextual_next_step"}
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_rebuilds_post_diagnostic_how_it_works_from_stale_final() -> None:
    context = _completed_diagnostic_context("como funciona mesmo?")
    payload = _diagnostic_complete_missing_urgency_payload(context)
    payload["diagnostic"]["ledger_updates"] = context.diagnostic_ledger
    payload.update(
        {
            "role": "product",
            "route": "product",
            "detected_intents": ["how_it_works", "product_how_it_works"],
            "direct_question_present": True,
            "direct_question_answered_first": True,
            "demo": {
                "customer_facing_concept": "commercial_product_demo",
                "status": "viewed_or_asked",
                "next_step": "offer_demo",
            },
            "template_plan": {
                "items": [
                    {
                        "template_id": "product.how_it_works_direct",
                        "variables": {
                            "product_fact_summary": {
                                "kind": "long_text",
                                "value": "Taliya organiza a rotina do studio.",
                                "source": "official_product_knowledge",
                                "evidence": ["product_knowledge.how_it_works"],
                                "max_length": 320,
                            }
                        },
                    },
                    {"template_id": "diagnostic.deliver_context"},
                ]
            },
        }
    )
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert {
        "template_plan_invalid",
        "diagnostic_final_staged_order_invalid",
    }.issubset({error.code for error in validator_result.errors})
    assert "post_diagnostic_demo_request_redelivered_diagnostic" not in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.route == "product"
    assert repair.repaired_decision.demo.next_step == "none"
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["product.how_it_works_direct"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_removes_redundant_how_it_works_followup() -> None:
    context = _context("como funciona a Taliya na pratica?")
    original_decision = ConductorDecision.model_validate(
        _how_it_works_redundant_decision_payload(context)
    )
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "how_it_works_redundant_followup" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.repaired_decision is not None
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["product.how_it_works_direct"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_answers_integration_scope_before_handoff() -> None:
    context = _context(
        "integra com Instagram e com meu sistema atual?",
        product_knowledge_keys=["integration_scope", "unsupported_claims"],
    )
    original_decision = ConductorDecision.model_validate(
        _integration_handoff_decision_payload(context)
    )
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "integration_scope_handoff_without_product_answer" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.route == "product"
    assert repair.repaired_decision.handoff.status == "none"
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["product.integration_scope_direct"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_keeps_pure_cold_greeting_out_of_diagnostic() -> None:
    context = _fresh_context("bom dia")
    original_decision = ConductorDecision.model_validate(
        _cold_greeting_bad_diagnostic_payload(context)
    )
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "cold_greeting_must_stay_entry" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.route == "entry"
    assert repair.repaired_decision.diagnostic.action == "none"
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["opening.cold_greeting"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_adds_reliable_first_name_to_cold_greeting() -> None:
    context = _fresh_context("oi", sender_name="Mariana Costa")
    payload = _price_decision_payload(context, include_price_hook=False)
    payload.update(
        {
            "role": "entry",
            "route": "entry",
            "current_state": "greeting_only",
            "next_state": "greeting_only",
            "detected_intents": ["greeting"],
            "direct_question_present": False,
            "diagnostic": {"action": "none"},
            "waitlist": {"eligibility": "unknown", "status": "none"},
            "template_plan": {"items": [{"template_id": "opening.cold_greeting"}]},
        }
    )
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "cold_greeting_reliable_name_missing" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    item = repair.repaired_decision.template_plan.items[0]
    assert item.template_id == "opening.cold_greeting_named"
    assert item.variables["first_name"].value == "Mariana"
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_removes_unreliable_first_name_from_cold_greeting() -> None:
    context = _fresh_context("oi", sender_name="Studio Viva Pilates")
    payload = _price_decision_payload(context, include_price_hook=False)
    payload.update(
        {
            "role": "entry",
            "route": "entry",
            "current_state": "greeting_only",
            "next_state": "greeting_only",
            "detected_intents": ["greeting"],
            "direct_question_present": False,
            "diagnostic": {"action": "none"},
            "waitlist": {"eligibility": "unknown", "status": "none"},
            "template_plan": {
                "items": [
                    {
                        "template_id": "opening.cold_greeting_named",
                        "variables": {
                            "first_name": {
                                "kind": "short_text",
                                "value": "Studio Viva Pilates",
                                "source": "channel_metadata",
                                "evidence": ["sender.name"],
                                "max_length": 40,
                            }
                        },
                    }
                ]
            },
        }
    )
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "cold_greeting_unreliable_name_used" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["opening.cold_greeting"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_rewrites_invalid_template_variable_source() -> None:
    context = _fresh_context("serve pro meu studio?")
    original_decision = ConductorDecision.model_validate(
        _plan_fit_bad_source_payload(context)
    )
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "template_plan_invalid" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    variable = repair.repaired_decision.template_plan.items[0].variables[
        "plan_fit_context"
    ]
    assert variable.source == "user_message"
    assert variable.evidence == ["serve pro meu studio?"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_restores_empty_widget_opening_template() -> None:
    context = _widget_empty_context()
    original_decision = ConductorDecision.model_validate(
        _widget_empty_bad_site_cta_payload(context)
    )
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "widget_empty_must_use_opening_template" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.route == "entry"
    assert repair.repaired_decision.diagnostic.action == "offer"
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["opening.widget_empty_diagnostic"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_removes_duplicate_diagnostic_cta_start_copy() -> None:
    context = _diagnostic_cta_context()
    payload = _price_decision_payload(context, include_price_hook=False)
    payload.update(
        {
            "role": "diagnostic",
            "route": "diagnostic",
            "current_state": "diagnostic_opening",
            "next_state": "diagnostic_in_progress",
            "detected_intents": ["request_diagnostic", "diagnostic_cta"],
            "direct_question_present": True,
            "direct_question_answered_first": False,
            "diagnostic": {
                "action": "start",
                "next_question_key": "active_students_or_size",
            },
            "template_plan": {
                "items": [
                    {"template_id": "opening.diagnostic_cta"},
                    {"template_id": "diagnostic.start"},
                    {"template_id": "diagnostic.ask_active_students"},
                ]
            },
        }
    )
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "diagnostic_cta_duplicate_start_template" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.direct_question_answered_first is True
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["opening.diagnostic_cta", "diagnostic.ask_active_students"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_keeps_sensitive_data_on_safe_fallback() -> None:
    context = _fresh_context("meu cpf e 12345678901, usa isso para cadastro?")
    original_decision = ConductorDecision.model_validate(
        _sensitive_data_bad_handoff_payload(context)
    )
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert {
        "handoff_route_mismatch",
        "handoff_ack_template_missing",
    }.issubset({error.code for error in validator_result.errors})
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.route == "safe_fallback"
    assert repair.repaired_decision.handoff.status == "none"
    assert repair.repaired_decision.facts == []
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["safety.sensitive_data"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_replaces_plan_fit_question_only_with_owner_copy() -> None:
    context = _fresh_context("qual plano voce recomenda pra mim?")
    original_decision = ConductorDecision.model_validate(
        _plan_fit_missing_answer_payload(context)
    )
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "plan_fit_direct_answer_template_missing" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.diagnostic.action == "offer"
    assert repair.repaired_decision.policy_checks.official_facts_only is False
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["product.plan_fit_with_diagnostic"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_normalizes_plan_fit_price_label_without_price_hook() -> None:
    context = _fresh_context("qual plano voce recomenda pra mim?")
    payload = _plan_fit_missing_answer_payload(context)
    payload["detected_intents"] = ["price_fit_question"]
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert "price_question_missing_diagnostic_hook" in [
        error.code for error in validator_result.errors
    ]
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.detected_intents == ["plan_fit_question"]
    assert [
        item.template_id for item in repair.repaired_decision.template_plan.items
    ] == ["product.plan_fit_with_diagnostic"]
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_completes_whatsapp_answer_from_product_knowledge() -> None:
    context = _fresh_context("como funciona no WhatsApp?")
    original_decision = ConductorDecision.model_validate(
        _whatsapp_incomplete_payload(context)
    )
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert {
        "whatsapp_direct_answer_incomplete",
        "whatsapp_direct_demo_link_missing",
    }.issubset({error.code for error in validator_result.errors})
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    variables = repair.repaired_decision.template_plan.items[0].variables
    assert "baixar aplicativo" in variables["product_fact_summary"].value
    assert "atualiza o painel" in variables["product_fact_summary"].value
    assert variables["official_demo_link"].value.endswith("/pilates/planos/demonstracao")
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_drops_ungrounded_diagnostic_update_from_whatsapp_answer() -> None:
    context = _fresh_context("como funciona no WhatsApp?")
    payload = _whatsapp_incomplete_payload(context)
    payload["diagnostic"] = {
        "action": "none",
        "ledger_updates": [
            {
                "question_key": "main_pain",
                "status": "answered",
                "answer_value": "WhatsApp",
                "evidence": [],
                "confidence": "medium",
            }
        ],
    }
    original_decision = ConductorDecision.model_validate(payload)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider({"should_not": "be called"})

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert {
        "diagnostic_answer_evidence_missing",
        "whatsapp_direct_answer_incomplete",
    }.issubset({error.code for error in validator_result.errors})
    assert provider.calls == []
    assert repair.status == "repaired"
    assert repair.repaired_decision is not None
    assert repair.repaired_decision.diagnostic.ledger_updates == []
    assert validate_conductor_result(repair.repaired_decision, context).status == "passed"


@pytest.mark.asyncio
async def test_repair_loop_fails_if_repaired_decision_still_fails_validation() -> None:
    context = _context()
    original_decision = _decision(context, include_demo_link=False)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider(
        {
            "decision": _decision_payload(context, include_demo_link=False),
            "model_usage": _usage(),
        }
    )

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert repair.status == "failed"
    assert repair.attempted is True
    assert repair.attempt_count == 1
    assert repair.repaired_decision is None
    assert "template_plan_invalid" in repair.errors_sent


@pytest.mark.asyncio
async def test_repair_loop_fails_without_customer_facing_fallback_on_bad_provider_output() -> None:
    context = _context()
    original_decision = _decision(context, include_demo_link=False)
    validator_result = validate_conductor_result(original_decision, context)
    provider = FakeRepairProvider("essa seria uma resposta livre")

    repair = await repair_conductor_decision(
        original_decision,
        context,
        validator_result,
        provider=provider,
    )

    assert repair.status == "failed"
    assert repair.attempted is True
    assert repair.attempt_count == 1
    assert repair.repaired_decision is None
    assert "repair_provider_output_invalid" in repair.errors_sent
    assert not hasattr(repair, "fallback_message")
