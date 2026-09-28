# Auditoria de cobertura mobile - PT-BR

> Status: revisao depois da lacuna de "Turmas". Esta auditoria percorre as 38 superficies mapeadas e decide como cada uma aparece no app mobile.

## Regra usada

Excluir do mobile somente o que for realmente desnecessario, perigoso ou estrutural demais para o celular.

O criterio nao e "usa pouco". O criterio e:

- se pode travar o dia, entra no app;
- se pode exigir aprovacao fora do computador, entra no app;
- se ajuda professor/recepcao/gestor durante a rotina, entra no app;
- se e configuracao essencial para ativar/operar, entra no app;
- se e configuracao estrutural profunda, fica web-first;
- se e auditoria longa ou relatorio profundo, fica web-first com resumo mobile.

## Resultado

| Superficie do CRM | Decisao mobile | Como aparece no app |
| --- | --- | --- |
| Onboarding e configuracao inicial | Completo guiado | Setup inicial pode ser feito no app; importacao grande e revisao profunda ficam web. |
| Hoje | Completo | Aba Hoje. |
| Inbox e conversas | Completo | Aba Inbox + tela Conversa. |
| Contatos | Parcial | Contato rapido a partir de conversa/aluno; sem modulo proprio de responsaveis/familia/consentimentos no MVP. |
| Qualidade de dados | Aprovacao/consulta | Tela dentro de Operacao para duplicidades e dados bloqueantes. |
| Alunos e perfil do aluno | Completo para consulta/acao | Aba Alunos + Perfil do aluno. |
| Historico do aluno | Parcial restrito | Historico permitido, notas e documentos essenciais. |
| Professor e notas | Completo para professor | Tela Professor e notas pendentes. |
| Agenda | Completo | Aba Agenda. |
| Grade, turmas e eventos | Parcial forte | Turmas, Eventos, Recursos/disponibilidade; grade estrutural fica web. |
| Aula e chamada | Completo | Aula + Chamada. |
| Reposicoes e lista de espera | Completo | Reposicoes + Lista de espera. |
| Interessados e vendas | Parcial | Interessados quentes e follow-up. |
| Aulas experimentais | Completo | Experimental do dia, faltas, remarques e pos-aula. |
| Matriculas | Consulta/aprovacao | Matricula rapida. |
| Vendas e origens | Consulta | Origens e indicacoes resumidas. |
| Financeiro | Consulta/acao | Financeiro essencial. |
| Pagamentos e cobrancas | Parcial forte | Pagamento/cobranca com acoes controladas. |
| Excecoes financeiras sensiveis | Aprovacao contextual | Sem tela propria; aparecem em Financeiro, Aprovacoes, Tarefas, Aluno ou Operacao com impacto. |
| Contratos e documentos financeiros | Consulta/acao simples | Contratos/documentos. |
| Retencao | Parcial forte | Retencao, riscos e retornos pendentes. |
| Cancelamentos e reativacao | Acao controlada | Cancelamentos e reativacao. |
| Reclamacoes e casos sensiveis | Aprovacao/acao controlada | Reclamacao/caso sensivel. |
| Jornadas e operacao | Completo para prioridade | Jornadas prioritarias e Caso operacional. |
| Tarefas e operacao | Completo | Tarefas. |
| Aprovacoes | Completo | Aprovacoes. |
| Agentes e fluxos | Configuracao essencial | Configurar agente/fluxo essencial, modo, limite e teste simples; configuracao avancada fica web. |
| Execucoes e incidentes de agentes | Alerta/consulta | Execucao de agente e incidentes. |
| Uso, cotas e economia | Consulta/acao simples | Cotas. |
| Relatorios e exportacoes | Resumo apenas | Relatorios resumidos; exportacao profunda fica web. |
| Configuracoes | Essencial no app | Studio, horario, canal, notificacoes, privacidade basica e convite simples; matriz avancada fica web. |
| Politicas operacionais | Fora como fluxo | Mostrar impacto/bloqueio; editar/versionar fica web. |
| Recursos, feriados e disponibilidade | Consulta/alerta | Recursos e disponibilidade quando afeta agenda. |
| Segmentos e comunicados | Aprovacao | Aprovar/rejeitar comunicado e ver falhas. |
| Integracoes | Status/alerta | Integracoes/status quando falha afeta rotina. |
| Auditoria | Resumo sensivel | Auditoria resumida em acoes sensiveis. |
| Privacidade e solicitacoes | Aprovacao sensivel | Privacidade/solicitacoes e acesso de suporte. |
| Assinatura e billing | Consulta/acao simples | Assinatura/billing resumido. |

## Telas adicionadas ou reforcadas nesta revisao

- Turmas;
- Eventos/workshops;
- Recursos e disponibilidade;
- Falhas de envio;
- Origens e indicacoes;
- Segmentos e comunicados;
- Excecoes financeiras sensiveis sem tela propria;
- Contratos/documentos;
- Retencao;
- Cancelamentos e reativacao;
- Qualidade de dados;
- Execucao de agente;
- Relatorios resumidos;
- Auditoria resumida;
- Privacidade/solicitacoes;
- Integracoes/status;
- Assinatura/billing.

## O que foi excluido de verdade

Excluido como fluxo principal mobile:

- importacao grande e revisao profunda de setup;
- configuracao avancada de agentes;
- simulacao profunda de fluxo;
- criacao/versionamento de politicas;
- reconfiguracao avancada de integracoes;
- auditoria longa;
- importacao/exportacao grande;
- edicao completa da matriz de permissoes da equipe;
- configuracao de canais/templates;
- relatorios profundos;
- billing completo;
- criacao de campos customizados;
- configuracao estrutural de salas/equipamentos.

Esses itens podem gerar alerta, resumo ou aprovacao no mobile. O app tambem deve fazer setup guiado e configuracao essencial; o web fica com a administracao profunda.

## Conclusao

A lacuna de Turmas era sinal de um problema maior: o app ainda estava subdimensionado.

Depois desta revisao, o app deixa de ser "consulta com algumas acoes" e vira:

```text
superficie de execucao diaria do studio.
```

O web continua sendo:

```text
superficie de configuracao avancada, governanca e revisao profunda.
```
