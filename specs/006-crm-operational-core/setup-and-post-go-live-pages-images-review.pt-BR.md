# Revisao De Paginas E Imagens - Setup Inicial E Pos-Go-Live

Status: revisao consolidada v0.1.
Data: 2026-05-14.

## Veredito

A arquitetura faz sentido e esta integrada ao funcionamento do CRM e dos agentes, desde que a fronteira abaixo seja mantida:

- Setup Inicial coloca o studio para operar com seguranca.
- Configuracoes Pos-Go-Live ajustam o sistema ja rodando.
- Agentes/Fluxos configuram automacao profunda.
- Control Planes governam execucao, falha, uso, cota, incidente, log e auditoria.

O setup inicial nao deve virar copia de `/app/configuracoes/*` nem builder de fluxo.

## Regras De Integracao

1. O CRM consome apenas configuracao publicada, default seguro ou snapshot versionado.
2. Rascunho de setup nao muda comportamento operacional.
3. Agente preparado no setup nao significa agente ativo.
4. Canal conectado ou modelo de mensagem pronto nao significa automacao pronta.
5. Toda pendencia pos-go-live precisa virar objeto rastreavel.
6. Dados importados de fonte fisica/informal exigem revisao do dono antes de publicar.
7. Control Planes nao configuram fluxo; apontam para a tela certa quando houver ajuste.

## Setup Inicial - Paginas E Imagens

| Rota | Decisao | Imagem | O que precisa provar |
|---|---|---|---|
| `/onboarding` | Obrigatoria | `51_round-4.1J_onboarding_01_inicio-retomada.png` | Shell proprio de onboarding, retomada, progresso, agente de setup e ajuda Taliya. |
| `/onboarding/diagnostico` | Obrigatoria | `52_round-4.1J_onboarding_02_diagnostico-guiado.png` | Perguntas simples, resumo do diagnostico, caminho adaptativo e chamada Taliya opcional. |
| `/onboarding/setup` | Obrigatoria | `53_round-4.1J_onboarding_03_setup-agente-checklist-impacto.png` | Checklist, agente, formulario contextual, painel de impacto e pendencias rastreaveis. |
| `/onboarding/configuracoes/[area]` | Obrigatoria como padrao reutilizavel | `54_round-4.1J_onboarding_04_configuracao-area.png` | Configuracao por area sem virar pos-go-live completo; previa de impacto, rascunho e validacao. |
| `/onboarding/configuracoes/consumo-aulas` | Obrigatoria propria | `55_round-4.1J_onboarding_05_cobranca-consumo-reposicao.png` | Relacao entre cobranca, direito de aula, consumo, reposicao, excecoes e impacto cruzado. |
| `/onboarding/importacao` | Obrigatoria propria | `56_round-4.1J_onboarding_06_importacao-dados-conflitos.png` | Importacao multimodal, confianca por campo, revisao humana, duplicidades e conflitos. |
| `/onboarding/revisao` | Obrigatoria | `57_round-4.1J_onboarding_07_revisao-publicacao.png` | Revisao + publicacao como experiencia unica: pronto agora, parcial, bloqueado, pendente e configurar depois. |
| `/onboarding/publicacao` | Opcional | Herdada da revisao | So vira rota propria se publicacao tiver muitos estados de validacao, erro ou auditoria. |
| `/onboarding/concluido` | Estado/modal | `58_round-4.1J_onboarding_08_setup-publicado.png` opcional | Sucesso, CRM aberto, pendencias pos-go-live e proximos passos. |

## Setup Inicial - Conteudo Minimo Por Pagina

### `/onboarding`

Deve conter:

- progresso geral;
- proxima etapa recomendada;
- pendencias principais;
- agente de configuracao;
- ajuda Taliya;
- plano Taliya detectado;
- entrada para continuar setup.

Nao deve conter:

- sidebar operacional completa;
- operacao diaria;
- logs, incidentes ou builder de agente.

### `/onboarding/diagnostico`

Deve conter:

- entrevista guiada;
- perguntas sobre agenda, financeiro, dados, WhatsApp, prioridade e plano;
- opcao `nao sei ainda`;
- resumo vivo do diagnostico;
- recomendacao de chamada Taliya quando houver complexidade.

Nao deve conter:

- pergunta tecnica de fluxo;
- modo manual/copiloto/autonomo por fluxo;
- publicacao.

### `/onboarding/setup`

Deve conter:

- checklist de progresso;
- agente + formulario contextual;
- painel de impacto;
- pendencias rastreaveis;
- atalhos para configuracao por area;
- separacao contextual entre `pronto agora` e `configurar depois`.

Nao deve conter:

- configuracao profunda de agentes;
- control planes;
- operacao diaria.

### `/onboarding/configuracoes/[area]`

Areas previstas:

- `studio`;
- `agenda`;
- `financeiro`;
- `canais`;
- `modelos-mensagem`;
- `equipe`;
- `permissoes`;
- `rotinas-operacionais`;
- `regras-seguranca`;
- `agentes`.

Deve conter:

- regras principais da area;
- campos simples;
- previa de impacto;
- pendencias;
- historico simples de rascunho;
- validacao.

Nao deve substituir:

- `/app/configuracoes/*`;
- `/app/agentes/[agentId]/fluxos/[flowId]`;
- `/app/politicas`.

### `/onboarding/configuracoes/consumo-aulas`

Deve conter:

- modelo de cobranca;
- direito de aula;
- regra de consumo;
- credito;
- reposicao;
- inadimplencia;
- excecoes;
- aprovadores;
- exemplos praticos.

Nao deve conter:

- desconto automatico;
- perdao financeiro automatico;
- agente decidindo excecao sozinho.

### `/onboarding/importacao`

Deve aceitar:

- planilha Excel/CSV;
- exportacao de sistema antigo;
- Google Agenda ou agenda externa;
- PDF escaneado;
- foto de caderno, ficha, quadro ou lista impressa;
- print ou lista informal com permissao;
- digitacao manual assistida.

Deve conter:

- origem do dado;
- tipo de dado;
- extracao assistida;
- confianca por campo;
- revisao obrigatoria;
- duplicidades;
- conflitos;
- importacao parcial segura;
- pendencias rastreaveis.

Regra:

- o agente pode ler, sugerir e estruturar;
- o dono revisa;
- o sistema valida;
- so dados aprovados entram.

### `/onboarding/revisao`

Deve conter:

- camadas publicaveis;
- validacao final;
- pronto agora;
- publicado parcialmente;
- pendente seguro;
- configurar depois;
- bloqueado;
- agentes preparados;
- pacotes recomendados em rascunho;
- pendencias com destino;
- confirmacao do gestor.

Camadas:

- CRM manual;
- Agenda;
- Financeiro;
- Canais/modelos de mensagem;
- Regras de seguranca/aprovacoes/excecoes;
- Agentes preparados;
- Pendencias de Agentes/Fluxos pos-go-live.

## Pos-Go-Live - Paginas E Imagens

| Rota | Decisao | Imagem | Observacao |
|---|---|---|---|
| `/app/configuracoes` | Obrigatoria propria | `59_round-4.1J_configuracoes_01_hub-detalhe-secao.png` | Hub pos-go-live com status, secoes, pendencias e detalhe lateral. |
| `/app/configuracoes/studio` | Herdada | Hub + formulario | Dados do studio, unidades, horarios e identidade. |
| `/app/configuracoes/agenda` | Herdada | Configuracao por area | Regras de agenda, aulas, turmas, chamada, no-show e reposicao. |
| `/app/configuracoes/agenda/consumo-aulas` | Pode herdar/expandir | Imagem 55 ou futura propria | Se for muito diferente pos-go-live, gerar variacao depois. |
| `/app/configuracoes/financeiro` | Herdada | Configuracao por area | Regras financeiras do studio, nao billing Taliya. |
| `/app/configuracoes/financeiro/modelos` | Herdada | Consumo/cobranca | Modelos de mensalidade, pacote, avulso e hibrido. |
| `/app/configuracoes/canais` | Herdada | Integracoes/configuracao por area | Preferencia de canal; status tecnico completo fica em Integracoes. |
| `/app/configuracoes/templates` | Herdada | Tabela/lista + drawer | Modelos de mensagem, variaveis, status e aprovacao. |
| `/app/configuracoes/equipe` | Herdada | Tabela/lista + drawer | Usuarios, convites e papeis. |
| `/app/configuracoes/permissoes` | Herdada | 3B.5 governanca | Matriz simples de permissoes. |
| `/app/configuracoes/notificacoes` | Herdada | Configuracao por area | Alertas e preferencias. |
| `/app/agentes` | Necessaria | Pode herdar ou gerar depois | Estado dos agentes, plano 0/1/3/7, responsaveis e saude resumida. |
| `/app/agentes/[agentId]/fluxos` | Necessaria | Pode herdar da imagem 61 | Lista de fluxos, status, modo, risco e ultima publicacao. |
| `/app/agentes/[agentId]/fluxos/[flowId]` | Obrigatoria propria | `61_round-4.1J_agentes-fluxos_01_configurar-simular.png` | Builder/configuracao profunda com modo, limite, fallback, simulacao e publicacao. |
| `/app/politicas` | Obrigatoria propria | `60_round-4.1J_politicas_01_versao-simulacao.png` | Regra versionada, diff, simulacao, aprovacao, publicacao e rollback. |
| `/app/uso` | Obrigatoria propria | `62_round-4.1J_uso-cotas_01_consumo-economia.png` | Cotas, consumo, economia, bloqueios e origem do uso. |
| `/app/controle/execucoes` | Obrigatoria propria | `63_round-4.1J_controle_01_execucoes-incidentes.png` | Trace, ferramenta, custo, bloqueio, retry e fallback. |
| `/app/controle/incidentes` | Herdada da imagem 63 | Mesma familia visual | Incidente, causa, acao segura, tarefa e reprocessamento. |
| `configuracao especifica da integracao` | Herdada | 3B.5 + 3C.3 | Conexao, status, logs, reconexao e jobs. |
| `/app/auditoria` | Herdada | 3C.3 | Logs imutaveis, filtros e detalhe. |
| `/app/billing` | Herdada | 3B.5 | Plano Taliya, faturas, agentes contratados e add-ons. |
| `/app/privacidade/solicitacoes` | Herdada | 3C.3 | Fila sensivel + drawer. |

## Pos-Go-Live - O Que Muda Em Relacao Ao Setup

Pos-go-live pode mostrar:

- diff antes/depois;
- simulacao real;
- rollback;
- versao publicada;
- impacto em fluxos ativos;
- historico;
- auditoria;
- cotas por fluxo;
- modo manual/copiloto/autonomo;
- fallback detalhado;
- preflight;
- logs e incidentes.

Setup inicial nao pode mostrar isso como configuracao principal.

## Revisao De Imagens

### Gerar agora

1. Onboarding inicio/retomada.
2. Diagnostico guiado.
3. Setup agente/checklist/impacto.
4. Configuracao por area.
5. Cobranca/consumo/reposicao.
6. Importacao multimodal.
7. Revisao/publicacao.

### Opcional agora

1. Setup publicado/concluido.
2. `/onboarding/publicacao` separada.

### Gerar depois

1. Hub de configuracoes pos-go-live.
2. Politicas/regras de seguranca.
3. Agentes/Fluxos.
4. Uso/Cotas.
5. Controle execucoes/incidentes.

### Herdar por enquanto

- Studio;
- Equipe;
- Permissoes;
- Notificacoes;
- Templates/modelos de mensagem;
- Integracoes;
- Auditoria;
- Billing;
- Privacidade.

## Ajustes Fechados Nesta Revisao

- Renumerar imagens de onboarding para evitar colisao com Suporte/Internal.
- Tratar `/onboarding/revisao` como revisao + publicacao por padrao.
- Deixar `/onboarding/publicacao` opcional.
- Confirmar importacao multimodal como parte central do setup.
- Exigir confianca por campo e revisao do dono em fonte fisica/informal.
- Manter agente de setup como guia, nao executor/publicador.
- Manter Control Planes fora do setup inicial.
