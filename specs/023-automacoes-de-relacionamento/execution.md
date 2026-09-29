# Execução preparada — 023: Automações enxutas de relacionamento

Preparação técnica baseada no código inspecionado; não é autorização para iniciar esta spec nem evidência de integração. Estado de execução continua em `STATUS.json` e `planning/tasks.json`.

**Responsável funcional:** Operação + backend/analytics. Pessoa responsável ainda deve ser nomeada. Arquivos compartilhados: executor único, sem subagentes.
**Dependências de spec:** 017, 020, 021, 022; todas devem estar concluídas antes de ativar esta spec.

## Fontes confirmadas

- `lib/landing/ai-attendant/n8n.ts`
- `docs/taliya-sdd/09_CONTEUDO_UX_E_AUTOMACOES.md`

Hashes e commits: `../../docs/taliya-sdd/planning/execution.json`. Revalidar diff antes de implementar; hashes documentam esta inspeção, não congelam evolução legítima.

## Interfaces, dados e falhas

PostHog segmenta; backend revalida opt-in/opt-out, humano, pagamento/acesso e canal imediatamente antes da entrega. Integrar provedor existente identificado; nunca criar motor próprio nem mensagens transacionais duplicadas.

Reusar ledger/outbox/dedup por gatilho/alvo/janela. Três fluxos desligados por padrão. Dry-run não envia. Timeout após aceite exige consultar recibo antes de repetir. Canais/templates/limites dependem homologação e aprovação de ativação.

## Caminhos propostos para o diff

Ainda não implementados; são destinos locais propostos, nunca endpoints publicados. Preferir extensão equivalente existente se descoberta, atualizando este mapa antes do código.

- `lib/landing/ai-attendant/relationship-eligibility.ts`
- `docs/taliya-sdd/operations/relationship-flows.md`
- `scripts/tests/sdd/relationship.test.mjs`

## Tarefas detalhadas

Os IDs e checkboxes canônicos permanecem em `tasks.md`; as descrições abaixo detalham a entrega sem marcar progresso. Fontes/caminhos acima são o recorte compartilhado desta spec. Não executar tarefas remotas sem a permissão específica registrada.

### T023-01

**Requisitos/casos:** R023-03 → C023-03.
**Pré-requisitos locais:** nenhum adicional. **Pendências externas diretas:** B013-01.
**Execução:** local_after_dependencies.

Inventariar notificações do billing/app/n8n/PostHog e fixar um dono por mensagem.

**Verificação:** Confirmação/cobrança/estorno permanecem no emissor existente; nenhum envio duplicado.
**Evidência:** `specs/023-automacoes-de-relacionamento/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T023-02

**Requisitos/casos:** R023-01 → C023-01.
**Pré-requisitos locais:** T023-01. **Pendências externas diretas:** B013-03.
**Execução:** local_after_dependencies.

Configurar três fluxos no sistema existente, Workflows se disponível/aprovado; exportar desligados.

**Verificação:** Dry-run registra elegíveis sem enviar; ausência de licença não cria motor novo.
**Evidência:** `specs/023-automacoes-de-relacionamento/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T023-03

**Requisitos/casos:** R023-02 → C023-02.
**Pré-requisitos locais:** T023-01. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Implementar entrega autenticada com consulta de estado atual e revalidação de consentimento/pausa.

**Verificação:** Pagamento ou opt-out entre segmento e entrega cancela envio; webhook falso/duplicado não envia.
**Evidência:** `specs/023-automacoes-de-relacionamento/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T023-04

**Requisitos/casos:** R023-01, R023-04 → C023-01, C023-04.
**Pré-requisitos locais:** T023-01. **Pendências externas diretas:** B013-03.
**Execução:** local_after_dependencies.

Preparar templates, destino autenticado e opt-out sem descontos ou promessas inventadas.

**Verificação:** Preview sanitizado aprovado; link não contém credencial; provedor/canal/template reais identificados.
**Evidência:** `specs/023-automacoes-de-relacionamento/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T023-05

**Requisitos/casos:** R023-02, R023-03, R023-04 → C023-02, C023-03, C023-04.
**Pré-requisitos locais:** T023-02, T023-03, T023-04. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Testar corrida com pagamento, humano, opt-out, falha e rate limit com ledger único.

**Verificação:** Máximo por gatilho e teto global proposto 1/7 dias; timeout pós-aceite não gera segundo envio.
**Evidência:** `specs/023-automacoes-de-relacionamento/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T023-06

**Requisitos/casos:** R023-01, R023-02, R023-03, R023-04, R023-05 → C023-01, C023-02, C023-03, C023-04, C023-05.
**Pré-requisitos locais:** T023-05. **Pendências externas diretas:** B013-03.
**Execução:** authorized_environment.

Preparar ativação gradual com donos, canal, volume, orçamento e kill switch.

**Verificação:** Só ativar após aprovação específica registrada; nesta entrega permanece desligado e sem pessoas reais.
**Evidência:** `specs/023-automacoes-de-relacionamento/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

## Sequência de verificação

1. Ler spec/plan/tasks/verification, este recorte e contratos referenciados; resolver esclarecimentos materiais e atualizar data-model/contrato quando o serviço real exigir.
2. Implementar teste negativo pertinente antes do efeito; separar mocks locais, integração sandbox e modelo real.
3. Rodar lint/build/tipos do código tocado e teste específico disponível. Os novos caminhos de testes acima são propostos; não alegar comando disponível antes de adicioná-lo ao repo.
4. Consultar `../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md` para comandos existentes e restrições. Não rodar eval legado em lote: há chamadas pagas e expectativas antigas.
5. Comparar critério de aceite de cada R/C em spec.md e verification.md, executar convergência e registrar pendências. Só então atualizar tasks/status/matriz e pointer.

## Reversão do recorte

Reverter somente o diff identificado desta entrega; preservar alterações concorrentes e recibos/dados. Migrações devem ser compatíveis e restauráveis. Desligar a capacidade afetada mantendo checkout, ajuda estática e atendimento; não restaurar o agente Pilates. Nenhum rollback/deploy remoto está autorizado por este documento.
