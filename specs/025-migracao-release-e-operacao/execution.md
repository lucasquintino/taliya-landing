# Execução preparada — 025: Migração, publicação controlada e operação

Preparação técnica baseada no código inspecionado; não é autorização para iniciar esta spec nem evidência de integração. Estado de execução continua em `STATUS.json` e `planning/tasks.json`.

**Responsável funcional:** Liderança técnica + operação/produto. Pessoa responsável ainda deve ser nomeada. Arquivos compartilhados: executor único, sem subagentes.
**Dependências de spec:** 024; todas devem estar concluídas antes de ativar esta spec.

## Fontes confirmadas

- `next.config.ts`
- `AGENTS.md`
- `docs/taliya-sdd/07_RUNBOOK_RELEASE_E_OPERACAO.md`
- `docs/taliya-sdd/STATUS.json`

Hashes e commits: `../../docs/taliya-sdd/planning/execution.json`. Revalidar diff antes de implementar; hashes documentam esta inspeção, não congelam evolução legítima.

## Interfaces, dados e falhas

Release manifesto fixa commits por serviço, migrações, flags, owners, aprovações e evidências G0–G6. Publicação e operação real só com autorização específica. Checkout independe do percentual do agente e das flags analytics.

Ensaio expand/contract, backup/restore/reconciliação antes de produção. Kill switch desliga geração/escritas/proativo seletivamente; preserva recibos, assinatura direta e humano. Nunca voltar ao agente Pilates. Não executar migração destrutiva no rollback.

## Caminhos propostos para o diff

Ainda não implementados; são destinos locais propostos, nunca endpoints publicados. Preferir extensão equivalente existente se descoberta, atualizando este mapa antes do código.

- `docs/taliya-sdd/operations/release-manifest.json`
- `docs/taliya-sdd/operations/rollback.md`
- `docs/taliya-sdd/evidence/release/`

## Tarefas detalhadas

Os IDs e checkboxes canônicos permanecem em `tasks.md`; as descrições abaixo detalham a entrega sem marcar progresso. Fontes/caminhos acima são o recorte compartilhado desta spec. Não executar tarefas remotas sem a permissão específica registrada.

### T025-01

**Requisitos/casos:** R025-01 → C025-01.
**Pré-requisitos locais:** nenhum adicional. **Pendências externas diretas:** B013-03.
**Execução:** authorized_environment.

Ensaiar inventário/migração de leads/sessões, backup/restore e reconciliação em ambiente autorizado.

**Verificação:** Contagens/IDs/recibos mantidos; nenhum merge automático por e-mail; resultados do ensaio anexados.
**Evidência:** `specs/025-migracao-release-e-operacao/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T025-02

**Requisitos/casos:** R025-02, R025-03 → C025-02, C025-03.
**Pré-requisitos locais:** T025-01. **Pendências externas diretas:** B013-03.
**Execução:** authorized_environment.

Montar manifesto de release com SHA por serviço, flags, migrações, aprovação e rollback.

**Verificação:** Sem autorização explícita o procedimento para antes de publicar; kill switches não dependem de PostHog.
**Evidência:** `specs/025-migracao-release-e-operacao/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T025-03

**Requisitos/casos:** R025-02 → C025-02.
**Pré-requisitos locais:** T025-02. **Pendências externas diretas:** B013-03.
**Execução:** authorized_environment.

Executar interno→5→25→100 por cento após gates e autorização, com mínimo proposto 24h/50 turnos por etapa.

**Verificação:** Registrar denominador/amostra/tempo; volume insuficiente não é sucesso; sintéticos distintos de tráfego real.
**Evidência:** `specs/025-migracao-release-e-operacao/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T025-04

**Requisitos/casos:** R025-04 → C025-04.
**Pré-requisitos locais:** T025-03. **Pendências externas diretas:** B013-03.
**Execução:** authorized_environment.

Monitorar latência/erro/financeiro/custo; testar desligamento seletivo e reconciliação.

**Verificação:** Uma falha crítica interrompe rollout; erros >1 por cento com n>=100 investigados; checkout preservado.
**Evidência:** `specs/025-migracao-release-e-operacao/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T025-05

**Requisitos/casos:** R025-03, R025-04 → C025-03, C025-04.
**Pré-requisitos locais:** T025-02. **Pendências externas diretas:** B013-03.
**Execução:** authorized_environment.

Treinar operação com incidentes provedor/banco/canal/analytics e exercício de retomada.

**Verificação:** Responsáveis nomeados e procedimento executado; nenhuma resposta tardia após humano e nenhum reenvio financeiro.
**Evidência:** `specs/025-migracao-release-e-operacao/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T025-06

**Requisitos/casos:** R025-01, R025-02, R025-03, R025-04, R025-05 → C025-01, C025-02, C025-03, C025-04, C025-05.
**Pré-requisitos locais:** T025-04, T025-05. **Pendências externas diretas:** B013-03.
**Execução:** authorized_environment.

Fechar gates G0–G6 e estabilização proposta 48h; atualizar continuidade e rotina no sistema da equipe.

**Verificação:** 100 por cento só com operação comprovada; sem automação criada no chat nem promessa de execução em segundo plano.
**Evidência:** `specs/025-migracao-release-e-operacao/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

## Sequência de verificação

1. Ler spec/plan/tasks/verification, este recorte e contratos referenciados; resolver esclarecimentos materiais e atualizar data-model/contrato quando o serviço real exigir.
2. Implementar teste negativo pertinente antes do efeito; separar mocks locais, integração sandbox e modelo real.
3. Rodar lint/build/tipos do código tocado e teste específico disponível. Os novos caminhos de testes acima são propostos; não alegar comando disponível antes de adicioná-lo ao repo.
4. Consultar `../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md` para comandos existentes e restrições. Não rodar eval legado em lote: há chamadas pagas e expectativas antigas.
5. Comparar critério de aceite de cada R/C em spec.md e verification.md, executar convergência e registrar pendências. Só então atualizar tasks/status/matriz e pointer.

## Reversão do recorte

Reverter somente o diff identificado desta entrega; preservar alterações concorrentes e recibos/dados. Migrações devem ser compatíveis e restauráveis. Desligar a capacidade afetada mantendo checkout, ajuda estática e atendimento; não restaurar o agente Pilates. Nenhum rollback/deploy remoto está autorizado por este documento.
