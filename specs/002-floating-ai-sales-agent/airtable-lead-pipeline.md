# Deprecated External Lead Pipeline

This document is kept only as historical context. It is no longer an implementation source of truth.

Current decision:

- Sales Inbox backed by Postgres is the v1 source of truth for leads.
- n8n is optional and limited to alerts, digests and allowed follow-up automations.
- External CRM/spreadsheet lead upsert is disabled for this phase.
- The agent brain, WhatsApp transport and Sales Inbox must not depend on any external spreadsheet pipeline.

Use `internal-sales-inbox.md`, `runtime-configuration.md`, `data-model.md` and `commercial-e2e-qa-checklist.md` for current behavior.
