from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from app.core.taliya_commercial.template_registry import VARIABLE_REGISTRY

Confidence = Literal["low", "medium", "high"]
Uncertainty = Literal["low", "medium", "high"]

TemplateVariableKind = Literal[
    "short_text",
    "long_text",
    "number",
    "boolean",
    "enum",
    "list",
    "url",
]
TemplateVariableSource = Literal[
    "user_message",
    "channel_metadata",
    "official_product_knowledge",
    "spec_006_product_contract",
    "diagnostic_ledger",
    "runtime_state",
    "model_decision",
]
ExtractedFactKind = Literal[
    "plan_price",
    "student_count",
    "phone",
    "date_time",
    "pain",
    "source",
    "unknown_number",
    "other",
]
LedgerStatus = Literal[
    "answered",
    "inferred_from_prior_message",
    "not_applicable",
    "pending",
]
DiagnosticQuestionKey = Literal[
    "active_students_or_size",
    "main_pain",
    "pain_detail",
    "current_process",
    "priority",
    "urgency",
]
ChunkPolicy = Literal["default", "whatsapp_max_3", "staged_diagnostic", "none"]


class SdkStrictModel(BaseModel):
    """Base for the SDK-facing output: strict-JSON-schema compatible by design.

    Every field is fully typed (no dict[str, Any]) so the Agents SDK can use
    this model as a strict `output_type` and the API guarantees schema-valid
    output instead of relying on repair retries.
    """

    model_config = ConfigDict(extra="forbid")


class SdkExtractedFact(SdkStrictModel):
    key: str
    kind: ExtractedFactKind
    raw_text: str
    value_text: str
    currency: Literal["BRL"] | None = None
    evidence: list[str] = Field(default_factory=list)


class SdkCommercialUnderstanding(SdkStrictModel):
    intents: list[str] = Field(default_factory=list)
    direct_question: str | None = Field(
        default=None,
        description=(
            "A direct question asked in the CURRENT inbound message only. "
            "Questions from earlier turns that were already answered are not "
            "direct questions of this turn; leave null when the current "
            "message asks nothing."
        ),
    )
    customer_need: str | None = None
    pain_context: str | None = None
    source_context: str | None = None
    mixed_intent: bool = False
    extracted_facts: list[SdkExtractedFact] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)


class SdkAnswerObligation(SdkStrictModel):
    obligation: str
    answering_template_id: str | None = Field(
        default=None,
        description=(
            "The template id in your template_plan that answers this obligation "
            "in this same turn, before any steering. Example: for 'qual o "
            "preco?', if your plan includes product.price_direct, set "
            "answering_template_id='product.price_direct'. Set null only when "
            "you are deliberately not answering this turn (e.g. delivery "
            "deferral). The runtime verifies this template is really in your "
            "plan; do not name a template you did not plan."
        ),
    )
    evidence: list[str] = Field(default_factory=list)


class SdkProductClaim(SdkStrictModel):
    claim: str
    fact_refs: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)


class SdkLedgerUpdate(SdkStrictModel):
    question_key: DiagnosticQuestionKey
    status: LedgerStatus
    answer_value: str | None = None
    evidence: list[str] = Field(default_factory=list)


class SdkDiagnosticProposal(SdkStrictModel):
    ledger_updates: list[SdkLedgerUpdate] = Field(default_factory=list)
    next_question_key: DiagnosticQuestionKey | None = Field(
        default=None,
        description=(
            "Set only while actually conducting the diagnostic: the next "
            "mandatory key to ask, in the fixed order. Leave null when merely "
            "offering the diagnostic or when delivering the final diagnostic."
        ),
    )
    final_diagnostic_ready: bool = False
    evidence: list[str] = Field(default_factory=list)


class SdkDemoProposal(SdkStrictModel):
    status: str = "not_offered"
    next_step: str = "none"
    evidence: list[str] = Field(default_factory=list)


class SdkWaitlistProposal(SdkStrictModel):
    eligibility: str = "unknown"
    intent: str = "none"
    missing_details: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)


class SdkHandoffProposal(SdkStrictModel):
    status: str = "none"
    reason: str | None = None
    pause_required: bool = False
    evidence: list[str] = Field(default_factory=list)


class SdkTemplateVariable(SdkStrictModel):
    name: str
    kind: TemplateVariableKind
    value: str
    source: TemplateVariableSource
    evidence: list[str] = Field(
        default_factory=list,
        description=(
            "REQUIRED: at least one evidence ref for where this value came "
            "from (a fact ref, ledger key, state field, or short lead-message "
            "excerpt). Variables with empty evidence fail validation."
        ),
    )
    max_length: int | None = None


class SdkTemplatePlan(SdkStrictModel):
    template_ids: list[str] = Field(
        default_factory=list,
        description=(
            "REQUIRED: at least one approved template id, chosen only from "
            "get_approved_template_catalog results. The runtime renders the lead "
            "reply exclusively from these templates; an empty list fails "
            "validation and no reply is sent."
        ),
    )
    variables: list[SdkTemplateVariable] = Field(
        default_factory=list,
        description=(
            "One entry per variable required by the chosen templates "
            "(see required_variables in the catalog). Compose values from "
            "official facts and concrete lead context; long_text needs max_length."
        ),
    )
    evidence: list[str] = Field(default_factory=list)


class SdkStatePatchHandoff(SdkStrictModel):
    status: str
    pause_ai: bool


class SdkStatePatchDelivery(SdkStrictModel):
    defer_inbound_during_chunks: bool
    deferred_inbound_count: int = 0


class SdkStatePatchProposal(SdkStrictModel):
    handoff: SdkStatePatchHandoff | None = None
    delivery: SdkStatePatchDelivery | None = None


class SdkSalesInboxProjection(SdkStrictModel):
    commercial_stage: str = "lead_conversation"
    last_intent: str | None = None
    diagnostic_status: str | None = None
    waitlist_status: str | None = None
    handoff_status: str | None = None
    next_action_hint: str | None = None


class SdkSafety(SdkStrictModel):
    guardrail_flags: list[str] = Field(default_factory=list)
    uncertainty: Uncertainty = "medium"


class SdkDeliveryProposal(SdkStrictModel):
    chunk_policy: ChunkPolicy = "default"


class TaliyaSdkTurnOutput(SdkStrictModel):
    """Model-facing structured output for the Spec 012 SDK spike.

    Identity fields (turn/conversation ids, channel, starting agent), the
    agent path, and usage are owned by the harness, never by the model. This
    model carries only commercial understanding and proposals; the adapter
    combines both into TaliyaTurnProposal before validation and rendering.
    """

    schema_version: Literal["012.sdk_turn_output.v1"] = "012.sdk_turn_output.v1"
    commercial_understanding: SdkCommercialUnderstanding
    answer_obligations: list[SdkAnswerObligation] = Field(default_factory=list)
    product_claims: list[SdkProductClaim] = Field(default_factory=list)
    diagnostic_proposal: SdkDiagnosticProposal = Field(default_factory=SdkDiagnosticProposal)
    demo_proposal: SdkDemoProposal = Field(default_factory=SdkDemoProposal)
    waitlist_proposal: SdkWaitlistProposal = Field(default_factory=SdkWaitlistProposal)
    handoff_proposal: SdkHandoffProposal = Field(default_factory=SdkHandoffProposal)
    template_plan: SdkTemplatePlan = Field(default_factory=SdkTemplatePlan)
    state_patch: SdkStatePatchProposal = Field(default_factory=SdkStatePatchProposal)
    safety: SdkSafety = Field(default_factory=SdkSafety)
    sales_inbox_projection: SdkSalesInboxProjection = Field(
        default_factory=SdkSalesInboxProjection
    )
    delivery: SdkDeliveryProposal = Field(default_factory=SdkDeliveryProposal)
    confidence: Confidence = "medium"
    risks: list[str] = Field(default_factory=list)


_OFFICIAL_VARIABLE_SOURCES = frozenset(
    {"official_product_knowledge", "spec_006_product_contract"}
)
_CONTEXT_SOURCE_PREFERENCE = (
    "user_message",
    "diagnostic_ledger",
    "runtime_state",
    "channel_metadata",
    "model_decision",
)


def _normalized_template_variable(variable: SdkTemplateVariable) -> dict[str, Any]:
    """Normalize kind/max_length/source to the official variable registry spec.

    The registry is the canonical rendering contract, so this is deterministic
    rendering plumbing, not commercial judgment. Source handling is split by
    risk class: for variables whose allowed sources include an official
    product source, the declared source is NEVER coerced - a wrong label there
    could mask an ungrounded product fact and must fail validation. For pure
    lead-context variables (no official source allowed), a disallowed label is
    a bookkeeping error, not a grounding risk, so it is normalized to the
    first allowed source.
    """

    spec = VARIABLE_REGISTRY.get(variable.name)
    kind = spec.kind if spec is not None else variable.kind
    max_length = variable.max_length if variable.max_length else None
    if spec is not None and spec.max_length is not None:
        max_length = spec.max_length
    source = variable.source
    if (
        spec is not None
        and source not in spec.allowed_sources
        and not (_OFFICIAL_VARIABLE_SOURCES & spec.allowed_sources)
    ):
        source = next(
            (
                candidate
                for candidate in _CONTEXT_SOURCE_PREFERENCE
                if candidate in spec.allowed_sources
            ),
            source,
        )
    payload: dict[str, Any] = {
        "kind": kind,
        "value": variable.value,
        "source": source,
        "evidence": list(variable.evidence),
    }
    if max_length is not None:
        payload["max_length"] = max_length
    return payload


def _numeric_value(fact: SdkExtractedFact) -> Any:
    if fact.kind in {"plan_price", "student_count", "unknown_number"}:
        text = fact.value_text.strip()
        try:
            return int(text)
        except ValueError:
            try:
                return float(text)
            except ValueError:
                return fact.value_text
    return fact.value_text


def sdk_turn_output_to_proposal_fields(output: TaliyaSdkTurnOutput) -> dict[str, Any]:
    """Convert the strict SDK output into TaliyaTurnProposal content fields.

    Identity, agent_path, and usage are intentionally absent: the harness adds
    them from its own run records, so the model cannot fabricate them.
    """

    understanding = output.commercial_understanding
    template_variables = {
        variable.name: _normalized_template_variable(variable)
        for variable in output.template_plan.variables
    }
    state_patch: dict[str, Any] = {}
    if output.state_patch.handoff is not None:
        state_patch["handoff"] = {
            "status": output.state_patch.handoff.status,
            "pause_ai": output.state_patch.handoff.pause_ai,
        }
    if output.state_patch.delivery is not None:
        state_patch["delivery"] = {
            "defer_inbound_during_chunks": (
                output.state_patch.delivery.defer_inbound_during_chunks
            ),
            "deferred_inbound_count": output.state_patch.delivery.deferred_inbound_count,
        }

    projection = {
        key: value
        for key, value in output.sales_inbox_projection.model_dump(mode="json").items()
        if value is not None
    }

    return {
        "commercial_understanding": {
            "intents": list(understanding.intents),
            "direct_question": understanding.direct_question,
            "customer_need": understanding.customer_need,
            "pain_context": understanding.pain_context,
            "source_context": understanding.source_context,
            "mixed_intent": understanding.mixed_intent,
            "extracted_facts": [
                {
                    "key": fact.key,
                    "kind": fact.kind,
                    "raw_text": fact.raw_text,
                    "value": _numeric_value(fact),
                    **({"currency": fact.currency} if fact.currency is not None else {}),
                    "evidence": list(fact.evidence),
                }
                for fact in understanding.extracted_facts
            ],
            "evidence": list(understanding.evidence),
        },
        # answered_before_steering is derived, never self-attested: it is true
        # only when the named answering template is actually in the plan.
        "answer_obligations": [
            {
                "obligation": obligation.obligation,
                "answered_before_steering": (
                    obligation.answering_template_id is not None
                    and obligation.answering_template_id
                    in output.template_plan.template_ids
                ),
                "evidence": list(obligation.evidence),
            }
            for obligation in output.answer_obligations
        ],
        "product_claims": [claim.model_dump(mode="json") for claim in output.product_claims],
        "diagnostic_proposal": output.diagnostic_proposal.model_dump(mode="json"),
        "demo_proposal": output.demo_proposal.model_dump(mode="json"),
        "waitlist_proposal": output.waitlist_proposal.model_dump(mode="json"),
        "handoff_proposal": output.handoff_proposal.model_dump(mode="json"),
        "template_proposal": {
            "template_ids": list(output.template_plan.template_ids),
            "variables": template_variables,
            "evidence": list(output.template_plan.evidence),
        },
        "safety": {
            "guardrails": [
                {"name": flag, "outcome": "flagged"}
                for flag in output.safety.guardrail_flags
            ],
            "uncertainty": output.safety.uncertainty,
        },
        "state_patch_proposal": state_patch,
        "sales_inbox_projection_proposal": projection,
        "delivery_proposal": {
            "chunk_policy": output.delivery.chunk_policy,
            "render_plan_only": True,
            "evidence": list(output.template_plan.evidence),
        },
        "confidence": output.confidence,
        "risks": list(output.risks),
    }
