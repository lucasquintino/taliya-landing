# Execução preparada — 014: Identidade, dados e segurança de base

Preparação técnica baseada no código inspecionado; não é autorização para iniciar esta spec nem evidência de integração. Estado de execução continua em `STATUS.json` e `planning/tasks.json`.

**Responsável funcional:** Backend + segurança. Pessoa responsável ainda deve ser nomeada. Arquivos compartilhados: executor único, sem subagentes.
**Dependências de spec:** 013; todas devem estar concluídas antes de ativar esta spec.

## Fontes confirmadas

- `app/api/internal/sales-inbox/auth.ts`
- `app/internal/sales-inbox/page.tsx`
- `lib/landing/ai-attendant/sales-inbox-store.ts`
- `lib/landing/ai-attendant/storage/postgres.ts`
- `lib/landing/ai-attendant/schema.ts`

Hashes e commits: `../../docs/taliya-sdd/planning/execution.json`. Revalidar diff antes de implementar; hashes documentam esta inspeção, não congelam evolução legítima.

## Interfaces, dados e falhas

Reutilizar auth.users, business_members, e01_resolve_business e e01_access_decision do app. Contexto autenticado server-side; sessão anônima separada; nenhuma tabela de contas paralela. Staff depende do mecanismo real confirmado na 013.

Extrair DDL em request para migrações versionadas; expandir apenas vínculos/recibos ausentes, índices únicos e versão. Ensaiar forward/restore em banco descartável; não aplicar migrations do Copiloto nesta landing. Falhar fechado sem DB/TLS válido.

## Caminhos propostos para o diff

Ainda não implementados; são destinos locais propostos, nunca endpoints publicados. Preferir extensão equivalente existente se descoberta, atualizando este mapa antes do código.

- `lib/landing/ai-attendant/session-context.ts`
- `lib/landing/ai-attendant/storage/migrations/`
- `scripts/tests/sdd/identity.test.mjs`

## Tarefas detalhadas

Os IDs e checkboxes canônicos permanecem em `tasks.md`; as descrições abaixo detalham a entrega sem marcar progresso. Fontes/caminhos acima são o recorte compartilhado desta spec. Não executar tarefas remotas sem a permissão específica registrada.

### T014-01

**Requisitos/casos:** R014-02 → C014-02.
**Pré-requisitos locais:** nenhum adicional. **Pendências externas diretas:** B013-01.
**Execução:** local_after_dependencies.

Mapear sessão/contato/pessoa/business/subscription; desenhar relação e owner no data-model da spec.

**Verificação:** Mesmo e-mail declarado em duas sessões não une pessoas nem libera acesso; não criar auth/billing.
**Evidência:** `specs/014-identidade-dados-e-seguranca/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T014-02

**Requisitos/casos:** R014-01 → C014-01.
**Pré-requisitos locais:** T014-01. **Pendências externas diretas:** B013-02.
**Execução:** local_after_dependencies.

Trocar shared token por sessão staff existente, RBAC viewer/operator/admin e validação issuer/audience/expiração quando aplicável.

**Verificação:** Viewer não escreve; x-operator-id forjado e token em query não autorizam; teste 401/403 e CSRF/origin.
**Evidência:** `specs/014-identidade-dados-e-seguranca/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T014-03

**Requisitos/casos:** R014-02, R014-03 → C014-02, C014-03.
**Pré-requisitos locais:** T014-01. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Emitir sessão opaca server-side e resolver posse de conversa; autenticação existente prova vínculo ao negócio.

**Verificação:** Trocar leadId/sessionId/businessId ou fabricar histórico não expõe nem grava dados; logout remove vínculo da sessão.
**Evidência:** `specs/014-identidade-dados-e-seguranca/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T014-04

**Requisitos/casos:** R014-04 → C014-04.
**Pré-requisitos locais:** T014-01. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Extrair DDL em request; testar migrations/índices/rollback, pool limitado e TLS validado; impedir memory fallback em produção.

**Verificação:** Sem banco, request não confirma persistência; certificado inválido falha; reexecução da migration não duplica entidades.
**Evidência:** `specs/014-identidade-dados-e-seguranca/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T014-05

**Requisitos/casos:** R014-05 → C014-05.
**Pré-requisitos locais:** T014-01. **Pendências externas diretas:** B013-03.
**Execução:** local_after_dependencies.

Mapear PII, retenção, finalidade/consentimento e exclusão correlacionada sem logs de token/texto privado.

**Verificação:** Opt-in de marketing não nasce de suporte; exclusão cobre vínculos/outbox/analytics/sessão remota conforme política aprovada.
**Evidência:** `specs/014-identidade-dados-e-seguranca/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T014-06

**Requisitos/casos:** R014-01, R014-02, R014-03, R014-04, R014-05 → C014-01, C014-02, C014-03, C014-04, C014-05.
**Pré-requisitos locais:** T014-02, T014-03, T014-04, T014-05. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Implementar testes de autenticação cruzada, merge indevido, sessão revogada e produção sem DB antes de concluir.

**Verificação:** Nenhum caso negativo altera linha autorizada/contagem; evidência registra usuário e negócio sintéticos e asserts.
**Evidência:** `specs/014-identidade-dados-e-seguranca/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

## Sequência de verificação

1. Ler spec/plan/tasks/verification, este recorte e contratos referenciados; resolver esclarecimentos materiais e atualizar data-model/contrato quando o serviço real exigir.
2. Implementar teste negativo pertinente antes do efeito; separar mocks locais, integração sandbox e modelo real.
3. Rodar lint/build/tipos do código tocado e teste específico disponível. Os novos caminhos de testes acima são propostos; não alegar comando disponível antes de adicioná-lo ao repo.
4. Consultar `../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md` para comandos existentes e restrições. Não rodar eval legado em lote: há chamadas pagas e expectativas antigas.
5. Comparar critério de aceite de cada R/C em spec.md e verification.md, executar convergência e registrar pendências. Só então atualizar tasks/status/matriz e pointer.

## Reversão do recorte

Reverter somente o diff identificado desta entrega; preservar alterações concorrentes e recibos/dados. Migrações devem ser compatíveis e restauráveis. Desligar a capacidade afetada mantendo checkout, ajuda estática e atendimento; não restaurar o agente Pilates. Nenhum rollback/deploy remoto está autorizado por este documento.
