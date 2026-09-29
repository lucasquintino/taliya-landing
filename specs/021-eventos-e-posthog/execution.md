# Execução preparada — 021: Instrumentação confiável e integração PostHog

Preparação técnica baseada no código inspecionado; não é autorização para iniciar esta spec nem evidência de integração. Estado de execução continua em `STATUS.json` e `planning/tasks.json`.

**Responsável funcional:** Backend/frontend + analytics. Pessoa responsável ainda deve ser nomeada. Arquivos compartilhados: executor único, sem subagentes.
**Dependências de spec:** 017, 018, 019, 020; todas devem estar concluídas antes de ativar esta spec.

## Fontes confirmadas

- `lib/landing/ai-attendant/funnel-events.ts`
- `app/api/landing/ai-attendant/events/route.ts`
- `lib/landing/ai-attendant/storage/postgres.ts`
- `components/landing/shared/FloatingAiAttendant.tsx`
- `docs/taliya-sdd/contracts/event.envelope.schema.json`
- `docs/taliya-sdd/contracts/events.catalog.v3.json`

Hashes e commits: `../../docs/taliya-sdd/planning/execution.json`. Revalidar diff antes de implementar; hashes documentam esta inspeção, não congelam evolução legítima.

## Interfaces, dados e falhas

Browser: interação; player: reprodução; backend: operação aceita; app: primeiro valor; billing: financeiro. IDs de evento e negócio não são credenciais. Relay transforma envelope canônico para PostHog depois de verificar contrato oficial/projeto.

Outbox na transação do produtor quando disponível; entre serviços, inbox/dedup e reconciliação. Não depender de browser aberto. Quota/timeout geram atraso/lacuna explícita; falha de analytics não bloqueia checkout.

## Caminhos propostos para o diff

Ainda não implementados; são destinos locais propostos, nunca endpoints publicados. Preferir extensão equivalente existente se descoberta, atualizando este mapa antes do código.

- `lib/landing/analytics/posthog-relay.ts`
- `scripts/tests/sdd/events.test.mjs`

## Tarefas detalhadas

Os IDs e checkboxes canônicos permanecem em `tasks.md`; as descrições abaixo detalham a entrega sem marcar progresso. Fontes/caminhos acima são o recorte compartilhado desta spec. Não executar tarefas remotas sem a permissão específica registrada.

### T021-01

**Requisitos/casos:** R021-01 → C021-01.
**Pré-requisitos locais:** nenhum adicional. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Mapear eventos legados ao catálogo v3 e indicar produtor, ID, versão, tempo e destino de cada um.

**Verificação:** Nenhum evento financeiro parte de browser/IA; eventos obsoletos têm destino explícito sem dupla emissão.
**Evidência:** `specs/021-eventos-e-posthog/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T021-02

**Requisitos/casos:** R021-01, R021-02 → C021-01, C021-02.
**Pré-requisitos locais:** T021-01. **Pendências externas diretas:** B013-01.
**Execução:** local_after_dependencies.

Instrumentar produtores reais app/billing/backend/browser/player com envelope minimizado.

**Verificação:** Cadastro/compra direta sem chat aparecem uma vez; retorno do checkout não emite payment_confirmed.
**Evidência:** `specs/021-eventos-e-posthog/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T021-03

**Requisitos/casos:** R021-03, R021-04 → C021-03, C021-04.
**Pré-requisitos locais:** T021-01. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Integrar SDK de browser/servidor com consentimento e reset de identidade no logout.

**Verificação:** PII/texto de chat/tokens não chegam ao payload; business_id separado e sem fingerprinting.
**Evidência:** `specs/021-eventos-e-posthog/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T021-04

**Requisitos/casos:** R021-05 → C021-05.
**Pré-requisitos locais:** T021-02. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Implementar relay/outbox com dedup e reconciliação, sem depender de after/browser aberto.

**Verificação:** Timeout/worker morto/repetição/quota não perdem efeito de domínio; atraso/lacuna registrados.
**Evidência:** `specs/021-eventos-e-posthog/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T021-05

**Requisitos/casos:** R021-04 → C021-04.
**Pré-requisitos locais:** T021-01. **Pendências externas diretas:** B013-03.
**Execução:** authorized_environment.

Configurar projeto/ambientes/limites e autocapture/replay conservadores somente quando autorizado.

**Verificação:** Tráfego sintético não contamina produção; nenhum addon pago ativado por script local.
**Evidência:** `specs/021-eventos-e-posthog/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T021-06

**Requisitos/casos:** R021-01, R021-02, R021-03, R021-04, R021-05 → C021-01, C021-02, C021-03, C021-04, C021-05.
**Pré-requisitos locais:** T021-02, T021-03, T021-04, T021-05. **Pendências externas diretas:** B013-03.
**Execução:** authorized_environment.

Comparar jornadas e totais com fontes canônicas e simular falso evento financeiro.

**Verificação:** Tentativa client-side não altera financeiro/acesso; outbox reenvia com ID estável e não infla contagem.
**Evidência:** `specs/021-eventos-e-posthog/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

## Sequência de verificação

1. Ler spec/plan/tasks/verification, este recorte e contratos referenciados; resolver esclarecimentos materiais e atualizar data-model/contrato quando o serviço real exigir.
2. Implementar teste negativo pertinente antes do efeito; separar mocks locais, integração sandbox e modelo real.
3. Rodar lint/build/tipos do código tocado e teste específico disponível. Os novos caminhos de testes acima são propostos; não alegar comando disponível antes de adicioná-lo ao repo.
4. Consultar `../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md` para comandos existentes e restrições. Não rodar eval legado em lote: há chamadas pagas e expectativas antigas.
5. Comparar critério de aceite de cada R/C em spec.md e verification.md, executar convergência e registrar pendências. Só então atualizar tasks/status/matriz e pointer.

## Reversão do recorte

Reverter somente o diff identificado desta entrega; preservar alterações concorrentes e recibos/dados. Migrações devem ser compatíveis e restauráveis. Desligar a capacidade afetada mantendo checkout, ajuda estática e atendimento; não restaurar o agente Pilates. Nenhum rollback/deploy remoto está autorizado por este documento.
