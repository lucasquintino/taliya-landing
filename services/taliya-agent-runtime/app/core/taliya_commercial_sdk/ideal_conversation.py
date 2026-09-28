from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from app.core.taliya_commercial_sdk.paid_spike_harness import (
    ScenarioReport,
    SpikeBudget,
    SpikeRunReport,
    run_spike_scenarios,
)
from app.core.taliya_commercial_sdk.run_context import TranscriptItem
from app.core.taliya_commercial_sdk.spike_scenarios import FrozenSpikeScenario

REQUIRED_DIAGNOSTIC_KEYS = (
    "active_students_or_size",
    "main_pain",
    "pain_detail",
    "current_process",
    "priority",
    "urgency",
)


@dataclass(frozen=True)
class ConversationTurnScript:
    user_text: str
    goal: str


# The ideal commercial conversation: one lead going through the whole funnel
# in a single continuous WhatsApp conversation - source opening, pain, direct
# price answer, full diagnostic (one question per turn, urgency last), staged
# final diagnostic, demo, and waitlist with clear contract intent.
IDEAL_CONVERSATION_SCRIPT: tuple[ConversationTurnScript, ...] = (
    ConversationTurnScript(
        "oi, vi o perfil de voces no Instagram",
        "Source opening: greet naturally, acknowledge source, no invented pain.",
    ),
    ConversationTurnScript(
        "tenho um studio de pilates e to perdendo aluno novo porque o "
        "WhatsApp vive atrasado",
        "Pain-first: understand and reuse the concrete pain naturally.",
    ),
    ConversationTurnScript(
        "quanto custa isso?",
        "Price-first: answer official price directly before any steering.",
    ),
    ConversationTurnScript(
        "faz sentido... como funciona esse diagnostico gratuito?",
        "Diagnostic start: begin and ask exactly one question (active students).",
    ),
    ConversationTurnScript(
        "120",
        "Numeric answer: 120 becomes active students; next question, no repeat.",
    ),
    ConversationTurnScript(
        "minha maior dor e perder interessado porque demoramos pra responder",
        "main_pain captured; continue without repeating answered questions.",
    ),
    ConversationTurnScript(
        "a gente so consegue responder de noite, ai o lead ja fechou com "
        "outro studio",
        "pain_detail captured; ledger keeps evolving.",
    ),
    ConversationTurnScript(
        "hoje e planilha e caderno mesmo, nada organizado",
        "current_process captured.",
    ),
    ConversationTurnScript(
        "minha prioridade e nao perder mais nenhum lead novo",
        "priority captured; urgency must be the only remaining key.",
    ),
    ConversationTurnScript(
        "quero resolver isso agora, esse mes ainda",
        "urgency captured; deliver the final staged diagnostic grounded in "
        "the ledger and official plan facts.",
    ),
    ConversationTurnScript(
        "consigo ver funcionando antes?",
        "Demo request: official demo path only; demo interest proposed.",
    ),
    ConversationTurnScript(
        "gostei. quero entrar na lista pra contratar",
        "Clear contract intent: waitlist offer is now appropriate.",
    ),
)


@dataclass
class ConversationState:
    """Deterministic state commit after validation, simulating the runtime."""

    snapshot: dict[str, Any] = field(default_factory=dict)
    transcript: list[TranscriptItem] = field(default_factory=list)

    def apply_validated_turn(self, report: ScenarioReport, user_text: str) -> None:
        self.transcript.append(TranscriptItem(role="user", text=user_text))
        for message in report.rendered_preview:
            text = message.get("text") if isinstance(message, dict) else None
            if text:
                self.transcript.append(TranscriptItem(role="assistant", text=text))

        proposal = report.turn_proposal or {}

        diagnostic = dict(self.snapshot.get("diagnostic") or {})
        ledger = dict(diagnostic.get("ledger") or {})
        diagnostic_proposal = proposal.get("diagnostic_proposal") or {}
        for update in diagnostic_proposal.get("ledger_updates", []):
            key = update.get("question_key")
            if not key:
                continue
            entry = {"status": update.get("status", "answered")}
            if update.get("answer_value") is not None:
                entry["answer_value"] = update["answer_value"]
            ledger[key] = entry
        if ledger:
            diagnostic["ledger"] = ledger
        next_key = diagnostic_proposal.get("next_question_key")
        if diagnostic_proposal.get("final_diagnostic_ready"):
            diagnostic["status"] = "complete"
            diagnostic["next_question_key"] = None
        elif next_key:
            diagnostic["status"] = "in_progress"
            diagnostic["next_question_key"] = next_key
        if diagnostic:
            self.snapshot["diagnostic"] = diagnostic

        for state_key, proposal_key in (
            ("demo", "demo_proposal"),
            ("waitlist", "waitlist_proposal"),
        ):
            payload = proposal.get(proposal_key) or {}
            meaningful = {
                key: value
                for key, value in payload.items()
                if key != "evidence" and value not in (None, "none", "unknown", [])
            }
            if meaningful:
                self.snapshot[state_key] = meaningful

        handoff = proposal.get("handoff_proposal") or {}
        if handoff.get("pause_required"):
            self.snapshot["human_status"] = "requested"

        # Deterministic obligation memory: questions answered in earlier turns
        # are committed state, so later turns must not resurrect them.
        answered = list(self.snapshot.get("answered_obligations") or [])
        for obligation in proposal.get("answer_obligations") or []:
            if obligation.get("answered_before_steering") and obligation.get(
                "obligation"
            ):
                answered.append(str(obligation["obligation"]))
        if answered:
            self.snapshot["answered_obligations"] = answered

        agent_path = proposal.get("agent_path") or []
        final_agent = next(
            (
                item.get("agent")
                for item in reversed(agent_path)
                if item.get("event") == "final" and item.get("agent")
            ),
            None,
        )
        # Sticky agents are only the flow owners while their flow is open: the
        # diagnostic agent during an in-progress diagnostic and the handoff
        # agent while paused. Product and waitlist answers are turn-local -
        # the next turn goes back through the router, otherwise a sticky
        # specialist absorbs flows it does not own (observed in
        # ideal-conversation run 3: product conducted the diagnostic badly;
        # run 5: completed diagnostic kept absorbing the demo request).
        diagnostic_in_progress = (
            (self.snapshot.get("diagnostic") or {}).get("status") == "in_progress"
        )
        if final_agent == "taliya_handoff_agent" or (
            final_agent == "taliya_diagnostic_agent" and diagnostic_in_progress
        ):
            self.snapshot["current_sdk_agent"] = final_agent
        else:
            self.snapshot.pop("current_sdk_agent", None)

        self.snapshot["summary"] = self._build_summary()

    def _build_summary(self) -> str:
        parts = ["Conversa comercial em andamento no WhatsApp da Taliya."]
        diagnostic = self.snapshot.get("diagnostic") or {}
        ledger = diagnostic.get("ledger") or {}
        answered = [
            f"{key}={entry.get('answer_value')}"
            for key, entry in ledger.items()
            if isinstance(entry, dict) and entry.get("status") == "answered"
        ]
        if diagnostic.get("status") == "complete":
            parts.append("Diagnostico completo e entregue.")
        elif answered:
            parts.append(
                "Diagnostico em andamento. Respondido: " + "; ".join(answered) + "."
            )
            if diagnostic.get("next_question_key"):
                parts.append(
                    f"Proxima pergunta pendente: {diagnostic['next_question_key']}."
                )
        demo = self.snapshot.get("demo")
        if demo:
            parts.append(f"Demo: {json.dumps(demo, ensure_ascii=False)}.")
        waitlist = self.snapshot.get("waitlist")
        if waitlist:
            parts.append(f"Waitlist: {json.dumps(waitlist, ensure_ascii=False)}.")
        answered = self.snapshot.get("answered_obligations")
        if answered:
            parts.append(
                "Perguntas diretas ja respondidas em turnos anteriores (nao "
                "criam novas obrigacoes): " + "; ".join(answered) + "."
            )
        return " ".join(parts)


@dataclass
class IdealConversationReport:
    turn_run_reports: list[SpikeRunReport] = field(default_factory=list)
    total_cost_usd: float = 0.0
    total_model_operations: int = 0
    turns_passed: int = 0
    stopped_at_turn: int | None = None
    final_state: dict[str, Any] = field(default_factory=dict)
    full_transcript: list[dict[str, str]] = field(default_factory=list)


async def run_ideal_conversation(
    *,
    paid_openai_approved: bool = False,
    model: Any | None = None,
    script: Sequence[ConversationTurnScript] | None = None,
    budget: SpikeBudget | None = None,
    report_dir: Path | str | None = None,
) -> IdealConversationReport:
    """Run the ideal full-funnel conversation turn by turn.

    Each turn goes through the same harness as the frozen scenarios; the
    state snapshot for turn N+1 is committed deterministically from turn N's
    validated proposal, mirroring the runtime's commit-after-validation rule.
    The conversation stops at the first turn that fails validation, because
    later turns would build on an unvalidated state.
    """

    active_script = tuple(script) if script is not None else IDEAL_CONVERSATION_SCRIPT
    active_budget = budget or SpikeBudget()
    state = ConversationState()
    conversation_report = IdealConversationReport()
    base_dir = Path(report_dir) if report_dir is not None else None
    remaining_cost = active_budget.max_total_cost_usd
    remaining_ops = active_budget.max_total_model_operations

    for index, turn in enumerate(active_script, start=1):
        scenario = FrozenSpikeScenario(
            number=index,
            scenario_id=f"ideal_turn_{index:02d}",
            channel="whatsapp",
            user_text=turn.user_text,
            required_proof=turn.goal,
            prior_transcript=tuple(state.transcript),
            state_snapshot=dict(state.snapshot),
        )
        turn_report = await run_spike_scenarios(
            paid_openai_approved=paid_openai_approved,
            model=model,
            scenarios=[scenario],
            budget=SpikeBudget(
                max_total_model_operations=remaining_ops,
                max_total_cost_usd=remaining_cost,
                max_model_operations_per_scenario=(
                    active_budget.max_model_operations_per_scenario
                ),
            ),
            report_dir=(base_dir / f"turn-{index:02d}") if base_dir else None,
        )
        conversation_report.turn_run_reports.append(turn_report)
        conversation_report.total_cost_usd += turn_report.total_cost_usd
        conversation_report.total_model_operations += (
            turn_report.total_model_operations
        )
        remaining_cost -= turn_report.total_cost_usd
        remaining_ops -= turn_report.total_model_operations

        scenario_report = (
            turn_report.scenario_reports[0] if turn_report.scenario_reports else None
        )
        if scenario_report is None or scenario_report.status != "passed_structural":
            conversation_report.stopped_at_turn = index
            break
        conversation_report.turns_passed += 1
        state.apply_validated_turn(scenario_report, turn.user_text)

    conversation_report.final_state = dict(state.snapshot)
    conversation_report.full_transcript = [
        {"role": item.role, "text": item.text} for item in state.transcript
    ]
    if base_dir is not None:
        base_dir.mkdir(parents=True, exist_ok=True)
        (base_dir / "conversation-summary.json").write_text(
            json.dumps(
                {
                    "turns_total": len(active_script),
                    "turns_passed": conversation_report.turns_passed,
                    "stopped_at_turn": conversation_report.stopped_at_turn,
                    "total_model_operations": (
                        conversation_report.total_model_operations
                    ),
                    "total_cost_usd": round(conversation_report.total_cost_usd, 6),
                    "final_state": conversation_report.final_state,
                    "transcript": conversation_report.full_transcript,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
    return conversation_report


def diagnostic_keys_answered(state: dict[str, Any]) -> list[str]:
    ledger = (state.get("diagnostic") or {}).get("ledger") or {}
    return [
        key
        for key in REQUIRED_DIAGNOSTIC_KEYS
        if isinstance(ledger.get(key), dict)
        and ledger[key].get("status") in {"answered", "inferred_from_prior_message"}
    ]


__all__ = [
    "IDEAL_CONVERSATION_SCRIPT",
    "ConversationState",
    "ConversationTurnScript",
    "IdealConversationReport",
    "REQUIRED_DIAGNOSTIC_KEYS",
    "diagnostic_keys_answered",
    "run_ideal_conversation",
]
