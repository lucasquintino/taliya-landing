# Execução preparada — 013: Fundação, governança e contratos da Taliya

Preparação técnica baseada no código inspecionado; não é autorização para iniciar esta spec nem evidência de integração. Estado de execução continua em `STATUS.json` e `planning/tasks.json`.

**Responsável funcional:** Liderança técnica + responsável pelo produto. Pessoa responsável ainda deve ser nomeada. Arquivos compartilhados: executor único, sem subagentes.
**Dependências de spec:** nenhuma; todas devem estar concluídas antes de ativar esta spec.

## Fontes confirmadas

- `docs/taliya-sdd/contracts/current-contracts.md`
- `next.config.ts`
- `.specify/feature.json`

Hashes e commits: `../../docs/taliya-sdd/planning/execution.json`. Revalidar diff antes de implementar; hashes documentam esta inspeção, não congelam evolução legítima.

## Interfaces, dados e falhas

Fechar autoridade das fontes, contrato-alvo do billing a construir e implantação Internal antes de G0. O serviço Asaas não existe conforme esclarecimento do usuário em 2026-09-29; não alterar Auth/app para preencher ausência nem declarar endpoint futuro como publicado. Ver `../../docs/taliya-sdd/DECISAO_BILLING_2026-09-29.md`.

Nenhuma migração. Guardar SHA, diff e evidência sanitizada; scripts locais não homologam serviços.

## Caminhos propostos para o diff

Ainda não implementados; são destinos locais propostos, nunca endpoints publicados. Preferir extensão equivalente existente se descoberta, atualizando este mapa antes do código.

- `docs/taliya-sdd/contracts/integration-handoff.md`

## Tarefas detalhadas

Os IDs e checkboxes canônicos permanecem em `tasks.md`; as descrições abaixo detalham a entrega sem marcar progresso. Fontes/caminhos acima são o recorte compartilhado desta spec. Não executar tarefas remotas sem a permissão específica registrada.

### T013-01

**Requisitos/casos:** R013-01 → C013-01.
**Pré-requisitos locais:** nenhum adicional. **Pendências externas diretas:** B013-02.
**Execução:** local_after_dependencies.

Atualizar matriz landing/runtime/app/Internal com SHA e dono e vincular cada rota ao deployment real.

**Verificação:** Comparar next.config.ts, rota física e URL servida; HTTP 401 isolado não comprova SHA.
**Evidência:** `specs/013-fundacao-e-contratos/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T013-02

**Requisitos/casos:** R013-01, R013-03 → C013-01, C013-03.
**Pré-requisitos locais:** nenhum adicional. **Pendências externas diretas:** nenhuma para o mapa local; sandbox B013-01 é da implementação 015.
**Execução:** local_after_dependencies.

Registrar contrato existente de identidade/negócio/acesso e desenhar as interfaces a implementar para oferta, checkout, assinatura, Pix Automático, webhook e reconciliação; documentar estados, erros e responsáveis sem payload publicado fictício.

**Verificação:** Diferenciar código observado de contrato-alvo; quatro combinações e compra direta permanecem para teste de implementação na 015/024.
**Evidência:** `specs/013-fundacao-e-contratos/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T013-03

**Requisitos/casos:** R013-02 → C013-02.
**Pré-requisitos locais:** nenhum adicional. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Preservar adendo de AGENTS/constituição e pointer 013 separado do número da branch.

**Verificação:** Diff limitado; histórico copy-only intacto e somente 013 ativa.
**Evidência:** `specs/013-fundacao-e-contratos/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T013-04

**Requisitos/casos:** R013-04 → C013-04.
**Pré-requisitos locais:** nenhum adicional. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Manter Bash oficial e versão CLI com procedência; executar prerequisites sem reinicializar.

**Verificação:** FEATURE_DIR deve resolver 013; hash/proveniência e comandos reais registrados.
**Evidência:** `specs/013-fundacao-e-contratos/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T013-05

**Requisitos/casos:** R013-05 → C013-05.
**Pré-requisitos locais:** nenhum adicional. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Reutilizar inventário de mídia e baseline desktop/mobile; registrar permissões e contas pendentes.

**Verificação:** Screenshots e hashes presentes; catálogo vazio não recebe mídia inventada.
**Evidência:** `specs/013-fundacao-e-contratos/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T013-06

**Requisitos/casos:** R013-01, R013-02, R013-03, R013-04, R013-05 → C013-01, C013-02, C013-03, C013-04, C013-05.
**Pré-requisitos locais:** T013-01, T013-02, T013-03, T013-04, T013-05, T013-07, T013-08, T013-09. **Pendências externas diretas:** B013-02, B013-03.
**Execução:** local_after_dependencies.

Consolidar consistência/revisão e evidências de todos os C013 antes de liberar dependentes.

**Verificação:** G0 continua bloqueado enquanto autoridade do Internal e homologação da fundação faltarem; billing funcional é gate da 015, não evidência exigida da 013.
**Evidência:** `specs/013-fundacao-e-contratos/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T013-07

**Requisitos/casos:** R013-01, R013-03 → C013-01, C013-03.
**Pré-requisitos locais:** nenhum adicional. **Pendências externas diretas:** nenhuma para o registro local.
**Execução:** local_after_dependencies.

Registrar que o billing não existe, localizar valores documentados, consultar o contrato oficial Asaas e atribuir construção e testes à 015. A cópia sem Git `taliya-copiloto-landing-incomplete-2026-09-28/specs/003-*` contém contrato antigo com URL placeholder e garantia de 30 dias/oferta anual condicionada; não é fonte do produto novo.

**Verificação:** Decisão do usuário, fonte de valores, contrato-alvo e limites de conta/sandbox registrados; nenhum endpoint ou cobrança alegado como existente. Evidência da busca histórica em `docs/taliya-sdd/evidence/billing-source-search.json`.
**Evidência:** `specs/013-fundacao-e-contratos/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T013-08

**Requisitos/casos:** R013-01 → C013-01.
**Pré-requisitos locais:** nenhum adicional. **Pendências externas diretas:** B013-02.
**Execução:** authorized_environment.

Confirmar URL→deployment→SHA do Internal e fluxo real de staff no serviço autoritativo.

**Verificação:** Prova autenticada sanitizada e origem dos dados; não deduzir versão dos deploys falhados.
**Evidência:** `specs/013-fundacao-e-contratos/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T013-09

**Requisitos/casos:** R013-01, R013-03, R013-05 → C013-01, C013-03, C013-05.
**Pré-requisitos locais:** T013-07, T013-08. **Pendências externas diretas:** B013-03.
**Execução:** authorized_environment.

Receber ambiente sintético, canais, permissões e limite de gasto; executar apenas consultas/testes aprovados da fundação. Homologação financeira das quatro combinações ocorre após a implementação na 015.

**Verificação:** Cinco casos C013 têm evidência adequada; registrar resultados não executados e decisões antes de G0.
**Evidência:** `specs/013-fundacao-e-contratos/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

## Sequência de verificação

1. Ler spec/plan/tasks/verification, este recorte e contratos referenciados; resolver esclarecimentos materiais e atualizar data-model/contrato quando o serviço real exigir.
2. Implementar teste negativo pertinente antes do efeito; separar mocks locais, integração sandbox e modelo real.
3. Rodar lint/build/tipos do código tocado e teste específico disponível. Os novos caminhos de testes acima são propostos; não alegar comando disponível antes de adicioná-lo ao repo.
4. Consultar `../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md` para comandos existentes e restrições. Não rodar eval legado em lote: há chamadas pagas e expectativas antigas.
5. Comparar critério de aceite de cada R/C em spec.md e verification.md, executar convergência e registrar pendências. Só então atualizar tasks/status/matriz e pointer.

## Reversão do recorte

Reverter somente o diff identificado desta entrega; preservar alterações concorrentes e recibos/dados. Migrações devem ser compatíveis e restauráveis. Desligar a capacidade afetada mantendo checkout, ajuda estática e atendimento; não restaurar o agente Pilates. Nenhum rollback/deploy remoto está autorizado por este documento.
