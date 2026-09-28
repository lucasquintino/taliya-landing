# Politicas operacionais versionadas - PT-BR

> Status: Rodada 0 v0.1. Politicas sao regras que humanos e agentes usam para decidir.

## Regra central

Se uma regra afeta agenda, dinheiro, mensagem, cancelamento, reposicao, autonomia ou risco, ela deve ser versionada.

## Politicas iniciais

| Politica | Exemplos de regra | Impacto |
| --- | --- | --- |
| Agenda | janela de confirmacao, tolerancia de falta, regras de encaixe. | Aulas, presenca, reposicao. |
| Reposicao | validade do credito, limite mensal, prioridade da lista. | Creditos e vagas. |
| Cobranca e consumo de aulas | modelo de cobranca, momento de consumo, acumulacao, expiracao e bloqueio. | Financeiro, chamada, reposicao, perfil do aluno e agentes. |
| Excecoes operacionais | credito manual, devolucao de consumo, extensao, liberacao pontual e ajuste controlado. | Agenda, financeiro, reposicao, aprovacao e auditoria. |
| Cancelamento/pausa | aviso previo, data efetiva, creditos restantes. | Financeiro, agenda, contrato. |
| Cobranca | quando lembrar, tom, numero de tentativas, canal. | Pagamentos, WhatsApp, cota. |
| Desconto/cortesia | quem pode aprovar, limite, motivo obrigatorio. | Financeiro e auditoria. |
| Comunicados | elegibilidade, consentimento, aprovacao, canal. | Segmentos e envios. |
| Retencao | risco, inatividade, primeira semana, reativacao. | Tarefas e mensagens. |
| Historico | visibilidade, dados sensiveis, professor permitido. | Privacidade e aula. |
| Autonomia de agente | limites, modo, fallback, confianca minima. | Execucao e cota. |
| Suporte | escopo, prazo, dados permitidos, revogacao. | Operacao interna Taliya. |

## Ciclo de vida

```text
rascunho
  -> simulada
  -> aguardando aprovacao
  -> publicada
  -> ativa
  -> substituida
  -> revertida
  -> arquivada
```

## Campos de uma versao

- politica;
- versao;
- descricao em linguagem simples;
- regra estruturada;
- area afetada;
- objetos afetados;
- data de vigencia;
- autor;
- aprovador;
- simulacao/impacto;
- rollback possivel;
- status;
- auditoria.

## Simulacao obrigatoria

Obrigatoria para:

- mudanca de reposicao;
- mudanca de modelo de cobranca ou consumo de aulas;
- mudanca de regra de excecao operacional;
- cancelamento/pausa;
- cobranca;
- autonomia de agente;
- comunicados em massa;
- descontos/cortesias acima do limite;
- mudanca que afeta muitas aulas/alunos.

## Snapshot

Execucoes de agente e decisoes sensiveis devem guardar qual versao da politica foi usada. Se a politica mudar depois, o historico continua explicavel.

## Aceite

Nenhuma tela de configuracao de regra esta pronta se nao mostrar:

- versao atual;
- rascunho ou alteracao pendente;
- impacto;
- vigencia;
- quem aprovou;
- rollback ou motivo para nao permitir rollback.
