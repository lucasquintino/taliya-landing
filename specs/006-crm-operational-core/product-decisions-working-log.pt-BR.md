# Decisoes de produto em revisao - Taliya CRM

> Status: working log. Este arquivo registra decisoes tomadas na revisao de produto antes de qualquer implementacao. Nao define banco, API, schema tecnico ou plano de engenharia.

## Decisoes fechadas nesta rodada

### 1. Suporte

- Suporte tera pagina propria.
- Rota principal: `/app/suporte`.
- Imagem canonica: `47_round-4.1J_suporte_01_central-studio-taliya.png.png`.
- Suporte e a relacao do studio com a Taliya: tickets, status de servicos, suporte 24/7, grants temporarios e historico.
- Suporte nao e atendimento aos alunos.
- Suporte nao substitui Inbox, Operacao, Aprovacoes, Privacidade ou backoffice interno.

### 2. Segmentos e Comunicados

- Segmentos e Comunicados ficam pos-MVP/produto futuro.
- Nao criar `/app/segmentos` como pagina propria agora.
- Nao criar `/app/comunicados` como pagina propria agora.
- Comunicacoes necessarias no produto atual aparecem de forma contextual em Inbox, Tarefas, Operacao, Retencao, Vendas, Agenda ou Aprovacoes.
- Modulo de campanhas, publicos salvos e disparos em massa fica fora do escopo atual.

### 3. Financeiro, Billing Taliya e Agente Financeiro

- Financeiro significa financeiro dos alunos do studio.
- Billing/Assinatura Taliya significa relacao financeira entre o studio e a Taliya.
- Uso/Cotas significa consumo de agentes, mensagens, automacoes, economia e extrato.
- Agente Financeiro atua no financeiro dos alunos do studio.
- Agente Financeiro nao atua sobre faturas da Taliya, upgrade, add-ons ou cobranca da assinatura Taliya.
- Billing/Assinatura Taliya deve ser tratado por Billing Taliya e Suporte Taliya.

### 4. Reposicoes, creditos e lista de espera

- `/app/reposicoes` fica como pagina principal de reposicoes e encaixe.
- Creditos de reposicao ficam dentro de Reposicoes.
- Nao criar `/app/creditos-reposicao` como pagina propria agora.
- Lista de espera de encaixe/reposicao pode aparecer dentro de Reposicoes quando relacionada a vaga aberta e credito/direito de reposicao.
- Lista de espera geral nao fica dentro de Reposicoes.
- Lista de espera geral nao tera pagina propria agora.
- Pessoas aguardando vaga fixa em turma/horario aparecem contextualizadas em Vendas/Interessados, Agenda/Turmas, Hoje/Tarefas e conversas, conforme origem e proxima acao.

### 5. Checkout de alunos

- Nao criar `/app/checkout-alunos` como pagina propria.
- Pagamento inicial, link/Pix, contrato e confirmacao ficam dentro de Matriculas, Financeiro, Aprovacoes e Operacao, conforme o caso.
- Checkout de alunos nao e modulo separado do CRM.

### 6. Conta basica, assinatura e acesso ao CRM

- Conta basica vem antes da assinatura.
- Conta basica deve permitir somente:
  - continuar com Google;
  - continuar com Microsoft;
  - continuar com e-mail.
- Criar conta por e-mail nao pede senha na primeira tela.
- No fluxo por e-mail, a Taliya envia um link seguro para o usuario continuar e definir senha depois.
- Facebook nao entra como provedor de conta do SaaS.
- Antes da assinatura confirmada, a conta nao libera o CRM.
- Antes da assinatura confirmada, o usuario pode no maximo escolher plano, ir para checkout, retomar pagamento, ver status da assinatura, falar com suporte e sair.
- Nao liberar `/app`, setup do studio, importacao, equipe, agentes ou uso operacional antes da assinatura confirmada.
- Checkout da assinatura Taliya acontece fora do CRM operacional, em checkout hospedado por provedor externo.
- Depois de revisar a assinatura, o CTA `Continuar para pagamento seguro` leva imediatamente para a tela 75 de confirmacao automatica.
- A tela 75 acompanha a confirmacao do pagamento e pode reabrir o pagamento seguro ou suporte como fallback, sem liberar o CRM.
- A tela 76 e a recuperacao de assinatura nao confirmada: cancelada, expirada, recusada, abandonada ou sem confirmacao dentro do tempo esperado.
- A tela 76 nao deve ser usada para casos ainda pendentes; enquanto a confirmacao ainda pode chegar normalmente, o usuario permanece na 75.
- A tela 77 confirma assinatura ativa e leva para o setup guiado pela Taliya.
- O setup inicial tera agente de configuracao guiando o usuario passo a passo antes do primeiro uso.
- A 77 deve oferecer `Comecar setup guiado` como CTA principal e `Agendar ajuda humana` como opcao secundaria.
- O CTA `Comecar setup guiado` abre `/onboarding`; se for primeiro acesso, coleta o nome e cria/identifica o espaco interno do studio, e se ja houver setup em andamento, retoma a proxima etapa incompleta.
- `Agendar ajuda humana` adiciona acompanhamento humano ao mesmo Setup Inicial, sem criar fluxo paralelo.
- A imagem 78 passa a ser a primeira entrada visual do setup guiado: `Bem-vindo a Taliya`, nome do studio e agente lateral, sem stepper e sem repetir configuracoes operacionais.
- A 51D v2 substitui a 51D antiga como referencia funcional do bloco `Studio`; o nome do studio fica na 78, e a 51D v2 foca em dias e horarios gerais.
- Depois da assinatura confirmada, a Taliya libera a ativacao do espaco interno do studio e o onboarding/setup do studio.

### 7. Politicas operacionais

- Nao criar pagina propria de Politicas Operacionais.
- Politicas operacionais sao configuracoes/pre-definicoes por area.
- Regras de agenda, reposicao, feriados, disponibilidade e encaixe ficam nas configuracoes de Agenda.
- Regras financeiras ficam nas configuracoes de Pagamentos/Financeiro.
- Regras de mensagens, horarios, canais e notificacoes ficam nas configuracoes de Canais/Notificacoes.
- Regras de autonomia, aprovacao, fallback e comportamento dos agentes ficam nas paginas de Agentes/Fluxos.
- O usuario nao deve precisar lidar com uma abstracao separada chamada Politicas para operar o produto.

### 8. Qualidade de dados

- Nao criar pagina propria de Qualidade de Dados.
- Qualidade de dados e um fluxo contextual, nao uma superficie principal.
- Duplicidades, conflitos, dados incompletos e problemas de importacao aparecem dentro de Onboarding/Importacao, Alunos, Contatos, Interessados, Agenda, Financeiro ou Aprovacoes, conforme a origem.
- Quando houver pendencia humana, ela pode virar tarefa, aprovacao ou alerta em Hoje.
- O produto deve resolver saneamento de dados no contexto onde o dado e usado, sem obrigar o usuario a abrir uma central separada.

### 9. Contatos

- Nao criar pagina propria de Contatos.
- Contatos e uma entidade transversal/contextual.
- Dados de contato aparecem dentro de Alunos, Interessados, Inbox/Conversas, Matriculas, Responsaveis e demais fluxos onde forem necessarios.
- O produto nao deve criar um modulo generico de contatos separado da operacao do studio.
- Busca, filtros ou seletores podem encontrar contatos, mas sem transformar Contatos em superficie principal.

### 10. Historico do aluno

- Nao criar pagina propria de Historico do Aluno.
- Historico do aluno fica dentro do Perfil do Aluno como aba, timeline, bloco ou painel contextual.
- Eventos de presenca, reposicoes, pagamentos, tarefas, conversas, observacoes, documentos e ocorrencias aparecem no contexto do aluno.
- Historico sensivel deve respeitar permissao e visibilidade por papel.
- O usuario acessa historico a partir do aluno, aula, financeiro, tarefa ou caso relacionado, sem precisar abrir uma central separada.

### 11. Professor e notas

- Nao criar pagina propria de Professor e Notas.
- Notas, observacoes e contexto do professor ficam dentro de Aula/Chamada, Perfil do Aluno, Turmas e Agenda, conforme o uso.
- Professor pode ter visao limitada e operacional, mas sem modulo separado nesta fase.
- Observacoes sensiveis devem respeitar permissao e aparecer no contexto do aluno/aula, nao em uma central isolada.

### 12. Contratos e documentos financeiros

- Nao criar pagina propria de Contratos e Documentos Financeiros.
- Contratos, documentos, comprovantes e anexos financeiros ficam contextuais em Financeiro, Matriculas e Perfil do Aluno.
- Documentos podem aparecer como etapa de checklist, anexo de cobranca, registro financeiro ou item do historico do aluno.
- Nao criar uma central separada de documentos nesta fase.

### 13. Recursos, feriados e disponibilidade

- Nao criar pagina propria de Recursos, Feriados e Disponibilidade.
- Este escopo ja fica definido dentro de Configuracoes de Agenda.
- Dias fechados, feriados, bloqueios, excecoes, disponibilidade e regras de agenda aparecem nas configuracoes de Agenda e nos contextos de Agenda/Turmas/Aulas quando afetam a operacao.

### 14. Exportacoes

- Nao criar pagina propria de Exportacoes.
- Cada pagina exportavel tera sua propria acao de exportacao no contexto.
- Exportacoes de relatorios ficam em Relatorios.
- Exportacoes financeiras ficam em Financeiro.
- Exportacoes de alunos/listas ficam na pagina correspondente.
- Exportacoes sensiveis devem respeitar permissao, confirmacao e auditoria, mas nao exigem uma central separada de exportacoes nesta fase.

### 15. Integracoes

- Nao criar pagina propria de Integracoes.
- Integracoes ficam distribuidas nas configuracoes de cada area.
- WhatsApp, e-mail e canais ficam em Configuracoes de Canais/Notificacoes.
- Pagamentos/provedor financeiro ficam em Configuracoes de Pagamentos/Financeiro.
- Agenda/calendario, feriados, disponibilidade e regras relacionadas ficam em Configuracoes de Agenda.
- Estados de erro de integracao aparecem no contexto operacional onde impactam a rotina, como Hoje, Tarefas, Financeiro, Agenda, Inbox ou Suporte.
- Nao criar uma central tecnica separada de integracoes nesta fase.

### 16. Privacidade e solicitacoes

- Nao criar pagina propria de Privacidade e Solicitacoes.
- O produto nao tera uma central onde a pessoa pede livremente exportacao, exclusao, anonimizacao ou outros fluxos amplos.
- O aceite de termos, consentimentos e regras de comunicacao deve acontecer nos pontos corretos do produto.
- Consentimentos e opt-outs aparecem de forma contextual em Alunos, Responsaveis, Interessados, Inbox/Conversas, Canais/Notificacoes e Financeiro quando impactarem uma acao.
- Casos excepcionais ou duvidas sensiveis devem ir para Suporte, nao para uma pagina operacional propria.
- Termos aceitos e eventos sensiveis devem ficar registrados/auditaveis, mas sem criar uma central de Privacidade nesta fase.

### 17. Auditoria

- Nao criar pagina propria de Auditoria para o studio nesta fase.
- Auditoria fica como historico/contexto dentro das paginas onde a acao aconteceu.
- Acoes sensiveis devem mostrar registro, responsavel, data, motivo e origem quando isso for relevante para a decisao do usuario.
- Historico de aprovacoes, mudancas de configuracao, envios, pagamentos, agentes e suporte aparece no contexto correspondente.
- Suporte Taliya pode usar registros de auditoria para diagnostico e seguranca, mas o studio nao precisa de uma central separada de auditoria agora.

### 18. Execucoes e incidentes de agentes

- Execucoes de fluxo ja estao definidas como detalhe contextual.
- Rota de detalhe: `/app/fluxos/execucoes/[runId]`.
- Imagem canonica: `70_round-4.1P_execucoes_01_fluxo-falta-com-aviso-aprovado.png`.
- Execucao e um recibo operacional de uma execucao real, nao uma nova familia grande.
- Execucao nao e log tecnico e nao serve para configurar/publicar fluxo.
- Incidentes nao precisam virar central separada nesta fase.
- Incidentes aparecem em execucao, tarefas, aprovacoes, operacao, suporte ou na pagina onde impactarem a rotina.

### 19. Aprovacoes

- Aprovacoes tera pagina propria.
- Rota principal: `/app/aprovacoes`.
- Imagem canonica: `25_round-4.1C_aprovacoes_01_lista-decisao-detalhe.png.png`.
- Aprovacoes e uma fila transversal de decisoes sensiveis.
- Recebe decisoes de financeiro, agenda, agentes, mensagens, permissoes, suporte, cancelamentos e outros fluxos.
- A pagina deve mostrar impacto, origem, risco, solicitante, decisor, motivo e status da decisao.

### 20. Checklists

- Checklists tera pagina propria.
- Rota principal: `/app/checklists`.
- Imagem canonica: `24_round-4.1C_checklists_01_lista-execucao-detalhe.png.png`.
- Checklists serve para rotinas recorrentes do studio.
- Checklists nao sao apenas componentes dentro de tarefas.
- A pagina deve cobrir listas recorrentes, execucoes, responsaveis, status, detalhe, historico e continuidade com Tarefas/Operacao/Aprovacoes quando necessario.

### 21. Eventos e workshops

- Nao criar pagina propria de Eventos/Workshops.
- Eventos e workshops ficam dentro de Agenda, Turmas e Aula.
- Eventos podem aparecer como tipo de aula, ocorrencia de agenda, item de turma, detalhe de aula ou contexto operacional.
- Nao criar superficie separada para eventos nesta fase.

### 22. Relatorios e Dinheiro na Mesa

- Relatorios tera pagina propria.
- Rota principal de Relatorios: `/app/relatorios`.
- Imagem canonica de Relatorios: `45_round-4.1I_relatorios_01_visao-gestao.png.png`.
- Dinheiro na Mesa tera pagina propria.
- Rota principal de Dinheiro na Mesa: `/app/dinheiro-na-mesa`.
- Imagem canonica de Dinheiro na Mesa: `46_round-4.1I_dinheiro-na-mesa_01_oportunidades-por-origem.png.png`.
- Dinheiro na Mesa e uma superficie acionavel de oportunidades, nao apenas um bloco dentro de Relatorios.

### 23. Retencao, Cancelamentos, Reativacoes e Reclamacoes

- Retencao tera pagina propria.
- Rota principal: `/app/retencao`.
- Imagem canonica: `41_round-4.1H_retencao_01_riscos-lista-drawer.png.png`.
- Cancelamentos tera pagina propria.
- Rota principal: `/app/cancelamentos`.
- Imagem canonica: `42_round-4.1H_cancelamentos_01_fila-salvamento-drawer.png.png`.
- Reativacoes tera pagina propria.
- Rota principal: `/app/retencao/reativacoes`.
- Imagem canonica: `43_round-4.1H_reativacoes_01_ex-alunos-retorno.png.png`.
- Reclamacoes tera pagina propria.
- Rota principal: `/app/reclamacoes`.
- Imagem canonica: `44_round-4.1H_reclamacoes_01_fila-caso-sensivel-drawer.png.png`.

### 24. Aulas experimentais e Matriculas

- Aulas experimentais tera pagina propria.
- Rota principal: `/app/aulas-experimentais`.
- Imagem canonica: `39_round-4.1G_experimental_01_lista-acompanhamento.png.png`.
- Matriculas tera pagina propria.
- Rota principal: `/app/matriculas`.
- Imagem canonica: `40_round-4.1G_matriculas_01_checklist-conversao.png.png`.
- Aulas experimentais e Matriculas nao devem ser absorvidas apenas por Vendas/Interessados.

### 25. Vendas e Interessados

- Vendas tera pagina propria.
- Rota principal: `/app/vendas`.
- Imagem canonica: `37_round-4.1G_vendas_01_pipeline-kanban.png.png`.
- Interessados tera pagina propria.
- Rota principal: `/app/interessados`.
- Imagem canonica: `38_round-4.1G_vendas_02_lista-interessados.png.png`.
- Vendas e Interessados sao paginas separadas, nao apenas visoes uma da outra.

### 26. Navegacao, sidebar e topbar

- Sidebar do app do studio deve ter somente familias principais.
- Topbar interna mostra os subitens da familia selecionada na sidebar.
- Topbar global mostra busca, alertas, uso/cota resumido, Suporte Taliya, Plano/Assinatura e Perfil/conta.
- Suporte tem pagina propria, mas nao entra na sidebar operacional; entra pela topbar global.
- Billing/Assinatura Taliya tem paginas proprias, mas nao entra na sidebar operacional; entra pela topbar global/menu de conta.
- Hoje e comando do dia, nao familia de Operacao.
- Operacao e a central profunda de jornadas, tarefas, checklists e aprovacoes.
- Backoffice interno Taliya fica fora do app do studio.

## Pendente para depois da revisao

- Avaliar se a revisao final de imagens exige alguma nova imagem apos consolidar a navegacao.
- Revisar docs historicos antigos apenas quando eles forem usados como fonte para prompts ou telas.
