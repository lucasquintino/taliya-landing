"""T012-030D tests: SDK agents rewired to the action-first contract."""

from __future__ import annotations

import pytest
from agents import AgentOutputSchema, RunConfig, Runner, set_tracing_disabled

from app.core.taliya_commercial_sdk.action_agents import (
    ACTION_AGENT_ORDER,
    STARTING_AGENT_BY_MODE,
    build_action_first_agents,
    starting_agent_name_for,
)
from app.core.taliya_commercial_sdk.agents import (
    DIAGNOSTIC_AGENT,
    PRODUCT_AGENT,
    TRIAGE_AGENT,
)
from app.core.taliya_commercial_sdk.conductor_decision import (
    ConductorActionDecision,
)
from app.core.taliya_commercial_sdk.decision_compiler import compile_action_decision
from app.core.taliya_commercial_sdk.turn_situation import build_turn_situation
from tests.test_spec012_sdk_paid_harness_dry_run import (
    ScriptedFakeModel,
    _function_call,
    _message,
)


def test_action_first_agents_use_conductor_decision_and_no_tools() -> None:
    agents_by_name = build_action_first_agents(model="gpt-test-no-call")

    assert list(agents_by_name) == ACTION_AGENT_ORDER
    for name, agent in agents_by_name.items():
        assert agent.output_type is ConductorActionDecision, name
        assert agent.tools == [], name
    AgentOutputSchema(ConductorActionDecision)

    triage = agents_by_name[TRIAGE_AGENT]
    assert triage.model_settings.tool_choice == "required"
    assert triage.model_settings.reasoning.effort == "none"
    assert [handoff.name for handoff in triage.handoffs] == ACTION_AGENT_ORDER[1:]
    # Specialists do not hand off: the per-turn mode already routed them.
    for name in ACTION_AGENT_ORDER[1:]:
        assert agents_by_name[name].handoffs == [], name
        assert agents_by_name[name].model_settings.reasoning.effort == "none", name


def test_starting_agent_is_deterministic_from_mode() -> None:
    price = build_turn_situation(
        state_snapshot={"canonical_state": "price_question"}, channel="whatsapp"
    )
    assert starting_agent_name_for(price) == PRODUCT_AGENT

    diagnostic = build_turn_situation(
        state_snapshot={"diagnostic": {"status": "in_progress", "ledger": {}}},
        channel="whatsapp",
    )
    assert starting_agent_name_for(diagnostic) == DIAGNOSTIC_AGENT

    entry = build_turn_situation(state_snapshot={}, channel="widget")
    assert starting_agent_name_for(entry) == TRIAGE_AGENT

    deferred = build_turn_situation(
        state_snapshot={"delivery": {"status": "delivering", "chunks_remaining": 1}},
        channel="whatsapp",
    )
    assert starting_agent_name_for(deferred) is None

    human_active = build_turn_situation(
        state_snapshot={"human_status": "active"}, channel="whatsapp"
    )
    assert starting_agent_name_for(human_active) is None

    assert set(STARTING_AGENT_BY_MODE) == {
        "entry",
        "diagnostic",
        "post_diagnostic",
        "product",
        "price",
        "demo",
        "waitlist",
        "handoff",
        "safety",
        "delivery_deferred",
    }


def test_instructions_carry_the_action_first_contract() -> None:
    agents_by_name = build_action_first_agents(model="gpt-test-no-call")
    for agent in agents_by_name.values():
        text = agent.instructions.lower()
        assert "exactly one action" in text
        assert "current inbound message" in text
        if agent.name != TRIAGE_AGENT:
            assert "never repeat" in text
        assert "you never output final customer text" in text
        assert "regex" not in text


def test_instructions_carry_delta_refusal_objection_and_resume_policy() -> None:
    agents_by_name = build_action_first_agents(model="gpt-test-no-call")
    product_text = agents_by_name[PRODUCT_AGENT].instructions.lower()
    diagnostic_text = agents_by_name[DIAGNOSTIC_AGENT].instructions.lower()
    waitlist_text = agents_by_name["taliya_waitlist_agent"].instructions.lower()

    assert "general objections" in product_text
    assert "conversation_resume" in product_text
    assert "post_diagnostic_context" in product_text
    assert "never restart the diagnostic" in product_text
    assert "respect_diagnostic_refusal" in diagnostic_text
    assert "do not compose answer_feedback" in diagnostic_text
    assert "runtime renders the approved short acknowledgement" in diagnostic_text
    assert "not a repeat of the lead's sentence" in agents_by_name[
        "taliya_entry_agent"
    ].instructions.lower()
    assert "do not offer diagnostic again in the same turn" in diagnostic_text
    assert "after a price answer" in product_text
    assert "budget or value concern" in product_text
    assert "wants to understand first" in waitlist_text
    assert "do not collect details" in waitlist_text


@pytest.mark.asyncio
async def test_no_cost_end_to_end_board_to_compiled_turn() -> None:
    """Fake model through the real Runner: board -> decision -> compiled turn."""

    set_tracing_disabled(True)
    situation = build_turn_situation(
        state_snapshot={"canonical_state": "new_lead"}, channel="whatsapp"
    )
    assert starting_agent_name_for(situation) == TRIAGE_AGENT

    decision_json = ConductorActionDecision.model_validate(
        {
            "selected_action": "answer_price",
            "interpreted_intents": ["price"],
            "direct_question": "quanto custa?",
            "product_fact_keys_used": ["prices"],
            "evidence": ["inbound.text"],
        }
    ).model_dump_json()
    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [_message(decision_json)],
        ]
    )
    agents_by_name = build_action_first_agents(model=fake_model)

    result = await Runner.run(
        agents_by_name[TRIAGE_AGENT],
        [
            {"role": "system", "content": situation.to_preamble()},
            {"role": "user", "content": "quanto custa?"},
        ],
        max_turns=2,
        run_config=RunConfig(tracing_disabled=True),
    )

    decision = result.final_output
    assert isinstance(decision, ConductorActionDecision)
    # Entry-mode menu includes the product answer action the router reached.
    compiled = compile_action_decision(
        decision,
        build_turn_situation(
            state_snapshot={"canonical_state": "price_question"}, channel="whatsapp"
        ),
        official_facts={
            "plan_price_summary": {
                "kind": "long_text",
                "value": "Base R$ 197/mes ate Completo R$ 1.497/mes.",
                "source": "official_product_knowledge",
                "evidence": ["product_knowledge.prices"],
                "max_length": 360,
            }
        },
    )
    assert compiled.ok, compiled.issues
    assert compiled.template_ids == ("product.price_direct", "diagnostic.price_hook")
    assert fake_model.calls == 2
