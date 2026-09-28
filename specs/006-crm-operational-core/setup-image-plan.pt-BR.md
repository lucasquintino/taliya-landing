# Setup E Configuracoes - Plano De Imagens

Status: plano visual v0.1.
Data: 2026-05-13.

## Objetivo

Definir quais imagens precisam ser geradas para setup/configuracoes, sem repetir telas que podem herdar padroes ja aprovados.

Antes das paginas finais, gerar os assets reutilizaveis definidos em `setup-reusable-visual-assets-map.pt-BR.md`.

## Principio

So gerar imagem quando a rota precisar provar layout, hierarquia ou estado diferente.

Quando a rota herda lista + filtros + drawer, kanban + drawer, tabela + detalhe ou painel de impacto ja aprovado, documentar sem imagem nova.

## Imagens novas recomendadas

Observacao de numeracao: a faixa `47-50` ja aparece em outros planos como Suporte/Internal. Para evitar colisao visual, a familia de onboarding passa a usar uma faixa propria a partir de `51`.

## Assets reutilizaveis antes das paginas

| Nome sugerido | Uso |
|---|---|
| `51A_round-4.1J_onboarding_asset_shell-base.png` | Shell proprio de onboarding para todas as paginas. |
| `51B_round-4.1J_onboarding_asset_agent-panel.png` | Chat lateral contextual do agente de configuracao. |
| `51C_round-4.1J_onboarding_asset_configuration-workspace.png` | Area central de configuracao guiada dentro do shell. |
| `53A_round-4.1J_onboarding_import_source-selector.png` | Seletor de fonte de importacao. |
| `53B_round-4.1J_onboarding_import_confidence-table.png` | Tabela de confianca por campo. |
| `54A_round-4.1J_onboarding_agent-prepared-card.png` | Card de agente preparado. |
| `55A_round-4.1J_onboarding_review-layer-summary.png` | Resumo de camadas da revisao/publicacao. |

Observacao apos aprovacao do `51B`: o `51A` deve ser revisado ou regerado para encaixar o chat lateral contextual do agente. O shell nao deve reservar a lateral direita para painel de cards, lista de proximos passos ou pendencias do agente.

Status atual:

- `51A` aprovado como shell global em `setup-51A-shell-base-approved.pt-BR.md`;
- `51B` aprovado como chat lateral em `setup-51B-agent-chat-approved.pt-BR.md`;
- `51C` aprovado como workspace central de configuracao em `setup-51C-configuration-workspace-approved.pt-BR.md`;
- `51D` aprovado como primeira tela real do setup, Bloco 1 Studio, em `setup-51D-bloco-1-studio-approved.pt-BR.md`;
- `51E` aprovado como Bloco 2 Equipe, em `setup-51E-bloco-2-equipe-approved.pt-BR.md`;
- `51F` aprovado como Bloco 3 Canais, em `setup-51F-bloco-3-canais-approved.pt-BR.md`.
- `51G` aprovado como Bloco 4 Planos, em `setup-51G-bloco-4-planos-approved.pt-BR.md`.
- `51K` aprovado como Bloco 5 Pagamento, em `setup-51K-bloco-5-pagamento-approved.pt-BR.md`.
- `51H` aprovado como padrao visual de Alunos, agora Bloco 6 oficial, em `setup-51H-bloco-5-alunos-approved.pt-BR.md`.
- `51I` aprovado como padrao visual de Turmas, agora Bloco 7 oficial, em `setup-51I-bloco-6-turmas-approved.pt-BR.md`.
- `51J` aprovado como padrao visual de Agenda, agora Bloco 8 oficial, em `setup-51J-bloco-7-agenda-approved.pt-BR.md`.
- `51L` aprovado como Bloco 9 Revisao, em `setup-51L-bloco-9-revisao-approved.pt-BR.md`.

Regra de stepper/progresso: ver `setup-stepper-progress-9-blocks.pt-BR.md`. Nao regenerar `51H`, `51I` e `51J` apenas por numeracao/progresso; ajustar isso na implementacao.

Arquivos consolidados na pasta nomeada:

- `D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\51A_round-4.1J_onboarding_shell-global-aprovado.png`;
- `D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\51B_round-4.1J_onboarding_agente-configuracao-chat-aprovado.png`;
- `D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\51C_round-4.1J_onboarding_workspace-configuracao-aprovado.png`;
- `D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\51D_round-4.1J_onboarding_bloco-1-studio-aprovado.png`;
- `D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\51E_round-4.1J_onboarding_bloco-2-equipe-aprovado.png`;
- `D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\51F_round-4.1J_onboarding_bloco-3-canais-aprovado.png`;
- `D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\51G_round-4.1J_onboarding_bloco-4-planos-aprovado.png`;
- `D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\51K_round-4.1J_onboarding_bloco-5-pagamento-aprovado.png`;
- `D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\51H_round-4.1J_onboarding_bloco-5-alunos-aprovado.png`;
- `D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\51I_round-4.1J_onboarding_bloco-6-turmas-aprovado.png`;
- `D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\51J_round-4.1J_onboarding_bloco-7-agenda-aprovado.png`;
- `D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\51L_round-4.1J_onboarding_bloco-9-revisao-aprovado.png`.

Decisao atualizada para Agenda:

- o Bloco 7 `Agenda` nao permite importacao externa;
- importacoes que ajudam a descobrir alunos ou turmas acontecem nos Blocos 5 e 6;
- o Bloco 7 apenas controla e revisa a semana base gerada dentro do Taliya.

Decisao atualizada para Pagamento:

- `Pagamento` entra no Setup Inicial como bloco proprio depois de `Planos`;
- `Planos` define o que o aluno compra e que cobrancas serao geradas;
- `Pagamento` define os meios aceitos no inicio e como a equipe registra/baixa pagamentos no Taliya;
- a tela deve ser organizada em 3 linhas completas: `Meios de pagamento`, `Exemplo da operacao` e `Pagamentos Taliya`;
- meios MVP: Pix, dinheiro e cartao, apresentados como cards/blocos fixos de selecao multipla;
- os meios nao abrem configuracao propria no Setup Inicial;
- a tela deve ter uma simulacao operacional forte e generica, mostrando uma cobranca saindo de um plano, sendo paga por um meio aceito e liberando o direito de aula/saldo;
- a tela deve ter uma linha de `Pagamentos Taliya`, deixando claro o que so sera ativado depois em automacao financeira;
- `Pagamentos Taliya`, Pix conectado, cartao online e recorrencia automatica ficam para pos-go-live;
- as imagens posteriores a Planos continuam aprovadas funcionalmente, mas seu stepper/progresso deve seguir a sequencia oficial de 9 blocos.

Decisao apos revisao:

- `51C` antigo, checklist/progresso, nao sera gerado. Ele foi substituido por `51C` novo: area central de configuracao guiada.
- O antigo `51E` de drawer de pendencias nao sera gerado agora. A letra `51E` passa a identificar a segunda tela real aprovada do setup: `Bloco 2 - Equipe`.
- O antigo `51D` de previa de impacto standalone nao sera gerado agora. A letra `51D` passa a identificar a primeira tela real aprovada do setup: `Bloco 1 - Studio`.
- A previa de impacto continua como slot/comportamento dentro das paginas finais quando necessario, usando o padrao central aprovado no 51C.

| Nome sugerido | Rota/tema | Por que precisa |
|---|---|---|
| `51_round-4.1J_onboarding_01_inicio-retomada.png` | `/onboarding` | Mostra o shell proprio de onboarding, progresso, retomada e ajuda do agente de setup. |
| `52_round-4.1J_onboarding_02_diagnostico-guiado.png` | `/onboarding/diagnostico` | Mostra diagnostico guiado do studio antes de configurar areas. |
| `53_round-4.1J_onboarding_03_setup-agente-checklist-impacto.png` | `/onboarding/setup` | Mostra agente de setup, checklist, pendencias e impacto do setup inicial. |
| `54_round-4.1J_onboarding_04_configuracao-area.png` | `/onboarding/configuracoes/[area]` | Mostra configuracao guiada por area, com regra em rascunho, validacao e impacto. |
| `55_round-4.1J_onboarding_05_cobranca-consumo-reposicao.png` | `/onboarding/configuracoes/consumo-aulas` | Area critica: cobranca, direito de aula, consumo, reposicao e excecoes. |
| `56_round-4.1J_onboarding_06_importacao-dados-conflitos.png` | `/onboarding/importacao` | Importacao multimodal: planilha, Google Agenda, foto/PDF/caderno, confianca por campo, saneamento, duplicidades e conflitos dentro do shell de onboarding. |
| `57_round-4.1J_onboarding_07_revisao-publicacao.png` | `/onboarding/revisao` | Mostra revisao e publicacao como uma experiencia: pronto, parcial, bloqueado ou pendente para pos-go-live. `/onboarding/publicacao` so vira rota propria se a publicacao precisar muitos estados. |
| `58_round-4.1J_onboarding_08_setup-publicado.png` | `/onboarding/concluido` | Opcional; pode virar estado/modal de conclusao sem imagem obrigatoria. |

## Imagens pos-go-live e control planes

Estas imagens nao pertencem ao setup inicial. Devem ser feitas depois, quando a familia Configuracoes/Agentes/Controle for atacada:

| Nome sugerido | Rota/tema | Por que precisa |
|---|---|---|
| `59_round-4.1J_configuracoes_01_hub-detalhe-secao.png` | `/app/configuracoes` | Hub pos-go-live com secoes, status e detalhe lateral. |
| `60_round-4.1J_politicas_01_versao-simulacao.png` | `/app/politicas` | Regras de seguranca/politicas sao sensiveis e precisam mostrar versao, simulacao e impacto. |
| `61_round-4.1J_agentes-fluxos_01_configurar-simular.png` | `/app/agentes/[agentId]/fluxos/[flowId]` | Configuracao profunda de fluxo: modo, limites, aprovacao, fallback, preflight, simulacao e publicacao. |
| `62_round-4.1J_uso-cotas_01_consumo-economia.png` | `/app/uso` | Cotas/uso precisam ser visiveis para autonomia e plano. |
| `63_round-4.1J_controle_01_execucoes-incidentes.png` | `/app/controle/execucoes` + `/app/controle/incidentes` | Control plane para traces, falhas, bloqueios, incidentes e reprocessamento seguro. |

## Imagens que podem herdar padrao existente

| Rota | Herda de | Motivo |
|---|---|---|
| `/app/configuracoes/studio` | Hub + formulario/drawer | Dados simples e secoes. |
| `/app/configuracoes/agenda` | Configuracao por area | Regras de agenda. |
| `/app/configuracoes/financeiro` | Configuracao por area | Regras financeiras. |
| `/app/configuracoes/canais` | Integracoes/configuracao por area | Conexoes e status. |
| `/app/configuracoes/templates` | Tabela/lista + drawer | Modelos, status e aprovacao. |
| `/app/configuracoes/equipe` | Tabela/lista + drawer | Usuarios e papeis. |
| `/app/configuracoes/permissoes` | Permissoes/governanca da 3B.5 | Matriz simples. |
| `/app/configuracoes/notificacoes` | Configuracao por area | Preferencias e alertas. |
| `configuracao especifica da integracao` | 3B.5 + 3C.3 | Status e falhas. |
| `/app/auditoria` | 3C.3 | Logs e detalhes. |
| `/app/billing` | 3B.5 | Plano, pagamento e faturas. |
| `/app/privacidade/solicitacoes` | 3C.3 | Fila sensivel + drawer. |

## Anexos recomendados para prompts

Usar poucos anexos por imagem para nao confundir o gerador:

### Setup inicial

- `16_round-4.1S_app-shell_01_base-web.png`
- `design-system-round-3c1-web-objects-setup-data` ou imagem equivalente da rodada 3C.1
- `design-system-round-3b4-web-communication-agents` ou imagem equivalente da rodada 3B.4

Observacao: o setup inicial deve herdar o DNA visual da Taliya, mas usar shell proprio de onboarding. Nao deve copiar a sidebar operacional completa do CRM.

### Configuracao por area

- `16_round-4.1S_app-shell_01_base-web.png`
- `3B.1 Inputs, Formularios e Filtros`
- `3B.2 Overlays e Feedback`

### Cobranca, consumo e reposicao

- `16_round-4.1S_app-shell_01_base-web.png`
- `34_round-4.1F_financeiro_04_movimentacoes-filtros-drawer.png`
- imagem aprovada de Agenda/Reposicoes quando disponivel

### Revisao e publicacao

- `16_round-4.1S_app-shell_01_base-web.png`
- `3B.5 Sistema, Plano e Governanca`
- `3C.3 Agentes Avancados, Auditoria e Relatorios`

## Regras para os prompts

Cada prompt deve dizer:

- qual rota esta sendo desenhada;
- qual decisao de usuario a tela precisa suportar;
- quais blocos devem existir;
- quais blocos nao devem existir;
- quais estados precisam aparecer;
- qual imagem aprovada deve ser respeitada;
- que o design deve seguir o DNA visual Taliya.

Cada prompt nao deve:

- explicar toda a historia do produto;
- pedir para inventar novas rotas;
- misturar onboarding, operacao diaria e configuracao pos-go-live na mesma imagem;
- configurar profundamente modo/limite de fluxo de agente no onboarding;
- transformar agente de setup em quem publica sozinho.

Cada prompt deve mostrar a diferenca entre `pronto agora` e `para depois` somente quando isso fizer parte da decisao visual da tela. Evitar banner repetitivo; preferir painel de impacto, status de pendencia, microcopy em card de agente ou resumo de revisao.

## Resultado esperado da familia 4.1J

Depois dessas imagens, devemos conseguir gerar:

- setup inicial;
- configuracao/reconfiguracao;
- regras de seguranca/aprovacoes;
- agentes/fluxos;
- uso/cotas;
- hub de configuracoes.

Isso fecha a parte critica antes de partir para mobile ou implementacao.
