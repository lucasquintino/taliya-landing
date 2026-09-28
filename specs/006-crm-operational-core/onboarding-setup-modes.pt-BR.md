# Onboarding E Setup - Modos De Configuracao

Status: decisao de produto em rascunho.
Data: 2026-05-13.

## Decisao

O Taliya tera um unico setup guiado por agente.

Durante esse setup, o studio pode:

1. continuar agora com o agente de IA;
2. agendar uma chamada online com um humano Taliya para acompanhar o mesmo fluxo.

A escolha por apoio humano nao muda as etapas, nao muda o motor de configuracao, nao muda as regras e nao muda as telas principais. Ela apenas adiciona acompanhamento de uma pessoa Taliya enquanto o studio percorre o mesmo setup.

## Principio central

O setup sempre usa o mesmo motor de configuracao:

- mesmas perguntas;
- mesmos presets;
- mesmas regras;
- mesmas simulacoes;
- mesmas validacoes;
- mesmas politicas;
- mesma auditoria;
- mesma publicacao controlada.

Isso evita criar dois produtos diferentes.

O que muda e quem acompanha o gestor:

- Se o studio continuar sozinho, o agente conduz a entrevista e o gestor aprova.
- Se o studio agendar chamada, o agente continua conduzindo o fluxo e o humano Taliya orienta/revisa durante a mesma experiencia.

Importante: nem o humano Taliya nem o agente de IA "configuram por fora" ou executam regras paralelas. Eles apenas guiam o studio, coletam respostas, explicam escolhas, apontam riscos e preparam a revisao. A configuracao real e aplicada pelo motor do sistema, usando formularios, presets, validacoes, politicas, permissoes e publicacao controlada.

## Apoio humano Taliya durante o setup

### Para que serve

Ideal para:

- primeiros clientes;
- studios com operacao complexa;
- migracao de base antiga;
- modelo financeiro hibrido;
- regras de reposicao pouco padronizadas;
- preparacao inicial de agentes e pacotes de fluxos recomendados;
- risco alto de configuracao errada;
- cliente que quer implantacao acompanhada.

### Como funciona

1. Gestor inicia onboarding.
2. Agente de setup entrevista o gestor.
3. Agente organiza respostas e identifica pendencias.
4. Studio pode agendar ou entrar em chamada com humano Taliya.
5. Humano Taliya acompanha e orienta quando houver duvida.
6. Sistema monta configuracao em rascunho a partir das respostas.
7. Agente mostra impactos e exemplos reais.
8. Humano Taliya revisa configuracoes sensiveis e aponta ajustes, sem aplicar regra por fora do sistema.
9. Gestor aprova e publica.
10. CRM fica ativo.
11. Agentes ficam preparados conforme plano, com fluxos recomendados em rascunho/pendencia quando exigirem configuracao profunda.

### O que o humano Taliya pode fazer

- Explicar decisoes operacionais.
- Guiar o gestor durante o preenchimento.
- Sugerir ajustes dentro da interface do sistema.
- Resolver ambiguidades.
- Revisar importacao.
- Recomendar preset.
- Validar modelo financeiro.
- Revisar politica de reposicao.
- Orientar ativacao dos agentes.
- Criar tarefas internas de implantacao.

O humano Taliya nao deve configurar o produto fora do fluxo oficial. Quando ele ajudar a alterar algo, a alteracao precisa passar pela interface, permissao, validacao, impacto e auditoria do sistema.

### O que continua exigindo aprovacao do gestor

- Publicar configuracao sensivel.
- Publicar ou alterar fluxo autonomo na area de Agentes/Fluxos.
- Alterar modelo de cobranca.
- Alterar politica de consumo de aulas.
- Alterar permissoes.
- Contratar agente/add-on/plano.
- Autorizar comunicacao externa automatica.

## Setup sem chamada humana

### Para que serve

Ideal para:

- self-service;
- studios menores;
- plano base com 0 agentes;
- plano com 1 agente;
- operacoes simples;
- gestor que quer configurar sozinho;
- ajustes posteriores ao setup inicial.

### Como funciona

1. Gestor inicia onboarding.
2. Agente pergunta como o studio funciona.
3. Gestor escolhe presets e responde perguntas simples.
4. Sistema cria rascunho de configuracao com apoio do agente.
5. Sistema executa validacoes.
6. Agente mostra impactos, riscos e exemplos.
7. Gestor aprova e publica.
8. O CRM entra em operacao.
9. Agentes ficam preparados conforme plano, mas nao aparecem como ativos/rodando; fluxos que exigem modo, limite, aprovacao ou fallback detalhado ficam como rascunho ou pendencia para configuracao pos-go-live.

### Limites do setup sem chamada

O setup sem chamada humana deve funcionar sem depender de humano Taliya, mas nao deve fingir seguranca onde nao existe.

Se uma configuracao for sensivel ou incerta, o sistema pode:

- publicar apenas em modo manual;
- manter automacao como rascunho ou pendencia;
- exigir aprovacao explicita do gestor;
- bloquear autonomia ate completar dados;
- recomendar revisao humana Taliya;
- criar checklist de pendencias;
- permitir seguir sem automacao naquela area.

Ou seja: o setup sem chamada nao deve travar o CRM. Ele deve ativar o que e seguro e deixar o restante pendente, manual ou em copiloto.

O agente tambem nao aplica configuracao diretamente. Ele conversa, orienta, interpreta respostas e pede confirmacoes. O sistema e quem transforma isso em configuracao, valida e publica apos aprovacao do gestor.

## Comparacao de experiencia

| Tema | Com chamada humana | Sem chamada humana |
|---|---|---|
| Publico ideal | implantacao assistida | self-service |
| Velocidade | media | alta |
| Complexidade suportada | alta | media |
| Revisao humana Taliya | sim | opcional |
| Aprovacao do gestor | obrigatoria | obrigatoria |
| Configuracao financeira complexa | recomendada com humano | possivel com limites |
| Autonomia de agentes | revisada antes de publicar | liberada apenas se segura |
| Melhor uso | cliente novo/complexo | cliente simples/ajustes |

## Estados do setup

- Nao iniciado.
- Em entrevista.
- Dados pendentes.
- Rascunho gerado.
- Validando.
- Pronto para revisar.
- Revisao humana Taliya.
- Aguardando aprovacao do gestor.
- Publicado.
- Publicado parcialmente.
- Bloqueado por risco.
- Bloqueado por plano/cota.

## O que o setup configura

### Base do studio

- unidades;
- horarios;
- equipe;
- papeis e permissoes;
- canais;
- modelos de mensagem;
- notificacoes;
- campos e tags.

### Operacao

- agenda;
- turmas;
- chamadas;
- reposicoes;
- no-show;
- consumo de aulas;
- financeiro;
- cobrancas;
- vendas;
- retencao.

### Agentes

- quais agentes estao disponiveis no plano;
- quais agentes serao preparados agora;
- areas de atuacao;
- responsaveis humanos;
- pacotes de fluxos recomendados adicionados como rascunho;
- fluxos que ficam pendentes para configurar depois;
- responsaveis;

O setup inicial nao configura profundamente modo manual/copiloto/autonomo, limites, cotas por fluxo, aprovacao por acao, fallback detalhado, simulacao final ou publicacao de fluxo autonomo. Isso pertence a Configuracoes Pos-Go-Live, na area de Agentes/Fluxos.

## Relacao com 0, 1, 3 e 7 agentes

### 0 agentes

O setup ainda e essencial.

Resultado esperado:

- CRM manual ativo;
- agenda configurada;
- financeiro configurado;
- equipe/permissoes ativas;
- tarefas, checklists e aprovacoes funcionando;
- agentes aparecem como opcionais/bloqueados por plano.

### 1 agente

Resultado esperado:

- CRM completo ativo;
- agente contratado preparado;
- demais agentes aparecem como indisponiveis ou upgrade;
- fluxos recomendados podem ficar como rascunho para configurar depois.

### 3 agentes

Resultado esperado:

- setup orientado por area coberta;
- areas sem agente continuam manuais;
- escopo e responsaveis de cada agente visiveis;
- cotas e economia configuradas.

### 7 agentes

Resultado esperado:

- setup mais controlado;
- revisao de regras de seguranca/aprovacoes;
- fluxos sensiveis marcados como pendencia obrigatoria para Agentes/Fluxos;
- observabilidade, cotas e incidentes mais visiveis.

## Integracao com casos de uso

Todo caso de uso deve consultar a configuracao publicada antes de agir.

Exemplo: aluno pede reposicao.

O sistema consulta:

- regra de reposicao;
- direito de aula;
- consumo de credito;
- status financeiro;
- disponibilidade de turma;
- permissao do usuario/agente;
- modo do fluxo, quando o fluxo ja tiver sido configurado em Agentes/Fluxos;
- politica de envio;
- cota disponivel;
- historico do aluno.

Resultado possivel:

- criar tarefa manual;
- sugerir resposta no copiloto;
- pedir aprovacao;
- enviar mensagem automaticamente;
- bloquear com motivo;
- criar incidente;
- acionar fallback manual.

## Regra de publicacao

Nenhum setup publica comportamento sensivel sem mostrar:

- resumo do que sera ativado;
- areas afetadas;
- exemplos reais;
- riscos;
- o que ficara manual;
- o que ficara apenas como rascunho/pendencia para configuracao posterior;
- quem pode aprovar;
- como reverter.

## Implicacao para UI

O onboarding precisa ter:

- checklist de progresso;
- conversa com agente;
- perguntas simples;
- presets por tipo de studio;
- painel de impacto;
- simulador;
- pendencias;
- opcao de chamar humano Taliya;
- publicacao parcial;
- historico de configuracao;
- retorno posterior para reconfigurar.

O retorno posterior para configurar fluxo de agente deve levar para Agentes/Fluxos, nao para repetir o onboarding.

Essa fronteira deve aparecer quando convem, nao o tempo todo. A UI e o agente devem explicar `pronto agora` versus `configurar depois` nos pontos de decisao: entrada do setup, painel de impacto, cards de agentes, configuracao por area quando houver pendencia avancada e revisao/publicacao final.

## Responsabilidade de execucao

O setup deve ser entendido assim:

1. Gestor informa como o studio trabalha.
2. Agente de IA traduz perguntas tecnicas para linguagem simples.
3. Humano Taliya orienta quando o modo contratado incluir acompanhamento.
4. Sistema gera rascunhos de configuracao.
5. Sistema valida consistencia, permissao, plano, cota e risco.
6. Gestor revisa e aprova.
7. Sistema publica e audita.

Portanto:

- humano guia;
- agente guia;
- gestor decide;
- sistema configura;
- auditoria registra.

## Refinamento pendente

Arquitetura fechada. Ainda precisamos refinar antes da implementacao:

- quais templates/presets iniciais serao oferecidos para studios de pilates.
- textos finais das perguntas do setup;
- thresholds de risco que recomendam chamada humana Taliya;
- defaults sugeridos para rascunhos de fluxos, sem publicar modo/limite no onboarding;
- provedores financeiros que entram no MVP.
