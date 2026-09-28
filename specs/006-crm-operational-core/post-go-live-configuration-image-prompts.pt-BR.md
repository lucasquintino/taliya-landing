# Taliya CRM - Plano De Imagens Para Configuracoes Pos-Go-Live

Status: plano v1.
Data: 2026-05-24.

## Objetivo

Registrar quais imagens devem ser geradas para Configuracoes Pos-Go-Live e quais paginas devem herdar imagens do Setup Inicial.

Este arquivo nao substitui os prompts individuais. Os prompts finais devem ser criados uma pagina por vez, no mesmo processo usado em Agentes/Rotinas/Fluxos.

Fonte funcional:

- `post-go-live-configuration-master-map.pt-BR.md`

Fonte visual:

- `post-go-live-configuration-visual-inheritance-audit.pt-BR.md`

## Shell Obrigatorio

Todas as imagens proprias de Configuracoes usam o shell CRM padrao:

```text
16_round-4.1S_app-shell_01_base-web.png
```

Regras:

- preservar browser frame, logo Taliya, rail lateral, topbar, busca, mensagens, notificacoes e avatar;
- destacar o icone de configuracoes no rail esquerdo;
- usar layout claro, denso, operacional e sem decoracao desnecessaria;
- usar Agente de Configuracao apenas nas paginas internas onde o usuario esta configurando algo;
- nao usar Agente de Configuracao no hub `/app/configuracoes`;
- nao criar dashboard, historico, atividade recente, metricas ou painel lateral vazio.

## Imagens Proprias Necessarias

### 1. Hub De Configuracoes

Rota:

```text
/app/configuracoes
```

Nome sugerido:

```text
60_round-4.1M_configuracoes_01_hub-8-cards-aprovado.png
```

Conteudo:

- 8 cards sem secoes;
- Studio;
- Equipe;
- Permissoes;
- Canais;
- Planos e modelos;
- Pagamentos e financeiro;
- Agenda;
- Notificacoes.

Imagem aprovada:

```text
60_round-4.1M_configuracoes_01_hub-8-cards-aprovado.png
```

Nao mostrar:

- Agente de Configuracao;
- painel direito;
- filtros;
- historico;
- atividade recente;
- metricas.

### 2. Permissoes

Rota:

```text
/app/configuracoes/permissoes
```

Nome sugerido:

```text
61_round-4.1M_configuracoes_02_permissoes-aprovado.png
```

Conteudo:

- Dono/Admin;
- Recepcao;
- Professor;
- permissao padrao de cada papel;
- ajustes sensiveis;
- resumo de impacto;
- Agente de Configuracao.

Imagem aprovada:

```text
61_round-4.1M_configuracoes_02_permissoes-aprovado.png
```

Anexos recomendados:

```text
16_round-4.1S_app-shell_01_base-web.png
12_round-3b5_sistema-plano-governanca_aprovada.png
08_round-3b1_inputs-formularios-filtros_aprovada.png
51B_round-4.1J_onboarding_agente-configuracao-chat-aprovado.png
```

### 3. Pagamentos E Financeiro

Rota:

```text
/app/configuracoes/financeiro/pagamentos
```

Nome sugerido:

```text
62_round-4.1M_configuracoes_03_pagamentos-financeiro-aprovado.png
```

Status:

```text
Aprovada em 2026-05-24.
```

Arquivo canonico:

```text
D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\62_round-4.1M_configuracoes_03_pagamentos-financeiro-aprovado.png
```

Conteudo:

- meios e baixa manual;
- regras financeiras simples;
- Pagamentos Taliya;
- link discreto para Integracoes quando houver falha tecnica;
- Agente de Configuracao.

Regras obrigatorias para prompt:

- comprovante nao e meio de pagamento;
- comprovante deve aparecer apenas como detalhe da baixa manual, sem bloco proprio;
- nao criar bloco final de impacto;
- planos nao escolhem meio de pagamento;
- depois de ativar Pagamentos Taliya, a pagina troca CTA de ativacao por preferencias/gerenciamento;
- meios manuais continuam disponiveis mesmo com Pagamentos Taliya ativo.

Anexos recomendados:

```text
16_round-4.1S_app-shell_01_base-web.png
51K_round-4.1J_onboarding_bloco-5-pagamento-aprovado.png
30_round-4.1F_financeiro_01_visao-geral-filas.png.png
34_round-4.1F_financeiro_04_movimentacoes-filtros-drawer.png.png
51B_round-4.1J_onboarding_agente-configuracao-chat-aprovado.png
```

### 4. Agenda

Rota:

```text
/app/configuracoes/agenda
```

Nome sugerido:

```text
63_round-4.1M_configuracoes_04_agenda-aprovado.png
```

Conteudo:

- dias fechados e excecoes;
- bloqueios temporarios;
- regras simples da agenda;
- impacto em aulas futuras somente dentro do item afetado, quando necessario;
- Agente de Configuracao.

Imagem aprovada:

```text
63_round-4.1M_configuracoes_04_agenda-aprovado.png
```

Nao mostrar:

- resumo de impacto;
- calendario operacional completo;
- grade semanal completa;
- pagamento;
- reposicao detalhada;
- fluxo de agente.

Anexos recomendados:

```text
16_round-4.1S_app-shell_01_base-web.png
51J_round-4.1J_onboarding_bloco-7-agenda-aprovado.png
26_round-4.1F_agenda_01_calendario-operacional.png.png
36_round-4.1F_grade_01_semana-modelo-bloqueio.png.png
51B_round-4.1J_onboarding_agente-configuracao-chat-aprovado.png
```

### 5. Notificacoes

Rota:

```text
/app/configuracoes/notificacoes
```

Nome sugerido:

```text
64_round-4.1M_configuracoes_05_notificacoes-aprovado.png
```

Conteudo:

- alertas por papel;
- tipos de alerta;
- frequencia;
- canais internos da equipe;
- WhatsApp interno significa WhatsApp da equipe, nao WhatsApp do aluno;
- silenciar alerta nao critico fora do horario;
- status geral quando algum alerta precisar revisao;
- Agente de Configuracao.

Imagem aprovada:

```text
64_round-4.1M_configuracoes_05_notificacoes-aprovado.png
```

Observacoes da imagem aprovada:

- `Nao critico` pode continuar ligado e, ao mesmo tempo, silenciado fora do horario;
- `Revisar 1 alerta` e apenas status geral da configuracao;
- nao gerar resumo de impacto, historico, template, automacao, cota, log tecnico ou mensagem para aluno.

Anexos recomendados:

```text
16_round-4.1S_app-shell_01_base-web.png
08_round-3b1_inputs-formularios-filtros_aprovada.png
09_round-3b2_overlays-feedback_aprovada.png
51B_round-4.1J_onboarding_agente-configuracao-chat-aprovado.png
```

## Paginas Que Herdam Imagem Do Setup Inicial

Estas paginas tem rota propria, mas nao precisam de imagem nova agora:

| Pagina | Herda de |
|---|---|
| `/app/configuracoes/studio` | `51D_round-4.1J_onboarding_bloco-1-studio-aprovado.png` |
| `/app/configuracoes/equipe` | `51E_round-4.1J_onboarding_bloco-2-equipe-aprovado.png` |
| `/app/configuracoes/canais` | `51F_round-4.1J_onboarding_bloco-3-canais-aprovado.png` |
| `/app/configuracoes/financeiro/modelos` | `51G_round-4.1J_onboarding_bloco-4-planos-aprovado.png` |

## Paginas Removidas Como Imagem/Rota Propria

Nao gerar imagem para:

| Pagina antiga | Motivo |
|---|---|
| `/app/configuracoes/agenda/consumo-aulas` | Foi incorporada em `Planos e modelos` |
| `/app/configuracoes/financeiro` | Foi incorporada em `Pagamentos e financeiro` |

## Status Das Imagens

1. Hub com 8 cards - aprovada.
2. Permissoes - aprovada.
3. Pagamentos e financeiro - aprovada.
4. Agenda - aprovada.
5. Notificacoes - aprovada.

Cada prompt deve ser escrito do zero para a pagina atual, sem reutilizar prompts antigos da versao de 10 cards.
