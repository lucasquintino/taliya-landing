# 013 — Fundação, governança e contratos da Taliya

**Status:** recorte local entregue; aceite integrado bloqueado.
**Responsável:** Liderança técnica + responsável pelo produto.
**Dependências:** nenhuma.

## Tarefas
- [ ] **T013-01** — Gerar inventário e matriz de autoridade a partir do commit atual; resolver rotas Internal locais/remotas. Requisitos: R013-01. Recorte: [execution.md#t013-01](execution.md#t013-01).
- [x] **T013-02** — Registrar contratos existentes de conta/negócio/acesso e contratos-alvo de oferta, checkout, assinatura e webhooks Asaas. Requisitos: R013-01, R013-03. Recorte: [execution.md#t013-02](execution.md#t013-02).
- [x] **T013-03** — Aplicar o adendo scoped de AGENTS/constituição; arquivar regras antigas sem excluí-las. Requisitos: R013-02. Recorte: [execution.md#t013-03](execution.md#t013-03).
- [x] **T013-04** — Verificar Spec Kit instalado, scripts ps/sh/py e disponibilidade de converge; fixar versão e registrar comandos corretos. Requisitos: R013-04. Recorte: [execution.md#t013-04](execution.md#t013-04).
- [x] **T013-05** — Salvar baselines de desktop/mobile e mapa de dependências materiais/contas/políticas; não ativar serviços pagos. Requisitos: R013-05. Recorte: [execution.md#t013-05](execution.md#t013-05).
- [ ] **T013-06** — Revisar checklist de requisitos, plan/tasks e registrar evidências sanitizadas antes de liberar a 014/015. Requisitos: R013-01, R013-02, R013-03, R013-04, R013-05. Recorte: [execution.md#t013-06](execution.md#t013-06).

Não marcar uma tarefa porque o arquivo existe. Acrescentar caminho do diff, comando e resultado verificável ao concluí-la. Se o código atual já atende, comprovar por teste e registrar reuso em vez de reimplementar.

## Detalhamento executado
- T013-01 parcial: repository-before/repository-sources, contratos e roteamento HTTP; falta SHA ativo e responsáveis.
- T013-02 concluída para o recorte documental local: Auth/membership/acesso do Copiloto e contrato-alvo de billing separados explicitamente. Homologação de pagamento pertence à 015.
- T013-03 concluída localmente: AGENTS/constitution/feature.json/EXECUTION_ADDENDUM; arquivos de aplicação preservados por hash.
- T013-04 concluída: CLI 1.0.7, Bash vendorizado, paths-only/setup-plan/prerequisites executados; manifests antigos preservados.
- T013-05 concluída para inventário: capturas desktop/mobile, mídia com approval not_verified, ambientes/permissões/bloqueios explícitos. Não é aceite humano nem integração.
- T013-06 parcial: análise/checklist/validação/handoff entregues; não liberar 014/015 antes do aceite integrado.

## Phase 1: Convergence
As lacunas abaixo especializam trabalho remanescente; não substituem os IDs originais.
- [x] **T013-07** — Registrar a correção de escopo, fonte dos valores documentados e contrato-alvo do novo billing Asaas, sem declarar API futura como publicada. Requisitos: R013-01, R013-03. (concluída localmente; HIGH) Recorte: [execution.md#t013-07](execution.md#t013-07).
- [ ] **T013-08** — Confirmar SHA da implantação Internal ativa, dono operacional e identidade staff real. Requisitos: R013-01. (partial; B013-02/B013-03; HIGH) Recorte: [execution.md#t013-08](execution.md#t013-08).
- [ ] **T013-09** — Homologar contratos externos no ambiente autorizado e fechar os cinco casos antes de liberar dependências. Requisitos: R013-01, R013-03, R013-05. (partial; B013-02/B013-03; HIGH) Recorte: [execution.md#t013-09](execution.md#t013-09).

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
