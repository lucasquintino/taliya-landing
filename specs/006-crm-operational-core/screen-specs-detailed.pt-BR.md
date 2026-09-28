# Especificacao profunda de telas - PT-BR

> Status: indice canonico v0.1. As fichas completas das telas vivem nas Rodadas 1-7; este documento define o contrato que cada ficha deve cumprir.

## Regra central

Uma tela so esta pronta para design/prototipo/implementacao quando descreve conteudo, layout funcional, dados, acoes, estados, permissoes, IA, cotas, auditoria, fallback e equivalente web/mobile.

## Ficha padrao por tela

```text
Nome
Tipo: web, mobile ou ambos
Objetivo
Usuario principal
Usuarios secundarios
Rotas relacionadas
Casos de uso cobertos
Fluxos de agente relacionados
Objetos de negocio usados
Fonte da verdade dos dados
Ciclo de vida afetado
Blocos da tela
Zona principal
Zona lateral/secundaria
Modais/gavetas relacionados
Componentes esperados
Campos exibidos
Campos editaveis
Campos obrigatorios
Campos sensiveis
Acoes/botoes
Posicao dos botoes
Acao manual
Acao com copiloto
Acao autonoma
Estados vazios
Estados de carregamento
Estados de erro
Estados bloqueados
Permissoes
IA/agentes
Cotas
Auditoria
Integracoes
Fallbacks
Web/mobile equivalente
Operacao sem agentes
Metricas afetadas
Fora de escopo desta tela
Decisoes pendentes
```

## Regras para preencher fichas

- Nao usar "etc." em campos, botoes ou estados.
- Se uma acao for sensivel, citar permissao e auditoria.
- Se uma acao usar agente, citar modo, cota e fallback.
- Se a tela existir no app, dizer o que e completo, parcial ou apenas consulta.
- Se uma tela for web-first, explicar por que.
- Se uma tela for mobile essencial, explicar qual tarefa do dia ela resolve.

## Controle por rodada

Observacao: este arquivo nao duplica todas as fichas. Para gerar prototipos ou telas no ChatGPT, usar as fichas dos documentos `round-1` a `round-7` como fonte funcional e este arquivo como checklist de completude.

| Rodada | Grupo de telas | Status |
| --- | --- | --- |
| 1 | Setup, configuracoes essenciais e agentes iniciais | v0.1 em `round-1-activation-setup-spec.pt-BR.md` |
| 2 | Hoje, jornadas/operacao, tarefas, aprovacoes, notificacoes, checklist e caso operacional | v0.1 em `round-2-daily-command-spec.pt-BR.md` |
| 3 | Inbox, contatos, alunos, historico, professor | v0.1 em `round-3-attendance-students-history-spec.pt-BR.md` |
| 4 | Agenda, turmas, aula, chamada, reposicoes | v0.1 em `round-4-schedule-classes-replacements-spec.pt-BR.md` |
| 5 | Vendas, experimental, matricula, comunicados | v0.1 em `round-5-sales-trials-enrollment-communications-spec.pt-BR.md` |
| 6 | Financeiro, contratos, retencao, cancelamentos, reclamacoes, privacidade | v0.1 em `round-6-finance-retention-sensitive-spec.pt-BR.md` |
| 7 | Agentes, execucoes, cotas, relatorios, integracoes, auditoria, billing, suporte | v0.1 em `round-7-agents-quotas-governance-spec.pt-BR.md` |

## Saida para Rodada 11

Quando uma ficha estiver pronta, ela deve ser suficiente para alimentar `chatgpt-screen-generation-prompts.pt-BR.md` sem o ChatGPT inventar produto.
