from __future__ import annotations

import inspect
import json
from types import SimpleNamespace

import pytest

from app.core.taliya_commercial_sdk import (
    COMMIT_TOOL_NAMES,
    DIAGNOSTIC_AGENT,
    ENTRY_AGENT,
    HANDOFF_AGENT,
    PRODUCT_AGENT,
    PROPOSAL_ONLY_TOOL_NAMES,
    READ_ONLY_TOOL_NAMES,
    TRIAGE_AGENT,
    WAITLIST_AGENT,
    build_sdk_agent_specs,
    build_sdk_agents,
    get_sdk_agent_manifest,
    get_sdk_tool_names,
    get_sdk_tools,
)


def test_spec012_minimal_sdk_agent_topology_matches_design_lock() -> None:
    specs = build_sdk_agent_specs()

    assert list(specs) == [
        TRIAGE_AGENT,
        ENTRY_AGENT,
        PRODUCT_AGENT,
        DIAGNOSTIC_AGENT,
        WAITLIST_AGENT,
        HANDOFF_AGENT,
    ]
    assert specs[TRIAGE_AGENT].handoffs == (
        ENTRY_AGENT,
        PRODUCT_AGENT,
        DIAGNOSTIC_AGENT,
        WAITLIST_AGENT,
        HANDOFF_AGENT,
    )
    assert specs[ENTRY_AGENT].handoffs == (
        PRODUCT_AGENT,
        DIAGNOSTIC_AGENT,
        WAITLIST_AGENT,
        HANDOFF_AGENT,
    )
    assert specs[PRODUCT_AGENT].handoffs == (
        DIAGNOSTIC_AGENT,
        WAITLIST_AGENT,
        HANDOFF_AGENT,
        TRIAGE_AGENT,
    )
    assert specs[DIAGNOSTIC_AGENT].handoffs == (
        PRODUCT_AGENT,
        WAITLIST_AGENT,
        HANDOFF_AGENT,
        TRIAGE_AGENT,
    )
    assert specs[WAITLIST_AGENT].handoffs == (
        PRODUCT_AGENT,
        DIAGNOSTIC_AGENT,
        HANDOFF_AGENT,
        TRIAGE_AGENT,
    )
    assert specs[HANDOFF_AGENT].handoffs == ()


def test_spec012_agent_instructions_preserve_llm_first_boundaries() -> None:
    manifest = get_sdk_agent_manifest()
    instructions_by_agent = {
        agent["name"]: agent["instructions"]
        for agent in manifest["agents"]
    }
    all_instructions = "\n".join(instructions_by_agent.values()).lower()

    for required in [
        "llm is the commercial understanding brain",
        "do not classify price",
        "mixed-intent",
        "do not deliver a final",
        "official product knowledge",
        "approved templates",
        "checkout links",
        "discounts",
        "client/studio whatsapp",
    ]:
        assert required in all_instructions

    assert "regex" not in all_instructions
    assert "if user says" not in all_instructions
    assert "contains(" not in all_instructions

    assert "answer direct questions first" in instructions_by_agent[PRODUCT_AGENT].lower()
    assert "accept simple answers such as \"120\"" in instructions_by_agent[
        DIAGNOSTIC_AGENT
    ].lower()
    assert "distinguish curiosity from buying intent" in instructions_by_agent[
        WAITLIST_AGENT
    ].lower()
    assert "propose that ai should pause" in instructions_by_agent[HANDOFF_AGENT].lower()


def test_spec012_builds_real_sdk_agents_with_sdk_tools_and_without_paid_run() -> None:
    agents = build_sdk_agents(model="gpt-test-no-call")

    assert set(agents) == {
        TRIAGE_AGENT,
        ENTRY_AGENT,
        PRODUCT_AGENT,
        DIAGNOSTIC_AGENT,
        WAITLIST_AGENT,
        HANDOFF_AGENT,
    }
    assert [agent.name for agent in agents[TRIAGE_AGENT].handoffs] == [
        ENTRY_AGENT,
        PRODUCT_AGENT,
        DIAGNOSTIC_AGENT,
        WAITLIST_AGENT,
        HANDOFF_AGENT,
    ]
    # Spike-evidence design revision (ideal-conversation runs 1-2): triage is
    # a pure router with no tools and required tool choice, so the only action
    # it can take is one handoff to a specialist of its semantic choice.
    assert [tool.name for tool in agents[TRIAGE_AGENT].tools] == []
    assert agents[TRIAGE_AGENT].model_settings.tool_choice == "required"
    assert [tool.name for tool in agents[PRODUCT_AGENT].tools] == get_sdk_tool_names()
    assert [tool.name for tool in agents[HANDOFF_AGENT].tools] == [
        "get_conversation_summary",
        "get_demo_waitlist_handoff_state",
        "propose_handoff",
        "propose_template_plan",
        "propose_sales_inbox_projection",
    ]
    assert agents[HANDOFF_AGENT].handoffs == []
    assert agents[PRODUCT_AGENT].model == "gpt-test-no-call"


def test_spec012_sdk_tool_catalog_matches_read_only_and_proposal_only_lock() -> None:
    assert COMMIT_TOOL_NAMES == ()
    assert get_sdk_tool_names() == [
        *READ_ONLY_TOOL_NAMES,
        *PROPOSAL_ONLY_TOOL_NAMES,
    ]
    tools_by_name = {tool.name: tool for tool in get_sdk_tools()}

    for name in READ_ONLY_TOOL_NAMES:
        assert name in tools_by_name
    for name in PROPOSAL_ONLY_TOOL_NAMES:
        assert name in tools_by_name

    for forbidden in [
        "save_lead_facts",
        "save_diagnostic_record",
        "mark_waitlist",
        "pause_for_human",
        "resume_from_human",
        "record_runtime_note",
    ]:
        assert forbidden not in tools_by_name


@pytest.mark.asyncio
async def test_spec012_sdk_tools_return_non_committing_envelopes() -> None:
    tools_by_name = {tool.name: tool for tool in get_sdk_tools()}

    product_tool = tools_by_name["get_product_knowledge"]
    product_result = await product_tool.on_invoke_tool(
        SimpleNamespace(tool_name=product_tool.name, run_config=None),
        json.dumps({"keys": ["prices", "checkout_status"]}),
    )
    assert product_result["side_effect_class"] == "read_only"
    assert product_result["commits_state"] is False
    assert product_result["renders_customer_response"] is False
    assert product_result["chooses_commercial_route"] is False
    assert product_result["payload"]["refs"]

    proposal_tool = tools_by_name["propose_waitlist_update"]
    proposal_result = await proposal_tool.on_invoke_tool(
        SimpleNamespace(tool_name=proposal_tool.name, run_config=None),
        json.dumps(
            {
                "update_json": json.dumps({"status": "candidate"}),
                "evidence": ["lead.explicit_next_step"],
                "uncertainty": "medium",
            }
        ),
    )
    assert proposal_result["side_effect_class"] == "proposal_only"
    assert proposal_result["commits_state"] is False
    assert proposal_result["payload"]["validation_required"] is True
    assert proposal_result["payload"]["commit_after_validation_only"] is True
    assert proposal_result["payload"]["missing_evidence"] is False


def test_spec012_sdk_tools_do_not_contain_commercial_shortcut_parser() -> None:
    import app.core.taliya_commercial_sdk.tools as sdk_tools

    source = inspect.getsource(sdk_tools)
    assert "import re" not in source
    assert "route_from_text" not in source
    assert "has_any_token" not in source
    assert "BUY_INTENT_TOKENS" not in source
    assert "DIRECT_QUESTION_TOKENS" not in source


def test_spec012_sdk_agents_are_not_imported_by_public_runtime_endpoint() -> None:
    import app.main as runtime_main

    main_source = inspect.getsource(runtime_main)
    assert "run_action_first_agent_turn" in main_source
    assert "spec012_action_first_enabled" not in main_source
    assert "run_spec011_agent_turn" not in main_source
    assert "paid_spike_harness" not in main_source
    assert "run_isolated_sdk_spike" not in main_source
