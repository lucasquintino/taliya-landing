# Design System Web - Rodada 3B.3 - Visualizacoes Operacionais

> Status: biblioteca visual v0.1 aprovada. Esta rodada documenta visualizacoes operacionais para listas, tabelas, kanban, calendario, historico e atividade.

## Objetivo

Definir os componentes de visualizacao que sustentam o CRM no dia a dia.

Esta rodada cobre:

- tabela completa;
- lista densa;
- kanban compacto;
- calendario compacto;
- timeline/historico;
- painel de atividade;
- cards de resumo operacional.

## Decisao

A imagem da Rodada 3B.3 fica aprovada como v0.1.

Ela acertou:

- trouxe densidade real de CRM operacional;
- usou filtros e busca alinhados a 3B.1;
- criou tabela completa com status, prioridade, responsavel e paginacao;
- kanban ficou compacto e plausivel;
- calendario ficou util sem virar tela final;
- timeline e atividade ficaram legiveis;
- cards de resumo ficaram coerentes com o sistema.

## Ressalvas

- A prancha e mais densa que as anteriores; em telas reais sera preciso hierarquia forte.
- A tabela usa muitas cores de status; essas cores devem ser micro acentos, nao nova paleta dominante.
- Kanban e calendario precisam herdar cinza frio e baixo contraste em paginas reais.
- Cards de resumo nao devem transformar o CRM em dashboard generico.
- Graficos e numeros devem ficar proximos de decisoes operacionais, nao decorativos.

## Regras De Uso

- Tabela completa e a base para listas administrativas e operacionais.
- Lista densa serve para atividade recente, conversas, tarefas e eventos curtos.
- Kanban serve para pipeline, casos, tarefas e oportunidades quando a mudanca de status for central.
- Calendario compacto serve para contexto; calendario completo entra em paginas de agenda.
- Timeline serve para historico auditavel e leitura de contexto.
- Painel de atividade deve ser filtravel e escaneavel.

## Nao Fazer

- Nao usar todos os componentes juntos em uma tela sem prioridade.
- Nao deixar status depender apenas de cor.
- Nao criar graficos grandes se a tarefa do usuario e operar lista, agenda ou caso.
- Nao usar kanban quando tabela resolve melhor.
- Nao transformar calendario compacto em tela de agenda completa nesta camada.

