# Dinheiro na Mesa — Calculadora

## Função

Dinheiro na Mesa é a prova financeira da landing. Deve ser uma calculadora interativa inspirada na lógica da Lufisio, mas com linguagem e visual próprios.

## Título

Quanto dinheiro pode estar escapando da sua operação?

## Subtítulo

Ajuste alguns números do seu studio e veja uma estimativa simples de perdas em faltas, reposições, mensalidades, horários vagos e alunos inativos.

## Inputs

- Alunos ativos
- Mensalidade média por aluno
- Faltas/cancelamentos por semana
- Turmas com vaga por semana
- Mensalidades atrasadas por mês
- Planos vencendo nos próximos 30 dias
- Alunos inativos nos últimos 30 dias
- Interessados recebidos por mês
- Aulas experimentais sem fechamento
- Horas manuais gastas por semana

## Resultado

R$ X/mês em dinheiro na mesa

## Fórmula base

```ts
agendaRecoverable = faltasPorSemana * 4 * valorPorHorario * 0.25

financeiroRecoverable =
  mensalidadesAtrasadas * mensalidadeMedia * 0.40 +
  planosVencendo * mensalidadeMedia * 0.20

retencaoRecoverable = alunosInativos * mensalidadeMedia * 0.12

vendasRecoverable = aulasExperimentaisSemFechamento * mensalidadeMedia * 0.10

atendimentoRecoverable = interessadosPorMes * mensalidadeMedia * 0.08

tempoEconomizadoValor = horasManuaisPorSemana * 4 * valorHoraEstimado

dinheiroNaMesa =
  agendaRecoverable +
  financeiroRecoverable +
  retencaoRecoverable +
  vendasRecoverable +
  atendimentoRecoverable +
  tempoEconomizadoValor
```

## Breakdown por agente

- Atendimento: interessados esquecidos / mensagens sem próximo contato
- Agenda: faltas/cancelamentos / turmas com vaga
- Vendas: aulas experimentais sem fechamento
- Financeiro: mensalidades atrasadas / planos vencendo
- Retenção: alunos inativos / queda de frequência
- Gestão: total consolidado / ações recomendadas
- Histórico/Evolução: horas economizadas / contexto organizado

## Disclaimer

Essa é uma estimativa simples. O valor real depende da rotina do studio, mensalidade média, frequência dos alunos e execução das ações.
