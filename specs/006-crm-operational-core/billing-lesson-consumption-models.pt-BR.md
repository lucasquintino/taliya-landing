# Modelo de cobranca e consumo de aulas - PT-BR

> Status: rascunho operacional v0.1. Este documento define como o Taliya deve permitir que cada studio configure a relacao entre cobranca, plano do aluno, direito de aula, chamada, faltas, reposicoes e creditos.

## Decisao central

Cada studio pode cobrar e consumir aulas de formas diferentes. O produto nao pode assumir que todo studio trabalha com mensalidade fixa, pacote de creditos ou reposicao da mesma forma.

O Taliya deve separar quatro conceitos:

1. **Modelo de cobranca**: como o aluno paga.
2. **Direito de aula**: o que o aluno pode usar dentro de um periodo ou contrato.
3. **Regra de consumo**: quando uma aula, vaga ou credito e consumido.
4. **Politica de reposicao**: quando uma falta, cancelamento ou ajuste gera direito de reposicao.

Financeiro, Agenda, Chamada, Reposicoes, Perfil do aluno e Agentes devem ler a mesma configuracao ativa.

## Por que isso existe

Studios de Pilates operam com variacoes reais:

- mensalidade com horario fixo;
- mensalidade por quantidade de aulas por semana;
- pacote de aulas/creditos;
- plano trimestral, semestral ou anual parcelado;
- aula avulsa;
- plano com reposicao livre, limitada ou sem reposicao;
- falta avisada que gera credito;
- falta avisada que apenas libera vaga;
- no-show que consome aula;
- credito que expira, acumula ou nao acumula;
- bloqueio financeiro que impede agenda ou apenas gera alerta.

Sem esse contrato, a mesma acao pode gerar comportamento errado: cobrar indevidamente, consumir credito errado, oferecer reposicao sem direito ou bloquear aluno que deveria continuar ativo.

## Modelos de cobranca suportados

| Modelo | Quando usar | O que gera |
| --- | --- | --- |
| Mensalidade por horario fixo | Aluno paga recorrente e tem vaga fixa em turma/horario. | Cobranca recorrente e direito operacional de frequentar a turma fixa. |
| Mensalidade por frequencia | Aluno paga recorrente por quantidade de aulas por semana/mes. | Cobranca recorrente e limite de aulas no ciclo. |
| Pacote de aulas/creditos | Aluno compra quantidade fechada de aulas. | Creditos de aula com validade e saldo. |
| Recorrente com creditos | Mensalidade gera N creditos por ciclo. | Cobranca recorrente e creditos renovados por ciclo. |
| Aula avulsa | Aluno paga aula unica ou evento pontual. | Direito unico de aula/evento. |
| Contrato parcelado | Plano trimestral/semestral/anual com parcelas. | Contrato com parcelas e direito de aula por vigencia/ciclo. |
| Modelo simples sem credito | Studio controla presenca e pagamento, mas nao usa banco de creditos. | Cobrancas e agenda sem ledger de creditos, exceto ajuste manual. |
| Hibrido/customizado | Studio tem regra propria por plano, turma ou aluno. | Usa o modelo base com overrides auditados. |

## Configuracoes por plano

Cada plano vendido pelo studio deve poder configurar:

- tipo de cobranca;
- valor;
- recorrencia ou parcelamento;
- dia de vencimento;
- metodo preferencial;
- unidade, turma ou escopo quando aplicavel;
- quantidade de aulas por ciclo, quando aplicavel;
- horario fixo, quando aplicavel;
- validade dos creditos, quando aplicavel;
- se creditos acumulam ou expiram;
- limite de creditos ativos;
- regra de pausa;
- regra de cancelamento;
- regra de bloqueio financeiro;
- permissao de override manual.

## Regra de consumo de aulas

O consumo deve ser configuravel por plano/modelo.

| Momento de consumo | Comportamento |
| --- | --- |
| Ao reservar/agendar | O credito ou direito e consumido quando a aula e reservada. Cancelamento pode devolver conforme politica. |
| Na chamada/presenca | O credito ou direito e consumido quando a presenca e confirmada. |
| No inicio/fim da aula | O consumo ocorre automaticamente pelo horario da aula se nao houver correcao. |
| No no-show | Ausencia sem aviso pode consumir aula/credito. |
| Manual | Usuario autorizado decide quando consumir, devolver ou ajustar. |

O sistema deve mostrar a consequencia antes de confirmar uma acao sensivel de chamada, falta, reposicao, pausa, cancelamento ou ajuste financeiro.

## Politica de falta e reposicao

Cada studio deve configurar como tratar:

- falta avisada dentro do prazo;
- falta avisada fora do prazo;
- no-show;
- aula cancelada pelo studio;
- troca de professor/sala/recurso;
- feriado/recesso;
- aluno pausado;
- aluno inadimplente;
- pedido manual de reposicao;
- cortesia/credito manual.

Resultado possivel:

| Resultado | Quando aplicar |
| --- | --- |
| Gerar credito de reposicao | Quando a politica reconhece direito futuro. |
| Liberar vaga sem credito | Quando a falta ajuda ocupacao, mas nao cria direito adicional. |
| Consumir aula/credito | Quando a presenca, reserva ou no-show conta como uso. |
| Manter direito intacto | Quando o studio cancelou ou a politica protege o aluno. |
| Exigir aprovacao | Quando a regra e excecao, fora do limite ou sensivel. |
| Criar tarefa/caso | Quando faltam dados, ha conflito ou precisa intervencao humana. |

## Precedencia das regras

Quando houver mais de uma regra aplicavel, a ordem deve ser:

1. Override especifico do aluno.
2. Regra do plano do aluno.
3. Regra da turma/aula.
4. Politica padrao do studio.
5. Padrao seguro do sistema.

Se duas regras conflitarem e o impacto for financeiro, de agenda ou de direito de aula, o sistema deve pedir revisao humana.

## Quebra-galhos e excecoes operacionais

O Taliya deve permitir que o studio resolva situacoes reais fora da regra padrao sem perder controle. Isso e parte do produto, nao um atalho escondido.

Exemplos:

- aluno perdeu prazo de reposicao, mas o gestor quer liberar uma cortesia;
- aluno teve problema pessoal e o studio quer devolver um credito;
- aluno esta inadimplente, mas o gestor quer liberar uma aula pontual;
- pacote venceu, mas o studio quer estender por alguns dias;
- no-show foi marcado errado e precisa devolver consumo;
- turma foi alterada e o studio quer compensar alunos afetados;
- aluno bom cliente precisa de uma excecao comercial controlada;
- agente encontrou uma situacao fora da politica e precisa pedir decisao humana.

Formas de execucao:

| Forma | Como funciona | Controle necessario |
| --- | --- | --- |
| Manual pelo sistema | Usuario autorizado cria ajuste, credito, devolucao, extensao, liberacao ou tarefa. | Motivo obrigatorio, antes/depois, impacto e auditoria. |
| Copiloto | Agente/sistema explica a regra, sugere a excecao e prepara a aprovacao ou ajuste. | Humano revisa antes de executar quando houver impacto sensivel. |
| Autonomo controlado | Agente executa apenas excecoes simples previamente permitidas por politica. | Limite claro, politica ativa, cota, auditoria e fallback. |
| Aprovacao obrigatoria | Excecao fica pendente ate dono/admin/financeiro aprovar. | Decisor, motivo, impacto e registro de politica. |

Tipos de quebra-galho que o produto deve suportar:

| Tipo | Exemplo | Deve afetar |
| --- | --- | --- |
| Credito manual | Criar credito de reposicao por cortesia. | Reposicoes, perfil do aluno e auditoria. |
| Devolucao de consumo | Desfazer consumo de aula por erro de chamada/no-show. | Chamada, direito de aula e historico. |
| Extensao de validade | Estender validade de credito ou pacote. | Creditos, agenda e reposicoes. |
| Liberacao pontual | Permitir aula mesmo com bloqueio financeiro. | Agenda, financeiro e auditoria. |
| Ajuste financeiro | Desconto, cortesia, estorno parcial ou ajuste de valor. | Financeiro, aprovacao e auditoria. |
| Excecao de encaixe | Permitir reposicao fora da regra normal. | Agenda, reposicoes e politica. |

Regra central: o sistema deve facilitar o atendimento humano do studio, mas nunca deixar excecao sensivel invisivel. Todo quebra-galho precisa preservar quem fez, quando fez, por que fez, qual regra foi ignorada/ajustada e qual foi o impacto.

## Objetos de dados necessarios

| Objeto | Papel |
| --- | --- |
| Modelo de cobranca | Define como o aluno paga e como a cobranca nasce. |
| Plano do aluno | Instancia contratada pelo aluno, com vigencia e configuracao aplicada. |
| Direito de aula | Direito gerado pelo plano, pacote, contrato ou cortesia. |
| Evento de consumo de aula | Registro de reserva, presenca, no-show, uso, devolucao ou ajuste. |
| Credito de reposicao | Direito de reposicao com origem, validade, status e politica usada. |
| Politica de consumo/reposicao | Regra versionada usada por humanos e agentes. |
| Movimentacao financeira | Mensalidade, parcela, cobranca, pagamento, estorno, desconto, ajuste ou falha. |
| Evento de auditoria | Antes/depois, ator, motivo, politica e impacto. |

## Impacto nas telas

| Area | Consequencia |
| --- | --- |
| Configuracoes | Deve existir configuracao de modelos de cobranca, consumo de aulas e reposicao. |
| Planos do aluno | Ao criar/editar plano, usuario escolhe modelo e regras aplicadas. |
| Aluno | Perfil mostra plano ativo, direito de aula, creditos, consumo recente e alertas. |
| Agenda/aula/chamada | A chamada deve indicar se a acao consome, preserva, gera credito ou exige aprovacao. |
| Reposicoes | Mostra origem do credito, validade, elegibilidade, politica e destino. |
| Financeiro | Movimentacoes mostram mensalidades, pacotes, parcelas, pagamentos e ajustes sem confundir com credito operacional sem valor. |
| Hoje | Mostra pendencias do dia derivadas de vencimento, consumo, reposicao, chamada e bloqueio financeiro. |
| Aprovacoes | Excecoes de credito, desconto, pausa, bloqueio e reposicao precisam antes/depois. |
| Agentes | Agente so sugere/executa dentro da politica vigente e guarda snapshot da regra usada. |

## Impacto por quantidade de agentes

| Plano Taliya | Comportamento |
| --- | --- |
| 0 agentes | Tudo funciona manual/programatico: cobranca, chamada, credito, reposicao e ajuste. |
| 1 agente | O agente da area ativa pode resumir, sugerir e redigir dentro da politica. Outras areas seguem manuais. |
| 3 agentes | Agenda, financeiro e atendimento podem cooperar, mas continuam presos a politica, permissao e aprovacao. |
| 7 agentes | Mais fluxos podem operar autonomamente, mas excecoes financeiras, creditos fora da regra e mudancas de plano sensiveis continuam com controle humano. |

## Modos de execucao

| Modo | Comportamento |
| --- | --- |
| Manual | Usuario aplica regra, cria/usa credito, ajusta cobranca, registra motivo e confirma impacto. |
| Copiloto | Sistema calcula consequencia, explica regra, sugere acao e prepara texto/tarefa/aprovacao. |
| Autonomo | Executa somente acoes de baixo risco permitidas pela politica: lembretes, convites elegiveis e tarefas. Excecoes exigem aprovacao. |

## Exemplos de ciclos

### Mensalidade com horario fixo

```text
plano ativo
  -> cobranca mensal gerada
  -> aluno esperado em aula fixa
  -> chamada registra presenca/falta/no-show
  -> politica decide se gera credito, consome aula ou apenas registra historico
  -> reposicao usa credito se elegivel
```

### Pacote de aulas

```text
pacote comprado
  -> creditos gerados
  -> aula reservada
  -> politica define se credito e consumido na reserva, presenca ou no-show
  -> credito usado, devolvido, expirado ou ajustado
```

### Aula cancelada pelo studio

```text
aula afetada
  -> impacto calculado
  -> alunos afetados identificados
  -> direito preservado ou credito gerado conforme politica
  -> comunicacao/tarefa/aprovacao criada
```

### Excecao manual

```text
usuario solicita excecao
  -> sistema mostra regra ativa e antes/depois
  -> aprovacao se politica exigir
  -> credito/cobranca/agenda ajustado
  -> auditoria registra motivo e politica
```

## Regras para agentes

Agentes nunca devem inventar direito de aula, perdoar pagamento, gerar cortesia ou mudar consumo sem politica.

O agente pode:

- explicar por que um aluno tem ou nao tem credito;
- sugerir encaixe elegivel;
- redigir convite de reposicao;
- criar tarefa para excecao;
- preparar aprovacao com antes/depois;
- enviar lembrete de cobranca permitido;
- resumir impacto de pausa, cancelamento ou alteracao de plano.

O agente nao pode, sem aprovacao quando sensivel:

- criar credito fora da politica;
- apagar consumo;
- perdoar no-show;
- aplicar desconto/cortesia;
- alterar contrato/plano;
- liberar aluno bloqueado por financeiro;
- mudar regra global de reposicao/cobranca.

## Decisoes ainda abertas

| Tema | Decisao pendente |
| --- | --- |
| Padrao inicial do MVP | Definir quais modelos aparecem no setup inicial e quais ficam em avancado. |
| Nomes comerciais | Definir microcopy final para "credito", "reposicao", "direito de aula" e "pacote" em PT-BR simples. |
| Calculo exato de prioridade | Definir formula final para encaixe quando ha credito, lista de espera e vaga aberta. |
| Provedor financeiro | Definir quais modelos serao integrados automaticamente e quais serao manuais no MVP. |
| Migracao/importacao | Definir como importar studios que ja possuem saldos, pacotes e regras antigas. |

## Criterio de aceite

Este contrato esta respeitado quando:

- nenhuma tela presume um unico modelo de cobranca;
- toda chamada consegue explicar impacto no direito de aula;
- toda reposicao tem origem, validade, status e politica;
- toda movimentacao financeira sabe se veio de mensalidade, pacote, parcela, aula avulsa ou ajuste;
- excecoes de credito/cobranca sao auditadas;
- agentes usam snapshot da politica vigente;
- o studio consegue operar com 0 agentes.
