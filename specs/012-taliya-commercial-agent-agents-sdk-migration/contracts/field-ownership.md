# Taliya Commercial Ops v1 - Field Ownership

`taliya-commercial-ops.v1` is the executable transport contract between the
commercial runtime, the landing gateway, Postgres/Supabase, and
`taliya-internal`.

| Data | Producer | Durable source | Internal rule |
|---|---|---|---|
| Lead identity and evidence | Runtime structured output | `sales_leads.data` and runtime state | Display evidence; never infer from prose |
| Conversation identity | Landing/WhatsApp gateway before runtime | `agent_runtime_conversations` | Join by canonical ID |
| Inbound/outbound messages | Channel gateway | `sales_lead_messages` | Preserve order, direction, delivery and safety status |
| Commercial decision | Runtime action-first output | `agent_runtime_runs.output` | Read structured fields only |
| Product sources | Runtime compiler/product knowledge | `agent_runtime_runs.output.sources` | Missing stays missing |
| Usage and cost | Runtime | `agent_runtime_model_usage` | Join by real `run_id`; do not double count |
| Acquisition events | Landing gateway | `ai_funnel_events` | Use persisted dimensions and denominators |
| Human decisions | Internal operator | `internal.*` overlays | Never overwrite raw agent/channel data |

## Canonical identity

Every meaningful turn carries `lead_id`, `conversation_id`, inbound
`message_id`, `run_id`, and `trace_id`. Channel-specific IDs are additional
references, never replacements for canonical IDs.

## Absence

Missing, not analyzed, not run, unavailable, and inconsistent are distinct
states. Consumers must not manufacture conversations, events, diagnostics,
quality approvals, sources, stages, or origins from rendered copy.

## Compatibility

Schema changes are additive within v1. A breaking field or semantic change
requires a new contract version. The runtime emits `contract_version`; the
gateway validates it before persistence, and the Internal exposes an explicit
incompatible/degraded source status instead of guessing.
