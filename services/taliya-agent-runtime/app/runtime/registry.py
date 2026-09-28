from __future__ import annotations

from dataclasses import dataclass, field

from app.domains.taliya_commercial.behavior_policy import TRIAGE_AGENT


class AgentRegistryError(Exception):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(message)


@dataclass(frozen=True)
class AgentDefinition:
    agent_key: str
    agent_family: str
    owner_scope: str
    tenant_id: str | None
    enabled: bool
    description: str
    default_agent_name: str
    reserved_for: str | None = None


@dataclass
class AgentRegistry:
    definitions: dict[str, AgentDefinition] = field(default_factory=dict)

    def register(self, definition: AgentDefinition) -> None:
        self.definitions[definition.agent_key] = definition

    def get_active(self, agent_key: str) -> AgentDefinition:
        definition = self.definitions.get(agent_key)
        if definition is None:
            raise AgentRegistryError("unknown_agent_key", f"Unknown agent key: {agent_key}")
        if not definition.enabled:
            raise AgentRegistryError("disabled_agent_key", f"Agent key is not enabled: {agent_key}")
        return definition

    def reserved_keys(self) -> list[str]:
        return [
            definition.agent_key
            for definition in self.definitions.values()
            if not definition.enabled
        ]


def build_default_registry() -> AgentRegistry:
    registry = AgentRegistry()
    registry.register(
        AgentDefinition(
            agent_key="taliya_commercial",
            agent_family="taliya",
            owner_scope="taliya",
            tenant_id=None,
            enabled=True,
            description="Commercial sales agent for Taliya leads from widget and Taliya-owned WhatsApp.",
            default_agent_name=TRIAGE_AGENT,
        )
    )
    for agent_key, agent_family, owner_scope, default_agent_name, reserved_for, description in [
        (
            "taliya_configuration",
            "taliya_configuration",
            "taliya",
            "taliya_configuration_triage_agent",
            "future_configuration_agent",
            "Future configuration/setup agent for Taliya-owned onboarding.",
        ),
        (
            "studio_configuration",
            "studio_operations",
            "studio",
            "studio_configuration_triage_agent",
            "legacy_reserved_configuration_alias",
            "Reserved legacy-compatible key; not active in this feature.",
        ),
        (
            "studio_lead_capture",
            "studio_operations",
            "studio",
            "studio_lead_capture_triage_agent",
            "future_studio_agent",
            "Future studio lead capture agent.",
        ),
        (
            "studio_scheduling",
            "studio_operations",
            "studio",
            "studio_scheduling_triage_agent",
            "future_studio_agent",
            "Future studio scheduling agent.",
        ),
        (
            "studio_reactivation",
            "studio_operations",
            "studio",
            "studio_reactivation_triage_agent",
            "future_studio_agent",
            "Future studio reactivation agent.",
        ),
        (
            "studio_billing",
            "studio_operations",
            "studio",
            "studio_billing_triage_agent",
            "future_studio_agent",
            "Future studio billing agent.",
        ),
        (
            "studio_support",
            "studio_operations",
            "studio",
            "studio_support_triage_agent",
            "future_studio_agent",
            "Future studio support agent.",
        ),
        (
            "studio_retention",
            "studio_operations",
            "studio",
            "studio_retention_triage_agent",
            "future_studio_agent",
            "Future studio retention agent.",
        ),
        (
            "studio_reporting",
            "studio_operations",
            "studio",
            "studio_reporting_triage_agent",
            "future_studio_agent",
            "Future studio reporting agent.",
        ),
        (
            "taliya_studio_sales",
            "studio_operations",
            "studio",
            "taliya_studio_sales_triage_agent",
            "legacy_reserved_customer_sales_alias",
            "Reserved legacy-compatible studio sales key; not active in this feature.",
        ),
    ]:
        registry.register(
            AgentDefinition(
                agent_key=agent_key,
                agent_family=agent_family,
                owner_scope=owner_scope,
                tenant_id=None,
                enabled=False,
                description=description,
                default_agent_name=default_agent_name,
                reserved_for=reserved_for,
            )
        )
    return registry
