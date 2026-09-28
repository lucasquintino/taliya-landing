# Catalogo final de prompts por superficie - PT-BR

> Status: catalogo v0.1. Cada linha define o prompt funcional minimo para gerar a tela sem inventar produto.

## Prompt base obrigatorio

```text
Gere a tela do Taliya usando as referencias visuais aprovadas de CRM por jornada.
Use somente os contratos funcionais fornecidos.
Nao invente regra, campo, permissao, cota, agente, fluxo ou autonomia.
Mostre o caminho manual, o estado sem agente e o estado bloqueado por plano quando aplicavel.
Se houver IA, mostre modo manual/copiloto/autonomo, cota, permissao, auditoria e fallback.
```

## Prompts por superficie

| Superficie | Prompt especifico |
| --- | --- |
| Onboarding e configuracao inicial | Gere fluxo de setup com escolha de preset, importacao, equipe, agentes inclusos e revisao final. |
| Hoje | Gere mesa de comando com prioridades, aulas, dinheiro, tarefas, riscos, cotas e bloqueios. |
| Inbox e conversas | Gere workspace de atendimento com lista, conversa, painel de contexto, sugestao e handoff. |
| Contatos | Gere tela herdada/simples de contatos com telefone compartilhado, vinculos operacionais, preferencias e validacao. Nao criar modulo proprio de responsaveis/familia/consentimentos no MVP. |
| Qualidade de dados | Gere fila de saneamento com duplicidades, dados ausentes, bloqueios e sugestoes revisaveis. |
| Alunos e perfil | Gere perfil CRM do aluno com plano, agenda, pagamentos, riscos e acoes rapidas. |
| Historico do aluno | Gere timeline sensivel com documentos, anamnese, permissoes e resumo permitido. |
| Professor e notas | Gere tela de professor com aulas, contexto permitido, notas pendentes e handoff. |
| Agenda | Gere calendario operacional com filtros, conflitos, capacidade e atalhos para aula/turma. |
| Grade, turmas e eventos | Gere configuracao operacional de grade, turmas, capacidade, eventos e recursos. |
| Aula e chamada | Gere tela de chamada com presenca, falta, no-show, observacao e reposicao. |
| Reposicoes e lista de espera | Gere fila de reposicoes com creditos, vagas, candidatos, encaixe programatico e convite. |
| Interessados e vendas | Gere pipeline de vendas com etapas, origem, proxima acao, conversa e conversao. |
| Aulas experimentais | Gere agenda de experimentais com lembrete, falta, pos-aula e conversao. |
| Matriculas | Gere checklist de pre-matricula com dados, plano, contrato, pagamento e primeira aula. |
| Vendas e origens | Gere painel de origens, indicacoes, demanda reprimida e segmentos comerciais. |
| Financeiro | Gere visao financeira com previsto, recebido, atrasado, falhas e excecoes. |
| Pagamentos e cobrancas | Gere fila de pagamentos com vencimentos, links, comprovantes, conciliacao e lembretes. |
| Excecoes financeiras sensiveis | Nao gere tela propria no MVP; represente a excecao dentro de Financeiro, Movimentacoes, Aprovacoes, Tarefas, Aluno ou Operacao, com impacto, risco, permissao e auditoria. |
| Contratos e documentos financeiros | Gere documentos financeiros com status, envio, anexo, recibo e auditoria. |
| Retencao | Gere painel de risco com frequencia, inativos, primeira semana e abordagem sugerida. |
| Cancelamentos e reativacao | Gere central de cancelamento/reativacao com motivo, plano e automacao pausada. |
| Reclamacoes e casos sensiveis | Gere caso sensivel com severidade, dono, prazo, resposta e escalonamento. |
| Jornadas e operacao | Gere mapa de jornadas com casos, bloqueios, incidentes, dono e proxima acao. |
| Tarefas e operacao | Gere fila de tarefas com responsavel, prazo, origem, checklist e status. |
| Aprovacoes | Gere fila de aprovacoes com antes/depois, risco, custo/cota, mensagem e decisao. |
| Agentes e fluxos | Gere console de agentes com slots, plano, fluxos, modo, limite, simulacao e pausa. |
| Execucoes e incidentes de agentes | Gere observabilidade de execucao com ferramenta, custo, erro, incidente e reprocessamento. |
| Uso, cotas e economia | Gere painel de uso com consumo, origem, previsao, 70/90/100, pacotes e economia. |
| Relatorios e exportacoes | Gere relatorios de semana, financeiro, vendas, ocupacao, risco, agentes e exportacoes. |
| Configuracoes | Gere configuracoes por secao com teste, impacto, permissao, auditoria e salvamento. |
| Politicas operacionais | Gere tela de politicas versionadas com simulacao, aprovacao, publicacao e rollback. |
| Recursos, feriados e disponibilidade | Gere recursos e indisponibilidade com impacto, simulacao e avisos aprovados. |
| Segmentos e comunicados | Gere comunicados com publico, consentimento, template, custo, aprovacao e envio. |
| Integracoes | Gere integracoes com status, logs, falhas, teste, reprocessamento e incidente. |
| Auditoria | Gere trilha de auditoria com ator, objeto, antes/depois, filtro e permissao. |
| Privacidade e solicitacoes | Gere LGPD/grants com validacao, prazo, aprovacao, execucao e auditoria. |
| Assinatura e billing | Gere billing Taliya com plano, agentes inclusos, fatura, add-ons, pacote e falha. |

## Complemento para app mobile

Para mobile, condensar cada superficie em:

- cabecalho compacto;
- cards acionaveis;
- footer/acao primaria quando houver tarefa de campo;
- busca global;
- estados de bloqueio por plano/cota/permissao;
- atalho para web quando a configuracao for avancada.
