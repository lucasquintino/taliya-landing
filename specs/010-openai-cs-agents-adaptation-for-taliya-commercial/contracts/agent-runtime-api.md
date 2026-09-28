# Contract: Agent Runtime API

## Overview

The Railway runtime exposes a generic API for agent runs. This feature uses only `agent_key: "taliya_commercial"`.

## Endpoint: Health

```http
GET /healthz
```

Response:

```json
{
  "ok": true,
  "service": "taliya-agent-runtime",
  "environment": "production"
}
```

## Endpoint: Run Agent Turn

```http
POST /v1/agent-runs
```

### Required Headers

```text
Content-Type: application/json
X-Taliya-Agent-Timestamp: 2026-05-22T12:00:00Z
X-Taliya-Agent-Signature: hex_hmac_sha256(timestamp + "." + raw_body)
X-Taliya-Agent-Request-Id: stable-request-id
```

Rules:

- Timestamp must be within the configured skew window. The initial value is 300 seconds.
- Signature must be computed over the exact raw body bytes received by Railway.
- Invalid HMAC rejects before any side effect.
- Duplicate request ids return the prior run result when available.

### Request Body

```json
{
  "agent_key": "taliya_commercial",
  "channel": "widget",
  "conversation": {
    "conversation_id": "conv_123",
    "lead_id": "lead_123",
    "channel_conversation_id": "widget_session_or_wa_thread",
    "source": "pilates_landing",
    "entry_intent": "price_question"
  },
  "message": {
    "idempotency_key": "widget:session:message",
    "channel_message_id": "provider_message_id",
    "type": "text",
    "text": "quanto custa e como funciona?",
    "timestamp": "2026-05-22T12:00:00Z"
  },
  "sender": {
    "name": "optional profile name",
    "whatsapp_phone": "optional e164",
    "email": null
  },
  "metadata": {
    "page_path": "/pilates",
    "utm_source": null,
    "provider": "widget"
  }
}
```

### Success Response

```json
{
  "run_id": "run_123",
  "conversation_id": "conv_123",
  "lead_id": "lead_123",
  "agent_key": "taliya_commercial",
  "current_agent": "taliya_commercial_product_agent",
  "status": "succeeded",
  "output": {
    "decision": {
      "previous_state": "new_lead",
      "current_state": "price_question",
      "next_state": "diagnostic_offered",
      "route": "product",
      "opening_type": "direct_question_opening",
      "detected_intents": ["price"],
      "direct_question_present": true,
      "direct_question_answered_first": true,
      "diagnostic_action": "offer",
      "diagnostic_allowed_now": true,
      "waitlist_allowed_now": false,
      "demo_status": "not_offered",
      "demo_next_step": "none",
      "profile_name_usage": "not_needed",
      "facts_used": ["official plan prices"],
      "facts_missing": [],
      "template_ids": ["product.price_direct", "diagnostic.offer_soft"],
      "template_variables": {
        "product.price_direct": {
          "price_summary_source": "taliya-commercial-2026-05-22"
        },
        "diagnostic.offer_soft": {
          "reason": "plan fit depends on studio context"
        }
      },
      "next_question_kind": "pain",
      "policy_checks": {
        "direct_question_answered_first": true,
        "diagnostic_timing_ok": true,
        "waitlist_timing_ok": true,
        "official_facts_only": true,
        "no_early_contact_capture": true,
        "no_whatsapp_phone_request": true,
        "no_fake_certainty": true,
        "no_human_overlap": true,
        "channel_brevity_ok": true
      }
    },
    "messages": [
      {
        "text": "Claro. Hoje os planos da Taliya para studios de Pilates comecam em ...",
        "template_id": "product.price_direct",
        "channel_hint": "widget",
        "kind": "text"
      },
      {
        "text": "Se fizer sentido, posso fazer um diagnostico gratuito rapidinho e te ajudar a comparar qual faixa combina melhor com a rotina do seu studio.",
        "template_id": "diagnostic.offer_soft",
        "channel_hint": "widget",
        "kind": "text"
      }
    ],
    "lead_facts": [],
    "diagnostic": {
      "status": "offered",
      "ledger": [],
      "facts_used": [],
      "unknowns": ["studio context for plan fit"],
      "confidence": "low",
      "next_question": null
    },
    "demo": {
      "status": "not_offered",
      "last_demo_link": null,
      "product_source_version": null,
      "lead_reaction": null,
      "contributed_to_waitlist_eligibility": false
    },
    "waitlist_action": null,
    "handoff": null,
    "sources": [
      {
        "type": "product_knowledge",
        "version": "taliya-commercial-2026-05-22"
      }
    ],
    "safety_flags": [],
    "usage": {
      "model": "gpt-5.4-mini",
      "input_tokens": 1200,
      "output_tokens": 180,
      "cost_usd": 0.00171
    }
  },
  "trace_id": "trace_123"
}
```

### Non-Reply Success Response

Used for human pause, duplicate suppression, unsupported input with no safe response, or cost cap.

```json
{
  "run_id": "run_124",
  "conversation_id": "conv_123",
  "lead_id": "lead_123",
  "agent_key": "taliya_commercial",
  "current_agent": "taliya_commercial_handoff_agent",
  "status": "human_paused",
  "output": {
    "decision": {
      "previous_state": "human_requested",
      "current_state": "human_handoff",
      "next_state": "paused_by_human",
      "route": "handoff",
      "opening_type": "none",
      "detected_intents": ["human_request"],
      "direct_question_present": false,
      "direct_question_answered_first": true,
      "diagnostic_action": "none",
      "diagnostic_allowed_now": false,
      "waitlist_allowed_now": false,
      "demo_status": "not_offered",
      "demo_next_step": "none",
      "profile_name_usage": "not_needed",
      "facts_used": [],
      "facts_missing": [],
      "template_ids": ["handoff.paused"],
      "template_variables": {
        "handoff.paused": {
          "reason": "manual WhatsApp reply detected"
        }
      },
      "next_question_kind": "handoff",
      "policy_checks": {
        "no_human_overlap": true
      }
    },
    "messages": [],
    "handoff": {
      "status": "active",
      "reason": "manual_whatsapp_reply_detected"
    },
    "sources": [],
    "safety_flags": ["human_active"],
    "usage": {
      "model": null,
      "input_tokens": 0,
      "output_tokens": 0,
      "cost_usd": 0
    }
  },
  "trace_id": "trace_124"
}
```

### Error Response

```json
{
  "error": {
    "code": "invalid_signature",
    "message": "Request signature is invalid.",
    "retryable": false
  }
}
```

Required error codes:

- `invalid_signature`
- `stale_timestamp`
- `malformed_request`
- `unknown_agent_key`
- `disabled_agent_key`
- `duplicate_in_progress`
- `product_knowledge_unavailable`
- `structured_output_invalid`
- `model_provider_timeout`
- `internal_error`

## Timeout

Next should configure `TALIYA_AGENT_RUNTIME_TIMEOUT_MS=60000`. If the timeout is hit, the channel adapter must not call the old deterministic runtime. It may send a short operational fallback or pause for human according to channel policy.

