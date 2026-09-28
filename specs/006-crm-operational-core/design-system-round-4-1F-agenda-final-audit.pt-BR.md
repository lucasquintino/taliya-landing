# Auditoria Final - Rodada 4.1F - Agenda, Turmas, Grade, Aula E Reposicoes

> Status: auditoria v0.1 apos imagens aprovadas 26, 29, 31, 35 e 36. Objetivo: fechar a cobertura web da familia Agenda / Aulas / Reposicoes, registrar herancas visuais e separar claramente Grade, Turmas, Agenda e Aula.

## Imagens Aprovadas

| Imagem | Rota/superficie | Papel | Status |
| --- | --- | --- | --- |
| `26_round-4.1F_agenda_01_calendario-operacional.png` | `/app/agenda` | Calendario operacional de aulas reais por dia/semana. | Aprovada |
| `35_round-4.1F_turmas_01_lista-detalhe.png` | `/app/turmas` | Lista/workspace de turmas recorrentes e detalhe lateral. | Aprovada |
| `36_round-4.1F_grade_01_semana-modelo-bloqueio.png` | `/app/grade` | Semana-modelo recorrente com blocos que geram aulas futuras. | Aprovada com ressalva funcional |
| `29_round-4.1F_aula_01_detalhe-com-chamada.png` | `/app/aulas/[id]` | Detalhe de aula concreta com drawer de chamada. | Aprovada |
| `31_round-4.1F_reposicoes_01_fluxo-encaixe.png` | `/app/reposicoes` | Fila de reposicoes, direito/credito, encaixe e detalhe lateral. | Aprovada |

## Diferenca Entre As Superficies

| Superficie | Pergunta que responde | Nao deve virar |
| --- | --- | --- |
| Grade | Como o studio funciona toda semana? | Agenda real, pagina de bloqueios ou dashboard. |
| Turmas | Quem esta em cada turma recorrente e onde ha vaga fixa? | Aula concreta, chamada ou perfil de aluno. |
| Agenda | O que acontece em datas reais hoje/esta semana? | Configuracao estrutural completa de grade/turmas. |
| Aula | O que aconteceu ou precisa acontecer nesta aula concreta? | Turma recorrente ou calendario inteiro. |
| Reposicoes | Quem precisa repor e qual encaixe seguro resolve? | Lista de espera geral, creditos isolados ou dashboard de ocupacao. |

Regra central:

**Grade define o padrao. Bloqueio cria excecao. Agenda mostra o efeito real. Aula registra a execucao.**

## Cobertura De Rotas

| Rota | Cobertura | Decisao |
| --- | --- | --- |
| `/app/agenda` | Imagem 26 | Coberta. |
| `/app/turmas` | Imagem 35 | Coberta. |
| `/app/turmas/[id]` | Herda imagem 35 | Sem imagem propria; rota direta expande o mesmo detalhe/painel. |
| `/app/grade` | Imagem 36 | Coberta com ressalva: foco e turmas recorrentes, nao bloqueios. |
| `/app/eventos` | Herda Turmas + Agenda | Sem imagem propria nesta rodada. |
| `/app/eventos/[eventId]` | Herda Turma/Aula | Sem imagem propria nesta rodada. |
| `/app/aulas/[id]` | Imagem 29 | Coberta. |
| `/app/aulas/[id]/chamada` | Nao e pagina principal | Chamada abre como painel/drawer contextual dentro da aula. |
| `/app/reposicoes` | Imagem 31 | Coberta. |
| `/app/creditos-reposicao` | Nao e pagina principal | Credito aparece dentro do fluxo de reposicao. |
| `/app/lista-espera` | Fora desta rodada | Lista de espera geral e superficie futura/separada. |
| `/app/recursos` e `/app/recursos/[resourceId]` | Nao entram como paginas principais | Recurso/sala/equipamento e opcional; catalogo futuro pode morar em Configuracoes. |

## Bloqueios, Feriados E Indisponibilidade

Bloqueio de agenda e um **objeto situacional**, nao uma pagina principal.

Tipos cobertos:

- feriado;
- recesso;
- fechamento pontual;
- professor indisponivel;
- horario bloqueado;
- sala/equipamento/recurso indisponivel, quando o studio usa esse controle.

Onde pode iniciar:

- Agenda, ao selecionar aula, horario ou conflito;
- Grade, por menu/contexto de bloco recorrente;
- Turma, quando afeta uma turma especifica;
- Aula, quando a indisponibilidade aparece na execucao.

Ressalva da imagem 36:

- a imagem mostra `Criar bloqueio` e bloqueio aplicado;
- na implementacao, isso deve ser tratado como acao secundaria/situacional;
- `Criar turma`, `Editar bloco` e `Simular impacto` continuam sendo acoes mais centrais da Grade.

Compensacao no drawer:

- bloqueio nao gera credito automaticamente sempre;
- o drawer do bloqueio deve mostrar a politica aplicada e a consequencia prevista antes de publicar;
- controles esperados: `Seguir politica do studio`, `Gerar credito de reposicao`, `Nao gerar credito` e `Revisar aluno por aluno`;
- creditos criados por bloqueio nascem com origem `Bloqueio de agenda` e aparecem em `/app/reposicoes`;
- Grade nao vira pagina de Reposicoes; o drawer decide a consequencia, e Reposicoes acompanha o credito/pedido depois.

## Ciclos Coerentes

### Turma recorrente

1. Usuario cria ou edita turma em `/app/turmas` ou `/app/grade`.
2. Grade/turma define dia, horario, capacidade, alunos fixos e professor/recurso opcionais.
3. Agenda gera aulas reais futuras.
4. Aula concreta registra chamada, presenca, falta, no-show, reposicao e observacoes.

### Bloqueio pontual

1. Grade tem turma recorrente, por exemplo sexta 17h.
2. Usuario cria bloqueio para uma sexta especifica.
3. A turma recorrente continua existindo.
4. A aula real daquela data fica bloqueada/cancelada/requer acao na Agenda.
5. Sistema mostra impacto e permite aviso, tarefa ou compensacao conforme politica.
6. No drawer, usuario segue a politica, gera credito, nao gera credito ou revisa aluno por aluno.
7. Se gerar credito, o credito aparece em `/app/reposicoes`.

### Bloqueio temporario

1. Grade tem turma recorrente, por exemplo sexta 17h.
2. Usuario cria bloqueio de ferias por duas semanas.
3. A turma recorrente continua existindo.
4. As aulas reais dentro do periodo ficam afetadas.
5. O drawer mostra aulas e alunos afetados, com compensacao prevista.
6. Usuario publica o bloqueio com a consequencia escolhida.
7. Ao fim do periodo, a recorrencia volta a gerar aulas normalmente.

### Reposicao

1. Falta/pedido gera direito ou pedido de reposicao conforme politica.
2. `/app/reposicoes` mostra validade, origem, preferencia e status.
3. Sistema calcula opcoes programaticamente.
4. Copiloto pode explicar e redigir convite.
5. Autonomo so age se politica, consentimento, cota, template e risco permitirem.
6. Aula de destino registra uso da reposicao.

## Manual, Copiloto E Autonomo

| Modo | Garantia nesta familia |
| --- | --- |
| 0 agentes | Agenda, Grade, Turmas, Aula, Chamada e Reposicoes continuam operaveis manualmente e por regras programaticas. |
| Manual | Usuario cria turma, edita grade, faz chamada, cria bloqueio, escolhe encaixe e envia aviso. |
| Programatico | CRM calcula aulas geradas, vagas, capacidade, impacto de bloqueio, candidatos de reposicao e estados. |
| Copiloto | Resume impacto, explica conflito, sugere encaixe, redige aviso ou convite. |
| Autonomo | Apenas envia avisos/convites ou cria tarefas seguras quando politica, consentimento, cota, template e risco permitirem. Nao altera grade, chamada ou decisao sensivel sozinho. |

## Paineis E Drawers

Todas as imagens com painel aberto representam **estado selecionado**, nao carregamento obrigatorio da rota.

| Pagina | Painel/drawer |
| --- | --- |
| Agenda | Contexto da aula, conflito, filtro rapido, vaga ou indisponibilidade selecionada. |
| Turmas | Detalhe de turma selecionada, com alunos fixos, vagas, proximas aulas e historico. |
| Grade | Detalhe de bloco recorrente selecionado e impacto futuro. Bloqueio e modo situacional. |
| Aula | Drawer de chamada ou outros drawers contextuais: aluno, reposicao, observacao, conflito ou aviso. |
| Reposicoes | Detalhe contextual por estado: pendente, com opcao, aguardando resposta, agendada, bloqueada ou encerrada. |

## O Que Nao Falta Para Web

- Agenda operacional tem imagem propria.
- Turmas recorrentes tem imagem propria.
- Grade/semana-modelo tem imagem propria.
- Aula/chamada tem imagem propria.
- Reposicoes/encaixe tem imagem propria.
- Rotas de detalhe herdadas estao contratadas.
- Bloqueios foram definidos como fluxo contextual, sem pagina de Recursos obrigatoria.
- Eventos foram classificados como heranca inicial, sem imagem propria agora.

## O Que Fica Para Futuro

- Eventos/workshops podem ganhar imagem propria se virarem modulo comercial/operacional forte.
- Lista de espera geral pode virar superficie propria fora de Reposicoes.
- Catalogo de recursos/salas/equipamentos pode morar em Configuracoes se algum studio precisar controle formal.
- Mobile precisa design especifico: Agenda em lista/dia, Aula/Chamada em tela focada, Reposicoes em lista + detalhe, Turmas/Grade em consulta e acoes essenciais.

## Risco Residual

| Risco | Mitigacao |
| --- | --- |
| Grade ser interpretada como pagina de bloqueios por causa da imagem 36. | Contrato registra que bloqueio e situacional; implementacao deve rebaixar `Criar bloqueio` para acao secundaria/menu. |
| Recurso/sala/equipamento parecer obrigatorio. | Todos os contratos marcam recurso como opcional. |
| Reposicoes virar lista de espera geral. | Contrato limita `/app/reposicoes` a reposicao e encaixe. |
| Chamada virar rota separada pesada. | Chamada permanece drawer/painel dentro de `/app/aulas/[id]`. |

## Veredito

A familia Agenda / Turmas / Grade / Aula / Reposicoes esta coberta para web v0.1 com cinco imagens aprovadas e contratos textuais para rotas herdadas.

Nao e necessario gerar novas imagens desta familia agora.
