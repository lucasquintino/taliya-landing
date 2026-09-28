# Arvore de telas - versao de leitura PT-BR

> Status: inventario exploratorio. Esta versao usa nomes de telas e areas de produto, nao caminhos tecnicos de rota.

## Como ler

- Esta lista mostra quais lugares podem existir no CRM web e no app mobile.
- Nem todo item precisa virar uma tela separada.
- Alguns itens podem virar botao, painel lateral, filtro, aba, alerta, tarefa ou automacao.
- Os caminhos tecnicos ficam nos documentos oficiais de implementacao, depois que a arquitetura for decidida.

## CRM web

| Area | Telas ou espacos provaveis | Para que serve |
| --- | --- | --- |
| Entrada e assinatura | Pagina inicial, pagina de Pilates, planos, demonstracao, checkout, confirmacao de assinatura, falha de assinatura | Vender, ativar e recuperar a compra do sistema. |
| Acesso e configuracao inicial | Login, ativacao da conta, perfil do studio, importacao, agentes, revisao final | Colocar o studio de pe antes do uso diario. |
| Hoje | Visao do dia, prioridades, notificacoes | Dar ao gestor uma mesa de comando diaria. |
| Atendimento | Caixa de entrada, conversas, envios, contatos, responsaveis, grupos | Centralizar WhatsApp, pedidos, respostas e dados de contato. |
| Alunos e historico | Lista de alunos, perfil do aluno, linha do tempo, documentos, permissoes, professores | Entender o aluno sem expor informacao sensivel para quem nao deve ver. |
| Agenda e aulas | Agenda, grade, turmas, aula, chamada, reposicoes, creditos, lista de espera, eventos | Operar a rotina de aulas, faltas, encaixes e reposicoes. |
| Vendas e matriculas | Vendas, captura, origens, interessados, experimental, matriculas, checkout de aluno, indicacoes, perdidos, segmentos | Converter interessados em alunos e entender onde as vendas nascem. |
| Financeiro | Visao financeira, pagamentos, cobrancas, conciliacao, excecoes, alteracoes de plano, acordos, reembolsos, documentos, contratos, planos de alunos | Cobrar, confirmar, corrigir e auditar dinheiro com seguranca. |
| Retencao e satisfacao | Retencao, riscos, campanhas, cancelamentos, satisfacao, reclamacoes | Evitar cancelamentos e recuperar confianca. |
| Operacao | Casos operacionais, incidentes, tarefas, aprovacoes, checklists, comunicados | Resolver o que travou, com dono, prazo e historico. |
| Relatorios | Receita em aberto, gargalos, capacidade, relatorios financeiros, vendas, risco, agentes, ocupacao | Ajudar o gestor a decidir com dados. |
| Agentes e automacoes | Agentes, configuracao de agente, fluxos, simulacao, execucoes | Controlar o que os agentes podem fazer e revisar o que fizeram. |
| Cotas e uso | Uso, cotas, custos, extrato, alertas, pacotes, regras de economia, limites por fluxo | Evitar surpresa de custo e limitar automacoes caras. |
| Administracao | Importacao, integracoes, auditoria, qualidade de dados, duplicidades, exportacoes, privacidade, acesso do suporte | Manter o sistema confiavel e governado. |
| Configuracoes | Studio, equipe, permissoes, canais, respostas prontas, agenda, financeiro, vendas, retencao, privacidade, recursos, campos, notificacoes | Ajustar regras que afetam a operacao inteira. |
| Politicas operacionais | Regras versionadas, simulacao de mudanca, ativacao de nova regra | Mudar regra sem quebrar automacoes e historico. |

## App mobile

| Area | Telas ou espacos provaveis | Para que serve |
| --- | --- | --- |
| Hoje | Prioridades, agenda do dia, alertas | Ver o que precisa de acao agora. |
| Inbox | Conversas, resposta rapida, assumir atendimento | Resolver conversa sem abrir o computador. |
| Agenda | Agenda, aula, chamada, reposicao, lista de espera | Operar aula e presenca no dia a dia. |
| Aluno | Perfil resumido, contatos, plano, historico permitido | Consultar contexto essencial. |
| Professor | Contexto da aula, observacao, restricao, lembrete de nota | Apoiar professor antes e depois da aula. |
| Aprovacoes | Acoes sugeridas, excecoes financeiras, comunicados, automacoes bloqueadas | Aprovar ou negar decisoes sensiveis. |
| Tarefas e casos | Minhas tarefas, casos urgentes, reclamacoes | Resolver pendencias fora da mesa. |
| Financeiro essencial | Pagamento, cobranca, atraso, comprovante | Tomar pequenas acoes financeiras com controle. |
| Agentes | Alertas, desempenho resumido, incidente, pausa emergencial | Acompanhar agentes sem administrar tudo pelo celular. |
| Cotas | Consumo, alerta de limite, pedido de pacote | Evitar que uso automatico estoure o combinado. |

## Decisao pendente

| Pergunta | Por que importa |
| --- | --- |
| O que fica no menu principal? | Menu grande demais deixa o CRM pesado. |
| O que vira botao contextual? | Muitos fluxos podem viver dentro da tela do aluno, da turma ou do pagamento. |
| O que fica apenas no computador? | Configuracoes sensiveis e revisoes grandes tendem a ser melhores no web. |
| O que precisa funcionar no celular? | Gestor e professor precisam agir durante a rotina, nao apenas no escritorio. |
| O que exige aprovacao humana? | Financeiro, historico sensivel, privacidade e autonomia dos agentes precisam de trava clara. |
