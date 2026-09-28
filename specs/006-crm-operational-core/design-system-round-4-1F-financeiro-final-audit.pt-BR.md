# Rodada 4.1F - Auditoria Final Da Familia Financeiro Web

> Status: v0.1 fechado em 13/05/2026. Esta auditoria consolida as decisoes visuais e funcionais da familia Financeiro antes de seguir para outras familias.

## Topbar Final

A topbar interna final da familia Financeiro fica:

```text
Visao geral | Kanban | Movimentacoes | Documentos
```

Nao existe aba `Casos` no MVP. Casos financeiros sensiveis sao resolvidos nas superficies existentes por fila, card, drawer, aprovacao, tarefa, aluno ou operacao.

## Rotas Fechadas

| Rota | Papel | Cobertura visual |
| --- | --- | --- |
| `/app/financeiro` | Central de filas financeiras e prioridades do periodo. | `30_round-4.1F_financeiro_01_visao-geral-filas.png` |
| `/app/financeiro` com item selecionado | Estado com drawer de cobranca/pagamento/pendencia selecionada. | `32_round-4.1F_financeiro_02_drawer-cobranca-selecionada.png` |
| `/app/financeiro/kanban` | Operacao visual por etapa para volume de cobrancas e pendencias. | `33_round-4.1F_financeiro_03_kanban-financeiro.png` |
| `/app/financeiro/movimentacoes` | Consulta completa, auditoria e filtros de mensalidades, cobrancas, pagamentos, falhas, promessas, comprovantes, conciliacao, estornos, descontos e ajustes. | `34_round-4.1F_financeiro_04_movimentacoes-filtros-drawer.png` |
| `/app/financeiro/documentos` | Documentos financeiros, contratos, recibos, notas, comprovantes e anexos. | Herdada; sem imagem nova. |

## Auditoria Como Usuario Financeiro Do Studio

Como responsavel pelo financeiro do studio, a familia cobre o trabalho diario sem obrigar o usuario a navegar por paginas demais:

- `Visao geral` responde o que precisa de acao agora: atrasos, vencimentos, comprovantes, falhas, promessas, excecoes e prioridades.
- `Kanban` organiza volume quando a equipe precisa acompanhar muitas cobrancas em paralelo.
- `Movimentacoes` permite procurar, filtrar, auditar e operar qualquer registro financeiro.
- `Documentos` guarda e opera os arquivos relacionados sem misturar arquivo com cobranca.

O modelo evita uma pagina separada de casos financeiros porque isso criaria duplicidade. O mesmo problema financeiro pode nascer de uma mensalidade, comprovante, falha, promessa, desconto, estorno, ajuste ou acordo; a rota correta e a origem financeira, com encaminhamento para aprovacao ou tarefa quando houver decisao humana.

## Auditoria Tecnica

As quatro rotas cobrem os modelos principais definidos em `billing-lesson-consumption-models.pt-BR.md`:

- mensalidade fixa;
- cobranca por frequencia;
- pacote de aulas;
- recorrencia com creditos;
- aula avulsa;
- contrato parcelado;
- modelo customizado;
- ajustes manuais e excecoes controladas.

As telas tambem preservam separacao de responsabilidades:

- dinheiro cobrado fica em Financeiro;
- credito operacional de aula fica em Agenda/Reposicoes, aparecendo em Financeiro apenas quando houver impacto financeiro;
- documentos ficam em Documentos;
- decisao sensivel fica em Aprovacoes;
- trabalho humano fica em Tarefas;
- contexto do aluno fica no perfil do aluno;
- incidente cruzando areas fica em Operacao.

## IA, Planos E Modos

Com 0 agentes, toda a familia continua funcional em modo manual: filtros, filas, kanban, movimentacoes, documentos, tarefas e aprovacoes.

Com agente Financeiro ativo, a IA pode:

- resumir historico;
- priorizar filas;
- redigir lembretes;
- sugerir proxima acao;
- preparar aprovacao;
- criar tarefa segura quando permitido.

Em modo copiloto, a sugestao aguarda revisao humana. Em modo autonomo, so lembretes simples e acoes explicitamente permitidas por politica podem executar sem aprovacao. Desconto, acordo, estorno, disputa, bloqueio/liberacao, cortesia, perdao de divida e alteracao sensivel de plano continuam humanos.

## O Que Fica Fora Do MVP

- Pagina propria de `Casos financeiros`.
- Rota `/app/financeiro/casos`.
- Rota dedicada de excecoes financeiras.
- Dashboard contabil/gerencial avancado.
- Fechamento financeiro completo.
- Previsao de caixa avancada.
- Imagem propria para `/app/financeiro/documentos`.
- Paginas separadas para cobrancas, pagamentos e conciliacao quando a mesma necessidade ja esta coberta por `Movimentacoes`, `Kanban` ou `Visao geral`.

## Conclusao

A familia Financeiro esta suficiente para gerar as rotas web do MVP:

- tem uma entrada rapida para o dia/semana/mes;
- tem operacao visual por etapa;
- tem consulta completa auditavel;
- tem documentos financeiros como rota herdada;
- tem regras claras para excecoes sensiveis;
- funciona com 0, 1, 3 ou 7 agentes sem depender da IA.

Se uma necessidade futura exigir nova imagem, ela deve provar mudanca real de modelo mental, nao apenas troca de filtro ou texto de drawer.
