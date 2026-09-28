# Formulário, Oferta e Tracking


## Atualizacao comercial posterior

Este documento e legado quando falar de acesso antecipado, beta ou validacao. A direcao atual esta em `specs/001-niche-landing-system/spec.md`, `specs/002-floating-ai-sales-agent/spec.md` e `specs/spec-1-2-final-readiness-map.md`: vender o SaaS vertical por nicho com consultor/agente de IA, planos, assinatura, WhatsApp e diagnostico de agente sob medida.

## Formulário de diagnóstico

Rota /pilates deve capturar automaticamente:

```ts
niche: "pilates",
sourcePage: "/pilates"
```

Campos:

- Nome
- WhatsApp
- Nome do studio
- Cidade/Estado
- Quantos alunos ativos você tem?
- Qual sua maior dor hoje?
- Você usa algum sistema hoje?
- Existe alguma rotina específica que você gostaria que um agente cuidasse?
- Tem interesse em acesso antecipado?

Dores:

- Faltas
- Reposições
- Mensalidades atrasadas
- Alunos inativos
- WhatsApp bagunçado
- Falta de gestão
- Histórico do aluno
- Ficha, restrições e evolução do aluno espalhadas
- Interessados que não são chamados de volta
- Outro

## Eventos

Criar `lib/landing/tracking.ts` com função placeholder.

Eventos:

- page_view_niche
- cta_click
- pain_selected
- agent_selected
- calculator_started
- calculator_result_updated
- form_started
- form_submitted
- early_access_clicked
- custom_agent_interest_clicked

Todos os eventos devem incluir niche e sourcePage.

## Acesso antecipado

Título:

Entre no acesso antecipado e descubra onde seu studio está deixando dinheiro na mesa

Oferta:

- Diagnóstico inicial
- Análise de Dinheiro na Mesa
- Acesso antecipado
- Priorização dos agentes principais
- Canal de feedback
- Vagas limitadas
