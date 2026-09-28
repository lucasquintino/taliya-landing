from app.domains.taliya_commercial.tools import (
    REQUIRED_TOOL_NAMES,
    get_model_callable_tool_names,
    get_model_callable_tools,
)


def test_required_tools_are_registered_for_model_calls():
    registered = set(get_model_callable_tool_names())

    assert set(REQUIRED_TOOL_NAMES).issubset(registered)


def test_registered_tools_have_model_callable_marker_or_sdk_name():
    tools = get_model_callable_tools()

    for tool in tools:
        name = getattr(tool, "name", None) or getattr(tool, "taliya_tool_name", None)
        assert name in REQUIRED_TOOL_NAMES
        assert getattr(tool, "taliya_model_callable", True) is True
