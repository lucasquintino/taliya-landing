from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SDK_DIR = (
    REPO_ROOT
    / "services"
    / "taliya-agent-runtime"
    / "app"
    / "core"
    / "taliya_commercial_sdk"
)
APP_DIR = REPO_ROOT / "services" / "taliya-agent-runtime" / "app"
NEXT_RUNTIME_CLIENT = REPO_ROOT / "lib" / "landing" / "ai-attendant" / "runtime-client.ts"
WHATSAPP_ROUTE = (
    REPO_ROOT / "app" / "api" / "landing" / "ai-attendant" / "whatsapp" / "route.ts"
)
COMMERCIAL_CORE_DIR = (
    REPO_ROOT
    / "services"
    / "taliya-agent-runtime"
    / "app"
    / "core"
    / "taliya_commercial"
)


def _source(relative: str) -> str:
    return (SDK_DIR / relative).read_text(encoding="utf-8")


def _between(source: str, start: str, end: str) -> str:
    start_index = source.index(start)
    end_index = source.index(end, start_index)
    return source[start_index:end_index]


def test_t012_037_next_runtime_turn_has_no_old_runner_public_fallback() -> None:
    source = NEXT_RUNTIME_CLIENT.read_text(encoding="utf-8")
    turn_function = _between(
        source,
        "export async function runTaliyaCommercialRuntimeTurn",
        "export function resolveTaliyaCommercialRuntimeEndpointPath",
    )
    runtime_path_function = _between(
        source,
        "export function resolveTaliyaCommercialRuntimeEndpointPath",
        "export async function syncTaliyaCommercialRuntimeHandoffState",
    )

    assert 'return "/v1/taliya-commercial/turn";' in runtime_path_function
    assert "resolveTaliyaCommercialRuntimeEndpointPath(request)" in turn_function
    assert "/v1/agent-runs" not in turn_function
    assert "createRuntimeMockResponse" not in turn_function
    assert "isSpec011CommercialCoreEnabled" not in source
    assert "TALIYA_SPEC011_COMMERCIAL_CORE_ENABLED" not in source

    forbidden_old_runner_fragments = (
        "agent-v2-loop",
        "agent-v2-semantic-interpreter",
        "agent-v2-diagnostic",
        "runAgentV2",
        "runFloatingAgent",
        "runLegacy",
        "fallbackCommercial",
    )
    violations = [
        fragment for fragment in forbidden_old_runner_fragments if fragment in source
    ]

    assert violations == []


def test_t012_037_whatsapp_route_delegates_to_runtime_not_ts_v2_engine() -> None:
    source = WHATSAPP_ROUTE.read_text(encoding="utf-8")
    agent_v2_imports = [
        line.strip()
        for line in source.splitlines()
        if line.strip().startswith("import") and "agent-v2" in line
    ]

    assert agent_v2_imports == [
        "import { completeAgentV2IdempotencyKey, "
        'reserveAgentV2IdempotencyKey } from "@/lib/landing/ai-attendant/'
        'agent-v2-idempotency";'
    ]
    assert (
        "import { runTaliyaCommercialRuntimeTurn as runAiAttendantTurn } "
        'from "@/lib/landing/ai-attendant/runtime-client";'
        in source
    )
    assert "response = await runAiAttendantTurn(requestPayload);" in source

    forbidden_old_runner_fragments = (
        "agent-v2-loop",
        "agent-v2-semantic-interpreter",
        "agent-v2-diagnostic",
        "runAgentV2",
        "runFloatingAgent",
        "runLegacy",
    )
    violations = [
        fragment for fragment in forbidden_old_runner_fragments if fragment in source
    ]

    assert violations == []


def test_t012_040_blocks_regex_as_commercial_brain_in_action_core() -> None:
    audited = {
        "turn_situation.py": _source("turn_situation.py"),
        "decision_compiler.py": _source("decision_compiler.py"),
        "action_agents.py": _source("action_agents.py"),
    }
    forbidden_fragments = (
        "import re",
        "from re import",
        "re.compile(",
        "re.search(",
        "re.match(",
        "re.fullmatch(",
        ".inbound.text",
        "message.text",
        "current_user_text",
        "regex",
    )

    violations = [
        f"{file_name}:{fragment}"
        for file_name, source in audited.items()
        for fragment in forbidden_fragments
        if fragment in source
    ]

    assert violations == []


def test_t012_040_sdk_tools_remain_read_only_or_proposal_only() -> None:
    source = _source("tools.py")

    assert "COMMIT_TOOL_NAMES: tuple[str, ...] = ()" in source
    assert '"commits_state": False' in source
    assert '"commit_after_validation_only": True' in source
    assert "def commit_" not in source
    assert "side_effect_class=\"commit" not in source


def test_t012_040_sdk_tools_cannot_commit_or_deliver_during_reasoning() -> None:
    source = _source("tools.py")
    module = ast.parse(source)

    exposed_tool_names = {
        node.name
        for node in module.body
        if isinstance(node, ast.FunctionDef)
        and any(
            isinstance(decorator, ast.Name) and decorator.id == "function_tool"
            for decorator in node.decorator_list
        )
    }
    expected_tool_names = {
        "get_product_knowledge",
        "get_spec006_product_contracts",
        "get_diagnostic_ledger",
        "get_conversation_summary",
        "get_demo_waitlist_handoff_state",
        "get_approved_template_catalog",
        "propose_diagnostic_update",
        "propose_waitlist_update",
        "propose_demo_state_update",
        "propose_handoff",
        "propose_template_plan",
        "propose_sales_inbox_projection",
    }

    assert exposed_tool_names == expected_tool_names
    assert all(
        name.startswith(("get_", "propose_")) for name in exposed_tool_names
    )

    forbidden_call_names = {
        "commit_state",
        "persist_state",
        "save_state",
        "upsert_state",
        "insert_state",
        "delete_state",
        "send_message",
        "deliver_message",
        "enqueue_message",
        "publish_message",
    }
    tool_body_violations: list[str] = []
    for node in module.body:
        if not isinstance(node, ast.FunctionDef) or node.name not in exposed_tool_names:
            continue
        for call in ast.walk(node):
            if not isinstance(call, ast.Call):
                continue
            func = call.func
            call_name = ""
            if isinstance(func, ast.Name):
                call_name = func.id
            elif isinstance(func, ast.Attribute):
                call_name = func.attr
            if call_name in forbidden_call_names:
                tool_body_violations.append(f"{node.name}:{call_name}")

    assert tool_body_violations == []


def test_t012_040_sdk_output_cannot_deliver_free_text_directly() -> None:
    output_schema = _source("output_schema.py")
    sdk_output_model = _source("sdk_output_model.py")

    assert "FORBIDDEN_DIRECT_OUTPUT_FIELDS" in output_schema
    assert "_reject_direct_output_fields(value)" in output_schema
    assert "final_text" not in sdk_output_model
    assert "freeform_response" not in sdk_output_model
    assert "assistant_message" not in sdk_output_model


def test_t012_040_isolated_runner_has_no_public_old_runner_fallback() -> None:
    runner = _source("action_turn_runner.py")
    spike_runner = _source("spike_runner.py")

    assert "app.runtime.runner" not in runner
    assert "app.runtime.runner" not in spike_runner
    assert "legacy" not in runner.casefold()
    assert "old runner" not in runner.casefold()
    assert "public fallback" not in runner.casefold()


def test_t012_040_sdk_path_is_the_only_public_commercial_runtime() -> None:
    violations: list[str] = []
    allowed = {
        "services/taliya-agent-runtime/app/main.py",
    }
    for path in APP_DIR.rglob("*.py"):
        if SDK_DIR in path.parents:
            continue
        source = path.read_text(encoding="utf-8")
        if "taliya_commercial_sdk" in source or "run_action_turn" in source:
            relative = str(path.relative_to(REPO_ROOT)).replace("\\", "/")
            if relative not in allowed:
                violations.append(relative)
            else:
                assert "run_action_first_agent_turn" in source
                assert "run_spec011_agent_turn" not in source
                assert "spec012_action_first_enabled" not in source
                assert "paid_spike_harness" not in source
                assert "run_isolated_sdk_spike" not in source

    assert violations == []


def test_t012_040_prompts_and_templates_do_not_hardcode_unsafe_promises() -> None:
    audited = {
        "action_agents.py": _source("action_agents.py"),
        "renderer.py": (COMMERCIAL_CORE_DIR / "renderer.py").read_text(
            encoding="utf-8"
        ),
    }
    forbidden_promise_fragments = (
        "checkout aberto",
        "checkout liberado",
        "link de pagamento",
        "pode pagar agora",
        "pagamento agora",
        "desconto garantido",
        "desconto especial",
        "acesso vip",
        "vaga garantida",
        "data garantida",
        "abertura garantida",
        "integracao garantida",
        "integração garantida",
        "migracao automatica",
        "migração automática",
        "setup automatico",
        "setup automático",
        "certificacao garantida",
        "certificação garantida",
        "criptografia garantida",
        "lgpd garantida",
    )

    violations = [
        f"{file_name}:{fragment}"
        for file_name, source in audited.items()
        for fragment in forbidden_promise_fragments
        if fragment in source.casefold()
    ]

    assert violations == []


def test_t012_040_sdk_external_tracing_stays_disabled() -> None:
    audited = {
        path.name: path.read_text(encoding="utf-8")
        for path in SDK_DIR.glob("*.py")
    }
    forbidden_fragments = (
        "set_tracing_disabled(False)",
        "tracing_disabled=False",
        '"tracing_disabled": False',
        "'tracing_disabled': False",
        '"external_trace_export": {"enabled": True',
        "'external_trace_export': {'enabled': True",
    )

    violations = [
        f"{file_name}:{fragment}"
        for file_name, source in audited.items()
        for fragment in forbidden_fragments
        if fragment in source
    ]

    assert violations == []

    runner = audited["action_turn_runner.py"]
    paid_harness = audited["paid_spike_harness.py"]
    trace = audited["action_trace.py"]
    assert "set_tracing_disabled(True)" in runner
    assert "tracing_disabled=True" in runner
    assert "set_tracing_disabled(True)" in paid_harness
    assert "tracing_disabled=True" in paid_harness
    assert '"enabled": False' in trace


def test_t012_040_sdk_trace_export_does_not_claim_public_delivery() -> None:
    audited = {
        path.name: path.read_text(encoding="utf-8")
        for path in SDK_DIR.glob("*.py")
    }
    forbidden_fragments = (
        '"public_delivery": True',
        "'public_delivery': True",
        '"outbox_reserved": True',
        "'outbox_reserved': True",
        '"direct_sdk_delivery_allowed": True',
        "'direct_sdk_delivery_allowed': True",
    )

    violations = [
        f"{file_name}:{fragment}"
        for file_name, source in audited.items()
        for fragment in forbidden_fragments
        if fragment in source
    ]

    assert violations == []

    trace = audited["action_trace.py"]
    assert '"public_delivery": False' in trace
    assert '"outbox_reserved": False' in trace
    assert '"direct_sdk_delivery_allowed": False' in trace
