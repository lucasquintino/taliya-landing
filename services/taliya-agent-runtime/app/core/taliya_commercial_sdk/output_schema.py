from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

Channel = Literal["widget", "whatsapp"]
Confidence = Literal["low", "medium", "high"]

FORBIDDEN_DIRECT_OUTPUT_FIELDS = frozenset(
    {
        "assistant_message",
        "assistant_reply",
        "assistant_response",
        "customer_message",
        "customer_response",
        "final_message",
        "final_response",
        "final_text",
        "freeform_response",
        "full_response",
        "message",
        "message_text",
        "response_text",
    }
)


class SdkSchemaModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


def _has_evidence(evidence: list[str]) -> bool:
    return any(item.strip() for item in evidence)


def _reject_direct_output_fields(value: Any, *, path: str = "proposal") -> None:
    if isinstance(value, dict):
        forbidden = sorted(FORBIDDEN_DIRECT_OUTPUT_FIELDS.intersection(value))
        if forbidden:
            raise ValueError(
                f"forbidden direct-output fields at {path}: {', '.join(forbidden)}"
            )
        for key, child in value.items():
            _reject_direct_output_fields(child, path=f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _reject_direct_output_fields(child, path=f"{path}[{index}]")


class AgentPathItem(SdkSchemaModel):
    event: Literal["start", "handoff", "tool", "guardrail", "final"]
    agent: str | None = None
    from_agent: str | None = None
    to_agent: str | None = None
    tool_name: str | None = None
    guardrail_name: str | None = None
    evidence: list[str] = Field(default_factory=list)


class CommercialUnderstanding(SdkSchemaModel):
    intents: list[str] = Field(default_factory=list)
    direct_question: str | None = None
    customer_need: str | None = None
    pain_context: str | None = None
    source_context: str | None = None
    mixed_intent: bool = False
    extracted_facts: list[dict[str, Any]] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)


class AnswerObligation(SdkSchemaModel):
    obligation: str
    answered_before_steering: bool = False
    evidence: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def obligation_requires_evidence(self) -> AnswerObligation:
        if not _has_evidence(self.evidence):
            raise ValueError("answer obligations require evidence")
        return self


class ProductClaimProposal(SdkSchemaModel):
    claim: str
    fact_refs: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def product_claims_require_official_refs(self) -> ProductClaimProposal:
        if not self.fact_refs:
            raise ValueError("product claims require official fact refs")
        if not _has_evidence(self.evidence):
            raise ValueError("product claims require evidence")
        return self


class DiagnosticProposal(SdkSchemaModel):
    ledger_updates: list[dict[str, Any]] = Field(default_factory=list)
    next_question_key: str | None = None
    final_diagnostic_ready: bool = False
    evidence: list[str] = Field(default_factory=list)


class DemoProposal(SdkSchemaModel):
    status: str = "not_offered"
    next_step: str = "none"
    evidence: list[str] = Field(default_factory=list)


class WaitlistProposal(SdkSchemaModel):
    eligibility: str = "unknown"
    intent: str = "none"
    missing_details: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)


class HandoffProposal(SdkSchemaModel):
    status: str = "none"
    reason: str | None = None
    pause_required: bool = False
    evidence: list[str] = Field(default_factory=list)


class TemplateProposal(SdkSchemaModel):
    template_ids: list[str] = Field(default_factory=list)
    variables: dict[str, Any] = Field(default_factory=dict)
    evidence: list[str] = Field(default_factory=list)

    @field_validator("variables")
    @classmethod
    def variables_cannot_be_whole_response(cls, value: dict[str, Any]) -> dict[str, Any]:
        _reject_direct_output_fields(value, path="template_proposal.variables")
        return value


class SafetyProposal(SdkSchemaModel):
    guardrails: list[dict[str, Any]] = Field(default_factory=list)
    uncertainty: str = "medium"


class DeliveryProposal(SdkSchemaModel):
    chunk_policy: str = "none"
    render_plan_only: bool = True
    evidence: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def delivery_must_remain_render_plan_only(self) -> DeliveryProposal:
        if not self.render_plan_only:
            raise ValueError("SDK delivery proposal must remain render_plan_only")
        return self


class UsageProposal(SdkSchemaModel):
    model: str | None = None
    model_operations: int = 0
    input_tokens: int = 0
    cached_input_tokens: int = 0
    cache_write_input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    handoffs: int = 0
    repairs: int = 0

    @model_validator(mode="after")
    def usage_values_cannot_be_negative(self) -> UsageProposal:
        for field_name in (
            "model_operations",
            "input_tokens",
            "cached_input_tokens",
            "cache_write_input_tokens",
            "output_tokens",
            "cost_usd",
            "handoffs",
            "repairs",
        ):
            if getattr(self, field_name) < 0:
                raise ValueError(f"usage field cannot be negative: {field_name}")
        return self


class TaliyaTurnProposal(SdkSchemaModel):
    schema_version: Literal["012.turn_proposal.v1"] = "012.turn_proposal.v1"
    turn_id: str
    conversation_id: str
    channel: Channel
    starting_agent: str
    agent_path: list[AgentPathItem]
    commercial_understanding: CommercialUnderstanding
    answer_obligations: list[AnswerObligation] = Field(default_factory=list)
    product_claims: list[ProductClaimProposal] = Field(default_factory=list)
    diagnostic_proposal: DiagnosticProposal = Field(default_factory=DiagnosticProposal)
    demo_proposal: DemoProposal = Field(default_factory=DemoProposal)
    waitlist_proposal: WaitlistProposal = Field(default_factory=WaitlistProposal)
    handoff_proposal: HandoffProposal = Field(default_factory=HandoffProposal)
    template_proposal: TemplateProposal = Field(default_factory=TemplateProposal)
    safety: SafetyProposal = Field(default_factory=SafetyProposal)
    state_patch_proposal: dict[str, Any] = Field(default_factory=dict)
    sales_inbox_projection_proposal: dict[str, Any] = Field(default_factory=dict)
    delivery_proposal: DeliveryProposal = Field(default_factory=DeliveryProposal)
    confidence: Confidence = "medium"
    risks: list[str] = Field(default_factory=list)
    usage: UsageProposal = Field(default_factory=UsageProposal)

    @model_validator(mode="before")
    @classmethod
    def reject_direct_output_before_validation(cls, value: Any) -> Any:
        _reject_direct_output_fields(value)
        return value

    @model_validator(mode="after")
    def proposal_requires_agent_path(self) -> TaliyaTurnProposal:
        if not self.agent_path:
            raise ValueError("TaliyaTurnProposal requires agent_path")
        if self.agent_path[0].event != "start":
            raise ValueError("agent_path must start with a start event")
        return self
