# Execução preparada — 017: Cinco ferramentas e ciclo de leads/clientes

Preparação técnica baseada no código inspecionado; não é autorização para iniciar esta spec nem evidência de integração. Estado de execução continua em `STATUS.json` e `planning/tasks.json`.

**Responsável funcional:** Backend comercial + app/billing. Pessoa responsável ainda deve ser nomeada. Arquivos compartilhados: executor único, sem subagentes.
**Dependências de spec:** 014, 015, 016; todas devem estar concluídas antes de ativar esta spec.

## Fontes confirmadas

- `app/api/landing/ai-attendant/route.ts`
- `lib/landing/ai-attendant/conversion.ts`
- `lib/landing/ai-attendant/leads.ts`
- `lib/landing/ai-attendant/sales-inbox-store.ts`
- `app/api/landing/ai-attendant/whatsapp/route.ts`
- `docs/taliya-sdd/contracts/tools.json`

Hashes e commits: `../../docs/taliya-sdd/planning/execution.json`. Revalidar diff antes de implementar; hashes documentam esta inspeção, não congelam evolução legítima.

## Interfaces, dados e falhas

Modelo pede operação; backend resolve contexto, autorização, evidência e resultado. Um dono por efeito entre tools, pós-processamento Next e webhooks. Billing produz compra/renovação/acesso; ferramentas nunca cobram nem marcam pago.

Projeções usam IDs canônicos/versão/event_id; registros órfãos vão para reconciliação. Reutilizar recibos/outbox de 014/016 e migrações aditivas. Duplicado devolve mesmo recibo; conflito de versão recarrega autoridade, não sobrescreve.

## Caminhos propostos para o diff

Ainda não implementados; são destinos locais propostos, nunca endpoints publicados. Preferir extensão equivalente existente se descoberta, atualizando este mapa antes do código.

- `services/taliya-agent-runtime/app/core/taliya_commercial_managed/tools/`
- `lib/landing/ai-attendant/billing-projection.ts`
- `scripts/tests/sdd/commercial-effects.test.mjs`

## Tarefas detalhadas

Os IDs e checkboxes canônicos permanecem em `tasks.md`; as descrições abaixo detalham a entrega sem marcar progresso. Fontes/caminhos acima são o recorte compartilhado desta spec. Não executar tarefas remotas sem a permissão específica registrada.

### T017-01

**Requisitos/casos:** R017-01 → C017-01.
**Pré-requisitos locais:** nenhum adicional. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Implementar somente cinco handlers a partir de tools.json; contexto de autorização fora dos argumentos do modelo.

**Verificação:** Schema estrito e resultado por recibo; SQL genérico, mark_paid, URLs livres e 6a ferramenta rejeitados.
**Evidência:** `specs/017-ferramentas-e-ciclo-comercial/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T017-02

**Requisitos/casos:** R017-02 → C017-02.
**Pré-requisitos locais:** T017-01. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Atualizar contato com allowlist e evidence_message_id original da conversa autorizada.

**Verificação:** Mensagem fabricada/de outra conversa e alteração de auth/consentimento financeiro não produzem patch.
**Evidência:** `specs/017-ferramentas-e-ciclo-comercial/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T017-03

**Requisitos/casos:** R017-03, R017-04, R017-05 → C017-03, C017-04, C017-05.
**Pré-requisitos locais:** T017-01. **Pendências externas diretas:** B013-01.
**Execução:** local_after_dependencies.

Consumir eventos reais de app/billing para projeção comercial e reconciliar IDs/ordem.

**Verificação:** Compra sem chat cria vínculo uma vez; renovação não cria novo cliente; replay/falsa assinatura não ativa acesso.
**Evidência:** `specs/017-ferramentas-e-ciclo-comercial/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T017-04

**Requisitos/casos:** R017-05 → C017-05.
**Pré-requisitos locais:** T017-02, T017-03. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Remover escrita duplicada do pós-processamento Next para o caminho novo e marcar origem legado.

**Verificação:** Tool+webhook+retry resultam num efeito; histórico preservado e nunca importado como instrução de sistema.
**Evidência:** `specs/017-ferramentas-e-ciclo-comercial/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T017-05

**Requisitos/casos:** R017-01, R017-03, R017-04 → C017-01, C017-03, C017-04.
**Pré-requisitos locais:** T017-01, T017-03. **Pendências externas diretas:** B013-01.
**Execução:** local_after_dependencies.

Resolver subscribe/resume/open_app/manage/verify via serviço existente e autorização server-side.

**Verificação:** Cliente ativo abre destino correto; URL retorno adulterada não paga; ferramenta não inicia operação financeira.
**Evidência:** `specs/017-ferramentas-e-ciclo-comercial/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T017-06

**Requisitos/casos:** R017-01, R017-02, R017-03, R017-04, R017-05 → C017-01, C017-02, C017-03, C017-04, C017-05.
**Pré-requisitos locais:** T017-04, T017-05. **Pendências externas diretas:** B013-03.
**Execução:** authorized_environment.

Cobrir contratação direta/assistida, cancelamento/estorno, renovação e contatos históricos.

**Verificação:** Cancelamento preserva período pago; pedido de estorno difere de concluído; uma pessoa multi-negócio não duplica receita.
**Evidência:** `specs/017-ferramentas-e-ciclo-comercial/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

## Sequência de verificação

1. Ler spec/plan/tasks/verification, este recorte e contratos referenciados; resolver esclarecimentos materiais e atualizar data-model/contrato quando o serviço real exigir.
2. Implementar teste negativo pertinente antes do efeito; separar mocks locais, integração sandbox e modelo real.
3. Rodar lint/build/tipos do código tocado e teste específico disponível. Os novos caminhos de testes acima são propostos; não alegar comando disponível antes de adicioná-lo ao repo.
4. Consultar `../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md` para comandos existentes e restrições. Não rodar eval legado em lote: há chamadas pagas e expectativas antigas.
5. Comparar critério de aceite de cada R/C em spec.md e verification.md, executar convergência e registrar pendências. Só então atualizar tasks/status/matriz e pointer.

## Reversão do recorte

Reverter somente o diff identificado desta entrega; preservar alterações concorrentes e recibos/dados. Migrações devem ser compatíveis e restauráveis. Desligar a capacidade afetada mantendo checkout, ajuda estática e atendimento; não restaurar o agente Pilates. Nenhum rollback/deploy remoto está autorizado por este documento.
