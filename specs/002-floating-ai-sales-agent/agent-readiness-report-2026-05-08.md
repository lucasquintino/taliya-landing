# Deprecated Readiness Report

This report is historical and predates the current lead-storage decision.

Current validation should prove:

- widget leads are stored in Sales Inbox/Postgres;
- WhatsApp leads are stored in Sales Inbox/Postgres;
- cold leads, hot leads, diagnostics and waitlist interest remain visible in Sales Inbox;
- optional n8n automation failure does not block chat, WhatsApp replies or operator actions.

Use current eval scripts and `commercial-e2e-qa-checklist.md` for new evidence.
