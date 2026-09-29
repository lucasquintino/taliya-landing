# Execução preparada — 022: Painéis SaaS, definições e limites de custo

Preparação técnica baseada no código inspecionado; não é autorização para iniciar esta spec nem evidência de integração. Estado de execução continua em `STATUS.json` e `planning/tasks.json`.

**Responsável funcional:** Analytics + produto. Pessoa responsável ainda deve ser nomeada. Arquivos compartilhados: executor único, sem subagentes.
**Dependências de spec:** 021; todas devem estar concluídas antes de ativar esta spec.

## Fontes confirmadas

- `docs/taliya-sdd/08_POSTHOG_METRICAS_E_CUSTOS.md`
- `docs/taliya-sdd/contracts/events.catalog.v3.json`
- `lib/landing/ai-attendant/funnel-events.ts`

Hashes e commits: `../../docs/taliya-sdd/planning/execution.json`. Revalidar diff antes de implementar; hashes documentam esta inspeção, não congelam evolução legítima.

## Interfaces, dados e falhas

Seis painéis no PostHog: aquisição, conversão, conteúdo, atendimento, ativação/retenção e receita. Propriedades financeiras canônicas; separar caixa, MRR, receita e clientes/negócios/usuários. Nenhum BI no Internal.

Sem banco analítico próprio. Exportar configurações/queries sem dados privados. Agregação por business_id sem ativar addon pago. Falta de amostra/coorte imatura mostra indisponibilidade, não zero inventado.

## Caminhos propostos para o diff

Ainda não implementados; são destinos locais propostos, nunca endpoints publicados. Preferir extensão equivalente existente se descoberta, atualizando este mapa antes do código.

- `docs/taliya-sdd/analytics/metric-dictionary.md`
- `docs/taliya-sdd/analytics/posthog-exports/`
- `scripts/tests/sdd/metrics.test.mjs`

## Tarefas detalhadas

Os IDs e checkboxes canônicos permanecem em `tasks.md`; as descrições abaixo detalham a entrega sem marcar progresso. Fontes/caminhos acima são o recorte compartilhado desta spec. Não executar tarefas remotas sem a permissão específica registrada.

### T022-01

**Requisitos/casos:** R022-01, R022-02, R022-03 → C022-01, C022-02, C022-03.
**Pré-requisitos locais:** nenhum adicional. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Definir denominadores, entidades, janelas, timezone, centavos e eventos de cada métrica.

**Verificação:** Mensal/anual, churn pedido/efetivo, garantia e coorte imatura têm exemplos reproduzíveis.
**Evidência:** `specs/022-paineis-metricas-e-custos/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T022-02

**Requisitos/casos:** R022-01, R022-02 → C022-01, C022-02.
**Pré-requisitos locais:** T022-01. **Pendências externas diretas:** B013-03.
**Execução:** authorized_environment.

Preparar seis painéis/insights no PostHog com filtros de ambiente e links de operação.

**Verificação:** Compra direta fica no funil; agent_assisted é associação, não causalidade; nada de BI no Internal.
**Evidência:** `specs/022-paineis-metricas-e-custos/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T022-03

**Requisitos/casos:** R022-03, R022-05 → C022-03, C022-05.
**Pré-requisitos locais:** T022-01. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Definir consultas/snapshots minimizados a partir de autoridades e exportar configuração versionada.

**Verificação:** Consultas não exigem cópia integral de DB; contagens distinguem usuários/membros/negócios/clientes.
**Evidência:** `specs/022-paineis-metricas-e-custos/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T022-04

**Requisitos/casos:** R022-03 → C022-03.
**Pré-requisitos locais:** T022-01, T022-03. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Testar fixtures financeiras identificadas com anual/renovação/cancelamento/estorno/fuso.

**Verificação:** Igualdade exata com valores canônicos; anual normalizado; reembolso solicitado não diminui caixa como concluído.
**Evidência:** `specs/022-paineis-metricas-e-custos/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T022-05

**Requisitos/casos:** R022-04 → C022-04.
**Pré-requisitos locais:** T022-01. **Pendências externas diretas:** B013-03.
**Execução:** authorized_environment.

Calcular volumes/addons e propor alarmes 70/85/95 por cento do orçamento aprovado.

**Verificação:** Teto proposto não é gasto autorizado; alerta não bloqueia acesso nem ativa Group Analytics/replay.
**Evidência:** `specs/022-paineis-metricas-e-custos/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T022-06

**Requisitos/casos:** R022-01, R022-02, R022-03, R022-04, R022-05 → C022-01, C022-02, C022-03, C022-04, C022-05.
**Pré-requisitos locais:** T022-02, T022-04, T022-05. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Entregar guia dos painéis, frescor, lacunas e dono de reconciliação.

**Verificação:** Operador consegue rastrear divergência até produtor; dado ausente não aparece como venda inexistente.
**Evidência:** `specs/022-paineis-metricas-e-custos/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

## Sequência de verificação

1. Ler spec/plan/tasks/verification, este recorte e contratos referenciados; resolver esclarecimentos materiais e atualizar data-model/contrato quando o serviço real exigir.
2. Implementar teste negativo pertinente antes do efeito; separar mocks locais, integração sandbox e modelo real.
3. Rodar lint/build/tipos do código tocado e teste específico disponível. Os novos caminhos de testes acima são propostos; não alegar comando disponível antes de adicioná-lo ao repo.
4. Consultar `../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md` para comandos existentes e restrições. Não rodar eval legado em lote: há chamadas pagas e expectativas antigas.
5. Comparar critério de aceite de cada R/C em spec.md e verification.md, executar convergência e registrar pendências. Só então atualizar tasks/status/matriz e pointer.

## Reversão do recorte

Reverter somente o diff identificado desta entrega; preservar alterações concorrentes e recibos/dados. Migrações devem ser compatíveis e restauráveis. Desligar a capacidade afetada mantendo checkout, ajuda estática e atendimento; não restaurar o agente Pilates. Nenhum rollback/deploy remoto está autorizado por este documento.
