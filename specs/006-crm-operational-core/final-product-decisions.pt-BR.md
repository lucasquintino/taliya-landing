# Decisoes finais v0.1 - PT-BR

> Status: fechado v0.1 pela Rodada 11. As decisoes D001-D037 foram assumidas como premissas de produto para gerar telas e prompts finais.

## Decisoes assumidas

| Tema | Decisao |
| --- | --- |
| Proposta do produto | Taliya e um CRM operacional completo para studios de Pilates com agentes de IA integrados. |
| WhatsApp | WhatsApp e canal, nao o produto inteiro. |
| Plano Base | Plano Base e CRM completo com 0 agentes ativos. |
| Agentes | Agentes atuam no WhatsApp, CRM web e app. |
| Web/app | Web governa profundidade; app opera o dia a dia e configuracoes essenciais. |
| Encaixe de vaga | Primeiro programatico; IA explica, prioriza, redige ou trata excecao. |
| Acoes sensiveis | Exigem permissao, impacto e auditoria; autonomia bloqueada por padrao. |
| Cotas | Cota e governanca operacional, nao apenas billing. |
| Suporte Taliya | Acesso interno so com grant, escopo, prazo e auditoria. |
| Prompts visuais | Produto vem dos docs; referencia visual guia composicao. |

## Decisoes que foram fechadas na Rodada 11

| Prioridade | Decisoes | Resultado |
| --- | --- | --- |
| Alta | D013, D021, D029 | Formulas explicaveis definidas para Hoje, encaixe e retencao. |
| Alta | D016, D017, D031 | Identidade, historico sensivel e LGPD tratados com permissao, resumo permitido e auditoria. |
| Alta | D020, D025, D028 | Reposicao, pre-matricula e contratos fechados em regras MVP. |
| Alta | D032, D033, D034, D035 | Autonomia, reprocessamento, incidentes e suporte fechados com guardrails. |
| Alta | D036, D037 | Presets e navegacao final definidos. |
| Media | D001-D012, D014-D015, D018-D019, D022-D027, D030 | Fechadas como premissas v0.1; detalhes estao em `round-11-product-closure.pt-BR.md`. |

## Decisao de uso dos docs atuais

Os documentos atuais podem ser usados como **base de prompts exploratorios v0.1**, desde que o prompt declare:

```text
Nao congelar regra de negocio.
Nao inventar campos.
Manter premissas da Rodada 11 como fonte funcional.
```

Para gerar telas finais de produto, usar `round-11-product-closure.pt-BR.md`, `final-navigation-web-app.pt-BR.md`, `studio-operational-presets.pt-BR.md` e `final-screen-contract-matrix.pt-BR.md`.
