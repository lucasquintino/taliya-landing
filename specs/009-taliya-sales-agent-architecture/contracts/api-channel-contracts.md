# Contract: API And Channel Adapters

## Widget Adapter

Existing widget endpoint remains the transport boundary for browser chat. It should normalize widget events into `AgentLoopInput` and render `ChannelDeliveryPlan` back to the widget UI.

Widget adapter responsibilities:

- session id handling
- page/source metadata
- quick reply/button metadata
- rendering text messages, buttons, cards and links
- preserving existing `/pilates` layout

Widget adapter must not:

- decide commercial stage
- decide diagnostic/waitlist/handoff
- invent product facts
- bypass guardrails

## WhatsApp Adapter

Existing WhatsApp webhook remains the transport boundary for Meta/Dualhook events.

WhatsApp adapter responsibilities:

- GET verify-token challenge
- POST payload normalization
- allowed `phone_number_id`/connection validation
- stable inbound idempotency key
- provider phone/profile metadata extraction
- message delivery via Cloud API access token
- typing indicator attempt before each chunk
- proportional delay between chunks
- delivery status logging

WhatsApp adapter must not:

- ask for phone number
- decide sales logic
- merge leads by name
- send a response after human pause
- create duplicate replies for duplicate webhooks

## Channel Delivery Plan

```ts
type ChannelDeliveryPlan = {
  channel: "widget" | "whatsapp";
  messages: Array<{
    text: string;
    role: "assistant";
    kind: "text" | "link" | "card_hint";
  }>;
  widgetActions?: Array<{
    id: string;
    label: string;
    type: "quick_reply" | "open_url" | "start_diagnostic";
    url?: string;
  }>;
  whatsappDelivery?: {
    chunks: Array<{
      text: string;
      typingDelayMs: number;
    }>;
    maxChunks: 3;
    sourceLinks?: Array<{
      label: string;
      url: string;
    }>;
  };
};
```

## WhatsApp Pacing Rules

- Attempt typing before every chunk.
- Minimum delay: 1500ms.
- Target delay: 35-55ms per character.
- Maximum delay: 7000ms per chunk.
- Maximum chunks: 3 unless human-approved.
- Normal chunk length: under 320 characters.

## Media Handling

When inbound message contains only media and no reliable text:

- record media receipt;
- do not infer diagnostic facts;
- ask for a short text summary or offer human help;
- avoid downloading/storing sensitive media unless later explicitly required.

## Subscribe/Assinar Entry

Landing "Assinar" or equivalent subscribe CTA should pass `entryIntent: "buy_or_subscribe"` to the agent loop. While broad availability is closed, this must route to qualified waitlist flow, not checkout.
