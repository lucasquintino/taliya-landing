# Modelo De Cobranca E Consumo De Aulas

Status: contrato v0.1.
Data: 2026-05-13.

## Decisao Central

O Taliya precisa separar tres coisas que muitos studios misturam no dia a dia:

1. como o aluno paga;
2. como o aluno consome aulas;
3. como o studio abre excecoes e quebra-galhos.

Se isso ficar misturado, Financeiro, Agenda, Reposicoes, Retencao e Agentes vao tomar decisoes erradas.

## Modelos De Cobranca Do Aluno

| Modelo | Como funciona | Impacto |
|---|---|---|
| Mensalidade fixa | Aluno paga valor recorrente por periodo. | Gera cobranca recorrente, status financeiro e regra de inadimplencia. |
| Pacote de aulas | Aluno compra quantidade de aulas/creditos. | Precisa controlar saldo, vencimento, uso e reposicao. |
| Plano hibrido | Mensalidade com limite, credito ou regra especifica. | Exige regra clara de consumo e excecoes. |
| Aula avulsa | Cobranca por aula/evento. | Gera movimento pontual e nao deve virar recorrencia sem confirmacao. |
| Cortesia/bolsa/desconto | Valor parcial ou gratuito com motivo. | Exige politica, aprovacao ou auditoria conforme regra do studio. |

## Modelos De Consumo De Aula

| Modelo | O que controla | Onde impacta |
|---|---|---|
| Presenca consome credito | Aula dada/presente reduz saldo. | Chamada, creditos, financeiro, reposicoes. |
| Agendamento reserva credito | Aula marcada segura vaga/credito. | Agenda, lista de espera, no-show, cancelamento. |
| No-show consome | Falta sem aviso perde credito. | Chamada, retencao, comunicacao, regra de reposicao. |
| Falta avisada gera reposicao | Aviso dentro da politica preserva direito. | Reposicoes, creditos, agenda. |
| Credito expira | Credito tem prazo de uso. | Financeiro, agenda, retencao, alertas. |

## Reposicoes E Encaixes

Reposicao nao e so agenda. Ela depende de:

- saldo/credito disponivel;
- regra de falta;
- vencimento do credito;
- turma e nivel compativeis;
- vaga real;
- restricao financeira;
- politica de excecao;
- canal permitido para convite;
- aprovacao quando houver impacto.

## Quebra-Galhos Permitidos

O sistema precisa permitir excecoes controladas para studios reais.

Exemplos:

- liberar aula mesmo com pagamento pendente;
- estender validade de credito;
- conceder reposicao extra;
- permitir encaixe manual;
- marcar pagamento prometido;
- pausar cobranca por acordo;
- aplicar desconto pontual;
- corrigir chamada que consumiu credito errado.

Essas excecoes podem nascer:

- manualmente pelo usuario;
- por sugestao do copiloto;
- por fluxo de agente que pede aprovacao;
- por regra programatica segura.

Mas sempre precisam ter:

- motivo;
- origem;
- responsavel;
- impacto;
- prazo quando aplicavel;
- auditoria;
- rollback ou correcao quando aplicavel.

## Regras Para Agentes

Agente nao decide excecao sensivel sozinho.

Ele pode:

- detectar oportunidade de encaixe;
- sugerir melhor reposicao;
- preparar mensagem;
- apontar conflito financeiro;
- criar tarefa;
- pedir aprovacao;
- executar regra permitida e simples quando preflight passar.

Ele nao pode, sem politica explicita:

- perdoar divida;
- dar credito extra;
- cancelar cobranca;
- liberar aula bloqueada;
- alterar contrato/plano;
- prometer vaga inexistente;
- enviar mensagem que contradiz regra financeira ou de agenda.

## Configuracoes Obrigatorias No Setup

O setup deve perguntar em linguagem simples:

- como o studio cobra alunos;
- se vende pacote, mensalidade, aula avulsa ou mistura;
- quando a aula consome credito;
- quando falta vira reposicao;
- quando no-show perde direito;
- se credito expira;
- quem pode abrir excecao;
- quais excecoes exigem aprovacao;
- quando o agente pode apenas sugerir;
- quando tudo deve ficar manual.

## Impacto Nas Paginas

| Area | Impacto |
|---|---|
| Hoje | Mostra dinheiro, reposicoes, bloqueios e tarefas do dia sem duplicar origem. |
| Agenda/Aulas | Mostra capacidade, chamada, no-show, reposicao e conflitos. |
| Reposicoes | Calcula elegibilidade e melhor encaixe. |
| Financeiro | Mostra cobrancas, pagamentos, promessas, falhas, conciliacao e excecoes em Movimentacoes. |
| Aluno | Mostra plano, saldo/uso, financeiro, proxima aula e pendencias. |
| Retencao | Usa ausencia, credito expirando e financeiro como sinais de risco. |
| Agentes | Respeitam regras publicadas e nao inventam concessoes. |
| Auditoria | Registra excecoes, mudancas e impactos. |

## Criterio De Aceite

O modelo esta correto quando um studio consegue operar mensalidade, pacote, aula avulsa e excecoes sem quebrar agenda, financeiro, reposicoes ou agentes.
