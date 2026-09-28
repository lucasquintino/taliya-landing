from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from app.domains.taliya_commercial.behavior_policy import normalize_text


LedgerStatus = Literal["missing", "answered", "inferred_from_prior_message", "unresolved", "not_applicable"]


REQUIRED_QUESTION_KEYS = (
    "active_students_or_size",
    "main_pain",
    "pain_detail",
    "current_process",
    "priority",
    "urgency",
)

QUESTION_TEXT: dict[str, str] = {
    "active_students_or_size": "Hoje seu studio tem mais ou menos quantos alunos ativos?",
    "main_pain": "Quais partes mais dão trabalho hoje: WhatsApp, agenda/reposições, vendas, financeiro ou acompanhamento dos alunos?",
    "pain_detail": "Hoje você consegue ver facilmente o que precisa ser resolvido no dia?",
    "current_process": "Hoje isso fica em algum sistema ou mais em WhatsApp, planilha e caderno?",
    "priority": "Pensando na rotina do studio, qual tarefa você mais gostaria de deixar mais leve primeiro?",
    "urgency": "Vocês estão buscando resolver isso agora ou só pesquisando por enquanto?",
}


@dataclass
class DiagnosticLedgerItem:
    question_key: str
    status: LedgerStatus = "missing"
    answer_value: str | None = None
    areas: list[str] | None = None
    evidence: list[str] | None = None
    confidence: str = "low"
    last_asked_timestamp: str | None = None
    may_ask_again: bool = True

    def to_dict(self) -> dict[str, object]:
        return {
            "question_key": self.question_key,
            "status": self.status,
            "answer_value": self.answer_value,
            "areas": self.areas or [],
            "evidence": self.evidence or [],
            "confidence": self.confidence,
            "last_asked_timestamp": self.last_asked_timestamp,
            "may_ask_again": self.may_ask_again,
        }


def empty_ledger() -> list[dict[str, object]]:
    return [DiagnosticLedgerItem(question_key=key).to_dict() for key in REQUIRED_QUESTION_KEYS]


def _coerce_ledger(ledger: list[dict[str, object]] | None) -> list[DiagnosticLedgerItem]:
    existing = {str(item.get("question_key")): item for item in ledger or []}
    items: list[DiagnosticLedgerItem] = []
    for key in REQUIRED_QUESTION_KEYS:
        raw = existing.get(key, {})
        items.append(
            DiagnosticLedgerItem(
                question_key=key,
                status=raw.get("status", "missing"),  # type: ignore[arg-type]
                answer_value=raw.get("answer_value") if isinstance(raw.get("answer_value"), str) else None,
                areas=_coerce_areas(raw.get("areas")),
                evidence=list(raw.get("evidence") or []) if isinstance(raw.get("evidence") or [], list) else [],
                confidence=str(raw.get("confidence") or "low"),
                last_asked_timestamp=raw.get("last_asked_timestamp") if isinstance(raw.get("last_asked_timestamp"), str) else None,
                may_ask_again=bool(raw.get("may_ask_again", True)),
            )
        )
    return items


def _coerce_area(value: str) -> str | None:
    normalized = normalize_text(value)
    if "atendimento" in normalized or "whatsapp" in normalized:
        return "atendimento"
    if "venda" in normalized or "comercial" in normalized or "interess" in normalized:
        return "vendas"
    if "agenda" in normalized or "reposi" in normalized or "falta" in normalized or "encaixe" in normalized:
        return "agenda_reposicoes"
    if "financeiro" in normalized or "cobranca" in normalized or "mensalidade" in normalized or "pagamento" in normalized:
        return "financeiro"
    if "acompanh" in normalized or "retencao" in normalized or "reten" in normalized or "inativo" in normalized:
        return "acompanhamento"
    if "gestao" in normalized or "gestão" in value.lower():
        return "gestao"
    return None


def _coerce_areas(raw: object) -> list[str]:
    if not isinstance(raw, list):
        return []
    areas: list[str] = []
    for value in raw:
        if not isinstance(value, str):
            continue
        area = _coerce_area(value)
        if area and area not in areas:
            areas.append(area)
    return areas


def _areas_from_text(normalized: str) -> list[str]:
    areas: list[str] = []
    for value in (
        "atendimento" if "whatsapp" in normalized or "atendimento" in normalized else "",
        "vendas" if "venda" in normalized or "comercial" in normalized or "interess" in normalized else "",
        "agenda_reposicoes" if "agenda" in normalized or "reposi" in normalized or "falta" in normalized or "encaixe" in normalized else "",
        "financeiro" if "financeiro" in normalized or "cobranca" in normalized or "mensalidade" in normalized or "pagamento" in normalized else "",
        "acompanhamento" if "acompanh" in normalized or "retencao" in normalized or "reten" in normalized or "inativo" in normalized else "",
        "gestao" if "gestao" in normalized else "",
    ):
        if value and value not in areas:
            areas.append(value)
    return areas


def infer_ledger_from_text(text: str, *, previous_ledger: list[dict[str, object]] | None = None, evidence_id: str | None = None) -> list[dict[str, object]]:
    normalized = normalize_text(text)
    items = _coerce_ledger(previous_ledger)
    expected_key = next_question_key([item.to_dict() for item in items])
    if expected_key is None:
        return [item.to_dict() for item in items]

    def answer(key: str, value: str, confidence: str = "medium") -> None:
        item = next(current for current in items if current.question_key == key)
        if item.status in {"answered", "inferred_from_prior_message"} and item.answer_value:
            return
        item.status = "inferred_from_prior_message"
        item.answer_value = value
        item.areas = _areas_from_text(normalize_text(value))
        item.evidence = [evidence_id or "current_message"]
        item.confidence = confidence
        item.may_ask_again = False

    has_number = bool(re.search(r"\b\d{1,5}\b", normalized))
    looks_like_name_only = bool(re.fullmatch(r"[^\W\d_]{2,}(?:\s+[^\W\d_]{2,})?", text.strip(), flags=re.UNICODE))
    yes_no_answer = normalized in {"sim", "nao", "consigo", "nao consigo", "mais ou menos"}
    has_urgency_answer = any(
        token in normalized
        for token in (
            "resolver agora",
            "quero resolver",
            "preciso resolver",
            "estou buscando resolver",
            "agora",
            "urgente",
            "esse mes",
            "este mes",
            "proximos meses",
            "sem pressa",
            "pesquisando",
            "pesquisa",
            "so olhando",
            "mais pra frente",
        )
    )
    if expected_key == "active_students_or_size" and (
        has_number
        or any(token in normalized for token in ("aluno", "alunos", "matricula", "matriculas", "studio pequeno", "studio grande"))
    ):
        answer("active_students_or_size", text)
    elif expected_key == "main_pain" and not looks_like_name_only and len(normalized) > 2:
        answer("main_pain", text)
    elif expected_key == "pain_detail" and (yes_no_answer or (not looks_like_name_only and len(normalized) > 2)):
        answer("pain_detail", text)
    elif expected_key == "current_process" and not looks_like_name_only and len(normalized) > 2:
        answer("current_process", text)
    elif expected_key == "priority" and not looks_like_name_only and len(normalized) > 2:
        answer("priority", text)
    elif expected_key == "urgency" and has_urgency_answer:
        answer("urgency", text)

    return [item.to_dict() for item in items]


def apply_diagnostic_answer_interpretation(
    interpretation: object | None,
    *,
    previous_ledger: list[dict[str, object]] | None = None,
    evidence_id: str | None = None,
) -> tuple[list[dict[str, object]], bool]:
    items = _coerce_ledger(previous_ledger)
    if interpretation is None:
        return [item.to_dict() for item in items], False

    expected_key = next_question_key([item.to_dict() for item in items])
    if expected_key is None:
        return [item.to_dict() for item in items], False

    applied = False

    def value_from(source: object, key: str) -> object:
        if isinstance(source, dict):
            return source.get(key)
        return getattr(source, key, None)

    def answer_from_interpretation(source: object, *, default_key: str | None = None) -> None:
        nonlocal applied
        status = str(value_from(source, "answer_status") or "answered")
        confidence = str(value_from(source, "confidence") or "low")
        answer_value = value_from(source, "answer_value")
        evidence = value_from(source, "evidence")
        areas = _coerce_areas(value_from(source, "areas"))
        question_key = str(value_from(source, "question_key") or value_from(source, "current_question") or default_key or "")
        if question_key != expected_key:
            return
        if status != "answered" or confidence not in {"medium", "high"}:
            return
        if not isinstance(answer_value, str) or not answer_value.strip():
            return
        if not isinstance(evidence, list) or not any(isinstance(item, str) and item.strip() for item in evidence):
            return
        item = next(current for current in items if current.question_key == question_key)
        if item.status in {"answered", "inferred_from_prior_message"} and item.answer_value:
            return
        evidence_values = [str(entry).strip() for entry in evidence if isinstance(entry, str) and entry.strip()]
        item.status = "inferred_from_prior_message"
        item.answer_value = answer_value.strip()
        item.areas = areas or _areas_from_text(normalize_text(answer_value))
        item.evidence = evidence_values or [evidence_id or "current_message"]
        item.confidence = confidence
        item.may_ask_again = False
        applied = True

    answer_from_interpretation(interpretation, default_key=expected_key)

    return [item.to_dict() for item in items], applied


def ledger_is_complete(ledger: list[dict[str, object]] | None) -> bool:
    items = _coerce_ledger(ledger)
    return all(item.status in {"answered", "inferred_from_prior_message", "not_applicable"} for item in items)


def missing_or_unresolved_keys(ledger: list[dict[str, object]] | None) -> list[str]:
    items = _coerce_ledger(ledger)
    return [item.question_key for item in items if item.status in {"missing", "unresolved"}]


def next_question_key(ledger: list[dict[str, object]] | None) -> str | None:
    missing = missing_or_unresolved_keys(ledger)
    return missing[0] if missing else None


def next_question_text(ledger: list[dict[str, object]] | None) -> str | None:
    key = next_question_key(ledger)
    return QUESTION_TEXT.get(key) if key else None
