# Taliya CRM - Mapa Mestre De Configuracoes Pos-Go-Live

Status: mapa mestre v1.
Data: 2026-05-24.

## Objetivo

Definir as Configuracoes Pos-Go-Live do Taliya CRM sem transformar o produto em uma parede de opcoes.

Configuracoes Pos-Go-Live existem para:

- ajustar o CRM base depois que o studio ja esta operando;
- completar o que ficou para depois do Setup Inicial;
- manter regras simples e necessarias em lugares previsiveis;
- apontar pendencias para a pagina certa;
- nao misturar configuracao comum com Agentes/Fluxos, Billing Taliya ou Control Planes.
- mostrar o status tecnico de uma integracao dentro da configuracao especifica, quando aquela integracao existir ou bloquear a operacao.

## Documentos Canonicos Relacionados

- `post-go-live-configuration-field-contracts.pt-BR.md`
  - campos, tipos, defaults, validacoes e objetos por pagina.
- `post-go-live-configuration-state-contracts.pt-BR.md`
  - estados de pagina, bloqueios, erros, permissao, integracao e entitlement.
- `post-go-live-configuration-visual-inheritance-audit.pt-BR.md`
  - imagens proprias e paginas herdadas.
- `post-go-live-configuration-final-audit.pt-BR.md`
  - auditoria final e mapas atualizados.

## Regra Principal

Quanto menos configuracao livre, melhor.

Uma pagina so fica em Configuracoes se o dono/admin realmente precisa ajustar aquilo para o CRM operar melhor.

Nao entram aqui:

- builder de agente;
- central tecnica separada de integracoes;
- billing da Taliya;
- execucoes/falhas/incidentes;
- politicas globais complexas;
- privacidade configuravel livre;
- dashboards de uso/cota;
- operacao diaria de agenda, financeiro, alunos ou tarefas.

## Lista Final De Paginas

Configuracoes Pos-Go-Live tera **9 paginas**:

1. `/app/configuracoes`
   - Hub de configuracoes.
2. `/app/configuracoes/studio`
   - Studio.
3. `/app/configuracoes/equipe`
   - Equipe.
4. `/app/configuracoes/permissoes`
   - Permissoes.
5. `/app/configuracoes/canais`
   - Canais.
6. `/app/configuracoes/financeiro/modelos`
   - Planos e modelos.
7. `/app/configuracoes/financeiro/pagamentos`
   - Pagamentos e financeiro.
8. `/app/configuracoes/agenda`
   - Agenda.
9. `/app/configuracoes/notificacoes`
   - Notificacoes.

## Paginas Removidas Como Rota Propria

| Pagina antiga | Decisao | Onde fica agora |
|---|---|---|
| `/app/configuracoes/agenda/consumo-aulas` | Removida como pagina propria | Dentro de `/app/configuracoes/financeiro/modelos`, por plano |
| `/app/configuracoes/financeiro` | Removida como pagina propria | Dentro de `/app/configuracoes/financeiro/pagamentos` |

Motivo:

- consumo de aulas e reposicao simples fazem parte de como cada plano funciona;
- financeiro geral separado criava configuracao demais;
- vencimento, tolerancia, inadimplencia e baixa manual cabem junto de pagamentos;
- excecoes mais profundas pertencem a operacao, Permissoes ou Agentes/Fluxos, nao a uma pagina de configuracao livre.

## 1. `/app/configuracoes` - Hub

### Para Que Serve

Ser a entrada simples das configuracoes do CRM.

O usuario deve bater o olho e escolher qual area quer ajustar.

### O Que Tem

- titulo `Configuracoes`;
- subtitulo curto: `Ajustes do CRM depois do go-live.`;
- 8 cards, um para cada pagina interna:
  - Studio;
  - Equipe;
  - Permissoes;
  - Canais;
  - Planos e modelos;
  - Pagamentos e financeiro;
  - Agenda;
  - Notificacoes;
- icone;
- descricao curta;
- status curto:
  - `Pronto`;
  - `Revisar`;
  - `Pendente`;
  - `Conectado`, quando for canal/pagamento;
- botao `Abrir`.

### O Que Nao Tem

- Agente de Configuracao;
- painel direito;
- historico;
- atividade recente;
- metricas;
- resumo grande;
- filtros;
- formularios.

## 2. `/app/configuracoes/studio` - Studio

### Para Que Serve

Editar dados basicos do studio e a janela institucional de funcionamento.

### O Que Tem

- nome do studio;
- nome publico;
- unidade principal;
- endereco;
- cidade/UF;
- fuso horario;
- dias de funcionamento;
- horario de abertura;
- horario de fechamento;
- pausa, se existir;
- previa da janela semanal de funcionamento;
- status `Publicado` ou `Alteracao manual`;
- botoes `Salvar alteracoes` e `Cancelar`;
- Agente de Configuracao explicando impacto curto.

### O Que Nao Tem

- WhatsApp;
- e-mail;
- redes sociais;
- feriados;
- bloqueios;
- turmas;
- aulas;
- alunos;
- reposicoes;
- fluxo de agente.

### Regra

Studio define a base institucional.

Feriados e bloqueios ficam em Agenda. Canais de contato ficam em Canais.

## 3. `/app/configuracoes/equipe` - Equipe

### Para Que Serve

Gerenciar quem usa o Taliya.

### O Que Tem

- lista de pessoas;
- nome;
- e-mail;
- WhatsApp interno, se usado;
- papel principal;
- status:
  - ativo;
  - inativo;
  - convite pendente;
- ultimo acesso;
- adicionar pessoa;
- reenviar convite;
- desativar pessoa;
- reativar pessoa;
- trocar dono/admin com confirmacao;
- link discreto para Permissoes.

### O Que Nao Tem

- matriz de permissoes;
- configuracao de agente;
- cotas;
- logs;
- escala de professor;
- comissoes;
- folha de pagamento.

### Regra

Equipe responde: `quem usa o Taliya`.

Permissoes responde: `o que cada papel pode fazer`.

## 4. `/app/configuracoes/permissoes` - Permissoes

### Para Que Serve

Definir o que cada papel pode fazer no CRM.

### O Que Tem

- papeis do MVP:
  - Dono/Admin;
  - Recepcao;
  - Professor;
- resumo do padrao de cada papel;
- poucos ajustes sensiveis:
  - professor pode ver telefone/WhatsApp do aluno;
  - professor pode adicionar observacao;
  - recepcao pode registrar pagamento;
  - recepcao pode editar plano do aluno;
  - recepcao pode aplicar desconto simples;
  - recepcao pode cancelar cobranca;
- resumo de impacto antes de salvar;
- historico leve de mudancas;
- status da regra;
- botoes `Salvar alteracoes` e `Cancelar`;
- Agente de Configuracao explicando o impacto das permissoes.

### O Que Nao Tem

- builder de permissao por campo;
- permissao de agente;
- limite de fluxo;
- cota;
- log tecnico;
- politica global complexa.

### Regra

Limites de pessoas ficam aqui.

Limites de agentes ficam em Agentes/Fluxos.

## 5. `/app/configuracoes/canais` - Canais

### Para Que Serve

Configurar por onde o studio pode falar e ser encontrado.

### O Que Tem

- WhatsApp Business do studio;
- status resumido da conexao oficial;
- e-mail do studio;
- Instagram;
- Facebook;
- TikTok;
- X;
- site;
- canal principal de contato;
- canal principal para avisos internos, quando aplicavel;
- pendencia de conexao;
- subarea tecnica compacta, quando houver detalhe de conexao, teste, reconexao ou log;
- botoes `Salvar canais` e `Cancelar`;
- Agente de Configuracao explicando fronteira com Integracoes.

### O Que Nao Tem

- texto de mensagem;
- template;
- campanha;
- automacao;
- agente respondendo aluno;
- logs tecnicos profundos.

### Regra

Canais responde: `por onde falar`.

O que sera dito fica no contexto que usa a mensagem.

Se o WhatsApp ou e-mail tiver erro tecnico, a propria pagina mostra o status, o impacto e a acao segura. Nao existe hub separado de Integracoes no MVP.

## 6. `/app/configuracoes/financeiro/modelos` - Planos E Modelos

### Para Que Serve

Configurar o que o aluno compra e como esse direito de aula funciona.

Esta pagina absorve a antiga ideia de `Consumo de aulas`.

### O Que Tem

- lista de planos;
- criar plano;
- editar plano;
- duplicar plano;
- inativar plano;
- status ativo/inativo;
- alunos usando o plano;
- impacto da alteracao;
- como o Taliya entende o plano.

Campos por plano:

- nome do plano;
- tipo:
  - mensalidade por frequencia semanal;
  - mensalidade por quantidade mensal;
  - pacote de aulas;
  - aula avulsa;
  - experimental/avaliacao;
  - outro, com revisao;
- valor;
- quantidade/frequencia de aulas;
- validade/ciclo;
- recorrencia comercial, quando aplicavel;
- se permite reposicao;
- aviso minimo para gerar reposicao;
- prazo para usar reposicao;
- regra simples para falta sem aviso;
- excecao manual permitida ou nao.

### O Que Nao Tem

- Pix;
- dinheiro;
- cartao;
- baixa;
- provedor;
- recorrencia automatica de pagamento;
- mensagem de cobranca;
- automacao de agente;
- simulacao profunda.

### Regra

Planos e modelos responde: `o que o aluno compra e como esse direito e usado`.

Pagamentos e financeiro responde: `como cobra, recebe, baixa e lida com atraso`.

## 7. `/app/configuracoes/financeiro/pagamentos` - Pagamentos E Financeiro

### Para Que Serve

Configurar o necessario para o studio cobrar, receber, dar baixa e ativar Pagamentos Taliya.

Esta pagina absorve a antiga ideia de `Financeiro geral`.

### O Que Tem

Bloco `Meios e baixa manual`:

- Pix manual;
- dinheiro;
- cartao presencial;
- baixa manual;
- comprovante permitido como detalhe da baixa manual, sem bloco proprio.

Bloco `Regras financeiras simples`:

- vencimento padrao;
- tolerancia de atraso;
- quando marcar aluno como inadimplente;
- baixa manual permitida;
- comprovante permitido dentro da baixa manual;
- desconto simples permitido ou nao;
- link para Permissoes quando a regra depender de papel.

Bloco `Pagamentos Taliya`:

- status dos Pagamentos Taliya;
- CTA `Ativar Pagamentos Taliya`;
- Pix Taliya;
- cartao online;
- recorrencia online;
- baixa automatica;
- conciliacao;
- estado pendente/ativo/bloqueado;
- subarea tecnica do provedor quando houver problema tecnico.

Estado `Pagamentos Taliya pendente`:

- Pix Taliya, cartao online, recorrencia online, baixa automatica e conciliacao aparecem bloqueados ate ativar;
- CTA principal: `Ativar Pagamentos Taliya`;
- meios manuais continuam ativos.

Estado `Pagamentos Taliya ativo`:

- Pix Taliya pode ser ligado/desligado;
- cartao online pode ser ligado/desligado;
- recorrencia online pode ser ligada/desligada quando houver cobranca recorrente;
- baixa automatica fica ativa para pagamentos online confirmados pelo provedor;
- conciliacao fica ativa/resumida;
- CTA principal vira `Salvar preferencias`;
- a pagina mostra `Gerenciar Pagamentos Taliya` ou `Ver detalhes tecnicos` como link secundario dentro da propria pagina;
- meios manuais continuam disponiveis para casos presenciais, excecoes ou falha do online.

### O Que Nao Tem

- criacao de plano;
- valor de mensalidade;
- regra de reposicao;
- template de cobranca;
- escolha livre de provedor;
- webhook/log tecnico como pagina separada;
- dados bancarios sensiveis;
- Billing Taliya;
- faturas da Taliya.
- configuracao de meio de pagamento por plano.
- bloco separado de comprovante;
- bloco final de impacto.

### Regra

Pagamentos e financeiro responde: `como o studio cobra, recebe e baixa pagamentos de alunos`.

Integracoes tecnicas respondem: `o provedor esta conectado e funcionando?`, mas aparecem dentro desta pagina quando o provedor financeiro existir ou falhar.

Billing Taliya responde: `qual a assinatura do studio com a Taliya?`.

Planos nao escolhem meio de pagamento.

O modelo correto e:

`Plano gera cobranca.`

`Aluno paga por um meio aceito.`

`Taliya registra ou identifica a baixa.`

`Cobranca paga libera ou mantem aulas/saldo.`

Recorrencia online depende do tipo de cobranca gerada pelo plano, nao de configurar um meio dentro do plano.

## 8. `/app/configuracoes/agenda` - Agenda

### Para Que Serve

Configurar excecoes e comportamento basico da agenda depois do go-live.

Nao e a agenda operacional do dia.

### O Que Tem

Bloco `Dias fechados e excecoes`:

- feriados;
- recessos;
- dias fechados;
- horarios especiais.

Bloco `Bloqueios temporarios`:

- periodo bloqueado;
- motivo;
- unidade/turma afetada, se necessario;
- impacto em aulas futuras.

Bloco `Regras simples da agenda`:

- lista de espera ligada/desligada;
- encaixe permitido ou nao;
- tolerancia simples para chamada/presenca, se necessario.

Subarea tecnica, somente quando aplicavel:

- calendario externo/importacao conectado;
- permissao expirada;
- ultimo job de importacao;
- falha legivel;
- testar leitura/reconectar;
- logs compactos do job.

Impacto de aulas futuras:

- aparece somente dentro do item afetado, quando necessario;
- nao existe bloco separado de resumo de impacto nesta pagina.

### O Que Nao Tem

- horario institucional basico do studio;
- edicao pesada de turma;
- agenda diaria;
- aluno especifico;
- saldo/reposicao detalhada;
- pagamento;
- mensagem automatica;
- fluxo de agente;
- regra profunda de falta/no-show.

### Regra

Studio define a janela institucional.

Agenda define excecoes e comportamento basico do calendario.

Planos e modelos define consumo/reposicao por plano.

## 9. `/app/configuracoes/notificacoes` - Notificacoes

### Para Que Serve

Definir quem da equipe recebe alertas internos do CRM.

### O Que Tem

- alertas por papel:
  - Dono/Admin;
  - Recepcao;
  - Professor;
- tipos de alerta:
  - aprovacao pendente;
  - pagamento critico;
  - integracao com falha;
  - aula com problema;
  - aluno sem contato;
  - cobranca manual;
  - convite de equipe pendente;
  - pendencia de configuracao;
- canal interno preferido, quando aplicavel;
  - WhatsApp interno significa WhatsApp da equipe, nao WhatsApp do aluno;
- frequencia:
  - imediato;
  - diario;
  - semanal;
- silenciar alerta nao critico fora do horario;
- status geral quando algum alerta precisar revisao.

### O Que Nao Tem

- mensagem para aluno;
- template;
- campanha;
- automacao;
- agente;
- cota;
- log tecnico.

### Regra

Notificacoes responde: `quem da equipe deve ser avisado`.

Canais responde: `por onde o studio se comunica`.

Agentes/Fluxos responde: `quem age automaticamente`.

## Imagens Necessarias

Estas paginas precisam de imagem propria:

1. `/app/configuracoes`
   - hub com 8 cards, sem secoes e sem painel direito.
   - Imagem aprovada: `60_round-4.1M_configuracoes_01_hub-8-cards-aprovado.png`.
2. `/app/configuracoes/permissoes`
   - matriz simples por papel.
   - Imagem aprovada: `61_round-4.1M_configuracoes_02_permissoes-aprovado.png`.
3. `/app/configuracoes/financeiro/pagamentos`
   - Pagamentos e financeiro, incluindo meios, baixa manual, regras simples e Pagamentos Taliya.
   - Imagem aprovada: `62_round-4.1M_configuracoes_03_pagamentos-financeiro-aprovado.png`.
4. `/app/configuracoes/agenda`
   - excecoes, bloqueios e regras simples de agenda.
   - Imagem aprovada: `63_round-4.1M_configuracoes_04_agenda-aprovado.png`.
5. `/app/configuracoes/notificacoes`
   - alertas internos por papel.
   - Imagem aprovada: `64_round-4.1M_configuracoes_05_notificacoes-aprovado.png`.

Observacao:

- nao gerar imagem propria para paginas que so mudam shell/estado em relacao ao Setup Inicial.

## Imagens Que Herdam Do Setup Inicial

Estas paginas tem rota propria, mas nao precisam de imagem nova agora:

| Pagina | Herda de | Ajuste necessario |
|---|---|---|
| `/app/configuracoes/studio` | `51D_round-4.1J_onboarding_bloco-1-studio-aprovado.png` | Trocar shell de onboarding por shell CRM, status publicado e CTAs de salvar/cancelar |
| `/app/configuracoes/equipe` | `51E_round-4.1J_onboarding_bloco-2-equipe-aprovado.png` | Trocar convites preparados por usuarios reais, convite pendente e ultimo acesso |
| `/app/configuracoes/canais` | `51F_round-4.1J_onboarding_bloco-3-canais-aprovado.png` | Trocar rascunho por status conectado/pendente e subarea tecnica compacta quando houver falha/conexao |
| `/app/configuracoes/financeiro/modelos` | `51G_round-4.1J_onboarding_bloco-4-planos-aprovado.png` | Acrescentar planos ativos/inativos, alunos usando, duplicar/inativar e consumo/reposicao simples por plano |

## O Que Fica Fora De Configuracoes

| Tema | Onde fica |
|---|---|
| Agentes, modos, limites, fallback, simulacao e publicacao de fluxos | `/app/agentes/*` |
| Logs tecnicos de WhatsApp, pagamento, e-mail e importacoes | subareas compactas dentro da configuracao especifica ou job contextual |
| Provedor financeiro conectado, webhooks e reprocessamento tecnico | `/app/configuracoes/financeiro/pagamentos`, dentro de Pagamentos Taliya |
| Assinatura do studio com a Taliya, agentes inclusos, add-ons e faturas | `/app/billing` |
| Uso, cotas e consumo de mensagens/IA | `/app/uso` |
| Auditoria completa | `/app/auditoria` |
| Incidentes e falhas de operacao | `/app/operacao/incidentes` |
| Operacao diaria de agenda | `/app/agenda` |
| Operacao diaria de financeiro | `/app/financeiro` |

## Decisao Final

As Configuracoes Pos-Go-Live ficam com 9 paginas e 5 imagens proprias.

Isso reduz configuracao desnecessaria sem perder as telas que precisam provar uma proposta propria.
