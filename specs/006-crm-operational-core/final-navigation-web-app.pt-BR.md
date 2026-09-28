# Navegacao final do Taliya CRM - PT-BR

> Status: fonte canonica de navegacao pos-revisao de produto. Este documento substitui a leitura direta de mapas antigos quando houver conflito sobre sidebar, topbar, topbar global, pre-CRM, suporte, billing e paginas contextuais.

## Principio

A navegacao do Taliya CRM se organiza em quatro camadas:

1. **Pre-CRM**: conta basica, assinatura e onboarding antes do app operacional.
2. **Sidebar do app**: familias principais de trabalho do studio.
3. **Topbar interna**: subitens da familia selecionada na sidebar.
4. **Topbar global**: busca, alertas, suporte, assinatura/billing e perfil.

Tudo que existe no produto nao precisa aparecer na sidebar. A sidebar deve responder: "em qual area do studio estou trabalhando?". A topbar interna deve responder: "qual visao desta area quero abrir?".

## Pre-CRM

Estas telas existem antes do usuario acessar o CRM operacional e nao aparecem na sidebar:

| Etapa | Papel | Observacao |
| --- | --- | --- |
| Criar conta basica | Criar login antes da assinatura. | Google, Microsoft ou e-mail com link seguro; sem senha na primeira tela. |
| Login | Entrar na conta. | Conta sem assinatura confirmada nao acessa `/app`. |
| Escolher plano | Selecionar plano Taliya. | Antes do checkout hospedado. |
| Checkout hospedado | Pagar/assinar com provedor externo. | Nao e pagina do CRM operacional. |
| Confirmacao de assinatura | Aguardar confirmacao segura apos iniciar pagamento. | Imagem 75; verificacao automatica, com retomar pagamento e suporte como fallback. |
| Assinatura pendente/falha | Retomar pagamento ou falar com suporte. | Acesso limitado; imagem 76 aprovada para resolver assinatura. |
| Assinatura confirmada | Confirmar sucesso e iniciar setup guiado. | Imagem 77; CRM ainda bloqueado ate configuracao inicial. |
| Onboarding/setup | Configurar o studio apos assinatura confirmada. | Setup guiado por agente de configuracao; usa shell proprio de onboarding, nao a sidebar operacional. |

Regra: antes da assinatura confirmada, o usuario nao acessa `/app`, nao configura studio, nao importa dados, nao convida equipe e nao ativa agentes.

## Sidebar web

A sidebar do app do studio tem 12 familias principais:

| Ordem | Sidebar | Rota inicial | Papel |
| ---: | --- | --- | --- |
| 1 | Hoje | `/app/hoje` | Comando do dia, prioridades, alertas e atalhos para a origem. |
| 2 | Inbox | `/app/inbox` | Conversas, WhatsApp, atendimento e handoff. |
| 3 | Alunos | `/app/alunos` | Lista, perfil, contexto operacional e historico permitido. |
| 4 | Agenda | `/app/agenda` | Agenda, grade, turmas, aulas, chamada e reposicoes. |
| 5 | Vendas | `/app/vendas` | Pipeline, interessados, aulas experimentais e matriculas. |
| 6 | Financeiro | `/app/financeiro` | Financeiro dos alunos do studio. |
| 7 | Retencao | `/app/retencao` | Riscos, cancelamentos, reativacoes e reclamacoes. |
| 8 | Operacao | `/app/operacao` | Jornadas, casos, tarefas, checklists e aprovacoes. |
| 9 | Agentes | `/app/agentes` | Agentes, fluxos, simulacoes, publicacoes e execucoes. |
| 10 | Uso e cotas | `/app/uso` | Consumo, limites, economia e extrato. |
| 11 | Relatorios | `/app/relatorios` | Relatorios e Dinheiro na Mesa. |
| 12 | Configuracoes | `/app/configuracoes` | Configuracoes pos-go-live por area. |

## Topbar interna por familia

### Hoje

Nao tem subabas estruturais. Pode ter filtros leves:

- Hoje;
- Esta semana;
- Criticos;
- Minha fila.

Hoje mostra prioridades e atalhos. A execucao completa fica na origem: Operacao, Tarefas, Aprovacoes, Agenda, Financeiro, Inbox etc.

### Inbox

Pode usar filtros ou chips, nao submodulos pesados:

- Todas;
- Aguardando humano;
- Nao lidas;
- Falhas/envios;
- Arquivadas.

### Alunos

Topbar da familia:

- Alunos.

O perfil do aluno abre como detalhe/pagina. Dentro do perfil, usar abas contextuais:

- Resumo;
- Agenda;
- Financeiro;
- Historico;
- Tarefas;
- Conversas.

Contatos, responsaveis, documentos, notas e consentimentos aparecem no contexto do aluno, sem pagina propria.

### Agenda

Topbar interna:

- Agenda;
- Grade;
- Turmas;
- Aulas;
- Reposicoes.

Lista de espera geral nao e pagina propria. Ela aparece contextualizada em Vendas/Interessados, Agenda/Turmas, Hoje/Tarefas e conversas. Creditos de reposicao ficam dentro de Reposicoes.

### Vendas

Topbar interna:

- Pipeline;
- Interessados;
- Experimentais;
- Matriculas.

Segmentos e Comunicados ficam pos-MVP. Checkout de alunos nao e pagina propria; pagamento inicial fica em Matriculas/Financeiro/Aprovacoes/Operacao conforme o caso.

### Financeiro

Topbar interna:

- Visao geral;
- Kanban;
- Movimentacoes.

Financeiro significa dinheiro dos alunos do studio. Billing/Assinatura Taliya nao entra aqui. Contratos, comprovantes, excecoes e exportacoes sao contextuais.

### Retencao

Topbar interna:

- Riscos;
- Cancelamentos;
- Reativacoes;
- Reclamacoes.

### Operacao

Topbar interna:

- Jornadas;
- Tarefas;
- Checklists;
- Aprovacoes.

Hoje mostra resumo/atalhos da Operacao, mas Operacao e a central de trabalho profunda.

### Agentes

Topbar interna:

- Agentes;
- Fluxos;
- Simulacoes;
- Execucoes.

Publicacao fica dentro de Fluxos/Simulacoes quando a rotina estiver pronta. Execucao e recibo operacional, nao log tecnico nem configuracao.

### Uso e cotas

Topbar interna:

- Visao geral;
- Extrato.

Add-ons e faturas ficam em Billing/Assinatura Taliya, acessado pela topbar global/menu de conta.

### Relatorios

Topbar interna:

- Relatorios;
- Dinheiro na Mesa.

Dinheiro na Mesa e pagina propria acionavel, nao apenas bloco dentro de Relatorios.

### Configuracoes

Configuracoes deve usar hub/cards e pode usar topbar curta quando necessario:

- Studio;
- Equipe;
- Permissoes;
- Agenda;
- Pagamentos/Financeiro;
- Canais;
- Notificacoes.

Politicas operacionais sao configuracoes/pre-definicoes por area, nao pagina propria. Integracoes ficam dentro da configuracao correspondente. Recursos, feriados e disponibilidade ficam em Configuracoes de Agenda. Privacidade fica contextual/termos/suporte, nao pagina propria.

## Topbar global

A topbar global fica sempre disponivel no app operacional:

| Item | Papel | Destino |
| --- | --- | --- |
| Busca global | Encontrar aluno, responsavel, conversa, aula, turma, tarefa, caso, interessado, cobranca, agente ou fluxo permitido. | Resultado/contexto correto. |
| Alertas | Mostrar pendencias, falhas, aprovacoes urgentes, cota e incidentes contextuais. | Origem do alerta. |
| Uso/cota resumido | Dar visibilidade rapida de consumo. | `/app/uso`. |
| Suporte Taliya | Ajuda do studio com a Taliya. | `/app/suporte`. |
| Plano/Assinatura | Plano, faturas, add-ons e pagamento da Taliya. | `/app/billing`. |
| Perfil/conta | Perfil, logout e troca de workspace quando houver. | Menu de conta. |

Suporte e Billing tem paginas proprias, mas nao entram na sidebar operacional.

## Paginas fora da sidebar principal

Estas paginas/superficies nao entram como familia de sidebar:

| Item | Como aparece |
| --- | --- |
| Suporte | Topbar global. |
| Billing/Assinatura Taliya | Topbar global/menu de conta. |
| Faturas Taliya | Dentro de Billing. |
| Add-ons Taliya | Dentro de Billing. |
| Perfil/conta | Topbar global/menu de conta. |
| Tarefas | Topbar interna de Operacao. |
| Checklists | Topbar interna de Operacao. |
| Aprovacoes | Topbar interna de Operacao. |
| Dinheiro na Mesa | Topbar interna de Relatorios. |
| Grade/Turmas/Aulas/Reposicoes | Topbar interna de Agenda. |
| Interessados/Experimentais/Matriculas | Topbar interna de Vendas. |
| Cancelamentos/Reativacoes/Reclamacoes | Topbar interna de Retencao. |
| Fluxos/Simulacoes/Execucoes | Topbar interna de Agentes. |
| Extrato de uso | Topbar interna de Uso e cotas. |

## Itens contextuais, sem pagina propria

| Item | Onde aparece |
| --- | --- |
| Contatos | Alunos, Interessados, Inbox, Matriculas, busca e seletores. |
| Qualidade de dados | Onboarding/importacao, Alunos, Agenda, Financeiro, Aprovacoes, Hoje e Tarefas. |
| Historico do aluno | Perfil do aluno e origens relacionadas. |
| Professor e notas | Aula/Chamada, Perfil do Aluno, Turmas e Agenda. |
| Contratos/documentos | Financeiro, Matriculas, Perfil do Aluno e historico contextual. |
| Excecoes financeiras | Financeiro, Aprovacoes, Tarefas, Aluno e Operacao. |
| Exportacoes | Acao local em cada pagina exportavel. |
| Integracoes | Configuracoes da area correspondente e alertas contextuais. |
| Auditoria | Historico/contexto da acao; sem central para o studio. |
| Privacidade/solicitacoes | Termos, consentimentos contextuais e Suporte para excecoes. |
| Politicas operacionais | Configuracoes/pre-definicoes por area e Agentes/Fluxos. |
| Recursos/feriados/disponibilidade | Configuracoes de Agenda e contexto de Agenda/Turmas/Aula. |
| Lista de espera geral | Contexto em Vendas/Interessados, Agenda/Turmas, Hoje/Tarefas e conversas. |
| Creditos de reposicao | Dentro de Reposicoes. |
| Checkout de alunos | Matriculas, Financeiro, Aprovacoes e Operacao. |

## Pos-MVP

| Item | Decisao |
| --- | --- |
| Segmentos | Pos-MVP/produto futuro. |
| Comunicados/campanhas | Pos-MVP/produto futuro. |
| Marketing amplo | Fora do escopo atual. |

## Backoffice interno Taliya

Backoffice interno nao aparece no app do studio.

| Area | Rota | Papel |
| --- | --- | --- |
| Operacao interna Taliya | `/internal` | Visao interna da Taliya. |
| Tenants | `/internal/tenants` | Lista e gestao interna de tenants. |
| Tenant detalhe | `/internal/tenants/[tenantId]` | Usuarios, grants, entitlements e suporte autorizado. |
| Sales inbox interno | `/internal/sales-inbox` | Operacao comercial da propria Taliya, separada do CRM dos studios. |

## App mobile

O app mobile segue outra hierarquia, com 5 abas fixas:

| Aba | Papel | Inclui |
| --- | --- | --- |
| Hoje | Comando do dia. | Prioridades, alertas, tarefas urgentes, aprovacoes e cotas. |
| Inbox | Atendimento. | Conversas, sugestoes, handoff e falhas. |
| Agenda | Rotina de aulas. | Agenda, turmas, aula, chamada e reposicoes. |
| Alunos | Consulta e acao rapida. | Busca, perfil, responsavel e historico permitido. |
| Mais | Areas complementares. | Operacao, vendas, financeiro, retencao, agentes, uso, relatorios, configuracoes, suporte e assinatura. |

Mobile nao define novas paginas web. Ele reorganiza o acesso conforme uso em campo.
