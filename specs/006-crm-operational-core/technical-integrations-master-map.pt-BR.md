# Taliya CRM - Mapa Geral De Integracoes Tecnicas

Status: mapa mestre v1.
Data: 2026-05-25.

Contrato detalhado:

- `technical-integrations-detailed-contract.pt-BR.md`.

## Objetivo

Definir a camada de Integracoes Tecnicas do Taliya CRM sem misturar:

- Setup Inicial;
- Configuracoes Pos-Go-Live;
- Agentes/Fluxos;
- Control Planes;
- Billing Taliya;
- operacao diaria do studio.

Integracao tecnica nao e onde o dono configura o negocio do studio.

## Decisao Atualizada - MVP

No MVP, Integracoes Tecnicas **nao sao uma familia de paginas separada para o dono navegar**.

Elas aparecem dentro da configuracao especifica depois que a integracao existe ou quando ela bloqueia aquela configuracao.

Regra simples:

- WhatsApp aparece dentro de `/app/configuracoes/canais`;
- Pagamentos Taliya/provedor financeiro aparece dentro de `/app/configuracoes/financeiro/pagamentos`;
- Google Agenda/importacao de calendario aparece dentro de `/app/configuracoes/agenda` ou no fluxo contextual de importacao;
- e-mail do studio aparece dentro de `/app/configuracoes/canais` e, se for alerta interno, em `/app/configuracoes/notificacoes`;
- importacoes aparecem no contexto que importou os dados.

Isso evita criar uma central tecnica que o dono do studio nao precisa visitar no dia a dia.

Quando houver erro tecnico, a propria configuracao mostra:

- status da conexao;
- ultimo evento/falha legivel;
- impacto operacional;
- acao segura: testar, reconectar, reprocessar quando seguro ou abrir suporte/incidente;
- acesso a logs tecnicos compactos dentro da propria configuracao.

Nao teremos hub navegavel `/app/integracoes` no MVP.

Rotas tecnicas internas podem existir na implementacao como subrotas ou drawers, mas nao como familia visual principal do produto.

Integracao tecnica responde:

- o provedor esta conectado?
- quando conectou?
- o que esta funcionando?
- o que falhou?
- qual parte do CRM foi afetada?
- da para testar, reconectar ou reprocessar?
- precisa abrir suporte ou incidente?

## Regra Central

As telas operacionais e de configuracao continuam sendo o lugar principal para o dono trabalhar.

Integracoes ficam como camada tecnica de conexao, saude, logs e recuperacao **embutida na pagina que usa aquela conexao**.

Exemplos:

- WhatsApp aparece em Canais, Inbox, Envios e Agentes/Fluxos.
- A saude tecnica do WhatsApp fica em `/app/configuracoes/canais`.
- Pagamentos aparecem em Financeiro e Pagamentos Taliya.
- A saude tecnica do provedor financeiro fica em `/app/configuracoes/financeiro/pagamentos`.
- Google Agenda entra no MVP como fonte de importacao assistida por agente.
- A saude tecnica do calendario fica em `/app/configuracoes/agenda` ou no job contextual de importacao.

## Rotas

### Sem Hub `/app/integracoes` No MVP

Decisao:

- nao criar hub navegavel de integracoes para o dono;
- nao criar cards duplicando Canais, Pagamentos, Agenda e Notificacoes;
- nao transformar logs em area principal.

O conteudo tecnico aparece dentro da configuracao correspondente.

### Subarea tecnica dentro da configuracao especifica

Funcao:

- status;
- provedor;
- conta/numero/calendario conectado;
- ultima sincronizacao/evento;
- ultimo erro legivel;
- impacto no CRM;
- acoes seguras: testar, reconectar, reprocessar quando seguro, abrir suporte/incidente;
- logs compactos/filtraveis quando necessario;
- painel direito do agente de configuracao/suporte explicando status e proxima acao.

Nao deve conter:

- configuracao profunda de fluxo de agente;
- criacao de plano;
- edicao de agenda;
- edicao de aluno;
- regras de negocio;
- payload bruto tecnico como foco principal;
- painel gigante de infraestrutura.

### Logs tecnicos da integracao

Funcao:

- investigar eventos tecnicos da integracao;
- entender falhas;
- reprocessar quando for seguro;
- abrir incidente quando impactar operacao.

Deve conter:

- lista de eventos;
- filtros por status, periodo, tipo e objeto afetado;
- erro legivel;
- tentativa/retry;
- idempotencia;
- objeto afetado;
- acao sugerida;
- botao de reprocessar quando seguro;
- botao de abrir incidente/suporte;
- detalhe lateral do evento.

Nao deve conter:

- dados sensiveis desnecessarios;
- segredo de API;
- payload completo por padrao;
- acao destrutiva sem confirmacao.

Onde fica:

- WhatsApp: dentro de `/app/configuracoes/canais`, em subarea/drawer `Logs do WhatsApp`.
- Pagamentos Taliya: dentro de `/app/configuracoes/financeiro/pagamentos`, em subarea/drawer `Logs do provedor`.
- Google Agenda/importacao: dentro de `/app/configuracoes/agenda` ou do job contextual de importacao.
- E-mail: dentro de `/app/configuracoes/canais` ou `/app/configuracoes/notificacoes`, conforme uso.

## Status Padrao

Toda integracao deve usar os mesmos status:

| Status | Significado | Exemplo |
|---|---|---|
| `nao_conectada` | Ainda nao foi conectada | Google Agenda nunca conectado |
| `pendente` | Precisa de acao do dono ou da Taliya | WhatsApp aguardando validacao |
| `conectada` | Funcionando normalmente | WhatsApp recebendo mensagens |
| `limitada` | Funciona parcialmente | WhatsApp recebe, mas envio esta bloqueado |
| `falhou` | Falha que impacta operacao | Webhook de pagamento nao chega |
| `indisponivel` | Provedor fora ou instavel | Gateway com instabilidade |
| `pausada` | Studio/Taliya pausou por seguranca | Envio externo pausado |
| `requer_reconexao` | Permissao expirou ou foi revogada | Google Agenda perdeu acesso |

## Integracoes Do MVP

### 1. WhatsApp Business

Status: essencial.

Onde aparece para o dono:

- Setup Inicial, bloco Canais;
- `/app/configuracoes/canais`;
- `/app/inbox`;
- `/app/envios`;
- `/app/agentes` e `/app/fluxos`, quando houver agentes;
- subarea tecnica do WhatsApp dentro de `/app/configuracoes/canais`.

Funcao tecnica:

- conectar o numero oficial do studio;
- receber mensagens;
- enviar mensagens permitidas;
- registrar conversas;
- registrar tentativas de envio;
- informar falhas de envio;
- respeitar opt-out, janela, permissao e template quando aplicavel.

Fonte da verdade:

- CRM controla conversa, contato, estado operacional, opt-out e historico;
- provedor informa entrega, falha, mensagem recebida e status tecnico.

Impacta:

- Inbox;
- Atendimento;
- Vendas;
- Agenda;
- Financeiro;
- Agentes/Fluxos;
- Notificacoes;
- Envios;
- Uso/cotas quando mensagens forem cobradas ou contarem consumo.

Acoes permitidas:

- conectar;
- testar envio/recebimento;
- reconectar;
- pausar envio;
- ver logs;
- abrir suporte;
- abrir incidente se a falha afetar operacao.

Nao deve fazer:

- configurar mensagens automaticas;
- configurar fluxo de agente;
- decidir autonomia de agente;
- editar templates globais dentro da integracao;
- permitir que agente conecte ou desconecte sozinho.

### 2. Pagamentos Taliya / Provedor Financeiro

Status: integracao pos-go-live para automacao financeira.

Onde aparece para o dono:

- `/app/configuracoes/financeiro/pagamentos`;
- `/app/financeiro`;
- `/app/financeiro/movimentacoes`;
- subarea tecnica do provedor dentro de `/app/configuracoes/financeiro/pagamentos`.

No Setup Inicial:

- Pagamentos Taliya nao e configurado;
- o bloco Pagamento apenas seleciona meios aceitos no comeco: Pix, dinheiro e cartao;
- pode existir uma faixa educativa dizendo que automacao financeira entra depois;
- nenhum provedor, webhook, Pix automatico, cartao online, recorrencia ou KYC e iniciado no setup.

Funcao tecnica:

- conectar provedor financeiro;
- permitir Pix automatico;
- permitir cartao online;
- permitir recorrencia online;
- receber webhooks de pagamento;
- confirmar pagamentos;
- registrar falhas;
- apoiar conciliacao;
- registrar disputas/estornos quando houver suporte do provedor.

Fonte da verdade:

- CRM controla cobranca, aluno, plano, status operacional e liberacao de aulas/saldo;
- provedor confirma pagamento, falha, chargeback, estorno e eventos financeiros tecnicos;
- confirmacao do provedor vence comprovante manual nao validado.

Impacta:

- Financeiro;
- movimentacoes;
- cobrancas;
- saldo/aulas liberadas;
- inadimplencia;
- planos;
- Billing do aluno dentro do studio;
- Agentes/Fluxos financeiros, se existirem.

Acoes permitidas:

- iniciar ativacao;
- abrir ambiente seguro do provedor;
- testar conexao;
- ver status;
- ver logs;
- reprocessar webhook seguro;
- abrir suporte/incidente.

Nao deve fazer:

- configurar plano do aluno;
- configurar preco;
- configurar politica de desconto;
- alterar Billing Taliya;
- expor dados bancarios sensiveis dentro do CRM.

### 3. Google Agenda

Status: entra no MVP como importacao assistida por agente.

Decisao:

- Google Agenda pode ser conectado no MVP para importar agenda existente;
- o agente ajuda a ler os eventos e transformar em rascunhos de alunos, turmas, horarios e agenda base;
- a importacao pode acontecer nos blocos de Alunos/Turmas do Setup Inicial e em importacoes contextuais depois;
- Google Agenda nao sera fonte operacional de verdade depois do go-live;
- Google Agenda nao sera sincronizacao viva obrigatoria no MVP;
- escrita/sincronizacao bidirecional fica para decisao futura.

Regra para manter simples:

- o CRM Taliya deve funcionar mesmo sem Google Agenda;
- Google Agenda serve para acelerar migracao de dados;
- o agente prepara rascunhos e marca pendencias;
- o dono revisa antes de publicar;
- depois que a agenda do Taliya estiver publicada, o CRM vence.

Onde aparece para o dono:

- `/app/configuracoes/agenda`, se for usado para excecoes ou sincronizacao;
- `/app/agenda`, quando houver eventos vindos de calendario;
- subarea tecnica de calendario/importacao dentro de `/app/configuracoes/agenda` ou do job contextual de importacao.

Funcao tecnica:

- importar eventos;
- sugerir turmas recorrentes a partir de eventos repetidos;
- sugerir alunos/vinculos quando aparecerem nomes nos eventos;
- detectar conflitos;
- criar rascunhos para revisao;
- mostrar calendario conectado;
- avisar quando permissao expirar.

Fonte da verdade:

- CRM Agenda vence para aulas, turmas, presencas e reposicoes;
- Google Agenda alimenta importacao/rascunho;
- Google Agenda nao sobrescreve aula critica sem revisao.

Impacta:

- Agenda;
- Turmas;
- Alunos, quando eventos ajudarem a identificar nomes/vinculos;
- bloqueios;
- disponibilidade;
- conflitos.

Acoes permitidas:

- conectar calendario;
- escolher calendario lido;
- importar periodo;
- revisar rascunhos gerados pelo agente;
- testar leitura;
- reconectar;
- ver logs;
- remover acesso.

Nao deve fazer:

- montar turmas automaticamente sem revisao;
- sobrescrever agenda do CRM sem aprovacao;
- manter sincronizacao viva obrigatoria;
- criar ou alterar alunos sem revisao quando houver baixa confianca;
- editar toda a operacao do studio.

### 4. E-mail

Status: separado em dois contextos.

Decisao:

- e-mails que a Taliya envia para leads da propria Taliya pertencem ao backoffice/comercial interno da Taliya, nao ao CRM do studio;
- isso nao exige uma integracao de e-mail configuravel pelo dono do studio;
- e-mail do studio so vira integracao tecnica do CRM se o Taliya enviar e-mails em nome do studio para alunos, equipe ou contatos;
- se for apenas e-mail cadastrado como contato do studio, fica em Canais, sem integracao tecnica.

Onde aparece para o dono:

- `/app/configuracoes/canais`;
- subarea tecnica de e-mail dentro de `/app/configuracoes/canais`, somente se houver envio real em nome do studio pelo Taliya;
- notificacoes internas, se forem por e-mail.

Funcao tecnica:

- enviar e-mails transacionais;
- registrar entrega/falha;
- enviar convites de equipe;
- enviar comunicacoes administrativas quando permitido.

Fonte da verdade:

- CRM controla destinatario, contexto, permissao e historico;
- provedor informa entrega, bounce, falha e spam quando disponivel.

Impacta:

- Equipe;
- convites;
- Notificacoes;
- Comunicados, se existir depois;
- suporte.

Acoes permitidas:

- verificar e-mail remetente;
- testar envio;
- reconectar provedor;
- ver logs.

Nao deve fazer:

- virar ferramenta de campanha;
- configurar template global complexo;
- substituir Inbox.

Fora do CRM do studio:

- e-mail comercial que a Taliya envia para leads da propria Taliya;
- e-mail de onboarding comercial antes do studio virar tenant ativo;
- campanhas de venda da Taliya.

### 5. Importacoes

Status: nao e integracao viva principal.

Decisao:

- importacao deve ser contextual;
- nao deve existir como central principal para o dono no MVP;
- pode existir rota tecnica/historica para jobs: `/app/importacao` e `/app/importacao/[jobId]`, se necessario.

Onde aparece para o dono:

- Alunos;
- Turmas;
- Planos, se necessario;
- Financeiro antigo, se existir depois;
- Setup Inicial nos blocos correspondentes.

Funcao tecnica:

- receber arquivo;
- processar planilha;
- processar foto/anotacao;
- colar lista;
- detectar duplicidade;
- marcar pendencia;
- criar rascunho;
- registrar origem do dado.

Fonte da verdade:

- CRM vence depois que o dado e revisado;
- importacao cria rascunho, sugestao ou pendencia;
- importacao nao sobrescreve dado sensivel sem revisao.

Impacta:

- Alunos;
- Turmas;
- Planos;
- Agenda inicial;
- Dados/duplicidades, quando existir.

Acoes permitidas:

- revisar;
- aprovar;
- rejeitar;
- mesclar;
- corrigir;
- reprocessar job quando seguro.

Nao deve fazer:

- virar uma integracao permanente;
- atualizar dados criticos sem revisao;
- substituir telas de Alunos/Turmas/Financeiro.

## Integracoes Fora Do MVP Ou Apenas Referenciais

### Instagram, Facebook, TikTok, X E Site

Status: canais publicos/referenciais, nao integracoes tecnicas no MVP.

Onde ficam:

- `/app/configuracoes/canais`.

Funcao:

- registrar onde o studio aparece;
- ajudar atendimento, vendas e identidade publica;
- servir como referencia para equipe.

Nao fazem no MVP:

- captura automatica de lead;
- leitura de DM;
- resposta automatica;
- webhook social;
- campanha.

Se virarem integracao depois:

- entram como integracao propria;
- precisam de consentimento, permissoes, logs, falhas, fonte da verdade e limites de automacao.

### Assinatura De Documentos

Status: futuro/condicional.

Possivel uso:

- contrato;
- termo;
- autorizacao;
- politica assinada.

Nao entra agora como integracao principal.

### Nota Fiscal / Contabilidade

Status: futuro/condicional.

Possivel uso:

- emissao fiscal;
- exportacao contabil;
- conciliacao com contador.

Nao entra agora como integracao principal.

### CRM Externo / Planilha Permanente

Status: nao recomendado para MVP.

Regra:

- Taliya deve ser a fonte operacional depois do go-live;
- planilhas servem para importacao, nao para sincronizacao permanente.

## Relacao Com Configuracoes Pos-Go-Live

| Area de configuracao | Onde mostra a parte tecnica |
|---|---|
| Canais | status do WhatsApp/e-mail, teste, reconexao e logs compactos |
| Pagamentos Taliya | status do provedor financeiro, validacao, webhooks, conciliacao e logs compactos |
| Agenda | calendario/importacao, permissao expirada, conflito importado e logs compactos |
| Notificacoes | canal interno indisponivel e falhas de entrega internas |

Configuracoes mostram o que o dono quer.

Integracoes mostram se a conexao tecnica esta funcionando, mas aparecem dentro da propria configuracao.

## Relacao Com Agentes/Fluxos

Agentes/Fluxos podem depender de integracoes, mas nao configuram a integracao.

Exemplos:

- agente de atendimento depende de WhatsApp conectado;
- agente financeiro depende de Pagamentos Taliya ou de baixa manual confiavel;
- agente de agenda depende de Agenda/Turmas e, se houver, calendario externo;
- agente de vendas pode depender de WhatsApp, mas nao conecta WhatsApp sozinho.

Se uma integracao cair:

- o fluxo deve pausar ou degradar;
- o agente explica o impacto;
- o sistema cria pendencia/incidente quando necessario;
- o dono/admin decide reconectar ou pedir suporte.

## Relacao Com Control Planes

Integracoes e Control Planes se encontram em falhas, logs e incidentes.

Integracoes mostram:

- status tecnico por provedor;
- logs por integracao;
- teste/reconexao/reprocessamento seguro.

Control Planes mostram:

- execucoes afetadas;
- incidentes;
- risco;
- auditoria;
- uso/cotas;
- impacto operacional agregado.

Regra:

- Integracao responde "o provedor esta funcionando?".
- Control Plane responde "o que aconteceu na operacao e qual risco isso gerou?".

## Agente No Painel De Integracoes

O agente pode:

- explicar status;
- traduzir erro tecnico;
- dizer o impacto no CRM;
- sugerir proxima acao;
- preparar ticket para suporte;
- resumir logs;
- indicar onde corrigir configuracao;
- avisar quando uma falha bloqueia agente/fluxo.

O agente nao pode:

- conectar integracao sozinho;
- desconectar integracao sozinho;
- conceder permissao;
- alterar billing;
- acessar dado sensivel sem autorizacao;
- reprocessar acao sensivel sem confirmacao quando houver risco.

## Dados Minimos De Uma Integracao

Toda integracao deve ter:

- `id`;
- `tenantId`;
- `tipo`;
- `provedor`;
- `status`;
- `statusOperacional`;
- `ultimoEventoEm`;
- `ultimaSincronizacaoEm`;
- `ultimoErro`;
- `areasAfetadas`;
- `permissoesConcedidas`;
- `conectadaPor`;
- `conectadaEm`;
- `requerAcaoDe`;
- `podeReprocessar`;
- `podeReconectar`;
- `podePausar`;
- `auditTrailRef`.

## Dados Minimos De Um Log De Integracao

Todo log deve ter:

- `id`;
- `tenantId`;
- `integrationId`;
- `tipoEvento`;
- `direcao`: entrada, saida ou interno;
- `status`;
- `objetoAfetado`;
- `idempotencyKey`;
- `providerEventId`;
- `tentativa`;
- `erroLegivel`;
- `erroTecnicoSeguro`;
- `criadoEm`;
- `processadoEm`;
- `reprocessavel`;
- `incidenteRef`;
- `auditTrailRef`.

## Falhas Padrao

| Falha | Impacto | Destino |
|---|---|---|
| WhatsApp desconectado | Inbox e envios podem parar | `/app/configuracoes/canais` |
| Envio WhatsApp falhou | Mensagem nao chegou | `/app/envios/[sendId]` e logs |
| Webhook de pagamento falhou | Baixa automatica pode atrasar | `/app/configuracoes/financeiro/pagamentos` |
| Pagamento sem match | Precisa conciliacao | `/app/financeiro/movimentacoes` |
| Google Agenda perdeu permissao | Importacao de calendario para | `/app/configuracoes/agenda` |
| Importacao falhou | Dados ficam em rascunho/pendencia | job de importacao ou tela contextual |
| Provedor indisponivel | Acao tecnica fica limitada | integracao + incidente, se impactar operacao |

## Mapa Final

| Integracao | MVP | Tipo | Onde aparece no app | Configuracao relacionada | Observacao |
|---|---|---|---|---|---|
| WhatsApp Business | Sim | Canal vivo | `/app/configuracoes/canais` | Canais | Essencial para Inbox, envios e agentes |
| Pagamentos Taliya | Pos-go-live | Financeira viva | `/app/configuracoes/financeiro/pagamentos` | Pagamentos Taliya | Integracao com provedor para automacoes financeiras |
| Google Agenda | Sim | Importacao assistida | `/app/configuracoes/agenda` ou job contextual | Alunos/Turmas/Agenda | Agente transforma eventos em rascunhos; CRM vence depois |
| E-mail do studio | Condicional | Envio transacional | `/app/configuracoes/canais` ou `/app/configuracoes/notificacoes` | Canais/Notificacoes | So se houver envio real em nome do studio |
| E-mail Taliya para leads | Sim, interno | Comercial Taliya | Backoffice interno | Nao se aplica ao CRM do studio | Nao e configuracao do cliente |
| Importacoes | Sim, contextual | Job/processamento | `/app/importacao/[jobId]` se necessario | Alunos/Turmas/Planos | Nao e conexao viva |
| Instagram/Facebook/TikTok/X | Nao | Referencia publica | Nao criar | Canais | Links publicos no MVP |
| Site | Nao | Referencia publica | Nao criar | Canais | URL publica do studio |
| Assinatura digital | Futuro | Documento | Futuro | Documentos/Contratos | Nao MVP |
| Nota fiscal/contabilidade | Futuro | Fiscal/contabil | Futuro | Financeiro | Nao MVP |

## Decisao Final

Para o MVP, Integracoes Tecnicas ficam enxutas e embutidas nas configuracoes especificas:

1. WhatsApp Business.
2. Pagamentos Taliya/provedor financeiro no pos-go-live.
3. Google Agenda como importacao assistida por agente.
4. E-mail do studio somente se o Taliya enviar e-mail real em nome do studio.
5. Importacoes como jobs contextuais, nao como integracao viva.

Tudo que for rede social fica em Canais como referencia, nao como integracao tecnica.

E-mails comerciais enviados pela propria Taliya para leads da Taliya ficam no backoffice/comercial interno, fora das integracoes configuraveis do studio.

O proximo passo visual nao e criar hub de Integracoes. E garantir que Canais, Pagamentos, Agenda e Notificacoes tenham estados tecnicos claros quando uma conexao existir ou falhar.
