# Design System Web - Rodada 4.1C - Pagina Aprovacoes

> Status: aprovada v0.1. Esta documentacao registra a imagem da rota `/app/aprovacoes`, cobrindo lista de decisoes e detalhe lateral de aprovacao.

## Arquivo

Arquivo aprovado:

`25_round-4.1C_aprovacoes_01_lista-decisao-detalhe.png`

Arquivos locais observados:

- `D:\Downloads\25_round-4.1C_aprovacoes_01_lista-decisao-detalhe.png.png`
- `D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\25_round-4.1C_aprovacoes_01_lista-decisao-detalhe.png.png`

Nome canonico:

`25_round-4.1C_aprovacoes_01_lista-decisao-detalhe.png`

## Decisao Central

**Aprovacoes** responde:

```text
Quais decisoes precisam de autorizacao humana antes do CRM, equipe ou agente seguir?
```

Aprovacao nao e tarefa.

Aprovacao nao e checklist.

Aprovacao e uma decisao auditavel com:

- origem canonica;
- solicitante, equipe, sistema ou agente;
- tipo;
- risco;
- impacto;
- custo ou cota quando aplicavel;
- politica/guardrail;
- proposta;
- historico;
- decisao humana.

## Rota Coberta

| Rota | Cobertura |
| --- | --- |
| `/app/aprovacoes` | Coberta pela imagem 25. |
| `/app/aprovacoes/[approvalId]` | Coberta parcialmente pelo painel lateral de detalhe. Pode virar rota/drawer profundo no futuro se necessario. |

## Layout Aprovado

A pagina usa:

- App Shell web aprovado;
- topbar do grupo com `Pendencias`, `Tarefas`, `Checklists`, `Aprovacoes`, `Incidentes` e `Historico`;
- `Aprovacoes` ativo;
- titulo `Aprovacoes`;
- subtitulo `Decisoes aguardando revisao humana`;
- busca e filtros por tipo, risco, origem, status e responsavel;
- lista central de aprovacoes;
- coluna esquerda com filas/tipos;
- painel direito com detalhe da aprovacao selecionada.

## Blocos Validados

| Bloco | Papel |
| --- | --- |
| Filtros superiores | Encontrar aprovacoes por busca, tipo, risco, origem, status e responsavel. |
| Filas laterais | Separar Todas, Hoje, Alta prioridade, Mensagens, Agenda, Financeiro, Agentes, Dados e Comunicados. |
| Lista central | Mostrar decisoes pendentes ou em revisao com origem, risco, custo/cota, prazo e status. |
| Painel direito | Mostrar contexto, proposta, impacto, politica, historico, comentario e acoes. |
| Paginacao | Permitir volume maior sem virar dashboard. |

## Conteudo Minimo Da Lista

Cada aprovacao deve mostrar:

- titulo;
- tipo;
- origem canonica;
- solicitante, equipe, sistema ou agente;
- risco;
- custo/cota quando existir;
- prazo;
- status;
- ultima atividade.

Exemplos validados na imagem:

- `Aprovar mensagem para Ana Paula`;
- `Aprovar alteracao de agenda`;
- `Aprovar excecao financeira`;
- `Aprovar comunicado de reposicao`;
- `Aprovar acao autonoma bloqueada`;
- `Aprovar correcao de cadastro`.

## Painel Direito

O painel direito representa o detalhe da decisao selecionada.

Na imagem aprovada, o exemplo e:

`Aprovar mensagem para Ana Paula`

Campos validados:

- badge `Aprovacao`;
- titulo;
- status;
- tipo;
- origem canonica;
- solicitante/agente;
- risco;
- custo/cota;
- prazo;
- contexto resumido;
- proposta principal;
- impacto esperado;
- politica/guardrail aplicado;
- historico;
- comentario recente;
- acoes.

Regra do painel direito:

- por padrao, `/app/aprovacoes` pode carregar sem aprovacao selecionada;
- a imagem aprovada mostra uma decisao selecionada, nao o estado inicial obrigatorio;
- o painel direito e contextual e muda conforme a aprovacao clicada;
- aprovacao continua sendo decisao humana: o agente pode preparar, explicar ou executar depois, mas nao aprovar sozinho.

Modos principais do painel de Aprovacao:

| Item clicado | Painel direito deve mostrar |
| --- | --- |
| Aprovacao pendente | Proposta, origem, risco, impacto, custo/cota, politica aplicada e acoes de aprovar, editar, rejeitar ou pedir dados. |
| Aprovacao de mensagem | Texto sugerido, canal, destinatario, consentimento, risco de linguagem e edicao antes de aprovar. |
| Aprovacao financeira/sensivel | Valor, regra, impacto, permissao, auditoria obrigatoria e acoes restritas. |
| Aguardando dados | Dado faltante, quem precisa informar, ultima solicitacao e acoes de pedir dados ou cancelar. |
| Aprovada/rejeitada | Decisao tomada, autor, data, justificativa, execucao posterior e link para origem. |
| Expirada/bloqueada | Motivo, politica, risco, acao manual permitida e proxima decisao segura. |

## Acoes Validadas

| Acao | Regra |
| --- | --- |
| `Aprovar` | Autoriza a proposta e registra auditoria. |
| `Editar` | Permite ajustar a proposta antes de aprovar. |
| `Rejeitar` | Recusa a proposta com motivo. |
| `Pedir dados` | Solicita informacao adicional antes da decisao. |
| `Abrir origem` | Abre a superficie canonica onde o dado ou conversa nasceu. |

## Relacao Com Agentes

Regra aprovada:

**Agente nunca aprova sozinho.**

Agentes podem:

- criar sugestao;
- preparar proposta;
- estimar risco;
- calcular custo/cota;
- explicar impacto;
- bloquear execucao quando politica exigir revisao;
- executar depois que a decisao humana aprovar, se o modo e a politica permitirem.

Agentes nao podem:

- aprovar decisao sensivel;
- ocultar risco;
- executar acao bloqueada por politica;
- consumir cota sem registro;
- apagar historico da decisao.

## Relacao Com Outras Paginas

| Superficie | Papel |
| --- | --- |
| Aprovacoes | Decidir se uma proposta pode seguir. |
| Tarefas | Executar trabalho humano unitario. |
| Checklists | Executar rotinas com varios passos. |
| Hoje | Priorizar aprovacoes que precisam decisao hoje. |
| Operacao | Acompanhar uma aprovacao como pendencia quando ela trava andamento. |
| Origem | Guarda o dado real, conversa, agenda, financeiro, cadastro ou fluxo. |

Regra aprovada:

- uma aprovacao pode nascer de agente, sistema, equipe ou origem canonica;
- uma aprovacao pode gerar tarefa depois de rejeitada ou ao pedir dados;
- uma tarefa pode pedir uma aprovacao antes de concluir;
- isso nao transforma aprovacao em tarefa.

## Estados Cobertos

- Pendente;
- Em revisao;
- Bloqueada por politica;
- risco baixo;
- risco medio;
- risco alto;
- com custo/cota;
- sem custo/cota.

Estados futuros nao representados, mas esperados:

- aprovada;
- rejeitada;
- expirada;
- editada;
- executada;
- falha apos aprovacao;
- aguardando dados.

## Planos E Modos

| Plano/modo | Comportamento |
| --- | --- |
| 0 agentes | Aprovacoes funcionam para equipe, regras programaticas, financeiro, agenda, dados e comunicados. |
| 1 agente | Aprovacoes de agente aparecem apenas no dominio coberto pelo agente ativo. |
| 3 agentes | Dominios ativos podem gerar propostas, risco, custo/cota e pedido de aprovacao. |
| 7 agentes | Todos os dominios podem gerar propostas, respeitando permissao, cota, politica e auditoria. |
| Manual | Usuario cria, revisa, aprova, edita, rejeita, pede dados e abre origem. |
| Copiloto | Sugere texto, resume contexto, estima risco, prepara proposta e explica impacto. |
| Autonomo | Nao aprova sozinho; quando bloqueado, envia para esta fila. |

## O Que Nao Deve Aparecer

- Kanban como visualizacao principal;
- checklist como estrutura principal;
- lista generica de tarefas;
- dashboard de KPIs;
- aprovacoes sem origem;
- aprovacoes sem risco/impacto quando a acao for sensivel;
- IA como decisora final;
- execucao sem auditoria.

## Observacao Sobre CTA

O botao `Criar aprovacao` foi aceito visualmente nesta imagem, mas deve ser tratado com cuidado em produto.

Preferencia futura:

- `Nova solicitacao`, quando a aprovacao for aberta manualmente;
- ou remover CTA global quando todas as aprovacoes nascerem de origem, agente, regra ou fluxo.

Isso nao bloqueia a imagem v0.1.

## Referencias

- `design-system-round-4-1C-tarefas-image-plan.pt-BR.md`
- `design-system-round-4-1C-checklists-approved.pt-BR.md`
- `agent-guardrails-evals-contract.pt-BR.md`
- `drawer-lifecycle-contracts.pt-BR.md`
- `audit-touchpoints.pt-BR.md`
