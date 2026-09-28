# Design System Web - Rodada 4.1A - Hoje 03 Estado Critico Aprovado

> Status: imagem aprovada v0.1. Esta documentacao registra a terceira imagem da pagina Hoje, mostrando a tela em estado critico do dia.

## Arquivo

Arquivo aprovado:

`19_round-4.1A_hoje_03_estado-critico-do-dia.png`

Arquivos locais observados:

- `D:\Downloads\19_round-4.1A_hoje_03_estado-critico-do-dia.png`
- `D:\Downloads\19_round-4.1A_hoje_03_estado-critico-do-dia.png.png`
- `D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\19_round-4.1A_hoje_03_estado-critico-do-dia.png`
- `D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\19_round-4.1A_hoje_03_estado-critico-do-dia.png.png`

Nome canonico:

`19_round-4.1A_hoje_03_estado-critico-do-dia.png`

## Objetivo Da Imagem

Validar que a pagina **Hoje** suporta um dia sob pressao operacional sem virar dashboard generico e sem transformar tudo em tarefa.

A imagem mostra:

- fila humana acima do normal;
- reposicoes sem encaixe;
- cota em modo de atencao/economia;
- bloqueios de agenda/dados/cota;
- tarefas pendentes e atrasadas;
- aprovacoes pendentes;
- dinheiro que exige acao hoje;
- checklist com item critico pendente;
- aulas com chamada pendente, lotacao e conflito.

## Estado Representado

O studio esta em um dia critico.

Nao ha drawer aberto.

A pagina continua sendo a mesa de comando do dia e responde:

```text
O que precisa acontecer hoje para o studio nao travar?
```

## Blocos Validados

| Bloco | Estado critico validado |
| --- | --- |
| Agora | Prioridades urgentes por fila humana, reposicao e cota. |
| Checklist do dia | Item critico de pagamentos pendente. |
| Aulas de hoje | Chamada pendente, aula lotada e sala em conflito. |
| Fila humana | 18 aguardando, com tempos de espera por origem. |
| Bloqueios de hoje | Sala em conflito, cadastro incompleto, cota em economia. |
| Tarefas de hoje | 9 pendentes e 3 atrasadas. |
| Aprovacoes de hoje | 5 pendentes com risco, impacto e cota. |
| Dinheiro hoje | R$ 2.020 exigem acao hoje. |

## Regras Funcionais Confirmadas

- Estado critico nao abre drawer por padrao.
- Itens continuam clicaveis por chevron/affordance.
- Acoes permanecem nos drawers ou origens, nao nos cards.
- Hoje nao vira lista unica de tarefas.
- Cota pode aparecer como prioridade e como bloqueio, desde que represente impacto diferente:
  - em `Agora`, aparece como prioridade do dia;
  - em `Bloqueios`, aparece como causa operacional.
- Itens tem origem implicita ou explicita: WhatsApp, Agenda, Uso/Cotas, Dados, Tarefas, Aprovacoes e Financeiro.

## Relacao Com Planos E Agentes

| Contexto | Comportamento esperado |
| --- | --- |
| 0 agentes | Estado critico ainda funciona por regras programaticas, tarefas, aprovacoes e caminhos manuais. |
| 1 agente | Apenas itens do dominio do agente ativo recebem sugestao/caminho de IA. |
| 3 agentes | Atendimento, Agenda e Vendas podem ter sugestoes se forem o bundle ativo. |
| 7 agentes | Todos os dominios podem ter sugestoes/autonomia permitida, mas cota, risco e permissao continuam valendo. |
| Manual | Usuario abre origem, cria tarefa/caso, aprova, delega ou resolve. |
| Copiloto | Agente explica prioridade, resume contexto e sugere proxima acao. |
| Autonomo | So executa acoes seguras; cota 90% pode converter baixa prioridade em tarefa/aprovacao/manual. |

## Pontos De Atencao

O exemplo `Cota em 92% afetando comunicados` aparece em `Agora` e tambem como bloqueio. Isso e aceitavel se:

- em `Agora` representar item priorizado;
- em `Bloqueios` representar causa operacional;
- o drawer ou origem explicar o impacto concreto.

Em iteracoes futuras, se a duplicidade visual incomodar, o bloqueio pode ser trocado por:

- integracao instavel;
- contato sem consentimento;
- reposicao sem vaga compativel;
- dado obrigatorio ausente.

## O Que Nao Deve Mudar

- Nao adicionar graficos.
- Nao adicionar KPIs soltos.
- Nao transformar tudo em tarefa.
- Nao abrir drawer nessa imagem.
- Nao duplicar a pagina Operacao/Jornadas.
- Nao transformar Hoje em relatorio.

## Fontes Relacionadas

- `design-system-round-4-1A-hoje-image-plan.pt-BR.md`
- `hoje-actionable-item-taxonomy.pt-BR.md`
- `drawer-lifecycle-contracts.pt-BR.md`
- `agent-plan-entitlements.pt-BR.md`
- `route-agent-mode-entitlement-matrix.pt-BR.md`
