# Execução preparada — 024: QA integrada, segurança, performance e evals

Preparação técnica baseada no código inspecionado; não é autorização para iniciar esta spec nem evidência de integração. Estado de execução continua em `STATUS.json` e `planning/tasks.json`.

**Responsável funcional:** QA + backend/frontend + produto. Pessoa responsável ainda deve ser nomeada. Arquivos compartilhados: executor único, sem subagentes.
**Dependências de spec:** 018, 019, 020, 021, 022, 023; todas devem estar concluídas antes de ativar esta spec.

## Fontes confirmadas

- `package.json`
- `scripts`
- `services/taliya-agent-runtime/tests`
- `docs/taliya-sdd/evals/acceptance-cases.json`
- `docs/taliya-sdd/06_TESTES_E_ACEITE.md`

Hashes e commits: `../../docs/taliya-sdd/planning/execution.json`. Revalidar diff antes de implementar; hashes documentam esta inspeção, não congelam evolução legítima.

## Interfaces, dados e falhas

Separar testes locais, banco descartável, integração sandbox e modelo real pago. Casos do plano vinculados ao código; fixture prova comportamento local, nunca integração real. Portar invariantes legados sem preservar expectativa Pilates.

Nenhuma migração de domínio. Ambiente isolado com egress bloqueado nas suítes offline; credenciais via mecanismo seguro. Relatórios possuem commit, amostra, custo, caso, esperado/obtido e evidência; sem resultados sintéticos verdes.

## Caminhos propostos para o diff

Ainda não implementados; são destinos locais propostos, nunca endpoints publicados. Preferir extensão equivalente existente se descoberta, atualizando este mapa antes do código.

- `scripts/tests/sdd/README.md`
- `docs/taliya-sdd/evidence/homologation/`
- `docs/taliya-sdd/evals/legacy-test-disposition.json`

## Tarefas detalhadas

Os IDs e checkboxes canônicos permanecem em `tasks.md`; as descrições abaixo detalham a entrega sem marcar progresso. Fontes/caminhos acima são o recorte compartilhado desta spec. Não executar tarefas remotas sem a permissão específica registrada.

### T024-01

**Requisitos/casos:** R024-01 → C024-01.
**Pré-requisitos locais:** nenhum adicional. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Criar comandos explícitos separados offline/DB descartável/sandbox/live e CI do código tocado.

**Verificação:** Suíte offline falha se tentar rede; scripts antigos pagos não entram no comando local por engano.
**Evidência:** `specs/024-qualidade-e-homologacao/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T024-02

**Requisitos/casos:** R024-01, R024-02 → C024-01, C024-02.
**Pré-requisitos locais:** T024-01. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Classificar casos legados preservar/adaptar/arquivar e ligar os 68 casos vigentes a testes/evidências.

**Verificação:** Nenhum teste é excluído só por falhar; invariantes mantidas, expectativas Pilates não governam produto atual.
**Evidência:** `specs/024-qualidade-e-homologacao/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T024-03

**Requisitos/casos:** R024-03 → C024-03.
**Pré-requisitos locais:** T024-01, T024-02. **Pendências externas diretas:** B013-03.
**Execução:** authorized_environment.

Regredir mensal/anual x cartão/Pix Automático no billing implementado na 015, em sandbox autorizado.

**Verificação:** Confirmação/falha/retomada/replay/cancelamento/estorno por IDs reais sanitizados, sem fixture como homologação.
**Evidência:** `specs/024-qualidade-e-homologacao/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T024-04

**Requisitos/casos:** R024-04 → C024-04.
**Pré-requisitos locais:** T024-01, T024-02. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Executar fault injection, IDOR, URLs, cookies, takeover, recuperação, a11y e desempenho.

**Verificação:** Asserts de banco/recibo e screenshots; sample/dispositivo/rede reportados; sem falsa medição de campo.
**Evidência:** `specs/024-qualidade-e-homologacao/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T024-05

**Requisitos/casos:** R024-02, R024-05 → C024-02, C024-05.
**Pré-requisitos locais:** T024-01, T024-02. **Pendências externas diretas:** B013-03.
**Execução:** authorized_environment.

Executar Luna/max com orçamento autorizado, rubric e revisão humana; repetir críticos >=3 vezes.

**Verificação:** Zero falha crítica; medir utilidade, p95 e custo com n e limites; modelo/esforço explicitamente comprovados.
**Evidência:** `specs/024-qualidade-e-homologacao/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T024-06

**Requisitos/casos:** R024-01, R024-02, R024-03, R024-04, R024-05 → C024-01, C024-02, C024-03, C024-04, C024-05.
**Pré-requisitos locais:** T024-03, T024-04, T024-05. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Rodar análise/convergência e consolidar dossiê por commit antes da 025.

**Verificação:** Zero P0/P1 aberto e todos casos com resultado adequado; falha gera tarefa corretiva, não ajuste do aceite.
**Evidência:** `specs/024-qualidade-e-homologacao/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

## Sequência de verificação

1. Ler spec/plan/tasks/verification, este recorte e contratos referenciados; resolver esclarecimentos materiais e atualizar data-model/contrato quando o serviço real exigir.
2. Implementar teste negativo pertinente antes do efeito; separar mocks locais, integração sandbox e modelo real.
3. Rodar lint/build/tipos do código tocado e teste específico disponível. Os novos caminhos de testes acima são propostos; não alegar comando disponível antes de adicioná-lo ao repo.
4. Consultar `../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md` para comandos existentes e restrições. Não rodar eval legado em lote: há chamadas pagas e expectativas antigas.
5. Comparar critério de aceite de cada R/C em spec.md e verification.md, executar convergência e registrar pendências. Só então atualizar tasks/status/matriz e pointer.

## Reversão do recorte

Reverter somente o diff identificado desta entrega; preservar alterações concorrentes e recibos/dados. Migrações devem ser compatíveis e restauráveis. Desligar a capacidade afetada mantendo checkout, ajuda estática e atendimento; não restaurar o agente Pilates. Nenhum rollback/deploy remoto está autorizado por este documento.
