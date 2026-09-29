# Execução preparada — 018: Landing, widget e integração à assinatura

Preparação técnica baseada no código inspecionado; não é autorização para iniciar esta spec nem evidência de integração. Estado de execução continua em `STATUS.json` e `planning/tasks.json`.

**Responsável funcional:** Frontend + design/QA. Pessoa responsável ainda deve ser nomeada. Arquivos compartilhados: executor único, sem subagentes.
**Dependências de spec:** 015, 017; todas devem estar concluídas antes de ativar esta spec.

## Fontes confirmadas

- `components/landing/NicheLandingPage.tsx`
- `components/landing/shared/FloatingAiAttendant.tsx`
- `components/landing/shared/FloatingAiAttendantPanel.tsx`
- `data/landing/niches/pilates.ts`
- `app/page.tsx`
- `app/robots.ts`
- `app/sitemap.ts`
- `next.config.ts`

Hashes e commits: `../../docs/taliya-sdd/planning/execution.json`. Revalidar diff antes de implementar; hashes documentam esta inspeção, não congelam evolução legítima.

## Interfaces, dados e falhas

CTA direto usa destino válido do billing e não espera agente/analytics. Widget apresenta aceite persistido e recupera estado autenticado por polling/SSE conforme transporte escolhido na 016. Browser não fornece identidade nem URL autoritativa.

Sem migração de banco. Preservar layout/rotas aprovadas e redirects atuais. Recuperar offline/reconexão/erro/humano sem spinner infinito; não reenviar efeito automaticamente ao remontar componente.

## Caminhos propostos para o diff

Ainda não implementados; são destinos locais propostos, nunca endpoints publicados. Preferir extensão equivalente existente se descoberta, atualizando este mapa antes do código.

- `scripts/tests/sdd/journey.spec.mjs`

## Tarefas detalhadas

Os IDs e checkboxes canônicos permanecem em `tasks.md`; as descrições abaixo detalham a entrega sem marcar progresso. Fontes/caminhos acima são o recorte compartilhado desta spec. Não executar tarefas remotas sem a permissão específica registrada.

### T018-01

**Requisitos/casos:** R018-01 → C018-01.
**Pré-requisitos locais:** nenhum adicional. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Mapear cada CTA para chat ou checkout real; manter escolha mensal/anual e remover oferta gratuita nos pontos afetados.

**Verificação:** Compra direta funciona com agente/PostHog indisponíveis; destino ausente apresenta erro honesto, não URL inventada.
**Evidência:** `specs/018-landing-widget-e-jornada/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T018-02

**Requisitos/casos:** R018-02, R018-03 → C018-02, C018-03.
**Pré-requisitos locais:** T018-01. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Adaptar widget para reply/schema, asset_id e action refs; usar ID estável do turno/recibo.

**Verificação:** Estados vazio/enviando/esperando/erro/offline/reconectando/humano sem spinner infinito e sem duplo efeito.
**Evidência:** `specs/018-landing-widget-e-jornada/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T018-03

**Requisitos/casos:** R018-03, R018-04 → C018-03, C018-04.
**Pré-requisitos locais:** T018-02. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Recuperar histórico autorizado do servidor após recarga/login sem confiar no histórico do browser.

**Verificação:** Duas abas e reconexão não duplicam mensagem nem exibem conversa alheia; logout limpa contexto privado.
**Evidência:** `specs/018-landing-widget-e-jornada/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T018-04

**Requisitos/casos:** R018-02, R018-04 → C018-02, C018-04.
**Pré-requisitos locais:** T018-02, T018-03. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Comparar baseline desktop/mobile e corrigir somente foco/teclado/scroll/safe area necessários.

**Verificação:** Screenshots mesmas dimensões, contraste/teclado/leitura e toque documentados; composição aprovada preservada.
**Evidência:** `specs/018-landing-widget-e-jornada/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T018-05

**Requisitos/casos:** R018-05 → C018-05.
**Pré-requisitos locais:** T018-01. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Atualizar FAQ/metadata/structured data apenas com fonte vigente; manter redirects/robots/noindex coerentes.

**Verificação:** HTML/JSON-LD não anuncia trial/preço legado nem inclui tokens; privadas exigem auth além de noindex.
**Evidência:** `specs/018-landing-widget-e-jornada/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

### T018-06

**Requisitos/casos:** R018-01, R018-02, R018-03, R018-04, R018-05 → C018-01, C018-02, C018-03, C018-04, C018-05.
**Pré-requisitos locais:** T018-04, T018-05. **Pendências externas diretas:** nenhuma adicional; respeitar dependências da spec.
**Execução:** local_after_dependencies.

Executar jornadas sem IA e assistidas no mobile/desktop com falhas dos serviços independentes.

**Verificação:** Canal humano, retorno login e checkout continuam corretos; evidência visual e assertions do backend separados.
**Evidência:** `specs/018-landing-widget-e-jornada/verification.md`: diff/SHA, comando, ambiente, caso, esperado/obtido e anexos sanitizados. Teste ainda não executado não recebe `passed`.

## Sequência de verificação

1. Ler spec/plan/tasks/verification, este recorte e contratos referenciados; resolver esclarecimentos materiais e atualizar data-model/contrato quando o serviço real exigir.
2. Implementar teste negativo pertinente antes do efeito; separar mocks locais, integração sandbox e modelo real.
3. Rodar lint/build/tipos do código tocado e teste específico disponível. Os novos caminhos de testes acima são propostos; não alegar comando disponível antes de adicioná-lo ao repo.
4. Consultar `../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md` para comandos existentes e restrições. Não rodar eval legado em lote: há chamadas pagas e expectativas antigas.
5. Comparar critério de aceite de cada R/C em spec.md e verification.md, executar convergência e registrar pendências. Só então atualizar tasks/status/matriz e pointer.

## Reversão do recorte

Reverter somente o diff identificado desta entrega; preservar alterações concorrentes e recibos/dados. Migrações devem ser compatíveis e restauráveis. Desligar a capacidade afetada mantendo checkout, ajuda estática e atendimento; não restaurar o agente Pilates. Nenhum rollback/deploy remoto está autorizado por este documento.
