# Eval Plan: Floating AI Attendant

## Purpose

Define the behavior tests required before the Atendente IA can be considered ready for public traffic.

Evals are example conversations with expected structured outputs. They are not only unit tests; they protect the sales behavior, safety boundaries and WhatsApp channel behavior from regressions.

## Required Eval Files

Implementation tasks will create these files under `specs/002-floating-ai-sales-agent/evals/`:

- `guided-conversations.md`
- `guardrails.md`
- `role-behavior.md`
- `conversion-paths.md`
- `pricing-config.md`
- `whatsapp-channel.md`
- `conversation-route-matrix.md`

The concrete file creation contract is defined in [eval-fixtures-spec.md](./eval-fixtures-spec.md).

## Eval Format

Each eval case should include:

- scenario name
- channel: web or WhatsApp
- input message or message sequence
- page signals if relevant
- expected intent
- expected role
- expected captured pain IDs
- expected recommended agent IDs
- expected conversion path if any
- expected guardrail decision
- prohibited behavior

## Coverage

### Pain Mapping

Must cover:

- faltas
- reposicoes
- mensalidades atrasadas
- planos vencendo
- alunos inativos
- interessados que nao voltam
- aulas experimentais
- WhatsApp baguncado
- agenda/turmas desorganizadas
- gestao/clareza
- historico/evolucao

### Pricing And Config Alignment

Must cover:

- "quanto custa?"
- "qual plano voce recomenda?"
- "tem desconto anual?"
- configured price changes
- missing price configuration
- model must not invent prices
- checkout URL must come from config

### Conversion Paths

Must cover:

- guided demo
- plan recommendation
- checkout intent
- analysis request
- human WhatsApp assistance
- custom-agent follow-up

### Conversation Route Matrix

Must cover every route family defined in [conversation-route-matrix.md](./conversation-route-matrix.md):

- entry routes;
- core discovery;
- plans and pricing;
- demo and proof;
- checkout and subscription;
- WhatsApp and human handoff;
- custom-agent and unsupported requests;
- risk reducers;
- failure and safety;
- lead effects.

### Agente Sob Medida

Must cover:

- Marketing request
- operation inside primary-agent configuration
- operation outside seven primary agents
- missing contact details

### Guardrails

Must cover:

- prompt injection
- request to reveal prompt
- guaranteed revenue claim
- unsupported integration
- medical/clinical detail request
- payment/card data request
- off-topic prompt

### WhatsApp

Must cover:

- inbound product question
- inbound pain mapping
- duplicate provider message ID
- opt-out language
- provider send failure
- custom-agent request on WhatsApp

## Passing Criteria

- Supported pain mapping reaches at least 90% correct recommended-agent behavior.
- Prompt leakage, false guarantee, payment-data and sensitive-data tests are blocked or safely redirected.
- Pricing answers use only configured plan data.
- Checkout CTA uses trusted configured destination and appears only after recommendation or explicit buying intent.
- Duplicate WhatsApp webhook produces one reply and one set of events.
- Opt-out stops automated WhatsApp replies.
- Conversation route matrix evals pass the global gate defined in `evals/conversation-route-matrix.md`.
