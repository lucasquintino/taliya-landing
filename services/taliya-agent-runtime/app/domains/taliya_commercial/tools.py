from __future__ import annotations

from typing import Any, Callable, TypeVar
import re

from app.domains.taliya_commercial.context import TaliyaCommercialContext
from app.shared.product_knowledge.source import get_product_knowledge_source

F = TypeVar("F", bound=Callable[..., Any])

REQUIRED_TOOL_NAMES = [
    "get_product_knowledge",
    "save_lead_facts",
    "save_diagnostic_record",
    "mark_waitlist",
    "pause_for_human",
    "resume_from_human",
    "record_runtime_note",
]


def function_tool(func: F | None = None, **kwargs: Any) -> F | Callable[[F], F]:
    """Local tool contract marker.

    SDK-facing wrappers are created in the agent definition layer so direct domain tools can accept
    the runtime context used by tests and persistence code.
    """

    def decorate(inner: F) -> F:
        setattr(inner, "taliya_tool_name", kwargs.get("name_override") or inner.__name__)
        setattr(inner, "taliya_model_callable", True)
        return inner

    return decorate(func) if func else decorate


@function_tool(name_override="get_product_knowledge")
async def get_product_knowledge(requested_keys: list[str] | None = None) -> dict[str, Any]:
    source = get_product_knowledge_source()
    return source.query(requested_keys)


@function_tool(name_override="save_lead_facts")
async def save_lead_facts(
    context: TaliyaCommercialContext,
    idempotency_key: str,
    facts: list[dict[str, Any]],
) -> dict[str, Any]:
    async def action() -> dict[str, Any]:
        await context.store.append_lead_facts(context.conversation_id, facts)
        return {"status": "ok", "saved_count": len(facts)}

    return await context.store.run_idempotent_tool(idempotency_key, action)


def extract_lead_facts_from_text(text: str, evidence_id: str) -> list[dict[str, Any]]:
    lowered = text.lower()
    facts: list[dict[str, Any]] = []
    active_students = re.search(r"\b(\d{2,4})\s+(?:alunos|clientes|matriculados)\b", lowered)
    if active_students:
        facts.append(
            {
                "key": "active_students",
                "value": active_students.group(1),
                "confidence": "high",
                "evidence": [evidence_id],
            }
        )
    pain_map = [
        ("reposicoes", ("reposicao", "reposicoes", "reposição", "reposições")),
        ("agenda", ("agenda", "horario", "horarios", "turma")),
        ("whatsapp", ("whatsapp", "mensagem", "atendimento")),
        ("vendas", ("interessado", "interessados", "venda", "experimental")),
        ("financeiro", ("mensalidade", "cobranca", "pagamento")),
        ("retencao", ("inativo", "sumiu", "faltas", "falta")),
    ]
    for value, tokens in pain_map:
        if any(token in lowered for token in tokens):
            facts.append({"key": "main_pain", "value": value, "confidence": "medium", "evidence": [evidence_id]})
            break
    if any(token in lowered for token in ("planilha", "caderno", "sistema", "tecnofit", "agenda")):
        facts.append({"key": "current_system", "value": "mentioned", "confidence": "medium", "evidence": [evidence_id]})
    if any(token in lowered for token in ("quero", "preciso", "aliviar", "resolver", "melhorar")):
        facts.append({"key": "priority_goal", "value": text[:180], "confidence": "medium", "evidence": [evidence_id]})
    return facts


@function_tool(name_override="save_diagnostic_record")
async def save_diagnostic_record(
    context: TaliyaCommercialContext,
    idempotency_key: str,
    diagnostic: dict[str, Any],
) -> dict[str, Any]:
    async def action() -> dict[str, Any]:
        context.state["diagnostic"] = diagnostic
        await context.store.save_diagnostic(context.conversation_id, diagnostic)
        return {"status": "ok", "diagnostic_status": diagnostic.get("status")}

    return await context.store.run_idempotent_tool(idempotency_key, action)


@function_tool(name_override="mark_waitlist")
async def mark_waitlist(
    context: TaliyaCommercialContext,
    idempotency_key: str,
    status: str,
    reason: str | None = None,
    missing_fields: list[str] | None = None,
) -> dict[str, Any]:
    async def action() -> dict[str, Any]:
        data = {
            "status": status,
            "reason": reason,
            "missing_fields": missing_fields or [],
        }
        context.state["waitlist"] = data
        await context.store.set_waitlist(context.conversation_id, data)
        return data

    return await context.store.run_idempotent_tool(idempotency_key, action)


@function_tool(name_override="pause_for_human")
async def pause_for_human(
    context: TaliyaCommercialContext,
    idempotency_key: str,
    reason: str,
) -> dict[str, Any]:
    async def action() -> dict[str, Any]:
        context.state["human_status"] = "active"
        context.state["human_reason"] = reason
        await context.store.set_human_status(context.conversation_id, "active", reason)
        return {"status": "active", "reason": reason}

    return await context.store.run_idempotent_tool(idempotency_key, action)


@function_tool(name_override="resume_from_human")
async def resume_from_human(
    context: TaliyaCommercialContext,
    idempotency_key: str,
) -> dict[str, Any]:
    async def action() -> dict[str, Any]:
        context.state["human_status"] = "resumed"
        context.state["human_reason"] = None
        await context.store.set_human_status(context.conversation_id, "resumed", "operator_resume")
        return {"status": "resumed"}

    return await context.store.run_idempotent_tool(idempotency_key, action)


@function_tool(name_override="record_runtime_note")
async def record_runtime_note(
    context: TaliyaCommercialContext,
    idempotency_key: str,
    note: str,
) -> dict[str, Any]:
    async def action() -> dict[str, Any]:
        notes = context.state.setdefault("notes", [])
        notes.append(note)
        return {"status": "ok", "note": note}

    return await context.store.run_idempotent_tool(idempotency_key, action)


def get_model_callable_tool_names() -> list[str]:
    return list(REQUIRED_TOOL_NAMES)


def get_model_callable_tools() -> list[Callable[..., Any]]:
    tools: list[Callable[..., Any]] = [
        get_product_knowledge,
        save_lead_facts,
        save_diagnostic_record,
        mark_waitlist,
        pause_for_human,
        resume_from_human,
        record_runtime_note,
    ]
    return tools
