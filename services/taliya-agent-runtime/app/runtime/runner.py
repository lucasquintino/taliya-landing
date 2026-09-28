from __future__ import annotations

import asyncio
import json
import re
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field

from app.runtime.events import RuntimeEvent
from app.runtime.schemas import (
    AgentMessage,
    AgentOutput,
    AgentRunRequest,
    AgentRunResponse,
    Confidence,
    DiagnosticAnswerInterpretation,
    DiagnosticOutput,
    HandoffOutput,
    LeadFact,
    RuntimeDecision,
    SourceRef,
    WaitlistAction,
)
from app.runtime.usage import build_usage_record, usage_from_tokens
from app.domains.taliya_commercial.behavior_policy import (
    AGENT_BY_ROUTE,
    BEHAVIOR_POLICY_PROMPT,
    BUY_INTENT_TOKENS,
    DIAGNOSTIC_AGENT,
    DIRECT_QUESTION_TOKENS,
    ENTRY_AGENT,
    HANDOFF_AGENT,
    HUMAN_TOKENS,
    PRODUCT_AGENT,
    TRIAGE_AGENT,
    WAITLIST_AGENT,
    assess_profile_name,
    has_any_token,
    is_cold_greeting_only,
    normalize_text,
    route_from_text,
)
from app.domains.taliya_commercial.context import TaliyaCommercialContext
from app.domains.taliya_commercial.diagnostic_ledger import (
    apply_diagnostic_answer_interpretation,
    infer_ledger_from_text,
    ledger_is_complete,
    next_question_key,
    next_question_text,
)
from app.domains.taliya_commercial.renderer import render_template_plan
from app.domains.taliya_commercial.state import next_state_after_response, normalize_state, state_for_route
from app.domains.taliya_commercial.templates import get_template, required_template_ids
from app.domains.taliya_commercial.tools import (
    extract_lead_facts_from_text,
    mark_waitlist,
    pause_for_human,
    resume_from_human,
    save_diagnostic_record,
    save_lead_facts,
)
from app.shared.memory.postgres import InMemoryMemoryStore, RuntimeState
from app.shared.product_knowledge.source import get_product_knowledge_source
from app.shared.guardrails.validators import redact_trace_payload
from app.settings import get_settings


class LLMStructuredDraft(BaseModel):
    current_agent: Literal[
        "taliya_commercial_entry_agent",
        "taliya_commercial_product_agent",
        "taliya_commercial_diagnostic_agent",
        "taliya_commercial_waitlist_agent",
        "taliya_commercial_handoff_agent",
    ] = ENTRY_AGENT
    decision: RuntimeDecision = Field(default_factory=RuntimeDecision)
    messages: list[str] = Field(default_factory=list, max_length=8)
    lead_facts: list[LeadFact] = Field(default_factory=list)
    diagnostic_answer_interpretation: DiagnosticAnswerInterpretation | None = None
    diagnostic: DiagnosticOutput | None = None
    waitlist_action: WaitlistAction | None = None
    handoff: HandoffOutput | None = None
    source_keys: list[str] = Field(default_factory=list)
    confidence: Confidence = "medium"


class ContextualIntentDecision(BaseModel):
    intent: Literal[
        "accept_diagnostic",
        "accept_and_ask_direct_question",
        "ask_direct_question",
        "acknowledgement_only",
        "refuse_diagnostic",
        "human_request",
        "unclear",
    ] = "unclear"
    direct_question_kind: Literal["price_or_plan", "demo", "whatsapp", "product", "human", "none"] = "none"
    confidence: Confidence = "medium"
    reason: str = "contextual interpretation"


class SimpleOpeningDecision(BaseModel):
    route: Literal["price_direct", "demo_direct", "thin_diagnostic", "needs_full_agent"] = "needs_full_agent"
    confidence: Confidence = "medium"
    reason: str = "simple opening interpretation"


class InterleavedDeliveryDecision(BaseModel):
    action: Literal["suppress_acknowledgement", "process_normally"] = "process_normally"
    confidence: Confidence = "medium"
    reason: str = "interleaved delivery interpretation"


StandardCtaKind = Literal["site_cta", "diagnostic_cta", "demo_cta", "plan_compare_cta", "subscribe_cta"]

OFFICIAL_SITE_WHATSAPP_CTA = normalize_text(
    "Oi, vim pelo site da Taliya e quero entender se faz sentido para o meu studio de Pilates."
)


OPENING_TYPE_ALIASES = {
    "site_social_opening": "site_forced_message",
    "site_opening": "site_forced_message",
    "site_cta_opening": "site_forced_message",
    "source_site_opening": "site_forced_message",
    "landing_site_opening": "site_forced_message",
}


def _coerce_llm_structured_draft(raw_output: Any) -> LLMStructuredDraft | None:
    if isinstance(raw_output, LLMStructuredDraft):
        return raw_output
    payload: Any = raw_output
    if isinstance(raw_output, str):
        try:
            payload = json.loads(raw_output)
        except json.JSONDecodeError:
            start = raw_output.find("{")
            end = raw_output.rfind("}")
            if start < 0 or end <= start:
                return None
            try:
                payload = json.loads(raw_output[start : end + 1])
            except json.JSONDecodeError:
                return None
    if not isinstance(payload, dict):
        return None
    messages = payload.get("messages")
    if isinstance(messages, list) and len(messages) > 5:
        payload["messages"] = messages[:5]
    decision = payload.get("decision")
    if isinstance(decision, dict):
        opening_type = normalize_text(str(decision.get("opening_type") or ""))
        if opening_type in OPENING_TYPE_ALIASES:
            decision["opening_type"] = OPENING_TYPE_ALIASES[opening_type]
    return LLMStructuredDraft.model_validate(payload)


def _coerce_llm_structured_draft_from_exception(exc: Exception) -> LLMStructuredDraft | None:
    message = str(exc)
    marker = "Invalid JSON when parsing "
    start = message.find(marker)
    end = message.find(" for TypeAdapter", start)
    if start < 0 or end <= start:
        return None
    raw_payload = message[start + len(marker) : end]
    return _coerce_llm_structured_draft(raw_payload)


def repair_structured_output_once(output: AgentOutput, *, violation_code: str) -> AgentOutput:
    """Return a safe fallback output without advancing commercial state.

    This is the deterministic repair boundary after a model/output validation failure. It is not
    a conversational brain; it only suppresses unsafe state changes and produces an operational
    fallback that can be persisted and reviewed.
    """

    previous_state = normalize_state(output.decision.previous_state).value
    output.decision.current_state = previous_state
    output.decision.next_state = previous_state
    output.decision.route = "safe_fallback"
    output.decision.diagnostic_action = "none"
    output.decision.diagnostic_allowed_now = False
    output.decision.waitlist_allowed_now = False
    output.decision.template_ids = ["fallback.invalid_json"]
    output.decision.template_variables = {"fallback.invalid_json": {"violation_code": violation_code}}
    output.decision.render_plan = [
        {
            "template_id": "fallback.invalid_json",
            "reason": violation_code,
        }
    ]
    output.messages = [
        AgentMessage(
            text="Tive uma instabilidade para organizar a resposta. Vou deixar sua mensagem registrada para a equipe continuar com seguranca.",
            channel_hint=output.messages[0].channel_hint if output.messages else "widget",
            template_id="fallback.invalid_json",
        )
    ]
    output.diagnostic = None
    output.waitlist_action = None
    output.safety_flags = [*output.safety_flags, f"repaired:{violation_code}"]
    return output


def _previous_state_value(previous_state: RuntimeState | None) -> str:
    if previous_state and previous_state.last_decision:
        candidate = previous_state.last_decision.get("next_state") or previous_state.last_decision.get("current_state")
        if isinstance(candidate, str):
            return normalize_state(candidate).value
    if previous_state and previous_state.human_status == "active":
        return "paused_by_human"
    return "new_lead"


def _sync_decision_state(
    decision: RuntimeDecision,
    previous_state: RuntimeState | None,
    *,
    waitlist_status: str | None = None,
) -> RuntimeDecision:
    previous_value = _previous_state_value(previous_state)
    current = state_for_route(
        decision.route,
        opening_type=decision.opening_type,
        diagnostic_action=decision.diagnostic_action,
        waitlist_status=waitlist_status,
    )
    next_state = next_state_after_response(
        current,
        diagnostic_action=decision.diagnostic_action,
        waitlist_status=waitlist_status,
    )
    decision.previous_state = previous_value
    decision.current_state = current.value
    decision.next_state = next_state.value
    if decision.diagnostic_action in {"complete"}:
        decision.diagnostic_ledger_status = "complete"
        decision.facts_missing = []
        decision.next_question_kind = "none"
    elif decision.diagnostic_action in {"ask_next", "offer", "start", "insufficient_evidence"}:
        decision.diagnostic_ledger_status = "incomplete"
    return decision


def _default_template_ids(draft: LLMStructuredDraft) -> list[str]:
    decision = draft.decision
    if decision.template_ids and decision.diagnostic_action != "ask_next":
        cleaned = _sanitize_template_ids(decision.template_ids)
        if cleaned:
            return cleaned
    if decision.opening_type == "cold_greeting_only":
        if decision.profile_name_usage == "used_reliable_name":
            return ["opening.cold_greeting_named"]
        return ["opening.cold_greeting"]
    if decision.opening_type == "social_source_opening":
        return ["opening.instagram_source"]
    if decision.opening_type == "site_forced_message":
        return ["opening.site_cta"]
    if decision.opening_type == "diagnostic_cta_opening" and decision.diagnostic_action != "ask_next":
        return ["opening.diagnostic_cta"]
    if decision.opening_type == "widget_opening":
        return ["opening.widget_empty_diagnostic"]
    if decision.route == "handoff":
        return ["handoff.acknowledge"]
    if decision.route == "safe_fallback":
        if "prompt_injection" in decision.detected_intents:
            return ["safety.prompt_injection"]
        if "unsupported_media" in decision.detected_intents:
            return ["fallback.unsupported_media"]
        if "sensitive_data" in decision.detected_intents:
            return ["safety.sensitive_data"]
        return ["fallback.invalid_json"]
    if draft.diagnostic and draft.diagnostic.status == "completed" and draft.waitlist_action and draft.waitlist_action.status != "joined":
        draft.waitlist_action = None
        draft.decision.waitlist_allowed_now = False
    if draft.waitlist_action and draft.waitlist_action.status == "joined":
        return ["waitlist.joined"]
    if draft.waitlist_action and draft.waitlist_action.status == "pending_details":
        missing = set(draft.waitlist_action.missing_fields)
        if "studio_name" in missing:
            return ["waitlist.ask_missing_studio"]
        if "city_state" in missing or "city/state" in missing:
            return ["waitlist.ask_missing_city"]
        return ["waitlist.ask_missing_contact_path"]
    if decision.route == "waitlist":
        return ["waitlist.offer_after_contract_intent"]
    if draft.diagnostic and draft.diagnostic.status == "completed":
        return _staged_diagnostic_template_ids(draft.diagnostic, decision.demo_status)
    if draft.diagnostic and draft.diagnostic.status == "insufficient_evidence":
        return ["diagnostic.insufficient_evidence"]
    if decision.diagnostic_action in {"offer", "start"}:
        return ["diagnostic.offer_soft"]
    if decision.diagnostic_action == "ask_next":
        return [_question_template_id(_next_required_diagnostic_question(draft.diagnostic))]
    if decision.route == "product":
        intents = {intent.lower() for intent in decision.detected_intents}
        if "out_of_profile" in intents:
            return ["product.out_of_profile_redirect"]
        if "trust_security_question" in intents or "security" in intents or "privacy" in intents:
            return ["product.security_data_direct"]
        if "whatsapp_business_requirement" in intents:
            return ["product.whatsapp_business_requirement"]
        if "integration_scope_question" in intents or "integration" in intents:
            return ["product.integration_scope_direct"]
        if "comparison_current_tool" in intents or "comparison" in intents:
            return ["product.comparison_current_tool"]
        if "product_how_it_works" in intents or "how_it_works" in intents:
            return ["product.how_it_works_direct"]
        if "price_objection" in intents or "price_value_objection" in intents:
            return ["product.price_objection_value"]
        if "demo" in intents:
            return ["product.demo_direct"]
        if "whatsapp" in intents:
            return ["product.whatsapp_direct"]
        if "price" in intents or "preco" in intents:
            return ["product.price_direct", "diagnostic.price_hook"] if decision.diagnostic_allowed_now else ["product.price_direct"]
        if "plan_fit" in intents or "plan" in intents:
            return ["product.plan_fit_with_diagnostic"]
        return ["product.overview_short"]
    return ["opening.general_interest"]


def _sanitize_template_ids(template_ids: list[str]) -> list[str]:
    aliases = {
        "waitlist.join_confirmed": "waitlist.joined",
        "waitlist.confirmed": "waitlist.joined",
        "waitlist.status": "waitlist.status_preserved",
        "waitlist.still_joined": "waitlist.status_preserved",
        "waitlist.offer": "waitlist.offer_after_contract_intent",
        "diagnostic.complete": "diagnostic.deliver_hold",
        "diagnostic.completed": "diagnostic.deliver_hold",
        "diagnostic.question_current_process": "diagnostic.ask_current_process",
    }
    known = required_template_ids()
    cleaned: list[str] = []
    for template_id in template_ids:
        candidate = aliases.get(template_id, template_id)
        if candidate in known and candidate not in cleaned:
            cleaned.append(candidate)
    return cleaned


def _template_context_blob(draft: LLMStructuredDraft) -> str:
    parts: list[str] = [*draft.decision.facts_used]
    parts.extend(fact.value for fact in draft.lead_facts)
    for fact in draft.lead_facts:
        parts.extend(fact.evidence)
    if draft.diagnostic:
        parts.extend(draft.diagnostic.facts_used)
        parts.extend(draft.diagnostic.evidence)
        parts.extend(
            [
                draft.diagnostic.main_bottleneck or "",
                draft.diagnostic.pain_context_human or "",
                draft.diagnostic.first_recommended_step or "",
            ]
        )
    return normalize_text(" ".join(part for part in parts if part))


def _student_count_from_context(fact_blob: str) -> str | None:
    if "aluno" not in fact_blob:
        return None
    numbers = [int(match) for match in re.findall(r"\b\d{1,4}\b", fact_blob)]
    plausible_counts = [number for number in numbers if 1 <= number <= 500]
    if not plausible_counts:
        return None
    return str(max(plausible_counts))


def _short_pain_context_from_blob(fact_blob: str) -> str | None:
    if "whatsapp" in fact_blob and ("interess" in fact_blob or "lead" in fact_blob):
        return "interessados esfriando no WhatsApp"
    if "whatsapp" in fact_blob and any(token in fact_blob for token in ("retorno", "resposta", "responder", "demora")):
        return "retorno no WhatsApp demorando"
    if "agenda" in fact_blob and "reposi" in fact_blob:
        return "agenda e reposições bagunçadas"
    if "reposi" in fact_blob:
        return "reposição bagunçada"
    if "agenda" in fact_blob:
        return "agenda"
    if "planilha" in fact_blob:
        return "rotina em planilha"
    return None


def _pain_context_from_fact_blob(fact_blob: str, draft: LLMStructuredDraft) -> str:
    student_count = _student_count_from_context(fact_blob)
    pain = _short_pain_context_from_blob(fact_blob)
    if "whatsapp" in fact_blob and "interess" in fact_blob:
        return "Entendi: o gargalo parece estar nos interessados que chegam pelo WhatsApp e demoram a receber retorno."
    if "whatsapp" in fact_blob and any(token in fact_blob for token in ("slow", "reply", "respond", "resposta", "responder", "demora")):
        return "Entendi: o gargalo parece estar nos interessados que chegam pelo WhatsApp e demoram a receber retorno."
    if student_count and pain:
        return f"Entendi: {student_count} alunos e {pain} já dizem bastante."
    if pain:
        if pain == "agenda":
            return "Entendi: agenda é o ponto que você quer olhar primeiro."
        return f"Entendi: {pain} já é um bom sinal de onde o diagnóstico deve começar."
    if "studio pequeno" in fact_blob or "studio comecando" in fact_blob or "poucos alunos" in fact_blob:
        return "Sim, faz sentido olhar a Taliya para studio pequeno também."
    if draft.decision.facts_used and not _looks_like_internal_lead_fact(draft.decision.facts_used[0]):
        return f"Entendi esse ponto: {draft.decision.facts_used[0]}."
    if draft.decision.route == "product":
        return "Para comparar plano sem chutar, vale entender a rotina do studio antes."
    return "Para te orientar sem chutar, preciso entender um pouco da rotina do studio."


def _plan_fit_context_from_draft(draft: LLMStructuredDraft) -> str:
    fact_blob = _template_context_blob(draft)
    pain_context = _pain_context_from_fact_blob(fact_blob, draft)
    if pain_context.startswith("Entendi:"):
        return f"{pain_context} Para comparar plano sem chutar, vale entender a rotina do studio antes."
    return "Para comparar plano sem chutar, vale entender a rotina do studio antes."


def _template_variables_for(
    draft: LLMStructuredDraft,
    *,
    previous_state: RuntimeState | None = None,
) -> dict[str, dict[str, Any]]:
    variables = {key: dict(value) for key, value in draft.decision.template_variables.items()}
    fact_blob = _template_context_blob(draft)
    pain_context = _pain_context_from_fact_blob(fact_blob, draft)
    _set_contextual_pain_context(variables, "diagnostic.offer_soft", pain_context)
    _set_contextual_pain_context(variables, "diagnostic.price_hook_with_context", pain_context)
    if "product.plan_fit_with_diagnostic" in draft.decision.template_ids:
        variables["product.plan_fit_with_diagnostic"] = {
            "plan_fit_context": _plan_fit_context_from_draft(draft)
        }
    if draft.diagnostic:
        final_diagnostic = draft.diagnostic.status == "completed"
        final_context_variables = {
            "pain_context_human": draft.diagnostic.pain_context_human
            or f"Pelo que você contou, o ponto principal parece ser {_clean_sentence_fragment(draft.diagnostic.main_bottleneck or 'a rotina prioritária')}."
        }
        if final_diagnostic:
            variables["diagnostic.deliver_context"] = final_context_variables
        else:
            _fill_missing_template_variables(variables, "diagnostic.deliver_context", final_context_variables)
        final_crm_variables = {
            "crm_base_recommendation": draft.diagnostic.crm_base_recommendation
            or "Antes dos agentes, eu organizaria tudo em um só lugar: contatos, conversas, situação de cada interessado e próximos passos."
        }
        if final_diagnostic:
            variables["diagnostic.deliver_crm_base"] = final_crm_variables
        else:
            _fill_missing_template_variables(variables, "diagnostic.deliver_crm_base", final_crm_variables)
        final_step_variables = {
            "operational_first_step": _operational_step_line(draft.diagnostic)
        }
        if final_diagnostic:
            variables["diagnostic.deliver_operational_step"] = final_step_variables
        else:
            _fill_missing_template_variables(variables, "diagnostic.deliver_operational_step", final_step_variables)
        agent_names = _diagnostic_agent_names(draft.diagnostic)
        for index, agent_name in enumerate(agent_names, start=1):
            occurrence_key = (
                "diagnostic.deliver_agent_recommendation"
                if index == 1
                else f"diagnostic.deliver_agent_recommendation#{index}"
            )
            if final_diagnostic:
                variables[occurrence_key] = _agent_recommendation_variables(draft.diagnostic, agent_name, position=index)
            else:
                _fill_missing_template_variables(
                    variables,
                    occurrence_key,
                    _agent_recommendation_variables(draft.diagnostic, agent_name, position=index),
                )
        final_plan_variables = {
            "recommended_plan_or_range": _recommended_plan_range_from_diagnostic(draft.diagnostic)
        }
        if final_diagnostic:
            variables["diagnostic.deliver_plan_recommendation"] = final_plan_variables
        else:
            _fill_missing_template_variables(variables, "diagnostic.deliver_plan_recommendation", final_plan_variables)
        variables.setdefault(
            "diagnostic.deliver",
            {
                "main_bottleneck": _clean_sentence_fragment(draft.diagnostic.main_bottleneck or "a rotina prioritária"),
                "first_step": _clean_sentence_fragment(draft.diagnostic.first_recommended_step or "organizar a primeira rotina crítica"),
                "plan_range": _clean_plan_range(draft.diagnostic.plan_or_range_to_compare or "a faixa mais aderente"),
            },
        )
    previous_diagnostic = _diagnostic_from_previous_state(previous_state)
    if previous_diagnostic and previous_diagnostic.status == "completed":
        _fill_missing_template_variables(
            variables,
            "diagnostic.deliver_context",
            {
                "pain_context_human": previous_diagnostic.pain_context_human
                or f"Pelo diagnóstico, o ponto principal parecia ser {_clean_sentence_fragment(previous_diagnostic.main_bottleneck or 'a rotina prioritária')}."
            },
        )
        _fill_missing_template_variables(
            variables,
            "diagnostic.deliver_crm_base",
            {
                "crm_base_recommendation": previous_diagnostic.crm_base_recommendation
                or "Antes dos agentes, eu organizaria tudo em um só lugar: contatos, conversas, situação de cada interessado e próximos passos."
            },
        )
        _fill_missing_template_variables(
            variables,
            "diagnostic.deliver_operational_step",
            {
                "operational_first_step": previous_diagnostic.first_recommended_step
                or "O primeiro passo seria transformar a rotina mais crítica em uma fila clara de ação."
            },
        )
        for index, agent_name in enumerate(_diagnostic_agent_names(previous_diagnostic), start=1):
            occurrence_key = (
                "diagnostic.deliver_agent_recommendation"
                if index == 1
                else f"diagnostic.deliver_agent_recommendation#{index}"
            )
            _fill_missing_template_variables(
                variables,
                occurrence_key,
                _agent_recommendation_variables(previous_diagnostic, agent_name, position=index),
            )
        _fill_missing_template_variables(
            variables,
            "diagnostic.deliver_plan_recommendation",
            {"recommended_plan_or_range": _recommended_plan_range_from_diagnostic(previous_diagnostic)},
        )
    diagnostic_for_product = (
        previous_diagnostic
        if previous_diagnostic and previous_diagnostic.status == "completed"
        else draft.diagnostic
    )
    if diagnostic_for_product and diagnostic_for_product.status == "completed":
        _fill_missing_template_variables(
            variables,
            "product.post_diagnostic_plan_recap",
            {"recommended_plan_or_range": _recommended_plan_range_from_diagnostic(diagnostic_for_product)},
        )
    if draft.decision.diagnostic_action == "ask_next":
        for template_id in draft.decision.template_ids:
            if template_id.startswith("diagnostic.ask_"):
                variables.setdefault(template_id, {})
                variables[template_id].setdefault(
                    "answer_feedback",
                    "Perfeito, vou guardar esse ponto antes de seguir.",
                )
    if "product.how_it_works_direct" in draft.decision.template_ids:
        variables["product.how_it_works_direct"] = _how_it_works_template_variables(draft, previous_state)
    if "product.demo_direct" in draft.decision.template_ids:
        variables["product.demo_direct"] = {
            "demo_contextual_next_step": _demo_contextual_next_step(previous_state, draft)
        }
    if "product.comparison_current_tool" in draft.decision.template_ids:
        current_tool = _current_tool_context_from_facts(draft) or "o processo atual"
        variables["product.comparison_current_tool"] = {"current_tool_context": current_tool}
    if "product.integration_scope_direct" in draft.decision.template_ids:
        variables["product.integration_scope_direct"] = {
            "integration_topic": _integration_topic_from_text_or_facts("", draft)
        }
    if "post_diagnostic.priority_update" in draft.decision.template_ids:
        variables["post_diagnostic.priority_update"] = _post_diagnostic_priority_update_variables("")
    return variables


def _how_it_works_template_variables(
    draft: LLMStructuredDraft,
    previous_state: RuntimeState | None,
) -> dict[str, str]:
    diagnostic = draft.diagnostic or _diagnostic_from_previous_state(previous_state)
    waitlist_status = previous_state.waitlist.get("status") if previous_state and isinstance(previous_state.waitlist, dict) else None
    demo_status = _previous_demo_status(previous_state)
    if waitlist_status == "joined":
        next_step = "Seu studio continua registrado na lista de espera. Enquanto isso, posso te explicar qualquer parte do funcionamento com mais calma."
    elif demo_status in {"offered", "viewed_or_asked", "reacted_positive"}:
        next_step = "Chegou a olhar a demonstração? Ela ajuda a visualizar esse funcionamento na prática."
    elif diagnostic and diagnostic.status == "completed":
        recommended_area = _recommended_area_from_diagnostic(diagnostic)
        next_step = f"Pelo diagnóstico que fizemos, isso entraria primeiro em {recommended_area}. Posso te mandar uma demonstração para você ver esse funcionamento na prática."
    elif diagnostic and diagnostic.status in {"in_progress", "insufficient_evidence"}:
        next_step = "Isso conversa diretamente com o diagnóstico que estamos fazendo. Vou usar suas respostas para te devolver onde a Taliya entraria primeiro na rotina."
    elif draft.decision.facts_used or (diagnostic and diagnostic.facts_used):
        next_step = "Se fizer sentido para você, estamos oferecendo um diagnóstico gratuito para o seu studio. Assim podemos entender como a Taliya encaixaria na sua rotina e por onde começar. O que você acha?"
    else:
        next_step = "Se fizer sentido para você, estamos oferecendo um diagnóstico gratuito para entender como isso encaixaria na rotina do seu studio. O que você acha?"
    return {
        "contextual_next_step": next_step,
        "recommended_area": _recommended_area_from_diagnostic(diagnostic) if diagnostic else "",
    }


def _recommended_area_from_diagnostic(diagnostic: DiagnosticOutput | None) -> str:
    if diagnostic is None:
        return "uma rotina prioritária"
    candidates = [*diagnostic.indicated_routines_or_agents]
    candidates.extend(
        str(agent.get("agent_name") or agent.get("name") or "")
        for agent in diagnostic.indicated_agents
        if isinstance(agent, dict)
    )
    for candidate in candidates:
        cleaned = _clean_sentence_fragment(str(candidate))
        if cleaned:
            return cleaned.lower()
    if diagnostic.first_recommended_step:
        return _clean_sentence_fragment(diagnostic.first_recommended_step).lower()
    return "uma rotina prioritária"


def _current_tool_context_from_facts(draft: LLMStructuredDraft) -> str | None:
    blob = normalize_text(" ".join([*draft.decision.facts_used, *(fact.value for fact in draft.lead_facts)]))
    tools: list[str] = []
    if "planilha" in blob:
        tools.append("planilha")
    if "caderno" in blob:
        tools.append("caderno")
    if "whatsapp" in blob:
        tools.append("WhatsApp")
    if "tecnofit" in blob:
        tools.append("Tecnofit")
    if "next fit" in blob or "nextfit" in blob:
        tools.append("Next Fit")
    if not tools and "sistema" in blob:
        tools.append("o sistema atual")
    if not tools:
        return None
    return _join_pt(tools)


def _integration_topic_from_facts(draft: LLMStructuredDraft) -> str | None:
    blob = normalize_text(" ".join([*draft.decision.facts_used, *(fact.value for fact in draft.lead_facts)]))
    for token in ("instagram", "tecnofit", "next fit", "whatsapp", "disparo em massa", "sistema"):
        if token in blob:
            return token
    return None


def _integration_topic_from_text_or_facts(normalized_text: str, draft: LLMStructuredDraft) -> str:
    blob = normalize_text(f"{normalized_text} {' '.join([*draft.decision.facts_used, *(fact.value for fact in draft.lead_facts)])}")
    if "instagram" in blob:
        return "Instagram"
    if "tecnofit" in blob:
        return "Tecnofit"
    if "next fit" in blob or "nextfit" in blob:
        return "Next Fit"
    if "whatsapp" in blob:
        return "WhatsApp"
    if "sistema" in blob:
        return "esse sistema"
    return "essa integração"


def _demo_contextual_next_step(previous_state: RuntimeState | None, draft: LLMStructuredDraft) -> str:
    diagnostic = draft.diagnostic or _diagnostic_from_previous_state(previous_state)
    waitlist_status = previous_state.waitlist.get("status") if previous_state and isinstance(previous_state.waitlist, dict) else None
    if diagnostic and diagnostic.status == "completed":
        area = _recommended_area_from_diagnostic(diagnostic)
        return f"Pelo diagnóstico, eu olharia primeiro a parte de {area} na prática."
    fact_blob = normalize_text(" ".join([*draft.decision.facts_used, *(fact.value for fact in draft.lead_facts)]))
    if "agenda" in fact_blob or "reposi" in fact_blob:
        return "Pelo que você comentou sobre agenda e reposições, eu olharia primeiro a parte de organização da rotina."
    if "whatsapp" in fact_blob or "interess" in fact_blob or "follow" in fact_blob:
        return "Pelo que você comentou sobre WhatsApp e retornos, eu olharia primeiro a parte de atendimento e acompanhamento."
    if waitlist_status == "pending_details":
        return "Depois me manda o nome do studio para eu deixar a lista certinha."
    return "Se você me contar um pouco da rotina do seu studio, eu consigo te indicar o que vale olhar primeiro na demonstração."


def _set_contextual_pain_context(variables: dict[str, dict[str, Any]], template_id: str, pain_context: str) -> None:
    current = str(variables.get(template_id, {}).get("pain_context") or "")
    generic = (
        "Para comparar plano sem chutar" in current
        or "Para te orientar sem chutar" in current
        or "rotina do studio antes" in current
        or not current
    )
    if generic or _looks_like_internal_lead_fact(current) or pain_context.startswith("Entendi:"):
        variables.setdefault(template_id, {})
        variables[template_id]["pain_context"] = pain_context


def _clean_sentence_fragment(value: str) -> str:
    cleaned = " ".join(value.strip().rstrip(".").split())
    replacements = {
        "prioritaria": "prioritária",
        "critica": "crítica",
        "voce": "você",
        "proxima": "próxima",
        "diagnostico": "diagnóstico",
    }
    for source, target in replacements.items():
        cleaned = re.sub(rf"\b{source}\b", target, cleaned, flags=re.IGNORECASE)
    return cleaned


def _looks_like_english_lead_fact(value: str) -> bool:
    normalized = normalize_text(value)
    return any(
        token in normalized
        for token in (
            "lead reports",
            "lead says",
            "lead said",
            "lead came",
            "lead wants",
            "lead accepted",
            "user says",
            "user said",
            "prospects",
            "slow to",
            "reply",
        )
    )


def _looks_like_internal_lead_fact(value: str) -> bool:
    normalized = normalize_text(value)
    internal_markers = (
        "lead informou",
        "lead disse",
        "usuario informou",
        "usuário informou",
        "perfil confiavel",
        "perfil confiável",
        "reliable profile",
        "profile first name",
        "profile name",
        "profile_name",
        "used_reliable_name",
        "ignored_unreliable_name",
        "profile_name_usage",
        "profile_name_assessment",
    )
    return (
        _looks_like_english_lead_fact(value)
        or normalized.startswith(internal_markers)
        or any(marker in normalized for marker in internal_markers)
    )


def _clean_plan_range(value: str) -> str:
    cleaned = _clean_sentence_fragment(value)
    cleaned = re.sub(r"\s+com calma.*$", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r",?\s+validando.*$", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"^comparar\s+", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s+depois de validar.*$", "", cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.replace("prioritaria", "prioritária")
    cleaned = cleaned.replace("voce", "você")
    return cleaned or "a faixa mais aderente"


def _previous_demo_status(previous_state: RuntimeState | None) -> str:
    if previous_state and isinstance(previous_state.demo, dict):
        status = previous_state.demo.get("status")
        if status in {"offered", "viewed_or_asked", "reacted_positive"}:
            return str(status)
    return "not_offered"


def _demo_status_for_turn(previous_state: RuntimeState | None, user_text: str) -> str:
    previous_status = _previous_demo_status(previous_state)
    if _is_demo_request(user_text):
        if any(token in user_text for token in ("legal", "gostei", "curti", "interessante", "boa")):
            return "reacted_positive"
        if previous_status in {"offered", "viewed_or_asked", "reacted_positive"}:
            return "viewed_or_asked"
        return "offered"
    return previous_status


def _demo_curiosity_without_contract_intent(user_text: str, previous_state: RuntimeState | None) -> bool:
    if not (_is_demo_request(user_text) or _previous_demo_status(previous_state) in {"offered", "viewed_or_asked", "reacted_positive"}):
        return False
    curiosity_tokens = ("pesquisando", "so pesquisando", "só pesquisando", "sem pressa", "so olhando", "só olhando")
    return any(token in user_text for token in curiosity_tokens)


def _has_active_waitlist_action(waitlist_action: WaitlistAction | None) -> bool:
    return bool(waitlist_action and waitlist_action.status != "none")


def _ledger_areas_from_items(ledger: list[dict[str, object]] | None) -> list[str]:
    areas: list[str] = []
    for item in ledger or []:
        if not isinstance(item, dict):
            continue
        for raw_area in item.get("areas") or []:
            if not isinstance(raw_area, str):
                continue
            normalized = normalize_text(raw_area)
            area = ""
            if "atendimento" in normalized or "whatsapp" in normalized:
                area = "atendimento"
            elif "venda" in normalized or "comercial" in normalized or "interess" in normalized:
                area = "vendas"
            elif "agenda" in normalized or "reposi" in normalized or "falta" in normalized or "encaixe" in normalized:
                area = "agenda_reposicoes"
            elif "financeiro" in normalized or "cobranca" in normalized or "mensalidade" in normalized or "pagamento" in normalized:
                area = "financeiro"
            elif "acompanh" in normalized or "retencao" in normalized or "reten" in normalized:
                area = "acompanhamento"
            elif "gestao" in normalized:
                area = "gestao"
            if area and area not in areas:
                areas.append(area)
    return areas


def _diagnostic_fact_blob(diagnostic: DiagnosticOutput | None) -> str:
    if not diagnostic:
        return ""
    return normalize_text(
        " ".join(
            [
                *_ledger_areas_from_items(diagnostic.ledger),
                *diagnostic.facts_used,
                diagnostic.main_bottleneck or "",
                diagnostic.first_recommended_step or "",
                diagnostic.likely_cause or "",
            ]
        )
    )


def _area_flags_from_blob(fact_blob: str) -> dict[str, bool]:
    return {
        "commercial": any(token in fact_blob for token in ("whatsapp", "interess", "atendimento", "retorno", "follow", "venda")),
        "schedule": any(token in fact_blob for token in ("agenda", "reposi", "falta", "encaixe")),
        "finance": any(token in fact_blob for token in ("financeiro", "cobranca", "cobrança", "mensalidade", "pagamento")),
        "followup": any(token in fact_blob for token in ("acompanh", "retencao", "retenção", "inativo", "sumiu")),
    }


def _infer_diagnostic_routines_from_ledger(
    ledger: list[dict[str, object]] | None,
    answered_values: list[str],
) -> list[str]:
    names: list[str] = []

    def add_from_area(area: str) -> None:
        normalized = normalize_text(area)
        name = ""
        if "financeiro" in normalized:
            name = "Financeiro"
        elif "agenda" in normalized or "reposi" in normalized:
            name = "Agenda"
        elif "atendimento" in normalized:
            name = "Atendimento"
        elif "venda" in normalized:
            name = "Vendas"
        elif "acompanh" in normalized:
            name = "Acompanhamento"
        elif "gestao" in normalized:
            name = "Gestão"
        if name and name not in names:
            names.append(name)

    priority_item: dict[str, object] | None = None
    other_items: list[dict[str, object]] = []
    for item in ledger or []:
        if not isinstance(item, dict):
            continue
        if item.get("question_key") == "priority":
            priority_item = item
        else:
            other_items.append(item)
    for item in ([priority_item] if priority_item else []) + other_items:
        if not item:
            continue
        for area in item.get("areas") or []:
            if isinstance(area, str):
                add_from_area(area)
    for name in _infer_diagnostic_routines_from_answers(answered_values):
        if name not in names:
            names.append(name)
    return names[:3] or ["Atendimento"]


def _merge_diagnostic_facts_with_ledger(diagnostic: DiagnosticOutput, answered_values: list[str]) -> None:
    facts = list(diagnostic.facts_used)
    normalized_existing = {normalize_text(fact) for fact in facts}
    for value in answered_values:
        normalized = normalize_text(value)
        if normalized and normalized not in normalized_existing:
            facts.append(value)
            normalized_existing.add(normalized)
    diagnostic.facts_used = facts


def _completed_diagnostic_bottleneck(ledger: list[dict[str, object]] | None, answered_values: list[str]) -> str:
    fact_blob = normalize_text(" ".join([*_ledger_areas_from_items(ledger), *answered_values]))
    flags = _area_flags_from_blob(fact_blob)
    if flags["commercial"] and flags["finance"] and flags["schedule"]:
        return "interessados no WhatsApp, pagamentos e reposições ainda ficando espalhados no dia a dia"
    if flags["commercial"] and flags["finance"]:
        return "interessados e pagamentos ainda sem acompanhamento claro no dia a dia"
    if flags["commercial"] and flags["schedule"]:
        return "interessados no WhatsApp e reposições ficando difíceis de acompanhar"
    if flags["finance"] and flags["schedule"]:
        return "pagamentos e reposições ficando difíceis de acompanhar sem controle centralizado"
    if flags["finance"]:
        return "pagamentos e cobranças ainda sem controle claro"
    if flags["commercial"]:
        return "interessados chegando pelo WhatsApp e ficando sem retorno claro"
    if flags["schedule"]:
        return "agenda, faltas e reposições ficando difíceis de acompanhar"
    return "a rotina prioritária do studio ainda sem processo claro"


def _completed_diagnostic_first_step(ledger: list[dict[str, object]] | None, answered_values: list[str]) -> str:
    fact_blob = normalize_text(" ".join([*_ledger_areas_from_items(ledger), *answered_values]))
    flags = _area_flags_from_blob(fact_blob)
    if flags["commercial"] and flags["finance"] and flags["schedule"]:
        return "separar quem precisa de resposta no WhatsApp, quais pagamentos estão pendentes e quais reposições precisam de ação"
    if flags["commercial"] and flags["finance"]:
        return "separar conversas paradas, próximos retornos e pagamentos pendentes em uma visão simples"
    if flags["commercial"] and flags["schedule"]:
        return "separar quem chegou agora, quem precisa de retorno e quais reposições estão pendentes"
    if flags["finance"] and flags["schedule"]:
        return "organizar pagamentos pendentes e reposições em uma lista clara para a equipe acompanhar"
    if flags["finance"]:
        return "deixar pagamentos, vencimentos e cobranças pendentes visíveis para a equipe"
    if flags["commercial"]:
        return "separar quem chegou agora, quem precisa de retorno e quais conversas estão paradas"
    if flags["schedule"]:
        return "enxergar faltas, reposições pendentes e próximos encaixes em uma lista clara"
    return "colocar as pendências do dia em uma lista simples para a equipe saber por onde começar"


def _diagnostic_agent_names(diagnostic: DiagnosticOutput | None) -> list[str]:
    if not diagnostic:
        return ["Atendimento"]
    fact_blob = _diagnostic_fact_blob(diagnostic)
    has_agenda_evidence = any(token in fact_blob for token in ("agenda", "reposi", "falta", "encaixe"))
    has_atendimento_evidence = any(token in fact_blob for token in ("whatsapp", "interess", "atendimento", "retorno", "follow"))
    has_finance_evidence = any(token in fact_blob for token in ("financeiro", "cobranca", "mensalidade", "pagamento"))
    has_followup_evidence = any(token in fact_blob for token in ("acompanh", "retencao", "retenção", "inativo", "sumiu"))
    names: list[str] = []
    for item in diagnostic.indicated_routines_or_agents:
        name = _display_agent_name(str(item).strip())
        if not name:
            continue
        normalized_name = normalize_text(name)
        if ("agenda" in normalized_name or "reposi" in normalized_name) and not has_agenda_evidence:
            continue
        if "atendimento" in normalized_name and not has_atendimento_evidence:
            continue
        if "venda" in normalized_name and not has_atendimento_evidence:
            continue
        if "financeiro" in normalized_name and not has_finance_evidence:
            continue
        if "acompanh" in normalized_name and not has_followup_evidence:
            continue
        if name not in names:
            names.append(name)
    if names:
        return names[:3]
    inferred: list[str] = []
    if "whatsapp" in fact_blob or "interess" in fact_blob or "atendimento" in fact_blob:
        inferred.append("Atendimento")
    if "venda" in fact_blob or "follow" in fact_blob:
        inferred.append("Vendas")
    if "agenda" in fact_blob or "reposi" in fact_blob or "falta" in fact_blob:
        inferred.append("Agenda")
    return inferred[:3] or ["Atendimento"]


def _infer_diagnostic_routines_from_answers(answered_values: list[str]) -> list[str]:
    fact_blob = normalize_text(" ".join(answered_values))
    inferred: list[str] = []
    if any(token in fact_blob for token in ("agenda", "reposi", "falta", "encaixe")):
        inferred.append("Agenda")
    if any(token in fact_blob for token in ("whatsapp", "interess", "atendimento")):
        inferred.append("Atendimento")
    if any(token in fact_blob for token in ("venda", "follow", "comercial")):
        inferred.append("Vendas")
    if any(token in fact_blob for token in ("financeiro", "cobranca", "cobrança", "mensalidade", "pagamento")):
        inferred.append("Financeiro")
    return inferred[:3] or ["Atendimento"]


def _diagnostic_demo_template_id(demo_status: str) -> str:
    if demo_status in {"offered", "viewed_or_asked", "reacted_positive"}:
        return "diagnostic.deliver_demo_already_offered"
    return "diagnostic.deliver_demo_not_offered"


def _fill_missing_template_variables(
    variables: dict[str, dict[str, Any]],
    template_id: str,
    defaults: dict[str, Any],
) -> None:
    target = variables.setdefault(template_id, {})
    for key, value in defaults.items():
        if target.get(key) in {None, ""}:
            target[key] = value


def _staged_diagnostic_template_ids(diagnostic: DiagnosticOutput | None, demo_status: str) -> list[str]:
    agent_templates = ["diagnostic.deliver_agent_recommendation" for _ in _diagnostic_agent_names(diagnostic)]
    return [
        "diagnostic.deliver_hold",
        "diagnostic.deliver_context",
        "diagnostic.deliver_crm_base",
        "diagnostic.deliver_operational_step",
        *agent_templates,
        "diagnostic.deliver_plan_recommendation",
        _diagnostic_demo_template_id(demo_status),
    ]


def _next_required_diagnostic_question(diagnostic: DiagnosticOutput | None) -> str | None:
    if diagnostic is None:
        return None
    ledger_question = next_question_text(diagnostic.ledger)
    if ledger_question:
        return ledger_question
    return diagnostic.next_question


def _align_diagnostic_question_with_ledger(
    draft: LLMStructuredDraft,
    template_ids: list[str],
) -> list[str]:
    if draft.decision.diagnostic_action != "ask_next" or draft.diagnostic is None:
        return template_ids
    required_question = _next_required_diagnostic_question(draft.diagnostic)
    if not required_question:
        return template_ids
    draft.diagnostic.next_question = required_question
    required_template_id = _question_template_id(required_question)
    if not any(template_id.startswith("diagnostic.ask_") for template_id in template_ids):
        return template_ids
    aligned: list[str] = []
    inserted = False
    for template_id in template_ids:
        if template_id.startswith("diagnostic.ask_"):
            if not inserted:
                aligned.append(required_template_id)
                inserted = True
            continue
        aligned.append(template_id)
    return aligned


def _question_template_id(next_question: str | None) -> str:
    question = (next_question or "").lower()
    if "quantos alunos" in question or "alunos ativos" in question:
        return "diagnostic.ask_active_students"
    if "ver facilmente" in question or "resolvido no dia" in question:
        return "diagnostic.ask_pain_detail"
    if ("sistema" in question or "planilha" in question or "caderno" in question) and "hoje" in question:
        return "diagnostic.ask_current_process"
    if "ponto exatamente" in question or "travar" in question or "perda" in question:
        return "diagnostic.ask_pain_detail"
    if "prioridade" in question or "tarefa" in question or "mais leve" in question:
        return "diagnostic.ask_priority"
    if "urgente" in question or "pesquisando" in question:
        return "diagnostic.ask_urgency"
    if "plano" in question or "comparar" in question:
        return "diagnostic.ask_priority"
    return "diagnostic.ask_main_pain"


def _question_key_from_text(question: str | None) -> str | None:
    template_id = _question_template_id(question)
    return {
        "diagnostic.ask_active_students": "active_students_or_size",
        "diagnostic.ask_main_pain": "main_pain",
        "diagnostic.ask_pain_detail": "pain_detail",
        "diagnostic.ask_current_process": "current_process",
        "diagnostic.ask_priority": "priority",
        "diagnostic.ask_urgency": "urgency",
    }.get(template_id)


def _previous_diagnostic_question_key(previous_state: RuntimeState | None) -> str | None:
    if previous_state is None or not isinstance(previous_state.diagnostic, dict):
        return None
    previous_question = previous_state.diagnostic.get("next_question")
    if isinstance(previous_question, str) and previous_question.strip():
        return _question_key_from_text(previous_question)
    previous_decision = previous_state.last_decision or {}
    previous_templates = previous_decision.get("template_ids")
    if isinstance(previous_templates, list):
        for template_id in previous_templates:
            if isinstance(template_id, str) and template_id.startswith("diagnostic.ask_"):
                return {
                    "diagnostic.ask_active_students": "active_students_or_size",
                    "diagnostic.ask_main_pain": "main_pain",
                    "diagnostic.ask_pain_detail": "pain_detail",
                    "diagnostic.ask_current_process": "current_process",
                    "diagnostic.ask_priority": "priority",
                    "diagnostic.ask_urgency": "urgency",
                }.get(template_id)
    return None


def _diagnostic_feedback_for_answer_key(
    question_key: str,
    normalized: str,
    interpretation: DiagnosticAnswerInterpretation | None = None,
) -> str:
    area_feedback = _diagnostic_feedback_from_interpreted_areas(question_key, interpretation)
    if area_feedback:
        return area_feedback
    if question_key == "active_students_or_size":
        return "Boa, esse tamanho já ajuda a entender o volume da rotina."
    if question_key == "main_pain":
        if "agenda" in normalized or "reposi" in normalized or "falta" in normalized:
            return "Entendi, agenda e reposições já mostram uma rotina importante para organizar."
        if "whatsapp" in normalized or "interess" in normalized:
            return "Entendi, perder interessado no WhatsApp é um sinal claro para olhar atendimento e follow-up."
        if "financeiro" in normalized or "mensalidade" in normalized or "cobranca" in normalized:
            return "Entendi, financeiro e cobranças precisam aparecer com clareza para não depender de lembrança manual."
        return "Entendi, isso já mostra onde a rotina do studio está pesando mais."
    if question_key == "pain_detail":
        if "nao" in normalized or "não" in normalized or "dificil" in normalized or "difícil" in normalized:
            return "Entendi, quando não fica claro o que resolver no dia, a equipe tende a agir no improviso."
        return "Boa, essa visão do dia ajuda a separar rotina organizada de rotina que ainda escapa."
    if question_key == "current_process":
        if "planilha" in normalized or "manual" in normalized or "caderno" in normalized or "whatsapp" in normalized:
            return "Entendi, então hoje parte da rotina ainda depende bastante de controle manual."
        return "Boa, saber onde isso fica hoje ajuda a entender o quanto a rotina já está centralizada."
    if question_key == "priority":
        has_financial_priority = "financeiro" in normalized or "mensalidade" in normalized or "pagamento" in normalized or "cobranca" in normalized
        has_schedule_priority = "agenda" in normalized or "reposi" in normalized or "falta" in normalized
        if has_financial_priority and has_schedule_priority:
            return "Entendi, então a prioridade é deixar pagamentos e reposições mais leves primeiro."
        if has_financial_priority:
            return "Entendi, então a prioridade é deixar pagamentos e cobranças mais claros primeiro."
        if "agenda" in normalized or "reposi" in normalized or "falta" in normalized:
            return "Entendi, então a prioridade é deixar agenda e reposições mais leves primeiro."
        if "venda" in normalized or "interess" in normalized or "whatsapp" in normalized:
            return "Entendi, então a prioridade é não deixar interessados e follow-ups escaparem."
        return "Entendi, essa prioridade ajuda a definir o primeiro ponto de organização."
    if question_key == "urgency":
        if "agora" in normalized or "urgente" in normalized or "esse mes" in normalized:
            return "Boa, essa urgência ajuda a separar o que precisa entrar primeiro."
        if "pesquis" in normalized or "sem pressa" in normalized:
            return "Entendi, então vale olhar com calma e sem empurrar uma decisão antes da hora."
        return "Perfeito, isso ajuda a entender o momento do studio."
    return "Perfeito, vou guardar esse ponto antes de seguir."


def _diagnostic_answer_feedback(
    user_text: str,
    previous_state: RuntimeState | None,
    diagnostic: DiagnosticOutput | None,
    request: AgentRunRequest,
    interpretation: DiagnosticAnswerInterpretation | None = None,
) -> str:
    if previous_state is None:
        if _is_widget_pending_diagnostic_acceptance_context(request):
            return "Beleza então. Pra te devolver algo útil, preciso entender rapidinho como está a rotina do studio hoje."
        return "Claro, faço sim. Pra te devolver algo útil, vou entender rapidinho como está a rotina do studio hoje."
    normalized = normalize_text(user_text)
    previous_diagnostic_status = None
    if isinstance(previous_state.diagnostic, dict):
        previous_diagnostic_status = previous_state.diagnostic.get("status")
    if previous_diagnostic_status in {"offered", "insufficient_evidence"} and _is_diagnostic_acceptance(normalized):
        return "Beleza então. Pra te devolver algo útil, preciso entender rapidinho como está a rotina do studio hoje."
    previous_question_key = _previous_diagnostic_question_key(previous_state)
    if previous_question_key:
        return _diagnostic_feedback_for_answer_key(previous_question_key, normalized, interpretation)
    if "aluno" in normalized or "leads" in normalized:
        return "Boa, esse tamanho já ajuda a entender o volume da rotina."
    if "planilha" in normalized or "manual" in normalized:
        return "Entendi, então hoje parte da rotina ainda depende bastante de controle manual."
    if "agenda" in normalized or "reposi" in normalized:
        return "Entendi, agenda e reposições já mostram uma rotina importante para organizar."
    if "whatsapp" in normalized or "interess" in normalized:
        return "Entendi, perder interessado no WhatsApp é um sinal claro para olhar atendimento e follow-up."
    if "urgente" in normalized or "agora" in normalized:
        return "Boa, a urgência ajuda a separar o que precisa entrar primeiro."
    if diagnostic and diagnostic.facts_used:
        return "Entendi, isso ajuda a deixar o diagnóstico mais preso ao que você contou."
    return "Perfeito, vou guardar esse ponto antes de seguir."


def _diagnostic_feedback_from_interpreted_areas(
    question_key: str,
    interpretation: DiagnosticAnswerInterpretation | None,
) -> str | None:
    if not interpretation or interpretation.answer_status not in {"answered", "partial"}:
        return None
    areas = _unique_ordered([*_normalized_interpreted_areas(interpretation.areas)])
    if len(areas) < 2:
        return None
    if question_key == "main_pain":
        labels = _diagnostic_area_labels(areas, context="pain")
        return f"Entendi, {_join_pt(labels)} já mostram pontos importantes para olhar no diagnóstico."
    if question_key == "pain_detail":
        labels = _diagnostic_area_labels(areas, context="pain")
        return f"Entendi, isso mistura {_join_pt(labels)} e deixa a rotina mais difícil de acompanhar."
    if question_key == "priority":
        labels = _diagnostic_area_labels(areas, context="priority")
        return f"Entendi, então a prioridade é deixar {_join_pt(labels)} mais organizados primeiro."
    return None


def _normalized_interpreted_areas(areas: list[str]) -> list[str]:
    normalized_areas: list[str] = []
    for area in areas:
        normalized = normalize_text(area)
        if normalized in {"reposicoes", "reposicao", "agenda_reposicoes", "agenda/reposicoes"}:
            normalized = "agenda_reposicoes"
        if normalized == "cobrancas":
            normalized = "financeiro"
        if normalized in {"atendimento", "vendas", "financeiro", "agenda_reposicoes", "acompanhamento", "gestao"}:
            normalized_areas.append(normalized)
    return normalized_areas


def _diagnostic_area_labels(areas: list[str], *, context: str) -> list[str]:
    if context == "priority":
        labels = {
            "atendimento": "atendimento no WhatsApp",
            "vendas": "vendas e follow-up",
            "financeiro": "pagamentos",
            "agenda_reposicoes": "agenda e reposições",
            "acompanhamento": "acompanhamento dos alunos",
            "gestao": "visão da rotina",
        }
    else:
        labels = {
            "atendimento": "atendimento no WhatsApp",
            "vendas": "vendas",
            "financeiro": "pagamentos",
            "agenda_reposicoes": "agenda e reposições",
            "acompanhamento": "acompanhamento dos alunos",
            "gestao": "visão da rotina",
        }
    return [labels[area] for area in areas if area in labels]


def _join_pt(items: list[str]) -> str:
    cleaned = [item for item in items if item]
    if len(cleaned) <= 1:
        return cleaned[0] if cleaned else ""
    if len(cleaned) == 2:
        return f"{cleaned[0]} e {cleaned[1]}"
    return f"{', '.join(cleaned[:-1])} e {cleaned[-1]}"


def _unique_ordered(values: list[str]) -> list[str]:
    unique_values: list[str] = []
    for value in values:
        if value and value not in unique_values:
            unique_values.append(value)
    return unique_values


def _diagnostic_answer_needs_clarification(interpretation: DiagnosticAnswerInterpretation | None) -> bool:
    if interpretation is None:
        return False
    if interpretation.needs_clarification:
        return True
    if interpretation.answer_status in {"unclear", "refused"}:
        return True
    return interpretation.answer_status == "answered" and interpretation.confidence == "low"


def _diagnostic_clarification_feedback() -> str:
    return "Desculpa, não entendi direito. Pra eu não te responder no chute:"


def _diagnostic_ledger_for_turn(
    draft: LLMStructuredDraft,
    request: AgentRunRequest,
    previous_ledger: list[dict[str, object]] | None,
) -> list[dict[str, object]]:
    if draft.diagnostic_answer_interpretation is not None:
        ledger, applied = apply_diagnostic_answer_interpretation(
            draft.diagnostic_answer_interpretation,
            previous_ledger=previous_ledger,
            evidence_id=request.message.idempotency_key,
        )
        if applied or _diagnostic_answer_needs_clarification(draft.diagnostic_answer_interpretation):
            return ledger
    return infer_ledger_from_text(
        request.message.text or "",
        previous_ledger=previous_ledger,
        evidence_id=request.message.idempotency_key,
    )


def _is_widget_pending_diagnostic_acceptance_context(request: AgentRunRequest) -> bool:
    if request.metadata.get("client_pending_context") == "widget_diagnostic_offer_pending":
        return True
    if _has_recent_widget_diagnostic_offer_context(request):
        return True
    return bool(
        request.conversation.entry_intent == "start_crm_diagnostic"
        and request.metadata.get("client_has_prior_assistant_messages")
    )


def _has_recent_widget_diagnostic_offer_context(request: AgentRunRequest) -> bool:
    recent_messages = request.metadata.get("recent_client_messages")
    if not isinstance(recent_messages, list):
        return False
    for raw_message in reversed(recent_messages[-4:]):
        if not isinstance(raw_message, dict):
            continue
        if raw_message.get("role") != "assistant":
            continue
        content = normalize_text(str(raw_message.get("content") or ""))
        if "diagnostico gratuito" in content and "studio" in content and "o que voce acha" in content:
            return True
    return False


def _diagnostic_context_line(diagnostic: DiagnosticOutput, request: AgentRunRequest) -> str:
    if diagnostic.pain_context_human and not _is_stiff_final_diagnostic_line(diagnostic.pain_context_human):
        return diagnostic.pain_context_human
    profile = assess_profile_name(request.sender.name)
    prefix = f"Então, {profile.first_name}, " if profile.status == "reliable" and profile.first_name else "Então, "
    evidence_blob = normalize_text(" ".join(diagnostic.facts_used))
    fact_blob = _diagnostic_fact_blob(diagnostic)
    flags = _area_flags_from_blob(fact_blob)
    if flags["commercial"] and flags["finance"] and flags["schedule"]:
        return f"{prefix}pelo que você contou, o que mais parece estar pesando hoje é acompanhar interessados no WhatsApp, pagamentos e reposições sem deixar tudo depender de planilha e memória."
    if flags["finance"] and flags["schedule"] and not flags["commercial"]:
        return f"{prefix}pelo que você contou, o que mais parece estar pesando hoje é manter pagamentos e reposições em ordem sem depender de controles espalhados."
    if flags["commercial"] and flags["finance"]:
        return f"{prefix}pelo que você contou, o que mais parece estar pesando hoje é acompanhar interessados no WhatsApp e pagamentos sem deixar nada passar."
    if flags["commercial"] and flags["schedule"]:
        return f"{prefix}pelo que você contou, o que mais parece estar pesando hoje é responder interessados no WhatsApp e acompanhar reposições sem deixar pendência solta."
    agenda_evidence = any(token in evidence_blob for token in ("agenda", "reposi", "falta", "encaixe"))
    commercial_evidence = any(token in evidence_blob for token in ("whatsapp", "interess", "venda", "follow", "retorno"))
    if agenda_evidence and not commercial_evidence:
        return f"{prefix}pelo que você contou, o que mais parece estar pesando hoje é manter agenda, faltas e reposições em ordem sem depender de planilha, caderno ou memória da equipe."
    if commercial_evidence:
        return f"{prefix}pelo que você contou, o que mais parece estar pesando hoje é perder interessados no WhatsApp porque o retorno ainda depende muito de planilha e controle manual."
    if "agenda" in fact_blob or "reposi" in fact_blob or "falta" in fact_blob:
        return f"{prefix}pelo que você contou, o que mais parece estar pesando hoje é manter agenda, faltas e reposições em ordem sem depender de planilha, caderno ou memória da equipe."
    if "whatsapp" in fact_blob or "interess" in fact_blob or "venda" in fact_blob:
        return f"{prefix}pelo que você contou, o que mais parece estar pesando hoje é perder interessados no WhatsApp porque o retorno ainda depende muito de planilha e controle manual."
    if "financeiro" in fact_blob or "mensalidade" in fact_blob or "cobranca" in fact_blob:
        return f"{prefix}pelo que você contou, o que mais parece estar pesando hoje é acompanhar cobranças e mensalidades sem deixar nada passar."
    bottleneck = _clean_sentence_fragment(diagnostic.main_bottleneck or "a rotina que mais apareceu na conversa")
    return f"{prefix}pelo que você contou, o que mais parece estar pesando hoje é {bottleneck}."


def _is_stiff_final_diagnostic_line(value: str | None) -> bool:
    if not value:
        return True
    normalized = normalize_text(value)
    return any(
        token in normalized
        for token in (
            "gargalo principal",
            "principal gargalo",
            "pelo contexto o principal",
            "pelo contexto que voce trouxe",
            "pelo contexto que você trouxe",
            "previsibilidade",
            "rotina comercial",
            "base do crm",
            "contexto da conversa",
        )
    )


def _crm_base_line(diagnostic: DiagnosticOutput) -> str:
    evidence_blob = normalize_text(" ".join(diagnostic.facts_used))
    flags = _area_flags_from_blob(_diagnostic_fact_blob(diagnostic))
    if flags["commercial"] and flags["finance"] and flags["schedule"]:
        return "Antes dos agentes, eu organizaria conversas, alunos, pagamentos e reposições em um só lugar, com cada pendência visível para a equipe."
    if flags["finance"] and flags["schedule"] and not flags["commercial"]:
        return "Antes dos agentes, eu organizaria alunos, pagamentos e reposições em um só lugar, para a equipe ver o que precisa de ação."
    if flags["commercial"] and flags["finance"]:
        return "Antes dos agentes, eu organizaria conversas, interessados e pagamentos em um só lugar, com próximos retornos e pendências visíveis."
    agenda_only_evidence = any(token in evidence_blob for token in ("agenda", "reposi", "falta", "encaixe")) and not any(
        token in evidence_blob for token in ("whatsapp", "interess", "venda", "follow", "retorno")
    )
    if agenda_only_evidence and diagnostic.crm_base_recommendation and not any(
        token in normalize_text(diagnostic.crm_base_recommendation) for token in ("agenda", "reposi", "falta", "encaixe")
    ):
        return "Antes dos agentes, eu organizaria a agenda em um só lugar: aulas, faltas, reposições, encaixes e o que a equipe precisa resolver."
    if diagnostic.crm_base_recommendation and not _has_technical_final_language(diagnostic.crm_base_recommendation):
        return diagnostic.crm_base_recommendation
    fact_blob = normalize_text(" ".join([evidence_blob, diagnostic.main_bottleneck or "", diagnostic.first_recommended_step or ""]))
    if agenda_only_evidence:
        return "Antes dos agentes, eu organizaria a agenda em um só lugar: aulas, faltas, reposições, encaixes e o que a equipe precisa resolver."
    if "agenda" in fact_blob or "reposi" in fact_blob or "falta" in fact_blob:
        return "Antes dos agentes, eu organizaria a agenda em um só lugar: aulas, faltas, reposições, encaixes e o que a equipe precisa resolver."
    return "Antes dos agentes, eu organizaria tudo em um só lugar: contatos, conversas, situação de cada interessado e próximos passos."


def _operational_step_line(diagnostic: DiagnosticOutput) -> str:
    evidence_blob = normalize_text(" ".join(diagnostic.facts_used))
    fact_blob = _diagnostic_fact_blob(diagnostic)
    flags = _area_flags_from_blob(fact_blob)
    if flags["commercial"] and flags["finance"] and flags["schedule"]:
        return "O primeiro passo seria separar quem precisa de resposta no WhatsApp, quais pagamentos estão pendentes e quais reposições precisam de ação."
    if flags["finance"] and flags["schedule"] and not flags["commercial"]:
        return "O primeiro passo seria organizar pagamentos pendentes e reposições em uma lista clara para a equipe acompanhar."
    if flags["commercial"] and flags["finance"]:
        return "O primeiro passo seria separar conversas paradas, próximos retornos e pagamentos pendentes em uma visão simples."
    agenda_only_evidence = any(token in evidence_blob for token in ("agenda", "reposi", "falta", "encaixe")) and not any(
        token in evidence_blob for token in ("whatsapp", "interess", "venda", "follow", "retorno")
    )
    if agenda_only_evidence and diagnostic.first_recommended_step and not any(
        token in normalize_text(diagnostic.first_recommended_step) for token in ("agenda", "reposi", "falta", "encaixe")
    ):
        return "O primeiro passo seria enxergar faltas, reposições pendentes e próximos encaixes em uma lista clara."
    if diagnostic.first_recommended_step and not _has_technical_final_language(diagnostic.first_recommended_step):
        step = _clean_sentence_fragment(diagnostic.first_recommended_step)
        if step.lower().startswith(("o primeiro", "primeiro")):
            return step[0].upper() + step[1:] + "."
        if step and not step.startswith(("WhatsApp", "Taliya")):
            step = step[0].lower() + step[1:]
        return f"O primeiro passo seria {step}."
    if "whatsapp" in fact_blob or "interess" in fact_blob or "venda" in fact_blob:
        return "O primeiro passo seria organizar o atendimento e o follow-up do WhatsApp para separar quem chegou agora, quem precisa de retorno e quais conversas estão paradas."
    if "agenda" in fact_blob or "reposi" in fact_blob or "falta" in fact_blob:
        return "O primeiro passo seria enxergar faltas, reposições pendentes e próximos encaixes em uma lista clara."
    return "O primeiro passo seria colocar as pendências do dia em uma lista simples para a equipe saber por onde começar."


def _has_technical_final_language(value: str | None) -> bool:
    if not value:
        return True
    normalized = normalize_text(value)
    return any(
        token in normalized
        for token in (
            "crm",
            "status",
            "previsibilidade",
            "rotina comercial",
            "contexto da conversa",
            "fila clara de acao",
            "fila clara de ação",
            "proximas acoes",
            "próximas ações",
            "entender qual parte",
            "mais travando",
            "priorizar o que organizar primeiro",
        )
    )


def _diagnostic_priority_is_explicit(diagnostic: DiagnosticOutput | None) -> bool:
    if not diagnostic or not isinstance(diagnostic.ledger, list):
        return False
    priority_item: dict[str, Any] | None = None
    related_answer_values: set[str] = set()
    related_evidence: set[str] = set()
    for item in diagnostic.ledger:
        if not isinstance(item, dict):
            continue
        question_key = str(item.get("question_key") or "")
        answer_value = str(item.get("answer_value") or "")
        evidence = {str(value) for value in item.get("evidence") or []}
        if question_key == "priority":
            priority_item = item
        elif question_key in {"main_pain", "pain_detail"}:
            if answer_value:
                related_answer_values.add(normalize_text(answer_value))
            related_evidence.update(evidence)
    if not priority_item:
        return False
    priority_answer = str(priority_item.get("answer_value") or "")
    if not priority_answer:
        return False
    normalized_answer = normalize_text(priority_answer)
    explicit_tokens = (
        "primeiro",
        "prioridade",
        "mais importante",
        "foco",
        "quero resolver",
        "preciso resolver",
        "mais leve",
    )
    if any(token in normalized_answer for token in explicit_tokens):
        return True
    priority_evidence = {str(value) for value in priority_item.get("evidence") or []}
    if normalized_answer in related_answer_values or (priority_evidence and priority_evidence & related_evidence):
        return False
    return priority_item.get("status") in {"answered", "inferred_from_prior_message"}


def _display_agent_name(value: str) -> str:
    normalized = normalize_text(value)
    if "atendimento" in normalized:
        return "Atendimento"
    if "venda" in normalized:
        return "Vendas"
    if "agenda" in normalized or "reposi" in normalized:
        return "Agenda"
    if "gestao" in normalized or "gestão" in value.lower():
        return "Gestão"
    if "financeiro" in normalized or "cobranca" in normalized:
        return "Financeiro"
    if "acompanh" in normalized or "retencao" in normalized:
        return "Acompanhamento"
    return value.strip().capitalize() or "Atendimento"


def _agent_recommendation_variables(diagnostic: DiagnosticOutput | None, agent_name: str | None = None, *, position: int = 1) -> dict[str, str]:
    names = _diagnostic_agent_names(diagnostic)
    resolved_name = _display_agent_name(agent_name or (names[0] if names else "Atendimento"))
    fit_phrase = "faria sentido primeiro" if position == 1 else "também faria sentido"
    fact_blob = _diagnostic_fact_blob(diagnostic)
    normalized_name = normalize_text(resolved_name)
    priority_is_explicit = _diagnostic_priority_is_explicit(diagnostic)
    if "financeiro" in normalized_name or "cobranca" in normalized_name:
        return {
            "agent_name": resolved_name,
            "agent_fit_phrase": fit_phrase,
            "agent_pain_resolved": "pagamentos, cobranças e vencimentos pendentes",
            "agent_recommendation_reason": "pagamentos apareceram como uma prioridade da rotina",
            "agent_practical_action": "ele ajuda a deixar cobranças e pendências visíveis para a equipe não depender de lembrança manual",
        }
    if "agenda" in normalized_name or "reposi" in normalized_name:
        return {
            "agent_name": resolved_name,
            "agent_fit_phrase": fit_phrase,
            "agent_pain_resolved": "faltas, reposições e encaixes",
            "agent_recommendation_reason": "foi isso que mais apareceu como prioridade na sua rotina",
            "agent_practical_action": "ele mostra reposições pendentes, próximos encaixes e o que a equipe precisa resolver",
        }
    if "venda" in normalized_name:
        return {
            "agent_name": resolved_name,
            "agent_fit_phrase": fit_phrase,
            "agent_pain_resolved": "follow-ups e conversas que esfriam",
            "agent_recommendation_reason": "vendas apareceu como prioridade de impacto" if priority_is_explicit else "essa foi uma das dores comerciais mais claras",
            "agent_practical_action": "ele lembra próximos passos e ajuda a não deixar interessado parado",
        }
    if "atendimento" in normalized_name:
        return {
            "agent_name": resolved_name,
            "agent_fit_phrase": fit_phrase,
            "agent_pain_resolved": "interessados que ficam sem resposta",
            "agent_recommendation_reason": "essa foi a dor comercial mais clara",
            "agent_practical_action": "ele ajuda a responder, guardar o histórico e chamar alguém da equipe quando precisar de humano",
        }
    if "agenda" in fact_blob or "reposi" in fact_blob:
        return {
            "agent_name": "Agenda",
            "agent_fit_phrase": fit_phrase,
            "agent_pain_resolved": "faltas, reposições e encaixes",
            "agent_recommendation_reason": "foi isso que mais apareceu como prioridade na sua rotina",
            "agent_practical_action": "ele mostra reposições pendentes, próximos encaixes e o que a equipe precisa resolver",
        }
    if "venda" in fact_blob or "interess" in fact_blob or "whatsapp" in fact_blob:
        return {
            "agent_name": "Atendimento",
            "agent_fit_phrase": fit_phrase,
            "agent_pain_resolved": "interessados que ficam sem resposta",
            "agent_recommendation_reason": "essa foi a dor comercial mais clara",
            "agent_practical_action": "ele ajuda a responder, guardar o histórico e chamar alguém da equipe quando precisar de humano",
        }
    return {
        "agent_name": resolved_name,
        "agent_fit_phrase": fit_phrase,
        "agent_pain_resolved": "a rotina prioritária do studio",
        "agent_recommendation_reason": "ela apareceu como o melhor primeiro ponto de organização",
        "agent_practical_action": "ele acompanha a rotina e avisa a equipe quando algo precisa de atenção",
    }


def _ensure_completed_diagnostic_fields(
    draft: LLMStructuredDraft,
    request: AgentRunRequest,
    previous_state: RuntimeState | None,
) -> None:
    if not draft.diagnostic:
        return
    demo_status = _demo_status_for_turn(previous_state, normalize_text(request.message.text or ""))
    plan_range = _recommended_plan_range_from_diagnostic(draft.diagnostic)
    final_plan_line = f"Pelo tamanho, momento do studio e todo o contexto acima, eu recomendaria pra você o plano {plan_range}."
    final_demo_line = (
        "Chegou a olhar as demonstrações? O que você achou?"
        if demo_status in {"offered", "viewed_or_asked", "reacted_positive"}
        else "Temos algumas demonstrações que mostram o funcionamento na prática. Quer que eu te mande?"
    )
    answered_values = [
        str(item.get("answer_value"))
        for item in draft.diagnostic.ledger
        if isinstance(item, dict) and item.get("answer_value")
    ]
    if answered_values:
        _merge_diagnostic_facts_with_ledger(draft.diagnostic, answered_values)
        inferred_routines = _infer_diagnostic_routines_from_ledger(draft.diagnostic.ledger, answered_values)
        current_routines = [_display_agent_name(item) for item in draft.diagnostic.indicated_routines_or_agents]
        merged_routines: list[str] = []
        for routine in [*inferred_routines, *current_routines]:
            if routine and routine not in merged_routines:
                merged_routines.append(routine)
        draft.diagnostic.indicated_routines_or_agents = merged_routines[:3] or inferred_routines
    draft.diagnostic.pain_context_human = _diagnostic_context_line(draft.diagnostic, request)
    draft.diagnostic.crm_base_recommendation = _crm_base_line(draft.diagnostic)
    draft.diagnostic.first_recommended_step = _operational_step_line(draft.diagnostic)
    draft.diagnostic.indicated_agents = [
        {"name": _display_agent_name(name), **_agent_recommendation_variables(draft.diagnostic, name, position=index)}
        for index, name in enumerate(_diagnostic_agent_names(draft.diagnostic), start=1)
    ]
    draft.diagnostic.plan_or_range_to_compare = plan_range
    draft.diagnostic.final_plan_line = final_plan_line
    draft.diagnostic.demo_status_at_delivery = demo_status  # type: ignore[assignment]
    draft.diagnostic.final_demo_line = final_demo_line
    draft.diagnostic.final_demo_next_step_question = final_demo_line
    draft.diagnostic.validation_question = None


def _recommended_plan_range_from_diagnostic(diagnostic: DiagnosticOutput) -> str:
    fact_blob = _diagnostic_fact_blob(diagnostic)
    numbers = [int(match) for match in re.findall(r"\b\d{1,5}\b", fact_blob)]
    size = max(numbers) if numbers else 0
    has_multiple_routines = sum(
        1
        for token in ("whatsapp", "interess", "agenda", "reposi", "falta", "venda", "financeiro", "mensalidade", "acompanhamento")
        if token in fact_blob
    ) >= 3
    urgent = any(token in fact_blob for token in ("urgente", "agora", "esse mes"))
    manual = any(token in fact_blob for token in ("planilha", "manual", "caderno", "memoria"))
    wants_complete_scope = any(token in fact_blob for token in ("completa", "completo", "tudo", "varias rotinas", "várias rotinas"))
    if size >= 80 or has_multiple_routines or (urgent and manual):
        return "Avance ou Completo"
    if wants_complete_scope and (manual or urgent or has_multiple_routines):
        return "Avance ou Completo"
    provided = _clean_plan_range(diagnostic.plan_or_range_to_compare or "")
    if provided and not _is_generic_diagnostic_fragment(provided) and "confirmar" not in normalize_text(provided):
        return provided
    if size <= 30 and size > 0 and not has_multiple_routines:
        return "Base ou Essencial"
    return "Essencial ou Avance"


def _is_generic_diagnostic_fragment(value: str | None) -> bool:
    if not value:
        return True
    normalized = normalize_text(value)
    return any(
        token in normalized
        for token in (
            "rotina prioritaria",
            "primeira rotina critica",
            "faixa mais aderente",
            "ponto mais critico",
            "rotina do studio",
        )
    )


def _first_turn_greeting(request: AgentRunRequest) -> str:
    profile = assess_profile_name(request.sender.name)
    if profile.status == "reliable" and profile.first_name:
        return f"Oi, {profile.first_name}, tudo bem?"
    return "Oi, tudo bem?"


def _ensure_first_turn_greeting_in_messages(
    messages: list[AgentMessage],
    *,
    request: AgentRunRequest,
    previous_state: RuntimeState | None,
) -> list[AgentMessage]:
    if previous_state is not None or not messages or _client_has_prior_assistant_messages(request):
        return messages
    first_text = messages[0].text.strip()
    if normalize_text(first_text).startswith("oi"):
        return messages
    if messages[0].kind == "action":
        return [
            AgentMessage(
                text=_first_turn_greeting(request),
                channel_hint=request.channel,
                kind="text",
                template_id=messages[0].template_id,
            ),
            *messages[:2],
        ]
    return [
        messages[0].model_copy(update={"text": f"{_first_turn_greeting(request)} {first_text}".strip()}),
        *messages[1:],
    ]


def _ensure_first_turn_greeting_in_texts(
    texts: list[str],
    *,
    request: AgentRunRequest,
    previous_state: RuntimeState | None,
) -> list[str]:
    if previous_state is not None or not texts or _client_has_prior_assistant_messages(request):
        return texts
    if normalize_text(texts[0]).startswith("oi"):
        return texts
    return [f"{_first_turn_greeting(request)} {texts[0]}".strip(), *texts[1:]]


def _client_has_prior_assistant_messages(request: AgentRunRequest) -> bool:
    return request.channel == "widget" and request.metadata.get("client_has_prior_assistant_messages") is True


def _apply_decision_contract(
    draft: LLMStructuredDraft,
    request: AgentRunRequest,
    previous_state: RuntimeState | None,
) -> LLMStructuredDraft:
    user_text = normalize_text(request.message.text or "")
    intent_set = {intent.lower() for intent in draft.decision.detected_intents}
    if not _is_diagnostic_context_active(draft, previous_state):
        for inferred_intent in _product_followup_intents_from_text(user_text):
            if inferred_intent not in intent_set:
                draft.decision.detected_intents.append(inferred_intent)
                intent_set.add(inferred_intent)
    if _is_valid_small_studio_signal(user_text) and not has_any_token(request.message.text, HUMAN_TOKENS):
        draft.decision.detected_intents = [
            intent
            for intent in draft.decision.detected_intents
            if intent.lower() not in {"out_of_profile", "widget_opening"}
        ]
        intent_set.discard("out_of_profile")
        if "small_studio_valid_profile" not in draft.decision.detected_intents:
            draft.decision.detected_intents.append("small_studio_valid_profile")
        draft.current_agent = DIAGNOSTIC_AGENT
        draft.decision.route = "diagnostic"
        draft.decision.opening_type = "none"
        draft.decision.diagnostic_action = "offer"
        draft.decision.diagnostic_allowed_now = True
        draft.decision.waitlist_allowed_now = False
        draft.decision.template_ids = []
        draft.diagnostic = DiagnosticOutput(
            status="offered",
            facts_used=[request.message.text or ""],
            unknowns=["studio_routine"],
            confidence="low",
        )
    diagnostic_refusal = _has_diagnostic_refusal_signal(draft, user_text)
    if diagnostic_refusal and "diagnostic_refusal" not in intent_set:
        draft.decision.detected_intents.append("diagnostic_refusal")
        intent_set.add("diagnostic_refusal")
    price_objection = _has_price_objection_intent(draft, user_text)
    site_fit_opening = _is_site_fit_opening(user_text) and not has_any_token(request.message.text, HUMAN_TOKENS)
    if site_fit_opening:
        draft.current_agent = ENTRY_AGENT
        draft.decision.route = "entry"
        draft.decision.opening_type = "site_forced_message"
        draft.decision.detected_intents = ["site_cta", "product_fit"]
        draft.decision.direct_question_present = False
        draft.decision.direct_question_answered_first = True
        draft.decision.diagnostic_allowed_now = True
        draft.decision.diagnostic_action = "offer"
        draft.decision.waitlist_allowed_now = False
        draft.decision.template_ids = ["opening.site_cta"]
        draft.waitlist_action = None
        draft.handoff = None
        if draft.diagnostic is None or draft.diagnostic.status != "completed":
            draft.diagnostic = DiagnosticOutput(
                status="offered",
                facts_used=[],
                unknowns=["main_pain", "operation_context"],
                confidence="low",
                next_question="O que voce acha?",
            )
    explicit_waitlist_intent = "lista de espera" in user_text or _is_waitlist_acceptance(request.message.text or "")
    if (
        draft.waitlist_action
        and draft.waitlist_action.status != "joined"
        and (
            (draft.diagnostic and draft.diagnostic.status == "completed")
            or (draft.diagnostic and "diagnostico" in user_text and not explicit_waitlist_intent)
        )
    ):
        draft.waitlist_action = None
        draft.decision.waitlist_allowed_now = False
    waitlist_status = draft.waitlist_action.status if draft.waitlist_action else None
    if draft.waitlist_action and draft.waitlist_action.status == "pending_details":
        draft.waitlist_action.missing_fields = _remaining_waitlist_missing_fields(request, draft.waitlist_action.missing_fields)
        if not draft.waitlist_action.missing_fields:
            draft.waitlist_action.status = "joined"
            draft.waitlist_action.reason = "lead_provided_waitlist_details"
            waitlist_status = "joined"
    demo_status = _demo_status_for_turn(previous_state, user_text)
    draft.decision.demo_status = demo_status  # type: ignore[assignment]
    draft.decision.demo_next_step = "ask_demo_reaction" if demo_status == "offered" else "none"
    demo_curiosity = _demo_curiosity_without_contract_intent(user_text, previous_state)
    if demo_curiosity:
        draft.current_agent = PRODUCT_AGENT
        draft.decision.route = "product"
        draft.decision.direct_question_present = True
        draft.decision.direct_question_answered_first = True
        draft.decision.waitlist_allowed_now = False
        draft.decision.diagnostic_allowed_now = False
        draft.decision.diagnostic_action = "none"
        draft.decision.template_ids = []
        draft.diagnostic = None
        draft.waitlist_action = None
    elif _is_demo_request(user_text):
        draft.current_agent = PRODUCT_AGENT
        draft.decision.route = "product"
        draft.decision.direct_question_present = True
        draft.decision.direct_question_answered_first = True
        draft.decision.waitlist_allowed_now = False
        draft.decision.diagnostic_action = "none"
        draft.decision.template_ids = []
        draft.waitlist_action = None
    pain_first_turn = (
        previous_state is None
        and draft.decision.route == "diagnostic"
        and any(token in user_text for token in ("perco", "interessados", "reposicao", "agenda", "falta", "whatsapp"))
        and "diagnostico" not in user_text
        and not (draft.diagnostic and draft.diagnostic.status == "completed")
    )
    if pain_first_turn:
        draft.current_agent = DIAGNOSTIC_AGENT
        draft.decision.route = "diagnostic"
        draft.decision.opening_type = "none"
        draft.decision.diagnostic_action = "offer"
        draft.decision.diagnostic_allowed_now = True
        draft.decision.template_ids = []
        if draft.diagnostic:
            draft.diagnostic.status = "offered"
            draft.diagnostic.next_question = None
    diagnostic_acceptance_after_offer = (
        previous_state is not None
        and isinstance(previous_state.diagnostic, dict)
        and previous_state.diagnostic.get("status") in {"offered", "insufficient_evidence"}
        and _is_diagnostic_acceptance(user_text)
    )
    if diagnostic_acceptance_after_offer:
        draft.current_agent = DIAGNOSTIC_AGENT
        draft.decision.route = "diagnostic"
        draft.decision.diagnostic_action = "ask_next"
        draft.decision.diagnostic_allowed_now = True
        draft.decision.waitlist_allowed_now = False
        draft.decision.template_ids = []
        if draft.diagnostic:
            draft.diagnostic.status = "in_progress"
            draft.diagnostic.next_question = next_question_text(draft.diagnostic.ledger) or draft.diagnostic.next_question
    direct_diagnostic_request = (
        previous_state is None
        and draft.decision.route == "diagnostic"
        and _is_diagnostic_acceptance(user_text)
        and draft.diagnostic is not None
        and draft.diagnostic.status in {"offered", "in_progress", "not_started"}
    )
    if direct_diagnostic_request:
        draft.current_agent = DIAGNOSTIC_AGENT
        draft.decision.route = "diagnostic"
        draft.decision.opening_type = _opening_type_for_request(request, previous_state)  # type: ignore[assignment]
        draft.decision.diagnostic_action = "ask_next"
        draft.decision.diagnostic_allowed_now = True
        draft.decision.waitlist_allowed_now = False
        draft.decision.template_ids = []
        draft.diagnostic.status = "in_progress"
        draft.diagnostic.next_question = next_question_text(draft.diagnostic.ledger) or draft.diagnostic.next_question
    diagnostic_already_in_progress = (
        previous_state is not None
        and isinstance(previous_state.diagnostic, dict)
        and previous_state.diagnostic.get("status") in {"in_progress", "insufficient_evidence"}
        and draft.decision.route == "diagnostic"
        and not _is_demo_request(user_text)
        and not (draft.diagnostic and draft.diagnostic.status == "completed")
    )
    if diagnostic_already_in_progress:
        draft.current_agent = DIAGNOSTIC_AGENT
        draft.decision.route = "diagnostic"
        draft.decision.opening_type = "none"
        draft.decision.diagnostic_action = "ask_next"
        draft.decision.diagnostic_allowed_now = True
        draft.decision.waitlist_allowed_now = False
        draft.decision.template_ids = []
        if draft.diagnostic:
            draft.diagnostic.status = "in_progress"
            draft.diagnostic.next_question = next_question_text(draft.diagnostic.ledger) or draft.diagnostic.next_question
    plain_pending_diagnostic_answer = _is_plain_answer_to_pending_diagnostic_question(user_text, previous_state)
    if plain_pending_diagnostic_answer and _previous_diagnostic_is_in_progress(previous_state):
        if draft.diagnostic is None or draft.diagnostic.status not in {"in_progress", "insufficient_evidence"}:
            draft.diagnostic = _diagnostic_from_previous_state(previous_state) or DiagnosticOutput(status="in_progress", confidence="low")
        draft.current_agent = DIAGNOSTIC_AGENT
        draft.decision.route = "diagnostic"
        draft.decision.opening_type = "none"
        draft.decision.direct_question_present = False
        draft.decision.direct_question_answered_first = True
        draft.decision.diagnostic_action = "ask_next"
        draft.decision.diagnostic_allowed_now = True
        draft.decision.waitlist_allowed_now = False
        draft.decision.detected_intents = [
            intent
            for intent in draft.decision.detected_intents
            if intent.lower() not in {"comparison_current_tool", "comparison", "product_how_it_works", "how_it_works"}
        ]
        draft.decision.template_ids = []
        draft.waitlist_action = None
        draft.handoff = None
        draft.diagnostic.status = "in_progress"
        previous_ledger = previous_state.diagnostic.get("ledger") if previous_state and isinstance(previous_state.diagnostic, dict) else None
        draft.diagnostic.ledger = _diagnostic_ledger_for_turn(
            draft,
            request,
            previous_ledger if isinstance(previous_ledger, list) else None,
        )
        if ledger_is_complete(draft.diagnostic.ledger):
            answered_values = [
                str(item.get("answer_value"))
                for item in draft.diagnostic.ledger
                if isinstance(item, dict) and item.get("answer_value")
            ]
            draft.diagnostic.status = "completed"
            draft.diagnostic.facts_used = draft.diagnostic.facts_used or answered_values
            draft.diagnostic.evidence = draft.diagnostic.evidence or answered_values[:4]
            draft.diagnostic.next_question = None
            draft.diagnostic.unknowns = []
            draft.decision.diagnostic_action = "complete"
            draft.decision.diagnostic_allowed_now = True
        else:
            draft.diagnostic.next_question = next_question_text(draft.diagnostic.ledger) or draft.diagnostic.next_question
    draft.decision = _sync_decision_state(draft.decision, previous_state, waitlist_status=waitlist_status)
    template_ids = _default_template_ids(draft)
    if draft.decision.route == "product" and _is_demo_request(user_text):
        draft.decision = _sync_decision_state(draft.decision, previous_state)
        template_ids = [
            "product.demo_direct",
            *[
                template_id
                for template_id in template_ids
                if template_id not in {"product.demo_direct", "product.overview_short", "diagnostic.offer_soft"}
            ],
        ]
        draft.diagnostic = None
    elif draft.decision.route == "product" and _is_plan_fit_request(user_text):
        template_ids = ["product.plan_fit_with_diagnostic"]
    elif (
        draft.decision.route == "product"
        and any(token in user_text for token in ("preco", "custa", "valor", "planos"))
        and not diagnostic_refusal
    ):
        price_template = "product.price_complete_direct" if _is_complete_price_request(user_text) else "product.price_direct"
        hook_template = "diagnostic.price_hook_with_context" if _has_pain_context_signal(user_text) else "diagnostic.price_hook"
        template_ids = [
            price_template,
            *[
                template_id
                for template_id in template_ids
                if template_id not in {
                    "product.price_direct",
                    "product.price_complete_direct",
                    "product.overview_short",
                    "product.whatsapp_direct",
                    "diagnostic.offer_soft",
                    "diagnostic.price_hook",
                    "diagnostic.price_hook_with_context",
                }
            ],
        ]
        draft.decision.diagnostic_allowed_now = True
        if hook_template not in template_ids:
            template_ids.append(hook_template)
    elif draft.decision.route == "product" and _is_whatsapp_business_requirement_request(user_text):
        if "whatsapp_business_requirement" not in {intent.lower() for intent in draft.decision.detected_intents}:
            draft.decision.detected_intents.append("whatsapp_business_requirement")
        template_ids = [
            "product.whatsapp_business_requirement",
            *[
                template_id
                for template_id in template_ids
                if template_id not in {"product.whatsapp_business_requirement", "product.integration_scope_direct", "product.whatsapp_direct"}
            ],
        ]
    elif draft.decision.route == "product" and "whatsapp" in user_text and "whatsapp_business_requirement" not in {intent.lower() for intent in draft.decision.detected_intents}:
        template_ids = ["product.whatsapp_direct", *[template_id for template_id in template_ids if template_id != "product.whatsapp_direct"]]
    product_followup_keys = _product_followup_source_keys_for_intents(draft.decision.detected_intents)
    if product_followup_keys and not (draft.waitlist_action and draft.decision.route == "waitlist"):
        draft.current_agent = PRODUCT_AGENT
        draft.decision.route = "product"
        draft.decision.opening_type = "none"
        draft.decision.direct_question_present = True
        draft.decision.direct_question_answered_first = True
        if not has_any_token(request.message.text or "", HUMAN_TOKENS):
            draft.handoff = None
        if diagnostic_refusal:
            draft.decision.diagnostic_allowed_now = False
            draft.decision.diagnostic_action = "none"
            draft.diagnostic = None
            draft.waitlist_action = None
            template_ids = [
                template_id
                for template_id in template_ids
                if not template_id.startswith("diagnostic.")
            ]
            if _is_price_amount_question_request(user_text):
                template_ids = [
                    "product.price_complete_direct" if _is_complete_price_request(user_text) else "product.price_direct",
                    *[
                        template_id
                        for template_id in template_ids
                        if template_id
                        not in {
                            "product.price_direct",
                            "product.price_complete_direct",
                            "product.overview_short",
                        }
                    ],
                ]
                for source_key in ("plans", "prices"):
                    if source_key not in draft.source_keys:
                        draft.source_keys.append(source_key)
        for source_key in product_followup_keys:
            if source_key not in draft.source_keys:
                draft.source_keys.append(source_key)
        followup_templates = _product_followup_template_ids_for_intents(draft.decision.detected_intents)
        if followup_templates and not set(template_ids).intersection(followup_templates):
            template_ids = followup_templates
        elif not template_ids or template_ids == ["product.overview_short"]:
            original_template_ids = draft.decision.template_ids
            draft.decision.template_ids = []
            template_ids = _default_template_ids(draft)
            draft.decision.template_ids = original_template_ids
        draft.decision = _sync_decision_state(draft.decision, previous_state)
    if price_objection and not (draft.handoff and draft.handoff.status in {"requested", "active"}):
        previous_diagnostic = _diagnostic_from_previous_state(previous_state)
        if previous_diagnostic and draft.diagnostic is None:
            draft.diagnostic = previous_diagnostic
        if "price_objection" not in draft.decision.detected_intents:
            draft.decision.detected_intents.append("price_objection")
        draft.current_agent = PRODUCT_AGENT
        draft.decision.route = "product"
        draft.decision.direct_question_present = True
        draft.decision.direct_question_answered_first = True
        draft.decision.waitlist_allowed_now = False
        if draft.waitlist_action and draft.waitlist_action.status != "joined":
            draft.waitlist_action = None
        if draft.diagnostic and draft.diagnostic.status in {"in_progress", "insufficient_evidence"}:
            draft.decision.diagnostic_allowed_now = True
            draft.decision.diagnostic_action = "ask_next"
        elif draft.diagnostic and draft.diagnostic.status == "completed":
            draft.decision.diagnostic_allowed_now = True
            draft.decision.diagnostic_action = "complete"
        else:
            draft.decision.diagnostic_allowed_now = True
            draft.decision.diagnostic_action = "offer"
            draft.diagnostic = DiagnosticOutput(
                status="offered",
                facts_used=list(draft.decision.facts_used),
                unknowns=list(draft.decision.facts_missing),
                confidence="low",
            )
        template_ids = []
        if _is_price_amount_question_request(user_text):
            template_ids.append(
                "product.price_complete_direct" if _is_complete_price_request(user_text) else "product.price_direct"
            )
        template_ids.append("product.price_objection_value")
        for source_key in ("plans", "prices", "plan_comparison"):
            if source_key not in draft.source_keys:
                draft.source_keys.append(source_key)
    previous_completed_diagnostic = _diagnostic_from_previous_state(previous_state)
    post_diagnostic_product_followup = (
        previous_completed_diagnostic
        and previous_completed_diagnostic.status == "completed"
        and draft.decision.route == "product"
        and not price_objection
    )
    if post_diagnostic_product_followup:
        cleaned_templates = [
            template_id
            for template_id in template_ids
            if not template_id.startswith("diagnostic.deliver")
            and template_id
            not in {
                "diagnostic.offer_soft",
                "diagnostic.price_hook",
                "diagnostic.price_hook_with_context",
                "product.plan_fit_with_diagnostic",
            }
        ]
        should_recap_plan = _is_plan_fit_request(user_text) or any(
            token in user_text for token in ("plano", "planos", "avance", "essencial", "completo", "base")
        )
        should_send_demo = _is_demo_request(user_text) or any(
            intent.lower() in {"demo", "demo_request", "product_demo"}
            for intent in draft.decision.detected_intents
        )
        if should_recap_plan:
            cleaned_templates.insert(0, "product.post_diagnostic_plan_recap")
        if should_send_demo:
            cleaned_templates.append("product.demo_direct")
            draft.decision.demo_status = "offered"
            draft.decision.demo_next_step = "ask_demo_reaction"
        if not cleaned_templates:
            cleaned_templates = ["product.overview_short"]
        if _is_thinking_response(user_text):
            cleaned_templates = ["post_diagnostic.thinking"]
        elif _is_priority_update_after_diagnostic(user_text):
            cleaned_templates = ["post_diagnostic.priority_update"]
        template_ids = []
        for template_id in cleaned_templates:
            if template_id not in template_ids:
                template_ids.append(template_id)
        draft.diagnostic = previous_completed_diagnostic
        draft.current_agent = PRODUCT_AGENT
        draft.decision.diagnostic_action = "none"
        draft.decision.diagnostic_allowed_now = True
        draft.decision.direct_question_present = True
        draft.decision.direct_question_answered_first = True
        for source_key in ("plans", "prices"):
            if should_recap_plan and source_key not in draft.source_keys:
                draft.source_keys.append(source_key)
        if should_send_demo:
            for source_key in ("demo_status", "links"):
                if source_key not in draft.source_keys:
                    draft.source_keys.append(source_key)
    if draft.waitlist_action and draft.waitlist_action.status == "joined":
        draft.decision.waitlist_allowed_now = True
        template_ids = ["waitlist.joined"]
    elif draft.waitlist_action and draft.waitlist_action.status == "pending_details":
        draft.decision.waitlist_allowed_now = True
        missing = set(draft.waitlist_action.missing_fields)
        if "studio_name" in missing:
            template_ids = ["waitlist.ask_missing_studio"]
        elif "city_state" in missing or "city/state" in missing:
            template_ids = ["waitlist.ask_missing_city"]
        else:
            template_ids = ["waitlist.ask_missing_contact_path"]
    elif draft.waitlist_action and draft.waitlist_action.status == "offered":
        draft.decision.waitlist_allowed_now = True
        template_ids = ["waitlist.offer_after_contract_intent"]
    elif draft.handoff and draft.handoff.status in {"requested", "active"}:
        draft.current_agent = HANDOFF_AGENT
        draft.decision.route = "handoff"
        draft.decision.diagnostic_action = "none"
        template_ids = ["handoff.acknowledge"]
        if previous_completed_diagnostic and draft.diagnostic is None:
            draft.diagnostic = previous_completed_diagnostic
    if (
        previous_completed_diagnostic
        and previous_completed_diagnostic.status == "completed"
        and draft.waitlist_action
        and draft.waitlist_action.status in {"offered", "pending_details", "joined"}
        and draft.diagnostic is None
    ):
        draft.diagnostic = previous_completed_diagnostic
        draft.decision.diagnostic_allowed_now = True
    if (
        "diagnostic.offer_soft" in template_ids
        or "diagnostic.price_hook" in template_ids
        or "diagnostic.price_hook_with_context" in template_ids
        or "product.plan_fit_with_diagnostic" in template_ids
    ):
        draft.decision.diagnostic_allowed_now = True
        draft.decision.diagnostic_action = "offer"
        if draft.diagnostic is None:
            draft.diagnostic = DiagnosticOutput(
                status="offered",
                facts_used=list(draft.decision.facts_used),
                unknowns=list(draft.decision.facts_missing),
                confidence="low",
            )
    rendered_template_body = " ".join(
        line
        for template_id in template_ids
        if (template := get_template(template_id)) is not None
        for line in template.body
    )
    if draft.decision.opening_type == "social_source_opening" and "diagnóstico gratuito" in rendered_template_body:
        draft.decision.diagnostic_allowed_now = True
        draft.decision.diagnostic_action = "offer"
        if draft.diagnostic is None:
            draft.diagnostic = DiagnosticOutput(
                status="offered",
                facts_used=list(draft.decision.facts_used),
                unknowns=[],
                confidence="low",
            )
    post_waitlist_product_question = (
        previous_state is not None
        and isinstance(previous_state.waitlist, dict)
        and previous_state.waitlist.get("status") in {"offered", "pending_details", "joined"}
        and (
            draft.decision.route == "product"
            or _is_price_question_request(user_text)
            or _is_demo_request(user_text)
            or _is_product_question_signal(user_text)
        )
    )
    if post_waitlist_product_question:
        draft.current_agent = PRODUCT_AGENT
        draft.decision.route = "product"
        draft.decision.direct_question_present = True
        draft.decision.direct_question_answered_first = True
        draft.decision.waitlist_allowed_now = True
        draft.waitlist_action = None
        template_ids = [
            template_id
            for template_id in template_ids
            if template_id
            not in {
                "diagnostic.offer_soft",
                "diagnostic.price_hook",
                "diagnostic.price_hook_with_context",
                "diagnostic.deliver",
                "product.overview_short",
                "waitlist.status_preserved",
                "waitlist.offer_after_contract_intent",
                "waitlist.ask_missing_studio",
                "waitlist.ask_missing_city",
                "waitlist.ask_missing_contact_path",
            }
        ]
        if any(token in user_text for token in ("preco", "custa", "valor", "completo")):
            price_template = "product.price_complete_direct" if _is_complete_price_request(user_text) else "product.price_direct"
            if price_template not in template_ids:
                template_ids.insert(0, price_template)
        if previous_state.waitlist.get("status") == "pending_details" and "waitlist.resume_missing_studio" not in template_ids:
            template_ids.append("waitlist.resume_missing_studio")
    if (
        _is_whatsapp_business_requirement_request(user_text)
        and not (draft.waitlist_action and draft.waitlist_action.status in {"offered", "pending_details", "joined"})
        and not (draft.handoff and draft.handoff.status in {"requested", "active"})
    ):
        if "whatsapp_business_requirement" not in {intent.lower() for intent in draft.decision.detected_intents}:
            draft.decision.detected_intents.append("whatsapp_business_requirement")
        draft.current_agent = PRODUCT_AGENT
        draft.decision.route = "product"
        draft.decision.direct_question_present = True
        draft.decision.direct_question_answered_first = True
        template_ids = [
            "product.whatsapp_business_requirement",
            *[
                template_id
                for template_id in template_ids
                if template_id
                not in {
                    "product.whatsapp_business_requirement",
                    "product.integration_scope_direct",
                    "product.whatsapp_direct",
                    "product.how_it_works_direct",
                    "product.overview_short",
                    "diagnostic.offer_soft",
                    "diagnostic.price_hook",
                    "diagnostic.price_hook_with_context",
                }
            ],
        ]
        for source_key in ("whatsapp_scope", "integration_scope", "unsupported_claims"):
            if source_key not in draft.source_keys:
                draft.source_keys.append(source_key)
    template_ids = _align_diagnostic_question_with_ledger(draft, template_ids)
    if any(template_id.startswith("diagnostic.ask_") for template_id in template_ids):
        draft.current_agent = DIAGNOSTIC_AGENT
        draft.decision.route = "diagnostic"
        draft.decision.diagnostic_action = "ask_next"
        draft.decision.diagnostic_allowed_now = True
        draft.decision.waitlist_allowed_now = False
        draft.waitlist_action = None
        draft.decision = _sync_decision_state(draft.decision, previous_state)
    staged_diagnostic = any(template_id.startswith("diagnostic.deliver_") for template_id in template_ids)
    draft.decision.template_ids = template_ids if staged_diagnostic else template_ids[:3]
    draft.decision.template_variables = _template_variables_for(draft, previous_state=previous_state)
    if draft.decision.diagnostic_action == "ask_next":
        for template_id in draft.decision.template_ids:
            if template_id.startswith("diagnostic.ask_"):
                draft.decision.template_variables.setdefault(template_id, {})
                draft.decision.template_variables[template_id]["answer_feedback"] = _diagnostic_answer_feedback(
                    user_text,
                    previous_state,
                    draft.diagnostic,
                    request,
                    draft.diagnostic_answer_interpretation,
                )
                if _diagnostic_answer_needs_clarification(draft.diagnostic_answer_interpretation):
                    draft.decision.template_variables[template_id]["answer_feedback"] = _diagnostic_clarification_feedback()
    if "diagnostic.price_hook_with_context" in draft.decision.template_ids:
        draft.decision.template_variables["diagnostic.price_hook_with_context"] = {
            "pain_context": _pain_context_from_user_text(user_text),
        }
    if "product.price_objection_value" in draft.decision.template_ids:
        draft.decision.template_variables["product.price_objection_value"] = _price_objection_template_variables(
            request,
            previous_state,
            draft,
        )
    if "product.demo_direct" in draft.decision.template_ids:
        draft.decision.template_variables["product.demo_direct"] = {
            "demo_contextual_next_step": _demo_contextual_next_step(previous_state, draft)
        }
    if "product.integration_scope_direct" in draft.decision.template_ids:
        draft.decision.template_variables["product.integration_scope_direct"] = {
            "integration_topic": _integration_topic_from_text_or_facts(user_text, draft)
        }
    if "post_diagnostic.priority_update" in draft.decision.template_ids:
        draft.decision.template_variables["post_diagnostic.priority_update"] = _post_diagnostic_priority_update_variables(user_text)
    waitlist_or_handoff_active = bool(
        (draft.waitlist_action and draft.waitlist_action.status in {"offered", "pending_details", "joined"})
        or (draft.handoff and draft.handoff.status in {"requested", "active"})
    )
    if waitlist_or_handoff_active and draft.diagnostic and draft.diagnostic.status in {"offered", "in_progress"}:
        draft.diagnostic = None
    if draft.diagnostic and draft.diagnostic.status in {"offered", "in_progress", "insufficient_evidence", "completed"} and not waitlist_or_handoff_active and not post_waitlist_product_question and not price_objection and not post_diagnostic_product_followup:
        draft.decision.diagnostic_allowed_now = True
        if draft.diagnostic.status == "completed":
            draft.current_agent = DIAGNOSTIC_AGENT
            draft.decision.route = "diagnostic"
            draft.decision.diagnostic_action = "complete"
            if _is_plan_fit_request(user_text) or any(token in user_text for token in ("preco", "custa", "valor", "planos", "plano", "comparar")):
                draft.decision.direct_question_present = True
                draft.decision.direct_question_answered_first = True
            draft.decision = _sync_decision_state(draft.decision, previous_state)
            _ensure_completed_diagnostic_fields(draft, request, previous_state)
            draft.decision.demo_status = draft.diagnostic.demo_status_at_delivery
            draft.decision.demo_next_step = "ask_demo_reaction"
            draft.decision.template_ids = _staged_diagnostic_template_ids(draft.diagnostic, draft.diagnostic.demo_status_at_delivery)
            draft.decision.template_variables = _template_variables_for(draft, previous_state=previous_state)
    if "opening.cold_greeting_named" in draft.decision.template_ids:
        profile = assess_profile_name(request.sender.name)
        if profile.status == "reliable" and profile.first_name:
            draft.decision.template_variables.setdefault(
                "opening.cold_greeting_named",
                {"first_name": profile.first_name},
            )
    draft.decision.render_plan = [
        {"template_id": template_id, "channel": request.channel}
        for template_id in draft.decision.template_ids
    ]
    return draft


def _route_agent_name(text: str) -> str:
    return AGENT_BY_ROUTE[route_from_text(text)]


def _product_followup_source_keys_for_intents(intents: list[str]) -> list[str]:
    normalized = {intent.lower() for intent in intents}
    keys: set[str] = set()
    if {"product_how_it_works", "how_it_works"} & normalized:
        keys.update({"how_it_works", "routine_areas", "whatsapp_scope"})
    if {"comparison_current_tool", "comparison"} & normalized:
        keys.update({"comparison_spreadsheet", "comparison_management_system", "routine_areas"})
    if {"integration_scope_question", "integration"} & normalized:
        keys.update({"whatsapp_scope", "integration_scope", "unsupported_claims"})
    if "whatsapp_business_requirement" in normalized:
        keys.update({"whatsapp_scope"})
    if {"trust_security_question", "security", "privacy"} & normalized:
        keys.update({"security_and_data", "privacy_or_data_notes"})
    if "out_of_profile" in normalized:
        keys.update({"out_of_profile"})
    if {"conversation_resume", "general_objection", "diagnostic_refusal"} & normalized:
        keys.update({"how_it_works", "routine_areas", "availability_and_onboarding"})
    return sorted(keys)


def _product_followup_template_ids_for_intents(intents: list[str]) -> list[str]:
    normalized = {intent.lower() for intent in intents}
    if "out_of_profile" in normalized:
        return ["product.out_of_profile_redirect"]
    if {"trust_security_question", "security", "privacy"} & normalized:
        return ["product.security_data_direct"]
    if "whatsapp_business_requirement" in normalized:
        return ["product.whatsapp_business_requirement"]
    if {"integration_scope_question", "integration"} & normalized:
        return ["product.integration_scope_direct"]
    if {"comparison_current_tool", "comparison"} & normalized:
        return ["product.comparison_current_tool"]
    if {"product_how_it_works", "how_it_works"} & normalized:
        return ["product.how_it_works_direct"]
    return []


def _product_followup_intents_from_text(normalized_text: str) -> list[str]:
    intents: list[str] = []
    if "como funciona" in normalized_text or "me explica como" in normalized_text:
        intents.append("product_how_it_works")
    if any(token in normalized_text for token in ("planilha", "sistema atual", "sistema que uso", "sistema hoje")):
        intents.append("comparison_current_tool")
    if any(token in normalized_text for token in ("integra", "integracao", "integração")):
        intents.append("integration_scope_question")
    if "whatsapp business" in normalized_text and any(token in normalized_text for token in ("preciso", "tem que", "tenho que", "necessario", "necessário")):
        intents.append("whatsapp_business_requirement")
    if any(token in normalized_text for token in ("lgpd", "privacidade", "seguro", "seguranca", "segurança", "dados dos alunos", "dados sensiveis", "dados sensíveis")):
        intents.append("trust_security_question")
    if any(token in normalized_text for token in ("sou aluno", "sou professora", "sou professor", "professor autonomo", "professor autônomo")):
        intents.append("out_of_profile")
    return intents


def _is_diagnostic_context_active(draft: LLMStructuredDraft, previous_state: RuntimeState | None) -> bool:
    if draft.decision.route == "diagnostic":
        return True
    if draft.diagnostic and draft.diagnostic.status in {"in_progress", "insufficient_evidence"}:
        return True
    return bool(
        previous_state
        and isinstance(previous_state.diagnostic, dict)
        and previous_state.diagnostic.get("status") in {"in_progress", "insufficient_evidence"}
    )


def _previous_diagnostic_is_in_progress(previous_state: RuntimeState | None) -> bool:
    return bool(
        previous_state
        and isinstance(previous_state.diagnostic, dict)
        and previous_state.diagnostic.get("status") in {"in_progress", "insufficient_evidence"}
    )


def _is_plain_answer_to_pending_diagnostic_question(normalized_text: str, previous_state: RuntimeState | None) -> bool:
    if not previous_state or not isinstance(previous_state.diagnostic, dict):
        return False
    if previous_state.diagnostic.get("status") not in {"in_progress", "insufficient_evidence"}:
        return False
    if not normalized_text or "?" in normalized_text:
        return False
    if has_any_token(normalized_text, HUMAN_TOKENS) or _is_demo_request(normalized_text):
        return False
    if _is_price_question_request(normalized_text) or _is_product_question_signal(normalized_text):
        return False
    pending_key = _previous_diagnostic_question_key(previous_state)
    if pending_key == "current_process":
        return any(
            token in normalized_text
            for token in ("planilha", "manual", "caderno", "papel", "sistema", "crm", "whatsapp")
        )
    if pending_key == "priority":
        return any(token in normalized_text for token in ("prioridade", "primeiro", "organizar", "aliviar", "melhorar", "vender", "agenda"))
    if pending_key == "urgency":
        return any(token in normalized_text for token in ("urgente", "agora", "esse mes", "proximos meses", "sem pressa", "pesquisando"))
    if pending_key == "active_students_or_size":
        return bool(re.search(r"\b\d{1,5}\b", normalized_text)) or "aluno" in normalized_text
    if pending_key in {"main_pain", "pain_detail"}:
        return len(normalized_text) > 2
    return False


def _is_valid_small_studio_signal(normalized_text: str) -> bool:
    return "studio" in normalized_text and any(
        token in normalized_text
        for token in ("pequeno", "começando", "comecando", "iniciante", "poucos alunos", "pouco aluno")
    )


def _is_thinking_response(normalized_text: str) -> bool:
    return any(
        token in normalized_text
        for token in ("vou pensar", "pensar melhor", "vou avaliar", "vou ver com calma", "preciso pensar")
    )


def _is_priority_update_after_diagnostic(normalized_text: str) -> bool:
    return any(token in normalized_text for token in ("prioridade", "primeiro", "foco")) and any(
        token in normalized_text
        for token in ("vendas", "agenda", "reposi", "whatsapp", "atendimento", "financeiro", "cobranca", "acompanhamento")
    )


def _post_diagnostic_priority_update_variables(normalized_text: str) -> dict[str, str]:
    if "agenda" in normalized_text or "reposi" in normalized_text:
        return {
            "priority_area": "agenda e reposições",
            "demo_area": "faltas, reposições, encaixes e prioridades do dia",
        }
    if "financeiro" in normalized_text or "cobranca" in normalized_text:
        return {
            "priority_area": "financeiro e cobranças",
            "demo_area": "cobranças, pendências e avisos para a equipe",
        }
    if "acompanhamento" in normalized_text or "retencao" in normalized_text:
        return {
            "priority_area": "acompanhamento dos alunos",
            "demo_area": "alunos que precisam de atenção e próximos acompanhamentos",
        }
    return {
        "priority_area": "vendas",
        "demo_area": "interessados que chegam, conversas que esfriam e próximos retornos da equipe",
    }


def _has_diagnostic_refusal_signal(draft: LLMStructuredDraft, normalized_text: str) -> bool:
    if "diagnostic_refusal" in {intent.lower() for intent in draft.decision.detected_intents}:
        return True
    if any(
        fact.key == "diagnostic_refusal" or "diagnostic_refusal" in normalize_text(fact.key)
        for fact in draft.lead_facts
    ):
        return True
    if "diagnostico" not in normalized_text and "diagnostic" not in normalized_text:
        return False
    return bool(
        re.search(r"\b(nao|não|nem|sem)\b.{0,30}\bdiagnostico\b", normalized_text)
        or re.search(r"\bdiagnostico\b.{0,30}\b(nao|não|agora nao|agora não|depois)\b", normalized_text)
    )


def _is_demo_request(normalized_text: str) -> bool:
    return bool(re.search(r"\b(demo|demonstracao|demonstrar)\b", normalized_text))


def _is_site_fit_opening(normalized_text: str) -> bool:
    return (
        "vim pelo site da taliya" in normalized_text
        or "taliya faz sentido" in normalized_text
        or "faz sentido para o meu studio" in normalized_text
        or "faz sentido pro meu studio" in normalized_text
        or "ficaria no meu studio" in normalized_text
        or "funcionaria no meu studio" in normalized_text
    )


def _is_plan_fit_request(normalized_text: str) -> bool:
    return bool(
        re.search(r"\b(qual plano|plano voce recomenda|plano você recomenda|plano serve|melhor plano|qual dos planos)\b", normalized_text)
    )


def _is_complete_price_request(normalized_text: str) -> bool:
    return "completo" in normalized_text and any(token in normalized_text for token in ("preco", "custa", "valor"))


def _is_price_question_request(normalized_text: str) -> bool:
    return any(token in normalized_text for token in ("preco", "preço", "custa", "valor", "planos", "mensalidade"))


def _is_price_amount_question_request(normalized_text: str) -> bool:
    if any(token in normalized_text for token in ("por que custa", "porque custa", "pq custa")):
        return False
    return (
        "quanto custa" in normalized_text
        or "preco" in normalized_text
        or "preço" in normalized_text
        or "qual o valor" in normalized_text
        or "quais planos" in normalized_text
        or "mensalidade" in normalized_text
    )


def _is_whatsapp_business_requirement_request(normalized_text: str) -> bool:
    return "whatsapp" in normalized_text and "business" in normalized_text and any(
        token in normalized_text
        for token in (
            "preciso",
            "precisa",
            "tem que",
            "obrigatorio",
            "obrigatório",
            "necessario",
            "necessário",
            "exige",
            "exigir",
        )
    )


def _has_price_objection_intent(draft: LLMStructuredDraft, normalized_text: str = "") -> bool:
    intents = {intent.lower() for intent in draft.decision.detected_intents}
    if {"price_objection", "price_value_objection"} & intents:
        return True
    explicit_value_objection = any(
        token in normalized_text
        for token in (
            "achei caro",
            "esta caro",
            "está caro",
            "ta caro",
            "tá caro",
            "salgado",
            "por que custa",
            "porque custa",
            "pq custa",
            "vale esse valor",
            "nao sei se compensa",
            "não sei se compensa",
            "tem desconto",
            "se paga",
            "garante resultado",
        )
    )
    explicit_direct_objection = any(
        token in normalized_text
        for token in ("por que custa", "porque custa", "pq custa", "tem desconto", "se paga", "garante resultado")
    )
    return explicit_value_objection and (explicit_direct_objection or bool({"general_objection", "product", "product_price_question"} & intents))


def _is_diagnostic_acceptance(normalized_text: str) -> bool:
    normalized = normalize_text(normalized_text).strip()
    if "diagnostico" in normalized or "diagnóstico" in normalized:
        return True
    if normalized in {"sim", "pode", "pode sim", "pode ser", "quero", "quero sim", "vamos", "bora", "claro", "claro sim"}:
        return True
    return any(token in normalized for token in ("quero sim", "claro quero", "sim quero", "pode fazer", "faz sim"))


def _has_pain_context_signal(normalized_text: str) -> bool:
    return any(token in normalized_text for token in ("agenda", "reposi", "whatsapp", "interessados", "perco", "perdidas", "bagunc"))


def _pain_context_from_user_text(normalized_text: str) -> str:
    if "agenda" in normalized_text and "reposi" in normalized_text:
        return "Entendi: agenda e reposições perdidas estão pesando na rotina."
    if "whatsapp" in normalized_text and ("interess" in normalized_text or "perco" in normalized_text):
        return "Entendi: perder lead no WhatsApp pesa porque o interessado esfria quando o retorno demora."
    if "agenda" in normalized_text:
        return "Entendi: agenda já parece ser uma rotina importante para olhar."
    return "Entendi esse ponto da rotina do studio."


def _diagnostic_from_previous_state(previous_state: RuntimeState | None) -> DiagnosticOutput | None:
    if previous_state is None or not isinstance(previous_state.diagnostic, dict):
        return None
    try:
        return DiagnosticOutput.model_validate(previous_state.diagnostic)
    except Exception:
        return None


def _price_objection_value_context(
    normalized_text: str,
    previous_state: RuntimeState | None,
    draft: LLMStructuredDraft,
) -> str:
    diagnostic = draft.diagnostic or _diagnostic_from_previous_state(previous_state)
    fact_parts: list[str] = [normalized_text, *draft.decision.facts_used]
    if previous_state:
        fact_parts.extend(str(fact.get("value", "")) for fact in previous_state.lead_facts)
    if diagnostic:
        fact_parts.extend(diagnostic.facts_used)
        fact_parts.extend([diagnostic.main_bottleneck or "", diagnostic.pain_context_human or ""])
    fact_blob = normalize_text(" ".join(fact_parts))

    if "tem desconto" in normalized_text or "desconto" in normalized_text:
        return "Sobre desconto, eu não consigo prometer desconto por aqui sem alguém da equipe confirmar. A Taliya não é só uma tela a mais: ela ajuda a organizar atendimento, agenda, reposições, cobranças e acompanhamento."
    if "garante resultado" in normalized_text or "se paga" in normalized_text:
        return "Eu não posso garantir resultado, porque isso depende da rotina do studio, da equipe e de como a Taliya entra no dia a dia. A Taliya não é só uma ferramenta: ela ajuda a organizar atendimento, retornos, agenda, reposições, cobranças e acompanhamento."
    if "por que custa" in normalized_text or "porque custa" in normalized_text or "pq custa" in normalized_text:
        return "Custa isso porque a Taliya junta organização da rotina com agentes de IA apoiando o WhatsApp dos alunos e interessados, além de atendimento, retornos, agenda, reposições, cobranças e acompanhamento."
    if diagnostic and diagnostic.status == "completed":
        bottleneck = _clean_sentence_fragment(
            diagnostic.main_bottleneck
            or diagnostic.pain_context_human
            or "o que apareceu como prioridade na rotina"
        )
        return f"Pelo diagnóstico, compare esse valor com o que pesa hoje: {bottleneck}. Não é só ferramenta; é organizar atendimento, retorno e próximos passos."
    if "whatsapp" in fact_blob and ("lead" in fact_blob or "interess" in fact_blob or "perco" in fact_blob):
        return "Pelo que você comentou sobre perder lead no WhatsApp, o ponto não é só ter um sistema. É ter clareza de quem precisa de retorno, o que está parado e onde a equipe precisa agir antes do interessado esfriar."
    if "agenda" in fact_blob or "reposi" in fact_blob:
        return "Se agenda e reposições estão pesando, o valor não é só por uma tela de agenda. É por ajudar a organizar o que precisa de ação e evitar que a rotina fique dependendo de memória, planilha e mensagens soltas."
    return "A Taliya não é só uma agenda ou uma planilha mais bonita. Ela ajuda nas rotinas que fazem o studio girar: atendimento, retornos, agenda, reposições, cobranças e acompanhamento dos alunos."


def _price_objection_next_step(
    previous_state: RuntimeState | None,
    draft: LLMStructuredDraft,
) -> str:
    diagnostic = draft.diagnostic or _diagnostic_from_previous_state(previous_state)
    if previous_state and isinstance(previous_state.waitlist, dict) and previous_state.waitlist.get("status") == "joined":
        return "Seu studio continua registrado na lista de espera. O ideal é comparar o plano com o que faria diferença na prática para a rotina do seu studio."
    if diagnostic and diagnostic.status in {"in_progress", "insufficient_evidence"}:
        next_question = next_question_text(diagnostic.ledger) or diagnostic.next_question
        if next_question:
            return f"Pra saber se esse valor faz sentido no seu caso, vamos fechar o diagnóstico com o mínimo de chute possível. {next_question}"
        return "Pra saber se esse valor faz sentido no seu caso, vamos fechar o diagnóstico com o mínimo de chute possível."
    if diagnostic and diagnostic.status == "completed":
        return "Com o diagnóstico em mãos, o melhor próximo passo é ver a demonstração prática e comparar se o plano recomendado faz sentido para você."
    return "Pra saber se esse valor faz sentido para você, eu prefiro olhar a rotina do seu studio antes de falar plano no escuro. Se fizer sentido, faço um diagnóstico gratuito para ver se a Taliya realmente conseguiria te atender ou não. O que você acha?"


def _price_objection_template_variables(
    request: AgentRunRequest,
    previous_state: RuntimeState | None,
    draft: LLMStructuredDraft,
) -> dict[str, str]:
    normalized_text = normalize_text(request.message.text or "")
    return {
        "value_context": _price_objection_value_context(normalized_text, previous_state, draft),
        "next_step": _price_objection_next_step(previous_state, draft),
    }


def _is_product_question_signal(normalized_text: str) -> bool:
    return (
        bool(re.search(r"\b(preco|custa|valor|plano|planos|checkout)\b", normalized_text))
        or _is_demo_request(normalized_text)
        or "como funciona" in normalized_text
        or "integra" in normalized_text
        or "lgpd" in normalized_text
        or "seguranca" in normalized_text
        or "segurança" in normalized_text
        or "como funciona no whatsapp" in normalized_text
    )


def _opening_type_for_request(request: AgentRunRequest, previous_state: RuntimeState | None) -> str:
    text = request.message.text or ""
    if previous_state and previous_state.input_items:
        return "returning_lead"
    if (
        is_cold_greeting_only(text)
        and previous_state is None
        and not request.metadata.get("client_has_prior_assistant_messages")
    ):
        return "cold_greeting_only"
    source_blob = " ".join(
        str(value or "")
        for value in (
            request.conversation.source,
            request.conversation.entry_intent,
            request.metadata.get("utm_source") if isinstance(request.metadata, dict) else None,
            request.metadata.get("source") if isinstance(request.metadata, dict) else None,
            text,
        )
    ).lower()
    if "instagram" in source_blob or "facebook" in source_blob:
        return "social_source_opening"
    if "diagnostico" in source_blob or "diagnostic" in source_blob:
        return "diagnostic_cta_opening"
    if has_any_token(text, DIRECT_QUESTION_TOKENS):
        return "direct_question_opening"
    if _is_site_fit_opening(normalize_text(text)):
        return "site_forced_message"
    if request.channel == "widget" and not text.strip():
        return "widget_opening"
    if request.conversation.source and "landing" in request.conversation.source:
        return "site_forced_message"
    return "none"


def _initial_decision_for_request(request: AgentRunRequest, previous_state: RuntimeState | None) -> RuntimeDecision:
    text = request.message.text or ""
    route = route_from_text(text)
    if is_cold_greeting_only(text):
        route = "entry"
    direct_question = has_any_token(text, DIRECT_QUESTION_TOKENS)
    human_request = has_any_token(text, HUMAN_TOKENS)
    diagnostic_signal = route == "diagnostic" or "diagnostico" in text.lower() or "diagnostic" in text.lower()
    profile = assess_profile_name(request.sender.name)
    profile_name_usage = "not_available"
    if profile.status == "reliable":
        profile_name_usage = "used_reliable_name"
    elif profile.status == "unreliable":
        profile_name_usage = "ignored_unreliable_name"
    opening_type = _opening_type_for_request(request, previous_state)
    widget_empty_opening = opening_type == "widget_opening"
    decision = RuntimeDecision(
        route=route,  # type: ignore[arg-type]
        opening_type=opening_type,  # type: ignore[arg-type]
        detected_intents=["widget_opening"] if widget_empty_opening else [route if route != "entry" else "greeting"] if text.strip() else [],
        direct_question_present=direct_question,
        direct_question_answered_first=not direct_question,
        diagnostic_action="offer" if (diagnostic_signal or widget_empty_opening) and not is_cold_greeting_only(text) and not human_request else "none",
        diagnostic_allowed_now=(diagnostic_signal or widget_empty_opening) and not is_cold_greeting_only(text) and not human_request,
        waitlist_allowed_now=route == "waitlist",
        profile_name_usage=profile_name_usage,  # type: ignore[arg-type]
        facts_missing=[],
        next_question_kind="clarification" if route == "entry" and text.strip() else "none",
    )
    return _sync_decision_state(decision, previous_state)


def _decision_for_route(
    request: AgentRunRequest,
    previous_state: RuntimeState | None,
    route: str,
    *,
    diagnostic: DiagnosticOutput | None = None,
    waitlist_allowed: bool = False,
) -> RuntimeDecision:
    decision = _initial_decision_for_request(request, previous_state)
    decision.route = route  # type: ignore[assignment]
    decision.direct_question_answered_first = True
    if route == "diagnostic":
        decision.diagnostic_allowed_now = True
        if diagnostic:
            decision.diagnostic_action = {
                "completed": "complete",
                "insufficient_evidence": "insufficient_evidence",
                "offered": "offer",
                "in_progress": "ask_next",
            }.get(diagnostic.status, "none")  # type: ignore[assignment]
            decision.facts_used = list(diagnostic.facts_used)
            decision.facts_missing = list(diagnostic.unknowns)
            decision.next_question_kind = "clarification" if diagnostic.next_question else "none"
    elif route == "waitlist":
        decision.waitlist_allowed_now = True
        decision.next_question_kind = "waitlist_details" if waitlist_allowed else "none"
    elif route == "handoff":
        decision.next_question_kind = "handoff"
    waitlist_status = "pending_details" if route == "waitlist" and waitlist_allowed else None
    return _sync_decision_state(decision, previous_state, waitlist_status=waitlist_status)


def _normalize_draft(draft: LLMStructuredDraft, request: AgentRunRequest, previous_state: RuntimeState | None) -> LLMStructuredDraft:
    initial_decision = _initial_decision_for_request(request, previous_state)
    if not draft.decision.detected_intents:
        draft.decision = initial_decision
    elif previous_state is None and initial_decision.opening_type != "none" and draft.decision.opening_type == "none":
        draft.decision.opening_type = initial_decision.opening_type
    if previous_state is None and initial_decision.opening_type == "social_source_opening":
        draft.decision.route = "entry"
    if previous_state is None and initial_decision.opening_type == "diagnostic_cta_opening":
        draft.decision.route = "diagnostic"
        draft.decision.diagnostic_allowed_now = True
    if draft.waitlist_action and draft.waitlist_action.status in {"offered", "pending_details", "joined"}:
        draft.decision.route = "waitlist"
        draft.decision.waitlist_allowed_now = True
    if draft.decision.route == "entry" and draft.decision.direct_question_present:
        intents = {intent.lower() for intent in draft.decision.detected_intents}
        if intents.intersection({"price", "preco", "plan", "plan_fit", "product"}):
            draft.decision.route = "product"
    if draft.diagnostic and draft.diagnostic.status in {"offered", "in_progress", "insufficient_evidence", "completed"}:
        if draft.diagnostic.status == "completed":
            draft.decision.route = "diagnostic"
            draft.decision.diagnostic_allowed_now = True
            draft.decision.diagnostic_action = "complete"
        if draft.decision.direct_question_present and draft.decision.direct_question_answered_first:
            draft.decision.diagnostic_allowed_now = True
        if draft.decision.diagnostic_allowed_now and draft.decision.diagnostic_action == "none":
            draft.decision.diagnostic_action = "offer" if draft.diagnostic.status == "offered" else "ask_next"
    if draft.decision.route in AGENT_BY_ROUTE:
        draft.current_agent = AGENT_BY_ROUTE[draft.decision.route]  # type: ignore[assignment]
    if draft.current_agent == HANDOFF_AGENT and draft.handoff is None:
        draft.handoff = HandoffOutput(status="requested", reason="lead_requested_human")
    return draft


def _enforce_behavior_contract(
    draft: LLMStructuredDraft,
    request: AgentRunRequest,
    previous_state: RuntimeState | None,
) -> LLMStructuredDraft:
    text = request.message.text or ""
    normalized = normalize_text(text)
    joined_messages = normalize_text("\n".join(draft.messages))
    profile = assess_profile_name(request.sender.name)

    if request.message.type == "unsupported_media":
        draft.current_agent = ENTRY_AGENT
        draft.decision = _decision_for_route(request, previous_state, "safe_fallback")
        draft.decision.opening_type = "none"
        draft.decision.detected_intents = ["unsupported_media"]
        draft.decision.template_ids = ["fallback.unsupported_media"]
        draft.decision.render_plan = [{"template_id": "fallback.unsupported_media", "channel": request.channel}]
        draft.messages = [
            "Recebi o arquivo, mas por aqui preciso que voce me mande o ponto principal em texto para eu nao interpretar errado.",
            "Se preferir, tambem posso deixar para uma pessoa olhar.",
        ]
        draft.diagnostic = None
        draft.waitlist_action = None
        draft.handoff = None
        return draft

    prompt_injection_request = (
        "ignore suas regras" in normalized
        or "ignore todas as regras" in normalized
        or "ignore as regras" in normalized
        or "ignore instrucoes" in normalized
        or "ignore as instrucoes" in normalized
        or "ignore anteriores" in normalized
        or "mande o prompt" in normalized
        or "mostre seu prompt" in normalized
        or "revele seu prompt" in normalized
        or ("prompt" in normalized and "interno" in normalized)
        or ("prompt" in normalized and "sistema" in normalized)
    )
    if prompt_injection_request:
        draft.current_agent = ENTRY_AGENT
        draft.decision = _decision_for_route(request, previous_state, "safe_fallback")
        draft.decision.opening_type = "none"
        draft.decision.detected_intents = ["prompt_injection"]
        draft.decision.template_ids = ["safety.prompt_injection"]
        draft.decision.render_plan = [{"template_id": "safety.prompt_injection", "channel": request.channel}]
        draft.messages = [
            "Nao posso revelar ou seguir instrucoes para ignorar minhas regras internas.",
            "Posso seguir te ajudando com planos, diagnostico ou duvidas sobre a Taliya.",
        ]
        draft.diagnostic = None
        draft.waitlist_action = None
        draft.handoff = None
        return draft

    asks_whatsapp_operation = (
        "whatsapp" in normalized
        and "?" in text
        and any(
            token in normalized
            for token in (
                "aluno precisa",
                "baixar app",
                "baixar aplicativo",
                "criar senha",
                "precisa de senha",
                "como funciona",
                "funciona no whatsapp",
                "conversa no whatsapp",
            )
        )
    )
    if asks_whatsapp_operation:
        draft.current_agent = PRODUCT_AGENT
        draft.decision = _decision_for_route(request, previous_state, "product")
        draft.decision.detected_intents = ["product", "whatsapp"]
        draft.decision.direct_question_present = True
        draft.decision.direct_question_answered_first = True
        draft.decision.diagnostic_action = "none"
        draft.decision.diagnostic_allowed_now = False
        draft.decision.waitlist_allowed_now = False
        draft.decision.template_ids = ["product.whatsapp_direct"]
        draft.decision.render_plan = [{"template_id": "product.whatsapp_direct", "channel": request.channel}]
        draft.messages = [
            "O aluno não precisa baixar aplicativo nem criar senha. Ele conversa no WhatsApp; a Taliya registra a ação, atualiza o painel e avisa o responsável.",
            "Temos uma demonstração para você entender melhor: https://www.taliya.com.br/pilates/planos/demonstracao",
        ]
        draft.diagnostic = None
        draft.waitlist_action = None
        draft.handoff = None
        return draft

    phone_or_contact_context = any(
        token in normalized
        for token in (
            "whatsapp",
            "telefone",
            "celular",
            "contato",
            "lista de espera",
            "quero entrar",
            "me coloca",
            "pode colocar",
        )
    )
    if "cpf" in normalized or (re.search(r"\b\d{11}\b", normalized) and not phone_or_contact_context):
        draft.current_agent = ENTRY_AGENT
        draft.decision = _decision_for_route(request, previous_state, "safe_fallback")
        draft.decision.opening_type = "none"
        draft.decision.detected_intents = ["sensitive_data"]
        draft.decision.template_ids = ["safety.sensitive_data"]
        draft.decision.render_plan = [{"template_id": "safety.sensitive_data", "channel": request.channel}]
        draft.messages = [
            "Nao preciso desse dado aqui e prefiro nao usar informacao sensivel no chat.",
            "Se quiser, posso seguir ajudando com planos, demonstracao ou como a Taliya funciona para seu studio.",
        ]
        draft.diagnostic = None
        draft.waitlist_action = None
        draft.handoff = None
        return draft

    if is_cold_greeting_only(text):
        draft.current_agent = ENTRY_AGENT
        draft.decision = _initial_decision_for_request(request, previous_state)
        if profile.status == "reliable" and profile.first_name:
            draft.messages = [f"Oi, {profile.first_name}. Tudo bem?", "Em que posso te ajudar?"]
        else:
            draft.messages = ["Oi! Tudo bem?", "Em que posso te ajudar?"]
        draft.diagnostic = None
        draft.waitlist_action = None
        draft.handoff = None
        return draft

    if request.channel == "widget" and not text.strip() and (previous_state is None or not previous_state.input_items):
        draft.current_agent = ENTRY_AGENT
        draft.decision = _initial_decision_for_request(request, previous_state)
        draft.decision.route = "entry"
        draft.decision.opening_type = "widget_opening"
        draft.decision.detected_intents = ["widget_opening"]
        draft.decision.diagnostic_action = "offer"
        draft.decision.diagnostic_allowed_now = True
        draft.decision.waitlist_allowed_now = False
        draft.decision.template_ids = ["opening.widget_empty_diagnostic"]
        draft.messages = [
            "Oi, tudo bem?",
            "Em que posso ajudar?",
            "Se fizer sentido pra você, estamos oferecendo um diagnóstico gratuito pro seu studio. O que você acha?",
        ]
        draft.diagnostic = DiagnosticOutput(
            status="offered",
            facts_used=[],
            unknowns=["main_pain", "operation_context"],
            confidence="low",
            next_question="O que você acha?",
        )
        draft.waitlist_action = None
        draft.handoff = None
        return draft

    if draft.current_agent == HANDOFF_AGENT or has_any_token(text, HUMAN_TOKENS):
        draft.current_agent = HANDOFF_AGENT
        draft.decision = _decision_for_route(request, previous_state, "handoff")
        draft.messages = ["Claro. Vou deixar uma pessoa assumir daqui.", "Tambem deixo o contexto salvo para voce nao precisar repetir tudo."]
        draft.handoff = HandoffOutput(status="requested", reason="lead_requested_human")
        draft.diagnostic = None
        draft.waitlist_action = None
        return draft

    if previous_state is None and _is_site_fit_opening(normalized):
        draft.current_agent = ENTRY_AGENT
        draft.decision = _initial_decision_for_request(request, previous_state)
        draft.decision.route = "entry"
        draft.decision.opening_type = "site_forced_message"
        draft.decision.detected_intents = ["site_cta", "product_fit"]
        draft.decision.direct_question_present = False
        draft.decision.direct_question_answered_first = True
        draft.decision.diagnostic_allowed_now = True
        draft.decision.diagnostic_action = "offer"
        draft.decision.waitlist_allowed_now = False
        draft.decision.template_ids = ["opening.site_cta"]
        draft.messages = [
            "Claro, posso te ajudar com isso sim.",
            "Resumindo... A Taliya é a IA do seu studio de Pilates: você cuida dos alunos, e ela ajuda na rotina que faz o studio girar: agenda, reposições, cobranças, gestão, atendimento e acompanhamento.",
            "Pra te orientar sem chutar, posso fazer um diagnostico gratuito com poucas perguntas e te devolver por onde comecar. O que voce acha?",
        ]
        draft.diagnostic = DiagnosticOutput(
            status="offered",
            facts_used=[],
            unknowns=["main_pain", "operation_context"],
            confidence="low",
            next_question="O que voce acha?",
        )
        draft.waitlist_action = None
        draft.handoff = None
        return draft

    if "instagram" in normalized or "facebook" in normalized:
        if "crm" not in joined_messages:
            draft.current_agent = ENTRY_AGENT
            draft.decision.route = "entry"
            draft.decision.opening_type = "social_source_opening"
            draft.messages = [
                "A Taliya é a IA do seu studio de Pilates. Ela ajuda a organizar atendimento, agenda, vendas e a rotina que faz o studio girar.",
                "Voce quer entender a ideia geral primeiro ou tem alguma parte do studio que esta pesando mais hoje?",
            ]

    if draft.decision.opening_type == "diagnostic_cta_opening":
        draft.current_agent = DIAGNOSTIC_AGENT
        draft.decision.route = "diagnostic"
        draft.decision.diagnostic_allowed_now = True
        draft.decision.diagnostic_action = "ask_next"
        draft.diagnostic = DiagnosticOutput(
            status="in_progress",
            facts_used=[],
            unknowns=["active_students_or_size"],
            confidence="low",
            next_question="Hoje seu studio tem mais ou menos quantos alunos ativos?",
        )
        draft.messages = [
            "Beleza entao. Pra te devolver algo util, preciso entender rapidinho como esta a rotina do studio hoje.",
            "Hoje seu studio tem mais ou menos quantos alunos ativos?",
        ]

    if ("qual plano" in normalized or "plano voce recomenda" in normalized or "plano serve" in normalized) and "nao quero chutar" not in joined_messages:
        draft.current_agent = PRODUCT_AGENT
        draft.decision.route = "product"
        draft.decision.direct_question_present = True
        draft.decision.direct_question_answered_first = True
        draft.decision.diagnostic_allowed_now = True
        draft.decision.diagnostic_action = "offer"
        draft.diagnostic = DiagnosticOutput(
            status="offered",
            facts_used=[],
            unknowns=["main_pain", "operation_context"],
            confidence="low",
            next_question="Qual e a principal dor hoje?",
        )
        draft.messages = [
            "Sem diagnostico, nao quero chutar um plano final.",
            "Posso te mostrar o comparativo direto ou fazer um diagnostico gratuito para entender o que organizar primeiro e qual faixa vale comparar.",
        ]

    if ("quais sao os planos" in normalized or "quero ver planos" in normalized) and "comparativo" not in joined_messages:
        draft.current_agent = PRODUCT_AGENT
        draft.decision.route = "product"
        draft.messages = [
            "Hoje os planos sao Base R$ 197/mes, Essencial R$ 497/mes, Avance R$ 897/mes e Completo R$ 1.497/mes.",
            "Posso te mostrar o comparativo direto ou recomendar um caminho pelo diagnostico gratuito.",
        ]

    if "o que e a taliya" in normalized or "entender melhor como funciona" in normalized:
        if "studio de pilates" not in joined_messages:
            draft.current_agent = PRODUCT_AGENT
            draft.decision.route = "product"
            draft.decision.detected_intents = ["product_how_it_works"]
            draft.decision.direct_question_present = True
            draft.decision.direct_question_answered_first = True
            draft.decision.template_ids = []

    if "como funciona no whatsapp" in normalized and "equipe continuar no controle" not in joined_messages:
        draft.current_agent = PRODUCT_AGENT
        draft.decision.route = "product"
        draft.messages = [
            "A ideia e a equipe continuar no controle, mas com a Taliya organizando contexto, historico e respostas da rotina.",
            "Ela ajuda a nao deixar conversa importante se perder. Hoje o WhatsApp pesa mais em atendimento, reposicoes ou vendas?",
        ]

    if "ia nao souber" in normalized and "nao deve inventar" not in joined_messages:
        draft.current_agent = ENTRY_AGENT
        draft.decision.route = "entry"
        draft.messages = [
            "Quando a Taliya nao tiver seguranca para responder, ela nao deve inventar.",
            "Nesses casos, o certo e pedir contexto ou passar para a equipe.",
        ]

    pain_signal = any(token in normalized for token in ("perco", "interessados", "reposicao", "agenda", "falta", "whatsapp"))
    product_question_signal = _is_product_question_signal(normalized)
    if pain_signal and not product_question_signal and not has_any_token(text, HUMAN_TOKENS):
        draft.current_agent = DIAGNOSTIC_AGENT
        draft.decision.route = "diagnostic"
        draft.decision.diagnostic_allowed_now = True
        draft.decision.diagnostic_action = "offer"
        draft.decision.template_ids = []
    if pain_signal and draft.current_agent == DIAGNOSTIC_AGENT and "diagnostico gratuito" not in joined_messages:
        draft.decision.diagnostic_allowed_now = True
        draft.decision.diagnostic_action = "offer"
        if not draft.diagnostic:
            draft.diagnostic = DiagnosticOutput(status="offered", unknowns=["operation_context"], confidence="low")
        draft.messages = [
            draft.messages[0] if draft.messages else "Entendi essa dor.",
            "Posso fazer um diagnostico gratuito com poucas perguntas e te dizer o caminho mais coerente: o que organizar primeiro, quais agentes fariam sentido e qual plano vale comparar.",
            "Quer que eu faca esse diagnostico?",
        ]

    buy_signal = any(token in normalized for token in ("assinar", "comprar", "contratar", "quero testar", "checkout"))
    accepted_waitlist = previous_state and previous_state.waitlist and _is_waitlist_acceptance(text)
    previous_diagnostic_completed = (
        previous_state
        and previous_state.diagnostic
        and previous_state.diagnostic.get("status") == "completed"
    )
    positive_after_diagnostic = bool(
        previous_diagnostic_completed
        and any(
            token in normalized
            for token in (
                "como comeco",
                "como começo",
                "quero comecar",
                "quero começar",
                "quero come",
                "quiser comecar",
                "quiser começar",
                "quiser come",
                "proximo passo",
                "próximo passo",
                "quero entrar",
                "quero contratar",
                "me avisa",
                "me coloca",
                "pode colocar",
                "coloca meu studio",
            )
        )
    )
    waitlist_acceptance_signal = _is_waitlist_acceptance(text)
    waitlist_details_ready = _has_waitlist_actionable_details(request)
    if buy_signal or positive_after_diagnostic:
        if positive_after_diagnostic and waitlist_acceptance_signal and waitlist_details_ready:
            waitlist_status: Literal["joined", "pending_details", "offered"] = "joined"
            waitlist_reason = "lead_accepted_waitlist_with_actionable_details"
            missing_fields: list[str] = []
            waitlist_messages = [
                "Perfeito, deixei seu studio na lista de espera da Taliya.",
                "Quando abrir uma proxima janela, a equipe chama com o contexto dessa conversa.",
            ]
        elif positive_after_diagnostic and waitlist_acceptance_signal:
            waitlist_status = "pending_details"
            waitlist_reason = "missing_waitlist_details"
            missing_fields = ["studio_name", "city_state"]
            waitlist_messages = [
                "Combinado. Para deixar a lista de espera acionável, ainda preciso do nome do studio e cidade/estado.",
                "Pode me mandar nessa mesma mensagem?",
            ]
        else:
            waitlist_status = "offered"
            waitlist_reason = "qualified_interest"
            missing_fields = []
            waitlist_messages = [
                "Estamos trabalhando com um numero pequeno de studios agora.",
                "Se fizer sentido, posso colocar seu studio na lista de espera e chamar assim que abrir uma proxima janela.",
            ]
        draft.current_agent = WAITLIST_AGENT
        draft.decision.route = "waitlist"
        draft.decision.waitlist_allowed_now = True
        draft.decision.diagnostic_action = "none"
        draft.diagnostic = None
        draft.waitlist_action = WaitlistAction(
            status=waitlist_status,
            reason=waitlist_reason,
            missing_fields=missing_fields,
        )
        draft.messages = waitlist_messages

    if accepted_waitlist:
        draft.current_agent = WAITLIST_AGENT
        draft.decision.route = "waitlist"
        draft.decision.waitlist_allowed_now = True
        draft.decision.next_question_kind = "waitlist_details"
        draft.waitlist_action = WaitlistAction(status="pending_details", reason="missing_waitlist_details", missing_fields=["studio_name", "city_state"])
        draft.messages = ["Perfeito. Para registrar certinho, qual e o nome do studio e de qual cidade ele e?"]

    if previous_state and previous_state.waitlist and previous_state.waitlist.get("status") == "joined" and "lista" in normalized:
        if "continua registrado" not in joined_messages:
            draft.current_agent = PRODUCT_AGENT
            draft.decision.route = "product"
            draft.messages = [
                "O Completo fica em R$ 1.497/mes.",
                "Seu studio continua registrado na lista de espera.",
            ]

    return draft


def _mock_message_for(request: AgentRunRequest) -> AgentMessage:
    text = (request.message.text or "").lower()
    channel = request.channel
    if "caro" in text or "carissimo" in text or "carÃ­ssimo" in text:
        return AgentMessage(
            text=(
                "Faz sentido olhar valor com cuidado. O melhor plano depende do tamanho do studio e do gargalo que mais custa tempo hoje; "
                "posso comparar as faixas e fazer um diagnostico rapido antes de qualquer proximo passo."
            ),
            channel_hint=channel,
        )
    if "pesquisando" in text or "sem pressa" in text:
        return AgentMessage(
            text=(
                "Sem pressa. Posso te mostrar os planos como referencia e, se quiser, deixo um diagnostico rapido para voce comparar com calma."
            ),
            channel_hint=channel,
            requires_product_source=True,
        )
    if "demo" in text or "demonstra" in text or "duvida" in text or "dÃºvida" in text:
        return AgentMessage(
            text=(
                "Nao vou te jogar para uma demo generica. A pagina oficial para demonstracao e /pilates/planos/demonstracao; "
                "antes disso, qual parte ficou mais importante ver na prática?"
            ),
            channel_hint=channel,
            requires_product_source=True,
        )
    if "qual plano" in text or "plano faz sentido" in text:
        return AgentMessage(
            text=(
                "Para recomendar plano sem chute, eu faria um diagnostico rapido: tamanho do studio, rotina que mais pesa e prioridade dos proximos 30 dias. "
                "Com isso eu comparo Base, Essencial, Avance e Completo sem empurrar assinatura direta."
            ),
            channel_hint=channel,
            requires_product_source=True,
        )
    if "preco" in text or "preÃ§o" in text or "custa" in text or "valor" in text:
        return AgentMessage(
            text=(
                "Claro. Hoje os planos da Taliya para studios de Pilates comecam em R$ 197/mes no Base, "
                "R$ 497/mes no Essencial, R$ 897/mes no Avance e R$ 1.497/mes no Completo. "
                "Se voce me contar o que mais pesa na rotina, eu te ajudo a entender qual faixa faz mais sentido."
            ),
            channel_hint=channel,
            requires_product_source=True,
        )
    if "ver planos" in text or text.strip() == "planos":
        return AgentMessage(
            text=(
                "Os planos oficiais sao Base, Essencial, Avance e Completo. Posso te explicar a diferenca por faixa e, se voce me disser a rotina que mais pesa hoje, eu comparo sem inventar link de pagamento."
            ),
            channel_hint=channel,
            requires_product_source=True,
        )
    if "taliya ficaria" in text or "caminho para comecar" in text or "caminho para comeÃ§ar" in text:
        return AgentMessage(
            text=(
                "Boa. A Taliya organiza a rotina comercial e operacional do studio sem exigir que voce siga um roteiro travado. "
                "Posso fazer um diagnostico rapido para entender onde agenda, reposicoes, vendas ou mensalidades mais pesam hoje."
            ),
            channel_hint=channel,
        )
    return AgentMessage(
        text=(
            "Oi. Eu te ajudo a entender a Taliya para Pilates, tirar duvidas de planos e enxergar onde o CRM pode aliviar a rotina do studio. "
            "Em que posso te ajudar agora? Se voce quiser, posso comecar por planos, diagnostico rapido da rotina ou uma duvida especifica sobre agenda, reposicoes, vendas e mensalidades."
        ),
        channel_hint=channel,
    )


def _build_diagnostic_output(user_text: str, evidence_id: str, channel: str) -> tuple[AgentMessage, list[LeadFact], DiagnosticOutput]:
    facts = [LeadFact.model_validate(fact) for fact in extract_lead_facts_from_text(user_text, evidence_id)]
    fact_keys = {fact.key for fact in facts}
    has_enough = "main_pain" in fact_keys and ("active_students" in fact_keys or "current_system" in fact_keys or "priority_goal" in fact_keys)
    if not has_enough:
        next_question = "Qual parte da rotina mais pesa hoje: agenda, reposicoes, interessados, mensalidades ou alunos inativos?"
        return (
            AgentMessage(text=next_question, channel_hint=channel),  # type: ignore[arg-type]
            facts,
            DiagnosticOutput(
                status="insufficient_evidence",
                facts_used=[fact.key for fact in facts],
                evidence=[evidence_id] if facts else [],
                unknowns=["main_pain", "operation_context"],
                confidence="low",
                next_question=next_question,
            ),
        )

    pain = next((fact.value for fact in facts if fact.key == "main_pain"), "rotina operacional")
    bottleneck = {
        "reposicoes": "reposicoes e agenda",
        "agenda": "agenda e encaixes",
        "whatsapp": "atendimento no WhatsApp",
        "vendas": "retorno de interessados",
        "financeiro": "mensalidades e renovacoes",
        "retencao": "frequencia e alunos em risco",
    }.get(pain, pain)
    message = (
        f"Pelo contexto que voce trouxe, o ponto que mais parece pesar hoje e {bottleneck}. "
        "O primeiro passo e transformar isso numa fila clara de proximas acoes, para a equipe nao depender de memoria ou planilha solta. "
        "Faz sentido com o que voce ve no dia a dia?"
    )
    return (
        AgentMessage(text=message, channel_hint=channel),  # type: ignore[arg-type]
        facts,
        DiagnosticOutput(
            status="completed",
            facts_used=[fact.key for fact in facts],
            main_bottleneck=bottleneck,
            likely_cause="rotina sem fila clara de proximas acoes e sem registro operacional consistente",
            first_recommended_step="organizar o gargalo em uma fila visivel de acoes e responsaveis",
            indicated_routines_or_agents=[pain],
            plan_or_range_to_compare="Comparar Essencial ou Avance depois de validar prioridade e volume",
            evidence=[evidence_id],
            unknowns=[],
            confidence="medium",
            next_question="Faz sentido com o que voce ve no dia a dia?",
            validation_question="Faz sentido com o que voce ve no dia a dia?",
        ),
    )


def _is_waitlist_acceptance(text: str) -> bool:
    lowered = text.lower()
    return any(token in lowered for token in ("pode colocar", "sim", "quero entrar", "me coloca", "coloca meu studio", "pode ser"))


def _has_waitlist_actionable_details(request: AgentRunRequest) -> bool:
    text = (request.message.text or "").lower()
    has_email_or_phone = bool("@" in text or any(char.isdigit() for char in text))
    has_contact = bool(request.sender.whatsapp_phone or request.sender.email) or bool(
        request.conversation.channel_conversation_id and request.channel == "whatsapp"
    ) or has_email_or_phone
    has_studio_or_city = any(token in text for token in ("studio", "estudio", "cidade", " em ", "sou de"))
    return has_contact and (has_studio_or_city or has_email_or_phone)


def _remaining_waitlist_missing_fields(request: AgentRunRequest, missing_fields: list[str]) -> list[str]:
    if not missing_fields:
        return []
    text = request.message.text or ""
    normalized = normalize_text(text)
    qualification = request.metadata.get("qualification")
    qualification_blob = json.dumps(qualification, ensure_ascii=False).lower() if isinstance(qualification, dict) else ""
    has_studio_name = (
        "studio" in normalized
        or "estudio" in normalized
        or "studioname" in qualification_blob
        or "studio_name" in qualification_blob
    )
    has_city_state = _looks_like_city_state_detail(text) or any(
        key in qualification_blob for key in ("citystate", "city_state", "studiocity", "studio_city")
    )

    remaining: list[str] = []
    for field in missing_fields:
        normalized_field = field.replace("/", "_")
        if normalized_field == "studio_name" and has_studio_name:
            continue
        if normalized_field == "city_state" and has_city_state:
            continue
        remaining.append(field)
    return remaining


def _looks_like_city_state_detail(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return False
    state_pattern = r"(?:AC|AL|AP|AM|BA|CE|DF|ES|GO|MA|MT|MS|MG|PA|PB|PR|PE|PI|RJ|RN|RS|RO|RR|SC|SP|SE|TO)"
    city_words = r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ\s'.-]{2,}"
    return bool(
        re.search(rf",\s*{city_words}\s+{state_pattern}\b", stripped, flags=re.IGNORECASE)
        or re.search(rf"\b{city_words}\s+{state_pattern}\b", stripped, flags=re.IGNORECASE)
    )


async def _record(
    memory_store: InMemoryMemoryStore,
    *,
    run_id: str,
    conversation_id: str,
    agent_key: str,
    type: str,
    agent: str,
    content: str = "",
    metadata: dict | None = None,
) -> None:
    safe_metadata = redact_trace_payload(metadata or {})
    await memory_store.record_event(
        RuntimeEvent(
            run_id=run_id,
            conversation_id=conversation_id,
            agent_key=agent_key,
            type=type,  # type: ignore[arg-type]
            agent=agent,
            content=content,
            metadata=safe_metadata,
        )
    )
    if type == "tool_call":
        await memory_store.record_tool_summary(
            conversation_id,
            {
                "run_id": run_id,
                "agent_key": agent_key,
                "agent": agent,
                "tool_name": content,
                "metadata": safe_metadata,
            },
        )
    if type == "guardrail":
        await memory_store.record_guardrail_event(
            conversation_id,
            {
                "run_id": run_id,
                "agent_key": agent_key,
                "agent": agent,
                "reason": content,
                "evidence": safe_metadata,
            },
        )
    if type == "usage":
        await memory_store.record_model_usage(
            conversation_id,
            {
                "run_id": run_id,
                "agent_key": agent_key,
                "agent": agent,
                **safe_metadata,
            },
        )


def _can_background_runtime_io(memory_store: InMemoryMemoryStore) -> bool:
    return memory_store.__class__.__name__ != "InMemoryMemoryStore"


def _schedule_runtime_background_task(label: str, coro: Any) -> None:
    async def runner() -> None:
        try:
            await coro
        except Exception as exc:
            print(f"[runtime-background:{label}] {type(exc).__name__}: {exc}")

    asyncio.create_task(runner())


def _usage_from_agent_result(result: Any, model: str, fallback_input: str, output_text: str) -> Any:
    input_tokens = 0
    output_tokens = 0
    for raw_response in getattr(result, "raw_responses", []) or []:
        usage = getattr(raw_response, "usage", None)
        input_tokens += int(getattr(usage, "input_tokens", 0) or 0)
        output_tokens += int(getattr(usage, "output_tokens", 0) or 0)
    if input_tokens == 0 and output_tokens == 0:
        input_tokens = max(1, len(fallback_input) // 4)
        output_tokens = max(1, len(output_text) // 4)
    return usage_from_tokens(model, input_tokens, output_tokens)


async def _interpret_contextual_widget_reply(
    request: AgentRunRequest,
    *,
    model: str,
) -> tuple[ContextualIntentDecision, Any]:
    shortcut = _local_contextual_widget_shortcut(request)
    if shortcut is not None:
        return shortcut, usage_from_tokens(model, 0, 0)

    settings = get_settings()
    if not settings.openai_api_key:
        return ContextualIntentDecision(intent="unclear", confidence="low", reason="missing_openai_api_key"), usage_from_tokens(model, 0, 0)

    try:
        from openai import AsyncOpenAI
    except Exception:
        return ContextualIntentDecision(intent="unclear", confidence="low", reason="openai_client_unavailable"), usage_from_tokens(model, 0, 0)

    schema = {
        "type": "object",
        "additionalProperties": False,
        "required": ["intent", "direct_question_kind", "confidence", "reason"],
        "properties": {
            "intent": {
                "type": "string",
                "enum": [
                    "accept_diagnostic",
                    "accept_and_ask_direct_question",
                    "ask_direct_question",
                    "acknowledgement_only",
                    "refuse_diagnostic",
                    "human_request",
                    "unclear",
                ],
            },
            "direct_question_kind": {
                "type": "string",
                "enum": ["price_or_plan", "demo", "whatsapp", "product", "human", "none"],
            },
            "confidence": {"type": "string", "enum": ["low", "medium", "high"]},
            "reason": {"type": "string"},
        },
    }
    prompt = {
        "task": "Interpret a free-form lead reply to a diagnostic invitation in the Taliya Pilates sales widget. Do not answer the lead.",
        "rules": [
            "Use the recent messages and current user message, not fixed keyword matching.",
            "If the lead clearly accepts the diagnostic without another question, use accept_diagnostic.",
            "If the lead asks price, plans, demo, WhatsApp, product, or human support, use ask_direct_question or accept_and_ask_direct_question.",
            "Direct questions must be answered before starting diagnostic.",
            "If the lead only acknowledges without a clear yes/no, use acknowledgement_only or unclear.",
            "If the lead declines or postpones, use refuse_diagnostic.",
        ],
        "client_pending_context": request.metadata.get("client_pending_context"),
        "recent_client_messages": request.metadata.get("recent_client_messages", []),
        "user_message": request.message.text,
    }
    started_input = json.dumps(prompt, ensure_ascii=False)
    try:
        async with AsyncOpenAI(api_key=settings.openai_api_key, timeout=3.5, max_retries=0) as client:
            result = await asyncio.wait_for(
                client.responses.create(
                    model=settings.guardrail_model or model,
                    input=[
                        {"role": "system", "content": "You classify contextual intent for a commercial sales agent. Return only JSON."},
                        {"role": "user", "content": started_input},
                    ],
                    text={
                        "format": {
                            "type": "json_schema",
                            "name": "taliya_contextual_intent",
                            "strict": False,
                            "schema": schema,
                        }
                    },
                ),
                timeout=3.8,
            ),
        raw_text = getattr(result, "output_text", "") or ""
        parsed = json.loads(raw_text)
        decision = ContextualIntentDecision.model_validate(parsed)
        usage = _usage_from_agent_result(result, settings.guardrail_model or model, started_input, raw_text)
        return decision, usage
    except Exception as exc:
        return _fallback_contextual_widget_intent(request, f"contextual_interpreter_failed:{type(exc).__name__}"), usage_from_tokens(settings.guardrail_model or model, max(1, len(started_input) // 4), 20)


async def _interpret_simple_opening_reply(
    request: AgentRunRequest,
    *,
    model: str,
) -> tuple[SimpleOpeningDecision, Any]:
    settings = get_settings()
    if not settings.openai_api_key:
        return SimpleOpeningDecision(route="needs_full_agent", confidence="low", reason="missing_openai_api_key"), usage_from_tokens(model, 0, 0)

    try:
        from openai import AsyncOpenAI
    except Exception:
        return SimpleOpeningDecision(route="needs_full_agent", confidence="low", reason="openai_client_unavailable"), usage_from_tokens(model, 0, 0)

    schema = {
        "type": "object",
        "additionalProperties": False,
        "required": ["route", "confidence", "reason"],
        "properties": {
            "route": {
                "type": "string",
                "enum": ["price_direct", "demo_direct", "thin_diagnostic", "needs_full_agent"],
            },
            "confidence": {"type": "string", "enum": ["low", "medium", "high"]},
            "reason": {"type": "string"},
        },
    }
    prompt = {
        "task": "Classify only simple first-turn Taliya Pilates sales openings. Do not answer the lead.",
        "routes": {
            "price_direct": "A direct question about price, values, monthly fee, or the list of plans. A message asking both price and what plans exist is still price_direct when it has no studio facts, pains, plan-fit context, WhatsApp implementation question, buying intent, or ambiguity.",
            "demo_direct": "Only a direct request for demo/demonstration/page to see the product, with no studio facts, pains, or ambiguity.",
            "thin_diagnostic": "Only a request to start the free diagnostic with no studio facts or other direct question.",
            "needs_full_agent": "Any mixed intent, pain, numbers, plan-fit question, WhatsApp/product implementation question, buying intent, refusal, human request, or unclear message.",
        },
        "hard_rule": "Do not send direct price/list-of-plans questions to needs_full_agent unless the lead also gives facts about their studio, asks which plan is ideal for their case, mentions pain, asks WhatsApp implementation details, or shows buying intent.",
        "examples": {
            "price_direct": ["quanto custa?", "quais planos existem?", "quanto custa a Taliya e quais planos existem?"],
            "demo_direct": ["tem demo?", "tem pagina para eu ver como funciona?"],
            "thin_diagnostic": ["quero fazer diagnostico gratuito", "pode fazer o diagnostico"],
            "needs_full_agent": ["tenho 80 alunos e quero o plano ideal", "agenda esta baguncada, quanto custa?", "como funciona no WhatsApp?"],
        },
        "user_message": request.message.text,
        "channel": request.channel,
    }
    started_input = json.dumps(prompt, ensure_ascii=False)
    try:
        async with AsyncOpenAI(api_key=settings.openai_api_key, timeout=3.0, max_retries=0) as client:
            result = await asyncio.wait_for(
                client.responses.create(
                    model=model,
                    input=[
                        {"role": "system", "content": "You are a strict routing classifier. Return only JSON. Prefer needs_full_agent if there is any doubt."},
                        {"role": "user", "content": started_input},
                    ],
                    text={
                        "format": {
                            "type": "json_schema",
                            "name": "taliya_simple_opening",
                            "strict": False,
                            "schema": schema,
                        }
                    },
                ),
                timeout=3.2,
            ),
        raw_text = getattr(result, "output_text", "") or ""
        decision = SimpleOpeningDecision.model_validate(json.loads(raw_text))
        usage = _usage_from_agent_result(result, model, started_input, raw_text)
        return decision, usage
    except Exception:
        return SimpleOpeningDecision(route="needs_full_agent", confidence="low", reason="simple_opening_interpreter_failed"), usage_from_tokens(model, 0, 0)


async def _interpret_interleaved_delivery_reply(
    request: AgentRunRequest,
    *,
    model: str,
) -> tuple[InterleavedDeliveryDecision, Any]:
    settings = get_settings()
    if not settings.openai_api_key:
        return InterleavedDeliveryDecision(action="process_normally", confidence="low", reason="missing_openai_api_key"), usage_from_tokens(model, 0, 0)

    try:
        from openai import AsyncOpenAI
    except Exception:
        return InterleavedDeliveryDecision(action="process_normally", confidence="low", reason="openai_client_unavailable"), usage_from_tokens(model, 0, 0)

    schema = {
        "type": "object",
        "additionalProperties": False,
        "required": ["action", "confidence", "reason"],
        "properties": {
            "action": {
                "type": "string",
                "enum": ["suppress_acknowledgement", "process_normally"],
            },
            "confidence": {"type": "string", "enum": ["low", "medium", "high"]},
            "reason": {"type": "string"},
        },
    }
    prompt = {
        "task": "Decide whether a WhatsApp user message sent while assistant chunks were still being delivered is only social acknowledgement/noise. Do not answer the lead.",
        "rules": [
            "Use suppress_acknowledgement only when the message merely acknowledges the assistant greeting or says the user is fine, with no acceptance, refusal, question, pain, fact, correction, urgency, price/demo/product/human request, or diagnostic answer.",
            "Use process_normally for any diagnostic acceptance such as yes/quero/pode ser, any business fact, any question, any complaint, any correction, any refusal, or any ambiguity with possible commercial meaning.",
            "When in doubt, use process_normally.",
        ],
        "recent_client_messages": request.metadata.get("recent_client_messages", []),
        "user_message": request.message.text,
    }
    started_input = json.dumps(prompt, ensure_ascii=False)
    try:
        async with AsyncOpenAI(api_key=settings.openai_api_key, timeout=3.0, max_retries=0) as client:
            result = await asyncio.wait_for(
                client.responses.create(
                    model=settings.guardrail_model or model,
                    input=[
                        {"role": "system", "content": "You classify WhatsApp delivery-interleaving noise for a sales agent. Return only JSON."},
                        {"role": "user", "content": started_input},
                    ],
                    text={
                        "format": {
                            "type": "json_schema",
                            "name": "taliya_interleaved_delivery_reply",
                            "strict": False,
                            "schema": schema,
                        }
                    },
                ),
                timeout=3.3,
            )
        raw_text = getattr(result, "output_text", "") or ""
        decision = InterleavedDeliveryDecision.model_validate(json.loads(raw_text))
        usage = _usage_from_agent_result(result, settings.guardrail_model or model, started_input, raw_text)
        return decision, usage
    except Exception:
        return InterleavedDeliveryDecision(action="process_normally", confidence="low", reason="interleaved_delivery_interpreter_failed"), usage_from_tokens(settings.guardrail_model or model, 0, 0)


def _local_contextual_widget_shortcut(request: AgentRunRequest) -> ContextualIntentDecision | None:
    normalized = normalize_text(request.message.text or "")
    if not normalized:
        return None

    asks_human = has_any_token(normalized, HUMAN_TOKENS)
    if asks_human:
        return ContextualIntentDecision(
            intent="human_request",
            direct_question_kind="human",
            confidence="high",
            reason="contextual_widget_shortcut:human_request_after_offer",
        )
    return None


def _fallback_contextual_widget_intent(request: AgentRunRequest, reason: str) -> ContextualIntentDecision:
    normalized = normalize_text(request.message.text or "")
    direct_question_kind: Literal["price_or_plan", "demo", "whatsapp", "product", "human", "none"] = "none"
    if any(token in normalized for token in ("preco", "custa", "valor", "plano", "planos")):
        direct_question_kind = "price_or_plan"
    elif any(token in normalized for token in ("demo", "demonstracao", "ver funcionando")):
        direct_question_kind = "demo"
    elif "whatsapp" in normalized:
        direct_question_kind = "whatsapp"
    elif has_any_token(normalized, HUMAN_TOKENS):
        direct_question_kind = "human"

    if direct_question_kind == "human":
        return ContextualIntentDecision(intent="human_request", direct_question_kind="human", confidence="medium", reason=reason)
    if direct_question_kind != "none":
        has_acceptance = any(token in normalized for token in ("sim", "ok", "pode", "quero", "claro", "beleza", "fechado"))
        return ContextualIntentDecision(
            intent="accept_and_ask_direct_question" if has_acceptance else "ask_direct_question",
            direct_question_kind=direct_question_kind,
            confidence="medium",
            reason=reason,
        )
    if any(token in normalized for token in ("nao", "não", "depois", "agora nao", "agora não")):
        return ContextualIntentDecision(intent="refuse_diagnostic", confidence="medium", reason=reason)
    if any(token in normalized for token in ("sim", "pode", "quero", "claro", "beleza", "fechado", "vamos", "bora")):
        return ContextualIntentDecision(intent="accept_diagnostic", confidence="medium", reason=reason)
    return ContextualIntentDecision(intent="unclear", confidence="low", reason=reason)


def _should_use_contextual_widget_fast_path(request: AgentRunRequest, previous_state: RuntimeState | None) -> bool:
    diagnostic_status = None
    if previous_state and isinstance(previous_state.diagnostic, dict):
        diagnostic_status = previous_state.diagnostic.get("status")
    has_widget_assistant_context = bool(
        request.metadata.get("client_has_prior_assistant_messages")
        and previous_state is None
    )
    return (
        request.channel == "widget"
        and (
            request.metadata.get("client_pending_context") == "widget_diagnostic_offer_pending"
            or _has_recent_widget_diagnostic_offer_context(request)
            or has_widget_assistant_context
        )
        and bool((request.message.text or "").strip())
        and (previous_state is None or diagnostic_status in {"offered", "in_progress", "insufficient_evidence"})
    )


def _zero_cost_template_route(request: AgentRunRequest, previous_state: RuntimeState | None) -> str | None:
    if previous_state is not None:
        return None
    if request.metadata.get("client_has_prior_assistant_messages"):
        return None
    text = request.message.text or ""
    normalized = normalize_text(text)
    if request.channel == "widget" and not normalized:
        return "entry"
    if is_cold_greeting_only(text):
        return "entry"
    if has_any_token(text, HUMAN_TOKENS):
        return "handoff"
    return None


def _should_use_zero_cost_template_path(request: AgentRunRequest, previous_state: RuntimeState | None) -> bool:
    return _zero_cost_template_route(request, previous_state) is not None


def _should_use_simple_opening_fast_path(request: AgentRunRequest, previous_state: RuntimeState | None) -> bool:
    if not get_settings().simple_opening_triage_enabled:
        return False
    if previous_state is not None:
        return False
    normalized = normalize_text(request.message.text or "")
    if not normalized or _has_context_sensitive_commercial_signal(normalized):
        return False
    return _is_simple_price_or_demo_question(normalized) or _is_simple_thin_diagnostic_request(normalized)


async def _run_interleaved_delivery_suppression_turn(
    request: AgentRunRequest,
    *,
    memory_store: InMemoryMemoryStore,
    model: str,
    previous_state: RuntimeState | None,
    run_id: str,
    trace_id: str,
) -> AgentRunResponse | None:
    decision, usage = await _interpret_interleaved_delivery_reply(request, model=model)
    if decision.action != "suppress_acknowledgement" or decision.confidence == "low":
        return None

    current_agent = previous_state.current_agent_name if previous_state else ENTRY_AGENT
    runtime_decision = RuntimeDecision(
        previous_state=previous_state.last_decision.get("current_state", "new_lead") if previous_state and previous_state.last_decision else "new_lead",
        current_state=previous_state.last_decision.get("next_state", "new_lead") if previous_state and previous_state.last_decision else "new_lead",
        next_state=previous_state.last_decision.get("next_state", "new_lead") if previous_state and previous_state.last_decision else "new_lead",
        route=previous_state.last_route if previous_state and previous_state.last_route in AGENT_BY_ROUTE else "entry",
        opening_type="returning_lead",
        detected_intents=["interleaved_delivery_acknowledgement"],
        direct_question_present=False,
        direct_question_answered_first=True,
        diagnostic_action="none",
        diagnostic_allowed_now=False,
        waitlist_allowed_now=False,
        template_ids=[],
    )
    output = AgentOutput(
        decision=runtime_decision,
        messages=[],
        usage=usage,
        confidence=decision.confidence,
    )
    state = previous_state.model_copy(deep=True) if previous_state else RuntimeState(
        conversation_id=request.conversation.conversation_id,
        agent_key=request.agent_key,
        current_agent_name=current_agent,
    )
    state.input_items.append({"role": "user", "content": request.message.text or "", "id": request.message.idempotency_key})
    state.current_agent_name = current_agent
    state.cost_usd = (previous_state.cost_usd if previous_state else 0) + usage.cost_usd
    state.last_decision = {**runtime_decision.model_dump(mode="json"), "cost_path": "interleaved_delivery_suppression", "reason": decision.reason}
    state.last_route = runtime_decision.route
    state.last_opening_type = runtime_decision.opening_type
    await memory_store.save_state(state)
    await _record(
        memory_store,
        run_id=run_id,
        conversation_id=request.conversation.conversation_id,
        agent_key=request.agent_key,
        type="guardrail",
        agent=TRIAGE_AGENT,
        content="suppressed interleaved social acknowledgement during WhatsApp chunk delivery",
        metadata={"decision": decision.model_dump(mode="json")},
    )
    await _record(
        memory_store,
        run_id=run_id,
        conversation_id=request.conversation.conversation_id,
        agent_key=request.agent_key,
        type="usage",
        agent=current_agent,
        content="interleaved_delivery_suppression",
        metadata=usage.__dict__,
    )
    return AgentRunResponse(
        run_id=run_id,
        conversation_id=request.conversation.conversation_id,
        lead_id=request.conversation.lead_id,
        agent_key=request.agent_key,
        current_agent=current_agent,
        status="succeeded",
        output=output,
        trace_id=trace_id,
    )


def _standard_cta_kind(request: AgentRunRequest, previous_state: RuntimeState | None) -> StandardCtaKind | None:
    normalized = normalize_text(request.message.text or "")
    entry_intent = normalize_text(request.conversation.entry_intent or "")
    if not normalized:
        return None

    if request.channel == "whatsapp" and normalized == OFFICIAL_SITE_WHATSAPP_CTA:
        return "site_cta"
    if entry_intent == "start_crm_diagnostic" and normalized in {"quero fazer diagnostico gratuito", "quero fazer diagnóstico gratuito"}:
        return "diagnostic_cta"
    if entry_intent == "guided_demo" and normalized.startswith("quero ver uma demo antes de assinar o plano ") and "me mostre o melhor caminho" in normalized:
        return "demo_cta"
    if entry_intent == "view_plans" and normalized.startswith("estou comparando os planos e quero confirmar se ") and "e o melhor para meu studio antes de assinar" in normalized:
        return "plan_compare_cta"
    if entry_intent == "waitlist_intent" and normalized.startswith("quero assinar o plano ") and "checkout seguro" in normalized:
        return "subscribe_cta"
    return None


def _select_llm_model_for_turn(request: AgentRunRequest, previous_state: RuntimeState | None, default_model: str) -> str:
    settings = get_settings()
    low_cost_model = settings.guardrail_model or default_model
    if previous_state is not None or low_cost_model == default_model:
        return default_model

    normalized = normalize_text(request.message.text or "")
    if not normalized:
        return default_model

    # This only selects the model for cost/latency. The selected LLM still conducts
    # the turn and returns structured JSON; it does not route or render by shortcut.
    if _has_context_sensitive_commercial_signal(normalized):
        return default_model
    if _is_simple_price_or_demo_question(normalized):
        return low_cost_model
    if _is_simple_thin_diagnostic_request(normalized):
        return low_cost_model
    return default_model


def _has_context_sensitive_commercial_signal(normalized_text: str) -> bool:
    if any(char.isdigit() for char in normalized_text):
        return True
    sensitive_tokens = (
        "aluno",
        "alunos",
        "lead",
        "leads",
        "agenda",
        "reposi",
        "falta",
        "faltas",
        "planilha",
        "caderno",
        "sistema",
        "whatsapp",
        "interessado",
        "interessados",
        "venda",
        "vendas",
        "financeiro",
        "cobranca",
        "cobrança",
        "acompanhamento",
        "dor",
        "problema",
        "bagunca",
        "bagunça",
        "urgente",
        "prioridade",
        "ideal",
        "serve",
        "meu studio",
        "minha rotina",
        "meu caso",
    )
    return any(token in normalized_text for token in sensitive_tokens)


def _is_simple_price_or_demo_question(normalized_text: str) -> bool:
    price_or_demo_tokens = (
        "preco",
        "preço",
        "custa",
        "valor",
        "valores",
        "plano",
        "planos",
        "mensalidade",
        "demo",
        "demonstracao",
        "demonstração",
        "ver funcionando",
    )
    return any(token in normalized_text for token in price_or_demo_tokens)


def _is_simple_thin_diagnostic_request(normalized_text: str) -> bool:
    diagnostic_tokens = ("diagnostico", "diagnóstico")
    acceptance_tokens = ("quero", "fazer", "faz", "gratuito", "gratis", "grátis", "pode", "sim")
    return any(token in normalized_text for token in diagnostic_tokens) and any(token in normalized_text for token in acceptance_tokens)


def _compact_previous_state_for_prompt(previous_state: RuntimeState | None) -> dict[str, Any]:
    if previous_state is None:
        return {}
    last_decision = previous_state.last_decision or {}
    decision_keys = (
        "previous_state",
        "current_state",
        "next_state",
        "route",
        "opening_type",
        "detected_intents",
        "diagnostic_action",
        "waitlist_allowed_now",
        "demo_status",
        "demo_next_step",
        "profile_name_usage",
        "template_ids",
        "diagnostic_ledger_status",
        "next_question_kind",
    )
    return {
        "current_agent_name": previous_state.current_agent_name,
        "last_decision": {key: last_decision.get(key) for key in decision_keys if key in last_decision},
        "last_route": previous_state.last_route,
        "last_opening_type": previous_state.last_opening_type,
        "diagnostic": _compact_diagnostic_for_prompt(previous_state.diagnostic),
        "post_diagnostic_context": _compact_post_diagnostic_context_for_prompt(previous_state),
        "waitlist": previous_state.waitlist,
        "demo": previous_state.demo,
        "human_status": previous_state.human_status,
        "human_reason": previous_state.human_reason,
        "lead_facts": previous_state.lead_facts[-12:],
        "recent_input_items": previous_state.input_items[-6:],
        "asked_questions": previous_state.asked_questions[-8:],
        "answered_direct_questions": previous_state.answered_direct_questions[-8:],
        "profile_name_status": previous_state.profile_name_status,
        "cost_usd": previous_state.cost_usd,
    }


def _compact_diagnostic_for_prompt(diagnostic: dict[str, Any] | None) -> dict[str, Any] | None:
    if not isinstance(diagnostic, dict):
        return None
    keys = (
        "status",
        "ledger",
        "facts_used",
        "unknowns",
        "main_bottleneck",
        "likely_cause",
        "first_recommended_step",
        "indicated_routines_or_agents",
        "plan_or_range_to_compare",
        "final_plan_line",
        "demo_status_at_delivery",
        "final_demo_line",
        "next_question",
        "validation_question",
        "confidence",
    )
    compact = {key: diagnostic.get(key) for key in keys if key in diagnostic}
    ledger = compact.get("ledger")
    if isinstance(ledger, list):
        compact["pending_question_key"] = next_question_key(ledger)
        compact["pending_question_text"] = next_question_text(ledger)
    return compact


def _compact_post_diagnostic_context_for_prompt(previous_state: RuntimeState | None) -> dict[str, Any] | None:
    if previous_state is None or not isinstance(previous_state.diagnostic, dict):
        return None
    diagnostic = previous_state.diagnostic
    if diagnostic.get("status") != "completed":
        return None
    indicated_agents = diagnostic.get("indicated_agents") or diagnostic.get("indicated_routines_or_agents") or []
    return {
        "pain_context_human": diagnostic.get("pain_context_human") or diagnostic.get("main_bottleneck"),
        "likely_cause": diagnostic.get("likely_cause"),
        "first_recommended_step": diagnostic.get("first_recommended_step"),
        "recommended_area": _recommended_area_from_diagnostic(_diagnostic_from_previous_state(previous_state)),
        "indicated_agents": indicated_agents,
        "recommended_plan_or_range": diagnostic.get("plan_or_range_to_compare") or diagnostic.get("final_plan_line"),
        "demo_status": (previous_state.demo or {}).get("status") if isinstance(previous_state.demo, dict) else None,
        "waitlist_status": (previous_state.waitlist or {}).get("status") if isinstance(previous_state.waitlist, dict) else None,
        "unknowns": diagnostic.get("unknowns") or [],
    }


def _product_knowledge_keys_for_prompt(request: AgentRunRequest, previous_state: RuntimeState | None) -> list[str]:
    normalized = normalize_text(request.message.text or "")
    keys: set[str] = {"unsupported_claims"}
    if any(token in normalized for token in ("preco", "valor", "custa", "plano", "planos", "assinatura", "mensalidade")):
        keys.update({"plans", "prices", "checkout_status", "waitlist_status"})
    if any(token in normalized for token in ("demo", "demonstracao", "ver funcionando")):
        keys.update({"demo_status", "links"})
    if any(token in normalized for token in ("whatsapp", "link", "site", "pagina")):
        keys.update({"links"})
    if any(token in normalized for token in ("como funciona", "me explica", "explica melhor", "o que a taliya faz", "como seria")):
        keys.update({"how_it_works", "routine_areas", "whatsapp_scope"})
    if "whatsapp" in normalized:
        keys.update({"whatsapp_scope"})
    if any(token in normalized for token in ("integra", "integracao", "instagram", "tecnofit", "next fit", "disparo em massa", "migracao", "migração")):
        keys.update({"whatsapp_scope", "integration_scope", "unsupported_claims"})
    if any(token in normalized for token in ("planilha", "caderno", "meu sistema", "ja tenho sistema", "já tenho sistema", "agenda?", "so uma agenda", "só uma agenda")):
        keys.update({"comparison_spreadsheet", "comparison_management_system", "routine_areas"})
    if any(token in normalized for token in ("seguro", "seguranca", "segurança", "lgpd", "privacidade", "dados", "conversas", "ia pode errar")):
        keys.update({"security_and_data", "privacy_or_data_notes"})
    if any(token in normalized for token in ("sou aluno", "professor autonomo", "professor autônomo", "academia", "clinica", "clínica", "ainda vou abrir")):
        keys.update({"out_of_profile"})
    if any(token in normalized for token in ("garantia", "cancel", "politica")):
        keys.update({"cancellation_or_guarantee_policy"})
    if any(token in normalized for token in ("disponivel", "disponibilidade", "quando abre", "vaga", "lista")):
        keys.update({"availability", "waitlist_status", "checkout_status"})
    if previous_state and previous_state.waitlist:
        keys.update({"waitlist_status"})
    if previous_state and previous_state.diagnostic and previous_state.diagnostic.get("status") == "completed":
        keys.update({"plans", "prices", "demo_status", "links", "waitlist_status", "checkout_status"})
        if any(token in normalized for token in ("como funciona", "me explica", "plano", "preco", "preço", "demo", "demonstracao", "caro", "pensar", "continuar")):
            keys.update({"how_it_works", "routine_areas", "availability_and_onboarding"})
    if not keys - {"unsupported_claims"}:
        keys.update({"checkout_status", "waitlist_status"})
    return sorted(keys)


def _compact_output_contract_for_prompt() -> dict[str, Any]:
    return {
        "current_agent": "entry|product|diagnostic|waitlist|handoff agent name",
        "decision": {
            "route": "entry|product|diagnostic|waitlist|handoff|safe_fallback",
            "opening_type": "none|cold_greeting_only|widget_opening|site_forced_message|social_source_opening|diagnostic_cta_opening|direct_question_opening|returning_lead",
            "detected_intents": [
                "normalized intents such as product_how_it_works, comparison_current_tool, integration_scope_question, trust_security_question, out_of_profile, conversation_resume, general_objection, diagnostic_refusal",
            ],
            "direct_question_present": "boolean",
            "direct_question_answered_first": "boolean",
            "diagnostic_action": "none|offer|start|ask_next|complete|insufficient_evidence",
            "diagnostic_allowed_now": "boolean",
            "waitlist_allowed_now": "boolean",
            "profile_name_usage": "used_reliable_name|ignored_unreliable_name|not_available|not_needed",
            "template_ids": ["prefer approved template ids when possible"],
            "policy_checks": "booleans for the critical guardrails",
        },
        "messages": ["1-3 concise pt-BR messages only when templates are not enough"],
        "lead_facts": "only facts explicitly supported by lead text/history",
        "diagnostic_answer_interpretation": {
            "when": "mandatory when diagnostic is in progress and the lead answers the pending diagnostic question; putting the answer only in facts_used is invalid because facts_used does not advance the diagnostic ledger",
            "current_question": "active_students_or_size|main_pain|pain_detail|current_process|priority|urgency",
            "answer_status": "answered|partial|unclear|refused|side_question",
            "answer_value": "human-readable answer only when supported by the current message",
            "areas": "normalized areas such as atendimento, vendas, agenda_reposicoes, financeiro, acompanhamento, gestao",
            "confidence": "low|medium|high",
            "evidence": "short exact snippets from the lead message; required when answer_status is answered",
            "needs_clarification": "true only as last resort when the answer cannot be interpreted safely",
            "additional_answers": "do not use to advance Taliya diagnostic questions; future details stay as context until officially asked",
            "example": {
                "pending_question": "active_students_or_size",
                "lead_message": "120",
                "required_output": {
                    "current_question": "active_students_or_size",
                    "answer_status": "answered",
                    "answer_value": "120",
                    "confidence": "high",
                    "evidence": ["120"],
                    "needs_clarification": False,
                },
            },
        },
        "diagnostic": "only when offered/in_progress/completed/insufficient_evidence",
        "waitlist_action": "only after real interest",
        "handoff": "only when human pause is needed",
        "confidence": "low|medium|high",
    }


def _turn_priorities_for_prompt(request: AgentRunRequest) -> list[str]:
    priorities = [
        "answer direct questions first",
        "use approved templates/ids when they match",
        "ask at most one focused diagnostic question",
        "never invent price/link/checkout/availability/promises",
        "treat 'como funciona' as a product explanation route, not an opening",
        "use studio-owner language and avoid technical SaaS terms for lay leads",
    ]
    pending_context = request.metadata.get("client_pending_context")
    if request.metadata.get("batched_during_assistant_delivery"):
        priorities.append(
            "this message arrived while previous assistant chunks were being delivered; do not repeat the previous explanation, and if it is only a social acknowledgement without a clear answer or question, return no user-facing messages"
        )
    if pending_context == "widget_diagnostic_offer_pending":
        priorities.append("interpret widget diagnostic-offer reply contextually; accept starts diagnostic, direct question is answered first")
    elif pending_context:
        priorities.append(f"honor explicit client context: {pending_context}")
    if request.message.type == "unsupported_media":
        priorities.append("unsupported media: ask for short text summary or offer human path")
    return priorities


def _llm_prompt_for(request: AgentRunRequest, previous_state: RuntimeState | None, source_payload: dict[str, Any]) -> str:
    initial_decision = _initial_decision_for_request(request, previous_state)
    profile = assess_profile_name(request.sender.name)
    return json.dumps(
        {
            "job": "Run the Taliya commercial sales conversation as an LLM-first attendant.",
            "policy_source": "Use the full behavior contract in your system instructions. This turn payload only adds state and official facts.",
            "turn_priorities": _turn_priorities_for_prompt(request),
            "initial_policy_read": initial_decision.model_dump(mode="json"),
            "profile_name_assessment": profile.__dict__,
            "channel": request.channel,
            "conversation": request.conversation.model_dump(mode="json"),
            "user_message": request.message.model_dump(mode="json"),
            "sender": request.sender.model_dump(mode="json"),
            "metadata": redact_trace_payload(request.metadata),
            "recent_client_messages": redact_trace_payload(request.metadata.get("recent_client_messages", [])),
            "previous_state": redact_trace_payload(_compact_previous_state_for_prompt(previous_state)),
            "product_knowledge": source_payload,
            "expected_output": _compact_output_contract_for_prompt(),
        },
        ensure_ascii=True,
    )


async def _run_llm_first_turn(
    request: AgentRunRequest,
    *,
    memory_store: InMemoryMemoryStore,
    model: str,
    previous_state: RuntimeState | None,
    run_id: str,
    trace_id: str,
) -> AgentRunResponse:
    try:
        from agents import Agent, AgentOutputSchema, Runner
    except Exception as exc:  # pragma: no cover - production dependency boundary
        raise RuntimeError("OpenAI Agents SDK is unavailable for non-mock runtime provider.") from exc

    source = get_product_knowledge_source()
    source_payload = source.query(_product_knowledge_keys_for_prompt(request, previous_state))
    prompt = _llm_prompt_for(request, previous_state, source_payload)
    agent = Agent(
        name=TRIAGE_AGENT,
        model=model,
        instructions=(
            "You are the Taliya commercial triage agent. Follow the OpenAI customer-service "
            "agents pattern: reason from context, choose the right specialist role, return "
            "structured output, and leave side effects to runtime tools.\n\n"
            f"{BEHAVIOR_POLICY_PROMPT}"
        ),
        output_type=AgentOutputSchema(LLMStructuredDraft, strict_json_schema=False),
    )
    result = await Runner.run(agent, prompt, max_turns=1)
    try:
        raw_draft = result.final_output_as(LLMStructuredDraft, raise_if_incorrect_type=True)
    except Exception as exc:
        coerced_draft = _coerce_llm_structured_draft(getattr(result, "final_output", None))
        if coerced_draft is None:
            coerced_draft = _coerce_llm_structured_draft_from_exception(exc)
        if coerced_draft is None:
            raise
        raw_draft = coerced_draft
    draft = _normalize_draft(raw_draft, request, previous_state)
    draft = _enforce_behavior_contract(draft, request, previous_state)
    previous_ledger = None
    if previous_state and previous_state.diagnostic:
        raw_ledger = previous_state.diagnostic.get("ledger")
        previous_ledger = raw_ledger if isinstance(raw_ledger, list) else None
    should_continue_diagnostic = (
        not _has_active_waitlist_action(draft.waitlist_action)
        and draft.decision.route not in {"waitlist", "handoff", "safe_fallback"}
        and (
            draft.decision.route == "diagnostic"
            or (previous_state is not None and previous_state.diagnostic is not None)
            or draft.diagnostic is not None
        )
    )
    if not draft.diagnostic and should_continue_diagnostic:
        draft.diagnostic = DiagnosticOutput(status="in_progress", confidence="low")
    if draft.diagnostic and should_continue_diagnostic:
        ledger = _diagnostic_ledger_for_turn(draft, request, previous_ledger)
        draft.diagnostic.ledger = ledger
        if ledger_is_complete(ledger) and draft.diagnostic.status != "completed":
            answered_values = [
                str(item.get("answer_value"))
                for item in ledger
                if item.get("answer_value")
            ]
            evidence = answered_values[:4]
            draft.diagnostic.status = "completed"
            _merge_diagnostic_facts_with_ledger(draft.diagnostic, answered_values)
            draft.diagnostic.evidence = draft.diagnostic.evidence or evidence
            answered_blob = normalize_text(" ".join([*_ledger_areas_from_items(ledger), *answered_values]))
            has_whatsapp_or_interest = any("whatsapp" in value.lower() or "interess" in value.lower() for value in answered_values) or "atendimento" in answered_blob
            inferred_bottleneck = _completed_diagnostic_bottleneck(ledger, answered_values)
            inferred_first_step = _completed_diagnostic_first_step(ledger, answered_values)
            inferred_plan_range = (
                "Essencial ou Avance"
                if has_whatsapp_or_interest or any("venda" in value.lower() for value in answered_values)
                else "a faixa mais aderente depois de validar a rotina prioritária"
            )
            if _is_generic_diagnostic_fragment(draft.diagnostic.main_bottleneck):
                draft.diagnostic.main_bottleneck = inferred_bottleneck
            draft.diagnostic.likely_cause = draft.diagnostic.likely_cause or "o atendimento e o acompanhamento ainda dependem demais de controle manual."
            if _is_generic_diagnostic_fragment(draft.diagnostic.first_recommended_step):
                draft.diagnostic.first_recommended_step = inferred_first_step
            inferred_routines = _infer_diagnostic_routines_from_ledger(ledger, answered_values)
            current_routines = [_display_agent_name(item) for item in draft.diagnostic.indicated_routines_or_agents]
            merged_routines: list[str] = []
            for routine in [*inferred_routines, *current_routines]:
                if routine and routine not in merged_routines:
                    merged_routines.append(routine)
            draft.diagnostic.indicated_routines_or_agents = merged_routines[:3] or inferred_routines
            if _is_generic_diagnostic_fragment(draft.diagnostic.plan_or_range_to_compare):
                draft.diagnostic.plan_or_range_to_compare = inferred_plan_range
            draft.diagnostic.unknowns = []
            draft.diagnostic.confidence = "medium"
            draft.diagnostic.next_question = None
            draft.diagnostic.validation_question = draft.diagnostic.validation_question or "Faz sentido com o que você vê no dia a dia?"
            draft.decision.diagnostic_action = "complete"
            draft.decision.diagnostic_allowed_now = True
        if draft.diagnostic.status == "completed" and not ledger_is_complete(ledger):
            draft.diagnostic.status = "insufficient_evidence"
            draft.diagnostic.next_question = next_question_text(ledger)
            draft.diagnostic.unknowns = list({*draft.diagnostic.unknowns, *[str(item.get("question_key")) for item in ledger if item.get("status") in {"missing", "unresolved"}]})
            draft.decision.diagnostic_action = "insufficient_evidence"
            draft.decision.diagnostic_allowed_now = True
    if (
        draft.waitlist_action
        and draft.waitlist_action.status in {"offered", "pending_details"}
        and previous_state
        and previous_state.waitlist
        and _is_waitlist_acceptance(request.message.text or "")
        and _has_waitlist_actionable_details(request)
    ):
        draft.waitlist_action.status = "joined"
        draft.waitlist_action.reason = "lead_accepted_waitlist_with_actionable_details"
        draft.waitlist_action.missing_fields = []
        draft.current_agent = WAITLIST_AGENT
        draft.decision.route = "waitlist"
        draft.decision.waitlist_allowed_now = True
        draft.decision.diagnostic_action = "none"
        draft.messages = [
            "Perfeito, deixei seu studio na lista de espera da Taliya. Quando abrir uma proxima janela, a equipe chama com o contexto dessa conversa."
        ]
    draft = _apply_decision_contract(draft, request, previous_state)
    rendered_messages = render_template_plan(
        draft.decision.template_ids,
        channel=request.channel,
        variables_by_template=draft.decision.template_variables,
    )
    rendered_messages = _ensure_first_turn_greeting_in_messages(
        rendered_messages,
        request=request,
        previous_state=previous_state,
    )
    message_texts = [message.text.strip() for message in rendered_messages if message.text.strip()]
    if not message_texts:
        message_texts = [text.strip() for text in draft.messages if text.strip()][:3]
        message_texts = _ensure_first_turn_greeting_in_texts(
            message_texts,
            request=request,
            previous_state=previous_state,
        )
    output_text = "\n\n".join(message_texts)
    context = TaliyaCommercialContext(
        conversation_id=request.conversation.conversation_id,
        lead_id=request.conversation.lead_id,
        memory_store=memory_store,
        state=previous_state.model_dump() if previous_state else {},
    )

    tool_results = []
    if draft.lead_facts:
        saved = await save_lead_facts(
            context,
            idempotency_key=f"facts:{request.message.idempotency_key}",
            facts=[fact.model_dump() for fact in draft.lead_facts],
        )
        tool_results.append({"name": "save_lead_facts", "status": "ok", "summary": str(saved.get("saved_count", 0))})
    if draft.diagnostic:
        saved = await save_diagnostic_record(
            context,
            idempotency_key=f"diagnostic:{request.message.idempotency_key}",
            diagnostic=draft.diagnostic.model_dump(),
        )
        tool_results.append({"name": "save_diagnostic_record", "status": "ok", "summary": saved.get("diagnostic_status")})
    if draft.waitlist_action and draft.waitlist_action.status != "none":
        saved = await mark_waitlist(
            context,
            idempotency_key=f"waitlist:{request.message.idempotency_key}",
            status=draft.waitlist_action.status,
            reason=draft.waitlist_action.reason,
            missing_fields=draft.waitlist_action.missing_fields,
        )
        tool_results.append({"name": "mark_waitlist", "status": "ok", "summary": saved.get("status")})
    if draft.handoff and draft.handoff.status in {"requested", "active"}:
        await pause_for_human(
            context,
            idempotency_key=f"handoff:request:{request.message.idempotency_key}",
            reason=draft.handoff.reason or "lead_requested_human",
        )
        tool_results.append({"name": "pause_for_human", "status": "ok", "summary": draft.handoff.status})

    usage = _usage_from_agent_result(result, model, prompt, output_text)
    usage_record = build_usage_record(
        run_id=run_id,
        conversation_id=request.conversation.conversation_id,
        agent_key=request.agent_key,
        operation="runner",
        usage=usage,
        budget_before=previous_state.cost_usd if previous_state else 0,
        review_cost_usd=get_settings().review_cost_usd,
        hard_cost_cap_usd=get_settings().hard_cost_cap_usd,
    )
    output = AgentOutput(
        decision=draft.decision,
        messages=rendered_messages
        if rendered_messages
        else [AgentMessage(text=text, channel_hint=request.channel) for text in message_texts],
        lead_facts=draft.lead_facts,
        diagnostic=draft.diagnostic,
        waitlist_action=draft.waitlist_action,
        handoff=draft.handoff,
        sources=[SourceRef(type="product_knowledge", version=source.version, keys=draft.source_keys or ["product_knowledge"])],
        safety_flags=[],
        tool_results=tool_results,
        usage=usage,
        confidence=draft.confidence,
    )
    human_status = "active" if draft.handoff and draft.handoff.status in {"requested", "active"} else "none"
    state = RuntimeState(
        conversation_id=request.conversation.conversation_id,
        agent_key=request.agent_key,
        current_agent_name=draft.current_agent,
        input_items=(previous_state.input_items if previous_state else [])
        + [{"role": "user", "content": request.message.text or "", "id": request.message.idempotency_key}],
        lead_facts=[fact.model_dump() for fact in draft.lead_facts],
        diagnostic=draft.diagnostic.model_dump() if draft.diagnostic else None,
        demo={"status": draft.decision.demo_status, "next_step": draft.decision.demo_next_step},
        waitlist=draft.waitlist_action.model_dump() if draft.waitlist_action else None,
        human_status=human_status,
        human_reason=draft.handoff.reason if draft.handoff else None,
        last_decision=draft.decision.model_dump(mode="json"),
        last_route=draft.decision.route,
        last_opening_type=draft.decision.opening_type,
        asked_questions=[draft.diagnostic.next_question] if draft.diagnostic and draft.diagnostic.next_question else [],
        answered_direct_questions=draft.decision.facts_used if draft.decision.direct_question_present else [],
        profile_name_status=draft.decision.profile_name_usage,
        product_source_version=source.version,
        cost_usd=usage_record.budget_after,
    )
    await memory_store.save_state(state)
    await _record(
        memory_store,
        run_id=run_id,
        conversation_id=request.conversation.conversation_id,
        agent_key=request.agent_key,
        type="handoff" if draft.current_agent != ENTRY_AGENT else "message",
        agent=TRIAGE_AGENT,
        content=f"{TRIAGE_AGENT} -> {draft.current_agent}",
        metadata={
            "source_agent": TRIAGE_AGENT,
            "target_agent": draft.current_agent,
            "decision": draft.decision.model_dump(mode="json"),
        },
    )
    for tool_result in tool_results:
        await _record(
            memory_store,
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            type="tool_call",
            agent=draft.current_agent,
            content=tool_result["name"],
            metadata=tool_result,
        )
    await _record(
        memory_store,
        run_id=run_id,
        conversation_id=request.conversation.conversation_id,
        agent_key=request.agent_key,
        type="usage",
        agent=draft.current_agent,
        content=usage.model or "",
        metadata=usage_record.__dict__,
    )
    return AgentRunResponse(
        run_id=run_id,
        conversation_id=request.conversation.conversation_id,
        lead_id=request.conversation.lead_id,
        agent_key=request.agent_key,
        current_agent=draft.current_agent,
        status="human_paused" if human_status == "active" else "succeeded",
        output=output,
        trace_id=trace_id,
    )


async def _run_contextual_widget_fast_turn(
    request: AgentRunRequest,
    *,
    memory_store: InMemoryMemoryStore,
    model: str,
    previous_state: RuntimeState | None,
    run_id: str,
    trace_id: str,
) -> AgentRunResponse:
    source = get_product_knowledge_source()
    decision, usage = await _interpret_contextual_widget_reply(request, model=model)
    text = request.message.text or ""

    if decision.intent == "human_request" or decision.direct_question_kind == "human":
        draft = LLMStructuredDraft(
            current_agent=HANDOFF_AGENT,
            decision=_decision_for_route(request, previous_state, "handoff"),
            handoff=HandoffOutput(status="requested", reason="lead_requested_human"),
        )
    elif decision.intent == "accept_diagnostic":
        draft = LLMStructuredDraft(
            current_agent=DIAGNOSTIC_AGENT,
            decision=RuntimeDecision(
                route="diagnostic",
                opening_type="none",
                detected_intents=["accepted_widget_diagnostic_offer"],
                diagnostic_action="ask_next",
                diagnostic_allowed_now=True,
                waitlist_allowed_now=False,
            ),
            diagnostic=DiagnosticOutput(
                status="in_progress",
                facts_used=[],
                unknowns=["active_students_or_size"],
                confidence=decision.confidence,
                next_question="Hoje seu studio tem mais ou menos quantos alunos ativos?",
            ),
            confidence=decision.confidence,
        )
        draft.decision.template_ids = ["diagnostic.ask_active_students"]
        draft.decision.template_variables = {
            "diagnostic.ask_active_students": {
                "answer_feedback": "Beleza então. Pra te devolver algo útil, preciso entender rapidinho como está a rotina do studio hoje."
            }
        }
        draft.decision = _sync_decision_state(draft.decision, previous_state)
    elif decision.intent in {"ask_direct_question", "accept_and_ask_direct_question"}:
        draft = LLMStructuredDraft(
            current_agent=PRODUCT_AGENT,
            decision=_decision_for_route(request, previous_state, "product"),
            diagnostic=DiagnosticOutput(status="offered", confidence="low") if decision.intent == "accept_and_ask_direct_question" else None,
            confidence=decision.confidence,
        )
        draft = _apply_decision_contract(draft, request, previous_state)
    elif decision.intent == "refuse_diagnostic":
        draft = LLMStructuredDraft(
            current_agent=ENTRY_AGENT,
            decision=_decision_for_route(request, previous_state, "entry"),
            messages=[
                "Tudo bem, sem problema.",
                "Posso tirar uma dúvida sobre a Taliya, planos, demo ou funcionamento no WhatsApp.",
            ],
            confidence=decision.confidence,
        )
    else:
        draft = LLMStructuredDraft(
            current_agent=ENTRY_AGENT,
            decision=_decision_for_route(request, previous_state, "entry"),
            messages=["Você quer que eu comece o diagnóstico gratuito ou prefere tirar alguma dúvida primeiro?"],
            confidence=decision.confidence,
        )

    rendered_messages = render_template_plan(
        draft.decision.template_ids,
        channel=request.channel,
        variables_by_template=draft.decision.template_variables,
    )
    rendered_messages = _ensure_first_turn_greeting_in_messages(
        rendered_messages,
        request=request,
        previous_state=previous_state,
    )
    if not rendered_messages:
        rendered_messages = [AgentMessage(text=message, channel_hint=request.channel) for message in draft.messages[:3]]

    context = TaliyaCommercialContext(
        conversation_id=request.conversation.conversation_id,
        lead_id=request.conversation.lead_id,
        memory_store=memory_store,
        state=previous_state.model_dump() if previous_state else {},
    )
    zero_cost_acceptance = (
        decision.intent == "accept_diagnostic"
        and usage.input_tokens == 0
        and usage.output_tokens == 0
        and draft.handoff is None
    )
    tool_results = []
    if draft.diagnostic and not zero_cost_acceptance:
        saved = await save_diagnostic_record(
            context,
            idempotency_key=f"diagnostic:{request.message.idempotency_key}",
            diagnostic=draft.diagnostic.model_dump(),
        )
        tool_results.append({"name": "save_diagnostic_record", "status": "ok", "summary": str(saved.get("status", ""))})
    if draft.handoff:
        paused = await pause_for_human(
            context,
            idempotency_key=f"handoff:request:{request.message.idempotency_key}",
            reason=draft.handoff.reason or "lead_requested_human",
        )
        tool_results.append({"name": "pause_for_human", "status": "ok", "summary": str(paused.get("status", ""))})

    usage_record = build_usage_record(
        run_id=run_id,
        conversation_id=request.conversation.conversation_id,
        agent_key=request.agent_key,
        operation="contextual_widget_interpreter",
        usage=usage,
        budget_before=previous_state.cost_usd if previous_state else 0,
        review_cost_usd=get_settings().review_cost_usd,
        hard_cost_cap_usd=get_settings().hard_cost_cap_usd,
    )
    state = RuntimeState(
        conversation_id=request.conversation.conversation_id,
        agent_key=request.agent_key,
        current_agent_name=draft.current_agent,
        input_items=(previous_state.input_items if previous_state else [])
        + [{"role": "user", "content": text, "id": request.message.idempotency_key}],
        diagnostic=draft.diagnostic.model_dump() if draft.diagnostic else (previous_state.diagnostic if previous_state else None),
        waitlist=draft.waitlist_action.model_dump() if draft.waitlist_action else (previous_state.waitlist if previous_state else None),
        human_status="active" if draft.handoff else (previous_state.human_status if previous_state else "none"),
        human_reason=draft.handoff.reason if draft.handoff else (previous_state.human_reason if previous_state else None),
        product_source_version=source.version,
        cost_usd=usage_record.budget_after,
        last_decision={**draft.decision.model_dump(mode="json"), "contextual_intent": decision.model_dump(mode="json")},
        last_route=draft.decision.route,
        last_opening_type=draft.decision.opening_type,
    )
    await memory_store.save_state(state)
    if not zero_cost_acceptance:
        await _record(
            memory_store,
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            type="handoff",
            agent=TRIAGE_AGENT,
            content=f"{TRIAGE_AGENT} -> {draft.current_agent}",
            metadata={"contextual_intent": decision.model_dump(mode="json")},
        )
        for result in tool_results:
            await _record(
                memory_store,
                run_id=run_id,
                conversation_id=request.conversation.conversation_id,
                agent_key=request.agent_key,
                type="tool_call",
                agent=draft.current_agent,
                content=str(result["name"]),
                metadata=result,
            )
        for message in rendered_messages:
            await _record(
                memory_store,
                run_id=run_id,
                conversation_id=request.conversation.conversation_id,
                agent_key=request.agent_key,
                type="message",
                agent=draft.current_agent,
                content=message.text,
            )
        await memory_store.record_model_usage(request.conversation.conversation_id, usage_record.__dict__)
        await _record(
            memory_store,
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            type="usage",
            agent=draft.current_agent,
            content=usage.model or "",
            metadata=usage_record.__dict__,
        )
    output = AgentOutput(
        decision=draft.decision,
        messages=rendered_messages,
        lead_facts=[],
        diagnostic=draft.diagnostic,
        waitlist_action=draft.waitlist_action,
        handoff=draft.handoff,
        sources=[SourceRef(type="product_knowledge", version=source.version, keys=["plans", "prices", "links"])],
        tool_results=tool_results,
        usage=usage,
        confidence=draft.confidence,
    )
    return AgentRunResponse(
        run_id=run_id,
        conversation_id=request.conversation.conversation_id,
        lead_id=request.conversation.lead_id,
        agent_key=request.agent_key,
        current_agent=draft.current_agent,
        status="human_paused" if draft.handoff else "succeeded",
        output=output,
        trace_id=trace_id,
    )


async def _run_simple_opening_fast_turn(
    request: AgentRunRequest,
    *,
    memory_store: InMemoryMemoryStore,
    model: str,
    previous_state: RuntimeState | None,
    run_id: str,
    trace_id: str,
) -> AgentRunResponse | None:
    source = get_product_knowledge_source()
    decision, usage = await _interpret_simple_opening_reply(request, model=model)
    if decision.route == "needs_full_agent" or decision.confidence == "low":
        return None

    if decision.route == "price_direct":
        draft = LLMStructuredDraft(
            current_agent=PRODUCT_AGENT,
            decision=RuntimeDecision(
                route="product",
                opening_type="direct_question_opening",
                detected_intents=["product", "price"],
                direct_question_present=True,
                direct_question_answered_first=True,
                diagnostic_action="offer",
                diagnostic_allowed_now=True,
                waitlist_allowed_now=False,
                template_ids=["product.price_direct", "diagnostic.price_hook"],
            ),
            diagnostic=DiagnosticOutput(status="offered", confidence=decision.confidence),
            confidence=decision.confidence,
        )
    elif decision.route == "demo_direct":
        draft = LLMStructuredDraft(
            current_agent=PRODUCT_AGENT,
            decision=RuntimeDecision(
                route="product",
                opening_type="direct_question_opening",
                detected_intents=["product", "demo_request"],
                direct_question_present=True,
                direct_question_answered_first=True,
                diagnostic_action="none",
                diagnostic_allowed_now=False,
                waitlist_allowed_now=False,
                demo_status="offered",
                demo_next_step="ask_demo_reaction",
                template_ids=["product.demo_direct"],
            ),
            confidence=decision.confidence,
        )
    else:
        draft = LLMStructuredDraft(
            current_agent=DIAGNOSTIC_AGENT,
            decision=RuntimeDecision(
                route="diagnostic",
                opening_type="diagnostic_cta_opening",
                detected_intents=["diagnostic_request"],
                direct_question_present=False,
                direct_question_answered_first=True,
                diagnostic_action="ask_next",
                diagnostic_allowed_now=True,
                waitlist_allowed_now=False,
                template_ids=["diagnostic.ask_active_students"],
            ),
            diagnostic=DiagnosticOutput(
                status="in_progress",
                facts_used=[],
                unknowns=["active_students_or_size"],
                confidence=decision.confidence,
                next_question="Hoje seu studio tem mais ou menos quantos alunos ativos?",
            ),
            confidence=decision.confidence,
        )
        draft.decision.template_variables = {
            "diagnostic.ask_active_students": {
                "answer_feedback": "Claro, faço sim. Pra te devolver algo útil, vou entender rapidinho como está a rotina do studio hoje."
            }
        }

    draft.decision = _sync_decision_state(draft.decision, previous_state)
    draft.decision.template_variables = _template_variables_for(draft, previous_state=previous_state) | draft.decision.template_variables
    rendered_messages = render_template_plan(
        draft.decision.template_ids,
        channel=request.channel,
        variables_by_template=draft.decision.template_variables,
    )
    rendered_messages = _ensure_first_turn_greeting_in_messages(
        rendered_messages,
        request=request,
        previous_state=previous_state,
    )
    if not rendered_messages:
        return None

    context = TaliyaCommercialContext(
        conversation_id=request.conversation.conversation_id,
        lead_id=request.conversation.lead_id,
        memory_store=memory_store,
        state=previous_state.model_dump() if previous_state else {},
    )
    tool_results = []
    if draft.diagnostic:
        saved = await save_diagnostic_record(
            context,
            idempotency_key=f"diagnostic:{request.message.idempotency_key}",
            diagnostic=draft.diagnostic.model_dump(),
        )
        tool_results.append({"name": "save_diagnostic_record", "status": "ok", "summary": str(saved.get("status", ""))})

    usage_record = build_usage_record(
        run_id=run_id,
        conversation_id=request.conversation.conversation_id,
        agent_key=request.agent_key,
        operation="simple_opening_interpreter",
        usage=usage,
        budget_before=previous_state.cost_usd if previous_state else 0,
        review_cost_usd=get_settings().review_cost_usd,
        hard_cost_cap_usd=get_settings().hard_cost_cap_usd,
    )
    state = RuntimeState(
        conversation_id=request.conversation.conversation_id,
        agent_key=request.agent_key,
        current_agent_name=draft.current_agent,
        input_items=(previous_state.input_items if previous_state else [])
        + [{"role": "user", "content": request.message.text or "", "id": request.message.idempotency_key}],
        diagnostic=draft.diagnostic.model_dump() if draft.diagnostic else (previous_state.diagnostic if previous_state else None),
        waitlist=previous_state.waitlist if previous_state else None,
        human_status=previous_state.human_status if previous_state else "none",
        human_reason=previous_state.human_reason if previous_state else None,
        product_source_version=source.version,
        cost_usd=usage_record.budget_after,
        last_decision={**draft.decision.model_dump(mode="json"), "simple_opening_decision": decision.model_dump(mode="json")},
        last_route=draft.decision.route,
        last_opening_type=draft.decision.opening_type,
    )
    await memory_store.save_state(state)
    await _record(
        memory_store,
        run_id=run_id,
        conversation_id=request.conversation.conversation_id,
        agent_key=request.agent_key,
        type="handoff",
        agent=TRIAGE_AGENT,
        content=f"{TRIAGE_AGENT} -> {draft.current_agent}",
        metadata={"simple_opening_decision": decision.model_dump(mode="json")},
    )
    for result in tool_results:
        await _record(
            memory_store,
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            type="tool_call",
            agent=draft.current_agent,
            content=str(result["name"]),
            metadata=result,
        )
    for message in rendered_messages:
        await _record(
            memory_store,
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            type="message",
            agent=draft.current_agent,
            content=message.text,
        )
    await memory_store.record_model_usage(request.conversation.conversation_id, usage_record.__dict__)
    await _record(
        memory_store,
        run_id=run_id,
        conversation_id=request.conversation.conversation_id,
        agent_key=request.agent_key,
        type="usage",
        agent=draft.current_agent,
        content=usage.model or "",
        metadata=usage_record.__dict__,
    )
    output = AgentOutput(
        decision=draft.decision,
        messages=rendered_messages,
        lead_facts=[],
        diagnostic=draft.diagnostic,
        waitlist_action=None,
        handoff=None,
        sources=[SourceRef(type="product_knowledge", version=source.version, keys=_product_knowledge_keys_for_prompt(request, previous_state))],
        tool_results=tool_results,
        usage=usage,
        confidence=draft.confidence,
    )
    return AgentRunResponse(
        run_id=run_id,
        conversation_id=request.conversation.conversation_id,
        lead_id=request.conversation.lead_id,
        agent_key=request.agent_key,
        current_agent=draft.current_agent,
        status="succeeded",
        output=output,
        trace_id=trace_id,
    )


async def _run_standard_cta_fast_turn(
    request: AgentRunRequest,
    *,
    memory_store: InMemoryMemoryStore,
    previous_state: RuntimeState | None,
    run_id: str,
    trace_id: str,
    cta_kind: StandardCtaKind,
) -> AgentRunResponse:
    source = get_product_knowledge_source()
    draft = _draft_for_standard_cta(request, previous_state, cta_kind)
    draft.decision = _sync_decision_state(
        draft.decision,
        previous_state,
        waitlist_status=draft.waitlist_action.status if draft.waitlist_action else None,
    )
    draft.decision.template_variables = _template_variables_for(draft, previous_state=previous_state) | draft.decision.template_variables
    rendered_messages = render_template_plan(
        draft.decision.template_ids,
        channel=request.channel,
        variables_by_template=draft.decision.template_variables,
    )
    rendered_messages = _ensure_first_turn_greeting_in_messages(
        rendered_messages,
        request=request,
        previous_state=None,
    )

    context = TaliyaCommercialContext(
        conversation_id=request.conversation.conversation_id,
        lead_id=request.conversation.lead_id,
        memory_store=memory_store,
        state=previous_state.model_dump() if previous_state else {},
    )
    tool_results = []
    if draft.waitlist_action and draft.waitlist_action.status != "none":
        saved_waitlist = await mark_waitlist(
            context,
            idempotency_key=f"waitlist:{request.message.idempotency_key}",
            status=draft.waitlist_action.status,
            reason=draft.waitlist_action.reason,
            missing_fields=draft.waitlist_action.missing_fields,
        )
        tool_results.append({"name": "mark_waitlist", "status": "ok", "summary": str(saved_waitlist.get("status", ""))})

    usage = usage_from_tokens(None, 0, 0)
    state = RuntimeState(
        conversation_id=request.conversation.conversation_id,
        agent_key=request.agent_key,
        current_agent_name=draft.current_agent,
        input_items=(previous_state.input_items if previous_state else [])
        + [{"role": "user", "content": request.message.text or "", "id": request.message.idempotency_key}],
        diagnostic=draft.diagnostic.model_dump() if draft.diagnostic else (previous_state.diagnostic if previous_state else None),
        waitlist=draft.waitlist_action.model_dump() if draft.waitlist_action else (previous_state.waitlist if previous_state else None),
        human_status=previous_state.human_status if previous_state else "none",
        human_reason=previous_state.human_reason if previous_state else None,
        demo={"status": draft.decision.demo_status, "next_step": draft.decision.demo_next_step} if draft.decision.demo_status else (previous_state.demo if previous_state else None),
        product_source_version=source.version,
        cost_usd=previous_state.cost_usd if previous_state else 0,
        last_decision={**draft.decision.model_dump(mode="json"), "cost_path": "standard_cta_fast", "standard_cta_kind": cta_kind},
        last_route=draft.decision.route,
        last_opening_type=draft.decision.opening_type,
    )
    await memory_store.save_state(state)

    async def record_standard_cta_observability() -> None:
        await _record(
            memory_store,
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            type="handoff",
            agent=TRIAGE_AGENT,
            content=f"{TRIAGE_AGENT} -> {draft.current_agent}",
            metadata={"cost_path": "standard_cta_fast", "standard_cta_kind": cta_kind},
        )
        for result in tool_results:
            await _record(
                memory_store,
                run_id=run_id,
                conversation_id=request.conversation.conversation_id,
                agent_key=request.agent_key,
                type="tool_call",
                agent=draft.current_agent,
                content=str(result["name"]),
                metadata=result,
            )
        for message in rendered_messages:
            await _record(
                memory_store,
                run_id=run_id,
                conversation_id=request.conversation.conversation_id,
                agent_key=request.agent_key,
                type="message",
                agent=draft.current_agent,
                content=message.text,
            )
        await _record(
            memory_store,
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            type="usage",
            agent=draft.current_agent,
            content="standard_cta_fast",
            metadata={"model": None, "input_tokens": 0, "output_tokens": 0, "cost_usd": 0},
        )

    if _can_background_runtime_io(memory_store):
        _schedule_runtime_background_task("standard_cta_observability", record_standard_cta_observability())
    else:
        await record_standard_cta_observability()

    output = AgentOutput(
        decision=draft.decision,
        messages=rendered_messages,
        diagnostic=draft.diagnostic,
        waitlist_action=draft.waitlist_action,
        sources=[SourceRef(type="product_knowledge", version=source.version, keys=_product_knowledge_keys_for_prompt(request, previous_state))],
        tool_results=tool_results,
        usage=usage,
        confidence=draft.confidence,
    )
    return AgentRunResponse(
        run_id=run_id,
        conversation_id=request.conversation.conversation_id,
        lead_id=request.conversation.lead_id,
        agent_key=request.agent_key,
        current_agent=draft.current_agent,
        status="succeeded",
        output=output,
        trace_id=trace_id,
    )


def _draft_for_standard_cta(
    request: AgentRunRequest,
    previous_state: RuntimeState | None,
    cta_kind: StandardCtaKind,
) -> LLMStructuredDraft:
    if cta_kind == "site_cta":
        return LLMStructuredDraft(
            current_agent=ENTRY_AGENT,
            decision=RuntimeDecision(
                route="entry",
                opening_type="site_forced_message",
                detected_intents=["site_cta", "product_fit"],
                direct_question_present=False,
                direct_question_answered_first=True,
                diagnostic_action="offer",
                diagnostic_allowed_now=True,
                waitlist_allowed_now=False,
                template_ids=["opening.site_cta"],
            ),
            diagnostic=DiagnosticOutput(
                status="offered",
                facts_used=[],
                unknowns=["main_pain", "operation_context"],
                confidence="low",
                next_question="O que voce acha?",
            ),
            confidence="high",
        )
    if cta_kind == "diagnostic_cta":
        draft = LLMStructuredDraft(
            current_agent=DIAGNOSTIC_AGENT,
            decision=RuntimeDecision(
                route="diagnostic",
                opening_type="diagnostic_cta_opening",
                detected_intents=["diagnostic_request"],
                direct_question_present=False,
                direct_question_answered_first=True,
                diagnostic_action="ask_next",
                diagnostic_allowed_now=True,
                waitlist_allowed_now=False,
                template_ids=["diagnostic.ask_active_students"],
            ),
            diagnostic=DiagnosticOutput(
                status="in_progress",
                facts_used=[],
                unknowns=["active_students_or_size"],
                confidence="high",
                next_question="Hoje seu studio tem mais ou menos quantos alunos ativos?",
            ),
            confidence="high",
        )
        draft.decision.template_variables = {
            "diagnostic.ask_active_students": {
                "answer_feedback": "Claro, faço sim. Pra te devolver algo útil, vou entender rapidinho como está a rotina do studio hoje."
            }
        }
        return draft
    if cta_kind == "demo_cta":
        return LLMStructuredDraft(
            current_agent=PRODUCT_AGENT,
            decision=RuntimeDecision(
                route="product",
                opening_type="direct_question_opening",
                detected_intents=["product", "demo_request"],
                direct_question_present=True,
                direct_question_answered_first=True,
                diagnostic_action="none",
                diagnostic_allowed_now=False,
                waitlist_allowed_now=False,
                demo_status="offered",
                demo_next_step="ask_demo_reaction",
                template_ids=["product.demo_direct"],
            ),
            confidence="high",
        )
    if cta_kind == "plan_compare_cta":
        return LLMStructuredDraft(
            current_agent=PRODUCT_AGENT,
            decision=RuntimeDecision(
                route="product",
                opening_type="direct_question_opening",
                detected_intents=["product", "plan_fit"],
                direct_question_present=True,
                direct_question_answered_first=True,
                diagnostic_action="offer",
                diagnostic_allowed_now=True,
                waitlist_allowed_now=False,
                template_ids=["product.plan_fit_with_diagnostic"],
            ),
            diagnostic=DiagnosticOutput(status="offered", confidence="medium"),
            confidence="high",
        )
    return LLMStructuredDraft(
        current_agent=WAITLIST_AGENT,
        decision=RuntimeDecision(
            route="waitlist",
            opening_type="direct_question_opening",
            detected_intents=["waitlist_intent", "checkout_intent"],
            direct_question_present=True,
            direct_question_answered_first=True,
            diagnostic_action="none",
            diagnostic_allowed_now=False,
            waitlist_allowed_now=True,
            template_ids=["waitlist.offer_after_contract_intent"],
        ),
        waitlist_action=WaitlistAction(status="offered", reason="standard_subscribe_cta", missing_fields=[]),
        confidence="high",
    )


async def _run_zero_cost_template_turn(
    request: AgentRunRequest,
    *,
    memory_store: InMemoryMemoryStore,
    previous_state: RuntimeState | None,
    run_id: str,
    trace_id: str,
) -> AgentRunResponse:
    source = get_product_knowledge_source()
    route = _zero_cost_template_route(request, previous_state) or "entry"
    current_agent = AGENT_BY_ROUTE[route]
    user_text = request.message.text or ""
    draft = LLMStructuredDraft(
        current_agent=current_agent,  # type: ignore[arg-type]
        decision=_decision_for_route(request, previous_state, route),
        handoff=HandoffOutput(status="requested", reason="lead_requested_human") if route == "handoff" else None,
        confidence="high",
    )
    draft = _apply_decision_contract(draft, request, previous_state)
    rendered_messages = render_template_plan(
        draft.decision.template_ids,
        channel=request.channel,
        variables_by_template=draft.decision.template_variables,
    )
    rendered_messages = _ensure_first_turn_greeting_in_messages(
        rendered_messages,
        request=request,
        previous_state=previous_state,
    )
    if not rendered_messages:
        rendered_messages = [AgentMessage(text=message, channel_hint=request.channel) for message in draft.messages[:3]]

    context = TaliyaCommercialContext(
        conversation_id=request.conversation.conversation_id,
        lead_id=request.conversation.lead_id,
        memory_store=memory_store,
        state=previous_state.model_dump() if previous_state else {},
    )
    tool_results = []
    if draft.diagnostic:
        saved = await save_diagnostic_record(
            context,
            idempotency_key=f"diagnostic:{request.message.idempotency_key}",
            diagnostic=draft.diagnostic.model_dump(),
        )
        tool_results.append({"name": "save_diagnostic_record", "status": "ok", "summary": str(saved.get("status", ""))})
    if draft.handoff:
        paused = await pause_for_human(
            context,
            idempotency_key=f"handoff:request:{request.message.idempotency_key}",
            reason=draft.handoff.reason or "lead_requested_human",
        )
        tool_results.append({"name": "pause_for_human", "status": "ok", "summary": str(paused.get("status", ""))})

    usage = usage_from_tokens(None, 0, 0)
    state = RuntimeState(
        conversation_id=request.conversation.conversation_id,
        agent_key=request.agent_key,
        current_agent_name=draft.current_agent,
        input_items=(previous_state.input_items if previous_state else [])
        + [{"role": "user", "content": user_text, "id": request.message.idempotency_key}],
        diagnostic=draft.diagnostic.model_dump() if draft.diagnostic else (previous_state.diagnostic if previous_state else None),
        waitlist=draft.waitlist_action.model_dump() if draft.waitlist_action else (previous_state.waitlist if previous_state else None),
        human_status="active" if draft.handoff else (previous_state.human_status if previous_state else "none"),
        human_reason=draft.handoff.reason if draft.handoff else (previous_state.human_reason if previous_state else None),
        product_source_version=source.version,
        cost_usd=previous_state.cost_usd if previous_state else 0,
        last_decision={**draft.decision.model_dump(mode="json"), "cost_path": "zero_cost_template"},
        last_route=draft.decision.route,
        last_opening_type=draft.decision.opening_type,
    )
    await memory_store.save_state(state)
    if route != "entry":
        await _record(
            memory_store,
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            type="handoff",
            agent=TRIAGE_AGENT,
            content=f"{TRIAGE_AGENT} -> {draft.current_agent}",
            metadata={"cost_path": "zero_cost_template"},
        )
    for result in tool_results:
        await _record(
            memory_store,
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            type="tool_call",
            agent=draft.current_agent,
            content=str(result["name"]),
            metadata=result,
        )
    for message in rendered_messages:
        await _record(
            memory_store,
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            type="message",
            agent=draft.current_agent,
            content=message.text,
        )

    output = AgentOutput(
        decision=draft.decision,
        messages=rendered_messages,
        lead_facts=draft.lead_facts,
        diagnostic=draft.diagnostic,
        waitlist_action=draft.waitlist_action,
        handoff=draft.handoff,
        sources=[SourceRef(type="product_knowledge", version=source.version, keys=_product_knowledge_keys_for_prompt(request, previous_state))],
        tool_results=tool_results,
        usage=usage,
        confidence=draft.confidence,
    )
    return AgentRunResponse(
        run_id=run_id,
        conversation_id=request.conversation.conversation_id,
        lead_id=request.conversation.lead_id,
        agent_key=request.agent_key,
        current_agent=draft.current_agent,
        status="human_paused" if draft.handoff else "succeeded",
        output=output,
        trace_id=trace_id,
    )


async def run_agent_turn(
    request: AgentRunRequest,
    *,
    memory_store: InMemoryMemoryStore,
    provider: str,
    model: str,
) -> AgentRunResponse:
    source = get_product_knowledge_source()
    run_id = f"run_{uuid4().hex}"
    trace_id = f"trace_{uuid4().hex}"
    user_text = request.message.text or ""
    current_agent_name = _route_agent_name(user_text)
    previous_state = await memory_store.load_state(request.conversation.conversation_id, request.agent_key)
    settings = get_settings()
    runtime_control = request.metadata.get("runtime_control") if isinstance(request.metadata, dict) else None
    if isinstance(runtime_control, dict):
        action = runtime_control.get("action")
        reason = str(runtime_control.get("reason") or action or "operator_control")
        context = TaliyaCommercialContext(
            conversation_id=request.conversation.conversation_id,
            lead_id=request.conversation.lead_id,
            memory_store=memory_store,
            state=previous_state.model_dump() if previous_state else {},
        )
        if action == "pause_human":
            result = await pause_for_human(
                context,
                idempotency_key=f"handoff:pause:{request.message.idempotency_key}",
                reason=reason,
            )
            output = AgentOutput(
                decision=_decision_for_route(request, previous_state, "handoff"),
                messages=[],
                handoff=HandoffOutput(status="active", reason=result.get("reason") or reason),
                safety_flags=["human_active", "operator_pause"],
                usage=usage_from_tokens(None, 0, 0),
                confidence="high",
            )
            state = RuntimeState(
                conversation_id=request.conversation.conversation_id,
                agent_key=request.agent_key,
                current_agent_name=HANDOFF_AGENT,
                input_items=(previous_state.input_items if previous_state else [])
                + [{"role": "system", "content": "operator paused automation", "id": request.message.idempotency_key}],
                human_status="active",
                human_reason=reason,
                product_source_version=source.version,
                cost_usd=previous_state.cost_usd if previous_state else 0,
            )
            await memory_store.save_state(state)
            await _record(
                memory_store,
                run_id=run_id,
                conversation_id=request.conversation.conversation_id,
                agent_key=request.agent_key,
                type="handoff",
                agent=HANDOFF_AGENT,
                content=f"operator -> {HANDOFF_AGENT}",
                metadata={"source_agent": "operator", "target_agent": HANDOFF_AGENT, "reason": reason},
            )
            return AgentRunResponse(
                run_id=run_id,
                conversation_id=request.conversation.conversation_id,
                lead_id=request.conversation.lead_id,
                agent_key=request.agent_key,
                current_agent=HANDOFF_AGENT,
                status="human_paused",
                output=output,
                trace_id=trace_id,
            )
        if action == "resume_human":
            await resume_from_human(
                context,
                idempotency_key=f"handoff:resume:{request.message.idempotency_key}",
            )
            output = AgentOutput(
                decision=_decision_for_route(request, previous_state, "handoff"),
                messages=[],
                handoff=HandoffOutput(status="resumed", reason=reason),
                safety_flags=["operator_resume"],
                usage=usage_from_tokens(None, 0, 0),
                confidence="high",
            )
            state = RuntimeState(
                conversation_id=request.conversation.conversation_id,
                agent_key=request.agent_key,
                current_agent_name=previous_state.current_agent_name
                if previous_state and previous_state.current_agent_name != HANDOFF_AGENT
                else TRIAGE_AGENT,
                input_items=(previous_state.input_items if previous_state else [])
                + [{"role": "system", "content": "operator resumed automation", "id": request.message.idempotency_key}],
                human_status="resumed",
                human_reason=None,
                product_source_version=source.version,
                cost_usd=previous_state.cost_usd if previous_state else 0,
            )
            await memory_store.save_state(state)
            await _record(
                memory_store,
                run_id=run_id,
                conversation_id=request.conversation.conversation_id,
                agent_key=request.agent_key,
                type="handoff",
                agent=HANDOFF_AGENT,
                content=f"{HANDOFF_AGENT} -> runtime_resumed",
                metadata={"source_agent": HANDOFF_AGENT, "target_agent": state.current_agent_name, "reason": reason},
            )
            return AgentRunResponse(
                run_id=run_id,
                conversation_id=request.conversation.conversation_id,
                lead_id=request.conversation.lead_id,
                agent_key=request.agent_key,
                current_agent=state.current_agent_name,
                status="succeeded",
                output=output,
                trace_id=trace_id,
            )

    if previous_state and previous_state.human_status == "active":
        output = AgentOutput(
            decision=_decision_for_route(request, previous_state, "handoff"),
            messages=[],
            handoff=HandoffOutput(status="active", reason=previous_state.human_reason or "human_active"),
            safety_flags=["human_active"],
            usage=usage_from_tokens(None, 0, 0),
            confidence="high",
        )
        state = previous_state.model_copy(deep=True)
        state.input_items.append(
            {"role": "user", "content": user_text, "id": request.message.idempotency_key}
        )
        state.current_agent_name = HANDOFF_AGENT
        state.product_source_version = source.version
        await memory_store.save_state(state)
        await _record(
            memory_store,
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            type="guardrail",
            agent=HANDOFF_AGENT,
            content="suppressed automated reply because human handoff is active",
            metadata={"reason": previous_state.human_reason or "human_active"},
        )
        return AgentRunResponse(
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            lead_id=request.conversation.lead_id,
            agent_key=request.agent_key,
            current_agent=HANDOFF_AGENT,
            status="human_paused",
            output=output,
            trace_id=trace_id,
        )
    if previous_state and previous_state.cost_usd >= settings.hard_cost_cap_usd:
        output = AgentOutput(
            decision=_decision_for_route(request, previous_state, "handoff"),
            messages=[],
            handoff=HandoffOutput(status="active", reason="cost_cap_reached"),
            safety_flags=["cost_cap_reached", "human_follow_up_required"],
            usage=usage_from_tokens(None, 0, 0),
            confidence="high",
        )
        state = previous_state.model_copy(deep=True)
        state.input_items.append(
            {"role": "user", "content": user_text, "id": request.message.idempotency_key}
        )
        state.current_agent_name = HANDOFF_AGENT
        state.human_status = "active"
        state.human_reason = "cost_cap_reached"
        await memory_store.save_state(state)
        await _record(
            memory_store,
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            type="guardrail",
            agent="cost_guardrail",
            content="automatic reply suppressed because hard cost cap was reached",
            metadata={"cost_usd": previous_state.cost_usd, "hard_cost_cap_usd": settings.hard_cost_cap_usd},
        )
        return AgentRunResponse(
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            lead_id=request.conversation.lead_id,
            agent_key=request.agent_key,
            current_agent=HANDOFF_AGENT,
            status="cost_capped",
            output=output,
            trace_id=trace_id,
        )
    if provider != "mock" and request.metadata.get("batched_during_assistant_delivery"):
        selected_model = _select_llm_model_for_turn(request, previous_state, model)
        suppressed_response = await _run_interleaved_delivery_suppression_turn(
            request,
            memory_store=memory_store,
            model=selected_model,
            previous_state=previous_state,
            run_id=run_id,
            trace_id=trace_id,
        )
        if suppressed_response is not None:
            return suppressed_response
    standard_cta_kind = _standard_cta_kind(request, previous_state)
    if provider != "mock" and standard_cta_kind:
        return await _run_standard_cta_fast_turn(
            request,
            memory_store=memory_store,
            previous_state=previous_state,
            run_id=run_id,
            trace_id=trace_id,
            cta_kind=standard_cta_kind,
        )
    if provider != "mock" and _should_use_contextual_widget_fast_path(request, previous_state):
        return await _run_contextual_widget_fast_turn(
            request,
            memory_store=memory_store,
            model=model,
            previous_state=previous_state,
            run_id=run_id,
            trace_id=trace_id,
        )
    if provider != "mock" and _should_use_zero_cost_template_path(request, previous_state):
        return await _run_zero_cost_template_turn(
            request,
            memory_store=memory_store,
            previous_state=previous_state,
            run_id=run_id,
            trace_id=trace_id,
        )
    if provider != "mock" and _should_use_simple_opening_fast_path(request, previous_state):
        selected_model = _select_llm_model_for_turn(request, previous_state, model)
        fast_response = await _run_simple_opening_fast_turn(
            request,
            memory_store=memory_store,
            model=selected_model,
            previous_state=previous_state,
            run_id=run_id,
            trace_id=trace_id,
        )
        if fast_response is not None:
            return fast_response
    if provider != "mock":
        selected_model = _select_llm_model_for_turn(request, previous_state, model)
        return await _run_llm_first_turn(
            request,
            memory_store=memory_store,
            model=selected_model,
            previous_state=previous_state,
            run_id=run_id,
            trace_id=trace_id,
        )
    if previous_state and previous_state.waitlist and _is_waitlist_acceptance(user_text):
        current_agent_name = WAITLIST_AGENT

    if current_agent_name == HANDOFF_AGENT:
        context = TaliyaCommercialContext(
            conversation_id=request.conversation.conversation_id,
            lead_id=request.conversation.lead_id,
            memory_store=memory_store,
            state=previous_state.model_dump() if previous_state else {},
        )
        await pause_for_human(
            context,
            idempotency_key=f"handoff:request:{request.message.idempotency_key}",
            reason="lead_requested_human",
        )
        decision = _decision_for_route(request, previous_state, "handoff")
        output = AgentOutput(
            decision=decision,
            messages=[
                AgentMessage(
                    text="Tudo bem. Vou pausar por aqui e deixar a conversa para uma pessoa da Taliya continuar.",
                    channel_hint=request.channel,
                )
            ],
            handoff=HandoffOutput(status="requested", reason="lead_requested_human"),
            safety_flags=["human_requested"],
            usage=usage_from_tokens(None, 0, 0),
            confidence="high",
        )
        state = RuntimeState(
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            current_agent_name=HANDOFF_AGENT,
            input_items=(previous_state.input_items if previous_state else [])
            + [{"role": "user", "content": user_text, "id": request.message.idempotency_key}],
            human_status="active",
            human_reason="lead_requested_human",
            demo=previous_state.demo if previous_state else None,
            last_decision=decision.model_dump(mode="json"),
            last_route=decision.route,
            last_opening_type=decision.opening_type,
            product_source_version=source.version,
        )
        await memory_store.save_state(state)
        await _record(
            memory_store,
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            type="handoff",
            agent=TRIAGE_AGENT,
            content=f"{TRIAGE_AGENT} -> {HANDOFF_AGENT}",
            metadata={"source_agent": TRIAGE_AGENT, "target_agent": HANDOFF_AGENT},
        )
        await _record(
            memory_store,
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            type="message",
            agent=HANDOFF_AGENT,
            content=output.messages[0].text,
        )
        return AgentRunResponse(
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            lead_id=request.conversation.lead_id,
            agent_key=request.agent_key,
            current_agent=HANDOFF_AGENT,
            status="human_paused",
            output=output,
            trace_id=trace_id,
        )

    if current_agent_name == DIAGNOSTIC_AGENT:
        message, lead_facts, diagnostic = _build_diagnostic_output(
            user_text,
            request.message.idempotency_key,
            request.channel,
        )
        context = TaliyaCommercialContext(
            conversation_id=request.conversation.conversation_id,
            lead_id=request.conversation.lead_id,
            memory_store=memory_store,
        )
        if lead_facts:
            await save_lead_facts(
                context,
                idempotency_key=f"facts:{request.message.idempotency_key}",
                facts=[fact.model_dump() for fact in lead_facts],
            )
        await save_diagnostic_record(
            context,
            idempotency_key=f"diagnostic:{request.message.idempotency_key}",
            diagnostic=diagnostic.model_dump(),
        )
        decision = _decision_for_route(request, previous_state, "diagnostic", diagnostic=diagnostic)
        output = AgentOutput(
            decision=decision,
            messages=[message],
            lead_facts=lead_facts,
            diagnostic=diagnostic,
            sources=[
                SourceRef(
                    type="product_knowledge",
                    version=source.version,
                    keys=["plans", "prices", "links"],
                )
            ],
            usage=usage_from_tokens(model if provider != "mock" else "gpt-5.2", 950, 180),
            confidence=diagnostic.confidence,
        )
        usage_record = build_usage_record(
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            operation="runner",
            usage=output.usage,
            budget_before=previous_state.cost_usd if previous_state else 0,
            review_cost_usd=settings.review_cost_usd,
            hard_cost_cap_usd=settings.hard_cost_cap_usd,
        )
        state = RuntimeState(
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            current_agent_name=current_agent_name,
            input_items=(previous_state.input_items if previous_state else [])
            + [{"role": "user", "content": user_text, "id": request.message.idempotency_key}],
            lead_facts=[fact.model_dump() for fact in lead_facts],
            diagnostic=diagnostic.model_dump(),
            demo=previous_state.demo if previous_state else None,
            last_decision=decision.model_dump(mode="json"),
            last_route=decision.route,
            last_opening_type=decision.opening_type,
            asked_questions=[diagnostic.next_question] if diagnostic.next_question else [],
            product_source_version=source.version,
            cost_usd=usage_record.budget_after,
        )
        await memory_store.save_state(state)
        await _record(
            memory_store,
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            type="handoff",
            agent=TRIAGE_AGENT,
            content=f"{TRIAGE_AGENT} -> {current_agent_name}",
            metadata={"source_agent": TRIAGE_AGENT, "target_agent": current_agent_name},
        )
        await _record(
            memory_store,
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            type="tool_call",
            agent=current_agent_name,
            content="save_lead_facts",
            metadata={"fact_count": len(lead_facts)},
        )
        await _record(
            memory_store,
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            type="tool_call",
            agent=current_agent_name,
            content="save_diagnostic_record",
            metadata={"status": diagnostic.status},
        )
        await _record(
            memory_store,
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            type="message",
            agent=current_agent_name,
            content=message.text,
        )
        await _record(
            memory_store,
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            type="usage",
            agent=current_agent_name,
            content=output.usage.model or "",
            metadata=usage_record.__dict__,
        )
        return AgentRunResponse(
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            lead_id=request.conversation.lead_id,
            agent_key=request.agent_key,
            current_agent=current_agent_name,
            status="succeeded",
            output=output,
            trace_id=trace_id,
        )

    if current_agent_name == WAITLIST_AGENT:
        context = TaliyaCommercialContext(
            conversation_id=request.conversation.conversation_id,
            lead_id=request.conversation.lead_id,
            memory_store=memory_store,
        )
        prior_waitlist = previous_state.waitlist if previous_state else None
        joining = bool(prior_waitlist) and _is_waitlist_acceptance(user_text)
        has_actionable_details = joining and _has_waitlist_actionable_details(request)
        waitlist_status = "joined" if has_actionable_details else "pending_details" if joining else "offered"
        waitlist_reason = "lead_accepted_waitlist" if has_actionable_details else "missing_waitlist_details" if joining else "lead_showed_buying_interest"
        missing_fields = [] if has_actionable_details else ["studio_name", "city_state"]
        waitlist_result = await mark_waitlist(
            context,
            idempotency_key=f"waitlist:{request.message.idempotency_key}",
            status=waitlist_status,
            reason=waitlist_reason,
            missing_fields=missing_fields,
        )
        if has_actionable_details:
            text = "Perfeito, deixei seu studio na lista de espera da Taliya. Quando abrir uma proxima janela, a equipe chama com o contexto dessa conversa."
        elif joining:
            text = "Combinado. Para deixar a lista de espera acionavel, ainda preciso do nome do studio e cidade/estado. Pode me mandar nessa mesma mensagem?"
        else:
            text = (
                "Hoje a Taliya esta trabalhando com um numero pequeno de studios e nao libera assinatura direta por aqui. "
                "Se fizer sentido, posso colocar seu studio na lista de espera e a equipe chama quando abrir uma proxima janela."
            )
        decision = _decision_for_route(request, previous_state, "waitlist", waitlist_allowed=bool(missing_fields))
        output = AgentOutput(
            decision=decision,
            messages=[AgentMessage(text=text, channel_hint=request.channel)],
            waitlist_action=WaitlistAction(
                status=waitlist_status,  # type: ignore[arg-type]
                reason=waitlist_reason,
                missing_fields=missing_fields,
            ),
            sources=[
                SourceRef(
                    type="product_knowledge",
                    version=source.version,
                    keys=["waitlist_status", "checkout_status", "availability"],
                )
            ],
            tool_results=[
                {
                    "name": "mark_waitlist",
                    "status": "ok",
                    "idempotency_key": f"waitlist:{request.message.idempotency_key}",
                    "summary": waitlist_result.get("status"),
                }
            ],
            usage=usage_from_tokens(model if provider != "mock" else "gpt-5.2", 700, 120),
            confidence="high",
        )
        usage_record = build_usage_record(
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            operation="runner",
            usage=output.usage,
            budget_before=previous_state.cost_usd if previous_state else 0,
            review_cost_usd=settings.review_cost_usd,
            hard_cost_cap_usd=settings.hard_cost_cap_usd,
        )
        state = RuntimeState(
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            current_agent_name=current_agent_name,
            input_items=(previous_state.input_items if previous_state else [])
            + [{"role": "user", "content": user_text, "id": request.message.idempotency_key}],
            waitlist=waitlist_result,
            demo=previous_state.demo if previous_state else None,
            last_decision=decision.model_dump(mode="json"),
            last_route=decision.route,
            last_opening_type=decision.opening_type,
            product_source_version=source.version,
            cost_usd=usage_record.budget_after,
        )
        await memory_store.save_state(state)
        await _record(
            memory_store,
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            type="handoff",
            agent=TRIAGE_AGENT,
            content=f"{TRIAGE_AGENT} -> {current_agent_name}",
            metadata={"source_agent": TRIAGE_AGENT, "target_agent": current_agent_name},
        )
        await _record(
            memory_store,
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            type="tool_call",
            agent=current_agent_name,
            content="mark_waitlist",
            metadata=waitlist_result,
        )
        await _record(
            memory_store,
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            type="message",
            agent=current_agent_name,
            content=text,
        )
        await _record(
            memory_store,
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            type="usage",
            agent=current_agent_name,
            content=output.usage.model or "",
            metadata=usage_record.__dict__,
        )
        return AgentRunResponse(
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            lead_id=request.conversation.lead_id,
            agent_key=request.agent_key,
            current_agent=current_agent_name,
            status="succeeded",
            output=output,
            trace_id=trace_id,
        )

    output_decision = _decision_for_route(
        request,
        previous_state,
        "product" if current_agent_name == PRODUCT_AGENT else "entry",
    )
    mock_draft = LLMStructuredDraft(
        current_agent=current_agent_name,  # type: ignore[arg-type]
        decision=output_decision,
        source_keys=["plans", "prices", "links"],
    )
    mock_draft = _apply_decision_contract(mock_draft, request, previous_state)
    rendered_messages = render_template_plan(
        mock_draft.decision.template_ids,
        channel=request.channel,
        variables_by_template=mock_draft.decision.template_variables,
    )
    rendered_messages = _ensure_first_turn_greeting_in_messages(
        rendered_messages,
        request=request,
        previous_state=previous_state,
    )
    output = AgentOutput(
        decision=mock_draft.decision,
        messages=rendered_messages or [_mock_message_for(request)],
        sources=[
            SourceRef(
                type="product_knowledge",
                version=source.version,
                keys=["plans", "prices", "links"],
            )
        ],
        usage=usage_from_tokens(model if provider != "mock" else "gpt-5.2", 900, 150),
        confidence="medium",
    )
    usage_record = build_usage_record(
        run_id=run_id,
        conversation_id=request.conversation.conversation_id,
        agent_key=request.agent_key,
        operation="runner",
        usage=output.usage,
        budget_before=previous_state.cost_usd if previous_state else 0,
        review_cost_usd=settings.review_cost_usd,
        hard_cost_cap_usd=settings.hard_cost_cap_usd,
    )
    state = RuntimeState(
        conversation_id=request.conversation.conversation_id,
        agent_key=request.agent_key,
        current_agent_name=current_agent_name,
        input_items=(previous_state.input_items if previous_state else [])
        + [{"role": "user", "content": user_text, "id": request.message.idempotency_key}],
        product_source_version=source.version,
        demo={"status": mock_draft.decision.demo_status, "next_step": mock_draft.decision.demo_next_step},
        last_decision=mock_draft.decision.model_dump(mode="json"),
        last_route=mock_draft.decision.route,
        last_opening_type=mock_draft.decision.opening_type,
        cost_usd=usage_record.budget_after,
    )
    await memory_store.save_state(state)
    if current_agent_name != ENTRY_AGENT:
        await _record(
            memory_store,
            run_id=run_id,
            conversation_id=request.conversation.conversation_id,
            agent_key=request.agent_key,
            type="handoff",
            agent=TRIAGE_AGENT,
            content=f"{TRIAGE_AGENT} -> {current_agent_name}",
            metadata={"source_agent": TRIAGE_AGENT, "target_agent": current_agent_name},
        )
    await _record(
        memory_store,
        run_id=run_id,
        conversation_id=request.conversation.conversation_id,
        agent_key=request.agent_key,
        type="tool_call",
        agent=current_agent_name,
        content="get_product_knowledge",
        metadata={"source_version": source.version},
    )
    await _record(
        memory_store,
        run_id=run_id,
        conversation_id=request.conversation.conversation_id,
        agent_key=request.agent_key,
        type="message",
        agent=current_agent_name,
        content=output.messages[0].text,
    )
    await _record(
        memory_store,
        run_id=run_id,
        conversation_id=request.conversation.conversation_id,
        agent_key=request.agent_key,
        type="usage",
        agent=current_agent_name,
        content=output.usage.model or "",
        metadata=usage_record.__dict__,
    )
    return AgentRunResponse(
        run_id=run_id,
        conversation_id=request.conversation.conversation_id,
        lead_id=request.conversation.lead_id,
        agent_key=request.agent_key,
        current_agent=state.current_agent_name,
        status="succeeded",
        output=output,
        trace_id=trace_id,
    )
