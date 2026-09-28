# Auditoria Final - Rodada 4.1H Retencao, Cancelamentos, Reativacoes E Reclamacoes Web

> Status: fechada para web v0.1 em 13/05/2026.

## Resultado Da Auditoria

A familia esta suficiente para o MVP web.

As quatro paginas aprovadas cobrem o ciclo completo de permanencia do aluno:

1. perceber risco antes da saida;
2. tratar pedido real de cancelamento ou pausa;
3. tentar retorno de ex-aluno, pausado ou inativo elegivel;
4. resolver reclamacao ou caso sensivel com resposta controlada.

Nao e necessario gerar imagem adicional agora.

## Imagens Aprovadas

| Imagem | Rota | Funcao |
| --- | --- | --- |
| `41_round-4.1H_retencao_01_riscos-lista-drawer.png` | `/app/retencao` ou `/app/retencao/riscos` | Risco preventivo antes de pedido formal de saida. |
| `42_round-4.1H_cancelamentos_01_fila-salvamento-drawer.png` | `/app/cancelamentos` | Pedido real de saida, pausa, salvamento e decisao humana. |
| `43_round-4.1H_reativacoes_01_ex-alunos-retorno.png` | `/app/retencao/reativacoes` | Retorno de ex-alunos, pausados e inativos elegiveis. |
| `44_round-4.1H_reclamacoes_01_fila-caso-sensivel-drawer.png` | `/app/reclamacoes` | Reclamacoes, casos sensiveis, resposta revisada e automacao pausada. |

## Topbar Final Da Familia

```text
Riscos | Cancelamentos | Reativacoes | Reclamacoes
```

## Rotas Finais

| Rota | Mantem? | Motivo |
| --- | --- | --- |
| `/app/retencao` | Sim | Entrada principal de risco preventivo. |
| `/app/retencao/riscos` | Opcional/alias | Pode ser alias ou subrota para a mesma tela de riscos. |
| `/app/cancelamentos` | Sim | Pedido real de saida/pausa precisa de superficie propria. |
| `/app/retencao/reativacoes` | Sim | Reativacao nao e campanha generica nem lead novo. |
| `/app/reclamacoes` | Sim | Reclamacao sensivel precisa de dono, prazo, pausa de automacao e auditoria. |
| `/app/reclamacoes/[caseId]` | Sim, como deep link | Pode abrir a mesma tela com drawer/detalhe do caso selecionado. |
| `/app/retencao/campanhas` | Nao no MVP | Substituida por `/app/retencao/reativacoes`. Campanhas massivas ficam fora do MVP. |
| `/app/satisfacao` | Nao no MVP | Satisfacao vira sinal/origem para Retencao, Reclamacoes e Relatorios, nao pagina propria. |
| `/app/casos-sensiveis` | Nao no MVP | Casos sensiveis de aluno entram em `/app/reclamacoes`; excecoes financeiras sensiveis entram em Financeiro/Aprovacoes/Tarefas. |

## Auditoria Como Gestor Do Studio

### 1. Aluno esta sumindo, mas nao pediu cancelamento

O gestor usa `Riscos`.

Ele consegue ver:

- quem esta em risco;
- por que esta em risco;
- ultima aula ou interacao;
- proxima acao sugerida;
- responsavel;
- historico curto;
- sugestao do copiloto.

Conclusao: coberto.

### 2. Aluno pediu cancelamento ou pausa

O gestor usa `Cancelamentos`.

Ele consegue ver:

- motivo declarado;
- impacto financeiro;
- aulas futuras afetadas;
- reposicoes em aberto;
- plano de salvamento;
- automacoes pausadas;
- decisao humana de pausar, salvar ou confirmar cancelamento.

Conclusao: coberto.

### 3. Aluno saiu, pausou ou ficou inativo e pode voltar

O gestor usa `Reativacoes`.

Ele consegue ver:

- motivo de saida;
- ultima atividade;
- oportunidade real de retorno;
- vaga/plano sugerido;
- restricoes de contato;
- historico;
- acao de mensagem, tarefa ou reserva de vaga com validacao.

Conclusao: coberto.

### 4. Aluno reclamou ou o caso ficou sensivel

O gestor usa `Reclamacoes`.

Ele consegue ver:

- severidade;
- origem;
- motivo principal;
- prazo;
- responsavel;
- impacto;
- automacao pausada;
- plano de resolucao;
- resposta sugerida pelo copiloto;
- historico e acoes controladas.

Conclusao: coberto.

## Auditoria Tecnica

### Estados Cobertos

| Estado | Pagina dona |
| --- | --- |
| Risco baixo/medio/alto | Retencao/Riscos |
| Queda de frequencia | Retencao/Riscos |
| Sem aula recente | Retencao/Riscos |
| Feedback negativo preventivo | Retencao/Riscos |
| Financeiro afetando permanencia | Retencao/Riscos + Financeiro |
| Pedido de cancelamento | Cancelamentos |
| Pedido de pausa | Cancelamentos |
| Salvamento em andamento | Cancelamentos |
| Aguardando aluno | Cancelamentos ou Reativacoes conforme fase |
| Cancelamento confirmado | Cancelamentos |
| Recuperado | Cancelamentos |
| Ex-aluno elegivel | Reativacoes |
| Pausado vencendo | Reativacoes |
| Interesse detectado | Reativacoes |
| Nao contatar | Reativacoes/Cancelamentos, com bloqueio de mensagem |
| Reativado | Reativacoes, depois historico/relatorios |
| Reclamacao alta/media/baixa | Reclamacoes |
| Aguardando resposta | Reclamacoes |
| Aguardando responsavel | Reclamacoes |
| Reaberta | Reclamacoes |
| Resolvida | Reclamacoes |
| Automacao pausada | Cancelamentos/Reclamacoes |

### Modos Manual, Copiloto E Autonomo

| Modo | Regra nesta familia |
| --- | --- |
| Manual | Tudo deve funcionar com 0 agentes: filtrar, abrir drawer, enviar mensagem manual, criar tarefa, registrar acompanhamento, pausar, cancelar, reativar e resolver. |
| Copiloto | Agente resume, sugere resposta, prepara plano, explica risco e organiza proximas acoes; usuario revisa antes de contato externo. |
| Autonomo | Permitido apenas para acoes seguras, com politica, consentimento, cota, horario e auditoria. Bloqueado em cancelamento ativo, `nao contatar` e alta severidade. |

### 0, 1, 3 E 7 Agentes

| Quantidade de agentes | Comportamento |
| --- | --- |
| 0 agentes | CRM continua completo. Todas as filas sao operadas por humanos e regras programaticas. |
| 1 agente | Normalmente Retencao/Atendimento pode sugerir mensagens e priorizar risco; decisoes sensiveis continuam humanas. |
| 3 agentes | Atendimento, Agenda e Financeiro podem alimentar sinais de risco, cancelamento e reclamacao; Retencao centraliza a decisao. |
| 7 agentes | Cada dominio pode enriquecer contexto, mas cancelamento, reativacao sensivel e reclamacao seguem guardrails, permissoes e auditoria. |

## Decisoes De Produto

1. `Reativacoes` substitui `Campanhas` no MVP.

Motivo: o objetivo agora e operacional e individualizado, nao campanha massiva.

2. `Satisfacao` nao vira rota propria no MVP.

Motivo: feedback simples alimenta Retencao, Reclamacoes, Alunos e Relatorios. Reclamacao sensivel entra em `/app/reclamacoes`.

3. Nao criar `/app/casos-sensiveis` no MVP.

Motivo: casos sensiveis de relacionamento ficam em Reclamacoes; outros dominios usam suas paginas donas e Aprovacoes/Tarefas.

4. Nao gerar estado visual severo adicional agora.

Motivo: a imagem 44 ja cobre a arquitetura. A variacao severa muda permissao, bloqueio e confirmacao, mas nao muda layout principal.

5. `Nao contatar` e regra forte.

Motivo: qualquer contato externo deve ser bloqueado quando esse estado estiver ativo, salvo acao administrativa explicita de alterar preferencia com permissao.

## Pendencias Para Implementacao

- Confirmar nomes finais no produto com acento: Retencao, Reativacoes e Reclamacoes devem aparecer acentuados na UI final.
- Padronizar URLs sem duplicar `/app` no mock visual.
- Implementar confirmacao forte para `Confirmar cancelamento`.
- Implementar confirmacao forte para `Marcar resolvida`.
- Fazer `Responder` abrir composer/revisao, nao envio direto.
- Fazer `Reservar vaga` validar agenda, turma, limite, conflito, permissao e politica.
- Variar responsaveis reais por permissao/papel.
- Registrar auditoria para mudancas de estado sensiveis.

## Conclusao

Familia 4.1H aprovada para web v0.1.

Nao falta rota obrigatoria para MVP dentro de Retencao/Cancelamentos/Reativacoes/Reclamacoes.

Nao falta imagem obrigatoria neste momento. A proxima rodada pode seguir para outra familia.
