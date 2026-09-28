from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

Channel = Literal["widget", "whatsapp"]
Confidence = Literal["low", "medium", "high"]
COMMERCIAL_OPS_CONTRACT_VERSION = "taliya-commercial-ops.v1"


class ConversationRef(BaseModel):
    conversation_id: str
    lead_id: str | None = None
    channel_conversation_id: str | None = None
    source: str | None = None
    entry_intent: str | None = None


class InboundMessage(BaseModel):
    idempotency_key: str
    channel_message_id: str | None = None
    type: Literal["text", "unsupported_media", "postback"] = "text"
    text: str | None = None
    timestamp: str | None = None


class SenderRef(BaseModel):
    name: str | None = None
    whatsapp_phone: str | None = None
    email: str | None = None


class AgentRunRequest(BaseModel):
    contract_version: Literal["taliya-commercial-ops.v1"] = COMMERCIAL_OPS_CONTRACT_VERSION
    agent_key: str
    agent_family: str = "taliya"
    owner_scope: Literal["taliya", "studio"] = "taliya"
    tenant_id: str | None = None
    channel: Channel
    conversation: ConversationRef
    message: InboundMessage
    sender: SenderRef = Field(default_factory=SenderRef)
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentMessage(BaseModel):
    text: str
    channel_hint: Channel
    kind: Literal["text", "link", "action"] = "text"
    template_id: str | None = None
    requires_product_source: bool = False


class LeadFact(BaseModel):
    key: str
    value: str
    confidence: Confidence = "medium"
    evidence: list[str] = Field(default_factory=list)


class DiagnosticAdditionalAnswer(BaseModel):
    question_key: str
    answer_value: str | None = None
    areas: list[str] = Field(default_factory=list)
    confidence: Confidence = "low"
    evidence: list[str] = Field(default_factory=list)


class DiagnosticAnswerInterpretation(BaseModel):
    current_question: str | None = None
    answer_status: Literal["answered", "partial", "unclear", "refused", "side_question"] = "unclear"
    answer_value: str | None = None
    areas: list[str] = Field(default_factory=list)
    confidence: Confidence = "low"
    evidence: list[str] = Field(default_factory=list)
    needs_clarification: bool = False
    side_question_kind: str | None = None
    additional_answers: list[DiagnosticAdditionalAnswer] = Field(default_factory=list)


class PolicyChecks(BaseModel):
    direct_question_answered_first: bool = True
    diagnostic_timing_ok: bool = True
    waitlist_timing_ok: bool = True
    official_facts_only: bool = True
    no_early_contact_capture: bool = True
    no_whatsapp_phone_request: bool = True
    no_fake_certainty: bool = True
    no_human_overlap: bool = True
    channel_brevity_ok: bool = True


class RuntimeDecision(BaseModel):
    previous_state: str = "new_lead"
    current_state: str = "new_lead"
    next_state: str = "new_lead"
    route: Literal[
        "entry",
        "product",
        "diagnostic",
        "waitlist",
        "handoff",
        "safe_fallback",
    ] = "entry"
    opening_type: Literal[
        "none",
        "cold_greeting_only",
        "widget_opening",
        "site_forced_message",
        "social_source_opening",
        "diagnostic_cta_opening",
        "direct_question_opening",
        "returning_lead",
    ] = "none"
    detected_intents: list[str] = Field(default_factory=list)
    direct_question_present: bool = False
    direct_question_answered_first: bool = True
    diagnostic_action: Literal[
        "none",
        "offer",
        "start",
        "ask_next",
        "complete",
        "insufficient_evidence",
    ] = "none"
    diagnostic_allowed_now: bool = False
    waitlist_allowed_now: bool = False
    demo_status: Literal[
        "not_offered",
        "offered",
        "viewed_or_asked",
        "reacted_positive",
    ] = "not_offered"
    demo_next_step: Literal[
        "none",
        "offer_demo",
        "ask_demo_reaction",
        "follow_positive_demo_interest",
    ] = "none"
    profile_name_usage: Literal[
        "used_reliable_name",
        "ignored_unreliable_name",
        "not_available",
        "not_needed",
    ] = "not_needed"
    facts_used: list[str] = Field(default_factory=list)
    facts_missing: list[str] = Field(default_factory=list)
    template_ids: list[str] = Field(default_factory=list)
    template_variables: dict[str, dict[str, Any]] = Field(default_factory=dict)
    render_plan: list[dict[str, Any]] = Field(default_factory=list)
    diagnostic_ledger_status: Literal[
        "not_started",
        "incomplete",
        "in_progress",
        "complete",
        "blocked",
    ] = "not_started"
    next_question_kind: Literal[
        "none",
        "pain",
        "current_process",
        "priority",
        "urgency",
        "plan_fit",
        "waitlist_details",
        "handoff",
        "clarification",
        "validation",
    ] = "none"
    policy_checks: PolicyChecks = Field(default_factory=PolicyChecks)

    @field_validator("template_variables", mode="before")
    @classmethod
    def coerce_template_variables(cls, value: Any) -> dict[str, dict[str, Any]]:
        if not isinstance(value, dict):
            return {}
        normalized: dict[str, dict[str, Any]] = {}
        for key, item in value.items():
            if isinstance(item, dict):
                normalized[str(key)] = item
            else:
                normalized[str(key)] = {"value": item}
        return normalized


class DiagnosticOutput(BaseModel):
    status: Literal[
        "not_started",
        "offered",
        "in_progress",
        "completed",
        "insufficient_evidence",
    ] = "not_started"
    ledger: list[dict[str, Any]] = Field(default_factory=list)
    facts_used: list[str] = Field(default_factory=list)
    main_bottleneck: str | None = None
    pain_context_human: str | None = None
    likely_cause: str | None = None
    crm_base_recommendation: str | None = None
    first_recommended_step: str | None = None
    indicated_routines_or_agents: list[str] = Field(default_factory=list)
    indicated_agents: list[dict[str, Any]] = Field(default_factory=list)
    plan_or_range_to_compare: str | None = None
    final_plan_line: str | None = None
    demo_status_at_delivery: Literal[
        "not_offered",
        "offered",
        "viewed_or_asked",
        "reacted_positive",
    ] = "not_offered"
    final_demo_line: str | None = None
    evidence: list[str] = Field(default_factory=list)
    unknowns: list[str] = Field(default_factory=list)
    confidence: Confidence = "low"
    next_question: str | None = None
    validation_question: str | None = None
    final_demo_next_step_question: str | None = None

    @field_validator("indicated_agents", mode="before")
    @classmethod
    def coerce_indicated_agents(cls, value: Any) -> list[dict[str, Any]]:
        if not isinstance(value, list):
            return []
        normalized: list[dict[str, Any]] = []
        for item in value:
            if isinstance(item, dict):
                normalized.append(item)
            elif isinstance(item, str) and item.strip():
                normalized.append({"name": item.strip()})
        return normalized


class WaitlistAction(BaseModel):
    status: Literal["none", "offered", "pending_details", "joined", "declined"] = "none"
    reason: str | None = None
    missing_fields: list[str] = Field(default_factory=list)


class HandoffOutput(BaseModel):
    status: Literal["none", "requested", "active", "resumed"] = "none"
    reason: str | None = None


class SourceRef(BaseModel):
    type: Literal["product_knowledge", "memory", "operator"]
    version: str | None = None
    keys: list[str] = Field(default_factory=list)


class ToolResult(BaseModel):
    name: str
    status: Literal["ok", "blocked", "error"]
    idempotency_key: str | None = None
    summary: str | None = None


class Usage(BaseModel):
    model: str | None
    model_operations: int = 0
    input_tokens: int = 0
    cached_input_tokens: int = 0
    cache_write_input_tokens: int = 0
    output_tokens: int = 0
    reasoning_tokens: int = 0
    repairs: int = 0
    latency_ms: float = 0
    cost_usd: float = 0


class DeliveryControl(BaseModel):
    shadow_mode: bool = False
    delivery_suppressed: bool = False
    suppression_reason: str | None = None
    rendered_message_count: int = 0
    trace_contains_rendered_messages: bool = False


class RuntimeInputSnapshot(BaseModel):
    contract_version: Literal["taliya-commercial-ops.v1"] = COMMERCIAL_OPS_CONTRACT_VERSION
    channel: Channel
    conversation_id: str
    lead_id: str | None = None
    channel_conversation_id: str | None = None
    source: str | None = None
    entry_intent: str | None = None
    message_id: str
    channel_message_id: str | None = None
    message_type: Literal["text", "unsupported_media", "postback"] = "text"
    message_timestamp: str | None = None
    page_path: str | None = None
    source_section: str | None = None
    campaign_stage: str | None = None


class AgentOutput(BaseModel):
    decision: RuntimeDecision = Field(default_factory=RuntimeDecision)
    messages: list[AgentMessage] = Field(default_factory=list)
    lead_facts: list[LeadFact] = Field(default_factory=list)
    diagnostic: DiagnosticOutput | None = None
    waitlist_action: WaitlistAction | None = None
    handoff: HandoffOutput | None = None
    sources: list[SourceRef] = Field(default_factory=list)
    safety_flags: list[str] = Field(default_factory=list)
    tool_results: list[ToolResult] = Field(default_factory=list)
    usage: Usage
    confidence: Confidence = "medium"
    context_snapshot: dict[str, Any] = Field(default_factory=dict)
    turn_situation: dict[str, Any] = Field(default_factory=dict)
    action_decision: dict[str, Any] = Field(default_factory=dict)
    action_repair_attempt_count: int = 0
    conductor_json: dict[str, Any] = Field(default_factory=dict)
    validator_results: list[dict[str, Any]] = Field(default_factory=list)
    repair_attempts: list[dict[str, Any]] = Field(default_factory=list)
    runtime_state: dict[str, Any] = Field(default_factory=dict)
    sales_inbox_projection: dict[str, Any] = Field(default_factory=dict)
    delivery_events: list[dict[str, Any]] = Field(default_factory=list)
    trace_complete: bool = False


class AgentRunResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contract_version: Literal["taliya-commercial-ops.v1"] = COMMERCIAL_OPS_CONTRACT_VERSION
    run_id: str
    conversation_id: str
    lead_id: str | None = None
    agent_key: str
    agent_family: str = "taliya"
    owner_scope: Literal["taliya", "studio"] = "taliya"
    tenant_id: str | None = None
    current_agent: str
    status: Literal["succeeded", "failed", "blocked", "human_paused", "cost_capped"]
    output: AgentOutput
    trace_id: str
    input_snapshot: RuntimeInputSnapshot | None = None
    delivery_control: DeliveryControl = Field(default_factory=DeliveryControl)


class CommercialOpsContract(BaseModel):
    contract_version: Literal["taliya-commercial-ops.v1"] = COMMERCIAL_OPS_CONTRACT_VERSION
    request: AgentRunRequest
    response: AgentRunResponse
