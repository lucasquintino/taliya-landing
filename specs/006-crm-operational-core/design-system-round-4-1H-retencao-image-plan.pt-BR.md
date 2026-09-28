# Rodada 4.1H - Retencao, Cancelamentos, Reativacoes E Reclamacoes Web

> Status: fechada para web v0.1. Imagens aprovadas em 13/05/2026: `41_round-4.1H_retencao_01_riscos-lista-drawer.png`, `42_round-4.1H_cancelamentos_01_fila-salvamento-drawer.png`, `43_round-4.1H_reativacoes_01_ex-alunos-retorno.png` e `44_round-4.1H_reclamacoes_01_fila-caso-sensivel-drawer.png`.

## Topbar Da Familia

A topbar interna desta familia deve ficar:

```text
Riscos | Cancelamentos | Reativacoes | Reclamacoes
```

Esta familia cobre permanencia do aluno, pedido de saida, retorno de ex-aluno/inativo e reclamacoes sensiveis.

## Imagens Planejadas

| Imagem | Nome | Rota | Status |
| --- | --- | --- | --- |
| 1 | `41_round-4.1H_retencao_01_riscos-lista-drawer.png` | `/app/retencao` ou `/app/retencao/riscos` | Aprovada com ajustes de especificacao. |
| 2 | `42_round-4.1H_cancelamentos_01_fila-salvamento-drawer.png` | `/app/cancelamentos` | Aprovada com ajustes de especificacao. |
| 3 | `43_round-4.1H_reativacoes_01_ex-alunos-retorno.png` | `/app/retencao/reativacoes` | Aprovada com ajustes de especificacao. |
| 4 | `44_round-4.1H_reclamacoes_01_fila-caso-sensivel-drawer.png` | `/app/reclamacoes` | Aprovada com ajustes de especificacao. |
| 5 | opcional | `/app/reclamacoes` estado severo | Nao gerar agora; cobrir por contrato textual ate aparecer necessidade real. |

## Imagem 1 Aprovada - Riscos De Retencao

Arquivo salvo:

```text
41_round-4.1H_retencao_01_riscos-lista-drawer.png
```

### Objetivo Da Pagina

Permitir que o gestor identifique alunos com risco de sair antes de haver pedido formal de cancelamento.

A tela nao e uma tela de cancelamento. Ela e uma fila preventiva de permanencia.

### Estrutura Aprovada

| Zona | Conteudo aprovado |
| --- | --- |
| App shell | Sidebar, topbar global, botoes circulares, fundo claro e visual Taliya aprovados. |
| Topbar interna | `Riscos`, `Cancelamentos`, `Reativacoes`, `Reclamacoes`, com `Riscos` ativo. |
| Titulo | `Retencao`. |
| Subtitulo | `Alunos em risco e proximas acoes`. |
| Filtros superiores | Hoje, Esta semana, Este mes, Unidade, Risco, Turma, Plano, Responsavel. |
| Coluna esquerda | Segmentos de risco. |
| Centro | Lista/tabela de alunos em risco. |
| Direita | Drawer do aluno selecionado. |

### Segmentos Aprovados

- Todos.
- Alto risco.
- Queda de frequencia.
- Sem aula recente.
- Primeira semana.
- Feedback negativo.
- Financeiro afetando retencao.
- Retorno pendente.

### Lista Central

Cada linha deve mostrar:

- avatar;
- nome do aluno;
- status ou plano, conforme ajuste abaixo;
- nivel de risco;
- motivo principal do risco;
- ultima aula ou ultima interacao;
- proxima acao sugerida;
- responsavel;
- seta/indicador de abertura do drawer.

Linha selecionada aprovada:

```text
Ana Paula Martins
Risco alto
Motivo: 14 dias sem aula
Proxima acao: enviar mensagem humana hoje
Responsavel: Mariana
```

### Drawer Aprovado

O drawer direito deve mostrar:

- badge de risco;
- nome do aluno;
- resumo: plano, turma, ultima aula, presenca recente, financeiro e responsavel;
- motivos do risco;
- sugestao do copiloto;
- proximas acoes;
- historico curto.

Acoes aprovadas:

- Enviar mensagem.
- Criar tarefa.
- Abrir aluno.
- Registrar acompanhamento.

### Ajustes Necessarios Antes De Implementar

1. Corrigir URL visual para evitar duplicidade. Usar:

```text
https://app.taliya.com/app/retencao
```

2. Trocar a coluna `Status` se ela ficar repetitiva. Preferencia:

```text
Plano
```

ou:

```text
Frequencia recente
```

Motivo: quase todos os alunos aparecem como ativos, entao `Status` pouco ajuda o gestor.

3. Variar melhor a origem do risco nas linhas:

- Agenda.
- WhatsApp.
- Financeiro.
- Professor.
- Frequencia.
- Feedback.

4. Manter `Sugestao do copiloto` como sugestao, nao decisao automatica.

Regra: o copiloto pode explicar e redigir, mas nao deve parecer que executa sozinho uma decisao sensivel de retencao.

5. Trocar o botao `Marcar acompanhado` por:

```text
Registrar acompanhamento
```

Motivo: deixa claro que a acao cria registro/auditoria, nao apenas remove o item da fila.

6. Cada linha pode abrir drawer pelo indicador de seta. Nao precisa ter varios botoes por linha.

## Regras Funcionais Da Pagina Riscos

- Risco deve ser explicavel, nao apenas um score.
- O usuario deve entender por que o aluno esta em risco.
- A proxima acao deve ser humana, acionavel e ligada a uma origem.
- A tela deve funcionar com 0 agentes.
- Com agente de Retencao ativo, IA pode resumir, sugerir contato e redigir mensagem.
- Em modo copiloto, o usuario revisa antes de acao externa.
- Em modo autonomo, apenas contato seguro permitido por politica, consentimento, cota e auditoria.
- Cancelamento ativo deve sair desta pagina e entrar em `/app/cancelamentos`.
- Reclamacao sensivel deve sair desta pagina e entrar em `/app/reclamacoes`.

## O Que Nao Pertence A Esta Imagem

- Funil comercial.
- Kanban.
- Dashboard gerencial cheio de graficos.
- Pagina de cancelamento.
- Pagina de reclamacao.
- Financeiro detalhado.
- Historico completo do aluno.
- Automacao parecendo decisao irreversivel.

## Imagem 2 Aprovada - Cancelamentos

Arquivo salvo:

```text
42_round-4.1H_cancelamentos_01_fila-salvamento-drawer.png
```

### Objetivo Da Pagina

Permitir que o gestor trate pedidos reais de saida, pausa ou duvida de cancelamento sem misturar isso com risco preventivo.

A pagina nao e uma pagina de vendas, nem uma fila generica de relacionamento. Ela e a mesa de decisao para proteger receita, entender motivo, tentar salvamento quando fizer sentido e concluir a saida com auditoria quando a decisao for cancelar.

### Estrutura Aprovada

| Zona | Conteudo aprovado |
| --- | --- |
| App shell | Sidebar, topbar global, botoes circulares e linguagem visual Taliya herdados do shell aprovado. |
| Topbar interna | `Riscos`, `Cancelamentos`, `Reativacoes`, `Reclamacoes`, com `Cancelamentos` ativo. |
| Titulo | `Cancelamentos`. |
| Subtitulo | `Pedidos de saida, pausas e planos de salvamento`. |
| Filtros superiores | Hoje, Esta semana, Este mes, Unidade, Status, Motivo, Plano, Responsavel e filtro avancado. |
| Coluna esquerda | Filas de pedido de saida e salvamento. |
| Centro | Lista/tabela de pedidos de cancelamento, pausa e duvida de saida. |
| Direita | Drawer do pedido selecionado. |

### Filas Aprovadas

- Todos.
- Novos pedidos.
- Em salvamento.
- Aguardando aluno.
- Pausa solicitada.
- Cancelamento confirmado.
- Recuperados.
- Nao contatar.

### Lista Central

Cada linha deve mostrar:

- avatar;
- nome do aluno;
- tipo do pedido: cancelamento, pausa ou duvida de saida;
- status operacional;
- motivo principal;
- impacto estimado;
- prazo;
- responsavel;
- seta/indicador de abertura do drawer.

Linha selecionada aprovada:

```text
Ana Paula Martins
Tipo: Cancelamento
Status: Em salvamento
Motivo: dificuldade de agenda
Impacto: R$ 420/mes + turma com vaga aberta
Prazo: hoje 16:00
Responsavel: Mariana
```

### Drawer Aprovado

O drawer direito deve mostrar:

- badges de tipo e status;
- nome do aluno;
- resumo do pedido;
- motivo declarado;
- impacto;
- plano de salvamento;
- aviso de automacao pausada;
- sugestao do copiloto;
- historico curto;
- acoes finais.

Acoes aprovadas:

- Enviar mensagem.
- Criar tarefa.
- Registrar pausa.
- Confirmar cancelamento.
- Abrir aluno.
- Abrir conversa.

### Ajustes Necessarios Antes De Implementar

1. Corrigir URL visual para evitar duplicidade. Usar:

```text
https://app.taliya.com/cancelamentos
```

2. `Confirmar cancelamento` nao deve executar direto.

Regra: deve abrir confirmacao forte com resumo de impacto, data efetiva, efeito financeiro, automacoes afetadas e campo opcional/obrigatorio de motivo conforme politica do studio.

3. `Registrar pausa` deve significar:

```text
Converter pedido em pausa
```

ou:

```text
Registrar pausa temporaria
```

Motivo: precisa ficar claro que a acao muda o estado operacional do aluno, e nao apenas cria uma nota.

4. Variar responsaveis nas linhas quando houver mais de uma pessoa operando a fila.

Na imagem quase todos aparecem com `Mariana`; isso e aceitavel como mock, mas o produto deve suportar recepcao, financeiro, coordenacao e gestor.

5. Trocar status `Retido` por:

```text
Recuperado
```

Motivo: a fila lateral usa `Recuperados`, e o termo fica mais claro para o gestor.

6. O drawer deve exibir efeito financeiro quando houver cancelamento ou pausa:

- proxima cobranca;
- valor mensal afetado;
- aulas futuras afetadas;
- reposicoes em aberto;
- turma/vaga liberada.

7. Manter o copiloto como apoio, nao como decisor.

Regra: em cancelamento ativo, o agente nao confirma saida sozinho. Ele pode resumir, sugerir resposta, preparar plano de salvamento e criar tarefa/aprovacao, mas a decisao final e humana.

### Regras Funcionais Da Pagina Cancelamentos

- Um pedido de cancelamento ativo deve sair de `Riscos` e entrar em `/app/cancelamentos`.
- Pausa solicitada pertence a esta pagina quando e alternativa a cancelamento.
- Reativacao nao pertence a esta pagina; alunos ja encerrados ou inativos elegiveis entram em `/app/retencao/reativacoes`.
- Reclamacao sensivel nao pertence a esta pagina; deve ir para `/app/reclamacoes`.
- Cancelamento deve pausar automacoes de cobranca e retencao ate decisao humana.
- Com 0 agentes, o gestor consegue registrar motivo, criar tarefa, enviar mensagem manualmente e concluir.
- Com 1, 3 ou 7 agentes, IA pode sugerir plano, redigir mensagem, detectar impacto e preparar proximas acoes conforme permissao.
- Em modo manual, o usuario conduz tudo.
- Em modo copiloto, o agente sugere e aguarda revisao.
- Em modo autonomo, nao confirmar cancelamento ativo; apenas executar acoes seguras permitidas por politica, consentimento, cota e auditoria.

### O Que Nao Pertence A Esta Imagem

- Funil de vendas.
- Reativacao de ex-aluno.
- Risco preventivo sem pedido de saida.
- Reclamacao sensivel.
- Financeiro detalhado de cobrancas.
- Dashboard gerencial com graficos.
- Decisao irreversivel executada por IA sem confirmacao humana.

## Imagem 3 Aprovada - Reativacoes

Arquivo salvo:

```text
43_round-4.1H_reativacoes_01_ex-alunos-retorno.png
```

### Objetivo Da Pagina

Permitir que o gestor encontre ex-alunos, alunos pausados ou inativos que podem voltar, sem tratar isso como lead novo nem como cancelamento ativo.

A pagina e uma mesa operacional de retorno: mostra quem pode ser contatado, por que existe uma oportunidade, qual vaga/plano faz sentido e quais restricoes precisam ser respeitadas antes de qualquer mensagem.

### Estrutura Aprovada

| Zona | Conteudo aprovado |
| --- | --- |
| App shell | Sidebar, topbar global, botoes circulares e visual Taliya herdados do shell aprovado. |
| Topbar interna | `Riscos`, `Cancelamentos`, `Reativacoes`, `Reclamacoes`, com `Reativacoes` ativo. |
| Titulo | `Reativacoes`. |
| Subtitulo | `Ex-alunos e alunos pausados com chance de retorno`. |
| Filtros superiores | Hoje, Esta semana, Este mes, Unidade, Status, Motivo de saida, Plano anterior, Responsavel e filtro avancado. |
| Coluna esquerda | Filas de elegibilidade e retorno. |
| Centro | Lista/tabela de ex-alunos, pausados e inativos elegiveis. |
| Direita | Drawer do aluno selecionado. |

### Filas Aprovadas

- Todos.
- Elegiveis para retorno.
- Pausados vencendo.
- Sem resposta.
- Interesse detectado.
- Nao contatar.
- Reativados.

### Lista Central

Cada linha deve mostrar:

- avatar;
- nome do aluno;
- status de retorno;
- motivo de saida;
- ultima atividade;
- oportunidade de retorno;
- proxima acao;
- responsavel;
- seta/indicador de abertura do drawer.

Linha selecionada aprovada:

```text
Ana Paula Martins
Status: Elegivel
Motivo de saida: dificuldade de agenda
Ultima atividade: cancelou em 29/04
Oportunidade: vaga aberta no Reformer Iniciante
Proxima acao: enviar convite humano hoje
Responsavel: Mariana
```

### Drawer Aprovado

O drawer direito deve mostrar:

- badges `Reativacao` e status do aluno;
- nome do aluno;
- resumo do aluno antes da saida;
- oportunidade de retorno;
- restricoes;
- sugestao do copiloto;
- historico curto;
- acoes finais.

Acoes aprovadas:

- Enviar mensagem.
- Criar tarefa.
- Reservar vaga.
- Marcar como nao contatar.
- Abrir aluno.
- Abrir conversa.

### Ajustes Necessarios Antes De Implementar

1. Corrigir URL visual para evitar duplicidade. Usar:

```text
https://app.taliya.com/retencao/reativacoes
```

2. `Reservar vaga` deve ser acao controlada.

Regra: antes de reservar, o sistema deve validar disponibilidade, politica do studio, conflitos de agenda, turma, limite de vagas e permissao do usuario. Se houver incerteza, abrir confirmacao ou criar tarefa.

3. Para alunos marcados como `Nao contatar`, remover ou desabilitar acoes de mensagem.

Regra: a proxima acao deve ser neutra, como:

```text
Respeitar preferencia
```

4. Para status `Reativado`, a proxima acao deve ser acompanhamento, nao reativacao.

Exemplos:

```text
Acompanhar retorno
Confirmar adaptacao da aula
```

Esses itens podem sair da fila principal depois de resolvidos e aparecer apenas em historico/relatorios.

5. Variar responsaveis nas linhas quando houver mais de uma pessoa operando retorno.

O produto deve suportar recepcao, coordenacao, financeiro e gestor, mesmo que a imagem use `Mariana` em varias linhas.

6. A tela deve diferenciar reativacao de venda.

Reativacao parte de aluno conhecido, historico, motivo de saida, restricao e oportunidade real. Lead novo pertence a Vendas.

### Regras Funcionais Da Pagina Reativacoes

- Reativacao entra depois de cancelamento concluido, pausa vencendo, interesse detectado ou inatividade elegivel.
- Aluno com cancelamento ativo ainda pertence a `/app/cancelamentos`.
- Aluno apenas em risco, sem saida, ainda pertence a `/app/retencao`.
- Aluno marcado como `Nao contatar` nao pode receber mensagem automatica.
- Com 0 agentes, o gestor consegue filtrar, abrir aluno, criar tarefa, enviar mensagem manual e registrar resultado.
- Com agente de Retencao ativo, IA pode sugerir mensagem, explicar oportunidade, detectar vaga compativel e preparar proxima acao.
- Em modo copiloto, o usuario revisa antes de contato externo.
- Em modo autonomo, contato so pode ocorrer se politica, consentimento, cota, horario e restricoes permitirem.
- Reativar aluno deve atualizar status, plano, turma, agenda, financeiro e historico.
- Se houver pendencia financeira, a reativacao pode gerar tarefa ou aprovacao antes de confirmar retorno.

### O Que Nao Pertence A Esta Imagem

- Funil de vendas de lead novo.
- Pedido de cancelamento ativo.
- Risco preventivo sem saida.
- Reclamacao sensivel.
- Campanha massiva de marketing.
- Automacao ignorando `Nao contatar`.
- Reserva de vaga irreversivel sem validacao.

## Imagem 4 Aprovada - Reclamacoes

Arquivo salvo:

```text
44_round-4.1H_reclamacoes_01_fila-caso-sensivel-drawer.png
```

### Objetivo Da Pagina

Permitir que o gestor trate reclamacoes e casos sensiveis de alunos com dono, prazo, contexto, resposta controlada e auditoria.

A pagina nao e suporte generico, nem uma fila comum de tarefas. Ela existe para recuperar confianca, evitar escalada indevida e impedir que automacoes respondam sozinhas quando o caso exige cuidado humano.

### Estrutura Aprovada

| Zona | Conteudo aprovado |
| --- | --- |
| App shell | Sidebar, topbar global, botoes circulares e visual Taliya herdados do shell aprovado. |
| Topbar interna | `Riscos`, `Cancelamentos`, `Reativacoes`, `Reclamacoes`, com `Reclamacoes` ativo. |
| Titulo | `Reclamacoes`. |
| Subtitulo | `Casos sensiveis, respostas e recuperacao de confianca`. |
| Filtros superiores | Hoje, Esta semana, Este mes, Unidade, Severidade, Status, Origem, Responsavel e filtro avancado. |
| Coluna esquerda | Filas por severidade/status operacional. |
| Centro | Lista/tabela de reclamacoes e casos sensiveis. |
| Direita | Drawer do caso selecionado. |

### Filas Aprovadas

- Todos.
- Alta severidade.
- Aguardando resposta.
- Aguardando responsavel.
- Reabertas.
- Resolvidas.
- Automacao pausada.

### Lista Central

Cada linha deve mostrar:

- avatar;
- nome do aluno;
- severidade;
- status;
- origem;
- motivo principal;
- prazo;
- responsavel;
- ultima atividade;
- seta/indicador de abertura do drawer.

Linha selecionada aprovada:

```text
Ana Paula Martins
Severidade: Alta
Status: Aguardando resposta
Origem: WhatsApp
Motivo principal: reclamacao sobre reposicao nao resolvida
Prazo: hoje 14:00
Responsavel: Mariana
Ultima atividade: mensagem recebida 09:20
```

### Drawer Aprovado

O drawer direito deve mostrar:

- badges `Reclamacao` e severidade;
- nome do aluno;
- resumo do caso;
- motivo declarado;
- impacto;
- automacao pausada;
- plano de resolucao;
- sugestao do copiloto;
- historico curto;
- acoes finais.

Acoes aprovadas:

- Responder.
- Criar tarefa.
- Escalar.
- Marcar resolvida.
- Abrir aluno.
- Abrir conversa.

### Ajustes Necessarios Antes De Implementar

1. Corrigir URL visual para evitar duplicidade. Usar:

```text
https://app.taliya.com/reclamacoes
```

2. `Responder` nao deve enviar direto.

Regra: deve abrir composer/revisao com texto sugerido, contexto do caso, canal, destinatario e confirmacao humana antes do envio.

3. `Marcar resolvida` nao deve concluir direto.

Regra: deve abrir confirmacao pedindo resumo da solucao, se houve resposta ao aluno, se precisa acompanhamento e se automacoes podem ser retomadas.

4. Casos de alta severidade podem exigir permissao maior.

Exemplos:

- escalonamento obrigatorio para gestor;
- revisao antes de resposta externa;
- bloqueio de acao autonoma;
- registro de auditoria completo.

5. Variar responsaveis nas linhas quando houver mais de uma pessoa operando a fila.

A imagem usa bastante `Mariana`; o produto deve suportar recepcao, coordenacao, professor responsavel, financeiro e gestor.

6. Automacao pausada deve ser regra visivel, nao decoracao.

Enquanto o caso estiver sensivel, mensagens automaticas e acoes autonomas do agente ficam pausadas ou exigem revisao humana.

### Regras Funcionais Da Pagina Reclamacoes

- Reclamacao entra quando ha insatisfacao explicita, risco reputacional, conflito com professor/aula, falha de reposicao, cobranca contestada ou resposta sensivel.
- Caso sensivel nao deve ficar apenas em Inbox, Hoje ou Tarefas; essas telas podem apontar para `/app/reclamacoes`.
- Com 0 agentes, o gestor consegue classificar, responder manualmente, criar tarefa, escalar e resolver.
- Com agente ativo, IA pode resumir, organizar evidencias, sugerir resposta e preparar proxima acao.
- Em modo copiloto, o usuario revisa antes de qualquer resposta externa.
- Em modo autonomo, autonomia deve ficar bloqueada por padrao para casos de alta severidade.
- Resolver caso deve registrar solucao, responsavel, horario, mensagem enviada e se havera acompanhamento.
- Reabrir caso deve preservar historico e motivo da reabertura.
- Automacoes pausadas so devem voltar quando o caso for resolvido ou liberado por humano.

### O Que Nao Pertence A Esta Imagem

- Dashboard de satisfacao.
- Suporte tecnico generico.
- Funil de vendas.
- Pedido simples de reposicao sem reclamacao.
- Cancelamento ativo sem reclamacao.
- Reativacao de ex-aluno.
- Resposta autonoma sem revisao humana.

## Proxima Etapa

Proxima etapa recomendada:

```text
Auditoria final da familia 4.1H
```

Objetivo: revisar se `Riscos`, `Cancelamentos`, `Reativacoes` e `Reclamacoes` cobrem todos os fluxos de permanencia, saida, retorno e caso sensivel; decidir se o estado severo opcional de reclamacao precisa de imagem propria.
