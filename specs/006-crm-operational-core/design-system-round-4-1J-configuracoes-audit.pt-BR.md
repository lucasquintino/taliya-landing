# Rodada 4.1J - Auditoria Da Familia Configuracoes

Status: rascunho de auditoria antes de decidir imagens finais.
Data: 2026-05-13.
Escopo: configuracoes do studio, agentes, fluxos dos agentes, politicas, cotas, integracoes, billing, privacidade e auditoria.

> Nota 2026-05-24: este documento e historico. A decisao final de Configuracoes Pos-Go-Live esta em `post-go-live-configuration-master-map.pt-BR.md`, `post-go-live-configuration-field-contracts.pt-BR.md`, `post-go-live-configuration-state-contracts.pt-BR.md` e `post-go-live-configuration-final-audit.pt-BR.md`.
>
> Rotas como `/app/configuracoes/agenda/consumo-aulas`, `/app/configuracoes/financeiro`, `/app/configuracoes/politicas`, `/app/configuracoes/privacidade`, `/app/configuracoes/templates`, `/app/configuracoes/vendas`, `/app/configuracoes/retencao`, `/app/configuracoes/recursos` e `/app/configuracoes/campos` nao fazem parte da familia final de Configuracoes Pos-Go-Live do MVP.

## Documentos usados

- `web-screen-map.pt-BR.md`
- `design-system-round-4-0-web-page-blueprints.pt-BR.md`
- `design-system-round-4-image-coverage-strategy.pt-BR.md`
- `design-system-round-4-1I-relatorios-gestao-image-plan.pt-BR.md`
- `final-screen-contract-matrix.pt-BR.md`
- `product-depth-matrix.pt-BR.md`
- `round-7-agents-quotas-governance-spec.pt-BR.md`
- `agent-flow-cardinality-audit.md`
- `agent-flow-screen-coverage.pt-BR.csv`
- `route-agent-mode-entitlement-matrix.pt-BR.md`
- `agent-plan-entitlements.pt-BR.md`
- `agent-guardrails-evals-contract.pt-BR.md`
- `billing-lesson-consumption-models.pt-BR.md`
- `source-of-truth-matrix.pt-BR.md`
- `permissions-matrix.pt-BR.md`
- `docs/taliya-agent-flow-configuration-plan.md`
- `docs/taliya-agent-flow-configuration-matrix.md`
- Imagens aprovadas/geradas das rodadas 3B, 3C e 4.1.

## Conclusao principal

Configuracoes nao deve ser uma pagina unica gigante. Ela deve ser uma familia com um hub e secoes profundas, porque mistura tres tipos de coisa:

1. Configuracoes de base do CRM: studio, equipe, permissao, notificacao, campos, templates.
2. Regras operacionais que afetam humanos e agentes: agenda, reposicao, financeiro, cobranca, consumo de aulas, vendas, retencao.
3. Configuracao pos-go-live de agentes e fluxos: agentes, pacotes de fluxo, builder de fluxo, modo, aprovacao, fallback, simulacao e publicacao.
4. Planos de controle: cotas, execucoes, incidentes, integracoes, auditoria, privacidade e billing.

A decisao mais importante e separar "configurar o studio" de "controlar automacoes". Se tudo ficar escondido em `/app/configuracoes`, o gestor perde clareza sobre o que e ajuste simples, o que muda comportamento dos agentes e o que tem impacto financeiro, legal ou operacional.

## Regra de separacao

Use esta regra para decidir onde cada coisa mora:

- Se muda dados fixos do studio, fica em `Configuracoes`.
- Se muda regra usada por humanos e agentes, fica em `Politicas` ou em uma configuracao operacional com simulacao/impacto.
- Se muda cadastro superficial do agente, fica em `Agentes`.
- Se muda o que um agente pode fazer em um processo, fica em `Agentes/Fluxos` como configuracao pos-go-live.
- Se muda custo, limite, plano contratado ou bloqueio por uso, fica em `Uso/Cotas` ou `Billing`.
- Se muda conexao externa, fica em `Integracoes`; se muda preferencia de canal/template, fica em `Configuracoes/Canais` ou `Templates`.
- Se e execucao, falha, bloqueio, incidente ou historico imutavel de quem fez o que, fica em Control Planes (`Controle`, `Uso`, `Integracoes`, `Auditoria`).

## Rotas MVP recomendadas

### Configuracoes base

- `/app/configuracoes`
  - Hub de configuracoes, status geral, pendencias de setup, atalhos para secoes criticas.
- `/app/configuracoes/studio`
  - Dados do studio, unidades, horarios comerciais, fuso, feriados/recessos simples.
- `/app/configuracoes/equipe`
  - Usuarios, convites, status, papeis atribuidos.
- `/app/configuracoes/permissoes`
  - Matriz por papel, permissoes sensiveis, solicitacoes de acesso.
- `/app/configuracoes/canais`
  - WhatsApp, e-mail e canais internos como preferencia operacional. O status tecnico completo continua em Integracoes.
- `/app/configuracoes/templates`
  - Modelos de mensagem, respostas rapidas, variaveis e tom.
- `/app/configuracoes/campos`
  - Campos customizados, tags, categorias e segmentos simples.
- `/app/configuracoes/notificacoes`
  - Alertas do gestor, equipe, limites, incidentes e aprovacoes.
- `/app/configuracoes/privacidade`
  - Preferencias de consentimento, retencao de dados e padroes LGPD.

### Configuracoes operacionais

- `/app/configuracoes/agenda`
  - Regras de agenda, aulas, reposicao, no-show, tolerancias, janelas e bloqueios simples.
- `/app/configuracoes/agenda/consumo-aulas`
  - Como presenca, falta, reposicao, aula avulsa e pacote consomem direito de aula.
- `/app/configuracoes/financeiro`
  - Regras financeiras gerais do studio, prazos, lembretes, metodos, cobranca e conciliacao.
- `/app/configuracoes/financeiro/modelos`
  - Modelos de cobranca e consumo: mensalidade fixa, frequencia mensal, pacote/creditos, recorrencia de creditos, aula avulsa, contrato parcelado, simples sem credito e hibrido.
- `/app/configuracoes/vendas`
  - Pipeline comercial, SLA de lead, origem, abordagem, proposta e follow-up.
- `/app/configuracoes/retencao`
  - Risco, cancelamento, pausa, salvamento, reativacao, reclamacao e tom de recuperacao.

### Agentes e fluxos pos-go-live

- `/app/agentes`
  - Agentes contratados/configurados, estado 0/1/3/7 agentes, area de atuacao, responsavel e status.
- `/app/agentes/[agentId]`
  - Detalhe do agente, canais, responsavel, fluxos vinculados, saude resumida e pendencias.
- `/app/agentes/[agentId]/fluxos`
  - Lista de fluxos daquele agente, status, risco, modo, pendencias e ultima publicacao.
- `/app/agentes/[agentId]/fluxos/[flowId]`
  - Configuracao profunda do fluxo: gatilho, condicao, acao, canal, mensagem, modo manual/copiloto/autonomo, aprovacao, limites, cotas, fallback, simulacao, teste, versao e publicacao.

Esta configuracao nao fica no setup inicial. O setup inicial pode apenas escolher agentes, responsaveis e pacotes de fluxos recomendados como rascunho.

### Planos de controle separados

- `/app/controle/agentes`
  - Saude dos agentes, pausas, riscos operacionais e acoes urgentes.
- `/app/controle/execucoes`
  - Execucoes, traces, bloqueios, falhas, retries e fallback manual.
- `/app/controle/incidentes`
  - Incidentes de agente, analise, reprocessamento seguro e abertura de tarefa.
- `/app/politicas`
  - Politicas operacionais versionadas. Deve ser canonica para regras sensiveis.
- `/app/uso`
  - Cotas, consumo, economia, bloqueios por limite, pacotes adicionais.
- `configuracao especifica da integracao`
  - Conexoes, status tecnico, logs, reconexao, jobs de importacao.
- `/app/auditoria`
  - Registro imutavel de mudancas, execucoes, aprovacoes e acessos.
- `/app/billing`
  - Plano Taliya, assinatura, faturas, add-ons, agentes contratados.
- `/app/privacidade/solicitacoes`
  - Solicitacoes LGPD operacionais, exportar/anonimizar/negar.

## O que nao entra como rota MVP

- Gargalos e Capacidade nao entram como rotas MVP dedicadas.
- Podem aparecer como indicadores dentro de Hoje, Agenda, Relatorios ou Operacao quando forem uteis.
- Configuracoes de recursos/salas/professores continuam necessarias em formato enxuto para agenda funcionar, mas isso nao cria uma familia de "capacidade" no MVP.

## Integracao com 0, 1, 3 e 7 agentes

### 0 agentes

- CRM completo continua ativo.
- Configuracoes de studio, agenda, financeiro, vendas e retencao funcionam manualmente.
- Secoes de agentes mostram estado educativo: sem agentes configurados, com CTA para contratar/configurar, sem bloquear o CRM.
- Politicas podem existir para padronizar operacao humana, mesmo sem automacao.

### 1 agente

- Apenas fluxos do agente contratado podem ser ativados.
- Configuracoes globais aparecem, mas cada fluxo mostra se esta incluido, bloqueado pelo plano ou aguardando setup.
- O gestor precisa ver impacto antes de ativar autonomia.

### 3 agentes

- Configuracao precisa deixar claro quais areas estao cobertas e quais continuam manuais.
- Exemplo recomendado: Atendimento, Agenda e Vendas.
- Financeiro/Retencao/Historico podem continuar como CRM manual, com sugestoes bloqueadas ou sem agente.

### 7 agentes

- Todas as familias podem ter fluxos configuraveis.
- A tela precisa priorizar controle, auditoria, cota e incidentes, nao apenas ativacao.
- Economia, fallback manual e aprovacao humana ficam mais importantes.

## Modos manual, copiloto e autonomo

Toda configuracao profunda de fluxo em Agentes/Fluxos deve permitir:

- Manual: o sistema organiza dados, filas, tarefas e aprovacoes; a pessoa executa.
- Copiloto: o sistema sugere, resume, redige, simula impacto e prepara acao.
- Autonomo: o agente executa apenas se passar por preflight de dados, permissao, politica, cota, canal, template, consentimento, risco e auditoria.

Publicar politica, alterar permissao, mudar plano/cobranca, perdoar pagamento, criar desconto sensivel, confirmar cancelamento irreversivel e mudar autonomia de fluxo nao devem ser autonomos.

No setup inicial, esses modos podem aparecer apenas como explicacao ou destino futuro. O onboarding nao deve publicar a configuracao profunda de modo/limite do fluxo; ele cria rascunho ou pendencia para configurar depois.

## Configuracoes que precisam mostrar impacto

Estas secoes nunca devem ser apenas formulario simples:

- Modelo de cobranca e consumo de aulas.
- Politicas de reposicao, falta, no-show e encaixe.
- Politicas financeiras de lembrete, cobranca, desconto, estorno e excecao.
- Modo dos fluxos dos agentes.
- Horarios/janelas de envio.
- Templates usados por agentes.
- Permissoes e papeis.
- Cotas, economia e fallback.
- Conexoes de WhatsApp, e-mail, gateway e importacao.

Cada uma precisa mostrar:

- Onde isso e usado.
- Quais rotas/fluxos serao afetados.
- Se afeta humanos, agentes ou ambos.
- O que muda para 0/1/3/7 agentes.
- Ultima alteracao e responsavel.
- Simulacao ou pre-visualizacao quando houver risco.

## Modelo de cobranca e consumo

A auditoria confirma que esse e um dos pontos mais criticos do produto.

O sistema deve separar:

1. Modelo de cobranca.
2. Direito de aula.
3. Regra de consumo.
4. Politica de reposicao.

Cada studio pode operar de forma diferente:

- mensalidade fixa por horario;
- mensalidade por frequencia;
- pacote de aulas/creditos;
- creditos recorrentes;
- aula avulsa;
- contrato parcelado;
- controle simples sem credito;
- modelo hibrido.

Tambem deve haver excecoes para "quebrar galho" do aluno:

- ajuste manual feito por usuario autorizado;
- sugestao do copiloto;
- proposta criada por agente para aprovacao;
- execucao autonoma apenas quando a politica permitir e o risco for baixo.

O agente nao pode inventar direito de aula, perdoar cobranca, dar desconto sensivel ou mudar consumo sem politica aprovada.

## Imagens necessarias

As imagens atuais ajudam bastante, mas Configuracoes ainda precisa de cuidado proprio.

### Necessarias

1. `Configuracoes - hub e detalhe de secao`
   - Mostra hub, secoes, status de setup, formulario central e painel de impacto/auditoria.
   - Serve para studio, equipe, permissoes, canais, templates, campos e notificacoes.

2. `Configuracoes - modelo de cobranca e consumo`
   - Mostra como configurar cobranca, direito de aula, consumo e reposicao.
   - Deve incluir impacto em Agenda, Financeiro, Perfil do aluno, Reposicoes e Agentes.

3. `Politicas operacionais - versao e simulacao`
   - Mostra regra versionada, simulador, diff antes/depois, aprovacao e publicacao.
   - Necessaria porque politicas afetam agentes e humanos.

### Separadas de Configuracoes

4. `Agentes e Fluxos`
   - Configuracao pos-go-live de agentes e fluxos, modo manual/copiloto/autonomo, preflight, fallback, simulacao e publicacao.

5. `Execucoes e Incidentes`
   - Control plane de trace, erro, fallback manual, reprocessamento seguro e incidente.

6. `Uso e Cotas`
   - Consumo, 70/90/100%, economia, bloqueios, pacote adicional e origem do uso.

### Herdadas, sem imagem nova inicialmente

- Integracoes: herda componentes de 3B.5/3C.1.
- Auditoria: herda 3C.3.
- Billing: herda 3B.5.
- Privacidade: herda 3C.3.
- Equipe/permissoes simples: herda 3B.1 e 3B.5, salvo se a matriz ficar complexa.

## Ajustes necessarios nos mapas atuais

1. Evitar duplicidade entre `/app/politicas` e `/app/configuracoes/politicas`.
   - Recomendacao: `/app/politicas` e rota canonica; Configuracoes apenas aponta para ela.

2. Separar `configuracao especifica da integracao` de `/app/configuracoes/canais`.
   - Canais configuram preferencia e templates.
   - Integracoes controlam conexao, logs, erro e reconexao.

3. Separar Financeiro do studio de Billing Taliya.
   - Financeiro do studio: alunos, mensalidades, cobrancas, pagamentos.
   - Billing: assinatura Taliya, agentes contratados, faturas e add-ons.

4. Tirar Gargalos/Capacidade do MVP como rotas dedicadas.
   - Continuam como indicadores ou blocos em rotas existentes.

5. Garantir que toda tela de configuracao sensivel tenha impacto, simulacao, permissao e auditoria.

## Riscos se decidirmos errado

- O gestor nao entende o que e configuracao simples versus automacao sensivel.
- Um ajuste financeiro pode quebrar agenda/reposicoes sem aviso.
- Um fluxo autonomo pode executar com regra desatualizada.
- O plano 0 agentes pode parecer incompleto, mesmo sendo CRM completo.
- Billing Taliya pode se misturar com financeiro do studio.
- Cotas podem parecer detalhe de plano, quando na pratica bloqueiam automacoes.
- Politicas podem virar "configuracoes soltas" sem versao, simulacao e aprovacao.

## Decisao recomendada para seguir

Antes de gerar imagens, fechar a arquitetura da familia Configuracoes em tres camadas:

1. Configuracoes do CRM.
2. Configuracoes operacionais por dominio.
3. Agentes/Fluxos como configuracao pos-go-live.
4. Planos de controle separados: Controle de execucoes/incidentes, Politicas, Uso/Cotas, Integracoes, Auditoria, Billing e Privacidade.

Depois disso, gerar apenas as imagens que realmente reduzem risco:

1. Hub + detalhe de configuracao.
2. Modelo de cobranca e consumo de aulas.
3. Politicas operacionais com simulacao.
4. Agentes/Fluxos pos-go-live.
5. Uso/Cotas.
6. Execucoes/Incidentes.

As demais rotas podem ser documentadas como herdadas enquanto nao aparecer uma necessidade visual diferente.
