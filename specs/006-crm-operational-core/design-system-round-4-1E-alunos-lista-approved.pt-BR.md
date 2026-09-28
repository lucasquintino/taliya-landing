# Design System Web - Rodada 4.1E - Alunos Lista

> Status: aprovada v0.1. Esta documentacao registra a imagem da rota `/app/alunos`, cobrindo lista de alunos com resumo lateral acionavel.

## Arquivo

Arquivo aprovado:

`27_round-4.1E_alunos_01_lista-perfil-resumido.png`

Arquivos locais observados:

- `D:\Downloads\27_round-4.1E_alunos_01_lista-perfil-resumido.png.png`

Nome canonico:

`27_round-4.1E_alunos_01_lista-perfil-resumido.png`

## Decisao Central

**Alunos** responde:

```text
Como encontro um aluno, entendo seu estado operacional e tomo uma acao rapida sem abrir o perfil completo?
```

Esta pagina e a central operacional da base de alunos.

Ela nao e:

- dashboard;
- agenda;
- pagina de vendas;
- perfil completo;
- financeiro completo;
- historico completo.

## Rota Coberta

| Rota | Cobertura |
| --- | --- |
| `/app/alunos` | Coberta pela imagem 27. |
| `/app/alunos/[id]` | Nao coberta. Precisa imagem propria de perfil completo. |

## Layout Aprovado

A pagina usa:

- App Shell web aprovado;
- topbar do grupo com `Alunos`, `Contatos`, `Segmentos` e `Linha do tempo`;
- `Alunos` ativo;
- titulo `Alunos`;
- subtitulo `Base ativa do estudio`;
- busca e filtros por status, plano, turma, risco e responsavel;
- botao principal `Novo aluno`;
- coluna esquerda com segmentos;
- lista central de alunos;
- painel direito com resumo acionavel do aluno selecionado.

## Blocos Validados

| Bloco | Papel |
| --- | --- |
| Filtros superiores | Encontrar aluno por busca, status, plano, turma, risco e responsavel. |
| Segmentos laterais | Separar Todos, Ativos, Em risco, Pendencias, Sem turma, Financeiro pendente, Consentimento pendente e Inativos. |
| Lista central | Mostrar alunos com status operacional suficiente para triagem. |
| Painel direito | Mostrar resumo rapido do aluno selecionado e acoes imediatas. |
| Paginacao | Suportar base grande sem transformar a tela em dashboard. |

## Conteudo Minimo Da Lista

Cada linha deve mostrar:

- aluno;
- status;
- plano;
- turma atual;
- responsavel;
- presenca;
- financeiro;
- risco;
- ultima atividade.

Exemplos validados na imagem:

- `Ana Paula Martins`;
- `Joao Pedro Silva`;
- `Carla Mendes`;
- `Pedro Henrique`;
- `Juliana Rocha`;
- `Mariana Costa`;
- `Lucas Oliveira`;
- `Fernanda Souza`;
- `Gabriel Santos`;
- `Patricia Lima`.

## Painel Direito

O painel direito e um resumo acionavel, nao um perfil completo.

Na imagem aprovada, o exemplo e:

`Ana Paula Martins`

Campos validados:

- avatar;
- nome;
- status;
- plano atual;
- turma atual;
- responsavel principal;
- WhatsApp/telefone;
- status simples de canal/WhatsApp, quando necessario;
- proximas 2 aulas;
- financeiro resumido;
- presenca recente;
- pendencias abertas;
- acoes rapidas.

Regra do painel direito:

- por padrao, `/app/alunos` pode carregar sem aluno selecionado;
- a imagem 27 mostra um aluno selecionado para documentar o resumo acionavel;
- o painel direito muda conforme o aluno clicado e seu estado operacional;
- o painel nao vira perfil completo e nao deve carregar historico, financeiro ou agenda completos.

Modos principais do painel de Aluno:

| Item clicado | Painel direito deve mostrar |
| --- | --- |
| Aluno ativo sem risco | Plano, turma, proximas aulas, contato principal, presenca recente e acoes rapidas. |
| Aluno com pendencia financeira | Financeiro resumido, impacto operacional, link para Financeiro e acoes seguras de mensagem/tarefa. |
| Aluno com reposicao pendente | Direito/credito resumido, proxima aula, link para Reposicoes e acao de criar tarefa ou mensagem. |
| Aluno com dados incompletos | Campos faltantes, origem do problema, acao de atualizar dados e cuidado com automacao. |
| Aluno pausado/inativo | Motivo, data, regras de retorno, ultimas interacoes e acoes restritas. |
| Aluno com risco/alerta | Motivo do risco, impacto, origem canonica e proxima acao segura. |

## Acoes Validadas

| Acao | Regra |
| --- | --- |
| `Abrir perfil` | Acao principal. Leva para `/app/alunos/[id]`. |
| `Enviar mensagem` | Abre conversa/canal respeitando status do canal e politica de envio. |
| `Criar tarefa` | Cria trabalho humano vinculado ao aluno. |
| `Registrar nota` | Registra observacao interna no historico do aluno. |
| `Atualizar dados` | Abre edicao/correcao de dados cadastrais. |

## Relacao Com Perfil Completo

Esta imagem nao substitui a rota `/app/alunos/[id]`.

O painel lateral deve responder apenas:

```text
Quem e esse aluno, existe algum risco e qual acao rapida posso tomar agora?
```

Detalhes profundos ficam no perfil completo:

- historico completo;
- documentos;
- contratos;
- agenda detalhada;
- financeiro completo;
- responsaveis/familia;
- consentimentos como secao propria;
- permissoes;
- timeline;
- tarefas e conversas relacionadas.

## Relacao Com Outras Paginas

| Superficie | Papel |
| --- | --- |
| Alunos | Encontrar, filtrar e agir rapidamente sobre alunos. |
| Perfil do aluno | Consultar e editar a ficha completa. |
| Contatos | Gerenciar contatos simples, incompletos, duplicados ou vindos de conversa. |
| Segmentos | Criar agrupamentos para comunicados, filtros e operacao. |
| Linha do tempo | Consultar eventos historicos da base/aluno. |
| Hoje | Mostra alunos apenas quando viram prioridade do dia. |
| Tarefas | Guarda trabalho humano vinculado ao aluno. |
| Inbox | Guarda conversas e mensagens do aluno/responsavel. |
| Financeiro | Guarda cobrancas, pagamentos e contratos financeiros. |

## Estados Cobertos

- Ativa;
- Ativo;
- Em risco;
- Sem turma;
- Inativa;
- financeiro OK;
- pagamento pendente;
- aguardando matricula;
- risco baixo;
- risco medio;
- risco alto;
- WhatsApp permitido ou bloqueado, quando necessario para envio.

Estados futuros nao representados, mas esperados:

- dados incompletos;
- duplicidade;
- WhatsApp bloqueado;
- responsavel conflitante;
- contrato pendente;
- aluno bloqueado;
- aluno arquivado;
- aluno reativado.

## Planos E Modos

| Plano/modo | Comportamento |
| --- | --- |
| 0 agentes | Lista, filtros, perfil resumido e acoes manuais funcionam normalmente. |
| 1 agente | Sugestoes aparecem apenas se o agente ativo cobrir o dominio relacionado. |
| 3 agentes | Dominios ativos podem sugerir risco, proxima acao, mensagem ou tarefa. |
| 7 agentes | Todos os dominios podem apoiar triagem, respeitando cota, permissao, risco e auditoria. |
| Manual | Usuario filtra, abre perfil, envia mensagem, cria tarefa, registra nota e atualiza dados. |
| Copiloto | Pode resumir aluno, explicar risco, sugerir mensagem ou proxima acao. |
| Autonomo | Nao altera dados sensiveis sozinho; pode criar lembretes/tarefas seguras quando permitido. |

## Observacao De Conteudo

Na imagem aprovada, a linha de `Ana Paula Martins` mostra financeiro `OK`, enquanto o painel direito mostra `pagamento pendente`.

Isso e uma inconsistencia de conteudo da imagem, nao de layout.

Regra de produto:

- lista e painel devem sempre usar a mesma fonte de verdade;
- se o painel mostrar `pagamento pendente`, a linha deve refletir o mesmo estado ou indicar que ha uma pendencia financeira.

## O Que Nao Deve Aparecer

- dashboard de KPIs;
- kanban;
- calendario grande;
- perfil completo dentro do painel direito;
- responsaveis/familia;
- consentimentos como modulo ou aba;
- historico profundo;
- documentos detalhados;
- vendas como foco principal;
- agente como acao principal.

## Referencias

- `design-system-round-4-0-web-page-blueprints.pt-BR.md`
- `design-system-round-4-image-coverage-strategy.pt-BR.md`
- `canonical-data-model.pt-BR.md`
- `drawer-lifecycle-contracts.pt-BR.md`
