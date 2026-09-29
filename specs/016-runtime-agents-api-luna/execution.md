# Execução preparada — 016: Runtime Agents API com Luna Max

Preparação técnica baseada no código inspecionado; não é autorização para iniciar esta spec nem evidência de integração. Estado de execução continua em `STATUS.json` e `planning/tasks.json`.

**Responsável funcional:** Backend/IA. Pessoa responsável ainda deve ser nomeada. Arquivos compartilhados: executor único, sem subagentes.
**Dependências de spec:** 014, 015; todas devem estar concluídas antes de ativar esta spec.

## Fontes confirmadas

- `lib/landing/ai-attendant/runtime-client.ts`
- `services/taliya-agent-runtime/app/main.py`
- `services/taliya-agent-runtime/pyproject.toml`
- `services/taliya-agent-runtime/app/core/taliya_commercial/outbox.py`
- `services/taliya-agent-runtime/migrations/001_agent_runtime_tables.sql`

Hashes e commits: `../../docs/taliya-sdd/planning/execution.json`. Revalidar diff antes de implementar; hashes documentam esta inspeção, não congelam evolução legítima.

## Interfaces, dados e falhas

Manter Next→Python/HMAC. Adaptador Agents API com Luna/max/none, uma sessão por conversa autorizada, exatamente cinco tools e reply.schema.json. Endpoint/payload/SDK final só após documentação oficial e smoke autorizado; config.intent.json não é request.

Reusar fila/outbox/locks existentes; persistir versão do agente, binding remoto, call/efeito/recibo e cursor de reconciliação. Migração aditiva no dono real de cada tabela, não dois migradores. Versionar lease/fencing e atendimento. Timeout não significa efeito não realizado.

## Caminhos propostos para o diff

Ainda não implementados; são destinos locais propostos, nunca endpoints publicados. Preferir extensão equivalente existente se descoberta, atualizando este mapa antes do código.

- `services/taliya-agent-runtime/app/core/taliya_commercial_managed/`
- `services/taliya-agent-runtime/tests/test_sdd_managed_runtime.py`

## Tarefas detalhadas

Os IDs e checkboxes canônicos permanecem em `tasks.md`; as descrições abaixo detalham a entrega sem marcar progresso. Fontes/caminhos acima são o recorte compartilhado desta spec. Não executar tarefas remotas sem a permissão específica registrada.

### T016-01

**Requisitos/casos:** R016-01, R016-02 → C016-01, C016-02.
**Pré-requisitos locais:** nenhum adicional. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Isolar managed adapter atrás de runtime-client.ts/main.py; definir envelope v2 preservando HMAC e IDs persistidos.

**Verificação:** Contrato local recusa payload inválido; desabilitado oferece jornada estática sem invocar o núcleo Pilates.
**Evidência:** `specs/016-runtime-agents-api-luna/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T016-02

**Requisitos/casos:** R016-01, R016-04 → C016-01, C016-04.
**Pré-requisitos locais:** T016-01. **Pendências externas diretas:** B013-03.
**Execução:** authorized_environment.

Fixar cliente suportado a partir de docs/tipos e smoke real autorizado com tools read-only Luna/max/none.

**Verificação:** Guardar versão/request sanitizado/response; incompatibilidade bloqueia, sem downgrade de modelo ou esforço.
**Evidência:** `specs/016-runtime-agents-api-luna/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T016-03

**Requisitos/casos:** R016-02 → C016-02.
**Pré-requisitos locais:** T016-02. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Persistir agent_version, remote_session_id e conversation_id autorizado; plano para sessões abertas.

**Verificação:** Duas conversas não compartilham sessão; migração pausa turno e transfere só resumo permitido, com recibo.
**Evidência:** `specs/016-runtime-agents-api-luna/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T016-04

**Requisitos/casos:** R016-03 → C016-03.
**Pré-requisitos locais:** T016-03. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Conectar aceite durável à fila existente com worker, lease/fencing, retry limitado e dead-letter.

**Verificação:** Fechar browser/reiniciar worker antes e depois do commit recupera uma única operação por conversa.
**Evidência:** `specs/016-runtime-agents-api-luna/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T016-05

**Requisitos/casos:** R016-03, R016-04 → C016-03, C016-04.
**Pré-requisitos locais:** T016-04. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Tratar required_actions e reconciliação por IDs; salvar efeito+resultado antes de confirmar ao provedor.

**Verificação:** Desconectar após efeito e antes da resposta, reentregar por stream/webhook: mesmo recibo, um efeito.
**Evidência:** `specs/016-runtime-agents-api-luna/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T016-06

**Requisitos/casos:** R016-01, R016-02, R016-03, R016-04, R016-05 → C016-01, C016-02, C016-03, C016-04, C016-05.
**Pré-requisitos locais:** T016-05. **Pendências externas diretas:** B013-03.
**Execução:** authorized_environment.

Aplicar limites de abuso/custo/timeout, validar reply público e medir conjunto real com Luna/max.

**Verificação:** P95/amostra/custo registrados; limite interrompe novas chamadas sem inventar sucesso nem afetar contratação direta.
**Evidência:** `specs/016-runtime-agents-api-luna/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

## Sequência de verificação

1. Ler spec/plan/tasks/verification, este recorte e contratos referenciados; resolver esclarecimentos materiais e atualizar data-model/contrato quando o serviço real exigir.
2. Implementar teste negativo pertinente antes do efeito; separar mocks locais, integração sandbox e modelo real.
3. Rodar lint/build/tipos do código tocado e teste específico disponível. Os novos caminhos de testes acima são propostos; não alegar comando disponível antes de adicioná-lo ao repo.
4. Consultar `../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md` para comandos existentes e restrições. Não rodar eval legado em lote: há chamadas pagas e expectativas antigas.
5. Comparar critério de aceite de cada R/C em spec.md e verification.md, executar convergência e registrar pendências. Só então atualizar tasks/status/matriz e pointer.

## Reversão do recorte

Reverter somente o diff identificado desta entrega; preservar alterações concorrentes e recibos/dados. Migrações devem ser compatíveis e restauráveis. Desligar a capacidade afetada mantendo checkout, ajuda estática e atendimento; não restaurar o agente Pilates. Nenhum rollback/deploy remoto está autorizado por este documento.
