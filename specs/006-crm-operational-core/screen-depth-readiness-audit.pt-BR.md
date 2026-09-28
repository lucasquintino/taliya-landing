# Auditoria de profundidade das telas - PT-BR

> Status: rodada de revisao sobre profundidade. Este documento responde se as paginas/telas web e mobile ja estao 100% prontas para design e implementacao.

## Veredito

Nao, ainda nao esta 100%.

O que temos hoje esta forte para **mapa de produto**:

- quais paginas existem;
- quais rotas agrupam cada pagina;
- o que cada pagina precisa conter;
- onde ficam topo, esquerda, centro, direita e mobile;
- quais casos de uso cada pagina cobre;
- quais areas devem ser web-first ou mobile-first.

Mas ainda falta chegar no nivel de **especificacao de tela pronta para design/implementacao**.

## Diferenca entre mapa e especificacao final

| Nivel | Estado atual | Falta |
| --- | --- | --- |
| Produto | Bom | Ajustes finos de decisao. |
| Paginas web | Bom | Campos, componentes, colunas, botoes, estados e permissao. |
| App mobile | Bom como direcao | Fluxos tela a tela e profundidade por papel. |
| Casos de uso | Cobertos | Aceite final, merge/defer/out quando necessario. |
| Agentes | Bem mapeados | Configuracao versionada, rollback e limites por fluxo em detalhe. |
| Cotas | Bem conceituadas | Como aparecem em cada tela/acao. |
| Permissoes | Parcial | Matriz por papel ainda precisa virar regra de tela. |

## O que ja esta suficiente

### 1. Quantidade e agrupamento

Esta parte esta consistente:

```text
12 menus principais web
38 paginas/superficies funcionais
158 rotas mapeadas
157 casos de uso cobertos
96 fluxos fortes de agentes
2 fluxos opcionais
```

Nao parece que falta uma grande area de produto agora.

### 2. Separacao web vs mobile

Tambem esta correta:

- web = operacao completa, configuracao, auditoria, agentes, cotas, relatorios e governanca;
- mobile = trabalho do dia, conversa, agenda, chamada, tarefas, aprovacoes, casos urgentes e alertas.

### 3. Direcao visual

A direcao esta correta:

```text
CRM por jornadas, cartoes, contexto lateral e acoes rapidas.
```

O risco agora nao e direcao. O risco e detalhe insuficiente por tela.

## O que ainda falta aprofundar

### 1. Campos exatos por tela

Para cada tela precisamos definir:

- campos obrigatorios;
- campos opcionais;
- campos sensiveis;
- campos calculados;
- campos editaveis;
- campos somente leitura;
- validações;
- mensagens de erro.

Exemplo: em `Aluno`, ainda sabemos que precisa de perfil, plano, agenda, pagamentos, presencas, riscos e timeline. Falta definir exatamente quais campos aparecem em cada bloco.

### 2. Botoes e acoes por estado

Hoje temos acoes essenciais, mas ainda falta a matriz:

```text
se status = X, mostrar botoes A/B/C
se permissao = Y, esconder ou bloquear botao Z
se cota = 90%, trocar automacao por aprovacao
se dado sensivel, exigir confirmacao
```

### 3. Estados vazios, erro e bloqueio

Cada tela precisa ter:

- estado vazio;
- carregando;
- erro;
- sem permissao;
- dado incompleto;
- cota perto do limite;
- cota esgotada;
- agente pausado;
- aguardando humano;
- conflito de dados;
- acao bloqueada.

### 4. Permissao por papel

Esse e o maior buraco antes de design/implementacao.

Precisamos mapear por papel:

- dono;
- admin;
- recepcao/operacao;
- financeiro;
- professor;
- agente/runtime;
- suporte Taliya.

E para cada papel:

- pode ver;
- pode editar;
- pode aprovar;
- pode executar;
- pode exportar;
- pode ver dado sensivel;
- pode acionar agente;
- pode pausar automacao.

### 5. Mobile por papel

O app mobile precisa decidir quem usa o que:

- gestor/dono;
- recepcao;
- professor;
- financeiro;
- admin.

Sem isso, o app pode ficar grande demais ou expor coisa sensivel.

### 6. Profundidade de agentes por tela

Ainda falta detalhar exatamente:

- onde aparece sugestao da IA;
- onde aparece botao contextual;
- quando existe "preparar resposta";
- quando existe "executar agora";
- quando vira aprovacao;
- quando fica bloqueado;
- quando consome cota;
- quando aparece simulacao.

### 7. Versionamento de configuracao

Principalmente em:

- agentes;
- fluxos;
- politicas;
- regras de economia;
- templates;
- permissoes.

Precisamos explicitar:

- rascunho;
- simulacao;
- publicacao;
- versao ativa;
- historico;
- rollback;
- auditoria.

## Profundidade atual por grupo de tela

| Grupo | Estado | Proxima rodada necessaria |
| --- | --- | --- |
| Hoje | Bom mapa | Definir cards, prioridades e regras de ordenacao. |
| Inbox/conversas | Bom mapa | Definir layout de conversa, botoes, anexos, handoff e opt-out. |
| Alunos/perfil | Bom mapa | Definir blocos, campos, permissoes e acoes por status. |
| Historico sensivel | Parcial | Definir permissao fina, consentimento, anamnese e visibilidade. |
| Agenda/aula/chamada | Bom mapa | Definir estados de aula, chamada, falta, reposicao e conflito. |
| Vendas/interessados | Bom mapa | Definir etapas do pipeline, campos de lead e conversao. |
| Financeiro | Parcial | Definir travas, aprovacao, impacto, conciliacao e auditoria. |
| Retencao | Bom mapa | Definir score/risco, listas e acoes recomendadas. |
| Reclamacoes | Parcial | Definir severidade, escalonamento, automacao pausada e recuperacao. |
| Jornadas/operacao | Bom conceito | Definir colunas/etapas, tipos de cartao e regras de movimento. |
| Tarefas | Bom mapa | Definir status, SLA/prazo, dono e recorrencia. |
| Aprovacoes | Bom mapa | Definir antes/depois, edicao, expiracao e impacto. |
| Agentes/fluxos | Parcial | Definir configuracao versionada, limites, simulacao, rollback. |
| Execucoes/incidentes | Parcial | Definir logs, explicacao, impacto e reprocessamento seguro. |
| Uso/cotas | Bom conceito | Definir visual por tela e comportamento por limite. |
| Relatorios | Enxuto ok | Definir quais relatorios entram no primeiro design. |
| Configuracoes | Parcial | Definir formularios e dependencias entre regras. |
| Politicas | Parcial | Definir versionamento e simulacao com detalhe. |
| Mobile | Bom mapa | Definir fluxo tela a tela por papel. |

## O que eu faria agora

Faria uma rodada chamada:

```text
Especificacao de tela por tela
```

Com uma ficha padrao para cada tela:

| Campo | Pergunta |
| --- | --- |
| Objetivo da tela | Para que ela existe? |
| Usuario principal | Quem usa mais? |
| Rotas | Quais rotas entram aqui? |
| Blocos | Quais secoes aparecem? |
| Dados | Quais campos aparecem? |
| Acoes | Quais botoes existem? |
| Estados | Quais estados precisam existir? |
| Permissoes | Quem pode ver/fazer o que? |
| IA | Onde a IA sugere/executa/bloqueia? |
| Cotas | Onde aparece custo ou limite? |
| Mobile | Como isso vira app ou nao vira? |
| Auditoria | O que precisa registrar? |

## Priorizacao da proxima passada

Nao recomendo detalhar as 38 telas com o mesmo peso de uma vez.

Ordem ideal:

1. Hoje
2. Inbox/conversas
3. Alunos/perfil
4. Agenda/aula/chamada/reposicoes
5. Vendas/interessados/experimental/matricula
6. Financeiro/pagamentos/casos financeiros
7. Jornadas/operacao/tarefas/aprovacoes
8. Agentes/fluxos/execucoes/uso-cotas
9. Retencao/reclamacoes/cancelamentos
10. Historico/professor
11. Configuracoes/politicas/permissoes
12. Relatorios/admin/billing/exportacoes

## Conclusao

Estamos no caminho certo, mas nao chamaria de 100%.

O estado correto hoje e:

```text
Mapa de produto: consistente.
Mapa web/mobile: consistente.
Profundidade por tela: suficiente para discutir, ainda insuficiente para design final.
```

Proxima etapa recomendada:

```text
criar uma especificacao detalhada tela a tela, com campos, botoes, estados, permissoes, IA, cotas e auditoria.
```
