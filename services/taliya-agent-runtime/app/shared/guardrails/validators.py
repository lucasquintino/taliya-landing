from __future__ import annotations

from copy import deepcopy
import re
from typing import Any

from app.runtime.schemas import AgentOutput
from app.domains.taliya_commercial.behavior_policy import BANNED_VOICE_PHRASES
from app.domains.taliya_commercial.diagnostic_ledger import ledger_is_complete
from app.domains.taliya_commercial.templates import get_template, template_allowed_in_state


class OutputValidationError(Exception):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(message)


SENSITIVE_KEY_PARTS = (
    "secret",
    "signature",
    "authorization",
    "cookie",
    "system_prompt",
    "prompt",
    "api_key",
)


def redact_trace_payload(payload: Any) -> Any:
    if isinstance(payload, dict):
        redacted: dict[str, Any] = {}
        for key, value in payload.items():
            lowered = str(key).lower()
            if any(part in lowered for part in SENSITIVE_KEY_PARTS):
                redacted[key] = "[REDACTED]"
            else:
                redacted[key] = redact_trace_payload(value)
        return redacted
    if isinstance(payload, list):
        return [redact_trace_payload(item) for item in payload]
    if isinstance(payload, str):
        if payload.startswith("sk-"):
            return "[REDACTED]"
        return payload
    return deepcopy(payload)


def _has_product_source(output: AgentOutput) -> bool:
    return any(source.type == "product_knowledge" and source.version for source in output.sources)


def _mentions_product_claim(text: str) -> bool:
    lowered = text.lower()
    return any(
        token in lowered
        for token in (
            "r$",
            "plano",
            "preco",
            "preço",
            "demonstra",
            "lista de espera",
            "checkout",
            "garantia",
            "cancel",
            "/pilates",
            "whatsapp business",
            "taliya ajuda",
            "agentes",
            "integra",
            "lgpd",
            "privacidade",
        )
    )


def _is_product_followup_template(template_id: str | None) -> bool:
    return template_id in {
        "product.how_it_works_direct",
        "product.comparison_current_tool",
        "product.integration_scope_direct",
        "product.whatsapp_business_requirement",
        "product.security_data_direct",
        "product.out_of_profile_redirect",
        "product.price_objection_value",
        "post_diagnostic.thinking",
        "post_diagnostic.priority_update",
    }


def _uses_technical_language_for_lay_lead(text: str) -> bool:
    lowered = text.lower()
    blocked_phrases = (
        "pipeline",
        "lead scoring",
        "arquitetura",
    )
    blocked_terms = ("webhook", "api", "runtime", "sdk", "stack")
    return any(phrase in lowered for phrase in blocked_phrases) or any(
        re.search(rf"\b{re.escape(term)}\b", lowered) for term in blocked_terms
    )


def _asks_for_whatsapp_phone(text: str) -> bool:
    lowered = text.lower()
    return bool(
        re.search(r"(qual|me passa|manda|informe|envia).{0,30}(whatsapp|telefone|celular)", lowered)
        or re.search(r"(whatsapp|telefone|celular).{0,30}(para continuar|podemos usar)", lowered)
    )


def _mentions_checkout_unsafely(text: str) -> bool:
    lowered = text.lower()
    if "checkout" not in lowered:
        return False
    if re.search(r"https?://\S*(checkout|pagamento|payment)", lowered):
        return True
    if re.search(r"\bcheckout\.[^\s]+", lowered):
        return True
    safe_negation = any(
        token in lowered
        for token in (
            "sem checkout",
            "nao tem checkout",
            "não tem checkout",
            "checkout indispon",
            "checkout nao",
            "checkout não",
            "nao libera",
            "não libera",
            "nao ha",
            "não há",
            "nao existe",
            "não existe",
            "checkout unavailable",
        )
    )
    unsafe_claim = any(
        token in lowered
        for token in (
            "link de checkout",
            "checkout para assinar",
            "checkout para fechar",
            "fechar pelo checkout",
            "assinar pelo checkout",
            "pagamento pelo checkout",
            "checkout disponivel",
            "checkout disponível",
        )
    )
    return unsafe_claim and not safe_negation


def _leaks_internal_agent_text(text: str) -> bool:
    lowered = text.lower()
    blocked_phrases = (
        "lead said",
        "lead says",
        "lead reports",
        "lead informou",
        "lead disse",
        "user said",
        "user says",
        "perfil confiável",
        "perfil confiavel",
        "reliable profile",
        "profile first name",
        "profile name",
        "profile_name",
        "used_reliable_name",
        "ignored_unreliable_name",
        "profile_name_usage",
        "profile_name_assessment",
        "detected intent",
        "template_id",
        "template id",
        "metadata",
        "route=",
        "current_state",
        "next_state",
    )
    return any(phrase in lowered for phrase in blocked_phrases)


def _mentions_diagnostic(text: str) -> bool:
    lowered = text.lower()
    return "diagnostico" in lowered or "diagnostico gratuito" in lowered or "diagnóstico" in lowered


def _mentions_waitlist(text: str) -> bool:
    lowered = text.lower()
    return "lista de espera" in lowered or "proxima janela" in lowered or "próxima janela" in lowered


def _asks_for_name_or_contact(text: str) -> bool:
    lowered = text.lower()
    return bool(
        re.search(r"(qual|me passa|manda|informe|envia).{0,35}(nome|contato|email|e-mail)", lowered)
        or "com quem eu falo" in lowered
    )


def _asks_for_waitlist_details(text: str) -> bool:
    lowered = text.lower()
    return bool(
        "nome do studio" in lowered
        or "city/state" in lowered
        or re.search(r"\bcidade\b", lowered)
        or re.search(r"\bestado\b", lowered)
    )


def validate_structured_output(output: AgentOutput, *, channel: str | None = None) -> None:
    decision = output.decision
    for template_id in decision.template_ids:
        try:
            template = get_template(template_id)
        except ValueError as exc:
            raise OutputValidationError(
                "unknown_template_id",
                f"Unknown template id: {template_id}",
            ) from exc
        if not template_allowed_in_state(template_id, decision.current_state):
            raise OutputValidationError(
                "template_not_allowed_in_state",
                f"Template {template_id} is not allowed in {decision.current_state}.",
            )
        if channel and template.channel_support not in {"both", channel}:
            raise OutputValidationError(
                "template_not_allowed_for_channel",
                f"Template {template_id} is not allowed for {channel}.",
            )
    for message in output.messages:
        if decision.template_ids and message.template_id not in decision.template_ids:
            raise OutputValidationError(
                "message_template_mismatch",
                "Rendered messages must come from selected template ids.",
            )

    if output.handoff and output.handoff.status == "active" and output.messages:
        raise OutputValidationError(
            "human_active_with_messages",
            "Human-active handoff cannot produce automated messages.",
        )

    if output.diagnostic and output.diagnostic.status == "completed":
        if not output.diagnostic.evidence:
            raise OutputValidationError(
                "diagnostic_without_evidence",
                "Completed diagnostics require concrete evidence.",
            )
        if not ledger_is_complete(output.diagnostic.ledger):
            raise OutputValidationError(
                "diagnostic_ledger_incomplete",
                "Completed diagnostics require all mandatory ledger items.",
            )
        if not output.diagnostic.likely_cause or not output.diagnostic.first_recommended_step:
            raise OutputValidationError(
                "diagnostic_without_recommendation",
                "Completed diagnostics require likely cause and first recommended step.",
            )

    if decision.direct_question_present and not decision.direct_question_answered_first:
        raise OutputValidationError(
            "direct_question_not_answered_first",
            "Direct questions must be answered before steering.",
        )

    if (
        not decision.diagnostic_allowed_now
        and output.diagnostic
        and output.diagnostic.status in {"offered", "in_progress", "completed"}
        and not (
            decision.route == "handoff"
            and decision.diagnostic_action == "none"
            and output.diagnostic.status == "completed"
        )
    ):
        raise OutputValidationError(
            "diagnostic_offered_too_early",
            "Diagnostic cannot be offered or completed in this turn.",
        )

    if (
        not decision.waitlist_allowed_now
        and output.waitlist_action
        and output.waitlist_action.status in {"offered", "pending_details", "joined"}
    ):
        raise OutputValidationError(
            "waitlist_offered_too_early",
            "Waitlist requires real interest.",
        )

    product_source_required = any(
        message.requires_product_source or _mentions_product_claim(message.text)
        for message in output.messages
    )
    if product_source_required and not _has_product_source(output):
        raise OutputValidationError(
            "missing_product_source",
            "Commercial product claims require product knowledge source.",
        )

    for message in output.messages:
        lowered = message.text.lower()
        if any(phrase in lowered for phrase in BANNED_VOICE_PHRASES):
            raise OutputValidationError(
                "banned_voice_phrase",
                "Message uses a banned voice phrase.",
            )
        if _leaks_internal_agent_text(message.text):
            raise OutputValidationError(
                "internal_text_leak",
                "Message leaked internal agent text.",
            )
        if _is_product_followup_template(message.template_id) and _uses_technical_language_for_lay_lead(message.text):
            raise OutputValidationError(
                "technical_language_for_lay_lead",
                "Product follow-up messages must use Pilates studio owner language.",
            )
        if _is_product_followup_template(message.template_id) and "crm" in lowered and message.template_id != "product.crm_direct":
            raise OutputValidationError(
                "crm_for_lay_lead",
                "Lay product follow-up messages must not use CRM unless the lead asked about CRM.",
            )
        if decision.opening_type == "cold_greeting_only":
            if _mentions_diagnostic(message.text):
                raise OutputValidationError(
                    "cold_greeting_diagnostic",
                    "Cold greetings must not offer diagnostic.",
                )
            if _mentions_waitlist(message.text):
                raise OutputValidationError(
                    "cold_greeting_waitlist",
                    "Cold greetings must not offer waitlist.",
                )
            if _asks_for_name_or_contact(message.text):
                raise OutputValidationError(
                    "cold_greeting_contact_capture",
                    "Cold greetings must not ask for name or contact.",
                )
            if _mentions_product_claim(message.text):
                raise OutputValidationError(
                    "cold_greeting_product_pitch",
                    "Cold greetings must not list product or plan details.",
                )
        if not decision.waitlist_allowed_now and _asks_for_waitlist_details(message.text):
            raise OutputValidationError(
                "early_waitlist_detail_capture",
                "Waitlist details can only be requested after waitlist eligibility.",
            )
        if channel == "whatsapp" and _asks_for_whatsapp_phone(message.text):
            raise OutputValidationError(
                "whatsapp_phone_request",
                "WhatsApp channel must not ask the lead for a phone number.",
            )
        if _mentions_checkout_unsafely(message.text):
            raise OutputValidationError(
                "invented_checkout",
                "Checkout links are unavailable in product knowledge.",
            )
        if "pelo que voce contou" in lowered and not output.lead_facts:
            diagnostic_evidence = output.diagnostic.evidence if output.diagnostic else []
            if not diagnostic_evidence:
                raise OutputValidationError(
                    "unsupported_evidence_phrase",
                    "Evidence framing requires actual lead evidence.",
                )
