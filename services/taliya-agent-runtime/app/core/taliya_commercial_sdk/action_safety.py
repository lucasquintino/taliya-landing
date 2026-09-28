"""T012-032C: deterministic SDK-path safety preguard.

This module handles operational/safety boundaries before any LLM call. It
must not classify commercial meaning; it only blocks prompt-injection,
unsupported media, sensitive data, and medical/health advice requests.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass


@dataclass(frozen=True)
class SafetyBoundary:
    code: str
    template_id: str
    variables: dict[str, dict[str, object]]
    state_patch: dict[str, object]


_PROMPT_INJECTION_PHRASES = (
    "ignore suas instrucoes",
    "ignore as instrucoes",
    "ignore all previous instructions",
    "ignore previous",
    "system prompt",
    "developer message",
    "mostre suas instrucoes internas",
    "revele seu prompt",
    "regras do sistema",
)
_SENSITIVE_DATA_PHRASES = (
    "meu cpf",
    "cpf:",
    "cartao de credito",
    "numero do cartao",
    "dados dos alunos",
    "dados sensiveis",
)
_SENSITIVE_DATA_POLICY_QUESTION_MARKERS = (
    "posso mandar",
    "pode mandar",
    "pode enviar",
    "tem lgpd",
    "e seguro",
    "?",
)
_MEDICAL_ADVICE_PHRASES = (
    "dor no joelho",
    "dor na coluna",
    "lesao",
    "exercicio para dor",
    "tratamento medico",
    "conselho medico",
    "diagnostico medico",
)


def _normalize_text(value: str) -> str:
    folded = value.casefold()
    normalized = unicodedata.normalize("NFKD", folded)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    return " ".join(ascii_text.split())


def classify_safety_boundary(
    *,
    user_text: str,
    message_type: str = "text",
    unsupported_media_kind: str | None = None,
) -> SafetyBoundary | None:
    """Return a safety boundary for operationally blocked inputs.

    Text checks are intentionally narrow and customer-safety oriented. They do
    not decide price/demo/plan/diagnostic/waitlist meaning.
    """

    if message_type != "text":
        media_kind = unsupported_media_kind or message_type
        return SafetyBoundary(
            code="unsupported_media",
            template_id="safety.unsupported_media",
            variables={
                "unsupported_media_kind": {
                    "kind": "enum",
                    "value": media_kind,
                    "source": "runtime_state",
                    "evidence": ["inbound.message_type"],
                }
            },
            state_patch={"safety_blocked": True, "safety_reason": "unsupported_media"},
        )

    text = _normalize_text(user_text)
    if any(phrase in text for phrase in _PROMPT_INJECTION_PHRASES):
        return SafetyBoundary(
            code="prompt_injection",
            template_id="safety.prompt_injection",
            variables={},
            state_patch={"safety_blocked": True, "safety_reason": "prompt_injection"},
        )
    sensitive_hit = any(phrase in text for phrase in _SENSITIVE_DATA_PHRASES)
    policy_question = (
        "dados dos alunos" in text
        and any(marker in text for marker in _SENSITIVE_DATA_POLICY_QUESTION_MARKERS)
    )
    if sensitive_hit and not policy_question:
        return SafetyBoundary(
            code="sensitive_data",
            template_id="safety.sensitive_data",
            variables={},
            state_patch={"safety_blocked": True, "safety_reason": "sensitive_data"},
        )
    if any(phrase in text for phrase in _MEDICAL_ADVICE_PHRASES):
        return SafetyBoundary(
            code="medical_advice",
            template_id="safety.no_medical_advice",
            variables={},
            state_patch={"safety_blocked": True, "safety_reason": "medical_advice"},
        )
    return None
