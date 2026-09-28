from __future__ import annotations

from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

Channel = Literal["widget", "whatsapp"]
Confidence = Literal["low", "medium", "high"]
Severity = Literal["P0", "P1", "P2"]

STUDIO_OWNER_LANGUAGE_TERMS = (
    "sistema",
    "rotina",
    "base organizada",
    "atendimento",
    "agenda",
    "vendas",
    "alunos",
    "turmas",
    "proximos passos",
)

CRM_ALLOWED_REASON_VALUES = (
    "lead_used_or_asked_crm",
    "approved_template_requires_crm",
    "category_name_needed",
)

DEMO_CUSTOMER_FACING_CONCEPT = "commercial_product_demo"

DEMO_EQUIVALENT_TERMS = (
    "commercial demo",
    "product demo",
    "demo",
    "demonstration",
    "ver funcionando",
)

DEMO_OUT_OF_SCOPE_TERMS = (
    "openai technical reference demo",
    "technical demo",
    "video production",
    "visual demo assets",
)

FORBIDDEN_DEMO_SCOPE_FIELDS = frozenset(
    {
        "demo_asset",
        "demo_assets",
        "demo_video",
        "openai_demo",
        "technical_demo",
        "video_demo",
        "video_production",
        "visual_demo_assets",
    }
)

IDENTITY_CONTACT_FACT_KEYS = frozenset(
    {
        "city",
        "city_state",
        "contact",
        "contact_path",
        "email",
        "first_name",
        "lead_name",
        "name",
        "person_name",
        "phone",
        "profile_name",
        "state",
        "studio_name",
        "whatsapp_phone",
    }
)

_SOURCE_RELIABILITY_COMPATIBILITY = {
    "channel_metadata": {"channel_provided", "internal"},
    "operator": {"operator_provided"},
    "sales_inbox_projection": {"channel_provided", "inferred", "unverified"},
    "user_message": {"customer_provided", "inferred", "unverified"},
    "official_product_knowledge": {"internal"},
}


def _has_evidence(evidence: list[str]) -> bool:
    return any(item.strip() for item in evidence)


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class InboundTurn(StrictModel):
    message_id: str
    idempotency_key: str
    text: str | None = None
    message_type: Literal["text", "unsupported_media", "postback"] = "text"
    timestamp: str | None = None


class ProductKnowledgeRef(StrictModel):
    key: str
    source: Literal["official_product_knowledge", "spec_006_product_contract"]
    version: str | None = None
    value: Any | None = None
    excerpt: str | None = None
    missing: bool = False
    renderable: bool = False
    evidence: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def known_facts_include_payload(self) -> ProductKnowledgeRef:
        if self.renderable:
            raise ValueError("product knowledge refs are source material, not renderable text")
        if self.missing:
            if self.value is not None or self.excerpt is not None:
                raise ValueError("missing product knowledge refs cannot include payload")
            return self
        if self.value is None and self.excerpt is None:
            raise ValueError("product knowledge refs require value or excerpt unless missing")
        return self


class TurnFact(StrictModel):
    key: str
    value: Any
    source: Literal[
        "user_message",
        "channel_metadata",
        "operator",
        "memory",
        "sales_inbox_projection",
        "official_product_knowledge",
    ]
    reliability: Literal[
        "customer_provided",
        "operator_provided",
        "channel_provided",
        "inferred",
        "unverified",
        "internal",
    ]
    renderable: bool = False
    confidence: Confidence = "medium"
    evidence: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def internal_facts_are_not_renderable(self) -> TurnFact:
        if self.source == "channel_metadata" and self.renderable:
            raise ValueError("channel metadata facts must never be renderable")
        if self.reliability == "internal" and self.renderable:
            raise ValueError("internal facts must never be renderable")
        allowed_reliability = _SOURCE_RELIABILITY_COMPATIBILITY.get(self.source)
        if allowed_reliability is not None and self.reliability not in allowed_reliability:
            raise ValueError("fact source and reliability are not compatible")
        if self.key in IDENTITY_CONTACT_FACT_KEYS:
            if self.reliability == "customer_provided" and not self.evidence:
                raise ValueError("customer-provided identity/contact facts require evidence")
            if (
                self.source == "sales_inbox_projection"
                and self.reliability in {"customer_provided", "operator_provided"}
            ):
                raise ValueError(
                    "projected identity/contact facts cannot be confirmed identity"
                )
        return self


class TurnContext(StrictModel):
    schema_version: str = "011.0"
    turn_id: str
    conversation_id: str
    agent_key: str
    channel: Channel
    inbound: InboundTurn
    facts: list[TurnFact] = Field(default_factory=list)
    product_knowledge: list[ProductKnowledgeRef] = Field(default_factory=list)
    compact_memory: list[dict[str, Any]] = Field(default_factory=list)
    recent_transcript: list[dict[str, Any]] = Field(default_factory=list)
    diagnostic_ledger: list[dict[str, Any]] = Field(default_factory=list)
    waitlist_state: dict[str, Any] = Field(default_factory=dict)
    demo_state: dict[str, Any] = Field(default_factory=dict)
    handoff_state: dict[str, Any] = Field(default_factory=dict)
    sales_inbox_inputs: dict[str, Any] = Field(default_factory=dict)


class NumericInterpretation(StrictModel):
    raw_text: str
    kind: Literal["plan_price", "student_count", "phone", "date_time", "unknown_number"]
    value: int | float | str
    currency: Literal["BRL"] | None = None
    evidence: list[str] = Field(default_factory=list)
    confidence: Confidence = "medium"

    @model_validator(mode="after")
    def numeric_interpretation_requires_evidence(self) -> NumericInterpretation:
        if not _has_evidence(self.evidence):
            raise ValueError("numeric interpretations require evidence")
        return self


class DiagnosticLedgerItem(StrictModel):
    question_key: Literal[
        "active_students_or_size",
        "main_pain",
        "pain_detail",
        "current_process",
        "priority",
        "urgency",
    ]
    status: Literal[
        "missing",
        "answered",
        "inferred_from_prior_message",
        "ambiguous",
        "refused",
        "not_applicable",
    ]
    answer_value: str | None = None
    evidence: list[str] = Field(default_factory=list)
    confidence: Confidence = "low"
    may_ask_again: bool = False


class DiagnosticDecision(StrictModel):
    action: Literal[
        "none",
        "offer",
        "start",
        "ask_next",
        "complete",
        "insufficient_evidence",
    ] = "none"
    ledger_updates: list[DiagnosticLedgerItem] = Field(default_factory=list)
    next_question_key: str | None = None
    final_fields: dict[str, Any] = Field(default_factory=dict)


class DemoDecision(StrictModel):
    customer_facing_concept: Literal["commercial_product_demo"] = (
        "commercial_product_demo"
    )
    status: Literal[
        "not_offered",
        "offered",
        "viewed_or_asked",
        "reacted_positive",
    ] = "not_offered"
    next_step: Literal[
        "none",
        "offer_demo",
        "ask_demo_reaction",
        "follow_positive_demo_interest",
    ] = "none"


class WaitlistDecision(StrictModel):
    eligibility: Literal["unknown", "not_eligible", "eligible"] = "unknown"
    status: Literal["none", "offered", "pending_details", "joined", "declined"] = "none"
    missing_details: list[str] = Field(default_factory=list)


class HandoffDecision(StrictModel):
    status: Literal["none", "requested", "active", "resumed"] = "none"
    reason: str | None = None


class LanguagePolicyDecision(StrictModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    language_register: Literal["studio_owner_practical"] = Field(alias="register")
    crm_term_policy: Literal["avoid_by_default", "allowed_with_evidence"]
    crm_allowed_reasons: list[
        Literal[
            "lead_used_or_asked_crm",
            "approved_template_requires_crm",
            "category_name_needed",
        ]
    ] = Field(default_factory=list)
    crm_evidence: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def crm_allowance_requires_reason_and_evidence(self) -> LanguagePolicyDecision:
        if self.crm_term_policy == "avoid_by_default":
            if self.crm_allowed_reasons or _has_evidence(self.crm_evidence):
                raise ValueError("CRM evidence is allowed only when CRM term policy allows it")
            return self

        if not self.crm_allowed_reasons:
            raise ValueError("CRM term allowance requires an allowed reason")
        if not _has_evidence(self.crm_evidence):
            raise ValueError("CRM term allowance requires evidence")
        return self


class TemplateVariableValue(StrictModel):
    kind: Literal["short_text", "long_text", "number", "boolean", "enum", "list", "url"]
    value: Any
    source: Literal[
        "user_message",
        "channel_metadata",
        "official_product_knowledge",
        "spec_006_product_contract",
        "diagnostic_ledger",
        "runtime_state",
        "model_decision",
    ]
    evidence: list[str] = Field(default_factory=list)
    max_length: int | None = None

    @model_validator(mode="after")
    def value_respects_declared_shape(self) -> TemplateVariableValue:
        if not _has_evidence(self.evidence):
            raise ValueError("template variables require evidence")
        if self.kind == "long_text" and self.max_length is None:
            raise ValueError("long_text variables require max_length")
        return self


FORBIDDEN_TEMPLATE_VARIABLE_NAMES = {
    "message_text",
    "freeform_response",
    "assistant_reply",
    "assistant_message",
    "response_text",
    "full_response",
}


class RenderPlanItem(StrictModel):
    template_id: str
    channel: Channel | None = None
    variables: dict[str, TemplateVariableValue] = Field(default_factory=dict)

    @field_validator("variables")
    @classmethod
    def reject_whole_response_variables(
        cls, value: dict[str, TemplateVariableValue]
    ) -> dict[str, TemplateVariableValue]:
        forbidden = sorted(FORBIDDEN_TEMPLATE_VARIABLE_NAMES.intersection(value))
        if forbidden:
            raise ValueError(f"forbidden whole-response template variables: {', '.join(forbidden)}")
        return value


class RenderPlan(StrictModel):
    items: list[RenderPlanItem] = Field(default_factory=list)
    chunk_policy: Literal["default", "whatsapp_max_3", "staged_diagnostic", "none"] = "default"


class PolicyChecks(StrictModel):
    direct_question_answered_first: bool
    diagnostic_timing_ok: bool
    waitlist_timing_ok: bool
    official_facts_only: bool
    no_internal_text_leak: bool
    no_early_contact_capture: bool
    no_human_overlap: bool


class DirectQuestionDecision(StrictModel):
    present: bool = False
    answered_first: bool = False
    answer_obligations: list[str] = Field(default_factory=list)


class CapturedSlot(StrictModel):
    key: str
    value: Any
    evidence: list[str] = Field(default_factory=list)
    confidence: Confidence = "medium"

    @model_validator(mode="after")
    def captured_slots_require_evidence(self) -> CapturedSlot:
        if not _has_evidence(self.evidence):
            raise ValueError("captured slots require evidence")
        return self


class ActionIntentDecision(StrictModel):
    status: str = "none"
    details: dict[str, Any] = Field(default_factory=dict)


class ConductorActionDecision(StrictModel):
    schema_version: Literal["011.action_decision.v1"]
    decision_id: str = Field(default_factory=lambda: f"action_{uuid4().hex}")
    turn_id: str
    conversation_id: str
    channel: Channel
    agent_key: str
    selected_action: str
    interpreted_intents: list[str] = Field(default_factory=list)
    direct_question: DirectQuestionDecision = Field(default_factory=DirectQuestionDecision)
    captured_slots: list[CapturedSlot] = Field(default_factory=list)
    product_fact_keys_used: list[str] = Field(default_factory=list)
    numeric_interpretations: list[NumericInterpretation] = Field(default_factory=list)
    diagnostic_intent: ActionIntentDecision = Field(default_factory=ActionIntentDecision)
    demo_intent: ActionIntentDecision = Field(default_factory=ActionIntentDecision)
    waitlist_intent: ActionIntentDecision = Field(default_factory=ActionIntentDecision)
    handoff_intent: ActionIntentDecision = Field(default_factory=ActionIntentDecision)
    reply_goal: str
    confidence: Confidence = "medium"
    evidence: list[str] = Field(default_factory=list)
    needs_clarification: bool = False
    repair_hints: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def action_decision_requires_evidence(self) -> ConductorActionDecision:
        if not _has_evidence(self.evidence):
            raise ValueError("action decision requires evidence")
        return self


class ConductorDecision(StrictModel):
    schema_version: str
    decision_id: str = Field(default_factory=lambda: f"decision_{uuid4().hex}")
    turn_id: str
    conversation_id: str
    channel: Channel
    agent_key: str
    role: Literal["entry", "product", "diagnostic", "waitlist", "handoff", "safety"]
    route: Literal["entry", "product", "diagnostic", "waitlist", "handoff", "safe_fallback"]
    previous_state: str
    current_state: str
    next_state: str
    detected_intents: list[str] = Field(default_factory=list)
    direct_question_present: bool = False
    direct_question_answered_first: bool = False
    facts: list[TurnFact] = Field(default_factory=list)
    numeric_interpretations: list[NumericInterpretation] = Field(default_factory=list)
    diagnostic: DiagnosticDecision = Field(default_factory=DiagnosticDecision)
    demo: DemoDecision = Field(default_factory=DemoDecision)
    waitlist: WaitlistDecision = Field(default_factory=WaitlistDecision)
    handoff: HandoffDecision = Field(default_factory=HandoffDecision)
    language_policy: LanguagePolicyDecision
    template_plan: RenderPlan
    policy_checks: PolicyChecks
    confidence: Confidence = "medium"
    repair_hints: list[str] = Field(default_factory=list)

    @field_validator("schema_version")
    @classmethod
    def schema_version_must_be_spec011(cls, value: str) -> str:
        if not value.startswith("011."):
            raise ValueError("ConductorDecision schema_version must start with 011.")
        return value

    @model_validator(mode="after")
    def extracted_facts_require_evidence(self) -> ConductorDecision:
        missing_evidence = [
            fact.key for fact in self.facts if not _has_evidence(fact.evidence)
        ]
        if missing_evidence:
            joined = ", ".join(sorted(missing_evidence))
            raise ValueError(f"conductor decision facts require evidence: {joined}")
        return self


class ValidationIssue(StrictModel):
    code: str
    severity: Severity
    message: str
    path: str | None = None


class ValidatorResult(StrictModel):
    decision_id: str
    status: Literal["passed", "repairable", "blocked", "failed"]
    errors: list[ValidationIssue] = Field(default_factory=list)
    warnings: list[ValidationIssue] = Field(default_factory=list)
    repair_attempt_count: int = 0
    final_disposition: Literal["accepted", "repaired", "blocked", "fallback"] | None = None


class RepairResult(StrictModel):
    attempted: bool = False
    attempt_count: int = 0
    status: Literal["not_needed", "repaired", "failed", "blocked"] = "not_needed"
    errors_sent: list[str] = Field(default_factory=list)
    repaired_decision: ConductorDecision | None = None
    model_usage: ModelUsage | None = None


class OutboxMessage(StrictModel):
    idempotency_key: str
    channel: Channel
    text: str
    template_id: str | None = None
    sequence: int


class OutboxPlan(StrictModel):
    messages: list[OutboxMessage] = Field(default_factory=list)
    deferred_inbound_count: int = 0


class IdentityField(StrictModel):
    key: str
    value: str
    source: Literal[
        "customer_provided",
        "operator_provided",
        "channel_provided",
        "inferred",
        "unverified",
    ]
    verified: bool = False


class SalesInboxProjection(StrictModel):
    conversation_id: str
    lead_id: str | None = None
    commercial_stage: str
    summary: str
    diagnostic_status: Literal[
        "not_started",
        "offered",
        "in_progress",
        "completed",
        "insufficient_evidence",
    ]
    waitlist_status: Literal["none", "offered", "pending_details", "joined", "declined"]
    handoff_status: Literal["none", "requested", "active", "resumed"]
    identity: list[IdentityField] = Field(default_factory=list)
    fields: dict[str, Any] = Field(default_factory=dict)


ProjectionResult = SalesInboxProjection


class ModelUsage(StrictModel):
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0

    @field_validator("model")
    @classmethod
    def model_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("model usage requires model name")
        return value

    @model_validator(mode="after")
    def usage_requires_provider_tokens(self) -> ModelUsage:
        if self.input_tokens <= 0:
            raise ValueError("model usage requires positive input_tokens")
        if self.output_tokens <= 0:
            raise ValueError("model usage requires positive output_tokens")
        if self.cost_usd < 0:
            raise ValueError("model usage cost_usd cannot be negative")
        return self


class RenderedMessage(StrictModel):
    text: str
    template_id: str | None = None
    channel: Channel | None = None
    sequence: int | None = None


class DeliveryEvent(StrictModel):
    event: str
    idempotency_key: str | None = None
    status: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class TraceRecord(StrictModel):
    trace_id: str
    turn_id: str
    input: TurnContext
    turn_situation: dict[str, Any] = Field(default_factory=dict)
    action_decision: dict[str, Any] = Field(default_factory=dict)
    action_repair_attempt_count: int = 0
    decision: ConductorDecision
    validator_result: ValidatorResult
    repair_result: RepairResult
    render_plan: RenderPlan
    rendered_messages: list[RenderedMessage]
    model_usage: ModelUsage
    runtime_state_diff: dict[str, Any]
    delivery_events: list[DeliveryEvent]
    sales_inbox_projection: SalesInboxProjection
    trace_complete: bool = True
