# Deprecated Readiness Audit

This document is historical. It predates the current lead-storage decision and is not an implementation source of truth.

Current decision:

- Sales Inbox/Postgres stores all leads and commercial state.
- n8n is optional for alerts, digests and allowed follow-up automations.
- External CRM/spreadsheet lead sync is disabled for this phase.

Use `spec.md`, `plan.md`, `tasks.md`, `internal-sales-inbox.md`, `runtime-configuration.md` and `commercial-e2e-qa-checklist.md` for current launch checks.
