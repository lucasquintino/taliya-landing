# Checkpoint ativo — Taliya SDD / fundação 013 — 2026-09-28

Este é o único arquivo de continuidade da integração. A seção de maio abaixo é histórica.

## Checkpoint mais recente — correção billing e fundação — 2026-09-29

- **Estado real informado pelo usuário:** ainda não existe pagamento nem Asaas. A premissa anterior de billing pronto está superada; app/Auth existentes continuam como base. A 015 agora inclui construir oferta, cartão recorrente, Pix Automático, webhooks, projeção de acesso, gestão e testes. Não foi criado serviço, endpoint, migração ou cobrança nesta entrega.
- **Fonte comercial localizada:** `data/landing/niches/pilates.ts` e contrato aprovado do app trazem R$ 59,90/mês e R$ 599/ano. O usuário confirmou que os valores estão documentados; a vigência comercial exata para ativar oferta ainda precisa ser ratificada. Strings de trial sem cartão e garantia de 30 dias são legado divergente. Decisão vigente: cobrar na contratação e garantia de 14 dias.
- **Recorte local fechado:** T013-02 e T013-07 concluídas como mapeamento e contrato-alvo, com evidência em `specs/013-fundacao-e-contratos/verification.md`, `docs/taliya-sdd/contracts/current-contracts.md` e `docs/taliya-sdd/DECISAO_BILLING_2026-09-29.md`. T013-03/04/05 já estavam concluídas localmente. T013-01/06/08/09 continuam abertas; 013 é a única spec ativa, G0 bloqueado.
- **Artefatos consistentes:** 13 specs, 87 tarefas, 68 requisitos e 68 casos. Asaas passou a ser implementação da 015 após a 014; 024 homologa o resultado da 015. `validate_progress.py`, `check_readiness.py --spec 013` e `check_readiness.py --spec 024` passaram como checagens estruturais; 23 testes unitários dos validadores e `git diff --check` passaram após a correção das fixtures. Não equivalem a testes de produto.
- **Checkout de trabalho:** landing `/Users/lucasquintino/Projects/taliya-copiloto-landing`, branch de snapshot `codex/taliya-sdd-local-snapshot-20260929`, criada de `main` no SHA `b09c4d39d0151822ab1a43f95edd68b9d4730df2`. O commit desta branch contém o diff SDD e as demais alterações locais não ignoradas solicitadas para envio ao GitHub; verificar o SHA atual com `git rev-parse HEAD`. App `/Users/lucasquintino/Downloads/copiloto-github`, branch `codex/e02-icloud-recovery-20260928`, SHA `d99ef897f3033ace6a23ee009e2578ffc04a259d`, com alterações E02 alheias preservadas. Nenhum código de runtime foi alterado pela correção documental de billing.
- **Mudança concorrente preservada:** durante a validação final, apareceu diff de 2 linhas em `components/landing/NicheLandingPage.tsx` ajustando a espera da animação de entrada. Esta execução não editou esse arquivo nem atribui o diff à fundação; reavaliar o working tree antes de mexer na landing.
- **Envio ao GitHub solicitado em 29/09:** snapshot completo dos arquivos locais não ignorados em branch separada, preservando `main`; o arquivo importado `evidence/CODIGO_VERIFICADO.md` teve apenas espaços finais removidos para `git diff --check`, com o ZIP original intacto em `docs/taliya-sdd/source/`. `npm run lint` passou com 6 warnings e `npm run build` passou; os 23 testes dos validadores passaram. Este envio não comprova G0–G6 nem ativa implantação ou billing.
- **Bloqueios reais:** B013-02 (deployment/SHA e identidade staff do Internal), B013-03 (ambiente sintético, canais, permissões e orçamento de homologação); B013-01 agora bloqueia ativação/homologação da 015 (conta Asaas sandbox, elegibilidade Pix Automático, credenciais seguras, URLs e preço vigente). Materiais B013-04 continuam pendentes para 019.
- **Próxima tarefa exata:** T013-08/T013-01: obter evidência do Internal efetivamente servido e identidade staff autorizada; em paralelo, concluir apenas documentação local de dependência/contrato ainda cabível, sem mudar spec ativa. Depois T013-09 no ambiente explicitamente autorizado, fechar G0, ativar 014 e então implementar 015. Não refazer a busca por um serviço de billing publicado: o usuário confirmou sua inexistência.

---

## Atualização mais recente — localização do serviço de billing — 2026-09-28

Meta ativa: implementar specs 013–025, uma spec por vez. A rechecagem atual pesquisou
a árvore de código da landing ativa e do app Copiloto, branches GitHub acessíveis e
uma cópia adicional de landing. Não foi encontrada a implementação/deployment de
billing Asaas. A cópia adicional não tem `.git` e contém apenas spec/contrato antigo
com URL placeholder, garantia de 30 dias e anual condicionado. Não é fonte autoritativa.

O código ativo ainda contém CTA de 14 dias grátis e conteúdo de garantia de 30 dias;
divergência a corrigir na etapa da landing depois de conectar a oferta verdadeira.
Nenhum código do produto foi alterado nesta rechecagem.

- Evidência de pesquisa: `docs/taliya-sdd/evidence/billing-source-search.json`.
- Mapa contratual e limitações: `docs/taliya-sdd/contracts/current-contracts.md`;
  critérios T013-07 em `specs/013-fundacao-e-contratos/verification.md`.
- Progresso mantém G0 bloqueado; T013-01/02/07 permanecem parciais/bloqueadas.
  014–025 não foram ativadas. Próximo passo para avançar T013-07: apontar o repo,
  diretório ou documento da implementação publicada de billing, sem compartilhar segredo.
- Verificação após atualizar artefatos: execute
  `python3 docs/taliya-sdd/scripts/validate_progress.py`,
  `python3 docs/taliya-sdd/scripts/check_readiness.py` e `git diff --check`.

## Preparação anterior — tarefas prontas para execução condicional

Pedido: deixar tudo preparado para implementar as tarefas. Fonte atual confirmada:
`main` em `b09c4d39d0151822ab1a43f95edd68b9d4730df2`; o trabalho continua como diff
local, sem commit/push/deploy desta execução. Apenas 013 ativa; G0 bloqueado.

- Entrada de execução: `docs/taliya-sdd/IMPLEMENTATION_READINESS.md`.
- 81 tarefas / 65 requisitos-casos / 13 specs detalhados em `specs/013-*`…`025-*/execution.md`:
  fontes reais, caminhos propostos, interfaces, migrações, erros, dependências, testes
  esperados e evidências. `spec/plan/tasks/verification` apontam aos recortes; checklists
  distinguem preparação de aceite. `planning/execution.json` indexa a preparação.
- Novo `check_readiness.py` verifica cobertura, dependências e bloqueios sem executar
  tarefas ou alterar pointer. Não é suíte de runtime nem autorização automática.
- Resultado: `evidence/preparation-validation.json`: 23 testes offline aprovados,
  snapshot original 87 checks, progresso/preparação consistentes, `git diff --check`
  aprovado. `--spec 014 --require-unblocked` retornou 2 como esperado: 013 incompleta.
  359 arquivos de aplicação comparados ao baseline, zero alterações.
- Snapshot desta preparação: `docs/taliya-sdd/evidence/preparation-snapshot.json`.
  `delivery-snapshot.json` anterior permanece como evidência histórica, não foi reescrito.
- Comandos adicionais: `python3 docs/taliya-sdd/scripts/check_readiness.py` e
  `python3 docs/taliya-sdd/scripts/check_readiness.py --spec 014 --require-unblocked`.
  Comandos anteriores abaixo continuam válidos. Hooks de commit são opcionais e
  foram dispensados; não estão globalmente desativados no YAML.

**Próxima tarefa exata continua T013-07**, receber localização da fonte do billing
publicado, ler instruções e registrar contratos reais conforme
`docs/taliya-sdd/contracts/integration-handoff.md`. Depois T013-08 (deployment/staff
Internal), T013-09 (homologação autorizada) e T013-06 (convergência/G0).
Billing, deployment, ambiente/orçamento e mídia aprovada não foram fornecidos por
esta preparação. Não refazer auditoria geral nem reconstruir app/billing.

Não executados nesta preparação: build/lint de aplicação (nenhuma mudança de aplicação),
suíte funcional nova, banco/migrações, integração remota, inferência Luna/max,
PostHog, envios de canal, billing real ou deploy. Preparação técnica não comprova
essas integrações; contratos específicos pendentes devem ser ratificados antes do código.

## Onde retomar

- Repositório: `/Users/lucasquintino/Projects/taliya-copiloto-landing`.
- SHA inicial: `862095261a617a4a1a73c1ab96a914a9249c63ec`, branch main, 8 alterações de SEO.
- SHA observado ao fechar: `b09c4d39d0151822ab1a43f95edd68b9d4730df2`, branch main.
  Outro processo commitou o SEO e voltou à main durante a execução; não revertido.
- Hook Spec Kit criou `015-fundacao-e-contratos` em 8620952; não usar a branch como
  número da spec. `.specify/feature.json` seleciona `specs/013-fundacao-e-contratos`.
- Entrega desta sessão é diff local, sem commit/push/deploy pela sessão.
- Snapshot de 2822 arquivos antes: `docs/taliya-sdd/evidence/repository-before.json`.
  Snapshot final do recorte: `docs/taliya-sdd/evidence/delivery-snapshot.json`.

## Entregue

- T013-03: adendo limitado de autoridade em AGENTS/constituição e pointer atualizado.
- T013-04: CLI 1.0.7 constatado; Bash oficial adicionado com hashes, sem reinit;
  PowerShell histórico preservado. Scripts de resolução/plano/prerequisites executados.
- T013-05: inventários de mídia, fontes, ambientes e baselines desktop/mobile atuais.
- T013-01/02 parcialmente executadas: contratos de landing/Python/Internal/Copiloto
  mapeados por SHA; HTTP sem auth e estado dos deploys registrados.
- T013-06 parcialmente executada: spec/plan/tasks/checklist/análise, validação de
  progresso, snapshot original, matriz/status/verificação reconciliados.
- 013–025 incorporadas sem sobrescrever specs anteriores. Cinco tools e Luna/max/none
  mantidos como intenção; runtime antigo não foi habilitado como fallback.

## Comandos e resultados

```sh
specify version
specify integration status
specify artifact list --json
bash .specify/scripts/bash/check-prerequisites.sh --json --paths-only
bash .specify/scripts/bash/setup-plan.sh --json
bash .specify/scripts/bash/check-prerequisites.sh --json --require-spec --require-tasks --include-tasks
python3 docs/taliya-sdd/scripts/validate_plan.py
python3 docs/taliya-sdd/scripts/validate_progress.py
python3 -m unittest discover -s docs/taliya-sdd/tests -v
git diff --check
```

CLI 1.0.7; integração 0.8.3.dev0 com 5 arquivos previamente customizados (WARNING).
94 hashes do pacote verificados; snapshot: 87 checks. Progresso: consistente.
12 testes isolados do validador aprovados. Baselines /pilates→/ com 200 desktop/mobile,
sem overflow/falhas locais e sem requests externos permitidos. Nada disso é QA integrada.

## Bloqueios e próxima tarefa exata

**T013-07/T013-02 — localizar o serviço publicado Asaas/assinatura**: usuário foi
perguntado pela fonte (repo, diretório ou documentação), sem solicitar credenciais.
Ao receber: ler instruções da fonte, registrar SHA e contratos de oferta, checkout,
identidade/vínculo, assinatura/acesso, eventos, idempotência, estados/erros e donos.
App/billing continuam considerados prontos conforme usuário; não reconstruir.

T013-08: confirmar SHA ativo e identidade de staff do Internal. Fonte main 7cbe9e9
localizada, mas três deployments mais recentes em failure e público retorna 401.
T013-09: executar homologação somente com ambiente e orçamento autorizados.
G0 bloqueado; G1–G6 não executados. Não iniciar 014/015 enquanto dependências não fecharem.

Não executados: inferência paga, testes remotos de billing, compra/reembolso, login de
staff, escrita em bancos, mensagens humanas, PostHog, publicação ou build nativo.

## Arquivos e evidências

- `AGENTS.md`, `.specify/memory/constitution.md`, `.specify/feature.json`, Bash oficial.
- `specs/README.md`, `specs/013-*`…`025-*` (só 013 executada).
- `docs/taliya-sdd/`: pacote incorporado, original em source/, contratos/ambientes,
  scripts/testes/evidências/status/matriz; o manifesto original verifica o ZIP.
- `specs/013-fundacao-e-contratos/verification.md`: critérios, resultados e limites.
- `docs/taliya-sdd/contracts/current-contracts.md`: interfaces e fontes reais.

## Histórico anterior preservado — não seguir como direção atual

# Handoff para nova conversa Codex - Taliya Landing + Agente

Data do handoff: 2026-05-14  
Repo: `C:\Users\lucas\agentes-landing-system`  
Branch atual de produção: `master`  
Último commit enviado: `f258be6 Fix diagnostic widget entry flow`

## Como retomar sem começar do zero

Na nova conversa, começar lendo nesta ordem:

1. `AGENTS.md`
2. `docs/conversation-handoff-2026-05-14.md`
3. `specs/002-floating-ai-sales-agent/spec.md`
4. `specs/002-floating-ai-sales-agent/plan.md`
5. `specs/002-floating-ai-sales-agent/tasks.md`
6. `specs/001-niche-landing-system/spec.md`
7. `docs/taliya-agent-flow-test-scenarios.md`
8. `docs/taliya-agent-flow-validation-matrix.md`
9. `docs/taliya-agent-flow-deep-map.md`
10. `docs/landing-agentes-pilates/source/README.md`

Regra mais importante: a frente visual/layout da `/pilates` está aprovada. Não redesenhar a landing. Mudanças futuras nela devem ser apenas integração, CTA, schema, tracking, acessibilidade, bugs responsivos ou wiring do agente.

## Estado atual em produção

Domínio e deploy:

- `taliya.com.br` está apontado para Vercel.
- Cloudflare está no meio como DNS/proxy.
- Vercel validou `taliya.com.br` e `www.taliya.com.br`.
- Deploy recente publicado a partir do commit `f258be6`.

Agente/widget:

- O widget flutuante existe na landing `/pilates`.
- Desktop deve mostrar o widget em modo pill completo.
- Mobile deve mostrar somente o ícone/mensagem compacto.
- Chat abre com botão de fechar.
- O agente usa OpenAI quando `OPENAI_API_KEY` está configurada.
- A chave antiga vazou em conversa e já foi trocada pelo usuário.
- O fluxo determinístico de diagnóstico CRM/agentes existe em `lib/landing/ai-attendant/crm-diagnostic.ts`.
- O diagnóstico gratuito virou o funil principal do agente.

Lead pipeline:

- Existe n8n Cloud em `taliyan8n.app.n8n.cloud`.
- Workflow existente: `Taliya - Lead Upsert`.
- Webhook usado: `https://taliyan8n.app.n8n.cloud/webhook/taliya/lead-upsert`.
- Airtable base foi criada e integrada via n8n para receber leads.
- Não colocar segredos no repo. Usar Vercel envs.

Última validação feita:

- `npm run lint` passou.
- `npx tsc --noEmit` passou.
- `npm run build` passou.
- Teste local API do diagnóstico passou.
- Teste em produção confirmou que a nova versão já estava ativa.

## Últimas correções feitas

Commit `f258be6 Fix diagnostic widget entry flow`:

- O widget abre com duas mensagens:
  - `Oi. Estou aqui pra te acompanhar e responder duvidas sobre a Taliya.`
  - `Se fizer sentido pra voce, podemos fazer um diagnostico gratuito do seu studio. O que voce acha?`
- Sugestão inicial: `Quero fazer diagnostico gratuito`.
- Se o usuário clicar/escrever algo que remeta a diagnóstico, força `start_crm_diagnostic`.
- Clicar em `Fazer diagnóstico gratuito` na landing envia uma mensagem real ao chat.
- Corrigido bug em que `Quero fazer diagnostico gratuito` virava nome/dor/objetivo do lead.
- Ajustada animação do widget para não sumir depois da primeira cutucada.
- Ajustada sugestão dinâmica para acompanhar melhor a pergunta atual do diagnóstico.

## Arquivos principais do agente

Frontend/widget:

- `components/landing/shared/FloatingAiAttendant.tsx`
- `components/landing/shared/FloatingAiAttendantButton.tsx`
- `components/landing/shared/FloatingAiAttendantPanel.tsx`
- `components/landing/NicheLandingPage.tsx`
- `app/globals.css`

Backend/agente:

- `app/api/landing/ai-attendant/route.ts`
- `app/api/landing/ai-attendant/whatsapp/route.ts`
- `lib/landing/floating-agent.ts`
- `lib/landing/ai-attendant/provider.ts`
- `lib/landing/ai-attendant/crm-diagnostic.ts`
- `lib/landing/ai-attendant/conversion-gates.ts`
- `lib/landing/ai-attendant/sales-cadence.ts`
- `lib/landing/ai-attendant/leads.ts`
- `lib/landing/ai-attendant/n8n.ts`
- `lib/landing/ai-attendant/sales-inbox-store.ts`

Config comercial:

- `data/landing/niches/pilates.ts`
- `data/landing/niches/types.ts`

Página de planos:

- `app/pilates/planos`
- Ainda precisa de uma rodada futura de copy/polish, mas não era a prioridade final desta conversa.

## Decisões de negócio já travadas

Landing:

- A landing `/pilates` não é mais só validação de nicho. Ela vende o SaaS vertical Taliya para studios de Pilates.
- Estratégia principal: não jogar o lead direto em planos caros.
- O caminho preferido é diagnóstico gratuito → recomendação → demo/planos/WhatsApp/assinatura.
- O botão `Falar com consultor`, o widget e o WhatsApp devem alimentar o mesmo funil comercial.

Planos:

- Organização por número de agentes: Base sem agentes, 1 agente, 3 agentes, 7 agentes.
- Plano Base = CRM sem agentes.
- 7 agentes é o plano recomendado/completo, salvo se config mudar.
- Agente sob medida não entra em nenhum plano.
- Over-limit não deixa estourar cota: upgrade ou compra de cota.
- WhatsApp do studio será o próprio WhatsApp do studio.
- O agente vendedor da Taliya usa o WhatsApp próprio da Taliya.
- Sem multi-unidade no começo.
- Sem trial gratuito.
- Cancelamento/reembolso: 30 dias de garantia.
- Setup: self-guided com agente de IA.
- Suporte: 24/7 com agente de IA.
- Implantação: poucos minutos para todos.
- Existe caso especial de piloto privado gratuito para um studio de Pilates, cobrando apenas custo operacional, tratado pessoalmente pelo usuário.

Agente do site:

- Deve conversar como vendedor humano, com cadência.
- Não deve ser agressivo.
- Não deve despejar preço/plano cedo.
- Deve cumprimentar, se apresentar, perguntar com quem fala e conduzir por etapas.
- Função principal agora: oferecer/fazer diagnóstico gratuito.
- Deve responder dúvidas, objeções e caminhos paralelos, mas puxar de volta para diagnóstico quando fizer sentido.
- Deve pedir contato cedo quando houver mínimo interesse.
- Deve registrar lead.
- Deve preservar intenção do usuário: planos, demo, humano, WhatsApp, agente sob medida, preço, objeção etc.

Perguntas do diagnóstico gratuito:

- Nome: `Boa. Antes de eu montar o diagnóstico: com quem eu falo?`
- Contato: pedir WhatsApp ou email para salvar o diagnóstico, permitindo continuar se preferir.
- Tamanho: quantos alunos ativos aproximadamente.
- Dores: pergunta abrangente sobre WhatsApp, agenda/reposições, vendas, financeiro, acompanhamento/gestão.
- Visão do dia: `Hoje você consegue ver facilmente o que precisa ser resolvido no dia?`
- Reposições: se aparecem como dor, perguntar se são fáceis ou viram troca de mensagem.
- Vendas: se aparecem como dor, perguntar se conseguem acompanhar interessado até virar aluno.
- Sistema atual: perguntar se fica em sistema ou WhatsApp/planilha/caderno.
- Objetivo: o que tiraria da mão primeiro este mês.
- Temperatura: se estão buscando resolver agora ou só pesquisando.

Diagnóstico final esperado:

- Identificar dores reais do studio.
- Explicar como o CRM Taliya organiza a operação.
- Explicar quais agentes resolvem aquelas dores.
- Recomendar o plano compatível.
- Só então mostrar CTAs adequados: ver planos, demo guiada quando existir, continuar no WhatsApp/humano, ou assinatura após confirmação clara.

## Pontos pendentes importantes

P0/P1 para próxima conversa:

1. Rodar teste manual completo do widget em produção:
   - abrir pelo widget normal;
   - clicar na sugestão `Quero fazer diagnostico gratuito`;
   - clicar no CTA `Fazer diagnóstico gratuito` antes de abrir chat;
   - abrir chat antes e depois clicar no CTA;
   - confirmar que o roteiro não duplica mensagens nem entra em loop.
2. Validar visual da animação do widget em produção:
   - desktop largo;
   - desktop com DPR 1.25;
   - mobile;
   - confirmar que ele cutuca sem sumir.
3. Calibrar o texto do agente com conversas reais:
   - tom humano;
   - mensagens curtas;
   - sem termos técnicos;
   - sem pressão de venda precoce;
   - resposta direta + gancho para diagnóstico.
4. Validar que lead vai para Airtable/n8n em cenário real:
   - diagnóstico completo;
   - pedido de WhatsApp;
   - pedido de humano;
   - lead quente.
5. Revisar página `/pilates/planos` futuramente:
   - menos poluição;
   - cards vendendo melhor;
   - incluir CRM web, Taliya App, WhatsApp, sistema e 7 agentes;
   - CTAs focados em assinatura e demo;
   - apenas um lugar para voltar ao consultor;
   - seção de agente sob medida igual home.

## Ajustes mapeados pelo usuário antes da migração

Esses pontos foram encontrados em teste real do widget/agente e devem ser tratados na próxima conversa antes de considerar o diagnóstico 100%.

### Widget e animação

- A animação do widget não pode aumentar largura/altura do componente e depois voltar ao tamanho normal.
- A animação deve ser fluida e sutil: pulso, pequeno pulo, badge de notificação ou cutucada visual.
- O widget não pode sumir nem reentrar de forma estranha depois da animação.
- Validar em desktop normal, desktop com DPR 1.25 e mobile.

### Interpretação das respostas do diagnóstico

- O agente repetiu a pergunta `Hoje você consegue ver facilmente o que precisa ser resolvido no dia?` mesmo depois de respostas como:
  - `tenho tudo num caderno anotado`
  - `sim`
  - `nao`
- O agente só avançou quando o usuário clicou na sugestão pronta. Isso está errado.
- O agente deve interpretar respostas livres equivalentes, não depender apenas de sugestões/quick replies.
- Essa regra vale para todas as perguntas do diagnóstico.

Também ocorreu bug na pergunta:

```text
Quais partes mais dão trabalho hoje: WhatsApp, agenda/reposições, vendas, financeiro ou acompanhamento dos alunos?
```

Resposta do usuário:

```text
n consigo vender bem meu studio
```

Resultado errado:

- O agente repetiu a mesma pergunta.
- Mesmo repetindo a resposta, ficou preso nessa etapa.

Resultado esperado:

- Interpretar como dor de vendas/interessados.
- Marcar dor correspondente.
- Humanizar a resposta.
- Avançar para a próxima pergunta do diagnóstico.

### Sugestões de próxima mensagem

- Na pergunta `Pra deixar esse diagnóstico salvo para você, Lucas, me passa um WhatsApp ou email? Se preferir, eu continuo mesmo assim, tudo bem?`, a sugestão apareceu como `Responder meu nome`. Está errado.
- Para pergunta de contato, sugestão deve ser algo como `Deixar meu WhatsApp` ou preencher input com `Meu WhatsApp é `.
- Na pergunta sobre dores, a sugestão estava sugerindo deixar WhatsApp, o que não condiz com a etapa.
- A sugestão deve sempre acompanhar a pergunta atual e o estado real do diagnóstico.

### Ritmo e humanização

- O ritmo atual está apressado.
- As mensagens podem ter delay maior.
- O fluxo está parecendo entrevista mecânica: agente pergunta, usuário responde, agente já joga outra pergunta.
- O comportamento esperado:
  1. agente faz uma pergunta;
  2. usuário responde;
  3. agente manda uma primeira mensagem curta reconhecendo a resposta de forma humana;
  4. depois emenda com outra mensagem curta contendo a próxima pergunta.
- Exemplo de padrão:
  - Usuário: `n consigo vender bem meu studio`
  - Agente msg 1: `Entendi. Quando a venda fica solta, muita gente interessada acaba esfriando antes de marcar uma aula.`
  - Agente msg 2: `Hoje você consegue ver facilmente o que precisa resolver no dia?`

### Geração do diagnóstico final

- O diagnóstico final deve parecer que levou tempo para ser montado.
- Quando o agente tiver as informações necessárias, deve dizer algo como:

```text
Ok, já tenho as informações necessárias para montar seu diagnóstico. Já te retorno.
```

- Depois disso, deve haver um delay maior.
- O diagnóstico deve sair por etapas, não tudo seco de uma vez.

Mensagem final 1 aprovada pelo usuário como boa:

```text
Pelo que você contou, o gargalo principal está em WhatsApp, reposições, faltas, vendas e interessados e gestão do dia. Antes de pensar em agente, a Taliya precisa organizar isso no CRM: alunos, conversas, agenda, financeiro e prioridades do dia no mesmo lugar.
```

Mensagem final 2 teve partes boas, mas precisa melhorar:

```text
Minha recomendação é começar olhando cadastro de alunos, histórico de conversas, agenda e presença, pipeline de interessados e painel do dia. Em cima disso, os agentes mais úteis seriam Atendimento, Agenda, Vendas e Gestão. Na prática, o CRM mostra prioridades e os agentes ajudam a agir. Pelo tamanho e momento do studio, eu compararia o 7 Agentes com calma, sem pular direto para assinatura. Quer que eu te mostre os planos já com essa recomendação?
```

Feedback do usuário:

- A recomendação precisa ser dinâmica conforme o diagnóstico.
- A parte depois de `Em cima disso...` ficou boa.
- Evitar recomendação genérica ou sempre empurrar o mesmo plano sem explicar o porquê.

### Agentes indicados no diagnóstico

- A seção/listagem `Agentes indicados` está feia e pouco funcional.
- Em vez de um bloco genérico, deve listar os agentes indicados um por vez.
- Para cada agente indicado, explicar:
  - qual dor ele resolve;
  - por que ele foi recomendado para aquele studio;
  - como ele atua na prática.
- Exemplo esperado:
  - `Atendimento`: resolve WhatsApp bagunçado e dúvidas repetidas.
  - `Agenda`: resolve reposições, faltas e encaixes.
  - `Vendas`: resolve perda de interessados e follow-up fraco.
  - `Gestão`: resolve falta de clareza do que precisa ser feito no dia.

## Estado do worktree

Depois do commit `f258be6`, ainda existem muitas alterações não commitadas em `specs/006-crm-operational-core/*`. Elas são da outra frente de conversa/sistema real.

Na próxima conversa:

- Não reverter essas mudanças.
- Não misturar essas mudanças com commits da landing/agente.
- Antes de commitar algo, usar `git status --short`.
- Se trabalhar na landing/agente, stagear apenas arquivos tocados nessa frente.

## Comandos úteis

Rodar local:

```powershell
npm run dev
```

Build/validação:

```powershell
npm run lint
npx tsc --noEmit
npm run build
```

Evals existentes:

```powershell
npm run eval:ai-routes
npm run eval:ai-multiturn
npm run eval:ai-sales-humanization
npm run eval:lead-pipeline
npm run eval:custom-diagnostic
npm run eval:whatsapp-webhook
```

## Prompt recomendado para abrir a nova conversa

Use este texto:

```text
Estamos migrando de uma conversa longa. Leia primeiro:
- AGENTS.md
- docs/conversation-handoff-2026-05-14.md
- specs/002-floating-ai-sales-agent/spec.md
- specs/002-floating-ai-sales-agent/plan.md
- specs/002-floating-ai-sales-agent/tasks.md
- specs/001-niche-landing-system/spec.md
- docs/taliya-agent-flow-test-scenarios.md
- docs/taliya-agent-flow-validation-matrix.md

Contexto: a landing /pilates está visualmente aprovada e protegida. Não redesenhar. O funil principal do widget/agente é diagnóstico gratuito consultivo, com tom humano e sem agressividade. O último commit em produção é f258be6. Existem muitas mudanças não commitadas em specs/006 da outra frente; não reverter nem misturar.

Primeira tarefa: confirmar o estado atual do widget/agente em produção e continuar a partir dos P0/P1 listados no handoff, sem começar do zero.
```
