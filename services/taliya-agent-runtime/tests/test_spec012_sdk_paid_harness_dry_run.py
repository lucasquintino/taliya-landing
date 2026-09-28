from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from agents import AgentOutputSchema
from agents.exceptions import UserError
from agents.items import ModelResponse
from agents.models.interface import Model
from agents.usage import Usage
from openai.types.responses import (
    ResponseFunctionToolCall,
    ResponseOutputMessage,
    ResponseOutputText,
)

from app.core.taliya_commercial_sdk import (
    DIAGNOSTIC_AGENT,
    DRY_RUN_MODEL_NAME,
    FROZEN_SCENARIO_IDS,
    MODEL_PRICING_USD_PER_MILLION,
    PRODUCT_AGENT,
    SdkSpikePaidCallBlocked,
    SpikeBudget,
    SpikePreconditionError,
    TaliyaSdkTurnOutput,
    TaliyaTurnProposal,
    build_sdk_agents,
    estimate_cost_usd,
    frozen_scenario_ids,
    get_frozen_scenario,
    load_frozen_spike_scenarios,
    run_spike_scenarios,
)


class ScriptedFakeModel(Model):
    """No-cost scripted SDK model for the T012-026B dry-run gate.

    Each scripted step is one model operation; the harness must measure usage
    from the runner, so each step reports fixed token counts.
    """

    spike_model_name = DRY_RUN_MODEL_NAME

    def __init__(
        self,
        script: list[list[Any]],
        *,
        input_tokens_per_call: int = 1000,
        output_tokens_per_call: int = 200,
    ) -> None:
        self._script = list(script)
        self._input_tokens = input_tokens_per_call
        self._output_tokens = output_tokens_per_call
        self.calls = 0

    async def get_response(
        self,
        system_instructions,
        input,
        model_settings,
        tools,
        output_schema,
        handoffs,
        tracing,
        *,
        previous_response_id,
        conversation_id,
        prompt,
    ) -> ModelResponse:
        if not self._script:
            raise AssertionError("ScriptedFakeModel ran out of scripted responses")
        self.calls += 1
        return ModelResponse(
            output=self._script.pop(0),
            usage=Usage(
                requests=1,
                input_tokens=self._input_tokens,
                output_tokens=self._output_tokens,
                total_tokens=self._input_tokens + self._output_tokens,
            ),
            response_id=None,
        )

    def stream_response(self, *args: Any, **kwargs: Any):
        raise NotImplementedError("dry-run fake model does not stream")


def _message(text: str) -> ResponseOutputMessage:
    return ResponseOutputMessage(
        id="msg_dry_run",
        content=[ResponseOutputText(annotations=[], text=text, type="output_text")],
        role="assistant",
        status="completed",
        type="message",
    )


def _function_call(name: str, arguments: str = "{}") -> ResponseFunctionToolCall:
    return ResponseFunctionToolCall(
        id="fc_dry_run",
        call_id=f"call_{name}",
        name=name,
        arguments=arguments,
        type="function_call",
        status="completed",
    )


def _price_first_structured_output() -> TaliyaSdkTurnOutput:
    return TaliyaSdkTurnOutput.model_validate(
        {
            "commercial_understanding": {
                "intents": ["price_question"],
                "direct_question": "quanto custa?",
                "mixed_intent": False,
                "evidence": ["inbound.text"],
            },
            "answer_obligations": [
                {
                    "obligation": "answer_price_before_diagnostic",
                    "answering_template_id": "product.price_direct",
                    "evidence": ["inbound.text"],
                }
            ],
            "product_claims": [
                {
                    "claim": "price summary uses official plan facts",
                    "fact_refs": ["product_knowledge.prices"],
                    "evidence": ["product_knowledge.prices"],
                }
            ],
            "template_plan": {
                "template_ids": ["product.price_direct"],
                "variables": [
                    {
                        "name": "plan_price_summary",
                        "kind": "long_text",
                        "value": (
                            "Os planos oficiais comecam no Base R$ 197/mes e chegam "
                            "ao Essencial R$ 497/mes, conforme escopo contratado."
                        ),
                        "source": "official_product_knowledge",
                        "evidence": ["product_knowledge.prices"],
                        "max_length": 360,
                    }
                ],
                "evidence": ["template_registry.product.price_direct"],
            },
            "delivery": {"chunk_policy": "whatsapp_max_3"},
            "confidence": "high",
        }
    )


def _diagnostic_120_structured_output() -> TaliyaSdkTurnOutput:
    return TaliyaSdkTurnOutput.model_validate(
        {
            "commercial_understanding": {
                "intents": ["diagnostic_answer"],
                "mixed_intent": False,
                "extracted_facts": [
                    {
                        "key": "numeric_interpretation",
                        "kind": "student_count",
                        "raw_text": "120",
                        "value_text": "120",
                        "evidence": ["inbound.text"],
                    }
                ],
                "evidence": ["inbound.text"],
            },
            "diagnostic_proposal": {
                "ledger_updates": [
                    {
                        "question_key": "active_students_or_size",
                        "status": "answered",
                        "answer_value": "120",
                        "evidence": ["inbound.text"],
                    }
                ],
                "next_question_key": "main_pain",
                "final_diagnostic_ready": False,
                "evidence": ["inbound.text"],
            },
            "template_plan": {
                "template_ids": ["diagnostic.ask_main_pain"],
                "variables": [
                    {
                        "name": "answer_feedback",
                        "kind": "short_text",
                        "value": (
                            "Entendi: com 120 alunos ativos, ja existe volume para "
                            "organizar atendimento com mais criterio."
                        ),
                        "source": "diagnostic_ledger",
                        "evidence": ["diagnostic_ledger.active_students_or_size"],
                        "max_length": 180,
                    }
                ],
                "evidence": ["template_registry.diagnostic.ask_main_pain"],
            },
            "delivery": {"chunk_policy": "whatsapp_max_3"},
            "confidence": "high",
        }
    )


def test_spec012_strict_output_schema_is_sdk_compatible() -> None:
    AgentOutputSchema(TaliyaSdkTurnOutput)

    with pytest.raises(UserError):
        AgentOutputSchema(TaliyaTurnProposal)


def test_spec012_agents_declare_strict_structured_output_type() -> None:
    agents_by_name = build_sdk_agents(model="gpt-test-no-call")

    for agent in agents_by_name.values():
        assert agent.output_type is TaliyaSdkTurnOutput


def test_spec012_frozen_scenarios_match_approval_packet() -> None:
    scenarios = load_frozen_spike_scenarios()

    assert tuple(frozen_scenario_ids(scenarios)) == FROZEN_SCENARIO_IDS
    assert [scenario.number for scenario in scenarios] == list(range(1, 16))
    assert scenarios[0].channel == "widget"
    assert all(scenario.channel == "whatsapp" for scenario in scenarios[1:])

    multi_turn_required = {
        "diagnostic_numeric_120",
        "diagnostic_urgency_final",
        "waitlist_contract_intent",
        "delivery_concurrency",
    }
    for scenario_id in multi_turn_required:
        scenario = get_frozen_scenario(scenario_id)
        assert scenario.prior_transcript, scenario_id
        assert scenario.state_snapshot, scenario_id

    urgency = get_frozen_scenario("diagnostic_urgency_final")
    ledger = urgency.state_snapshot["diagnostic"]["ledger"]
    assert ledger["urgency"]["status"] == "pending"
    assert all(
        ledger[key]["status"] == "answered"
        for key in ledger
        if key != "urgency"
    )


@pytest.mark.asyncio
async def test_spec012_dry_run_full_real_runner_path(tmp_path: Path) -> None:
    scenario = get_frozen_scenario("price_first")
    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [_function_call("get_product_knowledge", json.dumps({"keys": ["prices"]}))],
            [_message(_price_first_structured_output().model_dump_json())],
        ],
        input_tokens_per_call=1234,
        output_tokens_per_call=567,
    )

    report = await run_spike_scenarios(
        model=fake_model,
        scenarios=[scenario],
        report_dir=tmp_path,
    )

    assert report.proof_type == "mocked_dry_run"
    assert report.paid_call_status == "not_run"
    assert report.tracing_disabled is True
    assert report.public_cutover is False
    assert report.aborted is False
    assert fake_model.calls == 3

    [scenario_report] = report.scenario_reports
    assert scenario_report.status == "passed_structural"
    assert scenario_report.usage["model"] == DRY_RUN_MODEL_NAME
    assert scenario_report.usage["model_operations"] == 3
    assert scenario_report.usage["input_tokens"] == 3 * 1234
    assert scenario_report.usage["output_tokens"] == 3 * 567
    assert scenario_report.usage["cost_usd"] == 0
    assert scenario_report.rendered_preview
    assert all(message["text"].strip() for message in scenario_report.rendered_preview)

    path_events = {item["event"] for item in scenario_report.agent_path}
    assert {"start", "handoff", "tool", "final"} <= path_events
    tool_events = [
        call for call in scenario_report.tool_calls if call["event"] == "tool_call"
    ]
    assert any(call["name"] == "get_product_knowledge" for call in tool_events)
    handoff_events = [
        call for call in scenario_report.tool_calls if call["event"] == "handoff"
    ]
    assert any(call["to_agent"] == PRODUCT_AGENT for call in handoff_events)

    assert (tmp_path / "spike-run-report.json").exists()
    assert (tmp_path / "spike-run-report.md").exists()
    assert (tmp_path / "scenario-03-price_first.json").exists()
    summary = json.loads(
        (tmp_path / "spike-run-report.json").read_text(encoding="utf-8")
    )
    assert summary["tracing_disabled"] is True
    assert summary["total_cost_usd"] == 0


@pytest.mark.asyncio
async def test_spec012_dry_run_state_snapshot_reaches_tools_via_run_context() -> None:
    scenario = get_frozen_scenario("diagnostic_numeric_120")
    fake_model = ScriptedFakeModel(
        [
            [_function_call("get_diagnostic_ledger")],
            [_message(_diagnostic_120_structured_output().model_dump_json())],
        ]
    )

    report = await run_spike_scenarios(model=fake_model, scenarios=[scenario])

    [scenario_report] = report.scenario_reports
    assert scenario_report.status == "passed_structural"
    # Persisted current agent skips the triage handoff turn entirely.
    assert scenario_report.starting_agent == DIAGNOSTIC_AGENT
    assert scenario_report.usage["model_operations"] == 2
    tool_outputs = [
        call for call in scenario_report.tool_calls if call["event"] == "tool_output"
    ]
    assert tool_outputs, "ledger tool output must be recorded"
    ledger_payload = json.dumps(tool_outputs)
    assert "active_students_or_size" in ledger_payload
    assert "run_context_snapshot" in ledger_payload

    proposal = scenario_report.turn_proposal
    facts = proposal["commercial_understanding"]["extracted_facts"]
    assert facts == [
        {
            "key": "numeric_interpretation",
            "kind": "student_count",
            "raw_text": "120",
            "value": 120,
            "evidence": ["inbound.text"],
        }
    ]


@pytest.mark.asyncio
async def test_spec012_dry_run_single_repair_operation_recovers_validator_failure() -> None:
    scenario = get_frozen_scenario("price_first")
    broken_output = _price_first_structured_output().model_copy(deep=True)
    broken_output.answer_obligations[0].answering_template_id = None
    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [_message(broken_output.model_dump_json())],
            # Design-lock repair: one extra operation with validator feedback.
            [_message(_price_first_structured_output().model_dump_json())],
        ]
    )

    report = await run_spike_scenarios(model=fake_model, scenarios=[scenario])

    [scenario_report] = report.scenario_reports
    assert scenario_report.status == "passed_structural"
    assert scenario_report.usage["repairs"] == 1
    assert scenario_report.usage["model_operations"] == 3
    assert fake_model.calls == 3


@pytest.mark.asyncio
async def test_spec012_dry_run_repair_respects_per_scenario_operation_cap() -> None:
    scenario = get_frozen_scenario("price_first")
    broken_output = _price_first_structured_output().model_copy(deep=True)
    broken_output.answer_obligations[0].answering_template_id = None
    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [_function_call("get_product_knowledge", json.dumps({"keys": ["prices"]}))],
            [_message(broken_output.model_dump_json())],
        ]
    )

    report = await run_spike_scenarios(model=fake_model, scenarios=[scenario])

    [scenario_report] = report.scenario_reports
    # 3 operations already used: no room for the repair inside the cap.
    assert scenario_report.status == "failed"
    assert scenario_report.usage["repairs"] == 0
    assert fake_model.calls == 3


def test_spec012_validator_allows_unanswered_question_during_delivery_deferral() -> None:
    from app.core.taliya_commercial_sdk import validate_and_render_spike_output

    proposal = TaliyaTurnProposal.model_validate(
        {
            "turn_id": "turn_defer",
            "conversation_id": "conv_defer",
            "channel": "whatsapp",
            "starting_agent": "taliya_triage_agent",
            "agent_path": [
                {"event": "start", "agent": "taliya_triage_agent"},
                {
                    "event": "handoff",
                    "from_agent": "taliya_triage_agent",
                    "to_agent": "taliya_handoff_agent",
                },
                {"event": "final", "agent": "taliya_handoff_agent"},
            ],
            "commercial_understanding": {
                "intents": ["delivery_concurrency"],
                "direct_question": "voces atendem studios pequenos?",
                "evidence": ["inbound.text"],
            },
            "answer_obligations": [
                {
                    "obligation": "answer_small_studio_question_after_delivery",
                    "answered_before_steering": False,
                    "evidence": ["inbound.text"],
                }
            ],
            "template_proposal": {
                "template_ids": ["handoff.paused"],
                "variables": {},
                "evidence": ["template_registry.handoff.paused"],
            },
            "state_patch_proposal": {
                "delivery": {
                    "defer_inbound_during_chunks": True,
                    "deferred_inbound_count": 1,
                }
            },
            "delivery_proposal": {
                "chunk_policy": "whatsapp_max_3",
                "render_plan_only": True,
                "evidence": ["template_registry.handoff.paused"],
            },
        }
    )

    validated = validate_and_render_spike_output(proposal)

    assert validated.validator_result.status == "passed"


def test_spec012_diagnostic_sequence_guardrail_is_deterministic() -> None:
    from app.core.taliya_commercial_sdk import validate_and_render_spike_output

    base = _diagnostic_120_structured_output()
    proposal_payload = {
        "schema_version": "012.turn_proposal.v1",
        "turn_id": "turn_seq",
        "conversation_id": "conv_seq",
        "channel": "whatsapp",
        "starting_agent": "taliya_diagnostic_agent",
        "agent_path": [
            {"event": "start", "agent": "taliya_diagnostic_agent"},
            {"event": "final", "agent": "taliya_diagnostic_agent"},
        ],
        "commercial_understanding": {
            "intents": ["diagnostic_answer"],
            "evidence": ["inbound.text"],
        },
    }
    from app.core.taliya_commercial_sdk.sdk_output_model import (
        sdk_turn_output_to_proposal_fields,
    )

    fields = sdk_turn_output_to_proposal_fields(base)
    state = {
        "diagnostic": {
            "status": "in_progress",
            "next_question_key": "active_students_or_size",
            "ledger": {},
        }
    }

    # Correct sequence: 120 answers active_students, next is main_pain.
    good = TaliyaTurnProposal.model_validate({**proposal_payload, **fields})
    assert (
        validate_and_render_spike_output(good, state_snapshot=state)
        .validator_result.status
        == "passed"
    )

    # Wrong next question (skipping ahead) is blocked deterministically.
    skipped = base.model_copy(deep=True)
    skipped.diagnostic_proposal.next_question_key = "urgency"
    skipped.template_plan.template_ids = ["diagnostic.ask_urgency"]
    bad_fields = sdk_turn_output_to_proposal_fields(skipped)
    bad = TaliyaTurnProposal.model_validate({**proposal_payload, **bad_fields})
    result = validate_and_render_spike_output(bad, state_snapshot=state)
    codes = [issue.code for issue in result.validator_result.errors]
    assert "sdk_diagnostic_wrong_next_question" in codes

    # Delivering before all six keys are complete is blocked.
    premature = base.model_copy(deep=True)
    premature.diagnostic_proposal.next_question_key = None
    premature.diagnostic_proposal.final_diagnostic_ready = True
    premature.template_plan.template_ids = ["diagnostic.deliver"]
    premature_fields = sdk_turn_output_to_proposal_fields(premature)
    bad2 = TaliyaTurnProposal.model_validate({**proposal_payload, **premature_fields})
    result2 = validate_and_render_spike_output(bad2, state_snapshot=state)
    codes2 = [issue.code for issue in result2.validator_result.errors]
    assert "sdk_diagnostic_premature_completion" in codes2

    # Recording an answer without feedback before the next question is blocked.
    no_feedback = base.model_copy(deep=True)
    no_feedback.template_plan.variables = []
    nf_fields = sdk_turn_output_to_proposal_fields(no_feedback)
    bad3 = TaliyaTurnProposal.model_validate({**proposal_payload, **nf_fields})
    result3 = validate_and_render_spike_output(bad3, state_snapshot=state)
    codes3 = [issue.code for issue in result3.validator_result.errors]
    assert "sdk_diagnostic_feedback_missing" in codes3


@pytest.mark.asyncio
async def test_spec012_dry_run_free_form_output_aborts_run() -> None:
    scenario = get_frozen_scenario("price_first")
    fake_model = ScriptedFakeModel(
        [[_message("Oi! Os planos custam a partir de R$ 197/mes...")]]
    )

    report = await run_spike_scenarios(model=fake_model, scenarios=[scenario])

    assert report.aborted is True
    assert "sdk_output_not_structured" in (report.abort_reason or "")
    [scenario_report] = report.scenario_reports
    assert scenario_report.status == "aborted"


@pytest.mark.asyncio
async def test_spec012_dry_run_budget_meter_stops_before_ceiling() -> None:
    first = get_frozen_scenario("price_first")
    second = get_frozen_scenario("pain_first")
    fake_model = ScriptedFakeModel(
        [
            [_function_call("transfer_to_taliya_product_agent")],
            [_function_call("get_product_knowledge", json.dumps({"keys": ["prices"]}))],
            [_message(_price_first_structured_output().model_dump_json())],
        ]
    )

    report = await run_spike_scenarios(
        model=fake_model,
        scenarios=[first, second],
        budget=SpikeBudget(
            max_total_model_operations=3,
            max_total_cost_usd=1.00,
            max_model_operations_per_scenario=3,
        ),
    )

    assert report.aborted is True
    assert "model_operation_ceiling" in (report.abort_reason or "")
    assert len(report.scenario_reports) == 1
    assert report.total_model_operations == 3


@pytest.mark.asyncio
async def test_spec012_paid_run_remains_blocked_without_explicit_approval() -> None:
    with pytest.raises(SdkSpikePaidCallBlocked):
        await run_spike_scenarios(model="gpt-5.4-mini")


def test_spec012_luna_pricing_is_recorded_and_cache_aware() -> None:
    assert MODEL_PRICING_USD_PER_MILLION["gpt-5.6-luna"] == {
        "input": 1.00,
        "cached_input": 0.10,
        "cache_write_input": 1.25,
        "output": 6.00,
    }
    assert estimate_cost_usd(
        "gpt-5.6-luna",
        input_tokens=1_000_000,
        cached_input_tokens=500_000,
        cache_write_input_tokens=0,
        output_tokens=1_000_000,
    ) == pytest.approx(6.55)

    assert estimate_cost_usd(
        "gpt-5.6-luna",
        input_tokens=1_000_000,
        cached_input_tokens=250_000,
        cache_write_input_tokens=500_000,
        output_tokens=1_000_000,
    ) == pytest.approx(6.9)


@pytest.mark.asyncio
async def test_spec012_paid_run_preconditions_block_unpriced_model_and_missing_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    approval = {"paid_openai_approved": True}

    with pytest.raises(SpikePreconditionError, match="pricing"):
        await run_spike_scenarios(model="gpt-unpriced-model", **approval)

    api_key_env = "OPENAI" + "_API_KEY"
    monkeypatch.delenv(api_key_env, raising=False)
    with pytest.raises(SpikePreconditionError, match=api_key_env):
        await run_spike_scenarios(model="gpt-5.4-mini", **approval)


def test_spec012_agent_instructions_embed_official_template_catalog() -> None:
    from app.core.taliya_commercial.template_registry import TEMPLATE_REGISTRY
    from app.core.taliya_commercial_sdk.agents import (
        AGENT_TEMPLATE_PREFIXES,
        build_sdk_agent_specs,
    )

    specs = build_sdk_agent_specs()
    assert "product.price_direct" in specs[PRODUCT_AGENT].instructions
    assert "diagnostic.ask_active_students" in specs[DIAGNOSTIC_AGENT].instructions
    assert "plan_price_summary" in specs[PRODUCT_AGENT].instructions

    for agent_name, prefixes in AGENT_TEMPLATE_PREFIXES.items():
        instructions = specs[agent_name].instructions
        listed = [
            template_id
            for template_id in TEMPLATE_REGISTRY
            if any(template_id.startswith(prefix) for prefix in prefixes)
        ]
        assert listed, agent_name
        for template_id in listed:
            assert template_id in instructions, (agent_name, template_id)


def test_spec012_template_variables_normalize_to_official_registry_spec() -> None:
    from app.core.taliya_commercial_sdk.sdk_output_model import (
        SdkTemplateVariable,
        _normalized_template_variable,
    )

    # Model omitted max_length and declared the wrong kind for a registry
    # variable: the canonical rendering spec wins.
    normalized = _normalized_template_variable(
        SdkTemplateVariable(
            name="answer_feedback",
            kind="long_text",
            value="Entendi: 120 alunos ativos.",
            source="diagnostic_ledger",
            evidence=["diagnostic_ledger.active_students_or_size"],
        )
    )
    assert normalized["kind"] == "short_text"
    assert normalized["max_length"] == 180

    # Pure lead-context variables (no official source allowed): a disallowed
    # label is bookkeeping, normalized to the first allowed source.
    context_var = _normalized_template_variable(
        SdkTemplateVariable(
            name="answer_feedback",
            kind="short_text",
            value="texto",
            source="model_decision",
            evidence=["x"],
        )
    )
    assert context_var["source"] == "user_message"

    # Variables that can carry official product facts: the declared source is
    # NEVER coerced - a wrong label must fail validation, not be masked.
    fact_var = _normalized_template_variable(
        SdkTemplateVariable(
            name="recommended_plan_or_range",
            kind="short_text",
            value="Essencial",
            source="model_decision",
            evidence=["x"],
        )
    )
    assert fact_var["source"] == "model_decision"

    # Unknown variables pass through untouched for the validator to judge.
    unknown = _normalized_template_variable(
        SdkTemplateVariable(
            name="not_in_registry",
            kind="short_text",
            value="texto",
            source="user_message",
            evidence=["x"],
        )
    )
    assert unknown["kind"] == "short_text"
    assert "max_length" not in unknown


def test_spec012_harness_keeps_public_runtime_isolated() -> None:
    import inspect

    import app.main as runtime_main

    main_source = inspect.getsource(runtime_main)
    assert "run_action_first_agent_turn" in main_source
    assert "spec012_action_first_enabled" not in main_source
    assert "run_spec011_agent_turn" not in main_source
    assert "paid_spike_harness" not in main_source
