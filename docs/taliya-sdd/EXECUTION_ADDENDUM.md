# Autoridade e plano do recorte local 013

Ratificação: pedido do usuário em 28/09/2026, corrigido em 29/09/2026. Escopo:
integração do produto existente e construção do billing Asaas ainda inexistente,
sem redesign ou reconstrução de app/autenticação. A mudança e os contratos-alvo
estão em `DECISAO_BILLING_2026-09-29.md`. Este arquivo registra
decisões; a continuidade única permanece em `docs/conversation-handoff-2026-05-14.md`.

## Divergências registradas antes da alteração

| Observado | Autoridade atual e tratamento |
|---|---|
| AGENTS/constituição/pointer restringem à migração 001/copy-only | Adendo limitado em AGENTS e constituição; pointer para 013. Histórico preservado. |
| Specs de diretório 001–012, branches históricas 013/014, apenas 001 no namespace taliya-migration | Diretórios 013–025 livres; IDs mantidos. Hook Git criou 015-fundacao-e-contratos. Branch e spec são independentes no Spec Kit. |
| `/pilates` já redireciona para `/`; SEO tem alterações locais | Preservar código atual e snapshot, não restaurar rotas antigas pelo documento legado. |
| Código atual mantém diagnóstico/Pilates, pós-processamento de leads e token Internal | Constatar contratos; correções pertencem a 014/016/017/020, depois dos gates. |
| Copiloto encontrado ainda contém entitlement de trial no onboarding | Não converter em oferta aprovada. O usuário esclareceu em 29/09 que billing/Asaas não existe; construir no programa, preservando Auth e negócio. |
| Internal remoto tem fonte própria e contrato v2 | Não aplicar achados do Sales Inbox local como correções automáticas do remoto. |
| CLI 1.0.7, integração 0.8.3.dev0, PowerShell ausente | Adicionar scripts Bash oficiais da instalação 1.0.7, sem substituir scripts/templates/manifests antigos. |

## Implementação delimitada antes de alterar runtime

1. Incorporar o pacote em `docs/taliya-sdd/`, specs em `specs/013-*`…`025-*`.
   Guardar ZIP original, manifesto e resultado inicial separado; corrigir referências relativas.
2. Atualizar apenas AGENTS, constituição e ponteiro; adicionar scripts Bash com hashes de origem.
3. Completar spec/plan/tasks/checklist/analysis/contracts com caminhos realmente inspecionados.
4. Registrar fontes por SHA, contratos, limitações, ambientes, mídia e baselines desktop/mobile.
5. Separar `validate_plan.py` (snapshot) de validação de progresso; testar recusas de conclusão sem evidência.
6. Atualizar status, matriz e continuidade. Não liberar 014/015 se a fundação continuar parcial.

Interfaces alteradas nesta entrega: somente ferramentas locais de resolução/validação SDD.
Migrações: nenhuma. APIs, dependências de aplicação, UI e segredos: nenhuma mudança.
Responsável pelos arquivos compartilhados nesta sessão: Codex principal, sem delegação.

## Esclarecimentos

Modelo/esforço, cinco tools, contratação direta, Asaas, mensal/anual, cartão/Pix
Automático, garantia de 14 dias e catálogo real estão decididos pelo usuário.
Billing publicado não existe; conta/ambiente Asaas, elegibilidade Pix Automático,
implantação autoritativa do Internal e responsáveis operacionais nomeados permanecem
dependências concretas. Valores estão documentados e a confirmação dos vigentes foi
solicitada antes de ativar cobrança; nenhuma URL ou estado financeiro é inferido.
Credenciais devem vir do mecanismo seguro; nenhum segredo em artefato ou pergunta.

## Invocações reais

- `specify version`, `specify integration status`, `specify artifact list --json`.
- Hook existente: `bash .specify/extensions/git/scripts/bash/create-new-feature.sh --json --short-name fundacao-e-contratos 'Fundação Taliya SDD: contratos e governança'`.
- `bash .specify/scripts/bash/check-prerequisites.sh --json --paths-only`.
- `bash .specify/scripts/bash/setup-plan.sh --json` (não sobrescreve plano existente).
- `bash .specify/scripts/bash/check-prerequisites.sh --json --require-spec --require-tasks --include-tasks`.
- Skills presentes: `$speckit-specify`, `$speckit-clarify`, `$speckit-plan`,
  `$speckit-checklist`, `$speckit-tasks`, `$speckit-analyze`, `$speckit-implement`.
  São instruções de chat lidas e aplicadas com equivalentes Bash; não comandos de shell executados.
- O CLI 1.0.7 expõe `speckit.converge`, mas a skill não está instalada. O comando oficial do core_pack foi lido; revisão fica em
  `specs/013-fundacao-e-contratos/analysis.md` e `verification.md`.
- Hooks de commit estão configurados como opcionais no YAML e foram dispensados nesta execução; não incluir alterações locais do usuário em commit automático. Não foram globalmente desativados.

## Rollback

Reverter somente o diff desta entrega e restaurar o pointer registrado em
`evidence/repository-before.json`/ZIP. Não executar reset sobre a working tree.
Não existe mudança de runtime nesta entrega nem fallback para Pilates.

## Movimento concorrente observado
Durante a sessão, outro processo voltou o checkout para `main` e criou o commit
`b09c4d39d0151822ab1a43f95edd68b9d4730df2` (SEO), também observado em origin/main.
Esta execução não fez esse commit nem push. A branch criada pelo hook permaneceu
em 8620952. Hashes da aplicação iguais ao snapshot inicial comprovam preservação;
não trocar branch para desfazer trabalho concorrente. Pointer 013 continua ativo.
