# Guardrails e evals de agentes - PT-BR

> Status: contrato v0.1. Define quando agentes podem sugerir, executar, parar, escalar e ser avaliados.

## Principios

- Agente nao substitui permissao.
- Agente nao decide billing, LGPD, desconto, estorno, contrato, permissao ou acesso de suporte.
- Agente nao usa dado sensivel bruto quando resumo permitido basta.
- Agente deve explicar motivo, cota, risco e fallback quando participa de uma acao.

## Niveis de autonomia

| Nivel | Nome | Exemplo | Requisito |
| --- | --- | --- | --- |
| L0 | Manual | Usuario escreve mensagem. | Sempre disponivel. |
| L1 | Copiloto | Agente sugere texto/resumo. | Cota, permissao de leitura e revisao humana. |
| L2 | Autonomo baixo risco | Lembrete operacional permitido. | Qualidade >= 95%, politica, opt-out, cota e auditoria. |
| L3 | Autonomo condicionado | Follow-up comercial simples. | Piloto anterior, limite de tentativas e handoff. |
| L4 | Bloqueado | Estorno, LGPD, desconto, reclamacao severa. | Humano obrigatorio. |

## Thresholds v0.1

| Metrica | Minimo para autonomia |
| --- | ---: |
| Acuracia de classificacao | 95% |
| Taxa de handoff correto | 98% |
| Incidente severo recente | 0 |
| Reclame/opt-out por envio | abaixo de limite definido por fluxo |
| Cota disponivel | acima de 10% ou pacote ativo |
| Dados obrigatorios completos | 100% |
| Politica publicada | obrigatoria |

## Preflight de execucao autonoma

Antes de executar, verificar:

1. plano inclui agente;
2. fluxo esta ativo;
3. modo permite autonomia;
4. usuario/tenant tem permissao;
5. objeto tem dados obrigatorios;
6. contato tem consentimento/sem opt-out;
7. template/canal esta valido;
8. cota disponivel;
9. risco nao e sensivel;
10. auditoria pronta;
11. fallback manual existe;
12. pausa de emergencia disponivel.

## Ferramentas permitidas por agente

| Agente | Pode usar | Nunca usa sozinho |
| --- | --- | --- |
| Atendimento | conversa, contato, tarefa, opt-out, resumo permitido | dado sensivel, financeiro delicado, LGPD |
| Agenda | aula, turma, reposicao, lista de espera, aviso | mudar politica, remover aluno sem confirmacao |
| Vendas | interessado, experimental, follow-up, origem | contrato final, pagamento, desconto sensivel |
| Financeiro | pagamento, cobranca, comprovante, lembrete | estorno, acordo, disputa, desconto |
| Retencao | risco, tarefa, mensagem, reativacao | cancelamento severo, reclamacao severa |
| Historico/Professor | nota, handoff, contexto permitido | documento sensivel bruto |
| Gestao/Governanca | prioridade, resumo, cota, incidente | billing, permissao, suporte grant |

## Evals por fluxo

Cada fluxo autonomo precisa ter:

- dataset de exemplos reais/sinteticos;
- casos felizes;
- dados ausentes;
- opt-out;
- permissao negada;
- cota insuficiente;
- telefone compartilhado;
- tom sensivel;
- falha de integracao;
- avaliacao de output;
- avaliacao de ferramenta chamada;
- criterio de rollback.

## Monitoramento

| Evento | Acao |
| --- | --- |
| Cota 90% | Modo economia e alerta. |
| Cota 100% | Bloqueia automacao paga. |
| Falha repetida | Abrir incidente S2/S3. |
| Reclame/opt-out elevado | Pausar fluxo e revisar copy. |
| Handoff perdido | Pausar autonomia. |
| Dado sensivel detectado | Bloquear e pedir humano. |
| Incidente S1 | Pausar agente/fluxo imediatamente. |

## Aceite

Um fluxo autonomo so pode entrar em producao quando:

- passou nos evals;
- tem dono;
- tem limite;
- tem cota;
- tem auditoria;
- tem fallback manual;
- tem botao de pausa;
- tem criterio de rollback.
