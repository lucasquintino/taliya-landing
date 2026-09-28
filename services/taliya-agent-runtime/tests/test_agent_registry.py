import pytest

from app.runtime.registry import AgentRegistry, AgentRegistryError, build_default_registry


def test_default_registry_exposes_only_taliya_commercial_as_active():
    registry = build_default_registry()

    active = registry.get_active("taliya_commercial")

    assert active.agent_key == "taliya_commercial"
    assert active.agent_family == "taliya"
    assert active.owner_scope == "taliya"
    assert active.tenant_id is None
    assert active.enabled is True
    assert "taliya_configuration" in registry.reserved_keys()
    assert "studio_lead_capture" in registry.reserved_keys()
    assert "studio_retention" in registry.reserved_keys()


def test_reserved_future_agent_key_is_disabled():
    registry = build_default_registry()

    with pytest.raises(AgentRegistryError) as exc:
        registry.get_active("studio_retention")

    assert exc.value.code == "disabled_agent_key"


def test_unknown_agent_key_is_rejected():
    registry = AgentRegistry()

    with pytest.raises(AgentRegistryError) as exc:
        registry.get_active("unknown")

    assert exc.value.code == "unknown_agent_key"
