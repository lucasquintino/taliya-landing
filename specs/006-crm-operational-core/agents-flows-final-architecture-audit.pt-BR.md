# Taliya CRM - Auditoria Final Da Arquitetura De Agentes/Fluxos

Status: auditoria funcional v0.1.
Data: 2026-05-21.

## Objetivo

Registrar se a arquitetura funcional de Agentes/Fluxos esta definida o suficiente para virar base de UI, contrato de produto e implementacao futura.

Esta auditoria verifica:

- agentes;
- rotinas;
- fluxos;
- modos de autonomia;
- configuracao minima;
- simulacao;
- publicacao;
- fallback;
- pausa;
- rollback;
- integracao com CRM, Configuracoes, Integracoes, Billing, Uso/Cotas, Auditoria e Control Planes.

## Fontes De Verdade

Contratos principais:

- `agents-flows-routines-pages-final-contract.pt-BR.md`
- `agents-flows-routine-profile-map.pt-BR.md`
- `agents-flows-publication-versioning-and-evals.pt-BR.md`

Contratos de apoio:

- `agents-flows-functional-architecture.pt-BR.md`
- `agents-flows-configuration-minimal-audit.pt-BR.md`
- `agents-flows-flow-page-examples.pt-BR.md`

Mapas por agente:

- `agents-flows-atendimento-pages-dynamics.pt-BR.md`
- `agents-flows-agenda-pages-dynamics.pt-BR.md`
- `agents-flows-vendas-pages-dynamics.pt-BR.md`
- `agents-flows-financeiro-pages-dynamics.pt-BR.md`
- `agents-flows-retencao-pages-dynamics.pt-BR.md`
- `agents-flows-gestao-governanca-pages-dynamics.pt-BR.md`
- `agents-flows-historico-professor-pages-dynamics.pt-BR.md`

## Decisao Final

Agentes/Fluxos esta definido como:

```text
Agente nao configura.
Rotina organiza.
Perfil da rotina configura varios fluxos de uma vez.
Fluxo so abre para personalizacao quando necessario.
Modo do fluxo define quem conduz quando o fluxo dispara.
```

Termos finais:

| Termo antigo | Termo final |
|---|---|
| pacote | rotina |
| preset | perfil da rotina |
| ativar rotina | publicar rotina |
| default do fluxo | maior modo permitido ou modo aplicado pelo perfil |

## Auditoria Requisito A Requisito

| Requisito | Status | Evidencia |
|---|---|---|
| Funcionar com 0 agentes | Fechado | `agents-flows-routines-pages-final-contract.pt-BR.md`, secoes Perfil Inicial Por Plano e Regras De Bloqueio Por Plano. |
| Funcionar com 1 agente | Fechado | Mesmas secoes de plano; apenas agente contratado abre rotinas configuraveis. |
| Funcionar com 3 agentes | Fechado | Rotinas dos agentes contratados em Equilibrado, publicacao por rotina. |
| Funcionar com 7 agentes | Fechado | Filtros por agente, rotina, status, bloqueio e cota. |
| Agente nao ter configuracao propria | Fechado | Contrato final, secao Agente Nao Configura. |
| Rotina agrupar fluxos | Fechado | Contrato final, secao Rotina Agrupa, e mapas por agente. |
| Fluxo configurar somente o necessario | Fechado | Contrato final, secoes Fluxo Configura, Configuracao Visivel Deve Ser Minima e Campos Que Podem Aparecer No Fluxo. |
| Todo fluxo ter ficha com objetivo, area, agente, gatilho, condicao, acao, modo, permissao, canal, dados, integracao, fallback, aprovacao, cota, risco, simulacao, status e auditoria | Fechado | Contrato final, secao Ficha Obrigatoria Do Fluxo. |
| Tom de voz no fluxo | Fechado | Contrato final, secao Tom De Voz Fica No Fluxo. |
| Template no fluxo | Fechado | Contrato final, secao Template Fica No Fluxo. |
| Canal nao ser ajuste solto | Fechado | Contrato final, secao Canal Nao E Ajuste Solto. |
| Modos Manual/Copiloto/Modos autonomos | Fechado | Contrato final, secao Dinamica Do Fluxo Por Modo. |
| Perfil Mais manual/Equilibrado/Mais autonomo | Fechado | `agents-flows-routine-profile-map.pt-BR.md`. |
| Simulacao antes de publicar | Fechado | Contrato final e `agents-flows-publication-versioning-and-evals.pt-BR.md`. |
| Publicacao versionada | Fechado | `agents-flows-publication-versioning-and-evals.pt-BR.md`. |
| Pausa, fallback e rollback | Fechado | Contrato final e contrato de publicacao/versionamento. |
| Cotas e economia | Fechado | Contrato final, contrato de publicacao/versionamento e arquitetura funcional. |
| Auditoria | Fechado | Contrato final e Eventos De Auditoria no contrato de publicacao/versionamento. |
| Control Planes distribuidos | Fechado | Detalhe de execucao em `/app/fluxos/execucoes/[runId]` e relacao com Control Planes. |
| Setup Inicial nao publicar autonomia | Fechado | Relacao Com Outras Familias no contrato de publicacao/versionamento. |
| Configuracoes nao virar builder de agente | Fechado | Contrato final e arquitetura funcional. |
| Integracoes serem fonte de saude tecnica | Fechado | Gates De Publicacao e Relacao Com Outras Familias. |
| Billing decidir entitlement | Fechado | Gates De Publicacao e Relacao Com Outras Familias. |
| Uso/Cotas decidir consumo real | Fechado | Gates De Publicacao e Relacao Com Outras Familias. |

## Validacao Dos 96 Fluxos

Resultado da validacao automatizada:

```text
MASTER_PROFILE_ROWS=96
AGENT_PROFILE_UNIQUE_ROWS=96
PROFILE_MISSING=[]
PROFILE_EXTRA=[]
PROFILE_CONFLICTS=0
AGENT_DOCS=7
ADJUSTMENT_ROWS=96
ADJUSTMENT_AVG=3.17
ADJUSTMENT_COUNT_BY_SIZE={1: 1, 2: 16, 3: 47, 4: 30, 5: 2}
ADJUSTMENTS_5_PLUS=[B1, D1]
BAD_VISIBLE_ADJUSTMENT_TERMS=[]
ROUTE_MISSING=[]
```

Leitura:

- todos os 96 fluxos aparecem no mapa mestre;
- todos os 96 fluxos aparecem nos mapas por agente;
- nenhum fluxo falta;
- nenhum fluxo sobra;
- nenhum perfil diverge entre mapa mestre e mapas por agente;
- todos os mapas por agente tem paginas de rotina, ajustar, simular, publicar e execucoes;
- nenhum ajuste visivel usa canal, integracao, permissao, cota ou billing como configuracao solta.

## Configuracao Minima

A configuracao ficou limitada ao que muda a operacao real:

- modo do fluxo;
- perfil da rotina;
- horario, prazo, cadencia ou frequencia quando muda a rotina;
- limite simples quando evita excesso;
- template/tom quando existe comunicacao;
- responsavel, aprovador ou fila humana quando precisa sair do padrao herdado da rotina;
- fallback apenas quando existe escolha real.

Itens que nao devem virar configuracao de fluxo:

- canal;
- integracao;
- permissao real;
- cota real;
- billing;
- prompt livre;
- modelo de IA;
- payload;
- retry tecnico;
- idempotencia;
- regra tecnica de provedor.

## Pontos Mantidos

- Taliya continua sendo CRM operacional completo.
- Agentes sao camada integrada, nao produto inteiro.
- 0 agentes continua manual.
- Agentes/Fluxos fica fora do Setup Inicial.
- Setup Inicial pode preparar rascunho, mas nao publica autonomia.
- Autonomia exige preflight, simulacao, publicacao e auditoria.
- Billing, Integracoes, Uso/Cotas, Auditoria e Control Planes continuam fontes de verdade das suas areas.

## Pontos Corrigidos

- `pacote` foi rebaixado para termo legado; na UI final e `rotina`.
- `preset` foi rebaixado para termo legado; na UI final e `perfil da rotina`.
- `Ativar rotina` foi trocado por `Publicar rotina`.
- `Default` foi trocado por `modo aplicado pelo perfil` ou `maior modo permitido`.
- Canal saiu da lista de ajustes configuraveis e virou dependencia fixa.
- Responsavel/aprovador/fila humana viraram heranca da rotina, nao pergunta repetida em cada fluxo.

## Pontos Removidos Do MVP

- builder de prompt;
- builder tecnico livre de politicas;
- configuracao geral do agente;
- tom de voz no agente;
- canal como escolha solta por fluxo;
- publicacao autonoma no Setup Inicial;
- Control Plane central `/app/controle/*`;
- autonomia sem fallback;
- autonomia sem cota;
- publicacao sem simulacao.

## Residuo Aceito

Ainda existem documentos legados com o termo `pacote` ou `default_publicado`.

Regra de leitura:

```text
Quando houver conflito, vence:
1. agents-flows-routines-pages-final-contract.pt-BR.md
2. agents-flows-routine-profile-map.pt-BR.md
3. agents-flows-publication-versioning-and-evals.pt-BR.md
```

O CSV `agents-flows-configuration-matrix.pt-BR.csv` e artefato auxiliar legado e nao deve comandar a UI final.

## Conclusao

A arquitetura funcional de Agentes/Fluxos esta fechada para a etapa de produto.

Proxima etapa recomendada:

1. desenhar wireframes de baixa fidelidade das paginas de rotina, ajustar, simular e publicar;
2. transformar os contratos em modelo de dados/API;
3. criar criterios de aceite por tela antes de implementar UI.
