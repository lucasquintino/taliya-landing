# Sales Inbox Contract: Taliya Commercial Agent

**Status**: Binding for implementation.  
**Purpose**: Guarantee the internal Sales Inbox has a complete and useful record for every meaningful lead conversation.

## Core Rule

Every meaningful turn must update Sales Inbox. Sales Inbox completeness is part of agent correctness, not a secondary dashboard improvement.

## Required Lead Identity Fields

- lead id;
- channel: widget or WhatsApp;
- source path/source label/UTM when available;
- WhatsApp provider ids when available;
- verified person name, only when the lead supplied or confirmed a real person name;
- unverified profile name, if available from WhatsApp and useful for operator context;
- studio name, separate from person name;
- city/state if known;
- contact path: WhatsApp, widget, email, or unknown;
- phone/email when legitimately available from the channel or provided by the lead.

## Required Conversation Fields

- full transcript with inbound/outbound direction;
- message timestamps;
- delivery status;
- current state;
- previous state;
- proposed next state;
- detected intents;
- direct-question status;
- current specialist route;
- template IDs rendered;
- channel delivery plan;
- guardrails fired;
- fallback used, if any;
- handoff status.

## Required Lead Fact Fields

- main pain;
- current process;
- scale/active students/lead volume signal;
- priority;
- urgency;
- plan-fit context;
- demo status and demo reaction, when available;
- objections/concerns;
- source/origin statement, for example Instagram;
- confidence and evidence for each fact.

## Required Diagnostic Fields

- diagnostic status;
- diagnostic answer ledger;
- answered questions;
- missing/unresolved questions;
- evidence used;
- internal main bottleneck;
- customer-facing pain/context reading;
- likely cause;
- first recommended step;
- CRM base/routine recommended before agents;
- indicated Taliya routines/agents;
- for each indicated routine/agent: pain resolved, recommendation reason, and practical action;
- final plan or range recommendation;
- final demo next-step line;
- confidence;
- unknowns;
- final demo next-step question;
- delivered timestamp.

## Required Demo Fields

- demo status: not offered, offered, viewed/asked, reacted positive, or unknown;
- demo offered timestamp;
- demo channel/rendering: widget CTA/button or WhatsApp official link;
- official demo link/source version used;
- lead reaction to demo, if any;
- whether demo reaction contributed to waitlist eligibility;
- latest demo next-step question shown to the lead.

## Required Waitlist Fields

- waitlist status: none, eligible, offered, pending data, joined, declined;
- evidence of clear contract intent;
- offered timestamp;
- joined timestamp;
- missing fields;
- studio name if known;
- city/state if known;
- best contact path;
- context summary;
- priority;
- idempotency key or equivalent duplicate-prevention marker.

## Required Product Knowledge Fields

- product source version;
- product keys used;
- price/plan/link/demo/availability facts answered;
- unsupported facts requested;
- whether the answer was complete or needed human follow-up.
- for product-followup delta routes, product keys used may include `how_it_works`, `routine_areas`, `whatsapp_scope`, `integration_scope`, `comparison_spreadsheet`, `comparison_management_system`, `security_and_data`, `availability_and_onboarding`, and `out_of_profile`.

## Required Product Follow-Up Fields

For new routes introduced by [product-followup-delta-contract.md](./product-followup-delta-contract.md), Sales Inbox must preserve enough context for an operator to understand the conversation without reading raw traces:

- latest product-followup intent, when present: `product_how_it_works`, `comparison_current_tool`, `integration_scope_question`, `trust_security_question`, `out_of_profile`, `conversation_resume`, `general_objection`, or `diagnostic_refusal`;
- selected template ids;
- product knowledge keys used;
- whether post-diagnostic context was used;
- post-diagnostic summary fields used, if any: recommended area, recommended plan/range, demo status, waitlist status;
- unsupported fact or integration requested, if any;
- whether human confirmation was offered because official facts were missing;
- guardrail flags for unsupported promises, no-CRM lay-copy, sensitive data, or diagnostic refusal.

## Required Runtime/Cost Fields

- agent key;
- agent family;
- owner scope;
- trace id/run id when available;
- model used;
- token usage when available;
- cost estimate;
- latency;
- JSON repair attempt count;
- validator repair status;
- error class when applicable.

## Required Operator Fields

- lead summary;
- next recommended operator action;
- reason for action;
- human pause/resume state;
- handoff reason;
- risk flags;
- missing data;
- last meaningful lead intent.

## Completeness Tests

Sales Inbox completeness must be tested for:

- cold greeting;
- source/Instagram opening;
- price question;
- plan-fit question;
- pain-first message;
- diagnostic in progress;
- diagnostic completed;
- demo offered;
- demo already offered before diagnostic completion;
- post-demo reaction;
- post-diagnostic question;
- direct buying intent;
- waitlist offered;
- waitlist accepted with missing data;
- waitlist joined with complete data;
- human handoff;
- paused human conversation;
- duplicate webhook;
- invalid JSON fallback.
- "como funciona" product explanation;
- post-diagnostic follow-up using saved diagnostic context;
- comparison with spreadsheet/current system/competitor;
- WhatsApp Business/integration scope question;
- security/data question;
- out-of-profile lead;
- diagnostic refusal.

Passing a conversational eval without the corresponding Sales Inbox record is not acceptable.
