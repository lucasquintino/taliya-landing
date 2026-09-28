# Taliya CRM - Contrato Final De Agentes, Rotinas, Fluxos E Paginas

Status: contrato funcional v0.2.
Data: 2026-05-21.

## Objetivo

Definir, sem ambiguidade, como a familia Agentes/Fluxos funciona para todos os agentes canonicos do Taliya CRM.

Este documento fecha:

- quais paginas existem;
- o que cada pagina mostra;
- quais dinamicas cada pagina tem;
- quais rotinas existem por agente;
- quais fluxos existem em cada rotina;
- quais ajustes o studio pode fazer;
- o que deve ficar fixo e nao configuravel;
- como modo, template, tom, simulacao, publicacao, pausa e rollback funcionam.

Mapa exato de perfis por rotina:

- `agents-flows-routine-profile-map.pt-BR.md`

Mapas detalhados por agente:

- `agents-flows-atendimento-pages-dynamics.pt-BR.md`
- `agents-flows-agenda-pages-dynamics.pt-BR.md`
- `agents-flows-vendas-pages-dynamics.pt-BR.md`
- `agents-flows-financeiro-pages-dynamics.pt-BR.md`
- `agents-flows-retencao-pages-dynamics.pt-BR.md`
- `agents-flows-gestao-governanca-pages-dynamics.pt-BR.md`
- `agents-flows-historico-professor-pages-dynamics.pt-BR.md`

Contrato visual das paginas de rotina:

- `agents-flows-routine-page-visual-contract.pt-BR.md`

Contrato operacional das variacoes sem nova imagem:

- `agents-flows-operational-variation-contract.pt-BR.md`

Contrato do resultado consolidado de `Simular rotina`:

- `agents-flows-routine-simulation-result-contract.pt-BR.md`

Contrato de operacao leve pos-publicacao nas mesmas paginas:

- `agents-flows-post-publication-light-ops-contract.pt-BR.md`

## Revisao v0.2

Esta revisao reduz a superficie configuravel.

Decisoes novas:

- "Ajustes permitidos" passa a ser "ajustes visiveis quando necessario";
- rotinas tem composicao fixa no produto;
- o studio nao monta rotinas escolhendo fluxos soltos;
- a rotina tem um perfil de operacao que configura os fluxos em conjunto;
- o usuario entende o impacto do perfil antes de abrir fluxo por fluxo;
- dados, canais, integracoes, permissoes, cotas, fontes, metricas e documentos permitidos nao sao ajustes de fluxo;
- responsavel, fila e aprovador so aparecem quando precisam sair do padrao natural da area ou quando o fluxo exige decisao humana;
- template e tom aparecem apenas quando o fluxo produz mensagem, resposta, comunicado ou texto que sera enviado/lido por humano;
- fluxos internos usam "texto interno" ou "formato do resumo", nao tom de voz de comunicacao externa.

Regra de heranca para reduzir configuracao:

```text
Rotina define responsaveis, aprovadores e fila humana padrao.
Fluxo herda isso automaticamente.
Fluxo so pede alteracao quando precisa de alguem diferente, prazo diferente ou regra de excecao diferente.
```

Quando uma tabela abaixo citar `responsavel`, `aprovador` ou `fila de excecao`, leia como:

```text
mostrar apenas se o studio quiser trocar o padrao herdado da rotina
ou se aquele fluxo exigir uma aprovacao/triagem especifica.
```

## Decisoes Principais

### 1. Agente Nao Configura

O agente e uma area de navegacao, operacao e status.

Nao existe pagina de configuracoes do agente.

```text
Agente = onde o usuario encontra uma familia de rotinas.
Rotina = conjunto operacional para simular, publicar, pausar e acompanhar.
Fluxo = comportamento especifico configuravel.
```

### 2. Rotina Agrupa

A rotina existe para o dono/admin pensar por assunto do dia a dia, nao por automacao tecnica.

Exemplo:

```text
Agente Agenda
  Rotina Presenca e faltas
    B1 Confirmacao de presenca
    B2 Falta com aviso
    B3 No-show
    B14 Correcao de presenca
```

A rotina pode ter:

- status;
- versao publicada;
- lista de fluxos;
- simulacao do conjunto;
- publicacao;
- pausa;
- rollback;
- operacao do dia.

A rotina nao deve virar gaveta de configuracao solta.

Regra de composicao:

```text
Rotinas tem fluxos fixos definidos pela Taliya.
O studio pode ativar, pausar, ajustar e publicar os fluxos da rotina.
O studio nao monta uma rotina adicionando/removendo fluxos soltos.
```

### 2.1 Perfil Da Rotina

A rotina tem um perfil de operacao.

O perfil da rotina existe para o usuario nao precisar configurar os fluxos um por um.

Nomes user-facing:

- Mais manual;
- Equilibrado;
- Mais autonomo.

O perfil da rotina define automaticamente:

- quais fluxos ficam ativos;
- modo recomendado de cada fluxo;
- quanto humano entra na operacao;
- quais pontos pedem aprovacao;
- quais casos viram excecao;
- resumo do que vai acontecer quando publicar.

O perfil da rotina nao define:

- canal;
- integracao;
- permissao;
- cota;
- dados obrigatorios;
- billing;
- regra tecnica;
- composicao da rotina.

Regra:

```text
Perfil da rotina = configura varios fluxos de uma vez.
Modo do fluxo = define como um fluxo especifico funciona.
Ajuste individual do fluxo = excecao ao perfil da rotina.
```

Se o usuario alterar um fluxo individualmente, a rotina passa a mostrar:

```text
Perfil: Mais autonomo personalizado
1 fluxo diferente do perfil
```

### 2.2 O Que Cada Perfil Significa

| Perfil | Como explicar | O que muda nos fluxos |
|---|---|---|
| Mais manual | Voce controla quase tudo. O sistema organiza e o agente ajuda quando voce pedir ou aprovar. | Fluxos tendem a Manual ou Copiloto. Autonomos ficam desligados ou exigem aprovacao. |
| Equilibrado | O agente resolve o simples e chama humano nos pontos sensiveis. | Fluxos simples podem ser Autonomo; fluxos com excecao usam Autonomo com excecoes; fluxos sensiveis usam aprovacao. |
| Mais autonomo | O agente conduz mais etapas sozinho, dentro dos limites de cada fluxo. | Cada fluxo sobe ate o maior modo permitido pelo seu teto, mas ainda respeita aprovacao, excecao, cota, permissao e integracao. |

Mesmo no perfil Mais autonomo, um fluxo nunca ultrapassa seu teto.

O mapeamento exato de cada rotina e de cada fluxo fica em:

- `agents-flows-routine-profile-map.pt-BR.md`

### 2.3 Perfil Inicial Por Plano

O perfil inicial exibido na pagina de rotina e `Mais autonomo`, quando o plano e o preflight permitem.

| Plano | Como aparece |
|---|---|
| 0 agentes | Rotinas aparecem como catalogo/manual. Nao publica automacao. Pode simular valor e mostrar upgrade. |
| 1 agente | Apenas o agente contratado abre rotinas. Cada rotina abre em `Mais autonomo`, mas fluxos bloqueados por preflight ficam pendentes ou rebaixados com motivo. |
| 3 agentes | Rotinas dos agentes contratados abrem em `Mais autonomo`, com publicacao por rotina. Demais agentes aparecem como upgrade. |
| 7 agentes | Todas as rotinas abrem em `Mais autonomo`, respeitando teto, aprovacao, excecao, cota, permissao e integracao. |

`Mais autonomo` aparecer selecionado nao significa publicacao automatica. O usuario ainda precisa simular e revisar para publicar.

### 3. Fluxo Configura

Cada fluxo tem:

- modo;
- comportamento por modo;
- template, se houver mensagem;
- tom de voz;
- ajustes realmente importantes;
- roteamento humano, se houver aprovacao ou excecao;
- fallback;
- dependencias fixas;
- bloqueios;
- simulacao.

### 3.1 Ficha Obrigatoria Do Fluxo

Todo fluxo precisa ter uma ficha funcional estruturada.

Essa ficha e contrato do produto e do runtime. Ela nao vira formulario inteiro para o studio.

| Campo | O que define | Quem configura |
|---|---|---|
| objetivo | Resultado operacional esperado. | Taliya define; usuario le. |
| area do CRM | Onde o fluxo vive no CRM. | Taliya define. |
| agente responsavel | Qual agente e dono do fluxo. | Billing libera; Taliya define. |
| rotina | Qual rotina agrupa o fluxo. | Taliya define. |
| gatilho | O que inicia o fluxo: horario, evento, mensagem, webhook, botao ou lote. | Taliya define; usuario pode ajustar horario/cadencia quando fizer sentido. |
| condicao | O que precisa ser verdade para rodar. | Taliya define a regra; CRM/Integracoes/Billing/Uso validam. |
| acao | O que o fluxo pode fazer. | Taliya define; modo decide quem conduz. |
| modo | Quem conduz quando dispara. | Perfil da rotina sugere; usuario pode ajustar. |
| permissao | Quem pode configurar, aprovar, pausar e revisar. | Configuracoes/Permissoes e Billing validam. |
| canal | Canal usado, se houver. | Dependencia fixa; nao e ajuste solto. |
| dados necessarios | Dados minimos para executar. | CRM valida. |
| integracao necessaria | Provedor exigido, se houver. | Integracoes valida. |
| fallback | Caminho seguro quando nao pode agir. | Taliya sugere; usuario ajusta so se houver escolha real. |
| aprovacao | Quando precisa de humano antes de seguir. | Perfil/modo/risco definem; rotina herda aprovadores padrao. |
| cota estimada | Consumo previsto. | Uso/Cotas calcula. |
| risco | Nivel usado para bloquear, degradar ou pedir aprovacao. | Taliya define e runtime recalcula por contexto. |
| simulacao | Ultima simulacao valida. | Agentes/Fluxos gera. |
| status | Rascunho, simulado, publicado, ativo, pausado, bloqueado ou incidente. | Runtime atualiza. |
| auditoria | Eventos obrigatorios. | Auditoria registra. |

Na UI, a ficha aparece em camadas:

```text
Primeiro: modo, comportamento, bloqueio e proximo passo.
Depois: ajustes realmente importantes.
Avancado/leitura: gatilho, condicao, dados, canal, integracao, cota, risco e auditoria.
```

Regra:

```text
Todo fluxo tem esses campos.
Nem todo campo vira configuracao.
```

### 4. Tom De Voz Fica No Fluxo

O tom de voz e configuracao do fluxo.

Regra de produto:

```text
O primeiro tom escolhido em uma rotina vira sugestao automatica para os proximos fluxos da mesma rotina.
Cada fluxo pode manter esse tom ou trocar.
Nao existe checkbox para salvar como default.
Nao existe tom de voz no agente.
```

### 5. Template Fica No Fluxo

Template pertence ao fluxo porque cada fluxo fala sobre uma coisa diferente.

Exemplo:

- confirmacao de presenca tem template proprio;
- no-show tem template proprio;
- pagamento atrasado tem template proprio;
- reativacao tem template proprio.

O template pode ser fixo aprovado pela Taliya ou editavel dentro de campos seguros, dependendo do fluxo.

### 6. Canal Nao E Ajuste Solto

Canal e dependencia fixa do fluxo.

Exemplo:

```text
Fluxo Confirmacao de presenca
Canal necessario: WhatsApp
```

Se WhatsApp nao esta conectado, a tela nao pergunta qual canal usar. Ela mostra o bloqueio e permite reduzir o modo para Manual ou Copiloto quando fizer sentido.

### 7. Configuracao Visivel Deve Ser Minima

O studio so configura o que muda a operacao.

Nao expor:

- prompt livre;
- modelo de IA;
- ferramenta interna;
- payload;
- retry tecnico;
- idempotencia;
- politica de seguranca;
- regra de billing;
- integracao tecnica bruta;
- status tecnico detalhado;
- cota interna fina;
- limite sem valor claro para o dono.

Tambem nao expor como ajuste comum do fluxo:

- fontes aceitas;
- dono do lead;
- base de planos;
- documentos permitidos;
- tipos de midia aceitos;
- metricas exibidas;
- secoes do resumo;
- dados permitidos;
- canais alternativos quando o fluxo tem canal fixo;
- permissao real;
- cota real;
- integracao real.

Esses itens podem aparecer como leitura, bloqueio ou dependencia fixa.

### 8. Campos Que Podem Aparecer No Fluxo

Todo fluxo mostra o modo.

Os demais campos so aparecem quando forem necessarios:

| Campo | Quando aparece |
|---|---|
| Conteudo | Quando o fluxo envia mensagem, prepara resposta, resumo ou comunicado. |
| Tom de voz | Quando existe conteudo voltado para aluno/interessado ou comunicacao humana. |
| Texto interno | Quando o fluxo gera resumo, alerta ou tarefa para equipe. |
| Tempo/cadencia | Quando mudar horario, frequencia ou prazo muda a operacao. |
| Limite simples | Quando evita excesso: tentativas, convites, contatos ou lembretes. |
| Roteamento humano | Quando ha aprovacao, excecao, revisao ou mais de uma fila possivel. |
| Fallback | Quando existe uma escolha real; caso contrario vem fixo. |

### 9. Exposicao Progressiva

A pagina de ajustar rotina nao mostra todos os campos de uma vez.

Primeiro nivel:

- fluxo;
- modo;
- status;
- bloqueio;
- resumo do comportamento.

Ao abrir um fluxo:

- como funciona no modo escolhido;
- ajustes visiveis quando necessario;
- dependencias fixas;
- simulacao do fluxo.

Avancado:

- roteamento humano especifico;
- fallback especifico;
- detalhes de auditoria;
- detalhes de dependencia.

## Paginas Globais

### Catalogo De Agentes

Rota:

```text
/app/agentes
```

Mostra:

- os 7 agentes canonicos;
- status resumido por agente;
- quantidade de rotinas e fluxos;
- CTA para abrir cada agente.

Nao mostra:

- configuracao de agente;
- configuracao de rotina;
- lista de fluxos;
- KPI de cota;
- atividade recente;
- filtros;
- painel lateral;
- Agente de Configuracao.

Dinamicas:

- com 0 agentes, mostra os 7 agentes como catalogo indisponivel/upgrade, mas o CRM segue manual;
- com 1 agente, apenas o agente contratado abre rotinas configuraveis; os demais cards explicam que nao estao contratados;
- com 3 agentes, os 3 agentes do bundle abrem rotinas configuraveis; os demais ficam como nao contratados;
- com 7 agentes, todos os cards abrem seus agentes;
- downgrade pausa automacoes fora do entitlement, mas mantem historico;
- upgrade libera rotinas como rascunho, nunca como automacao ja publicada.

Imagem aprovada:

```text
52_round-4.1L_agentes_01_catalogo-agentes-aprovado.png
```
### Visao Geral Do Agente

Rota:

```text
/app/agentes/[agentId]
```

Mostra:

- nome do agente;
- papel operacional;
- status resumido: contratado, nao contratado, pausado ou bloqueado;
- rotinas do agente;
- quantidade de fluxos por rotina;
- CTA para abrir cada rotina.

Nao mostra:

- configuracoes do agente;
- tom geral do agente;
- modo geral do agente;
- fallback geral do agente;
- KPIs;
- cota;
- atividade recente;
- painel lateral;
- Agente de Configuracao;
- simulacao/publicacao fora da rotina.

Imagem aprovada para Agenda:

```text
53_round-4.1L_agentes_02_agente-agenda-rotinas-aprovado.png
```

Dinamicas:

- se o agente nao esta contratado, rotinas aparecem como preview/upgrade;
- se uma rotina tem rascunho, mostra status resumido no card;
- se uma rotina esta bloqueada, mostra motivo resumido no chip/status;
- se ha excecao, mostra `Excecao aberta` no card, mas continua abrindo a rotina;
- se ha aprovacao, mostra `Aprovacao pendente` no card, mas continua abrindo a rotina;
- se cota acabou, mostra `Cota bloqueada` no card e o detalhe fica em Uso/Cotas ou na rotina.

### Pagina Da Rotina

Rota:

```text
/app/agentes/[agentId]/rotinas/[routineId]
```

Papel:

Ser a pagina onde o dono/admin entende e controla uma rotina especifica.

Esta pagina nao e dashboard, nao e log e nao e lista de execucoes.

Imagem aprovada para o modelo de rotina:

```text
54_round-4.1L_agentes_03_rotina-presenca-faltas-aprovado.png
```

Estrutura obrigatoria:

- breadcrumb: `Agentes / [Agente] / [Rotina]`;
- titulo da rotina;
- subtitulo curto;
- chip de status da rotina;
- bloco `Como essa rotina deve trabalhar?`;
- seletor com `Mais manual`, `Equilibrado` e `Mais autonomo`;
- `Mais autonomo` selecionado por padrao quando o plano e preflight permitirem;
- texto explicando que a escolha se aplica aos fluxos e que cada fluxo pode ser ajustado individualmente;
- cards dos fluxos da rotina;
- acoes no rodape: `Simular rotina`, `Ajustar fluxos`, `Revisar para publicar`;
- painel direito com Agente de Configuracao.

Bloco obrigatorio:

```text
Como essa rotina deve trabalhar?

[Mais manual] [Equilibrado] [Mais autonomo]

Escolha um comportamento para a rotina inteira.
A Taliya aplica isso aos fluxos abaixo, e voce pode ajustar qualquer fluxo individualmente.
```

Regra dos cards de fluxo:

- nao exibir ID tecnico como `B1`, `C3` ou `D10` no titulo do card;
- titulo deve ser o nome humano do fluxo;
- chip de modo e chip de status ficam lado a lado no topo do card;
- o card deve ter explicacao humana e detalhes operacionais;
- detalhes tecnicos aparecem como linhas curtas, nao como tabela;
- cada card termina com CTA `Ver e ajustar`.

Campos do card de fluxo:

- titulo humano;
- chip de modo: `Manual`, `Copiloto`, `Autonomo`, `Autonomo com aprovacao` ou `Autonomo com excecoes`;
- chip de status: `Pronto`, `Precisa aprovacao`, `Bloqueado`, `Pausado`, `Pendente` ou similar;
- explicacao em linguagem natural do que vai acontecer;
- `Gatilho`;
- `Acao`;
- `Chama equipe`, `Aprovacao` ou `Fallback`, conforme o fluxo;
- CTA `Ver e ajustar`.

Exemplo de card:

```text
Confirmação de presença    [Autonomo] [Pronto]

Antes da aula, a Taliya envia confirmação para os alunos,
registra quem confirmou e deixa pendente quem não respondeu.

Gatilho: antes da aula
Acao: enviar confirmacao e registrar resposta
Chama equipe: falha de envio ou conflito

[Ver e ajustar]
```

Quando o usuario troca o perfil:

- a tela recalcula os modos dos fluxos;
- mantem ajustes individuais ja feitos, mas avisa que eles diferem do perfil;
- permite "Aplicar perfil a todos" para remover personalizacoes;
- exige nova simulacao antes de publicar.

Dinamicas:

- nunca publicada: mostra cards com status `Nao publicada` ou `Pendente`;
- rascunho simulado: mostra status da rotina `Rascunho simulado`;
- rascunho diferente da versao ativa: mostra status resumido e leva detalhes para a rotina/ajuste;
- publicada: cards continuam explicativos, com status de operacao;
- pausada: mostra o que parou e o que segue manual;
- bloqueada: chip do fluxo mostra o bloqueio principal;
- sem permissao: leitura continua, acao sensivel exige aprovacao/permissao;
- cota esgotada: chip do fluxo mostra `Cota bloqueada`, detalhe fica em Uso/Cotas;
- integracao/canal com falha: chip mostra bloqueio, detalhe fica em Integracoes;
- ajuste individual: rotina mostra `Personalizada` e quantos fluxos diferem do perfil.

### Ajustar Rotina E Fluxos

Rota:

```text
/app/agentes/[agentId]/rotinas/[routineId]/ajustar
```

Mostra os fluxos da rotina e abre a area de cada fluxo.

Antes da lista de fluxos, mostra o perfil atual da rotina.

```text
Perfil da rotina: Mais autonomo personalizado

Este perfil define o modo inicial dos fluxos.
Voce pode ajustar um fluxo individualmente quando ele precisar operar diferente.
```

Tambem mostra, quando a rotina tiver aprovacao ou excecao:

- responsaveis padrao da rotina, podendo ter mais de um;
- aprovadores padrao da rotina, podendo ter mais de um;
- fila humana padrao para excecoes;
- prazo padrao para resposta humana, quando existir SLA operacional.

Isso nao e configuracao do agente.
Isso evita repetir o mesmo responsavel/aprovador em cada fluxo.

Em cada fluxo:

- objetivo;
- modo escolhido;
- origem do modo: perfil da rotina ou ajuste individual;
- comportamento real no modo escolhido;
- ajustes visiveis quando necessario;
- template;
- tom de voz;
- roteamento humano;
- aprovadores, se houver;
- fallback;
- dependencias fixas;
- bloqueios;
- simulacao do fluxo.

Dinamica principal:

```text
Ao trocar o modo, muda o comportamento exibido e mudam os ajustes visiveis.
```

Se o modo do fluxo for alterado manualmente:

```text
Este fluxo ficou diferente do perfil da rotina.
```

Opcoes:

- manter ajuste individual;
- voltar ao perfil da rotina;
- aplicar perfil da rotina em todos os fluxos.

Modos:

- Manual;
- Copiloto;
- Autonomo com aprovacao;
- Autonomo com excecoes;
- Autonomo.

Regras:

- se o teto do fluxo e 3, nao mostra modos 4 e 5;
- se o teto do fluxo e 4, nao mostra modo 5;
- se plano/cota/permissao/integracao bloqueia, modo autonomo fica indisponivel;
- se falta template obrigatorio, nao publica envio autonomo;
- se falta aprovador em fluxo de aprovacao, nao publica;
- se falta fila humana em fluxo com excecao, nao publica.

Regra de prioridade:

```text
Teto do fluxo > bloqueios reais > ajuste individual > perfil da rotina.
```

Leitura:

- o perfil sugere;
- o ajuste individual sobrescreve;
- bloqueios reais rebaixam ou impedem;
- o teto do fluxo nunca pode ser ultrapassado.

### Simular Rotina

`Simular rotina` nao e uma pagina visual propria no MVP.

Ela e uma acao da pagina da rotina.

Ela valida o conjunto dos fluxos e atualiza:

- status geral da rotina;
- resultado por fluxo;
- preflight consolidado;
- CTA seguinte;
- bloqueios;
- avisos;
- prontidao para `Publicar rotina`.

O contrato completo fica em:

```text
agents-flows-routine-simulation-result-contract.pt-BR.md
```

Nao usar celular/conversa aqui. Celular/conversa pertence a `Simular fluxo`.

### Publicar Versao

Rota:

```text
/app/agentes/[agentId]/rotinas/[routineId]/publicar
```

Mostra:

- versao que sera publicada;
- perfil da rotina;
- fluxos que seguem o perfil;
- fluxos personalizados individualmente;
- modos de cada fluxo;
- ajustes que entram em vigor;
- templates e tons usados;
- checagens de preflight;
- o que passa a acontecer;
- o que nao passa a acontecer;
- bloqueios;
- quem esta publicando;
- trilha de auditoria.

Tambem mostra um resumo em linguagem simples:

```text
O que muda ao publicar esta rotina

Vai acontecer sozinho:
- ...

Vai pedir aprovacao:
- ...

Vai chamar humano quando sair do esperado:
- ...

Continua manual:
- ...
```

Bloqueia publicacao se faltar:

- permissao;
- simulacao valida;
- template obrigatorio;
- tom de voz;
- aprovador obrigatorio;
- fila humana obrigatoria;
- fallback;
- cota necessaria;
- integracao necessaria;
- dados obrigatorios;
- consentimento/opt-out valido.

### Execucoes Da Rotina

Nao criar pagina nova de operacao leve em Agentes/Fluxos.

A pagina da rotina publicada pode mostrar status leve e atalhos para execucoes.

Detalhe completo de execucao fica na rota global:

```text
/app/fluxos/execucoes/[runId]
```

Contrato da operacao leve pos-publicacao:

```text
agents-flows-post-publication-light-ops-contract.pt-BR.md
```

### Detalhe Global De Execucao

Rota:

```text
/app/fluxos/execucoes/[runId]
```

Mostra:

- agente;
- rotina;
- perfil da rotina publicado naquele momento;
- fluxo;
- versao publicada;
- modo ativo;
- gatilho;
- dados usados;
- mensagens/acoes feitas;
- decisoes do agente;
- aprovacao, se houve;
- humano chamado, se houve;
- fallback;
- cota;
- auditoria;
- links para objeto do CRM.

Essa pagina e Control Plane. Ela explica o que aconteceu. Ela nao configura fluxo.

### Pausa, Fallback E Rollback

Preferencia de UX:

```text
Pausar rotina, pausar fluxo e rollback aparecem como modal/drawer, nao como pagina pesada.
```

Pausar rotina:

- para autonomos da rotina;
- preserva manual e visualizacao;
- registra auditoria.

Pausar fluxo:

- para um fluxo especifico;
- outros fluxos da rotina continuam.

Rollback:

- volta para versao publicada anterior;
- exige permissao;
- exige confirmacao;
- registra auditoria;
- nao apaga historico.

## Dinamica Do Fluxo Por Modo

Todo fluxo usa a mesma logica de leitura:

```text
Modo do fluxo = quem conduz quando o fluxo dispara.
Botao de copiloto = ajuda pontual quando o humano pede ou precisa decidir.
```

### Manual

O sistema organiza.

Mostra:

- tarefa, checklist, caso ou item na tela de origem;
- responsavel humano;
- prazo, se fizer sentido;
- botao de ajuda se agente contratado e permitido.

Nao mostra:

- sugestao automatica do agente;
- envio autonomo;
- execucao autonoma.

### Copiloto

O agente sugere. Humano executa.

Mostra:

- sugestao;
- resumo;
- rascunho;
- recomendacao;
- botoes: aprovar, editar, rejeitar, transformar em tarefa.

Se o humano rejeitar, a execucao segue manual.

### Autonomo Com Aprovacao

O agente adianta, mas para antes de impacto sensivel.

Mostra:

- acao preparada;
- aprovador;
- prazo de aprovacao;
- efeito da aprovacao;
- fallback se ninguem aprovar.

### Autonomo Com Excecoes

O agente conduz o normal e chama humano quando sai do trilho.

Mostra:

- caso normal;
- sinais que viram excecao;
- fila humana;
- regra de escalonamento, se houver;
- onde a operacao continua.

### Autonomo

O agente resolve o caso comum sozinho dentro de limites.

Mostra:

- limites simples;
- condicoes obrigatorias;
- fallback;
- auditoria;
- quando para automaticamente.

## Agente Atendimento

Rota:

```text
/app/agentes/atendimento
```

Papel:

Organizar conversas, responder duvidas permitidas, proteger identidade/opt-out e chamar humano quando necessario.

Rotinas:

1. Conversas e triagem.
2. Identidade e privacidade.

### Atendimento - Conversas E Triagem

Rota:

```text
/app/agentes/atendimento/rotinas/conversas-e-triagem
```

| ID | Fluxo | Maior modo permitido | Ajustes visiveis quando necessario | Fixo e nao configuravel |
|---|---|---|---|---|
| A1 | Nova Conversa | Autonomo com excecoes | limite de respostas; fila de excecao se diferente do padrao; template/tom se houver resposta automatica | canal da conversa recebida; opt-out; identidade minima; sinais de risco; auditoria |
| A2 | Duvidas Permitidas | Autonomo | limite por conversa; template/tom | respostas permitidas vem da base aprovada; bloqueio fora da base; auditoria |
| A3 | Aluno Existente | Autonomo com excecoes | fila de excecao se diferente do padrao; template/tom se houver resposta; botao de ajuda manual | dados sensiveis protegidos; identidade validada; permissao; pedidos sensiveis chamam humano |
| A4 | Fora Do Escopo | Autonomo | resposta padrao; destino da tarefa/caso; tom | politica de escopo; bloqueio de promessa fora do CRM; auditoria |
| A5 | Chamada Humana | Autonomo | fila destino se diferente do padrao; prioridade | campos do resumo definidos pelo produto; criterio de baixa confianca/risco; registro da chamada humana |
| A10 | Ciclo De Vida/SLA | Autonomo | tempo de SLA; prioridade; texto interno do alerta | origem da conversa; trilha de SLA; fila natural da conversa; auditoria |

### Atendimento - Identidade E Privacidade

Rota:

```text
/app/agentes/atendimento/rotinas/identidade-e-privacidade
```

| ID | Fluxo | Maior modo permitido | Ajustes visiveis quando necessario | Fixo e nao configuravel |
|---|---|---|---|---|
| A6 | Consentimento/Opt-Out | Autonomo | responsavel de revisao se a frase for ambigua; texto de confirmacao; tom | opt-out sempre bloqueia envio; auditoria obrigatoria; canal de origem |
| A7 | Identidade/Midias | Autonomo com excecoes | responsavel de revisao; campos de identificacao que o studio quer pedir | documento/midia nao vira dado confiavel sem validacao; permissao; tipos aceitos definidos pelo produto; auditoria |
| A8 | Privacidade/Dados | Autonomo com aprovacao | aprovador de privacidade; prazo do caso; texto de recebimento do pedido | pedido LGPD/dados sensiveis exige caso e auditoria; nao executa exclusao livre |
| A9 | Telefone Compartilhado E Identidade | Autonomo com aprovacao | responsavel de revisao; prazo do caso | regra de validacao definida pelo produto; telefone ambiguo nao libera acao sensivel; identidade validada antes de expor dados |

## Agente Agenda

Rota:

```text
/app/agentes/agenda
```

Papel:

Organizar presenca, faltas, reposicoes, vagas, grade, primeira aula e eventos.

Rotinas:

1. Presenca e faltas.
2. Vagas, reposicoes e lista de espera.
3. Grade e capacidade.
4. Primeira aula e aulas especiais.
5. Agenda experimental.

### Agenda - Presenca E Faltas

Rota:

```text
/app/agentes/agenda/rotinas/presenca-e-faltas
```

| ID | Fluxo | Maior modo permitido | Ajustes visiveis quando necessario | Fixo e nao configuravel |
|---|---|---|---|---|
| B1 | Confirmacao De Presenca | Autonomo | quando confirmar; template/tom; tentativas; acao se nao responder; fila de excecao | WhatsApp como dependencia quando houver envio; aula/aluno ativos; opt-out; auditoria |
| B2 | Falta Com Aviso | Autonomo com excecoes | prazo para aviso; oferecer reposicao; template/tom; fila de excecao | aula existente; regra base de chamada; registro da falta; historico |
| B3 | No-Show | Autonomo com excecoes | quando considerar no-show; criar tarefa de recuperacao; template/tom; fila para casos sensiveis | chamada encerrada; aluno/aula vinculados; auditoria |
| B14 | Correcao Presenca | Autonomo com aprovacao | aprovador; prazo; motivo obrigatorio; fallback se ninguem aprovar | correcao exige motivo; motivos base definidos pelo produto; auditoria; usuario autorizado |

### Agenda - Vagas, Reposicoes E Lista De Espera

Rota:

```text
/app/agentes/agenda/rotinas/vagas-reposicoes-lista-espera
```

| ID | Fluxo | Maior modo permitido | Ajustes visiveis quando necessario | Fixo e nao configuravel |
|---|---|---|---|---|
| B4 | Recuperar Vaga Aberta | Autonomo com excecoes | antecedencia para oferecer vaga; limite de convites; template/tom; fila de excecao | capacidade da aula; elegibilidade; prioridade base da lista; consentimento; auditoria |
| B5 | Reposicao/Remarcacao | Autonomo com aprovacao | aprovador; prazo limite; template/tom; fallback | credito e politica vigente; regra de credito do CRM; conflito de agenda; auditoria |
| B6 | Lista De Espera | Autonomo com excecoes | tempo para responder; limite de convites; template/tom; fila de excecao | capacidade real; prioridade e ordem auditavel da lista; consentimento |
| B13 | Creditos Reposicao | Autonomo com aprovacao | aprovador; validade se o studio permite variar; aviso ao aluno se houver | saldo/credito auditavel; situacoes elegiveis; motivo obrigatorio; permissao |

### Agenda - Grade E Capacidade

Rota:

```text
/app/agentes/agenda/rotinas/grade-e-capacidade
```

| ID | Fluxo | Maior modo permitido | Ajustes visiveis quando necessario | Fixo e nao configuravel |
|---|---|---|---|---|
| B8 | Mudanca Horario Fixo | Autonomo com aprovacao | aprovador; antecedencia minima; template/tom de aviso; fila de excecao | impacto em aluno/turma; simulacao de conflito; auditoria |
| B9 | Cancelamento Pelo Studio | Autonomo com aprovacao | aprovador; template/tom de comunicado; prazo minimo | aula afetada; alunos impactados; opcoes oferecidas definidas pelo produto; registro operacional |
| B10 | Conflito Capacidade | Autonomo com aprovacao | aprovador; responsavel do caso | limite de capacidade; prioridade base; acao sugerida pelo produto; conflito detectado pelo CRM; auditoria |
| B11 | Ajuste De Grade | Autonomo com aprovacao | aprovador; data de vigencia; comunicacao necessaria | simulacao obrigatoria; limite de alteracao definido pelo produto; impacto na agenda; auditoria |

### Agenda - Primeira Aula E Aulas Especiais

Rota:

```text
/app/agentes/agenda/rotinas/primeira-aula-aulas-especiais
```

| ID | Fluxo | Maior modo permitido | Ajustes visiveis quando necessario | Fixo e nao configuravel |
|---|---|---|---|---|
| B15 | Primeira Aula | Autonomo com excecoes | lembrete; template/tom; fila de excecao | aluno/aula vinculados; checklist e gates obrigatorios; auditoria |
| B16 | Aula Especial/Workshop | Autonomo com aprovacao | aprovador; capacidade operacional; template/tom; prazo | evento/aula especial; limite de vagas; regra base de lista de espera; publicacao auditavel |

### Agenda - Agenda Experimental

Rota:

```text
/app/agentes/agenda/rotinas/agenda-experimental
```

| ID | Fluxo | Maior modo permitido | Ajustes visiveis quando necessario | Fixo e nao configuravel |
|---|---|---|---|---|
| B7 | Disponibilidade Experimental | Autonomo com excecoes | janela de horarios oferecidos; limite de ofertas; template/tom; quando chamar humano | agenda real; consentimento; interessado vinculado |
| B12 | Experimental No-Show | Autonomo com excecoes | quando abordar; tentativas; template/tom; encaminhamento humano | aula experimental registrada; historico do interessado; opt-out |

## Agente Vendas

Rota:

```text
/app/agentes/vendas
```

Papel:

Capturar, qualificar, acompanhar experimental, apoiar objecoes e preparar conversao sem prometer o que o CRM nao permite.

Rotinas:

1. Captura e qualificacao.
2. Experimental e acompanhamento.
3. Conversao e matricula.

### Vendas - Captura E Qualificacao

Rota:

```text
/app/agentes/vendas/rotinas/captura-e-qualificacao
```

| ID | Fluxo | Maior modo permitido | Ajustes visiveis quando necessario | Fixo e nao configuravel |
|---|---|---|---|---|
| C15 | Entrada Multicanal De Lead | Autonomo com excecoes | fila de triagem se diferente do padrao; regra de duplicidade visivel | origem registrada; fontes aceitas pelo CRM; contato minimo; dono natural do lead; auditoria |
| C8 | Origem/Qualificacao | Autonomo com excecoes | responsavel se diferente do padrao | campos de qualificacao vem do CRM; origem auditavel; lead vinculado; regra de duplicidade; historico |
| C9 | Perda Comercial | Autonomo com aprovacao | motivo; aprovador se perda sensivel; texto interno | perda definitiva exige registro; responsavel padrao da oportunidade; auditoria |
| C10 | Indicacao | Autonomo com aprovacao | aprovador de beneficio; mensagem/tom se houver aviso | beneficio nao concedido livremente; regra de vinculo definida pelo produto; aluno/interessado vinculados |

### Vendas - Experimental E Acompanhamento

Rota:

```text
/app/agentes/vendas/rotinas/experimental-e-acompanhamento
```

| ID | Fluxo | Maior modo permitido | Ajustes visiveis quando necessario | Fixo e nao configuravel |
|---|---|---|---|---|
| C2 | Aula Experimental | Autonomo com excecoes | janela de horarios oferecidos; responsavel comercial se diferente do padrao; limite de tentativas; template/tom | agenda real; consentimento; interessado vinculado |
| C3 | Lembrete Experimental | Autonomo | quando lembrar; template; tom; limite por aula | aula experimental existente; opt-out; dependencia de mensagem |
| C4 | Pos-Aula Experimental | Autonomo com excecoes | cadencia; quando virar tarefa; template/tom | aula concluida; interessado vinculado; responsavel comercial padrao; auditoria |
| C5 | Follow-Up Comercial | Autonomo com excecoes | cadencia; limite de tentativas; template/tom | consentimento; responsavel comercial padrao; historico da oportunidade; opt-out |
| C12 | Demanda Sem Vaga | Autonomo com excecoes | encaminhamento para lista de espera; template/tom; quando chamar humano | capacidade real; regra de promessa definida pelo produto; nao prometer vaga inexistente; auditoria |

### Vendas - Conversao E Matricula

Rota:

```text
/app/agentes/vendas/rotinas/conversao-e-matricula
```

| ID | Fluxo | Maior modo permitido | Ajustes visiveis quando necessario | Fixo e nao configuravel |
|---|---|---|---|---|
| C1 | Valores E Planos | Autonomo com excecoes | template/tom; quando chamar humano | valores e base de planos vem do CRM; sem desconto livre; auditoria |
| C6 | Pre-Matricula | Autonomo com aprovacao | aprovador; prazo; responsavel comercial se diferente do padrao | matricula exige dados obrigatorios; checklist do produto; plano valido; auditoria |
| C7 | Objecoes | Autonomo com aprovacao | aprovador; limite de promessa; template/tom | base de respostas definida pelo produto/CRM; promessa comercial limitada; desconto/oferta exige aprovacao |
| C11 | Checkout/Abandono | Autonomo com excecoes | cadencia; limite de contato; template/tom | checkout/pagamento de origem; responsavel comercial padrao; opt-out; auditoria |
| C13 | Interessado Para Aluno | Autonomo com aprovacao | aprovador; responsavel se diferente do padrao | conversao cria/ativa aluno; plano vem do CRM; checklist de matricula; dados obrigatorios; auditoria |
| C14 | Upsell/Upgrade | Autonomo com aprovacao | aprovador; template/tom da proposta; limite de oferta | plano/preco do CRM; responsavel comercial padrao; sem alteracao comercial livre |

## Agente Financeiro

Rota:

```text
/app/agentes/financeiro
```

Papel:

Apoiar cobrancas, falhas, documentos, conciliacao e mudancas financeiras com aprovacao onde houver impacto sensivel.

Rotinas:

1. Lembretes e pagamentos.
2. Ciclo do plano do aluno.
3. Excecoes e documentos financeiros.

### Financeiro - Lembretes E Pagamentos

Rota:

```text
/app/agentes/financeiro/rotinas/lembretes-e-pagamentos
```

| ID | Fluxo | Maior modo permitido | Ajustes visiveis quando necessario | Fixo e nao configuravel |
|---|---|---|---|---|
| D1 | Lembrete Vencimento | Autonomo | quando lembrar; template; tom; limite por cobranca; acao se nao responder | cobranca existente; opt-out; dependencia de mensagem; auditoria |
| D2 | Pagamento Atrasado | Autonomo com excecoes | tentativas; fila financeira; sinais que chamam humano; template/tom | valor e vencimento do CRM; sem acordo livre; auditoria |
| D3 | Pix/Link | Autonomo com aprovacao | aprovador; template/tom; limite de valor para aprovacao; prazo | provedor financeiro; pagamento existente; link idempotente |
| D7 | Falha Pagamento | Autonomo com excecoes | tentativas; fila financeira; quando abrir caso; template/tom | status do provedor; cobranca vinculada; auditoria |
| D8 | Recibo/Nota | Autonomo com excecoes | responsavel se exigir revisao; template/tom; fallback | documento fiscal/financeiro vem do CRM/provedor; documentos permitidos definidos pelo produto; auditoria |
| D10 | Conciliacao Interna | Autonomo com aprovacao | aprovador; responsavel; prazo | confianca minima definida pelo produto; pagamento/cobranca existentes; conciliacao auditavel |

### Financeiro - Ciclo Do Plano Do Aluno

Rota:

```text
/app/agentes/financeiro/rotinas/ciclo-do-plano-do-aluno
```

| ID | Fluxo | Maior modo permitido | Ajustes visiveis quando necessario | Fixo e nao configuravel |
|---|---|---|---|---|
| D5 | Renovacao Plano | Autonomo com aprovacao | aprovador; antecedencia; template/tom | plano vigente; responsavel financeiro padrao; preco do CRM; auditoria |
| D9 | Pausa/Trancamento | Autonomo com aprovacao | aprovador; prazo; responsavel se diferente do padrao | impacto mostrado pelo CRM; mudanca afeta agenda/cobranca; motivo obrigatorio |
| D15 | Encerramento Ou Alteracao Efetiva De Plano | Autonomo com aprovacao | aprovador; comunicacao; responsavel se diferente do padrao | checklist do produto; alteracao efetiva exige auditoria; plano/cobranca vinculados |

### Financeiro - Excecoes E Documentos Financeiros

Rota:

```text
/app/agentes/financeiro/rotinas/excecoes-documentos-financeiros
```

| ID | Fluxo | Maior modo permitido | Ajustes visiveis quando necessario | Fixo e nao configuravel |
|---|---|---|---|---|
| D4 | Confirmacao Pagamento | Autonomo com aprovacao | aprovador; responsavel se exigir revisao; prazo | evidencia exigida pelo produto; confirmacao exige prova; webhook/evidencia auditavel |
| D6 | Excecoes Financeiras | Autonomo com aprovacao | aprovador obrigatorio; prazo; responsavel | tipos de excecao definidos pelo produto; desconto/acordo/cortesia nao autonomos livres |
| D11 | Contrato/Termos | Autonomo com aprovacao | aprovador; template; tom; prazo | contrato/termo aprovado; aceite auditavel |
| D12 | Bloqueio/Liberacao | Autonomo com aprovacao | aprovador; motivo; texto interno; fallback | bloquear/liberar exige permissao e auditoria |
| D13 | Creditos/Cortesias | Autonomo com aprovacao | aprovador; limite de valor; motivo; responsavel | credito/cortesia exige motivo e auditoria |
| D14 | Fechamento Mensal | Autonomo com excecoes | responsavel; frequencia; quando abrir tarefa | secoes do resumo definidas pelo produto; dados financeiros do CRM; sem alteracao de registro pelo resumo |

## Agente Retencao

Rota:

```text
/app/agentes/retencao
```

Papel:

Detectar risco, organizar prevencao, apoiar retorno e proteger casos sensiveis de cancelamento, reclamacao e saude/evento pessoal.

Rotinas:

1. Retencao preventiva.
2. Casos sensiveis.

### Retencao - Retencao Preventiva

Rota:

```text
/app/agentes/retencao/rotinas/retencao-preventiva
```

| ID | Fluxo | Maior modo permitido | Ajustes visiveis quando necessario | Fixo e nao configuravel |
|---|---|---|---|---|
| E1 | Queda Frequencia | Autonomo com excecoes | regra de queda; responsavel; cadencia; template/tom | presenca historica; limite de contato; auditoria |
| E2 | Aluno Inativo | Autonomo com excecoes | dias de inatividade; responsavel; limite de contato; template/tom | status do aluno; opt-out; historico |
| E3 | Retorno | Autonomo com excecoes | responsavel se diferente do padrao; quando chamar humano; template/tom | aluno existente; disponibilidade real; regra de agenda do CRM; auditoria |
| E6 | Satisfacao | Autonomo com excecoes | janela; responsavel; quando abrir reclamacao; template/tom | feedback/reclamacao protegidos; limite de contato |
| E7 | Retorno Apos Pausa | Autonomo com excecoes | antecedencia; responsavel se diferente do padrao; template/tom | pausa registrada; regra de agenda do CRM; impacto financeiro/agenda fixo |
| E10 | Marco Engajamento | Autonomo com excecoes | responsavel; limite de contato; template/tom | tipos de marco definidos pelo produto; historico do aluno; opt-out; auditoria |

### Retencao - Casos Sensiveis

Rota:

```text
/app/agentes/retencao/rotinas/casos-sensiveis
```

| ID | Fluxo | Maior modo permitido | Ajustes visiveis quando necessario | Fixo e nao configuravel |
|---|---|---|---|---|
| E4 | Risco Cancelamento | Autonomo com aprovacao | dono do caso; aprovador; quando pausar automacoes; template/tom | risco alto vira caso; sem oferta livre; auditoria |
| E5 | Reativacao Ex-Aluno | Autonomo com aprovacao | aprovador; cadencia; template/tom | segmento permitido vem do CRM; consentimento; ex-aluno elegivel; opt-out |
| E8 | Risco Por Perfil | Autonomo com aprovacao | aprovador; responsavel; acao permitida | segmento sensivel vem do CRM e exige aprovacao; auditoria |
| E9 | Pos-Cancelamento | Autonomo com aprovacao | aprovador; quando contatar; responsavel; template/tom | cancelamento concluido; limite de contato; auditoria |
| E11 | Saude/Evento Pessoal | Autonomo com aprovacao | dono do caso; aprovador; tarefa humana | visibilidade definida por permissao; dado sensivel protegido; sem acao automatica livre |
| E12 | Segmentacao Risco | Autonomo com aprovacao | aprovador; acao permitida; responsavel | segmento vem do CRM; uso de segmento exige auditoria; sem campanha livre |
| E13 | Reclamacao E Recuperacao De Confianca | Autonomo com aprovacao | dono do caso; aprovador; pausa automatica; resposta/tom | reclamacao vira caso; compensacao/oferta exige aprovacao |

## Agente Gestao/Governanca

Rota:

```text
/app/agentes/gestao-governanca
```

Papel:

Priorizar operacao, expor gargalos, monitorar cotas, qualidade, incidentes, auditoria e mudancas de politica.

Rotinas:

1. Comando operacional.
2. Governanca de agentes.
3. Integracoes e importacao.

### Gestao/Governanca - Comando Operacional

Rota:

```text
/app/agentes/gestao-governanca/rotinas/comando-operacional
```

| ID | Fluxo | Maior modo permitido | Ajustes visiveis quando necessario | Fixo e nao configuravel |
|---|---|---|---|---|
| F1 | Prioridades Dia | Autonomo | horario do resumo; responsavel | secoes essenciais e fontes vem do produto/CRM; sem criar regra nova; auditoria do resumo |
| F2 | Dinheiro Na Mesa | Autonomo com excecoes | frequencia; responsavel; quando abrir tarefa | metricas definidas pelo produto; dados financeiros do CRM; sem acao financeira livre |
| F3 | Fila Humana | Autonomo | prioridade; responsaveis se diferente do padrao; tempo de destaque | filas reais de tarefas/aprovacoes; permissao |
| F4 | Gargalos | Autonomo com excecoes | frequencia; responsavel; tipo de alerta; limite de abertura de tarefa | metricas do CRM; sem mudar operacao automaticamente |
| F5 | Resumo Semanal | Autonomo | dia/hora; destinatarios internos | secoes definidas pelo produto; dados do periodo; sem envio externo livre |
| F6 | Qualidade Dados | Autonomo com excecoes | responsavel; prioridade; quando criar tarefa | tipos de dado definidos pelo produto; dado canonico do CRM; merge/exclusao exige aprovacao |
| F10 | Capacidade/Crescimento | Autonomo com excecoes | frequencia; responsavel; limite de alerta | metricas definidas pelo produto; capacidade/agenda reais; sugestao nao altera grade sozinha |

### Gestao/Governanca - Governanca De Agentes

Rota:

```text
/app/agentes/gestao-governanca/rotinas/governanca-de-agentes
```

| ID | Fluxo | Maior modo permitido | Ajustes visiveis quando necessario | Fixo e nao configuravel |
|---|---|---|---|---|
| F7 | Creditos/Limites | Autonomo | alertas de 70/90/100; responsavel; politica de economia visivel | billing/uso sao fonte primaria; cota nao editada aqui |
| F8 | Performance | Autonomo com excecoes | frequencia; responsavel; quando abrir tarefa | metricas definidas pelo produto; execucoes/auditoria como fonte; nao altera fluxo sozinho |
| F9 | Permissoes/Auditoria | Autonomo com aprovacao | aprovador; responsavel; prazo | tipos de evento definidos pelo produto; permissao real fica em Configuracoes/Permissoes; auditoria imutavel |
| F13 | Teste De Fluxo | Autonomo | cenarios de simulacao; responsavel por revisao | exemplos sugeridos pelo produto; teste nao publica sozinho; resultado bloqueia se falhar |
| F14 | Incidente De Automacao E Correcao Operacional | Autonomo com excecoes | severidade; responsavel; auto-pausa; criterio de reabertura | incidente fica em Operacao; correcao sensivel exige humano |
| F15 | Mudanca De Politica Ou Regra Operacional | Autonomo com aprovacao | aprovador; data de vigencia; simulacao; comunicacao interna | politica versionada; publicacao auditavel |

### Gestao/Governanca - Integracoes E Importacao

Rota:

```text
/app/agentes/gestao-governanca/rotinas/integracoes-e-importacao
```

| ID | Fluxo | Maior modo permitido | Ajustes visiveis quando necessario | Fixo e nao configuravel |
|---|---|---|---|---|
| F11 | Falhas/Webhooks | Autonomo com excecoes | responsavel; severidade; auto-pausa | logs ficam na integracao; retry seguro e idempotencia definidos pelo produto; retry nao idempotente bloqueado |
| F12 | Importacao/Migracao | Autonomo com aprovacao | aprovador; lote; responsavel; amostra de revisao | importacao/migracao exige job auditavel; merge em lote aprovado |

## Agente Historico/Professor

Rota:

```text
/app/agentes/historico-professor
```

Papel:

Apoiar professor com contexto permitido, notas, repasses, linha do tempo, documentos e protecao de dados sensiveis.

Rotinas:

1. Aula com contexto.
2. Historico protegido.

### Historico/Professor - Aula Com Contexto

Rota:

```text
/app/agentes/historico-professor/rotinas/aula-com-contexto
```

| ID | Fluxo | Maior modo permitido | Ajustes visiveis quando necessario | Fixo e nao configuravel |
|---|---|---|---|---|
| G1 | Contexto Antes Aula | Autonomo com excecoes | professor se diferente do padrao; quando chamar humano | secoes do resumo definidas pelo produto; visibilidade vem de permissao; permissao de historico; dado sensivel protegido |
| G2 | Observacao Pos-Aula | Autonomo com excecoes | lembrete; professor; template/tom interno | tipos de nota definidos pelo produto; aula finalizada; autor da nota; auditoria |
| G4 | Objetivo/Evolucao | Autonomo com excecoes | professor/responsavel; frequencia; tarefa | secoes de evolucao definidas pelo produto; historico do aluno; sem avaliacao clinica livre |
| G8 | Repasse Entre Professores | Autonomo com excecoes | professor destino; quando chamar humano | campos do resumo definidos pelo produto; visibilidade permitida; aluno/aula vinculados |
| G9 | Lembrete Professor | Autonomo | horario; frequencia; destino; texto interno | professor/aula existentes; tarefa interna; auditoria |
| G12 | Linha Do Tempo | Autonomo com excecoes | filtro padrao; responsavel por revisao | tipos de evento definidos pelo produto; linha do tempo vem do historico; dado sensivel protegido |

### Historico/Professor - Historico Protegido

Rota:

```text
/app/agentes/historico-professor/rotinas/historico-protegido
```

| ID | Fluxo | Maior modo permitido | Ajustes visiveis quando necessario | Fixo e nao configuravel |
|---|---|---|---|---|
| G3 | Restricao/Cuidado | Autonomo com aprovacao | aprovador; dono do caso; tarefa humana | visibilidade vem de permissao; dado sensivel; permissao; auditoria |
| G5 | Contexto Para Agente | Autonomo com aprovacao | aprovador; escopo; prazo | dados permitidos vem de permissao; agente so recebe contexto permitido; auditoria |
| G6 | Documentos/Anamnese | Autonomo com aprovacao | aprovador; responsavel; checklist | documentos exigidos vem do produto/setup; documento/anamnese protegidos; permissao |
| G7 | Correcao Historico | Autonomo com aprovacao | aprovador; motivo; prazo; fallback | correcao auditavel; evento original preservado |
| G10 | Compartilhar Contexto | Autonomo com aprovacao | aprovador; destinatario; template/tom | dados permitidos vem de permissao; compartilhar contexto exige permissao; auditoria |
| G11 | Permissao Historico | Autonomo com aprovacao | aprovador; prazo | papel e escopo real ficam em Configuracoes/Permissoes; auditoria |

## Regras De Bloqueio Por Plano

### 0 Agentes

- CRM continua manual.
- Paginas de agentes podem mostrar preview.
- Rotinas podem ser vistas como exemplo ou upgrade.
- Fluxos nao publicam IA.
- Simulacao mostra caminho manual e preview sem execucao real de agente.

### 1 Agente

- So o agente contratado permite ajustar, simular e publicar rotinas com IA.
- Demais agentes aparecem bloqueados por plano.
- Caminho manual continua existindo em todo CRM.

### 3 Agentes

- Interface prioriza rotinas dos agentes contratados.
- Publicacao deve acontecer por rotina, nao por 96 fluxos soltos.
- Fluxos fora do plano aparecem como upgrade/preview.

### 7 Agentes

- Todos os agentes ficam disponiveis.
- Paginas precisam de filtros por agente, rotina, status, bloqueio, excecao e cota.
- Ainda assim, configuracao acontece por rotina/fluxo, nao por painel tecnico.

## Checagens Antes De Publicar

Todo fluxo autonomo precisa passar:

- plano/entitlement;
- permissao do usuario;
- modo permitido pelo teto do fluxo;
- template definido quando houver mensagem;
- tom de voz definido quando houver mensagem;
- fila humana definida quando houver excecao;
- aprovador definido quando houver aprovacao;
- fallback definido;
- dados obrigatorios presentes;
- integracao/canal fixo funcionando quando houver envio;
- cota disponivel;
- simulacao valida;
- auditoria preparada.

## Estados

Rotina:

- Nao configurada;
- Rascunho;
- Pronta para simular;
- Simulada;
- Publicada;
- Pausada;
- Com bloqueio;
- Com incidente.

Fluxo:

- Nao configurado;
- Rascunho;
- Simulado;
- Ativo;
- Pausado;
- Bloqueado;
- Aguardando aprovacao;
- Com excecao;
- Com falha.

Execucao:

- Aguardando;
- Rodando;
- Concluida;
- Aguardando aprovacao;
- Chamou humano;
- Falhou;
- Pausada;
- Revertida.

## Resumo Final

Regra final do produto:

```text
Agente nao configura.
Rotina organiza.
Fluxo configura.
Modo muda o comportamento.
Template e tom ficam no fluxo.
Canal, integracao, permissao, dado e cota sao dependencias fixas.
Studio so ajusta o que muda a operacao real.
```
