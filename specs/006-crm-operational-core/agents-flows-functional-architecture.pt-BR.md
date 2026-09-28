# Taliya CRM - Arquitetura Funcional De Agentes/Fluxos

Status: contrato funcional v0.2.
Data: 2026-05-21.

## Nota De Atualizacao

Para a definicao final de paginas, rotinas, fluxos e configuracoes minimas, usar tambem:

- `agents-flows-routines-pages-final-contract.pt-BR.md`

Onde houver conflito de termo, vale a decisao mais recente:

- agente nao tem pagina de configuracoes proprias;
- configuracao real fica em rotina/fluxo;
- "pacote" como conceito de produto para o usuario vira "rotina";
- tom de voz fica no fluxo;
- canal, integracao, permissao, dado e cota sao dependencias fixas, nao ajustes soltos.

## Objetivo

Definir como a familia Agentes/Fluxos funciona no Taliya CRM sem misturar essa camada com Setup Inicial, Configuracoes Pos-Go-Live, Integracoes Tecnicas, Billing Taliya, Uso/Cotas, Auditoria ou Control Planes.

Agentes/Fluxos responde:

- quais agentes estao disponiveis no plano;
- quais fluxos existem;
- quais fluxos estao configurados, bloqueados, pausados ou ativos;
- qual modo cada fluxo usa: manual, copiloto ou autonomo;
- quais dados, canais, integracoes, templates, permissoes, cotas e aprovacoes sao necessarios;
- como simular, publicar, pausar, corrigir, reverter ou degradar um fluxo.

Agentes/Fluxos nao responde:

- como fazer o setup inicial do CRM;
- como configurar profundamente studio, equipe, agenda, financeiro ou canais comuns;
- se o provedor tecnico esta conectado;
- qual plano comercial o studio contratou com a Taliya;
- quanto ja foi consumido no ciclo como fonte primaria;
- o que aconteceu em uma execucao passada como superficie principal de investigacao.

## Decisao Central

Agentes/Fluxos e uma familia propria do produto.

O dono/admin nao monta IA do zero. Ele escolhe o perfil da rotina, revisa impacto, ajusta poucos pontos claros quando necessario, simula e publica a rotina.

O CRM continua sendo o produto principal. Agentes sao uma camada operacional configuravel dentro do CRM.

```text
CRM manual sempre disponivel
  -> copiloto quando contratado e permitido
  -> autonomia somente em fluxos seguros, simulados e publicados
```

## Fronteiras De Produto

| Familia | O que define | O que nao deve definir |
|---|---|---|
| Setup Inicial | CRM minimo para operar, pendencias e rascunhos de agentes quando aplicavel | modo, cota, fallback profundo, simulacao final ou publicacao autonoma de fluxo |
| Configuracoes Pos-Go-Live | Studio, equipe, permissoes, canais, agenda, financeiro, notificacoes e ajustes comuns do CRM | builder de agente, limites por fluxo, publicacao autonoma ou execucoes |
| Integracoes Tecnicas | conexao, saude, logs e recuperacao de provedores | regra de negocio, modo de agente, template de fluxo ou autonomia |
| Billing Taliya | plano contratado, agentes inclusos, add-ons, cotas comerciais e entitlements | configuracao operacional de fluxo |
| Uso/Cotas | consumo real, extrato, alertas, economia e bloqueios por limite | compra profunda de plano, regra de negocio ou builder de fluxo |
| Control Planes | execucoes, incidentes, logs, auditoria, risco, falhas e pausas emergenciais | configuracao permanente de fluxo |
| Auditoria | trilha imutavel de acoes sensiveis | edicao, correcao ou publicacao de regra |

Regra de produto:

- se a pergunta e "como esse fluxo deve agir?", fica em Agentes/Fluxos;
- se a pergunta e "o que aconteceu?", fica em Control Plane;
- se a pergunta e "o provedor esta funcionando?", fica em Integracoes;
- se a pergunta e "tenho direito a esse agente/cota?", fica em Billing/Entitlements;
- se a pergunta e "quanto consumiu?", fica em Uso/Cotas;
- se a pergunta e "como o CRM base opera?", fica em Configuracoes.

## Agentes Canonicos

O Taliya CRM trabalha com sete agentes canonicos.

| Agente | Area principal | Papel operacional |
|---|---|---|
| Atendimento | Inbox, conversas, contatos e repasse para humano | Resumir, classificar, sugerir resposta, detectar opt-out e encaminhar humano. |
| Agenda | Agenda, turmas, aulas, reposicoes e lista de espera | Sugerir encaixe, confirmar presenca, apoiar reposicao, detectar conflito e preencher vaga segura. |
| Vendas | Interessados, experimental, matricula e origens | Qualificar, lembrar, preparar follow-up, apoiar pos-aula experimental e conversao. |
| Financeiro | Cobrancas, pagamentos, contratos e excecoes | Priorizar cobrancas, preparar lembrete, apoiar comprovante e explicar pendencias com travas fortes. |
| Retencao | Risco, cancelamento, reclamacao e reativacao | Detectar risco, sugerir abordagem, acompanhar retorno e pausar automacao sensivel. |
| Historico/Professor | Historico permitido, notas, contexto de aula e repasse entre professores | Resumir contexto permitido, lembrar nota, apoiar professor e proteger dados sensiveis. |
| Gestao/Governanca | Hoje, operacao, cotas, incidentes, relatorios e qualidade | Priorizar, explicar gargalos, monitorar execucoes/cotas/incidentes e apoiar decisao. |

Agente sob medida nao e o oitavo agente principal. Ele e uma camada futura/comercial de expansao e nao deve entrar no catalogo principal do MVP.

## Planos E Entitlements

O numero de agentes muda automacao, copiloto, execucoes, cotas e bloqueios. Nao muda o fato de que o Taliya e um CRM completo.

| Plano | Comportamento |
|---|---|
| 0 agentes | CRM completo manual/programatico. Fluxos aparecem como sugestao, preview ou upgrade, sem automacao ativa. |
| 1 agente | Apenas o dominio contratado tem IA ativa/configuravel. O restante segue manual/programatico. |
| 3 agentes | Bundle recomendado: Atendimento + Agenda + Vendas, salvo troca deliberada. Publicacao por rotina e obrigatoria para reduzir complexidade. |
| 7 agentes | Todos os dominios ativos. Interface exige agrupamento forte por area, agente, risco, status, cota e responsavel. |

Regras:

- o caminho manual deve existir em todo plano;
- acao de agente nao incluso mostra bloqueio por plano e caminho manual;
- agente incluso mas nao configurado mostra "configurar/testar" e mantem manual;
- downgrade pausa fluxos fora do entitlement, mas historico, auditoria e execucoes continuam consultaveis;
- upgrade libera novos agentes como rotinas em rascunho recomendado, nao como autonomia ja publicada.

## Matriz Por Plano

| Capacidade | 0 agentes | 1 agente | 3 agentes | 7 agentes |
|---|---|---|---|---|
| Ver agentes | Mostra catalogo, beneficios e upgrade. | Mostra 1 agente configuravel e os demais bloqueados. | Mostra bundle ativo e proximos agentes sugeridos. | Mostra todos os agentes com filtros fortes. |
| Ver fluxos | Todos aparecem como manual, template, sugestao ou upgrade. | Fluxos do agente contratado podem usar IA; outros ficam manuais/bloqueados. | Fluxos dos 3 agentes ativos agrupam por rotina. | Catalogo completo com status, risco, cota e area. |
| Configurar perfil | Pode salvar preferencia como rascunho/preview. | Aplica somente ao agente contratado. | Aplica por rotina recomendada. | Aplica por rotina/agente, com revisao de risco. |
| Simular | Pode simular caminho manual e preview sem publicar IA. | Simula fluxos do agente contratado. | Simula rotina, destacando bloqueios dos outros agentes. | Simula rotina ou fluxo, com impacto por area. |
| Publicar autonomia | Nao. | Apenas fluxos seguros do agente contratado. | Apenas fluxos seguros dos 3 agentes ativos. | Apenas fluxos seguros dos 7 agentes, com filtros e aprovacoes. |
| Executar | CRM manual/programatico. | IA no dominio contratado, manual no resto. | IA nos dominios ativos, manual no resto. | IA em todos os dominios contratados, respeitando risco/cota. |
| Downgrade | Ja e manual. | Pausa o agente e preserva historico. | Pausa agentes removidos do plano. | Pausa agentes/fluxos fora do novo entitlement. |

## Camadas De Configuracao

Agentes/Fluxos tem tres camadas para evitar que o dono configure dezenas de itens manualmente.

### 1. Perfil Da Rotina

Perfil da rotina define a postura operacional daquele conjunto de fluxos.

Exemplos:

- `Mais manual`: mais manual e copiloto; autonomia minima.
- `Equilibrado`: autonomia apenas em lembretes e rotinas seguras.
- `Mais autonomo`: mais cadencias e automacoes dentro do teto de cada fluxo.

O perfil da rotina sugere modo, limite e fallback, mas nao publica sem simulacao e confirmacao.

### 2. Rotina

Rotina e um conjunto fixo de fluxos por agente ou objetivo.

Exemplos:

- Atendimento essencial;
- Agenda essencial;
- Vendas experimental;
- Financeiro lembretes seguros;
- Retencao preventiva;
- Professor contexto de aula;
- Gestao qualidade e cotas.

O usuario pode publicar por rotina, mas o sistema publica apenas os fluxos que passaram no preflight. Os demais ficam como rascunho, bloqueados ou pendentes com motivo claro.

### 3. Fluxo

Fluxo e o comportamento especifico que pode operar em manual, copiloto ou automatico.

Exemplos:

- confirmar presenca;
- preparar resposta de reposicao;
- lembrar aula experimental;
- preparar cobranca;
- detectar queda de frequencia;
- lembrar professor de nota;
- pausar fluxo por incidente.

## Objetos Funcionais

Agentes/Fluxos precisa de poucos objetos claros. O dono/admin nao deve ver isso como modelo tecnico, mas a arquitetura precisa separar as responsabilidades.

| Objeto | Para que existe | Fonte principal |
|---|---|---|
| Agente | Representa uma area operacional contratavel/configuravel, como Agenda ou Vendas. | Billing/Entitlements define se esta incluso; Agentes/Fluxos define configuracao. |
| Rotina | Agrupa fluxos fixos para publicar sem configurar tudo um a um. | Agentes/Fluxos. |
| Perfil da rotina | Define postura operacional: Mais manual, Equilibrado ou Mais autonomo. | Agentes/Fluxos. |
| Fluxo | Comportamento operacional com gatilho, condicao, acao, modo, fallback, cota, risco e auditoria. | Agentes/Fluxos. |
| Configuracao publicada | Snapshot versionado do que esta valendo. | Agentes/Fluxos com auditoria. |
| Simulacao | Teste pre-publicacao com exemplos, bloqueios, custo, risco e fallback. | Agentes/Fluxos. |
| Aprovacao | Decisao humana antes de publicar ou executar acao sensivel. | Aprovacoes/CRM, com origem em Agentes/Fluxos. |
| Execucao | Registro do que rodou, falhou, consumiu ou virou fallback. | Runtime/Control Plane. |
| Incidente | Caso de investigacao quando algo falha ou apresenta risco. | Operacao/Control Plane. |
| Lancamento de uso | Evento idempotente de consumo/custo. | Uso/Cotas. |
| Politica/template | Regra ou mensagem aprovada usada pelo fluxo. | Contexto do CRM ou fluxo; nao como builder global livre. |
| Fallback | Caminho seguro quando o fluxo nao pode agir. | Agentes/Fluxos define; CRM/Control Plane executa ou investiga. |

## Objeto Fluxo

Todo fluxo precisa ter uma ficha funcional.

| Campo | Descricao |
|---|---|
| `id` | Identificador estavel. |
| `nome` | Nome simples para o dono/admin. |
| `objetivo` | Resultado operacional esperado. |
| `areaCrm` | Area principal do CRM. |
| `agenteResponsavel` | Agente canonico dono do fluxo. |
| `rotina` | Rotina fixa onde o fluxo aparece. |
| `gatilho` | Evento, horario, mensagem, webhook, botao ou lote que inicia. |
| `condicao` | Regras para poder rodar. |
| `acao` | Tarefa, aprovacao, mensagem, caso, rascunho, alerta ou mudanca permitida. |
| `modo` | Manual, copiloto ou autonomo. |
| `canal` | WhatsApp, e-mail, interno, sistema ou nenhum. |
| `dadosNecessarios` | Dados obrigatorios antes de rodar. |
| `integracaoNecessaria` | Provedor exigido, se houver. |
| `templateOuRegra` | Template, politica ou mensagem aprovada. |
| `permissoes` | Quem pode configurar, aprovar, pausar e revisar. |
| `aprovacao` | Quando exige decisao humana. |
| `fallback` | Caminho quando nao pode executar. |
| `cotaEstimada` | Estimativa de consumo antes de publicar/executar. |
| `limites` | Tentativas, envios, periodo, custo e frequencia. |
| `risco` | Baixo, medio, alto, critico ou bloqueado. |
| `simulacao` | Resultado da ultima simulacao valida. |
| `status` | Rascunho, pendente, pronto para simular, simulado, ativo, pausado, bloqueado ou incidente. |
| `auditoria` | Eventos obrigatorios. |
| `versao` | Snapshot publicado da configuracao. |

## Modos De Operacao

Regra central:

O modo do fluxo define o que acontece quando o fluxo dispara. O botao de copiloto define ajuda sob demanda dentro da tela. Essas duas coisas nao sao iguais.

| Conceito | Pergunta que responde | Exemplo |
|---|---|---|
| Modo do fluxo | Quando este fluxo disparar, quem conduz? | D2 Pagamento Atrasado roda em manual, copiloto ou autonomo. |
| Copiloto contextual | Nesta tela, o usuario pode pedir ajuda ao agente? | Botao "Sugerir mensagem" dentro de uma cobranca. |

Assim:

- fluxo manual nao gera sugestao automatica, mas pode ter botao de ajuda se o agente/plano permitir;
- fluxo copiloto gera sugestao quando dispara, mas humano decide cada acao;
- fluxo autonomo e conduzido pelo agente, mas ainda pode mostrar copiloto para explicar, revisar aprovacao, apoiar chamada humana ou preparar acao manual.

### Manual

Manual significa que o sistema organiza trabalho, mas humano executa.

Pode criar:

- tarefa;
- checklist;
- caso operacional;
- aprovacao;
- alerta;
- rascunho sem envio.

No modo manual, o agente nao dispara o fluxo, nao conduz etapas e nao cria sugestao automatica.

Se o plano tiver o agente da area, a tela ainda pode mostrar ajuda sob demanda, como:

- resumir contexto;
- sugerir mensagem;
- explicar pendencia;
- preparar checklist.

Essa ajuda so roda quando o usuario pede.

Manual deve existir para todo caminho critico do CRM, para plano 0 agentes, fallback, pausa, cota bloqueada e escolha deliberada do dono/admin.

### Copiloto

Copiloto significa que o agente prepara, explica ou sugere, mas humano decide.

Pode:

- resumir contexto;
- sugerir proxima acao;
- redigir mensagem;
- preparar proposta;
- explicar impacto;
- classificar risco;
- recomendar responsavel.

No modo copiloto, o fluxo dispara uma sugestao automatica, mas nao executa a acao final sem aceite humano.

A execucao pode terminar de seis formas:

| Decisao humana | Resultado |
|---|---|
| aprovar sem editar | Executa a acao sugerida. |
| editar e aprovar | Executa a versao editada pelo humano. |
| rejeitar | Vira manual, encerrado ou nova pendencia. |
| pedir mais dados | Continua em copiloto. |
| transformar em tarefa | Vira operacao manual organizada. |
| pausar fluxo | Para novas sugestoes ate retomada. |

Copiloto e bom para adocao, revisao humana e acoes em que o agente ajuda muito, mas o studio ainda quer decisao caso a caso.

### Autonomo

Autonomo significa que o agente conduz o fluxo dentro de limites publicados.

Autonomo nao significa "sem humano nunca". O fluxo pode ter:

- aprovacoes obrigatorias;
- chamada humana quando aparece excecao;
- fallback manual;
- bloqueio por dado, canal, cota, permissao, integracao ou risco;
- pausa automatica;
- execucao direta quando o caso comum e simples.

So pode existir quando:

- plano inclui o agente;
- fluxo esta ativo;
- modo permite autonomia;
- usuario/tenant tem permissao;
- dados obrigatorios estao completos;
- contato tem consentimento e nao tem opt-out;
- canal necessario esta conectado e template esta valido;
- integracao necessaria esta ok;
- cota esta disponivel;
- risco nao e sensivel;
- auditoria esta pronta;
- fallback manual existe;
- pausa de emergencia esta disponivel;
- simulacao foi validada;
- publicacao foi confirmada por usuario autorizado.

Autonomo nunca deve parecer magico. A UI deve mostrar motivo, regra, limite, cota, aprovacao, chamada humana e fallback.

## Acoes Nunca Autonomas

Mesmo com 7 agentes, estas acoes exigem humano:

- desconto sensivel;
- cortesia relevante;
- estorno;
- disputa;
- reembolso;
- acordo financeiro;
- cancelamento sensivel;
- reclamacao severa;
- LGPD/exportacao/exclusao/anonimizacao;
- suporte Taliya/grant;
- mudanca de permissao;
- compra de add-on;
- alteracao de Billing Taliya;
- conexao/desconexao de integracao;
- alteracao estrutural ampla de politica, agenda, plano ou cobranca;
- compartilhamento de historico sensivel.

O agente pode explicar, preparar rascunho ou criar aprovacao. Nao decide sozinho.

## Simulacao

Simulacao e obrigatoria antes de publicar fluxo automatico e recomendada antes de publicar rotina com copiloto sensivel.

A simulacao deve mostrar:

- exemplos que passariam;
- exemplos que seriam bloqueados;
- exemplos que virariam tarefa;
- exemplos que virariam aprovacao;
- dados usados;
- canal usado;
- template/regra usada;
- custo/cota estimada;
- risco;
- aprovador, se houver;
- fallback;
- evento de auditoria previsto;
- pendencias de dados, permissao, canal, integracao ou plano.

Estados possiveis da simulacao:

| Estado | Significado |
|---|---|
| `aprovada` | Pode publicar conforme configuracao simulada. |
| `aprovada_com_avisos` | Pode publicar, mas ha pendencias nao bloqueantes. |
| `bloqueada` | Nao pode publicar ate corrigir requisito. |
| `exige_aprovacao` | Publicacao ou execucao depende de aprovador. |
| `degrada_para_manual` | Autonomia nao e segura; fluxo vira tarefa/caso. |

## Publicacao

Publicacao transforma rascunho em configuracao ativa.

Ciclo recomendado:

```text
rascunho
  -> pronto_para_simular
  -> simulado
  -> aguardando_aprovacao
  -> publicado
  -> ativo
```

Publicar exige:

- permissao de dono/admin;
- entitlement valido;
- preflight aprovado;
- simulacao valida;
- cota disponivel;
- fallback definido;
- auditoria pronta;
- versao/snapshot da configuracao;
- confirmacao explicita.

Publicacao por rotina:

- mostra todos os fluxos da rotina;
- separa "vai ativar", "vai ficar copiloto", "vai ficar manual", "bloqueado" e "nao contratado";
- permite publicar somente os seguros;
- registra cada fluxo publicado com versao propria;
- cria pendencias para os bloqueados.

O agente de configuracao pode explicar, comparar, preparar rascunho e sugerir perfil de rotina. Ele nao publica sozinho.

## Pausa, Rollback E Fallback

### Pausa

Um fluxo pode ser pausado por:

- dono/admin;
- usuario operacional em emergencia, quando permitido;
- cota 100%;
- modo economia;
- falha repetida;
- incidente;
- opt-out elevado;
- integracao indisponivel;
- template pausado/rejeitado;
- risco sensivel detectado;
- billing/entitlement limitado.

Pausa deve preservar:

- historico;
- execucoes;
- auditoria;
- configuracao publicada;
- motivo;
- caminho manual.

### Rollback

Rollback volta uma configuracao publicada anterior.

Nao deve fingir que desfaz acao externa ja feita.

Exemplos:

- mensagem ja enviada nao e apagada;
- pagamento ja confirmado nao e desconfirmado sem regra financeira;
- agenda ja alterada pode exigir caso de correcao;
- dado sensivel corrigido gera novo evento, nao edita auditoria antiga.

Se houve impacto real, abrir incidente ou tarefa de correcao.

### Fallback

Todo fluxo precisa de fallback.

Opcoes:

- parar;
- criar tarefa;
- pedir aprovacao;
- chamar fila responsavel;
- abrir caso operacional;
- mover para modo manual;
- seguir apenas interno, sem envio externo;
- abrir incidente;
- reprocessar somente se houver idempotencia e impacto conhecido.

## Cotas E Economia

Cotas sao governanca operacional, nao apenas billing.

Regras:

- toda automacao paga verifica cota antes de executar;
- todo consumo gera lancamento idempotente;
- retry da mesma execucao logica nao pode cobrar/contar duas vezes;
- simulacao mostra custo estimado;
- aprovacao mostra custo previsto;
- execucao mostra consumo real;
- Uso/Cotas e a fonte de consumo real.

Limites de lancamento:

| Plano | Cota de automacao ativa |
|---|---:|
| Base | 0 mensagens/execucoes ativas de agente por mes |
| 1 Agente | 1.500 mensagens de IA/mes |
| 3 Agentes | 5.000 mensagens de IA/mes |
| 7 Agentes | 15.000 mensagens de IA/mes |

Comportamento:

| Uso | Comportamento |
|---|---|
| 0-69% | Normal. |
| 70% | Alerta preventivo. |
| 90% | Economia: fluxos de baixa prioridade viram tarefa ou aprovacao. |
| 100% | Automacao paga bloqueada; CRM manual segue. |
| cota/add-on ativo | Fluxos elegiveis retomam conforme regra. |

Cada fluxo deve declarar prioridade em economia:

- essencial;
- media;
- baixa.

## Aprovacoes

Aprovacao e a superficie humana de decisao.

Uma aprovacao deve mostrar:

- o que o agente sugeriu;
- por que sugeriu;
- dados usados;
- objeto afetado;
- antes/depois seguro;
- risco;
- custo/cota previsto;
- canal usado e template usado;
- politica/versao;
- aprovador necessario;
- acoes: aprovar, editar, rejeitar, pedir dados, transformar em tarefa.

O agente nunca aprova a propria proposta.

## Paginas

### `/app/agentes`

Funcao:

- ser o catalogo de entrada dos agentes;
- mostrar os 7 agentes canonicos em cards iguais;
- indicar, de forma simples, status, rotinas e fluxos de cada agente;
- levar o usuario para a pagina do agente selecionado.

Deve conter:

- titulo `Agentes`;
- subtitulo `Areas automatizadas do CRM`;
- cards dos sete agentes canonicos;
- status resumido por agente;
- quantidade de rotinas e fluxos;
- CTA `Ver agente`, com excecao do agente em foco que pode usar CTA especifico, como `Abrir Agenda`.

Nao deve conter:

- KPIs;
- filtros;
- chips de plano;
- cota;
- atividade recente;
- graficos;
- tabelas;
- resumo lateral;
- painel do agente de configuracao;
- log tecnico profundo;
- lista completa de auditoria;
- configuracao de provedor;
- compra profunda de plano;
- payload bruto de execucao.

Decisao visual aprovada:

```text
52_round-4.1L_agentes_01_catalogo-agentes-aprovado.png
```

Observacao:

`/app/agentes` e escolha de entrada. Status profundos, cotas, execucoes, incidentes, aprovacoes e investigacao ficam nas paginas de agente, rotina, fluxo, uso/cotas, auditoria e control planes distribuidos.

### `/app/agentes/[agentId]`

Funcao:

- mostrar a area coberta pelo agente;
- listar as rotinas do agente;
- levar o usuario para a rotina certa.

Deve conter:

- breadcrumb;
- titulo do agente;
- subtitulo curto;
- status resumido do agente;
- cards das rotinas do agente;
- quantidade de fluxos por rotina;
- status resumido por rotina;
- CTA `Abrir rotina`.

Nao deve conter:

- configuracao do agente;
- KPIs;
- cota;
- atividade recente;
- painel lateral;
- Agente de Configuracao;
- simulacao/publicacao fora da rotina.

Decisao visual aprovada para Agenda:

```text
53_round-4.1L_agentes_02_agente-agenda-rotinas-aprovado.png
```

### `/app/agentes/[agentId]/rotinas`

Funcao:

- ser a visao filtrada das rotinas e fluxos de um agente;
- evitar que o usuario precise procurar o mesmo agente dentro da lista global;
- ajudar planos de 1 agente a parecerem simples.

Deve conter:

- rotinas do agente;
- fluxos do agente por status;
- bloqueios por plano, dado, canal, integracao, cota ou permissao;
- acao de publicar rotina;
- link para cada `/app/agentes/[agentId]/rotinas/[routineId]`;
- resumo de execucoes recentes, com link para Control Plane.

Regra:

Esta pagina nao deve duplicar uma segunda logica de configuracao. Ela e uma entrada filtrada para as mesmas rotinas e fluxos.

### Catalogo Global De Fluxos

Funcao:

- listar fluxos sem virar parede de 96 cards, se o MVP decidir manter uma visao global.
- a definicao final de paginas prioriza `/app/agentes`, paginas de agente e paginas de rotina.

Agrupamentos obrigatorios:

- agente;
- area do CRM;
- rotina;
- modo;
- status;
- risco;
- cota;
- bloqueio;
- contratado/nao contratado.

Estados visiveis:

- disponivel;
- bloqueado por plano;
- agente incluso nao configurado;
- rascunho;
- pronto para simular;
- simulado;
- ativo;
- pausado;
- bloqueado por dados;
- bloqueado por integracao;
- cota alta;
- incidente.

### `/app/fluxos/[flowId]`

Funcao:

- configurar um fluxo especifico.

Deve conter:

- objetivo;
- agente dono;
- area do CRM;
- modo;
- gatilho;
- condicao;
- acao;
- canal;
- dados necessarios;
- integracao necessaria;
- template/regra;
- aprovacao;
- fallback;
- limites;
- cota estimada;
- risco;
- preflight;
- status de simulacao;
- versao publicada;
- acoes: salvar rascunho, simular, publicar, pausar, rollback, abrir execucoes.

Nao deve conter:

- logs tecnicos completos;
- edicao de billing;
- conexao de provedor;
- lista global de auditoria.

### `/app/fluxos/[flowId]/simular`

Funcao:

- testar o fluxo antes de publicar.

Deve conter:

- cenario manual;
- exemplos gerados pelo sistema;
- resultado esperado;
- bloqueios;
- custo/cota;
- risco;
- auditoria prevista;
- fallback;
- comparacao entre manual, copiloto e autonomo quando aplicavel.

### `/app/fluxos/execucoes/[runId]`

Funcao:

- explicar uma execucao real.

Esta rota e Control Plane.

Deve conter:

- status;
- agente/fluxo;
- modo;
- objeto afetado;
- entrada segura;
- saida segura;
- ferramenta usada;
- custo/cota;
- politica/versao;
- erro;
- resultado;
- auditoria;
- acoes seguras: abrir origem, criar tarefa, abrir incidente, pausar fluxo, reprocessar quando idempotente.

Nao deve permitir:

- publicar fluxo;
- mudar modo permanente;
- conectar provedor;
- alterar billing.

## Catalogo De Fluxos

O catalogo de trabalho deve usar 96 fluxos fortes.

| Familia | Quantidade | Decisao |
|---|---:|---|
| Atendimento | 10 | manter |
| Agenda | 16 | manter |
| Vendas | 15 | 14 base + C15 |
| Financeiro | 15 | 14 base + D15 |
| Retencao | 13 | 12 base + E13 |
| Gestao/Governanca | 15 | 13 base + F14 + F15 |
| Historico/Evolucao | 12 | manter |
| Total | 96 | catalogo forte v0.1 |

E14 Primeira Semana Do Novo Aluno deve ficar como subfluxo/checklist ate provar independencia.

G13 Gate De Anamnese, Consentimento E Contato De Emergencia deve ficar como gate/subfluxo de historico, dados e primeira aula ate provar independencia.

## Relacao Com CRM

Fluxos nao substituem rotas do CRM.

Exemplos:

- Agenda continua em `/app/agenda`;
- Inbox continua em `/app/inbox`;
- Financeiro continua em `/app/financeiro`;
- Retencao continua em `/app/retencao`;
- Alunos continua em `/app/alunos`;
- Operacao continua em `/app/operacao`.

Agentes aparecem nessas telas como:

- sugestoes;
- botoes contextuais;
- aprovacoes;
- tarefas;
- execucoes recentes;
- alertas;
- pausas;
- explicacoes;
- links para configurar fluxo quando permitido.

Regra:

O usuario trabalha primeiro no objeto do CRM. Ele so vai para Agentes/Fluxos quando quer configurar como a automacao deve agir.

## Agente De Configuracao Em Agentes/Fluxos

O agente de configuracao pode:

- explicar o que cada agente faz;
- recomendar perfil de rotina;
- comparar manual, copiloto e autonomo;
- preparar rascunho;
- explicar bloqueio;
- sugerir limite;
- sugerir fallback;
- simular exemplos;
- explicar custo/cota;
- apontar integracao faltante;
- guiar publicacao.

O agente de configuracao nao pode:

- publicar sozinho;
- mudar modo sem simulacao;
- ignorar plano/cota/permissao;
- conectar integracao sozinho;
- comprar add-on;
- alterar billing;
- aprovar acao sensivel;
- transformar conversa em fonte da verdade.

Toda configuracao sensivel segue:

```text
usuario informa ou escolhe
  -> agente explica/sugere
  -> sistema gera rascunho estruturado
  -> sistema valida impacto, permissao, plano, cota, politica e risco
  -> usuario revisa
  -> usuario aprova quando necessario
  -> sistema publica, versiona e audita
```

## Conflitos E Correcoes

### Manter

- Taliya e CRM operacional completo com agentes integrados.
- WhatsApp e canal, nao produto inteiro.
- Base com 0 agentes e CRM completo.
- Agentes/Fluxos fora do Setup Inicial.
- Autonomia apenas depois de preflight, simulacao, publicacao e auditoria.
- Control Planes distribuidos, sem `/app/controle/*` no MVP.
- Billing Taliya como fonte de entitlements.
- Uso/Cotas como fonte de consumo real.

### Corrigir

- Rotas antigas de onboarding como `/onboarding/importacao` e `/onboarding/agentes` nao devem prevalecer sobre o Setup Inicial final de 9 blocos.
- Politicas globais livres nao devem voltar como configuracao comum do MVP. Para Agentes/Fluxos, politica deve aparecer contextualizada no fluxo ou em mudanca operacional especifica.
- Templates globais nao devem virar pagina principal pesada. Mensagens devem morar no contexto que usa: fluxo, atendimento, agenda, financeiro, retencao ou comunicado.
- Rotas antigas muito granulares de Uso, como custos, pacotes, regras de economia e limites de fluxo, devem ser tratadas com cuidado. No MVP atual, o essencial e `/app/uso`, `/app/uso/cotas`, `/app/uso/extrato` e `/app/uso/alertas`; limites permanentes por fluxo podem morar em `/app/fluxos/[flowId]`.
- Gestao/Governanca como agente contratado nao deve ser confundido com governanca basica do produto. Auditoria, cotas e incidentes existem mesmo sem esse agente; o agente de Gestao apenas adiciona copiloto/IA nesse dominio.

### Remover Do MVP

- builder tecnico livre de politica;
- builder de prompt;
- tela global de controle `/app/controle/*`;
- autonomia no Setup Inicial;
- publicacao de fluxo sem simulacao;
- fluxo autonomo sem fallback;
- fluxo autonomo sem cota;
- agente decidindo billing, permissao, LGPD, suporte ou acao financeira sensivel.

## Decisoes Fechadas E Pendencias

As decisoes de catalogo antigas foram registradas no complemento `agents-flows-packages-and-flow-cards.pt-BR.md`.
Para UI final, vale o contrato de rotinas:

- rotinas por agente;
- modo default dos 96 fluxos;
- autonomia MVP por fluxo;
- limites default por rotina/fluxo;
- prioridade de economia por fluxo;
- mini cards com gatilho, dados/canal e fallback.

As decisoes de publicacao abaixo foram fechadas no complemento `agents-flows-publication-versioning-and-evals.pt-BR.md`:

- estados de configuracao e publicacao;
- versionamento de perfil de rotina, rotina, fluxo, regra, limite, simulacao e aprovacao;
- gates obrigatorios de publicacao;
- severidade de incidente e criterio de auto-pausa;
- casos de avaliacao/eval para manter ou degradar autonomia;
- eventos de auditoria obrigatorios.

Ainda fica para a etapa de UI/implementacao:

1. Modelo visual detalhado da simulacao de fluxo.
2. Nomes finais exibidos na interface, mantendo linguagem simples para dono/admin.
3. Contrato tecnico de API/banco para persistir estes objetos.

## Criterios De Aceite

Agentes/Fluxos esta bem definido quando:

- 0 agentes continua CRM completo manual;
- 1 agente ativa somente o dominio contratado;
- 3 agentes funciona por rotinas recomendadas, sem exigir configuracao manual extensa;
- 7 agentes tem agrupamento, filtros, cotas, riscos e status sem virar painel tecnico demais;
- todo fluxo tem objetivo, area, agente, gatilho, condicao, acao, modo, permissao, canal, dados, integracao, fallback, aprovacao, cota, risco, simulacao, status e auditoria;
- autonomia so publica depois de preflight, simulacao e confirmacao autorizada;
- pausa, rollback e fallback estao definidos;
- Billing decide entitlement;
- Uso/Cotas decide consumo real;
- Integracoes decidem saude tecnica;
- Configuracoes decidem CRM base;
- Control Planes investigam execucao e risco;
- o agente de configuracao ajuda, mas nao publica sozinho.

## Proximo Artefato Recomendado

Criar, quando a arquitetura for aprovada, um artefato de implementacao com:

- modelos de dados finais;
- contratos de API;
- permissoes por acao;
- eventos de auditoria em formato implementavel;
- estados de UI por rota;
- criterios de teste.
