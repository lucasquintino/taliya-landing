# Design System Web - Rodada 4.1E - Perfil Do Aluno

> Status: aprovada v0.1. Esta documentacao registra a imagem da rota `/app/alunos/[id]`, cobrindo o perfil completo do aluno com a aba `Resumo` ativa.

## Arquivo

Arquivo aprovado:

`28_round-4.1E_aluno-perfil_01_resumo-operacional.png`

Arquivos locais observados:

- `D:\Downloads\28_round-4.1E_aluno-perfil_01_resumo-operacional.png.png`
- `D:\Downloads\28_round-4.1E_aluno-perfil_01_resumo-operacional.png (2).png`
- `D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\28_round-4.1E_aluno-perfil_01_resumo-operacional.png.png`

Nome canonico:

`28_round-4.1E_aluno-perfil_01_resumo-operacional.png`

## Decisao Central

**Perfil do aluno** responde:

```text
Quem e esse aluno, qual e o estado dele no studio e o que preciso fazer agora?
```

Esta pagina e a ficha operacional completa do aluno.

Ela nao e:

- lista de alunos;
- dashboard geral;
- agenda completa;
- financeiro completo;
- modulo de responsaveis/familia;
- cadastro juridico pesado;
- pagina de consentimentos.

## Rota Coberta

| Rota | Cobertura |
| --- | --- |
| `/app/alunos/[id]` | Coberta pela imagem 28 com aba `Resumo` ativa. |
| `/app/alunos` | Coberta pela imagem 27, nao por esta. |

## Layout Aprovado

A pagina usa:

- App Shell web aprovado;
- topbar do grupo com `Alunos`, `Contatos`, `Segmentos` e `Linha do tempo`;
- cabeçalho grande do aluno;
- abas internas;
- aba `Resumo` ativa;
- blocos operacionais no centro;
- painel lateral direito com proximas acoes, riscos, tarefas, conversa recente e botoes rapidos.

## Cabeçalho Do Aluno

Campos validados:

- avatar;
- nome `Ana Paula Martins`;
- status `Ativa`;
- plano `Plano Mensal`;
- turma principal `Reformer Iniciante`;
- telefone/WhatsApp;
- e-mail simples;
- tags de estado:
  - `pagamento pendente`;
  - `boa frequencia`;
  - `proxima aula marcada`.

Acoes no cabecalho:

- `Enviar mensagem`;
- `Criar tarefa`;
- `Registrar nota`;
- `Editar dados`.

## Abas Internas

Abas aprovadas:

- `Resumo`;
- `Agenda`;
- `Financeiro`;
- `Documentos`;
- `Historico`;
- `Tarefas`.

A imagem 28 cobre apenas a aba `Resumo`.

As demais abas herdam padroes de outras familias:

| Aba | Cobertura |
| --- | --- |
| Agenda | Herda familia Agenda/Aulas. |
| Financeiro | Herda familia Financeiro. |
| Documentos | Herda componentes de documentos/anexos. |
| Historico | Herda timeline/auditoria. |
| Tarefas | Herda pagina Tarefas. |

## Blocos Da Aba Resumo

| Bloco | Papel |
| --- | --- |
| Estado operacional | Resume presença, risco, proxima aula, plano e financeiro. |
| Agenda proxima | Mostra proximas aulas e reposicao pendente. |
| Plano e financeiro | Mostra plano, proxima mensalidade, ultimo pagamento e status financeiro. |
| Pendencias | Lista problemas acionaveis ligados ao aluno. |
| Notas recentes | Mostra observacoes internas curtas. |
| Linha do tempo curta | Mostra eventos recentes relevantes. |
| Painel lateral | Prioriza proximas acoes, riscos, tarefas abertas e ultima conversa. |

## Painel Lateral Direito

O painel lateral mostra:

- proximas acoes;
- riscos/alertas;
- tarefas abertas;
- ultima conversa;
- botoes rapidos.

Ele nao substitui:

- aba Historico completa;
- pagina Tarefas;
- Inbox/Conversas;
- Financeiro completo;
- Agenda completa.

Regra do painel lateral:

- a imagem 28 mostra a aba `Resumo` com painel lateral de proximas acoes;
- o painel lateral muda conforme aba ativa, risco do aluno e item clicado dentro do perfil;
- ele deve continuar sendo uma faixa acionavel, nao uma segunda pagina dentro do perfil;
- quando o usuario precisa profundidade, a acao abre a aba/rota canonica correspondente.

Modos principais do painel no Perfil do Aluno:

| Contexto clicado | Painel lateral deve mostrar |
| --- | --- |
| Resumo ativo | Proximas acoes, riscos, tarefas abertas, ultima conversa e botoes rapidos. |
| Pendencia selecionada | Origem, impacto, responsavel, proxima acao e link para origem canonica. |
| Tarefa selecionada | Contrato resumido de Tarefa, com acao para abrir Tarefas quando precisar profundidade. |
| Conversa selecionada | Ultima conversa permitida, status do canal, consentimento e acao para abrir Inbox. |
| Financeiro selecionado | Resumo permitido, proximo vencimento/pendencia e acao para abrir Financeiro. |
| Agenda/reposicao selecionada | Proxima aula, reposicao ou credito resumido e acao para abrir Agenda/Reposicoes. |

## Acoes Validadas

| Acao | Regra |
| --- | --- |
| `Enviar mensagem` | Abre conversa/canal do aluno. |
| `Criar tarefa` | Cria tarefa vinculada ao aluno. |
| `Registrar nota` | Adiciona nota interna ao historico do aluno. |
| `Editar dados` | Abre edicao de dados cadastrais simples. |
| `Ver agenda` | Abre aba/rota de agenda do aluno. |
| `Ver financeiro` | Abre aba/rota financeira do aluno. |
| `Ver todas tarefas` | Abre tarefas filtradas por aluno. |
| `Ver todas conversas` | Abre conversas filtradas por aluno. |
| `Alterar plano` | Acao sensivel; deve abrir fluxo com impacto financeiro, nao editar direto. |
| `Pausar aluno` | Acao sensivel; deve exigir confirmacao e motivo. |

## Pendencia Versus Tarefa

A imagem mostra `Pendencias` no centro e `Tarefas abertas` no painel lateral.

Regra aprovada:

- **Pendencia** e um problema, alerta ou necessidade detectada.
- **Tarefa** e trabalho humano criado com dono, prazo e status.

Uma pendencia pode virar tarefa quando precisar de acompanhamento separado.

Nem toda pendencia ja e tarefa.

## Escopo Removido

Conforme `alunos-scope-decision.pt-BR.md`, esta pagina nao deve incluir:

- responsaveis/familia;
- relacoes familiares;
- permissoes familiares;
- consentimentos como secao;
- perfil de responsavel.

Pode haver apenas campos simples de contato:

- telefone/WhatsApp;
- e-mail;
- contato de emergencia, se necessario.

## Estados Cobertos

- aluno ativo;
- pagamento pendente;
- boa frequencia;
- proxima aula marcada;
- reposicao pendente;
- tarefas abertas;
- risco/alerta financeiro;
- ultima conversa por WhatsApp.

Estados futuros nao representados, mas esperados:

- aluno em risco;
- aluno pausado;
- aluno inativo;
- aluno sem turma;
- aluno experimental;
- financeiro em atraso critico;
- documento pendente;
- dados incompletos.

## Planos E Modos

| Plano/modo | Comportamento |
| --- | --- |
| 0 agentes | Perfil completo funciona manualmente com agenda, financeiro, documentos, notas, tarefas e historico. |
| 1 agente | Sugestoes aparecem apenas nos dominios cobertos pelo agente ativo. |
| 3 agentes | Dominios ativos podem sugerir proxima acao, mensagem, tarefa ou alerta. |
| 7 agentes | Todos os dominios podem apoiar triagem, respeitando cota, permissao, risco e auditoria. |
| Manual | Usuario envia mensagem, cria tarefa, registra nota, edita dados, altera plano e pausa aluno. |
| Copiloto | Pode resumir historico permitido, sugerir proxima acao, texto e tarefa. |
| Autonomo | Nao altera plano, pausa aluno ou muda dados sensiveis sozinho. |

## O Que Nao Deve Aparecer

- responsaveis/familia;
- consentimentos como secao;
- permissoes familiares;
- dashboard geral;
- kanban;
- calendario grande;
- financeiro detalhado completo;
- historico completo expandido;
- agente como decisor principal.

## Referencias

- `alunos-scope-decision.pt-BR.md`
- `design-system-round-4-1E-alunos-lista-approved.pt-BR.md`
- `design-system-round-4-0-web-page-blueprints.pt-BR.md`
- `design-system-round-4-image-coverage-strategy.pt-BR.md`
- `drawer-lifecycle-contracts.pt-BR.md`
