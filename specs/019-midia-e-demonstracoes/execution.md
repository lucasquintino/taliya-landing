# Execução preparada — 019: Vídeos, demonstrações e UGCs na experiência

Preparação técnica baseada no código inspecionado; não é autorização para iniciar esta spec nem evidência de integração. Estado de execução continua em `STATUS.json` e `planning/tasks.json`.

**Responsável funcional:** Conteúdo + frontend. Pessoa responsável ainda deve ser nomeada. Arquivos compartilhados: executor único, sem subagentes.
**Dependências de spec:** 015; todas devem estar concluídas antes de ativar esta spec.

## Fontes confirmadas

- `components/landing/sections`
- `components/landing/shared`
- `data/landing`
- `docs/taliya-sdd/contracts/materials.catalog.json`
- `docs/taliya-sdd/contracts/material.schema.json`

Hashes e commits: `../../docs/taliya-sdd/planning/execution.json`. Revalidar diff antes de implementar; hashes documentam esta inspeção, não congelam evolução legítima.

## Interfaces, dados e falhas

Card resolve asset_id no catálogo vigente, máximo um por resposta. Player voluntário, captions/transcript e consentimento do embed. Recomendação, exposição, play e conclusão têm produtores distintos; link externo não prova vídeo assistido.

Sem migração. Catálogo em Git com direitos/aprovação/retirada; publicação depende B013-04. Falha/404/retirada mostra alternativa textual e mantém contratação disponível.

## Caminhos propostos para o diff

Ainda não implementados; são destinos locais propostos, nunca endpoints publicados. Preferir extensão equivalente existente se descoberta, atualizando este mapa antes do código.

- `components/landing/shared/ApprovedMaterialCard.tsx`
- `scripts/tests/sdd/material-player.spec.mjs`

## Tarefas detalhadas

Os IDs e checkboxes canônicos permanecem em `tasks.md`; as descrições abaixo detalham a entrega sem marcar progresso. Fontes/caminhos acima são o recorte compartilhado desta spec. Não executar tarefas remotas sem a permissão específica registrada.

### T019-01

**Requisitos/casos:** R019-01 → C019-01.
**Pré-requisitos locais:** nenhum adicional. **Pendências externas diretas:** B013-04.
**Execução:** local_after_dependencies.

Classificar inventário em explainer/demo/UGC com origem e direitos; solicitar só lacunas reais.

**Verificação:** Arquivo existente não vira aprovado automaticamente; catálogo pode ficar vazio com bloqueio explícito.
**Evidência:** `specs/019-midia-e-demonstracoes/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T019-02

**Requisitos/casos:** R019-01, R019-03 → C019-01, C019-03.
**Pré-requisitos locais:** T019-01. **Pendências externas diretas:** B013-04.
**Execução:** local_after_dependencies.

Preparar thumbnails/captions/transcrições e hospedagem existente sem publicar externamente.

**Verificação:** Legendas e texto equivalentes; URLs restritas; embed não carrega antes do consentimento quando exigido.
**Evidência:** `specs/019-midia-e-demonstracoes/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T019-03

**Requisitos/casos:** R019-02, R019-03 → C019-02, C019-03.
**Pré-requisitos locais:** T019-02. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Reusar card/player do DS ou adicionar componente mínimo no slot existente; uma mídia por resposta.

**Verificação:** Contratar não exige assistir; teclado/play/pause/foco funcionam; não redesenhar seção.
**Evidência:** `specs/019-midia-e-demonstracoes/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T019-04

**Requisitos/casos:** R019-04 → C019-04.
**Pré-requisitos locais:** T019-03. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Instrumentar intervalos assistidos e seek para emitir progress/conclusion confiáveis.

**Verificação:** Seek ao fim, aba oculta e link externo não geram conclusão falsa; reenvio de evento deduplicado.
**Evidência:** `specs/019-midia-e-demonstracoes/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T019-05

**Requisitos/casos:** R019-02, R019-03, R019-05 → C019-02, C019-03, C019-05.
**Pré-requisitos locais:** T019-03, T019-04. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Exercitar catálogo vazio, mídia retirada durante sessão, 404, rede lenta e navegação por teclado.

**Verificação:** Alternativa textual e contratação acessíveis; item retired não reaparece do cache.
**Evidência:** `specs/019-midia-e-demonstracoes/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T019-06

**Requisitos/casos:** R019-01, R019-02, R019-03, R019-04, R019-05 → C019-01, C019-02, C019-03, C019-04, C019-05.
**Pré-requisitos locais:** T019-05. **Pendências externas diretas:** B013-04.
**Execução:** local_after_dependencies.

Entregar biblioteca aprovada e guia de inclusão/retirada com revisão e responsável.

**Verificação:** Versão/rastreio editorial completos; material faltante segue bloqueado, sem fixture publicada.
**Evidência:** `specs/019-midia-e-demonstracoes/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

## Sequência de verificação

1. Ler spec/plan/tasks/verification, este recorte e contratos referenciados; resolver esclarecimentos materiais e atualizar data-model/contrato quando o serviço real exigir.
2. Implementar teste negativo pertinente antes do efeito; separar mocks locais, integração sandbox e modelo real.
3. Rodar lint/build/tipos do código tocado e teste específico disponível. Os novos caminhos de testes acima são propostos; não alegar comando disponível antes de adicioná-lo ao repo.
4. Consultar `../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md` para comandos existentes e restrições. Não rodar eval legado em lote: há chamadas pagas e expectativas antigas.
5. Comparar critério de aceite de cada R/C em spec.md e verification.md, executar convergência e registrar pendências. Só então atualizar tasks/status/matriz e pointer.

## Reversão do recorte

Reverter somente o diff identificado desta entrega; preservar alterações concorrentes e recibos/dados. Migrações devem ser compatíveis e restauráveis. Desligar a capacidade afetada mantendo checkout, ajuda estática e atendimento; não restaurar o agente Pilates. Nenhum rollback/deploy remoto está autorizado por este documento.
