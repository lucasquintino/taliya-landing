from __future__ import annotations

import unicodedata
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from app.core.taliya_commercial.product_knowledge import (
    DEFAULT_OFFICIAL_PRODUCT_KNOWLEDGE_KEYS,
    DEFAULT_SPEC006_CONTRACT_KEYS,
)
from app.runtime.schemas import AgentRunRequest
from app.shared.memory.postgres import RuntimeState

RUNTIME_CORE_PRODUCT_KNOWLEDGE_KEYS: tuple[str, ...] = (
    "plans",
    "prices",
    "plan_comparison",
    "links",
    "demo_status",
    "waitlist_status",
    "checkout_status",
    "availability",
    "how_it_works",
    "routine_areas",
    "whatsapp_scope",
    "integration_scope",
    "out_of_profile",
    "unsupported_claims",
)

RUNTIME_CORE_SPEC006_CONTRACT_KEYS: tuple[str, ...] = (
    "product_positioning",
    "plan_entitlements",
)

_DEFAULT_RUNTIME_TRANSCRIPT_ITEMS = 6
_DIAGNOSTIC_RUNTIME_TRANSCRIPT_ITEMS = 5

_COMPARISON_HINTS = (
    "planilha",
    "excel",
    "sistema atual",
    "meu sistema",
    "sistema que uso",
    "crm",
    "software",
    "gestao",
    "comparar",
    "comparacao",
    "substitui",
)

_SECURITY_HINTS = (
    "lgpd",
    "seguranca",
    "seguro",
    "dados",
    "privacidade",
    "senha",
    "permissao",
    "acesso aos dados",
    "vazamento",
)

_COMMERCIAL_POLICY_HINTS = (
    "cancelar",
    "cancelamento",
    "garantia",
    "reembolso",
    "devolucao",
    "fidelidade",
    "contrato",
)

_ONBOARDING_HINTS = (
    "onboarding",
    "setup",
    "configurar",
    "configuracao",
    "implantacao",
    "implementar",
    "comecar",
    "começar",
    "quando libera",
    "quando consigo",
    "depois de assinar",
)

_ACCESS_HINTS = (
    "acesso",
    "login",
    "painel",
    "tela",
    "app",
    "assinatura",
    "checkout",
    "pagamento",
)

_OPERATING_MODE_HINTS = (
    "automatico",
    "automático",
    "manual",
    "supervisionar",
    "modo",
    "pausar",
    "assumir atendimento",
)

_OUT_OF_PROFILE_HINTS = (
    "academia",
    "barbearia",
    "clinica",
    "clínica",
    "consultorio",
    "consultório",
    "fisio",
    "nutri",
    "nao sou pilates",
    "não sou pilates",
    "outro nicho",
)


@dataclass(frozen=True)
class RuntimeContextProfile:
    product_knowledge_keys: tuple[str, ...]
    spec006_contract_keys: tuple[str, ...]
    max_recent_transcript_items: int


def build_runtime_context_profile(
    *,
    request: AgentRunRequest,
    state: RuntimeState | None = None,
) -> RuntimeContextProfile:
    """Select source material for the prompt without deciding conversation behavior."""

    source_text = _normalized_source_text(request=request, state=state)
    product_keys: list[str] = list(RUNTIME_CORE_PRODUCT_KNOWLEDGE_KEYS)
    spec006_keys: list[str] = list(RUNTIME_CORE_SPEC006_CONTRACT_KEYS)

    if _contains_any(source_text, _COMPARISON_HINTS):
        product_keys.extend(
            ["comparison_spreadsheet", "comparison_management_system"]
        )
    if _contains_any(source_text, _SECURITY_HINTS):
        product_keys.extend(["privacy_or_data_notes", "security_and_data"])
    if _contains_any(source_text, _COMMERCIAL_POLICY_HINTS):
        product_keys.append("cancellation_or_guarantee_policy")
    if _contains_any(source_text, _ONBOARDING_HINTS):
        product_keys.append("availability_and_onboarding")
        spec006_keys.append("setup_scope")
    if _contains_any(source_text, _ACCESS_HINTS):
        spec006_keys.extend(["access_subscription", "navigation_routes"])
    if _contains_any(source_text, _OPERATING_MODE_HINTS):
        spec006_keys.append("operating_modes")
    if _contains_any(source_text, _OUT_OF_PROFILE_HINTS):
        product_keys.append("out_of_profile")

    return RuntimeContextProfile(
        product_knowledge_keys=tuple(
            _dedupe_known(product_keys, DEFAULT_OFFICIAL_PRODUCT_KNOWLEDGE_KEYS)
        ),
        spec006_contract_keys=tuple(
            _dedupe_known(spec006_keys, DEFAULT_SPEC006_CONTRACT_KEYS)
        ),
        max_recent_transcript_items=_runtime_transcript_limit(state),
    )


def _normalized_source_text(
    *,
    request: AgentRunRequest,
    state: RuntimeState | None,
) -> str:
    parts: list[str] = [
        _string_value(request.message.text),
        _string_value(request.conversation.entry_intent),
        _string_value(request.conversation.source),
        _string_value(request.metadata.get("page_path")),
        _string_value(request.metadata.get("utm_source")),
    ]
    if state is not None:
        parts.append(_string_value(state.summary))
        for item in state.input_items[-4:]:
            parts.append(_string_value(item.get("content")))
    return _normalize_text(" ".join(part for part in parts if part))


def _runtime_transcript_limit(state: RuntimeState | None) -> int:
    diagnostic_status = ""
    if state is not None and isinstance(state.diagnostic, dict):
        diagnostic_status = str(state.diagnostic.get("status") or "")
    if diagnostic_status in {"in_progress", "completed"}:
        return _DIAGNOSTIC_RUNTIME_TRANSCRIPT_ITEMS
    return _DEFAULT_RUNTIME_TRANSCRIPT_ITEMS


def _contains_any(text: str, needles: Iterable[str]) -> bool:
    return any(_normalize_text(needle) in text for needle in needles)


def _dedupe_known(keys: Iterable[str], known_keys: Iterable[str]) -> list[str]:
    known = set(known_keys)
    selected: list[str] = []
    seen: set[str] = set()
    for key in keys:
        normalized = str(key).strip()
        if not normalized or normalized in seen or normalized not in known:
            continue
        selected.append(normalized)
        seen.add(normalized)
    return selected


def _normalize_text(value: str) -> str:
    text = unicodedata.normalize("NFKD", value.lower())
    return "".join(char for char in text if not unicodedata.combining(char))


def _string_value(value: Any) -> str:
    return str(value or "").strip()
