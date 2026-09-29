# 019 — Vídeos, demonstrações e UGCs na experiência

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Conteúdo + frontend.
**Dependências:** 015.

## Tarefas
- [ ] **T019-01** — Inventariar arquivos de mídia entregues com direitos, classificação de UGC e relações com capacidades. Requisitos: R019-01. Recorte: [execution.md#t019-01](execution.md#t019-01).
- [ ] **T019-02** — Preparar thumbnails, legendas/transcrições revisadas e tamanhos adequados usando hospedagem existente. Requisitos: R019-01, R019-03. Recorte: [execution.md#t019-02](execution.md#t019-02).
- [ ] **T019-03** — Construir um card/player reutilizável para landing e chat sem tocar na composição global. Requisitos: R019-02, R019-03. Recorte: [execution.md#t019-03](execution.md#t019-03).
- [ ] **T019-04** — Implementar medição de intervalos assistidos quando suportado e poucos marcos, sem evento por segundo. Requisitos: R019-04. Recorte: [execution.md#t019-04](execution.md#t019-04).
- [ ] **T019-05** — Validar fallback sem vídeo, link quebrado, arquivo retirado e teclado/foco. Requisitos: R019-02, R019-03, R019-05. Recorte: [execution.md#t019-05](execution.md#t019-05).
- [ ] **T019-06** — Registrar biblioteca de lançamento e procedimento de manutenção com responsável. Requisitos: R019-01, R019-02, R019-03, R019-04, R019-05. Recorte: [execution.md#t019-06](execution.md#t019-06).

Não marcar uma tarefa porque o arquivo existe. Acrescentar caminho do diff, comando e resultado verificável ao concluí-la. Se o código atual já atende, comprovar por teste e registrar reuso em vez de reimplementar.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
