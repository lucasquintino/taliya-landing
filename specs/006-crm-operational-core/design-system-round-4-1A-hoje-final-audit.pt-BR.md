# Design System Web - Rodada 4.1A - Auditoria Final Da Pagina Hoje

> Status: auditoria v0.1 apos imagens aprovadas 18, 19 e 20 e contratos funcionais dos drawers. A imagem 17 ja e a base aprovada da primeira dobra.

## Conclusao

A pagina **Hoje** esta coerente como mesa de comando diaria do Taliya CRM.

Ela nao deve ser tratada como:

- dashboard de KPI;
- lista completa de tarefas;
- tela de relatorio;
- console de agentes;
- substituta de Operacao/Jornadas.

Ela deve continuar respondendo:

```text
O que precisa acontecer hoje para o studio nao travar?
```

## Imagens Da Familia Hoje

| Imagem | Arquivo | Status | Papel |
| --- | --- | --- | --- |
| 17 | `17_round-4.1A_hoje_01_acima-da-dobra.png` | Base aprovada | Primeira dobra da mesa de comando. |
| 18 | `18_round-4.1A_hoje_02_drawer-tarefa.png` | Aprovada e documentada | Exemplo de drawer de tarefa humana. |
| 19 | `19_round-4.1A_hoje_03_estado-critico-do-dia.png` | Aprovada e documentada | Pressao operacional sem drawer. |
| 20 | `20_round-4.1A_hoje_04_historico-de-hoje.png` | Aprovada e documentada | Abaixo da dobra com memoria operacional do dia. |

## Cobertura Funcional

| Necessidade | Cobertura |
| --- | --- |
| Ver prioridades do dia | Coberto por `Agora`. |
| Ver rotina diaria | Coberto por `Checklist do dia`. |
| Ver aulas de hoje | Coberto por `Aulas de hoje`. |
| Ver fila humana | Coberto por `Fila humana`. |
| Ver bloqueios | Coberto por `Bloqueios de hoje`. |
| Ver tarefas reais | Coberto por `Tarefas de hoje`. |
| Ver aprovacoes pendentes | Coberto por `Aprovacoes de hoje`. |
| Ver dinheiro que exige acao hoje | Coberto por `Dinheiro hoje`. |
| Abrir detalhe de uma tarefa | Coberto por imagem 18. |
| Suportar dia critico | Coberto por imagem 19. |
| Ver o que ja aconteceu hoje | Coberto por imagem 20. |

## Taxonomia E Drawers

A pagina Hoje possui tipos diferentes de itens acionaveis. Eles nao devem ser achatados como tarefas.

| Tipo | Contrato |
| --- | --- |
| Prioridade do Agora | Drawer do tipo real com cabecalho de prioridade. |
| Checklist do dia | Drawer de checklist. |
| Aula de hoje | Drawer de aula. |
| Fila humana | Drawer de fila humana. |
| Bloqueio | Drawer de bloqueio. |
| Tarefa | Drawer de tarefa. |
| Aprovacao | Drawer de aprovacao. |
| Financeiro | Drawer financeiro. |
| Alerta/cota | Drawer de alerta/cota. |
| Incidente | Drawer de incidente. |
| Problema de dados | Drawer de problema de dados. |

Referencias:

- `hoje-actionable-item-taxonomy.pt-BR.md`
- `drawer-lifecycle-contracts.pt-BR.md`

## Manual, Programatico, Copiloto E Autonomo

| Modo | Cobertura na pagina Hoje |
| --- | --- |
| Manual | Usuario abre itens, resolve na origem, cria tarefa/caso/aprovacao, delega, conclui. |
| Programatico | CRM cria prioridades, tarefas, alertas, checklist, bloqueios e historico sem IA. |
| Copiloto | Agente resume, explica prioridade, sugere texto, sugere proxima acao e preenche detalhes. |
| Autonomo | Executa apenas acoes seguras; em risco, cota ou falta de dado, cria fallback manual. |

## Planos 0, 1, 3 E 7 Agentes

| Plano | Comportamento esperado |
| --- | --- |
| 0 agentes | Hoje continua completo por regras, tarefas, aprovacoes, origem e caminho manual. |
| 1 agente | IA aparece apenas nos dominios cobertos pelo agente ativo. |
| 3 agentes | IA aparece nos dominios do bundle ativo, sem bloquear o resto do CRM. |
| 7 agentes | IA pode cobrir todos os dominios, respeitando cota, permissao, risco e auditoria. |

## Pontos Ainda Abertos

Estes pontos nao bloqueiam a pagina Hoje v0.1, mas devem ser fechados antes de implementacao final:

1. **Formula de priorizacao do Agora**
   - pesos de prazo, impacto, risco, fila, cota, dinheiro, alunos afetados e agente pausado.

2. **Empty states por bloco**
   - sem fila humana;
   - sem bloqueios;
   - sem aprovacoes;
   - sem dinheiro critico;
   - checklist completo;
   - sem tarefas pendentes.

3. **Permissoes por papel**
   - gestor;
   - recepcao/operacao;
   - financeiro;
   - professor;
   - admin.

4. **Mobile**
   - app mobile nao deve copiar a web;
   - precisa de lista priorizada e detalhe mobile.

5. **Drawers visuais dos demais tipos**
   - imagem 18 cobre tarefa;
   - os demais drawers estao contratados, mas ainda nao foram gerados visualmente.

## Decisao De Produto

Para a fase atual de geracao web, a familia **Hoje** pode ser considerada suficiente para seguir para a proxima familia de paginas, com as pendencias acima registradas.

Nao e necessario gerar todos os drawers agora, desde que o contrato de ciclo seja usado na implementacao e em futuras rodadas de imagem.
