# Design System Web - Rodada 4.1A - Hoje 04 Historico De Hoje Aprovado

> Status: imagem aprovada v0.1. Esta documentacao registra a quarta imagem da pagina Hoje, mostrando a area abaixo da dobra com o container `Historico de hoje`.

## Arquivo

Arquivo aprovado:

`20_round-4.1A_hoje_04_historico-de-hoje.png`

Arquivos locais observados:

- `D:\Downloads\20_round-4.1A_hoje_04_historico-de-hoje.png.png`
- `D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\20_round-4.1A_hoje_04_historico-de-hoje.png.png`

Observacao: os arquivos locais estao com extensao duplicada `.png.png`. O nome canonico nos documentos deve ser `20_round-4.1A_hoje_04_historico-de-hoje.png`.

## Objetivo Da Imagem

Mostrar o que existe abaixo da dobra da pagina **Hoje** sem duplicar os blocos de acao da primeira dobra.

A imagem valida que a pagina Hoje tem uma segunda camada util:

- nao e novo dashboard;
- nao e relatorio semanal;
- nao repete fila, bloqueios, tarefas, aprovacoes ou dinheiro;
- mostra memoria operacional do dia;
- ajuda o gestor a entender o que ja foi resolvido, alterado, executado ou decidido.

## Estado Representado

A pagina esta levemente rolada para baixo.

A primeira dobra ainda aparece parcialmente para manter contexto, mas o foco e um container principal de largura quase total:

`Historico de hoje`

Subtexto esperado:

`O que ja foi resolvido, alterado ou executado hoje.`

## Papel Do Historico De Hoje

O historico responde uma pergunta diferente dos blocos de acao:

```text
O que ja aconteceu hoje?
```

Os blocos acima da dobra respondem:

```text
O que ainda precisa de acao hoje?
```

Essa separacao evita duplicacao e mantem a pagina clara.

## Conteudo Do Container

O container deve funcionar como timeline/lista cronologica do dia.

Cada item deve conter:

- horario;
- icone/tipo;
- titulo;
- origem;
- ator/responsavel;
- resultado;
- chevron ou atalho discreto para abrir origem.

Exemplos adequados:

| Horario | Evento | Origem | Ator |
| --- | --- | --- | --- |
| 09:12 | Reposicao confirmada | Agenda / Reposicoes | Mariana |
| 09:28 | Conversa resolvida | WhatsApp | Atendimento |
| 10:04 | Chamada concluida | Aulas / Chamada | Rafael |
| 10:30 | Comprovante validado | Financeiro | Lucas |
| 11:05 | Aprovacao concluida | Aprovacoes | Juliana |
| 11:22 | Automacao executada | Agente Agenda | Sistema |
| 11:40 | Tarefa reagendada | Tarefas | Juliana |
| 12:10 | Bloqueio resolvido | Dados / Alunos | Recepcao |

## Regras Funcionais

- Historico nao cria pendencia nova.
- Historico nao mostra acoes de resolucao primarias.
- Historico nao deve competir visualmente com os blocos de cima.
- Cada linha deve abrir a origem correspondente.
- Eventos sensiveis devem respeitar permissao do usuario.
- Eventos de agente devem mostrar origem `Sistema`, `Agente` ou fluxo quando aplicavel.
- Eventos auditaveis devem preservar ator, horario e origem.

## Relacao Com Planos E Agentes

| Contexto | Comportamento |
| --- | --- |
| 0 agentes | Historico mostra acoes manuais, regras programaticas e eventos do CRM. |
| 1 agente | Historico mostra eventos do agente ativo quando ele cobrir o dominio. |
| 3 agentes | Historico mostra eventos dos dominios ativos do bundle. |
| 7 agentes | Historico pode mostrar eventos de todos os dominios, respeitando permissao. |
| Manual | Registra usuario, horario, origem e resultado. |
| Programatico | Registra regra do CRM e objeto afetado. |
| Copiloto | Registra sugestao usada ou decisao humana assistida. |
| Autonomo | Registra execucao, cota/custo se aplicavel, politica e resultado. |

## O Que Nao Deve Entrar

- resumo semanal;
- graficos;
- KPIs soltos;
- lista completa de tarefas;
- fila humana repetida;
- bloqueios repetidos;
- dinheiro repetido;
- aprovacoes pendentes;
- console de agentes;
- relatorio operacional profundo.

Se o usuario quiser aprofundar, deve abrir a origem do evento ou paginas como Operacao, Relatorios, Tarefas, Financeiro, Agenda ou Agentes.

## Fontes Relacionadas

- `design-system-round-4-1A-hoje-image-plan.pt-BR.md`
- `hoje-actionable-item-taxonomy.pt-BR.md`
- `drawer-lifecycle-contracts.pt-BR.md`
- `audit-touchpoints.pt-BR.md`
- `source-of-truth-matrix.pt-BR.md`
