# Intelligent Conversation Test Matrix

## Purpose

This matrix defines the smart validation set for the Taliya sales attendant on both web widget and WhatsApp. The goal is not to run every possible conversation until the waitlist. Most scenarios stop at the first important commercial decision: the assistant answered the buyer, understood the intent and chose the right next step.

## Global Acceptance Rules

- Answer the buyer's direct question before steering to the diagnostic.
- Use the free diagnostic as a natural next step, not as a barrier before answering.
- Keep language natural and consultative; avoid menu-like wording.
- Ask one short question at a time.
- Do not offer waitlist before strong interest after diagnostic, demo or explicit buying context.
- Do not invent integrations, demo availability, discounts, guarantees or timelines.
- WhatsApp replies must be separated into natural messages, must not quote the user's message and must preserve typing/delay behavior.
- Widget and WhatsApp share the same intent logic, while channel transport may differ.

## Short Entry And Triage Cases

These scenarios stop once the assistant has answered, captured or requested the minimum context and offered the correct next step.

| ID | Channels | User Signal | Stop Point | Required Outcome | Forbidden Outcome |
| --- | --- | --- | --- | --- | --- |
| `SHORT-PRICE` | widget, whatsapp | "Quanto custa?" | useful price answer + diagnostic/fit question | Mentions plan structure and asks a soft fit question | Checkout, waitlist, refusing to answer |
| `SHORT-DEMO` | widget, whatsapp | "Quero ver uma demo" | useful demo answer + context question | Explains demo purpose/availability honestly | Fake demo URL or claims demo is ready if not configured |
| `SHORT-KNOW` | widget, whatsapp | "Quero conhecer melhor" | product explanation + open question | Explains Taliya simply | Menu-like list as first answer |
| `SHORT-REPLACEMENTS` | widget, whatsapp | "Tenho problema com reposicoes" | pain recognition + diagnostic offer | Connects agenda/faltas/reposicoes and offers diagnostic | Plans/checkout/lista |
| `SHORT-WHATSAPP` | widget, whatsapp | "Meu WhatsApp esta uma bagunca" | pain recognition + diagnostic offer | Explains organization of conversations/priorities | Generic chatbot pitch |
| `SHORT-SALES` | widget, whatsapp | "Estou perdendo leads" | sales answer + follow-up question | Mentions follow-up/lead organization | Checkout/lista |
| `SHORT-FINANCE` | widget, whatsapp | "Financeiro esta dificil" | finance answer + diagnostic offer | Mentions cobranças/mensalidades/visibilidade | Unsupported accounting promises |
| `SHORT-MANAGEMENT` | widget, whatsapp | "Nao vejo o que acontece no dia" | management answer + diagnostic offer | Mentions rotina/prioridades/painel do dia | Plan push |
| `SHORT-HIRE` | widget, whatsapp | "Quero contratar" | high-intent answer + diagnostic gate | Explains small number of studios and asks to understand scenario | Immediate waitlist without context |
| `SHORT-EXISTING-SYSTEM` | widget, whatsapp | "Ja tenho sistema" | differentiation answer + gap question | Asks what current system does not solve | Attacks competitor or claims replacement blindly |
| `SHORT-RECEPTIONIST` | widget, whatsapp | "Isso substitui recepcionista?" | objection answer + diagnostic/proof question | Positions leverage/control | Says fully replaces the team |
| `SHORT-SMALL` | widget, whatsapp | "Meu studio e pequeno" | fit answer + pain question | Says fit depends on repeated routine | Disqualifies coldly |
| `SHORT-LARGE-MANUAL` | widget, whatsapp | "Tenho 120 alunos e uso caderno" | recognizes strong context + diagnostic offer | Mentions manual operation risk | Waitlist before diagnostic |
| `SHORT-RESEARCHING` | widget, whatsapp | "Estou so pesquisando" | low-pressure answer + compare question | No pressure, asks what they want to compare | Checkout/lista |
| `SHORT-INTEGRATION` | widget, whatsapp | "Integra com Google Agenda?" | honest answer + workflow question | Does not invent support | "sim, ja integra" unless configured |
| `SHORT-MEDIA` | whatsapp | image/audio inbound | safe text fallback | Asks for text summary | Runs normal diagnostic from media |

## Medium Diagnostic Entry Cases

These scenarios stop after the lead accepts the diagnostic and the assistant asks a few coherent diagnostic questions.

| ID | Channels | Pain | Stop Point | Required Outcome |
| --- | --- | --- | --- | --- |
| `MID-AGENDA` | widget, whatsapp | agenda/reposicoes | 2-3 diagnostic questions after acceptance | Does not lose state and keeps agenda context |
| `MID-WHATSAPP` | widget, whatsapp | WhatsApp/atendimento | 2-3 diagnostic questions after acceptance | Keeps WhatsApp pain and asks about size/routine |
| `MID-SALES` | widget, whatsapp | vendas/leads | 2-3 diagnostic questions after acceptance | Keeps sales context |
| `MID-FINANCE` | widget, whatsapp | financeiro/cobranca | 2-3 diagnostic questions after acceptance | Keeps finance context |
| `MID-BROAD` | widget, whatsapp | "tudo um pouco" | 2-3 diagnostic questions after acceptance | Avoids premature plan/lista |

## Canonical Long Cases

Only these go near the funnel end.

| ID | Channels | Stop Point | Required Outcome |
| --- | --- | --- | --- |
| `LONG-WA-WAITLIST` | whatsapp | waitlist accepted with studio/city | `waitlist_joined` |
| `LONG-WIDGET-WAITLIST` | widget | waitlist accepted with studio/city | `waitlist_joined` |
| `LONG-DIAG-NEGATIVE` | widget, whatsapp | negative response after diagnostic | No waitlist offer; route to demo/plans/product explanation |
| `LONG-DEMO-POSITIVE` | widget, whatsapp | positive response after demo discussion | Waitlist can be offered |
| `LONG-DEMO-NEGATIVE` | widget, whatsapp | negative response after demo discussion | Do not force waitlist |

## Regression Cases

These are always required:

- WhatsApp does not quote the user's inbound message.
- WhatsApp sends split replies for multi-message responses.
- WhatsApp typing/delay path is configured for real tokens.
- "Tudo bem, e vc? Meu nome e Lucas" extracts `Lucas`, not `Tudo bem`.
- WhatsApp state persists after name and pain.
- Business App echo pauses the AI.
- Outside 24h window does not send a free-form reply.
- Waitlist is never offered before strong interest.
- Unknown integrations and demo availability are not invented.
- Cold leads, warm leads, hot leads and waitlist leads are persisted in Sales Inbox.

## Passing Gate

- 100% of regression cases must pass.
- 90% or more of short and medium cases must pass.
- All canonical long cases must pass.
- Failures must include transcript, expected behavior, actual behavior and lead state when available.
