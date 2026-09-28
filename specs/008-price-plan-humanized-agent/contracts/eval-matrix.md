# Eval Matrix Contract

Every automated eval case must record:

- `id`
- `title`
- `channels`
- `initialState`
- `turns`
- `expectedText`
- `forbiddenText`
- `expectedConversionPath`
- `expectedCommercialStage`
- `expectedDiagnosticStatus`
- `expectedWaitlistStatus`
- `expectedPriority`
- `expectedLeadFields`
- `deliveryAssertions`
- `salesInboxAssertions`
- `usesRealAgentRuntime`
- `usageSummary`

Acceptance evals for conversation quality must use the real agent/runtime path. Deterministic mocks may appear only in infrastructure checks and must be labeled as non-acceptance tests.

## Price Cases

- `PRICE-SOURCE-OF-TRUTH-MATCH`: agent price/plan answer matches `/pilates/planos` or shared commercial config.
- `PRICE-COLD-FIRST-MSG`: "Quanto custa?" as first message.
- `PRICE-AFTER-NAME`: name known, then "Qual valor?"
- `PRICE-AFTER-PAIN`: pain known, then "E quanto custa?"
- `PRICE-DIAG-OFFERED`: diagnostic offered, then "Antes, quanto custa?"
- `PRICE-IN-DIAGNOSTIC`: in-progress diagnostic, then "Quero saber valores primeiro."
- `PRICE-AFTER-DIAG`: diagnostic complete, then "Quanto custa?"
- `PRICE-AFTER-DEMO`: demo discussed, then "Quanto fica?"

## Plan Cases

- `PLANS-COLD`: "Quais sao os planos?"
- `PLANS-VIEW-DIRECT`: "Quero ver planos."
- `PLANS-COMPARE`: "Quero comparar os planos."
- `PLANS-QUICK-REPLY-NO-DIAG`: quick reply `view_plans` without diagnostic.
- `PLANS-QUICK-REPLY-WITH-DIAG`: quick reply `view_plans` after diagnostic.
- `PLANS-PAGE-ENTRY`: conversation started from plans page context.

## Recommendation Cases

- `PLAN-RECOMMEND-NO-DIAG`: "Qual plano faz sentido?"
- `PLAN-RECOMMEND-WITH-PAIN-ONLY`: pain exists but no diagnostic.
- `PLAN-RECOMMEND-WITH-DIAG`: diagnostic complete.
- `PLAN-RECOMMEND-AFTER-DEMO`: demo positive/discussed.

## Buying Cases

- `BUY-NO-DIAG`: "Quero contratar" with no context.
- `BUY-WITH-PAIN`: pain exists, no diagnostic.
- `BUY-AFTER-DIAG-POSITIVE`: diagnostic complete and positive.
- `BUY-AFTER-DEMO-POSITIVE`: demo positive.
- `BUY-WAITLIST-CURRENT-REALITY`: strong interest routes to limited-studios waitlist.
- `DEMO-UNAVAILABLE-HONEST-ROUTE`: demo requested while not configured; agent does not invent demo and routes honestly.

## Objection Cases

- `PRICE-EXPENSIVE`
- `PRICE-DISCOUNT`
- `PRICE-FREE`
- `PRICE-TRIAL`
- `PRICE-ROI`
- `PRICE-SMALL-STUDIO`
- `PRICE-ONLY-ONE-PAIN`
- `PRICE-MANY-PAINS`

## Delivery And Humanization Cases

- `DELIVERY-FIRST-SPLIT`
- `DELIVERY-TYPING-BEFORE-EACH-WIDGET`
- `DELIVERY-TYPING-BEFORE-EACH-WHATSAPP`
- `DELIVERY-PROPORTIONAL-DELAY-WIDGET`
- `DELIVERY-PROPORTIONAL-DELAY-WHATSAPP`
- `DELIVERY-NO-LONG-BLOCKS`
- `DELIVERY-NO-USER-ECHO`
- `DELIVERY-NO-INSTANT-DRY-REPLY`
- `HUMAN-PRICE-COLD`
- `HUMAN-PLANS-DIRECT`
- `HUMAN-RECOMMEND-NO-DIAG`
- `HUMAN-OBJECTION-EXPENSIVE`
- `HUMAN-ONLY-RESEARCHING`
- `HUMAN-DEMO-NEGATIVE`

## Operational Cases

- `REAL-RUNTIME-USAGE-REPORTED`
- `REAL-RUNTIME-COST-GUARDRAIL`
- `ABUSE-WA-RATE-LIMIT`
- `ABUSE-WIDGET-RATE-LIMIT`
- `ABUSE-GLOBAL-DAILY-CAP`
- `ABUSE-LIMIT-REASON-STORED`
- `ABUSE-MID-CONVERSATION-LIMIT`
- `ABUSE-SPAM-REPEATED-MESSAGES`
- `HUMAN-ECHO-PAUSES-AI`
- `HUMAN-ACTIVE-NO-AI-REPLY`
- `HUMAN-REENABLE-AI`
- `HUMAN-REENABLE-AI-AUDIT`
- `MERGE-WIDGET-TO-WA-BY-PHONE`
- `MERGE-WA-TO-WIDGET-BY-PHONE`
- `MERGE-BY-EMAIL`
- `NO-MERGE-BY-NAME-ONLY`
- `MERGE-PRESERVES-HISTORY`
- `WAITLIST-MISSING-STUDIO`
- `WAITLIST-MISSING-CITY`
- `WAITLIST-MISSING-FIELDS-VISIBLE`
- `WAITLIST-WA-PHONE-AUTO-FILLED`
- `WAITLIST-JOINED-HAS-MINIMUM-DATA`
- `WAITLIST-NO-JOIN-WITHOUT-CONTACT`
- `WAITLIST-PRESERVES-DIAGNOSTIC-SUMMARY`
- `PRIORITY-COLD-PRICE-ONLY`
- `PRIORITY-WARM-PAIN`
- `PRIORITY-WARM-DIAGNOSTIC-STARTED`
- `PRIORITY-HOT-WAITLIST-JOINED`
- `PRIORITY-HOT-BUY-WITH-CONTEXT`
- `PRIORITY-MANUAL-HUMAN-REQUEST`
- `MEDIA-WA-AUDIO-COLD`
- `MEDIA-WA-IMAGE-COLD`
- `MEDIA-WA-AUDIO-AFTER-PAIN`
- `MEDIA-WA-DOCUMENT-IN-DIAGNOSTIC`
- `MEDIA-DOES-NOT-START-DIAGNOSTIC`
- `WEBHOOK-VALIDATION-PRESERVED`
- `WEBHOOK-PHONE-NUMBER-ID-MAPPED`
- `WEBHOOK-PROVIDER-MESSAGE-IDEMPOTENCY`
- `SEND-ERROR-WHATSAPP-OPERATOR-VISIBLE`
- `SEND-ERROR-WIDGET-OPERATOR-VISIBLE`
- `FUNNEL-PRICE-EVENT`
- `FUNNEL-DIAGNOSTIC-ACCEPTED-EVENT`
- `FUNNEL-WAITLIST-JOINED-EVENT`
- `FUNNEL-HUMAN-PAUSED-EVENT`
- `FUNNEL-REPORT-VISIBLE`
- `FUNNEL-NO-DUPLICATE-ON-RETRY`
- `HANDOFF-HUMAN-REQUEST`
- `HANDOFF-WAITLIST-JOINED`
- `HANDOFF-BUY-WITH-CONTEXT`
- `HANDOFF-RATE-LIMIT-MID-CONVERSATION`
- `HANDOFF-UNKNOWN-INTEGRATION-HOT-LEAD`
- `CLOSE-COLD-NO-RESPONSE`
- `CLOSE-DIAG-OFFERED-NO-RESPONSE`
- `CLOSE-USES-CONFIGURED-WINDOW`
- `CLOSE-WAITLIST-DECLINED`
- `CLOSE-WAITLIST-JOINED`
- `CLOSE-HUMAN-ACTIVE`
- `CLOSE-RATE-LIMIT-ERROR`

## Required Gates

- Price/plan matrix: 100%.
- Delivery/humanization matrix: 100%.
- Existing commercial matrix: 100%.
- WhatsApp webhook evals: 100%.
- Sales humanization evals: 100%.
- Lead pipeline evals: 100%.
- Build, lint and typecheck pass.
