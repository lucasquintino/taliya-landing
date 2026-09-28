# Auditoria Final - Rodada 4.1C - Tarefas, Checklists E Aprovacoes

> Status: aprovada v0.1. Esta auditoria fecha a familia 4.1C web e confirma as fronteiras entre trabalho humano, rotinas operacionais e decisoes auditaveis.

## Veredito

A familia **Tarefas / Checklists / Aprovacoes** esta suficientemente coberta para web nesta rodada.

As tres paginas tem papeis diferentes e nao se sobrepoem de forma problematica:

- **Tarefas**: trabalho humano unitario com dono, prazo, origem e conclusao.
- **Checklists**: rotina operacional com varios passos, progresso e execucao.
- **Aprovacoes**: decisao humana auditavel antes de uma acao seguir.

Nao e necessario gerar novas imagens desta familia agora.

## Imagens Aprovadas

| Imagem | Arquivo | Rota principal | Status |
| --- | --- | --- | --- |
| 23 | `23_round-4.1C_tarefas_01_lista-detalhe.png` | `/app/tarefas` | Aprovada |
| 24 | `24_round-4.1C_checklists_01_lista-execucao-detalhe.png` | `/app/checklists` | Aprovada |
| 25 | `25_round-4.1C_aprovacoes_01_lista-decisao-detalhe.png` | `/app/aprovacoes` | Aprovada |

## Cobertura De Rotas

| Rota | Cobertura | Decisao |
| --- | --- | --- |
| `/app/tarefas` | Imagem 23 | Coberta. |
| `/app/tarefas/[taskId]` | Painel lateral da imagem 23 + contrato de drawer de Tarefa | Nao precisa imagem propria agora. |
| `/app/checklists` | Imagem 24 | Coberta. |
| `/app/checklists/[runId]` | Painel lateral da imagem 24 | Nao precisa imagem propria agora. |
| `/app/aprovacoes` | Imagem 25 | Coberta. |
| `/app/aprovacoes/[approvalId]` | Painel lateral da imagem 25 | Nao precisa imagem propria agora. |

## Fronteiras De Produto

| Superficie | Pergunta que responde | Nao deve virar |
| --- | --- | --- |
| Hoje | O que precisa da minha atencao hoje? | Lista completa de tarefas, checklist ou aprovacoes. |
| Operacao | O que esta aberto e em que etapa esta? | Dono do dado real ou pagina de execucao. |
| Tarefas | Quem precisa fazer o que, ate quando, e de onde veio? | Aprovacao, checklist ou dashboard. |
| Checklists | Que rotina precisa ser executada e quais passos faltam? | Tarefa solta ou kanban. |
| Aprovacoes | Que decisao precisa de autorizacao humana? | Tarefa, checklist ou execucao autonoma. |
| Origem | Onde o dado real mora e muda? | Duplicata dos paineis de detalhe. |

## Regras De Conversao Entre Objetos

| Origem | Pode gerar | Quando |
| --- | --- | --- |
| Checklist | Tarefa | Um passo precisa de dono, prazo ou acompanhamento separado. |
| Tarefa | Aprovacao | A conclusao ou acao exige autorizacao sensivel. |
| Aprovacao | Tarefa | A decisao pede dados, revisao humana ou execucao posterior. |
| Aprovacao | Execucao | Apenas depois de aprovada e se politica/modo/cota permitirem. |
| Operacao | Tarefa/Aprovacao/Origem | Quando acompanhamento revela trabalho humano, decisao ou dado real a corrigir. |
| Hoje | Tarefa/Aprovacao/Origem | Quando a prioridade do dia ainda nao tem objeto acionavel. |

## Agentes, Planos E Modos

| Contexto | Tarefas | Checklists | Aprovacoes |
| --- | --- | --- | --- |
| 0 agentes | Funcionam manualmente e por regras programaticas. | Funcionam manualmente e por recorrencia/configuracao. | Funcionam para equipe, sistema, financeiro, agenda, dados e comunicados. |
| 1 agente | Copiloto aparece apenas em tarefas do dominio ativo. | Sugestoes aparecem apenas em rotinas relacionadas ao dominio ativo. | Aprovacoes de agente aparecem apenas no dominio ativo. |
| 3 agentes | Dominios ativos podem sugerir prioridade, checklist e proxima acao. | Dominios ativos podem sugerir passos e detectar bloqueios. | Dominios ativos podem criar propostas e pedidos de aprovacao. |
| 7 agentes | Todos os dominios podem ter apoio, respeitando cota, permissao e risco. | Todos os dominios podem ter apoio seguro. | Todos os dominios podem gerar propostas, mas agente nunca aprova sozinho. |
| Manual | Usuario cria, assume, conclui, comenta e abre origem. | Usuario marca passos, comenta, conclui e cria tarefa. | Usuario aprova, edita, rejeita, pede dados e abre origem. |
| Copiloto | Sugere resumo, prioridade, checklist e comentario. | Sugere passo, responsavel, bloqueio e proxima acao. | Resume contexto, sugere texto, risco e impacto. |
| Autonomo | Pode criar tarefa segura; conclui apenas com evidencia objetiva. | Pode marcar passo apenas com evidencia objetiva e regra clara. | Nao aprova sozinho; envia para fila quando politica exigir. |

## Pontos Corrigidos Nesta Auditoria

1. O blueprint da Rodada 4.0 separava `/app/checklists` dentro de Tarefas. Foi ajustado para tornar Checklists uma superficie propria.
2. O blueprint mencionava `lista densa/kanban` como centro de Tarefas. Foi ajustado: lista densa e o padrao base; kanban fica como opcional futuro.
3. O blueprint de Aprovacoes trazia `executar` como acao de drawer. Foi ajustado: a aprovacao decide; execucao ocorre depois, quando permitido.
4. A estrategia de cobertura visual foi atualizada com as imagens 24 e 25 aprovadas.

## Pontos Abertos Nao Bloqueantes

| Ponto | Decisao para agora |
| --- | --- |
| CTA `Criar aprovacao` | Aceito visualmente, mas deve virar `Nova solicitacao` ou ser removido se aprovacoes nascerem sempre de origem/fluxo. |
| Modelos de checklist | Nao precisam imagem agora; podem herdar Checklists + forms/componentes 3B.1. |
| Historico profundo | Nao precisa imagem propria nesta familia; herda Auditoria/Historico. |
| Estados vazios | Documentar futuramente por componente, nao por pagina. |
| Mobile | Rodada propria. |

## Proxima Familia Recomendada

Proxima familia recomendada:

**Inbox / Conversas**

Motivo:

- e a origem de muitas filas humanas;
- conversa com WhatsApp, agentes, tarefas e aprovacoes;
- precisa diferenciar conversa, atendimento humano, sugestao de copiloto e handoff;
- provavelmente exige imagem propria por ter layout e modelo mental diferentes.

## Referencias

- `design-system-round-4-1C-tarefas-image-plan.pt-BR.md`
- `design-system-round-4-1C-checklists-approved.pt-BR.md`
- `design-system-round-4-1C-aprovacoes-approved.pt-BR.md`
- `design-system-round-4-image-coverage-strategy.pt-BR.md`
- `drawer-lifecycle-contracts.pt-BR.md`
- `agent-guardrails-evals-contract.pt-BR.md`
