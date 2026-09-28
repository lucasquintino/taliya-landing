# Design System Web - Rodada 4.1A - Hoje 02 Drawer De Tarefa Aprovado

> Status: imagem aprovada v0.1. Esta documentacao registra a segunda imagem da pagina Hoje, mostrando o drawer de uma tarefa humana aberta a partir do bloco `Tarefas de hoje`.

## Arquivo

Arquivo aprovado:

`18_round-4.1A_hoje_02_drawer-tarefa.png`

Arquivo local observado:

`D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\18_round-4.1A_hoje_02_drawer-tarefa.png.png`

Observacao: o arquivo local esta com extensao duplicada `.png.png`. O nome canonico de referencia nos documentos deve ser `18_round-4.1A_hoje_02_drawer-tarefa.png`.

## Objetivo Da Imagem

Mostrar o comportamento da pagina **Hoje** quando o gestor clica em uma tarefa real.

A imagem valida que:

- Hoje continua visivel ao fundo;
- o item selecionado fica destacado;
- o detalhe abre em drawer lateral direito;
- o drawer representa uma **tarefa humana**, nao aprovacao, bloqueio, financeiro ou fila humana;
- as acoes ficam no drawer, nao nos cards da pagina;
- a tarefa tem origem canonica, prazo, responsavel, impacto e proxima acao.

## Estado Representado

Item selecionado:

`Confirmar reposicao com Ana Paula`

Bloco de origem visual:

`Tarefas de hoje`

Tipo real:

`Tarefa`

Origem canonica:

`Agenda / Reposicoes`

Motivo para aparecer no Hoje:

- prazo hoje;
- exige contato humano;
- impacta reposicao aguardando confirmacao;
- tem responsavel e acao concreta.

## Conteudo Do Drawer

O drawer aprovado contem:

- etiqueta de tipo: `Tarefa`;
- titulo: `Confirmar reposicao com Ana Paula`;
- status: `Pendente`;
- prioridade: `Alta`;
- prazo: `Hoje, 10:30`;
- responsavel: `Mariana`;
- origem: `Agenda / Reposicoes`;
- objeto afetado: `Reposicao - Ana Paula Martins`;
- descricao;
- impacto;
- sugestao de horario;
- canal sugerido;
- origem de criacao: `Criada por regra do CRM as 09:12`;
- checklist;
- ultima atividade;
- comentario recente;
- acoes principais.

## Acoes Aprovadas

| Acao | Comportamento esperado |
| --- | --- |
| Abrir conversa | Abre a conversa da aluna/responsavel para confirmar o horario. |
| Concluir | Abre conclusao estruturada. Nao deve apenas fechar a tarefa sem resultado. |
| Reagendar | Altera o prazo da tarefa/follow-up. |
| Delegar | Troca responsavel ou fila. |
| Abrir origem | Abre a reposicao em Agenda / Reposicoes. |

## Resultados Possiveis Ao Concluir

O botao `Concluir` deve abrir opcoes estruturadas, como:

| Resultado | Efeito |
| --- | --- |
| Aceitou horario | Tarefa concluida; reposicao confirmada/reservada na origem. |
| Recusou horario | Tarefa concluida; reposicao volta para buscar nova opcao. |
| Sem resposta | Tarefa nao conclui como sucesso; deve reagendar ou criar follow-up. |
| Horario indisponivel | Tarefa vira bloqueio de agenda ou caso operacional. |
| Contato invalido | Tarefa cria problema de dados ou tarefa de correcao. |

## Criacao Da Tarefa

A imagem usa a origem:

`Criada por regra do CRM as 09:12`

Isso comunica que a tarefa pode existir sem agente de IA, mantendo suporte ao plano **0 agentes**.

Outras criacoes possiveis, cobertas pelo contrato de ciclos:

- manual;
- a partir da origem;
- programatica;
- sugerida por copiloto;
- criada por autonomia segura;
- criada por fallback de cota, politica, consentimento ou integracao;
- criada como tarefa filha de caso operacional.

## Relacao Com Planos E Modos

| Contexto | Comportamento |
| --- | --- |
| 0 agentes | CRM cria por regra ou usuario cria manualmente; tarefa e resolvida por pessoa. |
| 1 agente | Agente so atua se o slot configurado cobrir Agenda/Reposicoes ou dominio relacionado. |
| 3 agentes | Se Agenda estiver ativo no bundle, copiloto pode sugerir horario e mensagem. |
| 7 agentes | Agente pode sugerir e, se permitido, executar acoes seguras dentro de politica/cota. |
| Manual | Usuario abre conversa, confirma, conclui, reagenda ou delega. |
| Copiloto | Agente sugere texto, resumo, horario e resultado. Humano confirma. |
| Autonomo | So cria ou conclui automaticamente se houver politica segura, consentimento, cota e evidencia objetiva. |

## O Que Esta Correto Na Imagem

- Drawer lateral direito, sem modal central.
- Item selecionado destacado no bloco correto.
- Tipo `Tarefa` explicito.
- Origem canonica clara.
- Acao principal alinhada ao trabalho real: `Abrir conversa`.
- `Concluir` com indicacao de opcoes.
- Tarefa criada por regra do CRM, deixando claro que nao depende de IA.
- Pagina Hoje permanece como mesa de comando, nao vira tela de detalhe.

## Cuidados Para Implementacao

- Nao usar este drawer como modelo universal para todos os itens do Hoje.
- Nao transformar aprovacao, bloqueio, financeiro, fila humana, aula ou checklist em tarefa por padrao.
- Nao colocar acoes dentro dos cards da pagina Hoje.
- Manter drawer por tipo conforme `drawer-lifecycle-contracts.pt-BR.md`.
- Sempre preservar origem canonica e resultado estruturado.

## Fontes Relacionadas

- `hoje-actionable-item-taxonomy.pt-BR.md`
- `drawer-lifecycle-contracts.pt-BR.md`
- `design-system-round-4-1A-hoje-image-plan.pt-BR.md`
- `route-agent-mode-entitlement-matrix.pt-BR.md`
