# Taxonomia de estados de UI - PT-BR

> Status: Rodada 0 v0.1. Este documento padroniza estados que toda tela deve considerar.

## Estados globais

| Estado | Quando aparece | Deve mostrar |
| --- | --- | --- |
| Carregando | Dados em busca ou acao em andamento. | Skeleton/spinner curto e contexto do que carrega. |
| Vazio | Nao ha itens para aquele filtro/contexto. | Explicacao e proxima acao, se existir. |
| Sem permissao | Usuario nao pode ver/fazer. | Motivo, papel necessario e pedir revisao quando permitido. |
| Erro recuperavel | Falha temporaria. | Tentar novamente, abrir suporte ou criar tarefa. |
| Erro bloqueante | Falha impede fluxo. | O que parou, impacto e dono do problema. |
| Dado incompleto | Falta dado essencial. | Campo/objeto faltante e caminho para corrigir. |
| Dado conflitante | Existem duas fontes divergentes. | Comparacao e acao de resolver. |
| Cota 70% | Uso preventivo. | Projecao e recomendacao. |
| Cota 90% | Economia ativa. | O que virou aprovacao/tarefa. |
| Cota 100% | Automacao paga bloqueada. | Alternativa manual e pacote/upgrade. |
| Agente pausado | Fluxo/agente parado. | Motivo, quem pausou, retomar se permitido. |
| Aguardando humano | Agente ou sistema precisa de pessoa. | Dono/fila, prazo e acao esperada. |
| Aguardando contato | Esperando aluno/responsavel/interessado. | Ultima tentativa, proxima acao e prazo. |
| Aguardando aprovacao | Proposta pendente. | Decisor, impacto e prazo de expiracao. |
| Integracao falhou | Provedor indisponivel ou erro. | Provedor, ultima tentativa, retry e fallback. |
| Suporte ativo | Taliya tem acesso temporario. | Escopo, prazo, motivo e revogar. |

## Estados por objeto

| Objeto | Estados minimos de UI |
| --- | --- |
| Aluno | ativo, pausado, inativo, cancelado, risco, inadimplente, dado sensivel. |
| Interessado | novo, quente, sem resposta, experimental, pre-matricula, perdido, sem vaga. |
| Aula | agendada, chamada pendente, concluida, cancelada, conflito, professor/sala indisponivel. |
| Presenca | esperada, presente, falta avisada, no-show, corrigida. |
| Reposicao | disponivel, reservada, aguardando resposta, usada, expirada, conflito. |
| Pagamento | previsto, pendente, atrasado, pago, falhou, disputa, reembolso. |
| Conversa | nova, agente respondendo, humano ativo, aguardando contato, opt-out, falha de envio. |
| Caso | aberto, atribuido, bloqueado, pendente de aprovacao, resolvido, reaberto. |
| Fluxo | rascunho, em teste, ativo, pausado, bloqueado por plano/dado/cota, falhou. |
| Politica | rascunho, simulada, aguardando aprovacao, ativa, substituida, revertida. |

## Estados mobile obrigatorios

No app, estados precisam ser curtos e acionaveis:

- urgente;
- atrasado;
- sem dono;
- precisa aprovacao;
- pode resolver agora;
- precisa computador;
- bloqueado por permissao;
- bloqueado por cota;
- agente pausado;
- falha de envio;
- dado sensivel.

## Regra de aceite para telas

Nenhuma tela esta pronta se tiver apenas estado feliz. Toda ficha de tela deve listar pelo menos:

- vazio;
- carregando;
- erro;
- sem permissao;
- bloqueio por dado;
- bloqueio por cota quando houver agente/uso;
- estado sensivel quando envolver financeiro, historico, privacidade ou suporte.
