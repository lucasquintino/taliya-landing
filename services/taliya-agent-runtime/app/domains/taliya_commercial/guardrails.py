from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DomainGuardrailResult:
    name: str
    passed: bool
    reason: str = ""


GUARDRAIL_NAMES = [
    "relevance_guardrail",
    "prompt_injection_guardrail",
    "sensitive_data_guardrail",
    "human_active_guardrail",
]


def prompt_injection_guardrail(text: str) -> DomainGuardrailResult:
    lowered = text.lower()
    risky = any(
        token in lowered
        for token in (
            "ignore as instrucoes",
            "ignore previous instructions",
            "system prompt",
            "prompt do sistema",
            "developer message",
        )
    )
    return DomainGuardrailResult(
        name="prompt_injection_guardrail",
        passed=not risky,
        reason="prompt injection pattern" if risky else "",
    )


def relevance_guardrail(text: str) -> DomainGuardrailResult:
    if not text.strip():
        return DomainGuardrailResult("relevance_guardrail", True)
    lowered = text.lower()
    unrelated = any(token in lowered for token in ("receita de bolo", "jogo do bicho", "criptomoeda"))
    return DomainGuardrailResult(
        name="relevance_guardrail",
        passed=not unrelated,
        reason="unrelated to Taliya commercial flow" if unrelated else "",
    )


def sensitive_data_guardrail(text: str) -> DomainGuardrailResult:
    lowered = text.lower()
    risky = any(token in lowered for token in ("cartao de credito", "senha", "cpf de aluno"))
    return DomainGuardrailResult(
        name="sensitive_data_guardrail",
        passed=not risky,
        reason="sensitive data overcollection" if risky else "",
    )


def human_active_guardrail(human_status: str) -> DomainGuardrailResult:
    active = human_status == "active"
    return DomainGuardrailResult(
        name="human_active_guardrail",
        passed=not active,
        reason="human handoff active" if active else "",
    )


def validate_diagnostic_evidence(diagnostic: dict) -> DomainGuardrailResult:
    if diagnostic.get("status") == "completed" and not diagnostic.get("evidence"):
        return DomainGuardrailResult(
            name="diagnostic_evidence_guardrail",
            passed=False,
            reason="completed_diagnostic_without_evidence",
        )
    return DomainGuardrailResult(name="diagnostic_evidence_guardrail", passed=True)


def validate_waitlist_no_checkout(text: str) -> DomainGuardrailResult:
    lowered = text.lower()
    blocked = "checkout" in lowered or "link de pagamento" in lowered or "pagar agora" in lowered
    return DomainGuardrailResult(
        name="waitlist_no_checkout_guardrail",
        passed=not blocked,
        reason="waitlist_must_not_offer_checkout" if blocked else "",
    )


def run_input_guardrails(text: str, *, human_status: str = "none") -> list[DomainGuardrailResult]:
    return [
        relevance_guardrail(text),
        prompt_injection_guardrail(text),
        sensitive_data_guardrail(text),
        human_active_guardrail(human_status),
    ]
