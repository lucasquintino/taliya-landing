# Rodada 9 - Simulacoes de usuario - PT-BR

> Status: v0.1. Esta rodada testa o produto como gestor/equipe antes de dizer que esta pronto para virar prompt visual ou prototipo.

## Resultado curto

As simulacoes nao revelaram uma area inteira sem tela. O principal achado e que o produto depende de decisoes finais em politicas, formulas e escopos sensiveis antes de ser chamado de 100%.

## Simulacoes obrigatorias

| # | Simulacao | Telas principais | Resultado v0.1 |
| ---: | --- | --- | --- |
| 1 | Studio compra e ativa pelo app | Setup mobile, Configuracao inicial, Agentes, Cotas | Resolvido com setup essencial; configuracao profunda vai para web. |
| 2 | Studio compra e ativa pelo web | Onboarding, Importacao, Agentes, Revisao | Resolvido; importacao insegura vira Qualidade de dados. |
| 3 | Gestor abre o dia | Hoje, Notificacoes, Tarefas, Aprovacoes | Resolvido; mesa de comando tem origem/dono/acao. |
| 4 | Recepcao responde WhatsApp | Inbox, Conversa, Contato, Aluno | Resolvido manual/copiloto/autonomo com consentimento/cota. |
| 5 | Professor opera aula e chamada | Agenda, Aula, Chamada, Professor | Resolvido no mobile; historico restrito aparece filtrado. |
| 6 | Turma tem vaga e precisa encaixe | Turmas, Reposicoes, Lista de espera | Resolvido; encaixe e programatico, IA ajuda em explicacao/mensagem. |
| 7 | Interessado vira experimental | Interessados, Experimental, Agenda | Resolvido; origem e proxima acao preservadas. |
| 8 | Experimental vira matricula | Experimental, Matriculas, Aluno, Financeiro | Resolvido com pendencias explicitas; minimos finais seguem D025. |
| 9 | Pagamento atrasa | Financeiro, Pagamentos, Conversa, Tarefas | Resolvido; cobranca sensivel respeita permissao/cota/template. |
| 10 | Comprovante chega | Inbox, Pagamentos, Conciliacao | Resolvido; comprovante nao confirmado vira analise. |
| 11 | Aluno pede cancelamento | Cancelamentos, Retencao, Financeiro, Aprovacoes | Resolvido com fluxo/tarefa e aprovacao se houver impacto financeiro. |
| 12 | Aluno reclama | Reclamacoes, Inbox, Caso operacional | Resolvido; automacoes relacionadas pausam. |
| 13 | Agente falha | Execucao, Incidentes, Operacao | Resolvido; cria incidente/tarefa ou reprocessa se seguro. |
| 14 | Cota chega a 90% | Uso/cotas, Hoje, Agentes | Resolvido; modo economia converte baixa prioridade em tarefa/aprovacao. |
| 15 | Cota chega a 100% | Uso/cotas, Hoje, Agentes | Resolvido; automacao paga bloqueia e CRM manual segue. |
| 16 | Dado duplicado bloqueia fluxo | Qualidade de dados, Contatos, Operacao | Resolvido; baixa confianca vira revisao. |
| 17 | Professor/sala fica indisponivel | Recursos, Agenda, Operacao | Resolvido; simula impacto e gera tarefa/caso/aviso aprovado. |
| 18 | LGPD/opt-out/acesso suporte | Privacidade, Suporte grants, Auditoria | Resolvido; identidade, escopo, prazo e auditoria obrigatorios. |
| 19 | Comunicados em massa precisam aprovacao | Segmentos, Comunicados, Aprovacoes | Resolvido; publico, consentimento, custo e falhas visiveis. |
| 20 | Gestor fecha o dia | Hoje, Checklist, Relatorios resumidos | Resolvido; pendencias viram tarefas/casos. |
| 21 | Importa base inicial | Importacao, Qualidade de dados, Alunos | Resolvido; divergencia nao sobrescreve dado sensivel. |
| 22 | Opera uma semana com 0 agentes | Hoje, Inbox, Agenda, Financeiro, Vendas | Resolvido; CRM continua manual. |
| 23 | Muda politica de reposicao/cobranca | Politicas, Agenda, Financeiro | Resolvido com simulacao/aprovacao; detalhes finais D020/D021. |
| 24 | WhatsApp/integracao critica cai | Integracoes, Inbox, Operacao, Incidentes | Resolvido; falha vira estado/caso/tarefa. |
| 25 | Suporte Taliya acessa conta | Privacidade, Suporte grants, Internal | Resolvido com grant escopado; escopo final D035. |
| 26 | Gestor revisa qualidade de agente | Relatorios agentes, Execucoes, Incidentes | Resolvido; thresholds finais D032. |
| 27 | Compara manual vs copiloto vs autonomo | Relatorios, Agentes, Execucoes | Resolvido em v0.1; metricas finais na Rodada 10. |
| 28 | Mensagem automatica precisa pausar por opt-out | Inbox, Contatos, Comunicados, Agentes | Resolvido; opt-out restritivo vence. |

## Achados por modo

| Modo | Achado |
| --- | --- |
| Manual | Caminhos criticos existem em todas as areas. |
| Copiloto | Sugestoes aparecem onde reduzem trabalho sem esconder decisao. |
| Autonomo | Funciona apenas onde politica, cota, consentimento, permissao e risco permitem. |
| 0 agentes | Produto continua sendo CRM completo; agentes viram upgrade/preview/configuracao. |

## Bloqueios conscientes para 100%

| Bloqueio | Decisao |
| --- | --- |
| Prioridade do Hoje e formulas | D013, D021, D029 |
| Regras sensiveis de historico/privacidade | D006, D007, D016, D017, D031 |
| Pre-matricula/contratos | D025, D028 |
| Autonomia e reprocessamento | D032, D033, D034 |
| Suporte interno Taliya | D035 |

## Criterio de aceite da Rodada 9

Rodada 9 esta pronta para v0.1 porque nenhuma simulacao terminou em vazio ou sumico. Toda simulacao terminou em um destes resultados:

- resolvido;
- tarefa criada;
- aprovacao criada;
- caso criado;
- bloqueado com explicacao;
- decisao aberta registrada.
