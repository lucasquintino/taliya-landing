# Feature Specification: Security, Code And Data Governance

**Feature Branch**: `codex/005-security-code-data`
**Created**: 2026-05-08
**Status**: Draft for review
**Input**: Define an exclusive security specification for everything related to security, code safety, data protection, AI agent guardrails, external integrations, WhatsApp, billing, internal tools and the future real SaaS.

## Purpose

This spec defines the security baseline for the whole product, including:

- public landing pages;
- AI sales attendant;
- WhatsApp channel;
- custom-agent diagnostic report;
- Sales Inbox;
- billing/subscription flows;
- onboarding;
- future multi-tenant SaaS web app;
- future mobile app;
- external integrations such as OpenAI, Meta WhatsApp, n8n and payment providers.

It is a cross-cutting spec. Feature specs may define their own local security requirements, but when there is conflict, this spec sets the minimum security bar.

## Security Principles

1. Server-side trust: secrets, provider calls, billing verification, AI prompts and authorization decisions stay on the server.
2. Least privilege: every user, operator, API key, integration and background job gets only the access needed for its job.
3. Tenant isolation by design: future paying studios must never access another studio's data through UI, API, jobs, caches, files, analytics or agent context.
4. Validate every boundary: browser input, AI input/output, webhooks, n8n payloads, WhatsApp payloads, billing events and uploaded/imported data are untrusted until validated.
5. Minimize sensitive data: collect, store, log and sync only what is necessary for the current business purpose.
6. Human confirmation for high-risk actions: payment, destructive, external-visible or customer-impacting actions require trusted gates and auditability.
7. Safe failure: integration failures must not leak secrets, duplicate actions, mark subscriptions incorrectly or leave the operator blind.
8. Audit critical actions: operator takeover, payment state changes, checkout link sends, AI pause/resume, lead status changes, entitlement changes and admin actions must be traceable.

## Data Classes

| Class | Examples | Rules |
| --- | --- | --- |
| Public content | landing copy, plan names, public prices, FAQ | Can be rendered publicly, but must come from trusted configuration where required. |
| Commercial lead data | name, WhatsApp, email, studio, city/state, pain, interested plan, safe summary | Store only when there is purpose/context; Sales Inbox/Postgres is the source of truth; optional n8n payloads receive safe summaries only. |
| Conversation data | chat turns, WhatsApp messages, AI metadata, summaries | Prefer safe summaries and structured metadata; avoid full raw transcript storage by default. |
| Sensitive customer/student data | health details, payment credentials, private student records, full billing docs | Do not request or store in landing/agent flows. Future SaaS access must be scoped and protected. |
| Secrets | OpenAI key, Meta token, webhook secrets, n8n URLs, database credentials, billing secrets | Server-side env only; never expose to browser, logs, screenshots, client bundles or committed files. |
| Payment state | checkout intent, invoice/payment status, subscription, entitlement | Only trusted billing provider/webhook can confirm paid/active state. |
| Tenant data | studio config, agents, students, conversations, agenda, billing owner | Must be scoped by tenant/workspace and role in the real SaaS. |

## Trust Boundaries

- Browser to Next.js routes.
- AI model/provider to server-side response parser.
- WhatsApp provider webhooks to server.
- Payment provider webhooks to billing routes.
- n8n webhooks and automation jobs.
- Sales Inbox operator UI to server actions.
- Future SaaS tenant UI to application services/repositories.
- Background jobs to persistence and external providers.

Every boundary must have explicit validation, authentication or signature verification where applicable, error handling and safe logging.

## Functional Requirements

- **FR-001**: Secrets MUST live only in server-side environment/configuration and MUST NOT be hardcoded, committed, logged, exposed to Client Components or sent to the browser.
- **FR-002**: Public client code MUST NOT call OpenAI, Meta WhatsApp, n8n, database or billing provider APIs directly with privileged credentials.
- **FR-003**: All public API routes MUST validate request method, content type, payload shape, size limits and allowed values before business logic.
- **FR-004**: Webhook routes MUST verify provider authenticity using the best available signature/token/shared-secret mechanism and reject unverifiable production events.
- **FR-005**: Webhook processing MUST be idempotent by stable provider event/message IDs to prevent duplicate replies, duplicate leads, duplicate checkout effects or duplicate entitlements.
- **FR-006**: All external URLs used for checkout, plans, WhatsApp or redirects MUST come from trusted configuration or allowlisted destinations, never from raw user/model output.
- **FR-007**: The system MUST NOT collect card numbers, payment credentials, private billing documents or sensitive student health details in landing, chat, WhatsApp or Sales Inbox flows.
- **FR-008**: AI prompts, tool instructions, guardrail policies and internal routing logic MUST NOT be disclosed to visitors or synced to third-party lead tools.
- **FR-009**: AI inputs MUST pass guardrails for prompt injection, off-topic abuse, sensitive-data attempts, unsafe commitments and unsupported requests before tool/action execution.
- **FR-010**: AI outputs MUST be parsed/validated against structured schemas before they can drive CTAs, tracking, lead updates, WhatsApp sends, checkout links or operator actions.
- **FR-011**: AI agents MUST NOT perform high-risk actions directly. Checkout send, WhatsApp human takeover, subscription activation, entitlement changes and destructive/admin actions require server-side gates and/or operator/billing confirmation.
- **FR-012**: The Sales Inbox MUST require internal authentication/authorization before showing leads, messages, operator actions or audit events.
- **FR-013**: Sales Inbox operator actions MUST be authorized server-side and audited with actor, action, target lead/session, timestamp and safe before/after metadata where applicable.
- **FR-014**: Operator replies through WhatsApp MUST be sent by the server-side provider adapter and MUST NOT expose provider credentials or arbitrary provider payloads to the browser.
- **FR-015**: Human takeover state MUST be enforced server-side so the AI cannot continue WhatsApp replies while `human_active` unless the operator explicitly resumes it.
- **FR-016**: Lead merge MUST use strong identifiers such as `leadId`, verified/provided email, normalized WhatsApp number, provider contact ID or explicit session continuation token; it MUST NOT merge by studio name, pain, IP or browser fingerprint alone.
- **FR-017**: n8n MUST receive safe summaries and structured metadata by default, not full raw transcripts or secrets.
- **FR-018**: n8n MUST NOT bypass opt-out, human pause, template approval, payment confirmation, entitlement enforcement or provider idempotency.
- **FR-019**: WhatsApp proactive/out-of-window messages MUST be blocked unless the exact Meta template is approved, configured, eligible and not opted out.
- **FR-020**: Billing/payment state MUST be confirmed only by trusted billing provider responses/webhooks; landing, chat, plan page or Sales Inbox click events MUST NOT activate a subscription.
- **FR-021**: Future tenant-scoped SaaS APIs MUST verify tenant membership and role server-side for every object-level read/write.
- **FR-022**: Future tenant-scoped background jobs, caches, search indexes, analytics and files MUST carry tenant/workspace scope and MUST NOT mix data across studios.
- **FR-023**: Admin/operator impersonation or support access to customer tenants MUST be explicit, tightly permissioned and audited.
- **FR-024**: Logs, analytics, traces and error reports MUST redact or avoid secrets, payment data, unnecessary PII, prompt internals and sensitive customer/student content.
- **FR-025**: Rate limits and abuse controls MUST exist for public chat, custom diagnostic, WhatsApp webhook processing, checkout-intent creation and operator actions where applicable.
- **FR-026**: The system MUST fail safely when OpenAI, Meta WhatsApp, n8n, database or billing providers are unavailable: record safe status, avoid duplicate side effects and keep operator-visible state where possible.
- **FR-027**: Frontend rendering MUST avoid unsafe HTML/markdown execution, unsafe URL rendering and XSS-prone DOM APIs for visitor-provided or AI-provided content.
- **FR-028**: State-changing browser requests MUST use appropriate authentication/session checks and CSRF/same-site protections where applicable.
- **FR-029**: File import/upload features in the future SaaS MUST define size, type, scanning/storage rules and access controls before implementation.
- **FR-030**: Dependency additions MUST be reviewed for supply-chain risk, client bundle exposure, maintenance status and need; security-relevant updates require regression checks.
- **FR-031**: Each production release touching auth, billing, WhatsApp, AI tools, tenant data, webhooks or Sales Inbox MUST include a security review checklist before launch.
- **FR-032**: Security decisions that affect data retention, deletion, export, incident response or compliance MUST be documented before the real SaaS production launch.

## AI Agent Guardrails

AI agents may guide, explain, diagnose and recommend. They must not become an unchecked authority over data or external actions.

Required guardrail layers:

- input guardrail: block prompt injection, policy exfiltration, unsafe data requests and irrelevant abuse;
- context guardrail: only provide trusted product/config/tenant context that the current user/session may access;
- tool guardrail: use allowlisted tools only, with schemas, scopes, idempotency and confirmation gates;
- output guardrail: prevent false claims, leaked secrets, unsupported promises and unsafe instructions;
- operations guardrail: log guardrail decisions and alert on repeated abuse.

## Security Acceptance Criteria

- **SC-001**: A secrets audit finds no provider keys, webhook secrets, billing secrets, database credentials or n8n credentials in client bundles, source files, logs or screenshots.
- **SC-002**: Webhook tests reject invalid signatures/tokens and accept valid provider events.
- **SC-003**: Duplicate WhatsApp and billing webhook events do not duplicate replies, leads, checkout state or entitlements.
- **SC-004**: Prompt-injection evals fail to reveal system prompts, private policies, secrets or unauthorized internal data.
- **SC-005**: AI output validation prevents malformed/model-invented CTAs, arbitrary URLs and unsupported checkout/handoff actions.
- **SC-006**: Sales Inbox cannot be opened or used without internal authorization.
- **SC-007**: Operator takeover pauses WhatsApp AI replies until explicit resume.
- **SC-008**: n8n payload samples contain safe summaries/metadata and no full raw transcript by default.
- **SC-009**: A future tenant-isolation test confirms a user from Studio A cannot read or mutate Studio B data by changing IDs, routes, filters or API payloads.
- **SC-010**: Payment/entitlement tests confirm only billing confirmation can activate a plan.
- **SC-011**: XSS tests with visitor-provided and AI-provided content render as safe text or sanitized output.
- **SC-012**: Production launch checklist includes security review for auth, authorization, webhooks, secrets, logs, AI guardrails, Sales Inbox, WhatsApp, billing and tenant isolation.

## Out Of Scope For This Spec

- Specific payment provider implementation details.
- Final database schema for the future SaaS.
- Final auth provider choice.
- Full LGPD legal policy text.
- External penetration test execution.

These belong in implementation plans or legal/security review before production, but this spec defines the minimum product/security behavior they must satisfy.
