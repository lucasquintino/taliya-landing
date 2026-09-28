from __future__ import annotations

from typing import Any

from app.domains.taliya_commercial.templates import get_template
from app.runtime.schemas import AgentMessage


class RenderError(ValueError):
    pass


def _format_body(text: str, variables: dict[str, Any]) -> str:
    try:
        return text.format(**variables)
    except KeyError as exc:
        raise RenderError(f"missing template variable: {exc.args[0]}") from exc


def _chunk_text(text: str, max_chars: int) -> list[str]:
    cleaned = " ".join(text.split())
    if len(cleaned) <= max_chars:
        return [cleaned]
    chunks: list[str] = []
    current = ""
    for word in cleaned.split(" "):
        candidate = f"{current} {word}".strip()
        if len(candidate) > max_chars and current:
            chunks.append(current)
            current = word
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks


def render_template(
    template_id: str,
    *,
    channel: str,
    variables: dict[str, Any] | None = None,
) -> list[AgentMessage]:
    template = get_template(template_id)
    if template.channel_support != "both" and template.channel_support != channel:
        raise RenderError(f"template {template_id} is not allowed for channel {channel}")
    values = variables or {}
    if template_id == "product.demo_direct" and not values.get("demo_contextual_next_step"):
        values = {
            **values,
            "demo_contextual_next_step": "Se você me contar um pouco da rotina do seu studio, eu consigo te indicar o que vale olhar primeiro na demonstração.",
        }
    if template_id == "product.integration_scope_direct" and not values.get("integration_topic"):
        values = {**values, "integration_topic": "essa integração"}
    if template_id == "product.comparison_current_tool" and not values.get("current_tool_context"):
        values = {**values, "current_tool_context": "o processo atual"}
    if template_id == "post_diagnostic.priority_update":
        values = {
            "priority_area": "vendas",
            "demo_area": "interessados que chegam, conversas que esfriam e próximos retornos da equipe",
            **values,
        }
    for required in template.required_variables:
        if required not in values or values[required] in {None, ""}:
            raise RenderError(f"missing required variable {required} for {template_id}")
    messages: list[AgentMessage] = []
    answer_feedback = values.get("answer_feedback")
    if template_id.startswith("diagnostic.ask_") and isinstance(answer_feedback, str) and answer_feedback.strip():
        messages.append(
            AgentMessage(
                text=" ".join(answer_feedback.split()),
                channel_hint=channel,  # type: ignore[arg-type]
                kind="text",
                template_id=template_id,
                requires_product_source=bool(template.product_keys),
            )
        )
    for body in template.body:
        formatted = _format_body(body, values)
        kind = "action" if channel == "widget" and template.buttons_allowed and "http" in formatted else "text"
        for chunk in _chunk_text(formatted, template.max_chars_per_chunk):
            messages.append(
                AgentMessage(
                    text=chunk,
                    channel_hint=channel,  # type: ignore[arg-type]
                    kind=kind,  # type: ignore[arg-type]
                    template_id=template_id,
                    requires_product_source=bool(template.product_keys),
                )
            )
    return messages[: template.max_messages]


def render_template_plan(
    template_ids: list[str],
    *,
    channel: str,
    variables_by_template: dict[str, dict[str, Any]] | None = None,
) -> list[AgentMessage]:
    rendered: list[AgentMessage] = []
    variables_by_template = variables_by_template or {}
    occurrence_counts: dict[str, int] = {}
    for template_id in template_ids:
        occurrence_counts[template_id] = occurrence_counts.get(template_id, 0) + 1
        occurrence = occurrence_counts[template_id]
        occurrence_key = f"{template_id}#{occurrence}"
        variables = variables_by_template.get(occurrence_key, variables_by_template.get(template_id, {}))
        rendered.extend(
            render_template(
                template_id,
                channel=channel,
                variables=variables,
            )
        )
    staged_diagnostic = any(template_id.startswith("diagnostic.deliver_") for template_id in template_ids)
    if staged_diagnostic:
        return rendered
    product_followup = any(
        template_id
        in {
            "product.how_it_works_direct",
            "product.comparison_current_tool",
            "product.integration_scope_direct",
            "product.whatsapp_business_requirement",
            "product.security_data_direct",
            "product.out_of_profile_redirect",
            "post_diagnostic.thinking",
            "post_diagnostic.priority_update",
        }
        for template_id in template_ids
    )
    if product_followup:
        return rendered[:5]
    if channel == "whatsapp":
        return rendered[:3]
    return rendered[:3]
