# Contrato Simples - Admin, Auditoria, Integracoes, Suporte E Billing - PT-BR

> Status: historico v0.1. As decisoes finais de Integracoes Tecnicas, Configuracoes Pos-Go-Live e Billing Taliya foram refinadas depois deste contrato. Use este arquivo apenas como referencia de escopo antigo quando houver conflito.

## Decisao De Escopo

Nao criar `/app/admin` como pagina principal.

Admin e uma camada de permissao, risco e governanca que aparece em Configuracoes, Auditoria, Suporte, Uso/Cotas e Billing.

No MVP:

- Auditoria nao precisa imagem propria;
- Integracoes Tecnicas nao tem hub proprio no MVP; aparecem embutidas na configuracao especifica;
- Importacao nao precisa imagem propria;
- Privacidade nao precisa imagem propria;
- Suporte precisa pagina completa e tem imagem propria aprovada;
- Billing Taliya tem pagina propria em `/app/billing`.

Essas superficies herdam padroes ja aprovados: tabela/lista densa, detalhe lateral, cards de status, logs, grants, planos/cotas, formularios sensiveis e auditoria.

Imagem aprovada de Suporte:

`47_round-4.1J_suporte_01_central-studio-taliya.png`

## Rotas Oficiais

| Area | Rotas |
| --- | --- |
| Auditoria | `/app/auditoria`, `/app/auditoria/[eventId]` |
| Integracoes Tecnicas | embutidas em `/app/configuracoes/canais`, `/app/configuracoes/financeiro/pagamentos`, `/app/configuracoes/agenda`, `/app/configuracoes/notificacoes` e jobs contextuais |
| Importacao | `/app/importacao`, `/app/importacao/[jobId]` |
| Privacidade | `/app/privacidade/solicitacoes`, `/app/privacidade/solicitacoes/[requestId]` |
| Suporte | `/app/suporte`, `/app/suporte/tickets`, `/app/suporte/tickets/[ticketId]`, `/app/suporte/acessos`, `/app/suporte/acessos/[grantId]` |
| Billing/assinatura | `/app/billing`, `/app/billing/invoices`, `/app/billing/add-ons`, `/app/uso`, `/app/uso/cotas` |

## Papel De Cada Area

### Auditoria

Trilha de prova do sistema.

Responde:

> Quem fez o que, quando, em qual objeto, de qual origem e com qual antes/depois?

Exemplos:

- usuario alterou politica de reposicao;
- gestor aprovou desconto;
- recepcao marcou chamada;
- sistema criou cobranca recorrente;
- agente sugeriu mensagem;
- suporte Taliya acessou a conta com grant;
- exportacao sensivel foi baixada.

### Integracoes

Conexao, status, logs e reprocessamento dos provedores.

Inclui:

- WhatsApp;
- pagamentos/Pix/gateway;
- webhooks;
- importacao;
- status de provedor;
- teste de conexao;
- logs;
- falhas e reprocessamento;
- abertura de incidente quando a falha impacta operacao.

### Importacao

Entrada e reconciliacao de dados externos.

Inclui:

- jobs de importacao;
- status;
- arquivos;
- erros;
- duplicidades;
- linhas ignoradas;
- reprocessamento;
- abertura de Qualidade de dados quando algo bloquear uso real.

### Privacidade

Solicitacoes sensiveis de dados.

Inclui:

- exportar dados;
- apagar/anonimizar quando permitido;
- opt-out;
- revisao humana;
- validacao de identidade;
- execucao auditada;
- negacao com motivo.

### Suporte

Pagina completa de relacionamento e resolucao de problemas entre o studio e a Taliya.

Responde:

> O que o studio pediu para a Taliya, qual o status, quem esta responsavel, qual impacto, e se a Taliya tem acesso temporario permitido?

Suporte e dedicado ao studio como cliente da Taliya.

Suporte nao e atendimento aos alunos do studio.

A pagina deve ser integrada a um **agente de suporte Taliya 24/7**.

Esse agente ajuda o studio a:

- tirar duvidas de uso do CRM;
- explicar configuracoes;
- consultar status de servicos;
- orientar correcao de falhas simples;
- criar ticket quando nao resolver;
- resumir logs e incidentes;
- preparar pedido de grant temporario quando a Taliya precisar investigar;
- encaminhar para suporte humano quando houver risco, billing, privacidade, bug real ou acao sensivel.

Fronteira:

- Inbox trata conversas com alunos e interessados;
- Operacao trata problemas internos do studio;
- Suporte trata problemas, duvidas, incidentes e solicitacoes do studio com a Taliya;
- Suporte/acessos trata autorizacao temporaria para a Taliya acessar a conta do studio;
- Auditoria prova o que aconteceu.

Suporte nao substitui Operacao do studio. Ele trata problemas do produto Taliya, duvidas de uso, falhas de integracao, incidentes, billing da assinatura e pedidos de ajuda.

Entram em Suporte:

- WhatsApp do studio desconectado;
- importacao com duplicidade ou falha;
- dificuldade para configurar Pix, pagamento ou integracao;
- duvida sobre cobranca da Taliya;
- agente parado, bloqueado ou com comportamento inesperado;
- pedido para autorizar acesso temporario da Taliya;
- erro no app ou em uma tela;
- duvida sobre configuracao de politica.

Nao entram em Suporte:

- aluno pedindo reposicao;
- interessado perguntando preco;
- cobranca de mensalidade do aluno;
- tarefa da recepcao;
- aprovacao de desconto para aluno;
- reclamacao de aluno sobre aula.

### Billing/Assinatura

Assinatura do studio com a Taliya.

Nao confundir com Financeiro do studio com seus alunos.

Inclui:

- plano atual;
- faturas da Taliya;
- metodo de pagamento da assinatura;
- agentes liberados;
- cotas;
- pacotes;
- upgrade/downgrade;
- bloqueios por inadimplencia;
- historico de alteracoes de entitlement.

## Pagina Completa De Suporte

Rota principal:

`/app/suporte`

Imagem aprovada:

`47_round-4.1J_suporte_01_central-studio-taliya.png`

Objetivo:

Centralizar pedidos do studio para a Taliya, status de atendimento, incidentes conhecidos, acessos temporarios e canais de ajuda. A pagina e do studio como cliente da Taliya, nao dos alunos do studio.

Blocos MVP:

| Bloco | Conteudo |
| --- | --- |
| Agente de suporte 24/7 | conversa assistida com a Taliya para duvidas, diagnostico inicial e abertura de ticket |
| Tickets abertos | pedidos, duvidas, falhas e incidentes reportados pelo studio |
| Status dos servicos | WhatsApp, pagamentos, importacao, agentes e app Taliya |
| Acessos temporarios | grants ativos, pendentes, expirados ou revogados |
| Historico recente | ultimas respostas, mudancas de status e acoes de suporte |
| Canais | contato com suporte, prioridade do plano, horario de atendimento |
| Base rapida | links para guias curtos quando houver |

Agente de suporte 24/7:

- deve estar visivel como ponto de entrada principal da pagina;
- pode responder duvidas operacionais usando docs e contexto permitido da conta;
- pode sugerir passos de resolucao;
- pode coletar contexto antes de abrir ticket;
- pode anexar resumo tecnico ao ticket;
- pode indicar servico afetado e impacto provavel;
- deve deixar claro quando esta escalando para humano;
- nao substitui aprovacao humana para acoes sensiveis.

Lista de tickets:

- titulo;
- tipo (`duvida`, `falha`, `incidente`, `billing`, `configuracao`, `pedido`);
- severidade;
- status;
- responsavel Taliya;
- ultima resposta;
- proxima acao;
- origem relacionada, quando existir;
- SLA ou expectativa de resposta, quando o plano tiver.

Detalhe de ticket:

- resumo;
- contexto do studio;
- conversa/historico;
- anexos;
- eventos relacionados;
- origem do problema;
- status;
- responsavel;
- proxima acao;
- necessidade de grant de acesso;
- auditoria de respostas e acoes.

Acoes:

- `Abrir ticket`;
- `Perguntar ao suporte 24/7`;
- `Responder`;
- `Anexar arquivo`;
- `Marcar resolvido`;
- `Reabrir`;
- `Abrir origem`;
- `Autorizar acesso temporario`;
- `Revogar acesso`;
- `Ver auditoria`.

O que nao entra em Suporte:

- tarefas internas do studio;
- atendimento a alunos;
- conversa WhatsApp com alunos;
- operacao diaria;
- aprovacao operacional do CRM;
- resolucao financeira dos alunos.

## Grants De Acesso Do Suporte

Rotas:

- `/app/suporte/acessos`;
- `/app/suporte/acessos/[grantId]`.

Um grant e uma autorizacao temporaria para a Taliya acessar dados ou operar uma acao limitada em nome do studio.

Campos minimos:

- solicitante;
- aprovador;
- motivo;
- escopo;
- objetos permitidos;
- permissoes concedidas;
- inicio;
- expiracao;
- status;
- ticket relacionado;
- trilha de auditoria.

Estados:

- `pendente`;
- `aprovado`;
- `ativo`;
- `expirado`;
- `revogado`;
- `negado`;
- `usado`.

Regras:

- suporte Taliya nao tem acesso livre;
- todo acesso precisa escopo, motivo e expiracao;
- grants sensiveis exigem dono/admin autorizado;
- toda acao feita via grant deve aparecer em Auditoria;
- agente autonomo nunca aprova grant;
- agente de suporte 24/7 pode preparar o pedido de grant, mas nao pode conceder acesso sozinho.

## O Que Cada Rota Precisa Ter No MVP

### `/app/auditoria`

- filtros por ator, objeto, origem, risco, data e tipo de evento;
- lista/tabela de eventos;
- destaque de eventos sensiveis;
- abertura do objeto original;
- exportacao quando permitido;
- detalhe lateral ou rota direta de evento.

### `/app/auditoria/[eventId]`

- ator;
- acao;
- objeto;
- origem;
- antes/depois quando houver;
- horario;
- IP/dispositivo quando aplicavel;
- agente/execucao quando aplicavel;
- ticket/grant/exportacao relacionada quando aplicavel.

### Integracoes Tecnicas Embutidas

- ficam dentro da configuracao especifica;
- nao tem hub proprio no MVP;
- mostram o provedor usado por aquela configuracao;
- status (`conectado`, `pendente`, `falhou`, `limitado`, `indisponivel`);
- ultima sincronizacao;
- teste de conexao;
- reconectar/desconectar quando permitido;
- abrir logs compactos;
- abrir incidente;
- aviso de impacto operacional.

### Logs Tecnicos Compactos

- eventos tecnicos filtraveis;
- payload resumido quando permitido;
- erro legivel;
- tentativa/retry;
- objeto afetado;
- reprocessar quando seguro;
- abrir incidente;
- auditoria.

### `/app/importacao`

- jobs recentes;
- arquivo/origem;
- status;
- linhas importadas;
- erros;
- duplicidades;
- itens pendentes de revisao;
- reprocessar;
- abrir Qualidade de dados.

### `/app/importacao/[jobId]`

- parametros;
- resumo por tipo de dado;
- erros por linha;
- duplicidades;
- decisoes tomadas;
- reprocessamento;
- auditoria.

### `/app/privacidade/solicitacoes`

- lista de solicitacoes;
- tipo;
- pessoa/objeto;
- status;
- prazo;
- responsavel;
- risco;
- proxima acao.

### `/app/privacidade/solicitacoes/[requestId]`

- identidade;
- base da solicitacao;
- dados afetados;
- impacto;
- validacao humana;
- aprovacao/negacao;
- execucao auditada;
- historico.

### `/app/suporte`

- resumo de tickets;
- entrada principal para o agente de suporte Taliya 24/7;
- status dos servicos;
- grants ativos/pendentes;
- atalhos de contato;
- historico recente;
- alertas de incidentes Taliya;
- botao para abrir ticket.

### `/app/suporte/tickets`

- lista de tickets;
- filtros por status, tipo, severidade e responsavel;
- SLA/expectativa quando aplicavel;
- detalhe lateral com conversa e proxima acao.

### `/app/suporte/tickets/[ticketId]`

- detalhe completo do ticket;
- conversa;
- anexos;
- eventos relacionados;
- status;
- responsavel;
- grant relacionado;
- auditoria.

### Billing/assinatura

- plano atual;
- proxima fatura;
- status de pagamento;
- cotas contratadas;
- agentes liberados;
- pacotes extras;
- historico;
- upgrade/downgrade quando permitido;
- bloqueios por billing explicados sem misturar com Financeiro dos alunos.

## Padroes Visuais Herdados

| Superficie | Padrao herdado |
| --- | --- |
| Auditoria | tabela/log + detalhe lateral + diff/antes-depois `3C.3` |
| Integracoes | cards de status + logs + falha/reprocessamento `3C.1` e `3C.3` |
| Importacao | fluxo de setup/importacao + tabela de erros/duplicidades |
| Privacidade | lista sensivel + detalhe lateral + confirmacao forte |
| Suporte | lista de tickets + status cards + detalhe lateral + grants |
| Billing | plano/cota/governanca `3B.5` e Uso/Cotas futuro |

## Auditoria Visual Da Imagem 47

Imagem aprovada:

`47_round-4.1J_suporte_01_central-studio-taliya.png`

Decisoes registradas:

- cobre `/app/suporte`;
- mostra a central studio ↔ Taliya, nao atendimento aos alunos;
- o agente de suporte 24/7 e entrada principal e fica acima dos tickets recentes;
- tickets recentes, status dos servicos, acessos temporarios e prioridade do plano aparecem na mesma superficie sem virar Inbox;
- painel direito representa um ticket selecionado;
- `Responder` responde ao ticket com a Taliya, nao a aluno;
- `WhatsApp desconectou` neste contexto significa problema da integracao do studio, nao conversa de aluno;
- `Autorizar acesso` exige escopo, motivo, permissao e expiracao mesmo quando aparece como botao simples;
- `Ver auditoria` depende de permissao;
- o agente de suporte 24/7 nao conta como agente operacional do studio nos planos 0/1/3/7;
- o agente de suporte 24/7 nao aprova grant, nao altera billing, nao executa privacidade e nao conecta/desconecta integracao sozinho;
- detalhe lateral aberto representa estado selecionado para documentacao visual; carregamento padrao pode abrir sem detalhe ou com o ultimo ticket selecionado conforme produto.

Correcao de implementacao:

- a URL canonica e `/app/suporte`; qualquer referencia visual com `/app/app/suporte` deve ser tratada como erro de geracao de imagem, nao como rota real.

## Manual, Copiloto E Autonomo

| Modo | Comportamento |
| --- | --- |
| 0 agentes | Tudo funciona manualmente para usuarios autorizados. |
| Manual | Admin autorizado filtra, decide, conecta, aprova, revoga e exporta. |
| Copiloto | Pode resumir log, explicar erro, sugerir proxima acao, redigir resposta de suporte e ajudar o agente de suporte 24/7 a abrir ticket com contexto. |
| Autonomo | Nao aprova grant, nao executa privacidade, nao altera billing, nao conecta/desconecta integracao e nao concede acesso. |

O agente de suporte 24/7 e um agente da Taliya para atendimento ao studio. Ele nao conta como agente operacional do studio para falar com alunos e nao deve ser confundido com os agentes de CRM contratados pelo studio.

## O Que Nao Deve Aparecer

- `/app/admin` como dashboard generico;
- suporte Taliya com acesso livre;
- agente de suporte 24/7 atendendo alunos do studio;
- agente aprovando grant ou privacidade sozinho;
- billing misturado com financeiro dos alunos;
- integracao escondendo falha critica;
- auditoria editavel;
- exportacao sensivel sem permissao;
- privacidade sem validacao e trilha de auditoria;
- tickets de suporte substituindo tarefas internas do studio.

## Criterio Para Imagem Futura

Gerar imagem propria apenas se:

- Integracoes virar etapa central de onboarding/configuracao;
- Auditoria precisar demonstrar diff complexo;
- Privacidade tiver fluxo sensivel recorrente;
- Billing/Uso/Cotas for fechado visualmente junto com Agentes;
- grants de suporte precisarem de tela de decisao propria por risco.

Suporte ja tem imagem propria aprovada. Para as demais superficies, contrato textual + padroes herdados sao suficientes.
