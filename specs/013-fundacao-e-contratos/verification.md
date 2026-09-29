# 013 — Verificação da entrega local / 2026-09-29

Estado: PARCIAL. G0 bloqueado. Não liberar 014/015. Nenhum produto marcado 100%.
Em 29/09, T013-02 e T013-07 fecharam seu recorte documental local: fonte dos
preços identificada, correção do usuário registrada, contrato-alvo Asaas separado
dos contratos observados de Auth/negócio/acesso. `validate_progress.py` e
`check_readiness.py --spec 013` passaram como consistência de artefatos;
`git diff --check` passou. C013-01/C013-03 continuam parciais porque Internal
e integração externa não foram homologados. Não houve teste de billing.
Correção do usuário em 2026-09-29: não existe pagamento/Asaas. As seções históricas
abaixo que solicitam fonte de billing publicado foram supersedidas por
`../../docs/taliya-sdd/DECISAO_BILLING_2026-09-29.md`. Billing será implementado
na 015, após 014; esta 013 somente estabelece estado e contrato-alvo.
Baseline: landing 862095261a617a4a1a73c1ab96a914a9249c63ec + working tree preservada;
branch criada pelo hook 015-fundacao-e-contratos; spec resolvida por pointer 013.
Responsável pela execução/revisão: Codex principal. Aceite humano/integrado pendente.

| Caso | Resultado | Evidência e limite |
|---|---|---|
| C013-01 / R013-01 | PARCIAL | contracts/current-contracts.md, repository-sources.json, internal-routing.json e decisão billing de 29/09; billing ausente agora confirmado, SHA/donos do Internal seguem pendentes |
| C013-02 / R013-02 | PASSOU LOCAL | Diff AGENTS/constituição/adendo + pointer/prerequisites; legado preservado e escopo limitado |
| C013-03 / R013-03 | PARCIAL | App/Auth/acesso localizados; usuário confirmou que billing não existe. Contrato-alvo e fonte documentada de valores registrados; confirmação comercial e convergência da 015 pendentes. Nenhuma rota futura alegada como publicada. |
| C013-04 / R013-04 | PASSOU LOCAL | specify version 1.0.7; integration status WARNING por managed files customizados; Bash oficial executado e hashes salvos |
| C013-05 / R013-05 | PASSOU INVENTÁRIO LOCAL | Baselines desktop/mobile atuais, mídia sem aprovação, permissões/ambientes/bloqueios registrados; dependência ausente não impediu tarefas locais |

## Comandos efetivamente executados e resultados

- `specify version`: 1.0.7. Integração declarada 0.8.3.dev0; pwsh não instalado.
- `specify integration status`: WARNING, 5 managed files já modificados antes da entrega;
  0 faltantes. Sem init/upgrade/force.
- `specify artifact list --json` e `specify artifact info command:speckit.converge --json`:
  converge existe no core_pack 1.0.7, mas não na lista de skills instalada. Instrução
  oficial foi lida; revisão de lacunas produziu T013-07/08/09, append-only.
- Hook Git Bash: criou 015-fundacao-e-contratos. IDs 013–025 livres em specs;
  branch diferente não muda IDs, conforme speckit-specify instalado.
- `bash .specify/scripts/bash/check-prerequisites.sh --json --paths-only`:
  FEATURE_DIR=specs/013-fundacao-e-contratos. Campo BRANCH sintetizado pelo script
  é 013-fundacao-e-contratos; Git real é 015-fundacao-e-contratos.
- `bash .specify/scripts/bash/setup-plan.sh --json`: plano existente preservado.
- `bash .specify/scripts/bash/check-prerequisites.sh --json --require-spec --require-tasks --include-tasks`: passou.
- ZIP: 94 entradas de manifesto verificadas; validador original em extração
  temporária: 87 checks, planning_integrity_only. Não é runtime.
- Capturas locais via Playwright/Chrome instalado: 1440x1000 e 390x844; /pilates→/,
  200, sem overflow/falhas locais; requests externos bloqueados. Primeiro browser
  bundled ausente; recuperado com Chrome existente, sem instalar dependências.
- HTTP GET sem auth: Internal local/remoto 401; Sales Inbox local 200 não configurado.
- GitHub read-only: três deploys recentes Internal para SHA 7cbe9e9 em failure.
  Fonte remota encontrada não comprova código ativo em produção.

Resultados dos testes do validador e da preservação ficam em evidence/local-validation.json.
Os testes da aplicação não foram executados: nenhum arquivo de runtime foi alterado.
Não foram executados login staff, banco, migração, webhook, compra, envio humano,
PostHog, inferência Agents API ou E2E externo. Não há budget/ambiente autorizado para eles.

## Convergência

Cinco requisitos revistos: três com evidência local suficiente ao recorte, dois
parciais/bloqueados. Nenhuma lacuna autoriza reconstrução ou inventar endpoint.
T013-07 especializa o contrato-alvo do novo billing e está concluída localmente;
T013-08 cobre implantação/staff e T013-09 a homologação. T013-01/06 permanecem
abertas; T013-02/03/04/05 concluídas localmente.
Veja ../../docs/taliya-sdd/environments.md para B013-01–04 e donos necessários.

## Próxima tarefa exata

T013-08/T013-01: confirmar o deployment ativo, SHA, dono e identidade staff do
Internal; depois T013-09 homologa a fundação em ambiente autorizado. Vigência
comercial dos preços e habilitação Asaas são gate da 015. Nenhuma spec dependente
iniciada.

## Rechecagem histórica de localização do billing — 2026-09-28

Busca somente leitura na landing ativa (`app`, `lib`, `services`, `data`), no checkout
Copiloto e nas branches remotas listadas não localizou handler de billing Asaas. Foi
encontrada uma cópia sem `.git` com spec 003 e contrato textual antigo. Ausência dos
paths nela e placeholder na URL do exemplo impedem aceitar esse material como serviço
publicado. A spec declara garantia de 30 dias e oferta anual condicionada, diferentes das decisões atuais.
O código ativo também tem strings de 14 dias grátis e de 30 dias de garantia; isso
confirma divergência de implementação, não altera a oferta comercial autoritativa.

Evidência: `../../docs/taliya-sdd/evidence/billing-source-search.json`; SHA e limite
da busca registrados ali. Resultado atual: B013-01 aberto; aguarda localização do
serviço real ou referência verificável de deployment, sob a premissa antiga agora
refutada pelo usuário. Sem credenciais, requests,
operações financeiras ou alteração de produto nesta tarefa.

## Movimento concorrente observado
Durante a sessão, outro processo voltou o checkout para `main` e criou o commit
`b09c4d39d0151822ab1a43f95edd68b9d4730df2` (SEO), também observado em origin/main.
Esta execução não fez esse commit nem push. A branch criada pelo hook permaneceu
em 8620952. Hashes da aplicação iguais ao snapshot inicial comprovam preservação;
não trocar branch para desfazer trabalho concorrente. Pointer 013 continua ativo.

Capturas foram atualizadas após esperar 4 s pela animação inicial. Primeira dobra
desktop/mobile foi inspecionada visualmente. Na recaptura, Chrome encerrou mas Node
ficou pendente na limpeza e foi terminado após salvar imagens; métricas JSON vêm
da primeira captura concluída, com os mesmos hashes de aplicação.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).

### Evidência da preparação solicitada

`../../docs/taliya-sdd/evidence/preparation-validation.json`: 81 tarefas detalhadas,
65 requisitos/casos cobertos, 23 testes locais dos validadores aprovados, 87 checks
do snapshot inicial, validadores de progresso/preparação aprovados. O comando
`check_readiness.py --spec 014 --require-unblocked` retornou exit 2 corretamente.
359 arquivos de aplicação comparados ao baseline inicial, zero mudanças.

Não executados: build/lint da aplicação (código não alterado), testes funcionais
propostos, migrações e homologação real. Nenhum caso C013 bloqueado foi promovido a
passed. T013-06 recebeu preparação adicional, mas permanece parcial até G0.
Snapshot: `../../docs/taliya-sdd/evidence/preparation-snapshot.json`.
