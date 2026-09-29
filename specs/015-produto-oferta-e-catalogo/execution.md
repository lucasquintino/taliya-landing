# Execução preparada — 015: Fonte única de produto, oferta, billing e materiais

Preparação técnica baseada no código inspecionado; não é autorização para iniciar esta spec nem evidência de integração. Estado de execução continua em `STATUS.json` e `planning/tasks.json`.

**Responsável funcional:** Produto + frontend/backend. Pessoa responsável ainda deve ser nomeada. Arquivos compartilhados: executor único, sem subagentes.
**Dependências de spec:** 013 e 014; ambas devem estar concluídas antes de ativar esta spec.

## Fontes confirmadas

- `data/landing/niches/pilates.ts`
- `lib/landing/ai-attendant/commercial-knowledge.ts`
- `services/taliya-agent-runtime/app/shared/product_knowledge/source.py`
- `docs/taliya-sdd/contracts/material.schema.json`
- `docs/taliya-sdd/contracts/materials.catalog.json`
- App Copiloto: `supabase/migrations/20260922142218_e01_identity_access.sql`, `supabase/migrations/20260922142222_e01_access_policy.sql`, `supabase/functions/_shared/business-context.ts`, `supabase/functions/_shared/access-gate.ts`

Hashes e commits: `../../docs/taliya-sdd/planning/execution.json`. Revalidar diff antes de implementar; hashes documentam esta inspeção, não congelam evolução legítima.

## Interfaces, dados e falhas

Construir fonte de oferta versionada no backend do app, com leitura pública limitada, tentativa de contratação autenticada e dois adaptadores Asaas: Checkout recorrente hospedado para cartão e autorização Pix Automático. Nenhuma API foi implantada nesta preparação. Conta/eligibilidade Asaas e homologação aguardam B013-01/B013-03. Landing e agente lerão a mesma versão; catálogo compartilhado permanece como dados versionados no repo, sem CMS nem preço no prompt.

No app, migrations aditivas precisarão de oferta/versionamento, tentativa/recibo, vínculo com cliente/checkout/autorização/assinatura do provedor, inbox de webhook e estado financeiro auditável. Reutilizar `business_id`, Auth e `access_entitlements`; nenhuma identidade paralela. Hash/constraint de idempotência e transições de estado impedem efeito duplicado; resultado remoto desconhecido exige consulta/reconciliação antes de repetir. Cache invalida mudança de oferta/retirada. Erros distinguem auth, negócio inexistente, plano/forma indisponível, conflito, timeout, fonte inválida e material ausente; não responder preço vencido como atual.

## Caminhos propostos para o diff

Ainda não implementados; são destinos locais propostos, nunca endpoints publicados. Preferir extensão equivalente existente se descoberta, atualizando este mapa antes do código.

- `lib/landing/ai-attendant/offer-source.ts`
- `lib/landing/ai-attendant/material-catalog.ts`
- `scripts/tests/sdd/catalog.test.mjs`
- No repo Copiloto, após revisar seus AGENTS e fonte atual: `supabase/functions/billing-offer/`, `billing-checkout/`, `billing-webhook/`, `billing-operations/`, migration versionada criada pelo CLI, `packages/domain/src/billing/` e testes focados. Estes são candidatos, não endpoints publicados.

## Tarefas detalhadas

Os IDs e checkboxes canônicos permanecem em `tasks.md`; as descrições abaixo detalham a entrega sem marcar progresso. Fontes/caminhos acima são o recorte compartilhado desta spec. Não executar tarefas remotas sem a permissão específica registrada.

### T015-01

**Requisitos/casos:** R015-01 → C015-01.
**Pré-requisitos locais:** nenhum adicional. **Pendências externas diretas:** nenhuma para o catálogo de capacidades.
**Execução:** local_after_dependencies.

Confrontar capacidades do produto publicado com commercial-knowledge.ts/source.py; retirar pressupostos Pilates da fonte nova.

**Verificação:** Fixture de recurso não confirmado retorna indisponível; nenhum diagnóstico legado vira requisito.
**Evidência:** `specs/015-produto-oferta-e-catalogo/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T015-02

**Requisitos/casos:** R015-02, R015-05 → C015-02, C015-05.
**Pré-requisitos locais:** T015-01. **Pendências externas diretas:** confirmação de preços vigentes para publicação; trabalho estrutural local pode avançar.
**Execução:** local_after_dependencies.

Implementar fonte server-side e leitor da oferta versionada com centavos/BRL, vigência, disponibilidade e garantia, reusados por landing/agente/checkout.

**Verificação:** Alteração de preço/URL na autoridade propaga; mensal/anual e garantia não anunciam trial; falha não inventa preço.
**Evidência:** `specs/015-produto-oferta-e-catalogo/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T015-03

**Requisitos/casos:** R015-03 → C015-03.
**Pré-requisitos locais:** T015-01. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Adaptar catálogo/schema compartilhado existente para leitura pelo frontend e runtime.

**Verificação:** Mesmo asset_id/versão resolve nas duas linguagens; schema rejeita propriedade extra e item sem direitos.
**Evidência:** `specs/015-produto-oferta-e-catalogo/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T015-04

**Requisitos/casos:** R015-03 → C015-03.
**Pré-requisitos locais:** T015-03. **Pendências externas diretas:** B013-04.
**Execução:** local_after_dependencies.

Incluir somente arquivos reais com aprovação, direitos, resumo/transcrição e captions; manter ausentes ocultos.

**Verificação:** Nenhum UGC ilustrativo é depoimento; registro sem autorização não fica publicado.
**Evidência:** `specs/015-produto-oferta-e-catalogo/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T015-05

**Requisitos/casos:** R015-03, R015-04, R015-05 → C015-03, C015-04, C015-05.
**Pré-requisitos locais:** T015-03. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Implementar verificação editorial/URLs allowlist/protocolo/versionamento/retirada antes de consumir material.

**Verificação:** URL arbitrária, aprovação ausente, revisão vencida e retired são recusados; não criar CMS.
**Evidência:** `specs/015-produto-oferta-e-catalogo/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T015-06

**Requisitos/casos:** R015-01 a R015-08 → C015-01 a C015-08.
**Pré-requisitos locais:** T015-02, T015-04, T015-05, T015-10, T015-11, T015-12. **Pendências externas diretas:** B013-01, B013-03, B013-04 para aceite integral.
**Execução:** local_after_dependencies.

Convergir oferta, billing e catálogo; testar mudança de versão/retirada durante conversa e escrever guia de operação com dono.

**Verificação:** Sessão antiga não emite item retirado nem preço obsoleto; erro recuperável e versão observáveis.
**Evidência:** `specs/015-produto-oferta-e-catalogo/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T015-07

**Requisitos/casos:** R015-06, R015-07 → C015-06, C015-07.
**Pré-requisitos locais:** T015-02 e 014 concluída. **Pendências externas diretas:** nenhuma para migration local.
**Execução:** local_after_dependencies.

Criar modelo/migrações de tentativas, vínculo Asaas por negócio e fatos financeiros sem alterar Auth.

**Verificação:** Preço em centavos e versão ficam fixos por tentativa; cross-business é negado; intenção não cria entitlement.
**Evidência:** `specs/015-produto-oferta-e-catalogo/verification.md`: migration/revisão de grants, teste local de banco descartável, rollback e payload sanitizado.

### T015-08

**Requisitos/casos:** R015-06 → C015-06.
**Pré-requisitos locais:** T015-07. **Pendências externas diretas:** B013-01 somente para sandbox/ativação.
**Execução:** local_after_dependencies.

Implementar checkout hospedado para cartão recorrente mensal/anual com idempotência e retorno sem concessão de acesso.

**Verificação:** Contrato local separa criação de confirmação; timeout não recria checkout; callback não ativa entitlement.
**Evidência:** `specs/015-produto-oferta-e-catalogo/verification.md`: testes de adaptador sem rede, depois resultado sandbox autorizado.

### T015-09

**Requisitos/casos:** R015-06, R015-07 → C015-06, C015-07.
**Pré-requisitos locais:** T015-07. **Pendências externas diretas:** B013-01 somente para elegibilidade/sandbox.
**Execução:** local_after_dependencies.

Implementar Pix Automático mensal/anual com QR inicial e estado de autorização separado do pagamento.

**Verificação:** Pagamento inicial recebido não implica recorrência ativa; recusa posterior mantém fatos independentes e não agenda outro débito.
**Evidência:** `specs/015-produto-oferta-e-catalogo/verification.md`: testes de transição sem rede, depois fluxo sandbox autorizado.

### T015-10

**Requisitos/casos:** R015-07 → C015-07.
**Pré-requisitos locais:** T015-07, T015-08 e T015-09. **Pendências externas diretas:** B013-01 somente para webhook real.
**Execução:** local_after_dependencies.

Implementar webhook autenticado, inbox, processamento idempotente, reconciliação e projeção de acesso.

**Verificação:** Duplicado, fora de ordem e reinício têm um efeito; HTTP 200 só após persistência; redirect/chat não liberam acesso.
**Evidência:** `specs/015-produto-oferta-e-catalogo/verification.md`: banco descartável, testes de eventos sintéticos identificados e depois webhook sandbox.

### T015-11

**Requisitos/casos:** R015-08 → C015-08.
**Pré-requisitos locais:** T015-10. **Pendências externas diretas:** política exata de acesso ao primeiro ciclo Pix pago sem autorização ativa; sandbox para efeito real.
**Execução:** local_after_dependencies.

Implementar consulta/gestão de assinatura, cancelamento e solicitação de reembolso com estados explícitos.

**Verificação:** Solicitação não confirma reembolso; timeout mantém pendente/reconciliação; acesso segue períodos pagos e política ratificada.
**Evidência:** `specs/015-produto-oferta-e-catalogo/verification.md`: testes locais de estado e sandbox autorizado.

### T015-12

**Requisitos/casos:** R015-06, R015-07, R015-08 → C015-06, C015-07, C015-08.
**Pré-requisitos locais:** T015-08, T015-09, T015-10 e T015-11. **Pendências externas diretas:** B013-01, B013-03.
**Execução:** authorized_environment.

Homologar no sandbox autorizado as quatro combinações, falhas, replay, cancelamento e garantia.

**Verificação:** Registrar requisições/respostas sanitizadas, cobrança inicial, autorização Pix, webhooks, entitlement, custo e recuperação; zero dinheiro real.
**Evidência:** `specs/015-produto-oferta-e-catalogo/verification.md`: SHA, ambiente, conta de teste, matriz 2×2, esperados/obtidos e limites.

## Sequência de verificação

1. Ler spec/plan/tasks/verification, este recorte e contratos referenciados; resolver esclarecimentos materiais e atualizar data-model/contrato quando o serviço real exigir.
2. Implementar teste negativo pertinente antes do efeito; separar mocks locais, integração sandbox e modelo real.
3. Rodar lint/build/tipos do código tocado e teste específico disponível. Os novos caminhos de testes acima são propostos; não alegar comando disponível antes de adicioná-lo ao repo.
4. Consultar `../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md` para comandos existentes e restrições. Não rodar eval legado em lote: há chamadas pagas e expectativas antigas.
5. Comparar critério de aceite de cada R/C em spec.md e verification.md, executar convergência e registrar pendências. Só então atualizar tasks/status/matriz e pointer.

## Reversão do recorte

Reverter somente o diff identificado desta entrega; preservar alterações concorrentes e recibos/dados. Migrações devem ser compatíveis e restauráveis. Desligar a capacidade afetada mantendo checkout, ajuda estática e atendimento; não restaurar o agente Pilates. Nenhum rollback/deploy remoto está autorizado por este documento.
