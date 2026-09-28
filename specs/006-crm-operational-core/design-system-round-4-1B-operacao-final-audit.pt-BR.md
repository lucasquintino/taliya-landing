# Auditoria Final - Pagina Operacao - Rodada 4.1B

> Status: aprovada v0.1. Esta auditoria fecha a pagina Operacao web apos as imagens `21_round-4.1B_operacao_01_kanban-geral.png` e `22_round-4.1B_operacao_02_kanban-com-drawer.png`.

## Veredito

A pagina Operacao esta suficientemente coberta para web nesta rodada.

As duas imagens aprovadas cobrem:

1. estado geral da pagina como kanban operacional de pendencias acompanhadas;
2. estado de interacao principal com card selecionado e drawer lateral especifico por tipo.

Nao e necessario gerar novas imagens de Operacao nesta rodada.

## 1. Cobertura Das Imagens

| Imagem | Cobertura | Status |
| --- | --- | --- |
| `21_round-4.1B_operacao_01_kanban-geral.png` | Estrutura geral: app shell, topbar, filtros, filtros rapidos, kanban de pendencias, cards unitarios, origens canonicas, atividade recente. | Aprovada |
| `22_round-4.1B_operacao_02_kanban-com-drawer.png` | Interacao principal: mesmo kanban com card selecionado e drawer de Bloqueio de agenda/Reposicao. | Aprovada |

Cobertura suficiente porque a pagina tem um padrao principal simples:

- lista/kanban para acompanhar;
- drawer para entender e agir;
- origem canonica para resolver dado real.

## 2. Sobreposicao Funcional Dos Containers

Nao ha sobreposicao funcional problematica entre containers.

| Container | Papel | Observacao |
| --- | --- | --- |
| Topbar | Navegar entre superficies do grupo Operacao. | Nao duplica sidebar. |
| Filtros superiores | Refinar busca por origem, dono, tipo, status e bloqueio. | Nao substitui colunas. |
| Filtros rapidos laterais | Atalhos de triagem: minhas, sem dono, bloqueadas, aguardando, cota/agente. | Complementa os filtros superiores. |
| Kanban | Superficie principal de acompanhamento. | Nao vira Hoje nem Tarefas. |
| Cards | Cada card representa 1 item operacional unitario. | Nao agrupa varios itens. |
| Atividade recente | Historico leve de movimento. | Nao substitui Auditoria. |
| Drawer | Detalhe e acoes do item selecionado. | Nao duplica a tela de origem. |

Risco evitado:

- Hoje decide prioridade do momento;
- Operacao acompanha andamento;
- Tarefas guarda trabalho humano;
- Aprovacoes guarda decisoes;
- Origem guarda o dado real.

## 3. Drawers Mapeados

Os drawers estao mapeados como contrato compartilhado por tipo entre Hoje e Operacao em `drawer-lifecycle-contracts.pt-BR.md`.

Regra aprovada:

- mesmo tipo real = mesmo drawer;
- Hoje muda o motivo de entrada;
- Operacao muda a etapa/acompanhamento;
- origem canonica, acoes, bloqueios e modos continuam iguais.

Tipos cobertos:

| Tipo | Status |
| --- | --- |
| Tarefa | Mapeado |
| Bloqueio | Mapeado e visualizado na imagem 22 |
| Aprovacao | Mapeado |
| Conversa/fila humana | Mapeado |
| Financeiro | Mapeado |
| Dados | Mapeado |
| Agenda/Reposicao | Mapeado e visualizado na imagem 22 |
| Incidente | Mapeado |
| Cota/Uso | Mapeado |

Nao falta drawer para a pagina web de Operacao nesta rodada.

## 4. Coerencia Dos Ciclos

O ciclo da pagina esta coerente e simples:

1. Item nasce na origem canonica.
2. Se precisa acompanhamento, aparece em Operacao.
3. Usuario ve status no kanban.
4. Usuario abre drawer.
5. Usuario toma uma acao segura ou abre origem.
6. Origem/tarefa/aprovacao/incidente muda o estado real.
7. Operacao atualiza coluna e atividade.
8. Item sai do acompanhamento quando resolvido.

Colunas aprovadas:

- Novo;
- Assumido;
- Aguardando;
- Bloqueado;
- Resolvido.

Regra critica:

Cada card representa 1 item operacional unitario. Se houver varios itens parecidos, isso aparece como filtro/contador, nao como card agregado.

## 5. Planos 0, 1, 3 E 7 Agentes

| Plano | Funcionamento em Operacao |
| --- | --- |
| 0 agentes | Pagina funciona manualmente e por regras programaticas do CRM. Cards, filtros, colunas, drawer, tarefas, aprovacoes e origem continuam disponiveis. |
| 1 agente | IA atua apenas se o agente ativo cobrir o dominio do item. Caso contrario, o caminho manual permanece. |
| 3 agentes | IA pode ajudar nos dominios ativos do pacote, normalmente Atendimento, Agenda e Vendas, salvo configuracao/troca. |
| 7 agentes | Todos os dominios podem ter IA, sempre respeitando permissao, cota, politica, risco e auditoria. |

A pagina nao depende de agente para ser util.

## 6. Manual, Copiloto E Autonomo

| Modo | Cobertura |
| --- | --- |
| Manual | Coberto como caminho principal: abrir origem, assumir, delegar, criar tarefa, pedir aprovacao, marcar resolvido quando permitido. |
| Programatico | Coberto: CRM pode detectar estados e colocar itens em Operacao sem IA. |
| Copiloto | Coberto de forma discreta: resumo, sugestao, explicacao de bloqueio e proxima acao. |
| Autonomo | Coberto com restricao: apenas fallback seguro, tarefa interna ou acao idempotente permitida. Nunca decide aprovacao, nao altera dado sensivel e nao substitui origem. |

O visual aprovado mostra IA como apoio, nao como protagonista.

## 7. O Que Falta Para Web

Nao falta imagem para fechar a pagina Operacao web nesta rodada.

Ficam apenas refinamentos futuros de contrato, nao bloqueadores:

- harmonizar documentos antigos que ainda usam "mapa de jornadas" ou "caso operacional profundo" como metafora principal;
- definir microcopy final dos estados vazios, erro, loading e sem permissao;
- detalhar comportamento de drag-and-drop versus mudanca de status por menu;
- definir contador/filtro quando houver muitos itens parecidos sem criar card agregado;
- em implementacao real, garantir acessibilidade de kanban e drawer por teclado.

## 8. O Que Fica Para Mobile

Mobile nao deve tentar reproduzir o kanban completo.

Recomendacao para mobile:

- usar lista priorizada de pendencias operacionais;
- filtros em chips ou bottom sheet;
- tabs simples: `Abertas`, `Aguardando`, `Bloqueadas`, `Resolvidas`;
- drawer vira tela cheia ou bottom sheet;
- acoes principais no footer fixo;
- foco em abrir origem, assumir/delegar e acompanhar pendencias urgentes;
- nao mostrar atividade recente completa por padrao;
- nao tentar arrastar cards entre colunas no mobile.

Mobile deve responder:

> Quais pendencias operacionais eu preciso acompanhar agora e qual proxima acao posso tomar pelo celular?

Nao precisa ser imagem desta rodada.

## Fechamento

A pagina Operacao web esta fechada como:

> Kanban operacional de pendencias acompanhadas, com cards unitarios, origem canonica, modos de agente discretos e drawer compartilhado por tipo com Hoje.

Essa definicao evita complexidade de casos, nao duplica Hoje e mantem a resolucao conectada as superficies corretas do CRM.
