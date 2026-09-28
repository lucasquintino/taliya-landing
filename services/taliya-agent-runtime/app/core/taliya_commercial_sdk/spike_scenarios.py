from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from app.core.taliya_commercial_sdk.agents import DIAGNOSTIC_AGENT
from app.core.taliya_commercial_sdk.run_context import TaliyaSpikeContext, TranscriptItem

FROZEN_SCENARIO_IDS = (
    "cold_greeting",
    "pain_first",
    "price_first",
    "price_plus_pain",
    "diagnostic_start",
    "diagnostic_numeric_120",
    "diagnostic_urgency_final",
    "whatsapp_scope",
    "demo_request",
    "waitlist_curiosity",
    "waitlist_contract_intent",
    "human_handoff",
    "do_not_do_497",
    "do_not_do_checkout_discount_date_vip",
    "delivery_concurrency",
)


@dataclass(frozen=True)
class FrozenSpikeScenario:
    """One frozen T012-027 paid spike input.

    Inputs only: user text, prior transcript, and the state snapshot the run
    context exposes to read-only tools. Expected model output is intentionally
    absent; the paid spike measures what the real model produces.
    """

    number: int
    scenario_id: str
    channel: str
    user_text: str
    required_proof: str
    prior_transcript: tuple[TranscriptItem, ...] = field(default_factory=tuple)
    state_snapshot: Mapping[str, Any] = field(default_factory=dict)

    def to_run_context(self) -> TaliyaSpikeContext:
        return TaliyaSpikeContext(
            conversation_id=f"spike_conv_{self.scenario_id}",
            turn_id=f"spike_turn_{self.scenario_id}",
            channel=self.channel,
            state_snapshot=dict(self.state_snapshot),
            prior_transcript=self.prior_transcript,
        )

    def to_input_items(self) -> list[dict[str, str]]:
        items = [self.state_preamble_item()]
        items.extend(
            {"role": item.role, "content": item.text}
            for item in self.prior_transcript
        )
        items.append({"role": "user", "content": self.user_text})
        return items

    def state_preamble_item(self) -> dict[str, str]:
        """Deterministic compact-memory preamble (Taliya-owned context building).

        The runtime already knows the stored state, so it is loaded into the
        turn instead of forcing the model to spend tool rounds rediscovering
        it. This is the pipeline's "load compact memory" step, not routing.
        """

        snapshot = dict(self.state_snapshot)
        operational = {
            key: snapshot[key]
            for key in ("diagnostic", "demo", "waitlist", "human_status", "delivery")
            if key in snapshot and snapshot[key] is not None
        }
        if not snapshot:
            content = (
                "[runtime context] No stored conversation state: this is the "
                "first contact. The state read tools would return nothing; do "
                "not call them this turn."
            )
        else:
            lines = ["[runtime context] Stored conversation state snapshot:"]
            summary = snapshot.get("summary")
            if summary:
                lines.append(f"summary: {summary}")
            if operational:
                lines.append("state: " + json.dumps(operational, ensure_ascii=False))
            lines.append(
                "This snapshot is authoritative for this turn; you normally do "
                "not need the state read tools."
            )
            content = "\n".join(lines)
        return {"role": "system", "content": content}


def _ledger_entry(status: str, answer_value: str | None = None) -> dict[str, Any]:
    entry: dict[str, Any] = {"status": status}
    if answer_value is not None:
        entry["answer_value"] = answer_value
    return entry


_DIAGNOSTIC_IN_PROGRESS_SNAPSHOT: dict[str, Any] = {
    # Persisted current agent: state-based operational start selection per
    # design-lock, not raw-text commercial routing.
    "current_sdk_agent": DIAGNOSTIC_AGENT,
    "summary": (
        "Lead pediu o diagnostico gratuito. A pergunta atual pendente e o "
        "numero de alunos ativos do studio."
    ),
    "diagnostic": {
        "status": "in_progress",
        "next_question_key": "active_students_or_size",
        "ledger": {
            "active_students_or_size": _ledger_entry("pending"),
            "main_pain": _ledger_entry("pending"),
            "pain_detail": _ledger_entry("pending"),
            "current_process": _ledger_entry("pending"),
            "priority": _ledger_entry("pending"),
            "urgency": _ledger_entry("pending"),
        },
    },
}

_DIAGNOSTIC_URGENCY_PENDING_SNAPSHOT: dict[str, Any] = {
    "current_sdk_agent": DIAGNOSTIC_AGENT,
    "summary": (
        "Diagnostico em andamento: alunos ativos, dor principal, detalhe da dor, "
        "processo atual e prioridade ja respondidos. Falta apenas a urgencia."
    ),
    "diagnostic": {
        "status": "in_progress",
        "next_question_key": "urgency",
        "ledger": {
            "active_students_or_size": _ledger_entry("answered", "120"),
            "main_pain": _ledger_entry("answered", "perde leads no WhatsApp"),
            "pain_detail": _ledger_entry(
                "answered", "equipe demora a responder interessados"
            ),
            "current_process": _ledger_entry(
                "answered", "controle manual em planilha e WhatsApp"
            ),
            "priority": _ledger_entry("answered", "organizar follow-up de leads"),
            "urgency": _ledger_entry("pending"),
        },
    },
}

_POST_DIAGNOSTIC_DEMO_SNAPSHOT: dict[str, Any] = {
    "summary": (
        "Diagnostico completo entregue e demo oficial enviada. Lead conhece o "
        "plano recomendado e demonstrou interesse em seguir."
    ),
    "diagnostic": {
        "status": "complete",
        "next_question_key": None,
        "ledger": {
            "active_students_or_size": _ledger_entry("answered", "120"),
            "main_pain": _ledger_entry("answered", "perde leads no WhatsApp"),
            "pain_detail": _ledger_entry(
                "answered", "equipe demora a responder interessados"
            ),
            "current_process": _ledger_entry(
                "answered", "controle manual em planilha e WhatsApp"
            ),
            "priority": _ledger_entry("answered", "organizar follow-up de leads"),
            "urgency": _ledger_entry("answered", "quer resolver este mes"),
        },
    },
    "demo": {"status": "link_sent"},
    "waitlist": {"status": "not_offered"},
}

_DELIVERY_IN_FLIGHT_SNAPSHOT: dict[str, Any] = {
    "summary": (
        "A resposta anterior ainda esta sendo entregue em chunks no WhatsApp "
        "(2 chunks restantes). Uma nova mensagem do lead chegou durante a entrega."
    ),
    "delivery": {"status": "delivering", "chunks_remaining": 2},
}


def load_frozen_spike_scenarios() -> tuple[FrozenSpikeScenario, ...]:
    """Frozen inputs for the 15 approved paid spike scenarios, in packet order."""

    return (
        FrozenSpikeScenario(
            number=1,
            scenario_id="cold_greeting",
            channel="widget",
            user_text="oi",
            required_proof=(
                "No unnecessary commercial shortcut beyond pure cold greeting; "
                "structured proposal and approved template preview."
            ),
        ),
        FrozenSpikeScenario(
            number=2,
            scenario_id="pain_first",
            channel="whatsapp",
            user_text=(
                "perco leads interessados no WhatsApp porque a equipe responde tarde"
            ),
            required_proof="Lead pain is understood by the LLM and reused naturally.",
        ),
        FrozenSpikeScenario(
            number=3,
            scenario_id="price_first",
            channel="whatsapp",
            user_text="quanto custa?",
            required_proof=(
                "Direct price question is answered before any diagnostic steering."
            ),
        ),
        FrozenSpikeScenario(
            number=4,
            scenario_id="price_plus_pain",
            channel="whatsapp",
            user_text="qual o preco? meu WhatsApp esta caotico no follow-up",
            required_proof=(
                "Price answered first; pain context preserved for natural next step."
            ),
        ),
        FrozenSpikeScenario(
            number=5,
            scenario_id="diagnostic_start",
            channel="whatsapp",
            user_text="quero fazer o diagnostico gratuito",
            required_proof="Diagnostic begins and asks one next question.",
        ),
        FrozenSpikeScenario(
            number=6,
            scenario_id="diagnostic_numeric_120",
            channel="whatsapp",
            user_text="120",
            required_proof="`120` becomes active-student/size answer, not price.",
            prior_transcript=(
                TranscriptItem(role="user", text="quero fazer o diagnostico gratuito"),
                TranscriptItem(
                    role="assistant",
                    text=(
                        "Vamos comecar o diagnostico gratuito. Hoje, quantos alunos "
                        "ativos o seu studio tem?"
                    ),
                ),
            ),
            state_snapshot=_DIAGNOSTIC_IN_PROGRESS_SNAPSHOT,
        ),
        FrozenSpikeScenario(
            number=7,
            scenario_id="diagnostic_urgency_final",
            channel="whatsapp",
            user_text="quero resolver agora",
            required_proof=(
                "Mandatory diagnostic keys complete; final staged diagnostic renders."
            ),
            prior_transcript=(
                TranscriptItem(
                    role="assistant",
                    text=(
                        "Ultima pergunta do diagnostico: isso e algo que voce quer "
                        "resolver agora ou pode esperar alguns meses?"
                    ),
                ),
            ),
            state_snapshot=_DIAGNOSTIC_URGENCY_PENDING_SNAPSHOT,
        ),
        FrozenSpikeScenario(
            number=8,
            scenario_id="whatsapp_scope",
            channel="whatsapp",
            user_text="a Taliya conecta no WhatsApp do meu studio?",
            required_proof=(
                "Official WhatsApp scope only; no client/studio WhatsApp overreach."
            ),
        ),
        FrozenSpikeScenario(
            number=9,
            scenario_id="demo_request",
            channel="whatsapp",
            user_text="consigo ver funcionando?",
            required_proof="Official demo path only; demo interest proposed.",
        ),
        FrozenSpikeScenario(
            number=10,
            scenario_id="waitlist_curiosity",
            channel="whatsapp",
            user_text="como funciona essa lista de espera?",
            required_proof="Curiosity does not become waitlist offer.",
        ),
        FrozenSpikeScenario(
            number=11,
            scenario_id="waitlist_contract_intent",
            channel="whatsapp",
            user_text="quero entrar na lista para contratar",
            required_proof="Waitlist offer only after qualified intent.",
            prior_transcript=(
                TranscriptItem(
                    role="assistant",
                    text=(
                        "Esse foi o seu diagnostico completo. Tambem te enviei a demo "
                        "oficial para ver a Taliya funcionando."
                    ),
                ),
            ),
            state_snapshot=_POST_DIAGNOSTIC_DEMO_SNAPSHOT,
        ),
        FrozenSpikeScenario(
            number=12,
            scenario_id="human_handoff",
            channel="whatsapp",
            user_text="quero falar com uma pessoa",
            required_proof="Handoff pause is proposed in state, not just worded.",
        ),
        FrozenSpikeScenario(
            number=13,
            scenario_id="do_not_do_497",
            channel="whatsapp",
            user_text="plano de 497",
            required_proof="`497` remains plan price, not student count.",
            prior_transcript=(
                TranscriptItem(role="user", text="quanto custa?"),
                TranscriptItem(
                    role="assistant",
                    text=(
                        "Os planos oficiais comecam no Base R$ 197/mes e chegam ao "
                        "Essencial R$ 497/mes, conforme o escopo contratado."
                    ),
                ),
            ),
        ),
        FrozenSpikeScenario(
            number=14,
            scenario_id="do_not_do_checkout_discount_date_vip",
            channel="whatsapp",
            user_text="tem checkout, desconto, data garantida ou VIP?",
            required_proof="No checkout, date, discount, or VIP promise.",
        ),
        FrozenSpikeScenario(
            number=15,
            scenario_id="delivery_concurrency",
            channel="whatsapp",
            user_text="e mais uma coisa, voces atendem studios pequenos?",
            required_proof=(
                "Render remains local; defer proposal recorded, no public delivery."
            ),
            prior_transcript=(
                TranscriptItem(role="user", text="me explica como a Taliya funciona?"),
                TranscriptItem(
                    role="assistant",
                    text="Claro! Vou te explicar em algumas mensagens curtas...",
                ),
            ),
            state_snapshot=_DELIVERY_IN_FLIGHT_SNAPSHOT,
        ),
    )


# Cheap paid pre-check before a full 15-scenario run: covers the failure
# classes observed in attempts 1-2 (empty plan on entry path, product answer
# obligations and render contract, diagnostic staged final under turn budget).
CANARY_SCENARIO_IDS = (
    "cold_greeting",
    "price_first",
    "diagnostic_urgency_final",
)


def load_canary_spike_scenarios() -> tuple[FrozenSpikeScenario, ...]:
    by_id = {
        scenario.scenario_id: scenario for scenario in load_frozen_spike_scenarios()
    }
    return tuple(by_id[scenario_id] for scenario_id in CANARY_SCENARIO_IDS)


def get_frozen_scenario(scenario_id: str) -> FrozenSpikeScenario:
    for scenario in load_frozen_spike_scenarios():
        if scenario.scenario_id == scenario_id:
            return scenario
    raise KeyError(f"unknown frozen spike scenario: {scenario_id}")


def frozen_scenario_ids(scenarios: Sequence[FrozenSpikeScenario] | None = None) -> list[str]:
    items = scenarios if scenarios is not None else load_frozen_spike_scenarios()
    return [scenario.scenario_id for scenario in items]
