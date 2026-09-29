# Execução preparada — 020: Taliya Internal mínimo e operação humana

Preparação técnica baseada no código inspecionado; não é autorização para iniciar esta spec nem evidência de integração. Estado de execução continua em `STATUS.json` e `planning/tasks.json`.

**Responsável funcional:** Frontend/backend + operação. Pessoa responsável ainda deve ser nomeada. Arquivos compartilhados: executor único, sem subagentes.
**Dependências de spec:** 014, 017; todas devem estar concluídas antes de ativar esta spec.

## Fontes confirmadas

- `components/internal/SalesInboxClient.tsx`
- `app/internal/sales-inbox/page.tsx`
- `app/api/internal/sales-inbox/leads/[leadId]/actions/route.ts`
- `next.config.ts`
- `lib/landing/ai-attendant/sales-inbox-store.ts`

Hashes e commits: `../../docs/taliya-sdd/planning/execution.json`. Revalidar diff antes de implementar; hashes documentam esta inspeção, não congelam evolução legítima.

## Interfaces, dados e falhas

Escolher fonte autoritativa só com B013-02. Internal independente usa /internal/actions, cookie de staff e commercial-ops.v2; embedded usa outro contrato. Aplicar UI/rotas no repo dono, remover exposição duplicada somente após verificar roteamento. Não desenvolver duas caixas.

take_over/resume usam versão de atendimento + ator verificado + recibo + outbox na mesma transação onde possível. Worker/dispatcher rejeitam versão anterior antes da operação e da entrega. Janela WhatsApp deriva da última mensagem inbound, não lead.updatedAt.

## Caminhos propostos para o diff

Ainda não implementados; são destinos locais propostos, nunca endpoints publicados. Preferir extensão equivalente existente se descoberta, atualizando este mapa antes do código.

- `docs/taliya-sdd/operations/internal-cutover.md`
- `scripts/tests/sdd/human-handoff.test.mjs`

Fontes externas read-only: `services/security/internal-auth.ts`, `services/operators/current-operator.ts`, `services/views/operational-view.ts`, `services/actions/postgres-rpc-actions.ts`, `app/internal/actions/route.ts` em `lucasquintino/taliya-internal`, SHA `7cbe9e9b92a4d3b18b3961ab51f9eec10515b38e`. O checkout em `/tmp` é referência; obter checkout de trabalho do deployment confirmado antes de editar.

## Tarefas detalhadas

Os IDs e checkboxes canônicos permanecem em `tasks.md`; as descrições abaixo detalham a entrega sem marcar progresso. Fontes/caminhos acima são o recorte compartilhado desta spec. Não executar tarefas remotas sem a permissão específica registrada.

### T020-01

**Requisitos/casos:** R020-01 → C020-01.
**Pré-requisitos locais:** nenhum adicional. **Pendências externas diretas:** B013-02.
**Execução:** authorized_environment.

Confirmar implantação/contratos reais e escolher um Internal; planejar corte das rotas duplicadas.

**Verificação:** Mapa URL→repo→SHA→banco e auth verificados; não editar clone temporário como se fosse deploy ativo.
**Evidência:** `specs/020-internal-minimo/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T020-02

**Requisitos/casos:** R020-02, R020-05 → C020-02, C020-05.
**Pré-requisitos locais:** T020-01. **Pendências externas diretas:** B013-02.
**Execução:** local_after_dependencies.

Reusar fila/ficha atuais e projetar conta/business/assinatura oficiais; retirar métricas financeiras manuais.

**Verificação:** Sem funil Pilates ou editor de pagamento/acesso; suporte enxerga status derivado e links autorizados.
**Evidência:** `specs/020-internal-minimo/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T020-03

**Requisitos/casos:** R020-04 → C020-04.
**Pré-requisitos locais:** T020-01. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Unificar take_over/resume_ai e handoff via versão/lock/recibo consumidos por tools/worker/dispatcher.

**Verificação:** Corrida entre operador, tool e entrega: nenhuma escrita/resposta tardia após pausa; retomada exige papel válido.
**Evidência:** `specs/020-internal-minimo/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T020-04

**Requisitos/casos:** R020-03 → C020-03.
**Pré-requisitos locais:** T020-03. **Pendências externas diretas:** B013-03.
**Execução:** authorized_environment.

Entregar humano no canal original com receipt e timestamp inbound WhatsApp correto.

**Verificação:** Web não recebe falso sucesso de envio WhatsApp; atualização da ficha não reabre janela; falha é explícita.
**Evidência:** `specs/020-internal-minimo/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T020-05

**Requisitos/casos:** R020-02, R020-05 → C020-02, C020-05.
**Pré-requisitos locais:** T020-02. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Limitar pesquisa/filtros/notas/atalhos oficiais aos papéis permitidos e dados necessários.

**Verificação:** Viewer não modifica; mark_won não produz pagamento; nenhum CRM/BI/editor adicional.
**Evidência:** `specs/020-internal-minimo/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T020-06

**Requisitos/casos:** R020-01, R020-02, R020-03, R020-04, R020-05 → C020-01, C020-02, C020-03, C020-04, C020-05.
**Pré-requisitos locais:** T020-04, T020-05. **Pendências externas diretas:** B013-03.
**Execução:** authorized_environment.

Ensaiar operação com usuários sintéticos, dois operadores, erro de canal e audit trail.

**Verificação:** Ator servidor, request_id e efeito correlacionados; instruções de recuperação e limite operacional documentados.
**Evidência:** `specs/020-internal-minimo/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

## Sequência de verificação

1. Ler spec/plan/tasks/verification, este recorte e contratos referenciados; resolver esclarecimentos materiais e atualizar data-model/contrato quando o serviço real exigir.
2. Implementar teste negativo pertinente antes do efeito; separar mocks locais, integração sandbox e modelo real.
3. Rodar lint/build/tipos do código tocado e teste específico disponível. Os novos caminhos de testes acima são propostos; não alegar comando disponível antes de adicioná-lo ao repo.
4. Consultar `../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md` para comandos existentes e restrições. Não rodar eval legado em lote: há chamadas pagas e expectativas antigas.
5. Comparar critério de aceite de cada R/C em spec.md e verification.md, executar convergência e registrar pendências. Só então atualizar tasks/status/matriz e pointer.

## Reversão do recorte

Reverter somente o diff identificado desta entrega; preservar alterações concorrentes e recibos/dados. Migrações devem ser compatíveis e restauráveis. Desligar a capacidade afetada mantendo checkout, ajuda estática e atendimento; não restaurar o agente Pilates. Nenhum rollback/deploy remoto está autorizado por este documento.
