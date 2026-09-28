"""No-cost preflight gate for T012-027 paid spike runs.

Lesson from paid attempts 1 and 2: most failures were predictable mismatches
between what the model receives (instructions, schema, tool payloads) and what
the validators/renderer enforce (template registry, variable registry, turn
budget). This gate makes those mismatches fail here, before any paid call.

It cannot predict the model's conversational judgment - that is what the paid
canary/full runs measure - but it guarantees the model is never set up to fail
for reasons we already know.
"""

from __future__ import annotations

from app.core.taliya_commercial.template_registry import (
    TEMPLATE_REGISTRY,
    VARIABLE_REGISTRY,
)
from app.core.taliya_commercial_sdk import load_frozen_spike_scenarios
from app.core.taliya_commercial_sdk.agents import build_sdk_agent_specs
from app.core.taliya_commercial_sdk.spike_scenarios import (
    CANARY_SCENARIO_IDS,
    load_canary_spike_scenarios,
)
from tests.test_spec012_sdk_mocked_contracts import _scenarios as golden_scenarios


def test_preflight_every_template_variable_has_a_registry_spec() -> None:
    """A template requiring an unspecced variable would fail render at paid time."""

    missing: list[tuple[str, str]] = []
    for template_id, template in TEMPLATE_REGISTRY.items():
        for name in (*template.required_variables, *template.optional_variables):
            if name not in VARIABLE_REGISTRY:
                missing.append((template_id, name))
    assert not missing, f"template variables without registry spec: {missing}"


def test_preflight_golden_templates_are_in_the_final_agents_embedded_catalog() -> None:
    """Every golden answer must be expressible by the agent that owns it.

    The golden mocked-contract outputs are the approved behavior target. If a
    golden template id is not embedded in the instructions of the agent that
    finishes that scenario, the real model cannot reproduce the golden without
    an extra catalog tool round - the exact failure class of paid attempt 2.
    """

    specs = build_sdk_agent_specs()
    gaps: list[tuple[str, str, str]] = []
    for scenario in golden_scenarios():
        final_agent = scenario.output["agent_path"][-1]["agent"]
        instructions = specs[final_agent].instructions
        for template_id in scenario.output["template_proposal"]["template_ids"]:
            if template_id not in instructions:
                gaps.append((scenario.scenario_id, final_agent, template_id))
    assert not gaps, f"golden templates missing from embedded catalogs: {gaps}"


def test_preflight_golden_variables_conform_to_registry_specs() -> None:
    """Golden variables must match the canonical kind and an allowed source."""

    issues: list[tuple[str, str, str]] = []
    for scenario in golden_scenarios():
        variables = scenario.output["template_proposal"]["variables"]
        for name, variable in variables.items():
            spec = VARIABLE_REGISTRY.get(name)
            if spec is None:
                issues.append((scenario.scenario_id, name, "no registry spec"))
                continue
            if variable["kind"] != spec.kind:
                issues.append(
                    (
                        scenario.scenario_id,
                        name,
                        f"kind {variable['kind']} != registry {spec.kind}",
                    )
                )
            if variable["source"] not in spec.allowed_sources:
                issues.append(
                    (
                        scenario.scenario_id,
                        name,
                        f"source {variable['source']} not allowed",
                    )
                )
    assert not issues, f"golden variables out of registry contract: {issues}"


def test_preflight_canary_subset_covers_observed_failure_classes() -> None:
    """The cheap canary run must touch every failure class seen in attempts 1-2.

    cold_greeting: entry path, empty-plan class. price_first: product path,
    answer obligations and render contract. diagnostic_urgency_final: state
    snapshot, staged final delivery, and turn-budget pressure (max_turns).
    """

    assert CANARY_SCENARIO_IDS == (
        "cold_greeting",
        "price_first",
        "diagnostic_urgency_final",
    )
    canary = load_canary_spike_scenarios()
    assert [scenario.scenario_id for scenario in canary] == list(CANARY_SCENARIO_IDS)
    frozen_ids = [scenario.scenario_id for scenario in load_frozen_spike_scenarios()]
    assert all(scenario_id in frozen_ids for scenario_id in CANARY_SCENARIO_IDS)


def test_preflight_persisted_current_agents_are_valid_agent_names() -> None:
    """A stale/typo current_sdk_agent must fall back to triage, never crash."""

    specs = build_sdk_agent_specs()
    for scenario in load_frozen_spike_scenarios():
        persisted = dict(scenario.state_snapshot).get("current_sdk_agent")
        if persisted is not None:
            assert persisted in specs, (scenario.scenario_id, persisted)


def test_preflight_embedded_catalogs_only_list_registry_templates() -> None:
    """Instructions must never advertise a template id the renderer rejects."""

    specs = build_sdk_agent_specs()
    for spec in specs.values():
        marker = "Approved templates for this role:"
        if marker not in spec.instructions:
            # Pure routers never finalize, so they carry no template catalog.
            assert spec.name == "taliya_triage_agent"
            continue
        section = spec.instructions.split(marker, 1)[1]
        for line in section.splitlines():
            line = line.strip()
            if not line.startswith("- ") or ":" in line.split(" (", 1)[0]:
                continue
            template_id = line[2:].split(" (", 1)[0].strip()
            if "." not in template_id:
                continue
            assert template_id in TEMPLATE_REGISTRY, (spec.name, template_id)
