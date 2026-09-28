# Matriz final de imagens, rotas e status - PT-BR

> Status: matriz visual canonica pos-revisao de produto. Pasta auditada: `D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508`.

## Regra

- Imagem aprovada guia pagina, familia ou componente.
- Imagem historica nao deve guiar implementacao visual final.
- Imagem de familia pode cobrir varias rotas/abas quando o produto decidiu heranca.
- Pagina cortada/contextual nao precisa imagem propria.

## Design system e app shell

| Imagem | Status | Uso |
| --- | --- | --- |
| `crm_1.webp` | Referencia | Referencia visual inicial, nao rota. |
| `01_round-1_visual-dna-tokens_aprovada.png` | Aprovada | DNA visual e tokens. |
| `02_round-1_visual-dna-tokens_duplicata.png` | Duplicata | Nao usar como fonte separada. |
| `03_round-2_app-shell_tentativa-1_nao-aprovada.png` | Historica/nao aprovada | Nao usar como final. |
| `04_round-2a_app-shell-tela-base_tentativa-2.png` | Historica | Rastro de iteracao. |
| `05_round-2a1_app-shell-tela-base_refino.png` | Historica | Rastro de iteracao. |
| `06_round-2a2_app-shell-tela-base_aprovada.png` | Aprovada | App shell base anterior. |
| `07_round-3a_componentes-web-referencia_aprovada.png` | Aprovada | Componentes web. |
| `08_round-3b1_inputs-formularios-filtros_aprovada.png` | Aprovada | Inputs, formularios e filtros. |
| `09_round-3b2_overlays-feedback_aprovada.png` | Aprovada | Overlays, drawers e feedback. |
| `10_round-3b3_visualizacoes-operacionais_aprovada.png` | Aprovada | Visualizacoes operacionais. |
| `11_round-3b4_comunicacao-agentes_aprovada.png` | Aprovada | Comunicacao, WhatsApp e agentes. |
| `12_round-3b5_sistema-plano-governanca_aprovada.png` | Aprovada | Sistema, plano e governanca. |
| `13_round-3c1_objetos-setup-dados_aprovada.png` | Aprovada | Objetos, setup e dados. |
| `14_round-3c2_agenda-financeiro-documentos_aprovada.png` | Aprovada | Agenda, financeiro e documentos. |
| `15_round-3c3_agentes-auditoria-relatorios_aprovada.png` | Aprovada | Agentes, auditoria e relatorios. |
| `16_round-4.1S_app-shell_01_base-web.png` | Aprovada | Shell global do app web. |

## App do studio

| Imagem | Rota/familia canonica | Status |
| --- | --- | --- |
| `17_round-4.1A_hoje_01_acima-da-dobra.png.png` | `/app/hoje` | Aprovada |
| `18_round-4.1A_hoje_02_drawer-tarefa.png.png` | `/app/hoje`, `/app/tarefas` | Aprovada |
| `19_round-4.1A_hoje_03_estado-critico-do-dia.png` | `/app/hoje` | Aprovada |
| `20_round-4.1A_hoje_04_historico-de-hoje.png.png` | `/app/hoje` | Aprovada |
| `21_round-4.1B_operacao_01_kanban-geral.png.png` | `/app/operacao` | Aprovada |
| `22_round-4.1B_operacao_02_kanban-com-drawer.png` | `/app/operacao` detalhe/drawer | Aprovada |
| `23_round-4.1C_tarefas_01_lista-detalhe.png.png` | `/app/tarefas` | Aprovada |
| `24_round-4.1C_checklists_01_lista-execucao-detalhe.png.png` | `/app/checklists` | Aprovada |
| `24_round-4.1D_inbox_01_conversa-aberta.png.png` | `/app/inbox` | Aprovada |
| `25_round-4.1C_aprovacoes_01_lista-decisao-detalhe.png.png` | `/app/aprovacoes` | Aprovada |
| `26_round-4.1F_agenda_01_calendario-operacional.png.png` | `/app/agenda` | Aprovada |
| `27_round-4.1E_alunos_01_lista-perfil-resumido.png.png` | `/app/alunos` | Aprovada |
| `28_round-4.1E_aluno-perfil_01_resumo-operacional.png.png` | `/app/alunos/[id]` | Aprovada |
| `29_round-4.1F_aula_01_detalhe-com-chamada.png.png` | `/app/aulas/[id]` | Aprovada |
| `30_round-4.1F_financeiro_01_visao-geral-filas.png.png` | `/app/financeiro` | Aprovada |
| `31_round-4.1F_reposicoes_01_fluxo-encaixe.png.png` | `/app/reposicoes` | Aprovada |
| `32_round-4.1F_financeiro_02_drawer-cobranca-selecionada.png.png` | `/app/financeiro` drawer | Aprovada |
| `33_round-4.1F_financeiro_03_kanban-financeiro.png.png` | `/app/financeiro/kanban` | Aprovada |
| `34_round-4.1F_financeiro_04_movimentacoes-filtros-drawer.png.png` | `/app/financeiro/movimentacoes` | Aprovada |
| `35_round-4.1F_turmas_01_lista-detalhe.png.png` | `/app/turmas` | Aprovada |
| `36_round-4.1F_grade_01_semana-modelo-bloqueio.png.png` | `/app/grade` | Aprovada |
| `37_round-4.1G_vendas_01_pipeline-kanban.png.png` | `/app/vendas` | Aprovada |
| `38_round-4.1G_vendas_02_lista-interessados.png.png` | `/app/interessados` | Aprovada |
| `39_round-4.1G_experimental_01_lista-acompanhamento.png.png` | `/app/aulas-experimentais` | Aprovada |
| `40_round-4.1G_matriculas_01_checklist-conversao.png.png` | `/app/matriculas` | Aprovada |
| `41_round-4.1H_retencao_01_riscos-lista-drawer.png.png` | `/app/retencao` | Aprovada |
| `42_round-4.1H_cancelamentos_01_fila-salvamento-drawer.png.png` | `/app/cancelamentos` | Aprovada |
| `43_round-4.1H_reativacoes_01_ex-alunos-retorno.png.png` | `/app/retencao/reativacoes` | Aprovada |
| `44_round-4.1H_reclamacoes_01_fila-caso-sensivel-drawer.png.png` | `/app/reclamacoes` | Aprovada |
| `45_round-4.1I_relatorios_01_visao-gestao.png.png` | `/app/relatorios` | Aprovada |
| `46_round-4.1I_dinheiro-na-mesa_01_oportunidades-por-origem.png.png` | `/app/dinheiro-na-mesa` | Aprovada |
| `47_round-4.1J_suporte_01_central-studio-taliya.png.png` | `/app/suporte` | Aprovada |

## Backoffice interno Taliya

| Imagem | Rota/familia canonica | Status |
| --- | --- | --- |
| `48_round-4.1K_internal_01_visao-operacional.png.png` | `/internal` | Aprovada |
| `49_round-4.1K_internal_02_tenants-lista-detalhe.png` | `/internal/tenants` | Aprovada |
| `50_round-4.1K_internal_03_tenant-detalhe-usuarios-grants.png` | `/internal/tenants/[tenantId]` | Aprovada |

## Onboarding/setup

| Imagem | Rota/familia canonica | Status |
| --- | --- | --- |
| `51A_round-4.1J_onboarding_shell-global-aprovado.png` | `/onboarding/*` shell | Aprovada |
| `51B_round-4.1J_onboarding_agente-configuracao-chat-aprovado.png` | `/onboarding/*` chat lateral | Aprovada |
| `51C_round-4.1J_onboarding_workspace-configuracao-aprovado.png` | `/onboarding/*` workspace | Aprovada |
| `78_round-4.1Q_onboarding_bem-vindo-taliya-setup-guiado-aprovado.png` | Entrada do setup guiado; boas-vindas e nome do studio | Aprovada |
| `51D_round-4.1J_onboarding_bloco-1-studio-v2-sem-nome-aprovado.png` | setup Studio; dias e horarios gerais, sem repetir nome | Aprovada; substitui 51D antiga como referencia funcional |
| `51D_round-4.1J_onboarding_bloco-1-studio-aprovado.png` | setup Studio antigo | Historica; substituida por 51D v2 para evitar repetir nome do studio |
| `51E_round-4.1J_onboarding_bloco-2-equipe-aprovado.png` | setup Equipe | Aprovada |
| `51F_round-4.1J_onboarding_bloco-3-canais-aprovado.png` | setup Canais | Aprovada |
| `51G_round-4.1J_onboarding_bloco-4-planos-aprovado.png` | setup Planos | Aprovada |
| `51H_round-4.1J_onboarding_bloco-5-alunos-aprovado.png` | setup Alunos | Aprovada |
| `51I_round-4.1J_onboarding_bloco-6-turmas-aprovado.png` | setup Turmas | Aprovada |
| `51J_round-4.1J_onboarding_bloco-7-agenda-aprovado.png` | setup Agenda | Aprovada |
| `51K_round-4.1J_onboarding_bloco-5-pagamento-aprovado.png` | setup Pagamento | Aprovada; numeracao visual conflita com bloco 5 |
| `51L_round-4.1J_onboarding_bloco-9-revisao-aprovado.png` | setup Revisao | Aprovada |

## Acesso e assinatura pre-CRM

| Imagem | Rota/familia canonica | Status |
| --- | --- | --- |
| `71_round-4.1Q_acesso-assinatura_shell-base-aprovado.png` | Shell base pre-CRM para conta, login, revisao de assinatura, confirmacao e bloqueio | Aprovada |
| `72_round-4.1Q_acesso-assinatura_signup-criar-conta-salvo-ajustes.png` | Criar conta pre-CRM com Google, Microsoft ou e-mail com link seguro | Salva; ajustes finos documentados |
| `73_round-4.1Q_acesso-assinatura_signin-entrar-salvo-ajustes.png` | Entrar na Taliya com Google, Microsoft ou e-mail/senha | Salva; ajustes finos documentados |
| `74_round-4.1Q_acesso-assinatura_revisar-assinatura-aprovado.png` | Revisar assinatura antes de checkout externo; plano, inclusoes, conta, cupom, total e CTA | Aprovada |
| `75_round-4.1Q_acesso-assinatura_aguardando-confirmacao-aprovado.png` | Aguardar confirmacao de assinatura apos iniciar pagamento seguro externo | Aprovada |
| `76_round-4.1Q_acesso-assinatura_resolver-assinatura-aprovado.png` | Resolver assinatura nao confirmada, expirada, recusada ou cancelada | Aprovada |
| `77_round-4.1Q_acesso-assinatura_assinatura-confirmada-setup-guiado-aprovado.png` | Assinatura confirmada; iniciar setup guiado pela Taliya | Aprovada |

## Agentes, fluxos e execucoes

| Imagem | Rota/familia canonica | Status |
| --- | --- | --- |
| `52_round-4.1L_agentes_01_catalogo-agentes-aprovado.png` | `/app/agentes` | Aprovada |
| `53_round-4.1L_agentes_02_agente-agenda-rotinas-aprovado.png` | `/app/agentes/[agentId]` | Aprovada |
| `54_round-4.1L_agentes_03_rotina-presenca-faltas-aprovado.png` | rotina/fluxos do agente | Aprovada |
| `55_round-4.1L_agentes_04_fluxo-falta-com-aviso-aprovado.png` | historica | Substituida por 56 |
| `56_round-4.1L_agentes_04_fluxo-falta-com-aviso-v2-aprovado.png` | `/app/fluxos/[flowId]` | Aprovada |
| `58_round-4.1L_agentes_05_teste-fluxo-falta-com-aviso-aprovado.png` | `/app/fluxos/[flowId]/simular` | Aprovada; linguagem final e Simulacao |
| `59_round-4.1L_agentes_06_publicar-rotina-presenca-faltas-aprovado.png` | publicacao contextual de rotina | Aprovada |
| `70_round-4.1P_execucoes_01_fluxo-falta-com-aviso-aprovado.png` | `/app/fluxos/execucoes/[runId]` | Aprovada |

## Configuracoes, billing e uso

| Imagem | Rota/familia canonica | Status |
| --- | --- | --- |
| `60_round-4.1M_configuracoes_01_hub-8-cards-aprovado.png` | `/app/configuracoes` | Aprovada |
| `61_round-4.1M_configuracoes_02_permissoes-aprovado.png` | `/app/configuracoes/permissoes` | Aprovada |
| `62_round-4.1M_configuracoes_03_pagamentos-financeiro-aprovado.png` | `/app/configuracoes/pagamentos` | Aprovada |
| `63_round-4.1M_configuracoes_04_agenda-aprovado.png` | `/app/configuracoes/agenda` | Aprovada |
| `64_round-4.1M_configuracoes_05_notificacoes-aprovado.png` | `/app/configuracoes/notificacoes` | Aprovada |
| `65_round-4.1N_billing_01_assinatura-taliya-aprovado.png` | `/app/billing` | Aprovada |
| `66_round-4.1N_billing_02_faturas-taliya-aprovado.png` | `/app/billing/invoices` | Aprovada |
| `67_round-4.1N_billing_03_add-ons-taliya-aprovado.png` | `/app/billing/add-ons` | Aprovada |
| `68_round-4.1O_uso_01_visao-geral-aprovado.png` | `/app/uso` | Aprovada |
| `69_round-4.1O_uso_02_extrato-aprovado.png` | `/app/uso/extrato` | Aprovada |

## Paginas/contextos sem imagem propria por decisao

| Item | Decisao |
| --- | --- |
| Contatos | Contextual; nao precisa imagem propria. |
| Qualidade de dados | Contextual; nao precisa imagem propria. |
| Historico do aluno | Aba/timeline no Perfil do Aluno. |
| Professor e notas | Contextual em Aula/Chamada, Perfil, Turmas e Agenda. |
| Contratos/documentos financeiros | Contextual em Financeiro, Matriculas e Perfil do Aluno. |
| Recursos/feriados/disponibilidade | Configuracoes de Agenda. |
| Exportacoes | Acao local por pagina exportavel. |
| Integracoes | Configuracoes por area. |
| Auditoria | Historico contextual; sem central para o studio. |
| Privacidade/solicitacoes | Termos/consentimentos contextuais e Suporte. |
| Politicas operacionais | Configuracoes/pre-definicoes por area e Agentes/Fluxos. |
| Lista de espera geral | Contextual em Vendas/Interessados, Agenda/Turmas, Hoje/Tarefas e conversas. |
| Creditos de reposicao | Dentro de Reposicoes. |
| Checkout de alunos | Matriculas, Financeiro, Aprovacoes e Operacao. |
| Eventos/workshops | Agenda, Turmas e Aula. |

## Imagens orfas/historicas

| Imagem | Motivo |
| --- | --- |
| `02_round-1_visual-dna-tokens_duplicata.png` | Duplicata da 01. |
| `03_round-2_app-shell_tentativa-1_nao-aprovada.png` | Tentativa nao aprovada. |
| `04_round-2a_app-shell-tela-base_tentativa-2.png` | Historica. |
| `05_round-2a1_app-shell-tela-base_refino.png` | Historica. |
| `55_round-4.1L_agentes_04_fluxo-falta-com-aviso-aprovado.png` | Substituida por 56. |
| Ausencia de `57` | Buraco de numeracao, nao lacuna de produto. |
