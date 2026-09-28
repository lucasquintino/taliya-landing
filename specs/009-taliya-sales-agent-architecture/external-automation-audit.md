# External Automation Audit

Sales Inbox/Postgres remains the source of truth for this feature.

## n8n

n8n may receive safe alerts or digests for:

- high-intent lead alert;
- operator action notification;
- safety/fallback event.

n8n must not decide:

- prices, plans or product facts;
- lead state;
- diagnostic output;
- waitlist status;
- payment/checkout availability;
- agent routing.

## Airtable

Airtable is not part of the feature path and must not be used as a lead, waitlist, pricing, diagnostic or state source.

