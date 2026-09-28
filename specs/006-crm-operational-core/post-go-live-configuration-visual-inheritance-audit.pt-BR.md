# Taliya CRM - Auditoria Visual Das Configuracoes Pos-Go-Live

Status: decisao v1.
Data: 2026-05-24.

## Objetivo

Definir quais paginas de Configuracoes Pos-Go-Live precisam de imagem propria e quais herdam imagens aprovadas do Setup Inicial.

Esta auditoria acompanha o mapa mestre:

- `post-go-live-configuration-master-map.pt-BR.md`

## Criterio

Gerar imagem propria somente quando a pagina precisa provar uma proposta visual/funcional nova.

Nao gerar imagem nova quando a pagina:

- repete a decisao principal do Setup Inicial;
- muda apenas shell, rota, estado publicado e CTA;
- pode ser documentada com diferencas claras sobre uma imagem ja aprovada.

Uma pagina pode usar componentes ja aprovados e ainda precisar de imagem propria. O criterio nao e reaproveitamento de componentes, e sim clareza da proposta.

## Decisao Final

Configuracoes Pos-Go-Live tem 9 paginas:

| Pagina | Precisa imagem propria? | Motivo |
|---|---:|---|
| `/app/configuracoes` | Sim | Hub novo com 8 cards |
| `/app/configuracoes/studio` | Nao | Herda Studio do Setup Inicial |
| `/app/configuracoes/equipe` | Nao | Herda Equipe do Setup Inicial com lista operacional |
| `/app/configuracoes/permissoes` | Sim | Nao existe no Setup Inicial |
| `/app/configuracoes/canais` | Nao | Herda Canais do Setup Inicial |
| `/app/configuracoes/financeiro/modelos` | Nao | Herda Planos do Setup Inicial e absorve consumo/reposicao simples |
| `/app/configuracoes/financeiro/pagamentos` | Sim | Pagamentos e financeiro tem proposta propria |
| `/app/configuracoes/agenda` | Sim | Agenda pos-live nao e a agenda base do setup |
| `/app/configuracoes/notificacoes` | Sim | Nao existe equivalente forte no Setup Inicial |

## Imagens Necessarias

### 1. `/app/configuracoes`

Imagem propria.

Nome sugerido:

```text
60_round-4.1M_configuracoes_01_hub-8-cards-aprovado.png
```

Status:

- aprovada em 2026-05-23;
- arquivo canonico:
  `D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\60_round-4.1M_configuracoes_01_hub-8-cards-aprovado.png`.

Deve mostrar:

- shell CRM padrao;
- rota `/app/configuracoes`;
- titulo `Configuracoes`;
- subtitulo `Ajustes do CRM depois do go-live.`;
- 8 cards sem secoes:
  - Studio;
  - Equipe;
  - Permissoes;
  - Canais;
  - Planos e modelos;
  - Pagamentos e financeiro;
  - Agenda;
  - Notificacoes;
- cada card com icone, descricao curta, status e botao `Abrir`.

Nao deve mostrar:

- Agente de Configuracao;
- painel direito;
- filtros;
- historico;
- atividade recente;
- metricas;
- resumo grande.

### 2. `/app/configuracoes/permissoes`

Imagem propria.

Nome sugerido:

```text
61_round-4.1M_configuracoes_02_permissoes-aprovado.png
```

Status:

- aprovada em 2026-05-23;
- arquivo canonico:
  `D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\61_round-4.1M_configuracoes_02_permissoes-aprovado.png`.

Deve mostrar:

- shell CRM;
- rota `/app/configuracoes/permissoes`;
- titulo `Permissoes`;
- status da configuracao;
- cards/colunas para:
  - Dono/Admin;
  - Recepcao;
  - Professor;
- ajustes sensiveis:
  - professor ve telefone/WhatsApp do aluno;
  - professor adiciona observacao;
  - recepcao registra pagamento;
  - recepcao edita plano do aluno;
  - recepcao aplica desconto simples;
  - recepcao cancela cobranca;
- resumo de impacto antes de salvar;
- historico leve;
- Agente de Configuracao no painel direito.

Referencias:

```text
16_round-4.1S_app-shell_01_base-web.png
12_round-3b5_sistema-plano-governanca_aprovada.png
08_round-3b1_inputs-formularios-filtros_aprovada.png
51B_round-4.1J_onboarding_agente-configuracao-chat-aprovado.png
```

### 3. `/app/configuracoes/financeiro/pagamentos`

Imagem propria.

Nome sugerido:

```text
62_round-4.1M_configuracoes_03_pagamentos-financeiro-aprovado.png
```

Status:

```text
Aprovada.
```

Arquivo canonico:

```text
D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\62_round-4.1M_configuracoes_03_pagamentos-financeiro-aprovado.png
```

Estado representado:

- Pagamentos Taliya pendente;
- meios manuais ativos;
- regras financeiras simples visiveis;
- comprovante tratado apenas como detalhe da baixa manual;
- sem bloco separado de comprovante;
- sem bloco final de impacto.

Titulo visual recomendado:

```text
Pagamentos e financeiro
```

Deve mostrar:

- shell CRM;
- rota `/app/configuracoes/financeiro/pagamentos`;
- status: `Manual ativo`, `Pagamentos Taliya pendente` ou `Pagamentos Taliya ativo`;
- bloco `Meios e baixa manual`:
  - Pix manual;
  - dinheiro;
  - cartao presencial;
  - baixa manual;
  - comprovante permitido como detalhe da baixa manual, sem bloco proprio;
- bloco `Regras financeiras simples`:
  - vencimento padrao;
  - tolerancia de atraso;
  - quando marcar inadimplente;
  - desconto simples permitido ou nao;
  - link para Permissoes quando depender de papel;
- bloco `Pagamentos Taliya`:
  - Pix Taliya;
  - cartao online;
  - recorrencia online;
  - baixa automatica;
  - conciliacao;
  - CTA `Ativar Pagamentos Taliya`;
- estado depois de ativo:
  - Pix Taliya, cartao online e recorrencia online podem ser gerenciados;
  - baixa automatica fica ativa para pagamentos online confirmados;
  - meios manuais continuam disponiveis;
  - CTA vira `Salvar preferencias` ou `Gerenciar Pagamentos Taliya`;
- detalhe tecnico compacto dentro da propria pagina em caso de falha;
- Agente de Configuracao no painel direito.

Nao deve mostrar:

- escolha livre de provedor;
- webhook;
- payload;
- logs tecnicos;
- dados bancarios sensiveis;
- faturas da Taliya;
- Billing Taliya;
- criacao de plano.
- bloco separado de comprovante;
- bloco final de impacto.

Referencias:

```text
16_round-4.1S_app-shell_01_base-web.png
51K_round-4.1J_onboarding_bloco-5-pagamento-aprovado.png
30_round-4.1F_financeiro_01_visao-geral-filas.png.png
34_round-4.1F_financeiro_04_movimentacoes-filtros-drawer.png.png
51B_round-4.1J_onboarding_agente-configuracao-chat-aprovado.png
```

### 4. `/app/configuracoes/agenda`

Imagem propria.

Nome sugerido:

```text
63_round-4.1M_configuracoes_04_agenda-aprovado.png
```

Status:

- aprovada em 2026-05-24;
- arquivo canonico:
  `D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\63_round-4.1M_configuracoes_04_agenda-aprovado.png`.

Deve mostrar:

- shell CRM;
- rota `/app/configuracoes/agenda`;
- titulo `Agenda`;
- status da configuracao;
- bloco `Dias fechados e excecoes`:
  - feriados;
  - recessos;
  - dias fechados;
  - horarios especiais;
- bloco `Bloqueios temporarios`:
  - periodo;
  - motivo;
  - unidade/turma afetada, se necessario;
  - impacto local em aulas futuras, apenas dentro do item afetado;
- bloco `Regras simples da agenda`:
  - lista de espera ligada/desligada;
  - encaixe permitido ou nao;
  - tolerancia simples de chamada/presenca, se necessario;
- Agente de Configuracao no painel direito.

Nao deve mostrar:

- agenda diaria operacional;
- aluno especifico;
- pagamento;
- saldo/reposicao detalhada;
- regra profunda de falta/no-show;
- mensagem automatica;
- fluxo de agente;
- resumo de impacto como bloco separado.

Referencias:

```text
16_round-4.1S_app-shell_01_base-web.png
51J_round-4.1J_onboarding_bloco-7-agenda-aprovado.png
26_round-4.1F_agenda_01_calendario-operacional.png.png
36_round-4.1F_grade_01_semana-modelo-bloqueio.png.png
51B_round-4.1J_onboarding_agente-configuracao-chat-aprovado.png
```

### 5. `/app/configuracoes/notificacoes`

Imagem propria.

Nome sugerido:

```text
64_round-4.1M_configuracoes_05_notificacoes-aprovado.png
```

Status:

- aprovada em 2026-05-24;
- arquivo canonico:
  `D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\64_round-4.1M_configuracoes_05_notificacoes-aprovado.png`.

Deve mostrar:

- shell CRM;
- rota `/app/configuracoes/notificacoes`;
- titulo `Notificacoes`;
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
- frequencia:
  - imediato;
  - diario;
  - semanal;
- canais internos da equipe:
  - dentro do Taliya;
  - e-mail interno;
  - WhatsApp interno da equipe;
- silenciar alerta nao critico fora do horario;
- status geral quando algum alerta precisar revisao;
- Agente de Configuracao no painel direito.

Nao deve mostrar:

- mensagem para aluno;
- template;
- campanha;
- automacao;
- agente;
- cota;
- log tecnico;
- WhatsApp de aluno.

Referencias:

```text
16_round-4.1S_app-shell_01_base-web.png
08_round-3b1_inputs-formularios-filtros_aprovada.png
09_round-3b2_overlays-feedback_aprovada.png
51B_round-4.1J_onboarding_agente-configuracao-chat-aprovado.png
```

## Imagens Que Herdam Do Setup Inicial

### 1. `/app/configuracoes/studio`

Herda:

```text
51D_round-4.1J_onboarding_bloco-1-studio-aprovado.png
```

Mudancas documentadas:

- shell onboarding vira shell CRM;
- rota vira `/app/configuracoes/studio`;
- stepper some;
- status vira `Publicado` ou `Alteracao manual`;
- CTA vira `Salvar alteracoes` e `Cancelar`;
- Agente de Configuracao explica impacto curto.

### 2. `/app/configuracoes/equipe`

Herda:

```text
51E_round-4.1J_onboarding_bloco-2-equipe-aprovado.png
```

Mudancas documentadas:

- convites preparados viram usuarios reais;
- aparecem status ativo/inativo/convite pendente;
- aparece ultimo acesso;
- aparecem reativar/desativar e reenviar convite;
- link discreto para Permissoes.

### 3. `/app/configuracoes/canais`

Herda:

```text
51F_round-4.1J_onboarding_bloco-3-canais-aprovado.png
```

Mudancas documentadas:

- rascunho vira configuracao publicada;
- aparece status conectado/pendente;
- aparece detalhe tecnico compacto na propria pagina quando houver falha, teste, reconexao ou log necessario;
- textos/templates continuam fora desta pagina.

### 4. `/app/configuracoes/financeiro/modelos`

Herda:

```text
51G_round-4.1J_onboarding_bloco-4-planos-aprovado.png
```

Mudancas documentadas:

- lista mostra planos ativos/inativos;
- mostra alunos usando;
- permite duplicar/inativar;
- mostra impacto da alteracao;
- inclui consumo/reposicao simples por plano:
  - permite reposicao;
  - aviso minimo;
  - prazo para usar reposicao;
  - falta sem aviso;
  - excecao manual permitida ou nao.

## Anexos Base Obrigatorios Por Tipo

### Para imagens proprias de Configuracoes

Usar sempre:

```text
16_round-4.1S_app-shell_01_base-web.png
51B_round-4.1J_onboarding_agente-configuracao-chat-aprovado.png
08_round-3b1_inputs-formularios-filtros_aprovada.png
09_round-3b2_overlays-feedback_aprovada.png
```

### Para paginas herdadas

Usar a imagem de setup correspondente e documentar diferencas, sem gerar imagem nova.

## Decisao Final

Configuracoes Pos-Go-Live precisa de:

- 5 imagens proprias;
- 4 paginas herdadas do Setup Inicial;
- 0 imagens para variacoes de estado neste momento.

Variacoes de estado devem ficar documentadas, nao gerar imagem separada.
