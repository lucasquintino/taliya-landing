# 022 — Painéis SaaS, definições e limites de custo

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Analytics + produto.
**Dependências:** 021.

## Tarefas
- [ ] **T022-01** — Versionar dicionário de métricas, denominadores e fontes de receita antes dos gráficos. Requisitos: R022-01, R022-02, R022-03. Recorte: [execution.md#t022-01](execution.md#t022-01).
- [ ] **T022-02** — Construir os seis dashboards no PostHog com filters padrão e links de investigação. Requisitos: R022-01, R022-02. Recorte: [execution.md#t022-02](execution.md#t022-02).
- [ ] **T022-03** — Preparar consultas/snapshots analíticos sanitizados; evitar sincronizar banco inteiro ou ativar CDC sem revisão. Requisitos: R022-03, R022-05. Recorte: [execution.md#t022-03](execution.md#t022-03).
- [ ] **T022-04** — Conferir resultados com fixture financeira e casos anual/renovação/estorno/inadimplência. Requisitos: R022-03. Recorte: [execution.md#t022-04](execution.md#t022-04).
- [ ] **T022-05** — Configurar custo/uso e alertas 70/85/95% do teto aprovado por produto; registrar limite do plano/projetos. Requisitos: R022-04. Recorte: [execution.md#t022-05](execution.md#t022-05).
- [ ] **T022-06** — Documentar guia de leitura dos painéis e auditoria semanal de dados, sem duplicar no Internal. Requisitos: R022-01, R022-02, R022-03, R022-04, R022-05. Recorte: [execution.md#t022-06](execution.md#t022-06).

Não marcar uma tarefa porque o arquivo existe. Acrescentar caminho do diff, comando e resultado verificável ao concluí-la. Se o código atual já atende, comprovar por teste e registrar reuso em vez de reimplementar.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
