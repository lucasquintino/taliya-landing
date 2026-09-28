# Design System Web - Rodada 4.1D - Pagina Inbox

> Status: aprovada v0.1. Objetivo: definir `/app/inbox` como workspace de atendimento com conversa aberta, contexto do aluno/responsavel e controle simples de agente.

## Decisao Central

**Inbox** responde:

> Quem esta falando com o studio, qual contexto eu preciso para responder bem, e quem controla essa conversa agora?

Inbox nao e:

- Hoje;
- Operacao;
- Tarefas;
- CRM completo do aluno;
- tela de campanhas em massa;
- dashboard de atendimento;
- console de agentes.

Inbox e a superficie de **atendimento ativo**. Conversas podem gerar tarefas, aprovacao, problema de dados ou item em Operacao, mas a conversa continua tendo origem canonica no Inbox.

## Simplificacao De Identidade E Contatos

Decisao de produto da Rodada 4.1D:

- nao criar pagina principal de Contatos nesta rodada;
- nao criar pagina propria de Responsaveis;
- nao criar pagina propria de Grupos/familias;
- nao modelar relacionamento entre alunos como superficie visual;
- manter apenas o necessario para operar: aluno, responsavel do aluno, interessado e canal de contato.

Consequencia:

- dados de aluno e responsaveis ficam em Alunos;
- dados de interessados ficam em Vendas/Interessados;
- Inbox mostra apenas contexto minimo para responder;
- duplicidade, telefone compartilhado ou identidade incerta viram problema de dados ou acao contextual, nao uma pagina inteira de contatos.

Regra:

Se e aluno matriculado, resolver em Alunos. Se ainda nao matriculou, resolver em Interessados/Vendas. Se esta falando agora, resolver no Inbox. Se e erro de dado, tratar como problema de dados.

## Layout Da Rota

Rota principal:

`/app/inbox`

Rota herdada:

`/app/conversas/[id]`

Decisao:

- `/app/inbox` tem 1 imagem propria aprovada;
- `/app/conversas/[id]` herda a mesma imagem, com conversa selecionada por URL;
- `/app/envios` e `/app/envios/[sendId]` ficam como contrato textual nesta rodada, herdando lista densa + detalhe lateral.

## Cobertura Da Rota De Detalhe

Rota:

`/app/conversas/[id]`

Decisao:

Nao precisa imagem propria nesta rodada.

A rota de detalhe da conversa herda:

- imagem `24_round-4.1D_inbox_01_conversa-aberta.png`;
- layout de lista + conversa + contexto lateral;
- componentes de comunicacao/agentes `3B.4`;
- painel de contexto de contato/aluno `3C.1`;
- estados e variacoes documentados nesta pagina.

Quando acessada por URL direta, a rota deve abrir a conversa solicitada como item selecionado:

- desktop largo: lista lateral continua visivel, conversa selecionada no centro e painel de contexto aberto;
- desktop menor: lista pode recolher para preservar leitura da conversa;
- mobile: detalhe da conversa abre em tela cheia, com contexto em aba/bottom sheet.

Estados especiais:

| Estado | Comportamento |
| --- | --- |
| Conversa inexistente | Mostrar erro/estado vazio com retorno ao Inbox. |
| Sem permissao | Mascarar conversa ou bloquear acesso, sem expor mensagens sensiveis. |
| Conversa arquivada | Abrir em modo consulta, com acao para reabrir se permitido. |
| Conversa encerrada | Composer reduzido ou bloqueado conforme politica; permitir reabrir se autorizado. |
| Canal desconectado | Mostrar banner de canal indisponivel e caminho manual. |
| Cota 100% | Bloquear automacao paga e manter resposta manual. |

So deve ganhar imagem propria no futuro se deixar de ser conversa dentro do Inbox e virar uma superficie diferente, como auditoria longa, historico completo de mensagens, replay de execucao de agente ou investigacao tecnica.

## Cobertura Da Rota De Envios

Rotas:

- `/app/envios`
- `/app/envios/[sendId]`

Decisao:

Nao precisam imagem propria nesta rodada.

Estas rotas existem para explicar **tentativas de envio e entregabilidade operacional**, nao para substituir Inbox.

Pergunta que respondem:

> O que o Taliya tentou enviar, o que entregou, o que falhou, por que falhou e qual acao segura pode ser tomada?

Padrao visual herdado:

- lista densa de envios/tentativas, similar ao padrao de Tarefas;
- detalhe lateral do envio selecionado, similar aos paineis de detalhe ja aprovados;
- topbar de Atendimento com `Envios` ativo;
- filtros por canal, status, origem, data, agente/responsavel e motivo de falha.

Conteudo minimo:

| Bloco | Conteudo |
| --- | --- |
| Lista | destinatario, canal, origem, status, horario, tentativa, motivo curto e proxima acao. |
| Detalhe | mensagem original, conversa/origem, provider/status tecnico resumido, cota, consentimento, janela de envio, idempotencia e auditoria curta. |
| Acoes | tentar de novo se seguro, enviar manualmente, cancelar, criar tarefa, abrir conversa, abrir origem, abrir canal/provedor quando permitido. |

Estados:

- enviado;
- entregue;
- lido;
- falhou;
- aguardando provedor;
- janela fechada;
- opt-out;
- cota esgotada;
- canal desconectado;
- template invalido;
- telefone invalido;
- duplicidade evitada.

Relação com outras superficies:

| Superficie | Relacao |
| --- | --- |
| Inbox | Abre a conversa relacionada ao envio. |
| Tarefas | Cria acompanhamento humano quando reenvio nao e seguro ou precisa dono/prazo. |
| Operacao | Recebe apenas falhas que bloqueiam fluxo ou exigem acompanhamento por etapa. |
| Privacidade | Opt-out e consentimento sao governanca de privacidade, nao edicao livre em Envios. |
| Agentes/Execucoes | Falhas de agente, trace e reprocessamento profundo pertencem a Execucoes/Incidentes. |

Quando ganhar imagem propria:

- se falhas de WhatsApp/envio virarem fluxo operacional frequente;
- se for necessario mostrar reprocessamento seguro e auditoria visual;
- se a pagina passar a ter volume alto, triagem propria ou muitos status tecnicos;
- se `/app/envios/[sendId]` virar investigacao detalhada, nao apenas detalhe lateral.

Mobile:

Fica como acao parcial: lista de falhas e detalhe em tela cheia/bottom sheet, com foco em reenvio seguro ou criacao de tarefa.

## Estado Padrao

Ao carregar `/app/inbox`:

- a lista de conversas fica visivel;
- nenhuma conversa precisa estar selecionada por padrao em telas estreitas;
- em desktop largo, pode abrir a conversa mais prioritaria ou a ultima selecionada;
- o painel direito de contexto deve aparecer apenas quando houver conversa selecionada;
- se a imagem mostrar conversa aberta e painel direito preenchido, ela representa estado selecionado para documentacao visual.

## Blocos Principais

| Zona | Conteudo |
| --- | --- |
| App shell | Mesmo shell aprovado da Taliya, com menu lateral e topo global. |
| Topo da pagina | Titulo `Inbox`, subtitulo do studio, busca, filtros por canal/status/responsavel/nao lidas, acao `Nova conversa`. |
| Esquerda interna | Filas/tabs: Todas, WhatsApp, Email, Aguardando humano, Agente pausado, Falhas, Arquivadas. |
| Lista de conversas | Cards/linhas com contato, aluno/interessado vinculado, canal, ultima mensagem, SLA, dono/fila, status e risco. |
| Centro | Conversa selecionada com mensagens, nota interna, sugestao do copiloto e composer. |
| Direita | Perfil vinculado, consentimento, identidade, resumo, tarefas relacionadas, historico curto, confianca/status do agente e acoes. |

## Regra Do Painel Direito

O painel direito e contextual ao item/conversa selecionado.

- por padrao, em desktop largo ele pode abrir para a conversa prioritaria ou ultima conversa selecionada;
- em telas estreitas ele deve ficar fechado ate selecao explicita;
- a imagem 24 mostra um estado selecionado, nao o estado inicial obrigatorio;
- o painel direito muda conforme identidade, canal, consentimento, status do agente, falha, opt-out ou tipo de assunto;
- o painel nao substitui Perfil do Aluno, Financeiro, Privacidade, Envios ou Operacao.

Modos principais do painel direito:

| Item clicado | Painel direito deve mostrar |
| --- | --- |
| Conversa identificada | Aluno/interessado vinculado, consentimento, historico curto, tarefas relacionadas, status do agente e acoes rapidas. |
| Identidade incerta | Possiveis vinculos, dados minimos seguros, acao de confirmar identidade e restricao de resposta sensivel. |
| Opt-out/sem consentimento | Preferencia restritiva, canal bloqueado/limitado, auditoria e acoes permitidas de registrar ou abrir privacidade. |
| Falha de envio | Motivo tecnico/politica, ultima tentativa, canal alternativo, reenvio seguro e link para Envios. |
| Agente pausado/bloqueado | Motivo da pausa/bloqueio, politica/cota/risco, acao manual e opcao de assumir ou retomar se permitido. |
| Assunto financeiro/sensivel | Resumo permitido, mascaramento quando necessario, link para origem canonica e reducao de autonomia. |

## Ciclo Da Conversa

1. Mensagem chega por WhatsApp, email ou canal interno.
2. CRM identifica contato/aluno quando possivel.
3. Conversa entra em uma fila com status: nova, aguardando humano, agente respondendo, agente pausado, falha de envio ou encerrada.
4. Usuario responde manualmente ou usa sugestao do copiloto.
5. Se precisar acompanhar depois, cria tarefa.
6. Se tiver problema de dado, abre problema de dados.
7. Se cruzar areas ou travar operacao, pode aparecer em Operacao.
8. Se a resposta/acao for sensivel, vira aprovacao.
9. Conversa encerra, reabre ou fica aguardando retorno.

## Modos De Agente

| Plano/modo | Comportamento |
| --- | --- |
| 0 agentes | Inbox funciona totalmente manual: responder, vincular, criar tarefa, registrar opt-out e abrir perfil. |
| 1 agente | Copiloto aparece somente se o agente ativo cobrir Atendimento. |
| 3 agentes | Atendimento normalmente esta ativo; copiloto sugere resumo, resposta e classificacao. |
| 7 agentes | Todos os dominios podem enriquecer contexto, respeitando permissao, cota, politica e risco. |
| Manual | Humano responde, assume, pausa agente, vincula contato e registra preferencia. |
| Copiloto | Sugere resposta, resume conversa, classifica intent e recomenda proxima acao. |
| Autonomo | So responde se identidade, consentimento, cota, politica, canal e risco estiverem OK. |

## Variacoes Por Conversa E Autonomia

A pagina pode ter muitas variacoes de estado sem exigir uma imagem propria para cada uma.

A imagem 24 cobre o padrao base: conversa aberta, humano no controle, copiloto sugerindo e autonomia bloqueada/condicionada.

As variacoes abaixo devem ser implementadas com os mesmos blocos da imagem 24, mudando badges, banners, acoes e permissoes:

| Variacao | O que muda na tela | Acoes principais | Precisa nova imagem? |
| --- | --- | --- | --- |
| Manual puro | Nao ha bloco de copiloto; composer e acoes manuais ficam em destaque. | responder, criar tarefa, abrir perfil, registrar opt-out. | Nao. |
| Copiloto sugeriu | Bloco de sugestao aparece acima do composer; resposta ainda editavel. | usar sugestao, editar, enviar, descartar. | Coberto pela imagem 24. |
| Autonomo ativo | Mostrar agente respondendo ou resposta preparada/enviada com status e auditoria curta. | pausar agente, assumir, revisar historico, abrir execucao. | Nao por enquanto; contrato textual. |
| Autonomo bloqueado | Badge/banner explica bloqueio por risco, cota, consentimento, identidade ou politica. | assumir, responder manualmente, criar tarefa, pedir aprovacao. | Coberto pela imagem 24. |
| Aguardando humano | Conversa entra em fila com SLA/tempo de espera e dono/fila. | assumir, responder, delegar, criar tarefa. | Coberto pela imagem 24. |
| Agente pausado | Banner no centro e status no painel direito explicam motivo da pausa. | retomar se permitido, assumir, responder manualmente. | Coberto pela imagem 24. |
| Sem consentimento/opt-out | Composer bloqueado ou limitado; painel direito destaca preferencia restritiva. | registrar/confirmar opt-out, criar tarefa, abrir privacidade. | Nao, salvo rodada de privacidade. |
| Identidade incerta | Painel direito pede vinculo/confirmacao antes de expor dado ou responder assunto sensivel. | vincular a aluno ou interessado, validar responsavel do aluno, responder sem dado sensivel. | Nao; vira acao contextual ou problema de dados. |
| Telefone compartilhado | Mais de um aluno/responsavel possivel; contexto fica parcial ate confirmar quem fala. | confirmar pessoa, vincular ao aluno/interessado correto, abrir problema de dados. | Nao; nao cria pagina de contatos. |
| Falha de envio | Mensagem/linha de tentativa mostra erro, motivo e proxima acao segura. | tentar de novo se seguro, enviar manual, criar tarefa, abrir envios. | Nao nesta rodada; `/app/envios` fica como contrato textual. |
| Conversa financeira | Painel mostra resumo financeiro permitido, sem expor financeiro completo. | abrir financeiro, criar tarefa, pedir aprovacao, responder. | Nao nesta rota. |
| Conversa sensivel | Historico sensivel fica mascarado; copiloto/autonomia reduzidos. | pedir permissao, criar tarefa, escalar, responder com cuidado. | Nao nesta imagem; pode aparecer em Historico/Privacidade. |

Regra:

- variacao muda o estado operacional da conversa, nao a arquitetura da pagina;
- nao criar um layout novo para cada modo de autonomia;
- usar badges, banners, disabled states, tooltip/explicacao curta e acoes contextuais;
- se a variacao exigir superficie nova, ela deve ir para a origem canonica: Envios, Alunos, Interessados/Vendas, Privacidade, Financeiro, Historico, Operacao ou Agentes/Execucoes.

## Estados Que A Imagem Deve Mostrar

A imagem unica deve representar o estado mais explicativo:

- conversa aberta;
- status `Aguardando humano` ou `Agente pausado`;
- sugestao do copiloto pronta, mas revisavel;
- contato/aluno vinculado;
- consentimento OK ou alerta leve de identidade;
- uma conversa com falha/opt-out visivel na lista, sem dominar a tela;
- caminho manual claro: responder, assumir, criar tarefa, abrir perfil.

## O Que Nao Deve Aparecer

- dashboard com graficos;
- campanhas em massa;
- pagina de marketing;
- kanban;
- lista de tarefas como superficie principal;
- historico sensivel completo;
- financeiro completo;
- professor acessando inbox geral;
- IA respondendo como unica opcao;
- drawer aberto por padrao;
- excesso de cards ou paineis duplicados.

## Imagem Necessaria

### 24. Inbox - Conversa Aberta

Status:

**Aprovada v0.1.** Imagem salva no pacote local como `24_round-4.1D_inbox_01_conversa-aberta.png.png`.

Arquivo esperado:

`24_round-4.1D_inbox_01_conversa-aberta.png`

Origem local conhecida:

`D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/24_round-4.1D_inbox_01_conversa-aberta.png.png`

Observacao:

O pacote local tambem contem um arquivo antigo com prefixo `24_round-4.1C_checklists_01_lista-execucao-detalhe.png.png`. Para Inbox, o nome canonico correto e `24_round-4.1D_inbox_01_conversa-aberta.png`.

Objetivo:

Mostrar `/app/inbox` como workspace de atendimento ativo com lista de conversas, conversa selecionada e painel de contexto.

Estado representado:

- recepcao/operacao atendendo conversa de reposicao ou duvida de agenda;
- conversa selecionada em `Aguardando humano`;
- copiloto sugeriu resposta, mas humano ainda revisa;
- painel direito mostra aluno/responsavel, consentimento, historico curto, tarefas relacionadas e status do agente.
- navegacao superior de Atendimento com `Conversas`, `Envios` e `Historico`, com `Conversas` ativa. Se a imagem aprovada mostrar `Contatos`, tratar como atalho temporario/contextual que nao define pagina principal nesta rodada;
- lista de conversas com estados variados: aguardando humano, em andamento, copiloto sugeriu, falha de envio e opt-out;
- eventos de sistema discretos no centro da conversa;
- acao de opt-out como acao secundaria, nao dominante.

Cobertura:

- cobre `/app/inbox`;
- cobre `/app/conversas/[id]`;
- cobre estados principais de manual/copiloto/autonomo bloqueado;
- nao cobre visualmente `/app/envios`, que fica como contrato textual herdado ate falhas de envio exigirem imagem propria.

Mobile:

Fica para rodada mobile. No mobile, Inbox vira lista de conversas e detalhe em tela cheia/bottom sheet, nao tres colunas.

## Ajustes Aprovados Na Imagem Final

A versao final corrigiu:

- topbar antiga de Operacao removida;
- navegacao de Atendimento aplicada;
- conversa central com mais espaco;
- evento de sistema mais discreto;
- bloco de copiloto com acao `Usar sugestao`;
- opt-out reduzido para `Mais acoes`;
- painel direito preservado como contexto, sem virar perfil completo do aluno.
