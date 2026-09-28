# Setup Inicial - 51L Bloco 9 Revisao Aprovado

Status: aprovado v0.1.
Data: 2026-05-20.

Imagem aprovada:

`D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\51L_round-4.1J_onboarding_bloco-9-revisao-aprovado.png`

## Objetivo

Validar o Bloco 9 do Setup Inicial: `Revisao`.

Este bloco e a ultima conferencia antes da publicacao do setup inicial.

A tela responde:

`O que entra em operacao agora, o que precisa de atencao e o que fica para depois?`

## Decisao Principal

A tela de Revisao nao e formulario, dashboard analitico nem configuracao.

Ela deve ser organizada em faixas horizontais claras:

1. `Publicado agora`;
2. `Pendencias`;
3. `Depois do go-live`;
4. `Publicacao segura`.

Nao deve existir uma faixa separada de `Resumo do setup`, porque ela repete informacoes que ja aparecem nas demais secoes.

## Escopo Do Setup Inicial

O bloco `Revisao` pode:

- mostrar o que sera publicado agora;
- mostrar pendencias que bloqueiam ou permitem publicacao com aviso;
- mostrar o que fica para depois do go-live;
- permitir voltar para o bloco anterior;
- salvar rascunho;
- exigir confirmacao explicita antes de publicar;
- publicar o setup inicial quando nao houver bloqueio real.

Nao configurar aqui:

- studio;
- equipe;
- canais;
- planos;
- pagamento;
- alunos;
- turmas;
- agenda;
- agentes;
- fluxos;
- automacoes;
- Pagamentos Taliya;
- control planes;
- logs;
- auditoria avancada;
- cotas;
- simulacao de fluxos.

## Estrutura Aprovada Da Tela

A tela usa o shell global aprovado em `51A`, com:

- stepper lateral esquerdo;
- header do onboarding;
- rodape global de rascunho/pendencias;
- painel lateral do Agente de Configuracao no padrao `51B`.

No stepper, a sequencia oficial e:

1. `Studio` concluido;
2. `Equipe` concluido;
3. `Canais` concluido;
4. `Planos` concluido;
5. `Pagamento` concluido;
6. `Alunos` concluido;
7. `Turmas` concluido;
8. `Agenda` concluido;
9. `Revisao` em andamento.

## Linha 1 - Publicado Agora

Titulo:

`1. Publicado agora`

Subtexto:

`Estas areas entram em operacao quando o setup inicial for publicado.`

Cards aprovados:

1. `Studio`
   - `Nome e horarios gerais`;
   - status: `Pronto`.
2. `Equipe`
   - `Dono confirmado e convites preparados`;
   - status: `Pronto`.
3. `Canais`
   - `WhatsApp Business, e-mail e canais publicos`;
   - status: `Pronto`.
4. `Planos`
   - `Planos principais e reposicao simples`;
   - status: `Pronto`.
5. `Pagamento`
   - `Pix, dinheiro e cartao para baixa manual`;
   - status: `Pronto`.
6. `Alunos`
   - `57 alunos preparados`;
   - status: `Revisar`.
7. `Turmas`
   - `10 turmas recorrentes`;
   - status: `Pronto`.
8. `Agenda`
   - `Semana base gerada`;
   - status: `Revisar`.

Os cards podem ser clicaveis para voltar ao bloco correspondente.

## Status Concluido Versus Revisar

No stepper, `Concluido` significa que o bloco foi preenchido e salvo o bastante para chegar a revisao.

Nos cards da Revisao, `Revisar` significa que a area tem aviso ou pendencia relacionada.

Assim, uma area pode aparecer como `Concluido` no stepper e `Revisar` na revisao final.

## Linha 2 - Pendencias

Titulo:

`2. Pendencias`

Subtexto:

`Revise o que bloqueia publicacao e o que pode seguir com aviso.`

Grupos aprovados:

### Bloqueia Publicacao

Visual vermelho suave.

Item:

- `1 aluno sem nome ou contato`.

Acao:

- `Resolver`.

### Pode Publicar Com Aviso

Visual laranja suave.

Itens:

- `2 alunos sem plano`;
- `1 turma sem professor`;
- `WhatsApp ainda nao conectado oficialmente`.

Acao:

- `Revisar avisos`.

Nao misturar itens de `Depois do go-live` nesta faixa.

## Linha 3 - Depois Do Go-Live

Titulo:

`3. Depois do go-live`

Subtexto:

`Essas configuracoes avancadas ficam para depois, nas Configuracoes do CRM.`

Cards aprovados:

1. `Pagamentos Taliya`
   - `Pix automatico, cartao online e recorrencia automatica`.
2. `Fluxos de agentes`
   - `Modos manual, copiloto e autonomo`.
3. `Automacoes avancadas`
   - `Mensagens, aprovacoes e regras por fluxo`.
4. `Control planes`
   - `Cotas, logs, auditoria, incidentes e risco`.

Texto auxiliar aprovado:

`Esses itens nao bloqueiam a publicacao do setup inicial.`

Esses cards sao explicativos. Nao devem abrir configuracao profunda dentro do Setup Inicial.

## Linha 4 - Publicacao Segura

Titulo:

`4. Publicacao segura`

Texto:

`Nada sera publicado sem sua confirmacao.`

Checklist aprovado:

- `Dados principais revisados`;
- `Pendencias criticas verificadas`;
- `Convites da equipe serao enviados ao publicar`;
- `Ajustes avancados ficam para depois do go-live`.

Checkbox obrigatorio:

`Revisei as informacoes e entendo o que sera publicado agora.`

Acoes aprovadas:

- `Voltar para agenda`;
- `Salvar rascunho`;
- `Publicar setup inicial`.

## Regra De Bloqueio Do Botao Principal

Na imagem aprovada, existe uma pendencia em `Bloqueia publicacao` e o botao `Publicar setup inicial` parece ativo.

Na implementacao, seguir a regra de produto:

- se houver bloqueio real, o botao principal deve ficar desabilitado;
- o CTA principal alternativo deve ser `Resolver bloqueios`;
- se nao houver bloqueio real, o botao `Publicar setup inicial` pode ficar ativo;
- pendencias com aviso nao bloqueiam necessariamente a publicacao, mas devem ficar registradas.

## Painel Do Agente

Mensagem de impacto aprovada:

`Esta e a revisao final antes de publicar o setup inicial.`

Balao 1:

`Eu organizei a revisao em tres partes: publicado agora, pendencias e depois do go-live.`

Balao 2:

`Nada sera publicado sem sua confirmacao. Voce ainda pode voltar em qualquer bloco antes de publicar.`

Balao 3:

`Configuracoes avancadas ficam para depois, sem bloquear o inicio da operacao.`

Chips aprovados:

- `O que sera publicado?`;
- `O que bloqueia?`;
- `O que fica para depois?`;
- `O que acontece depois?`.

## Nao Fazer

Nao mostrar nesta tela:

- faixa de resumo do setup;
- card `Pronto para publicar` no topo;
- card `Operacao inicial` no topo;
- card `Depois do go-live` no topo;
- formularios;
- drawer;
- modal;
- builder de agente;
- configuracao de automacoes;
- configuracao de Pagamentos Taliya;
- configuracao de control planes;
- logs ou auditoria avancada como configuraveis;
- repeticao da mesma informacao em varias secoes.

## Criterios De Aceite

- A tela e uma revisao final, nao uma configuracao.
- A area central e organizada em faixas horizontais.
- `Publicado agora`, `Pendencias` e `Depois do go-live` aparecem separados.
- O usuario entende o que entra agora.
- O usuario entende o que bloqueia ou pode seguir com aviso.
- O usuario entende o que fica para pos-go-live.
- Nada e publicado sem confirmacao explicita.
- Bloqueios reais impedem a publicacao na implementacao.
