# Deprecated External Lead Sync Setup

This document is kept only as historical context. It is no longer an implementation or production setup guide.

Current production setup:

- Configure `DATABASE_URL` for Sales Inbox/Postgres.
- Do not configure a lead-upsert webhook for an external spreadsheet.
- Keep n8n optional for urgent lead alerts, daily digests, safety notifications and allowed follow-up automations.
- Production QA should verify that widget and WhatsApp leads appear in Sales Inbox with `externalSyncStatus`, and that n8n failures do not block chat, WhatsApp or operator actions.

Use `runtime-configuration.md`, `internal-sales-inbox.md` and `commercial-runtime-env-map.md` for current setup.
