# 013 — Fundação, governança e contratos da Taliya

**Status:** recorte local definido; integrações dependentes bloqueadas.
**Responsável:** Liderança técnica + responsável pelo produto.
**Dependências:** nenhuma.

## Abordagem técnica
Registrar o estado real, retirar conflitos de autoridade e fixar as interfaces existentes. Reutilizar app/Auth e especificar billing Asaas a construir, conforme `../../docs/taliya-sdd/DECISAO_BILLING_2026-09-29.md`.

A abordagem de domínio e as interfaces propostas estão em `../../docs/taliya-sdd/03_ARQUITETURA_E_CONTRATOS.md`. A implementação deve referenciar as interfaces reais descobertas na 013; os caminhos abaixo pertencem ao ZIP inspecionado e são candidatos de integração, não prova da árvore atual.

## Pontos de integração observados
- `AGENTS.md`
- `.specify/memory/constitution.md`
- `.specify/feature.json`
- `.specify/init-options.json`
- `next.config.ts`
- `docs/landing-migration/decisions.md`

## Ordem de execução
1. Gerar inventário e matriz de autoridade a partir do commit atual; resolver rotas Internal locais/remotas.
2. Registrar contratos existentes de conta/negócio/acesso e contratos-alvo de oferta, checkout, assinatura e webhooks; separar observação de código de API futura.
3. Aplicar o adendo scoped de AGENTS/constituição; arquivar regras antigas sem excluí-las.
4. Verificar Spec Kit instalado, scripts ps/sh/py e disponibilidade de converge; fixar versão e registrar comandos corretos.
5. Salvar baselines de desktop/mobile e mapa de dependências materiais/contas/políticas; não ativar serviços pagos.
6. Revisar checklist de requisitos, plan/tasks e registrar evidências sanitizadas antes de liberar a 014/015.

## Dados, permissões e observabilidade
Cada mudança de estado material deve ter ator, autorização, recibo persistido e evento de domínio. Fronteiras entre bancos/serviços usam outbox e reconciliação, não uma transação distribuída presumida. Métricas públicas de browser não comprovam dinheiro ou acesso. Não registrar segredos ou dados de terceiros em prompts/analytics.

## Testes e rollback
Executar os casos `C013-01` a `C013-05` e a regressão dos contratos afetados. Usar feature flag da capacidade e migrações compatíveis para rollback; nenhuma volta ao roteiro Pilates. Registrar em `verification.md`.

## Esforço de referência
1–2 dias de engenharia focada, estimativa de planejamento, não prazo garantido. Não inclui espera por autorização, fornecimento de mídia ou acesso externo. Reestimar ao fechar 013.

## Plano técnico refinado a partir do repositório real
Base: landing 862095261a617a4a1a73c1ab96a914a9249c63ec, working tree de SEO preservada.
Stack existente Next 16.2.9/React 19.2.4/Python >=3.12/Postgres; não atualizar dependências de runtime na 013.

| Tarefa | Caminhos e interface | Teste/erro/limite |
|---|---|---|
| T013-01 | evidence/repository-before.json, contracts/current-contracts.md; Next routes e Internal 7cbe9e9 | SHAs e HTTP sem autenticação; 401 não prova sessão autorizada |
| T013-02 | contracts/current-contracts.md; Copiloto d99ef897; contrato-alvo em DECISAO_BILLING_2026-09-29.md | Comprovar ausência de billing e mapeamento de integração; endpoints futuros não são publicados |
| T013-03 | AGENTS.md, constitution.md, feature.json, EXECUTION_ADDENDUM.md | Verificar pointer e preservação dos arquivos da aplicação por SHA |
| T013-04 | .specify/scripts/bash/*.sh e PROVENANCE.json | CLI 1.0.7, paths-only, setup-plan não destrutivo e prerequisites; PowerShell ausente |
| T013-05 | evidence/baseline-*.png, visual-baseline.json, environments.md | Desktop 1440x1000/mobile 390x844; sem requests externos do browser; mídia sem aprovação não entra em catálogo |
| T013-06 | scripts/validate_plan.py e validate_progress.py, tests/test_validate_progress.py; status/matriz/verification/handoff | Snapshot inicial separado; testes negativos de falso done/dependência/evidência; nenhuma prova de runtime inferida |

Caminhos relativos de evidence/contracts referem-se a docs/taliya-sdd, salvo os artefatos da spec.
Não há migrações ou mudança de payload de aplicação nesta entrega. Tool nova só de validação SDD offline.
Plano → checklist → tarefas → análise precedem adaptação do validador. Dependências não resolvidas ficam abertas.
Não executar banco local existente: pode servir outra sessão. Não usar `npm run eval:*` sem inspecionar custo/remoto.
Constitution check: adendo explicitamente autorizado; preservação visual, nenhum deploy e nenhum billing paralelo.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
