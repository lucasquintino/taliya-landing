from pathlib import Path

from app.domains.taliya_commercial.agents import get_taliya_agent_manifest


def test_reference_file_structure_is_present():
    root = Path(__file__).resolve().parents[1] / "app" / "domains" / "taliya_commercial"

    for name in ["agents.py", "tools.py", "guardrails.py", "context.py", "prompts.py", "behavior_policy.py"]:
        assert (root / name).exists(), name


def test_taliya_manifest_has_triage_specialists_tools_guardrails_and_handoffs():
    manifest = get_taliya_agent_manifest()

    assert manifest["entry_agent"] == "taliya_commercial_triage"
    agent_names = {agent["name"] for agent in manifest["agents"]}
    assert {
        "taliya_commercial_triage",
        "taliya_commercial_entry_agent",
        "taliya_commercial_product_agent",
        "taliya_commercial_diagnostic_agent",
        "taliya_commercial_waitlist_agent",
        "taliya_commercial_handoff_agent",
    }.issubset(agent_names)
    triage = next(agent for agent in manifest["agents"] if agent["name"] == "taliya_commercial_triage")
    assert "taliya_commercial_product_agent" in triage["handoffs"]
    assert "get_product_knowledge" in triage["tools"]
    assert "prompt_injection_guardrail" in triage["input_guardrails"]


def test_non_mock_runtime_path_uses_openai_agents_runner():
    runner = (Path(__file__).resolve().parents[1] / "app" / "runtime" / "runner.py").read_text()

    assert "Runner.run" in runner
    assert 'if provider != "mock"' in runner
    assert "output_type=AgentOutputSchema(LLMStructuredDraft" in runner

