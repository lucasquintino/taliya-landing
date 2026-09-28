# Setup Inicial - Mapa De Imagens E Componentes Reutilizaveis

Status: plano visual v0.2.
Data: 2026-05-14.

## Objetivo

Antes de gerar as imagens finais das paginas do Setup Inicial, gerar e aprovar os blocos visuais reutilizaveis.

Os prompts completos para gerar estes assets estao em `setup-reusable-visual-assets-prompts.pt-BR.md`.

Esses blocos devem funcionar como base para:

- `/onboarding`;
- `/onboarding/diagnostico`;
- `/onboarding/setup`;
- `/onboarding/configuracoes/[area]`;
- `/onboarding/configuracoes/consumo-aulas`;
- `/onboarding/importacao`;
- `/onboarding/revisao`;
- estados opcionais de publicacao/conclusao.

## Regra Central

O setup inicial usa shell proprio de onboarding.

Nao usar:

- sidebar operacional completa do CRM;
- navegacao principal do app;
- widgets de Hoje/Inbox/Financeiro operacional;
- control planes;
- builder de fluxo;
- logs/traces/incidentes.

O onboarding deve parecer uma experiencia guiada, leve e focada em colocar o studio em operacao com seguranca.

## Ordem Recomendada De Geracao

Gerar primeiro:

1. Shell base do onboarding.
2. Kit de componentes do agente de configuracao.
3. Padrao de formulario guiado por area.
4. Primeira tela real do setup: Bloco 1 Studio.
5. Padrao de importacao/revisao de dados, se uma pagina futura exigir.
6. Padrao de revisao/publicacao.

Status de telas reais aprovadas:

- `51D_round-4.1J_onboarding_bloco-1-studio-aprovado.png`: Bloco 1 - Studio.
- `51E_round-4.1J_onboarding_bloco-2-equipe-aprovado.png`: Bloco 2 - Equipe.
- `51F_round-4.1J_onboarding_bloco-3-canais-aprovado.png`: Bloco 3 - Canais.
- `51G_round-4.1J_onboarding_bloco-4-planos-aprovado.png`: Bloco 4 - Planos.
- `51K_round-4.1J_onboarding_bloco-5-pagamento-aprovado.png`: Bloco 5 - Pagamento aprovado.
- `51H_round-4.1J_onboarding_bloco-5-alunos-aprovado.png`: padrao visual de Alunos, agora Bloco 6 oficial.
- `51I_round-4.1J_onboarding_bloco-6-turmas-aprovado.png`: padrao visual de Turmas, agora Bloco 7 oficial.
- `51J_round-4.1J_onboarding_bloco-7-agenda-aprovado.png`: padrao visual de Agenda, agora Bloco 8 oficial.
- `51L_round-4.1J_onboarding_bloco-9-revisao-aprovado.png`: Bloco 9 - Revisao aprovado.

Regra de stepper/progresso: usar a sequencia oficial de 9 blocos documentada em `setup-stepper-progress-9-blocks.pt-BR.md`. As imagens `51H`, `51I` e `51J` nao precisam ser regeradas apenas por mostrarem numeracao antiga.

Depois gerar as paginas finais usando esses blocos como anexos/referencias.

## Imagens Base Reutilizaveis

### `51A_round-4.1J_onboarding_shell-global-aprovado.png`

Uso: todas as paginas do setup.

Status: aprovado em `setup-51A-shell-base-approved.pt-BR.md`.

Mostra:

- topo simples com marca Taliya;
- nome do studio;
- status do setup;
- progresso geral;
- acao de ajuda Taliya;
- stepper/checklist lateral esquerdo de etapas do onboarding;
- area central livre, sem conteudo especifico de pagina;
- slots neutros para conteudo futuro da etapa atual;
- painel lateral direito do agente integrado como chat contextual, seguindo o 51B aprovado;
- rodape global discreto de setup/rascunhos/pendencias;
- sem sidebar operacional do CRM.

Decisoes visuais:

- deve herdar DNA visual Taliya;
- deve ser mais simples que o app shell operacional;
- deve ser uma casca global reutilizavel, nao uma pagina final;
- deve ter sensacao de onboarding guiado, nao dashboard operacional;
- deve reservar espaco para formularios, tabelas, importacao, revisao e impacto em variacoes futuras;
- deve encaixar o chat lateral do agente sem transformar a lateral direita em painel de cards.

Nao mostrar:

- menu Hoje/Agenda/Financeiro/Inbox;
- conteudo real de uma etapa;
- formulario preenchido;
- cards de impacto/pedencias como conteudo final;
- lista de proximos passos do agente;
- pergunta `Por onde voce quer comecar?`;
- graficos de operacao;
- tabelas densas;
- agentes ativos;
- logs.

### `51B_round-4.1J_onboarding_agente-configuracao-chat-aprovado.png`

Uso: todas as paginas.

Status: aprovado conceitualmente em `setup-51B-agent-chat-approved.pt-BR.md`.

Mostra:

- agente de configuracao como chat/copiloto lateral;
- mensagens curtas e contextuais sobre a etapa atual;
- alerta ou sugestao principal, quando houver;
- acoes rapidas embutidas na conversa;
- campo para perguntar sobre a etapa;
- ajuda humana Taliya discreta;
- indicador de que o agente guia, prepara rascunhos e alerta, mas nao publica sozinho.

Estados possiveis do componente:

- orientando;
- explicando impacto;
- encontrou pendencia;
- recomenda chamada Taliya;
- aguardando revisao do dono.

Esses estados nao devem aparecer todos ao mesmo tempo. O asset 51B deve mostrar o estado base `orientando`, com um exemplo leve de alerta/impacto. As outras variacoes podem ser derivadas depois se necessario.

O painel nao deve conter:

- pergunta oficial da etapa se essa pergunta ja estiver no centro;
- formulario principal;
- lista completa de etapas;
- lista fixa de "proximos passos" competindo com a sequencia do onboarding;
- grade grande de estados do agente;
- card institucional explicando quem e o agente.

Nao mostrar:

- agente como executor autonomo;
- agente publicando configuracao;
- agente resolvendo dado duvidoso sem confirmacao.

### `51C_round-4.1J_onboarding_workspace-configuracao-aprovado.png`

Uso: `/onboarding/configuracoes/[area]`, `/onboarding/configuracoes/consumo-aulas`, partes de `/onboarding/setup` e revisao com configuracao editavel.

Mostra a area central de configuracao guiada dentro do shell 51A.

Exemplo base: `Consumo de aulas`.

Deve mostrar:

- cabecalho da area;
- status de rascunho;
- blocos de configuracao;
- campos, seletores e toggles;
- validacoes inline;
- excecoes simples na propria tela;
- acoes da etapa;
- slot reservado para `Previa de impacto`.

Nao deve mostrar:

- checklist/progresso do setup;
- drawer de pendencia;
- previa de impacto completa;
- configuracao profunda de agentes;
- cotas;
- modo manual/copiloto/autonomo;
- logs ou control planes.

### `51D_round-4.1J_onboarding_bloco-1-studio-aprovado.png`

Uso: `/onboarding/setup`, Bloco 1 - Studio.

Status: aprovado em `setup-51D-bloco-1-studio-approved.pt-BR.md`.

Mostra:

- primeira tela real do setup dentro do shell 51A;
- Bloco 1 de 8: `Studio`;
- campo `Nome do studio`;
- dias de funcionamento;
- horario geral;
- pausa;
- janela semanal de funcionamento em grade visual;
- `Ajustar horarios por dia` dentro do card da janela semanal;
- agente lateral explicando que esses horarios ainda nao criam aulas.

Decisoes:

- chamar a previa de `Janela semanal de funcionamento`, nao agenda;
- nao mostrar aulas, turmas, alunos, planos ou importacao;
- manter a grade visual como impacto imediato da configuracao;
- abrir ajuste por dia em drawer/modal simples, nao expandir tabela grande na tela principal.

Arquivo consolidado:

`D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\51D_round-4.1J_onboarding_bloco-1-studio-aprovado.png`

### Previa De Impacto Standalone

Status: nao gerar agora.

Motivo: o 51C aprovado ja define como a configuracao acontece na area central e reserva espaco para impacto quando necessario. A previa de impacto deve ser desenhada dentro das paginas finais ou componentes especificos, sem criar asset intermediario obrigatorio neste momento.

### Pendencias Detalhadas / Drawer

Status: nao gerar agora.

Motivo: pendencias simples devem aparecer na propria tela, perto do campo ou configuracao que falta. Pendencias globais aparecem no rodape do shell. Quando houver necessidade de detalhe, usar padroes herdados de drawer/modal ja aprovados, sem criar asset proprio agora.

Atualizacao 2026-05-15: a identificacao `51E` passou a ser usada para a segunda tela real aprovada do setup, `Bloco 2 - Equipe`, documentada em `setup-51E-bloco-2-equipe-approved.pt-BR.md`.

### Ajuda Taliya / Modal De Agendamento

Uso: `/onboarding`, `/onboarding/diagnostico`, `/onboarding/setup`, paginas de area, revisao.

Status: nao gerar agora.

Atualizacao 2026-05-15: a identificacao `51F` passou a ser usada para a terceira tela real aprovada do setup, `Bloco 3 - Canais`, documentada em `setup-51F-bloco-3-canais-approved.pt-BR.md`.

Atualizacao 2026-05-15: a identificacao `51G` passou a ser usada para a quarta tela real aprovada do setup, `Bloco 4 - Planos`, documentada em `setup-51G-bloco-4-planos-approved.pt-BR.md`.

Atualizacao 2026-05-15: a identificacao `51H` passou a ser usada para a quinta tela real aprovada do setup, `Bloco 5 - Alunos`, documentada em `setup-51H-bloco-5-alunos-approved.pt-BR.md`.

Atualizacao 2026-05-15: a identificacao `51I` passou a ser usada para a sexta tela real aprovada do setup, `Bloco 6 - Turmas`, documentada em `setup-51I-bloco-6-turmas-approved.pt-BR.md`.

Atualizacao 2026-05-15: a identificacao `51J` passou a ser usada para a setima tela real aprovada do setup, `Bloco 7 - Agenda`, documentada em `setup-51J-bloco-7-agenda-approved.pt-BR.md`.

Regra atualizada: o Bloco 7 nao importa agenda, Google Agenda, planilhas ou fotos. Qualquer dado externo usado para descobrir alunos, turmas, horarios ou vinculos entra antes, nos Blocos 5 e 6.

Mostra:

- card compacto de ajuda Taliya;
- modal/drawer de agendamento;
- horario;
- link de chamada;
- resumo para especialista;
- pendencias que devem ser discutidas;
- anotacoes/recomendacoes.

Estados:

- sem chamada;
- chamada recomendada;
- chamada agendada;
- em revisao com Taliya;
- anotacoes recebidas.

Regra:

- humano Taliya orienta dentro do fluxo;
- nao configura por fora.

## Componentes Reutilizaveis De Formulario

### `52A_round-4.1J_onboarding_component_guided-question-card.png`

Uso: diagnostico, setup e configuracoes por area.

Mostra:

- pergunta simples;
- opcoes de resposta;
- `Nao sei ainda`;
- exemplo;
- impacto da resposta;
- campo livre quando necessario.

Estados:

- respondida;
- nao sei ainda;
- resposta incompleta;
- resposta gera pendencia;
- resposta recomenda ajuda Taliya.

### `52B_round-4.1J_onboarding_component_area-rule-card.png`

Uso: configuracoes por area.

Mostra:

- nome da regra;
- status;
- valor atual em rascunho;
- impacto resumido;
- responsavel;
- acao `Editar`;
- acao `Marcar para depois`.

Estados:

- rascunho;
- pronto;
- pronto parcialmente;
- pendente seguro;
- bloqueado;
- sensivel.

### `52C_round-4.1J_onboarding_component_before-after-impact.png`

Uso: consumo de aulas, regras de seguranca, revisao.

Mostra:

- antes;
- depois;
- exemplo pratico;
- area afetada;
- alerta se houver risco.

Nao chamar de simulacao.

## Componentes Reutilizaveis De Importacao

### `53A_round-4.1J_onboarding_import_source-selector.png`

Uso: `/onboarding/importacao`.

Mostra opcoes:

- importar planilha;
- conectar Google Agenda;
- enviar foto ou PDF;
- digitar manualmente;
- comecar sem importar.

Cada opcao deve ter:

- tipo de origem;
- o que pode extrair;
- nivel esperado de revisao;
- aviso de privacidade quando necessario.

### `53B_round-4.1J_onboarding_import_confidence-table.png`

Uso: `/onboarding/importacao`.

Mostra tabela de revisao com:

- dado encontrado;
- origem;
- confianca;
- sugestao do sistema;
- campo editavel;
- status.

Estados de confianca:

- alta;
- precisa revisar;
- nao entendi;
- conflito;
- duplicidade provavel;
- dado sensivel.

### `53C_round-4.1J_onboarding_import_conflict-drawer.png`

Uso: `/onboarding/importacao`.

Mostra detalhe de:

- duplicidade;
- telefone compartilhado;
- aluno sem turma;
- turma sem horario;
- plano sem valor;
- status financeiro incerto;
- nome ilegivel;
- informacao contraditoria.

Acoes:

- aceitar sugestao;
- editar;
- mesclar;
- manter separado;
- criar pendencia;
- descartar.

## Componentes Reutilizaveis De Agentes No Setup

### `54A_round-4.1J_onboarding_agent-prepared-card.png`

Uso: `/onboarding/setup`, `/onboarding/configuracoes/agentes`, `/onboarding/revisao`.

Mostra:

- agente incluso no plano;
- dominio;
- responsavel humano;
- status `preparado`;
- pacotes recomendados em rascunho;
- destino pos-go-live.

Estados:

- nao incluso no plano;
- incluido mas nao preparado;
- preparado;
- rascunhos criados;
- pendente para Agentes/Fluxos;
- manual por enquanto.

Nao mostrar:

- ativo;
- rodando;
- autonomo;
- copiloto publicado;
- fluxo publicado.

### `54B_round-4.1J_onboarding_agent-package-draft-row.png`

Uso: paginas de agentes e revisao.

Mostra:

- pacote recomendado;
- area;
- motivo;
- responsavel;
- status rascunho/pendente;
- destino `/app/agentes/[agentId]/fluxos`;
- porque fica para depois.

## Componentes Reutilizaveis De Revisao/Publicacao

### `55A_round-4.1J_onboarding_review-layer-summary.png`

Uso: `/onboarding/revisao`.

Mostra camadas:

- CRM manual;
- Agenda;
- Financeiro;
- Canais/modelos de mensagem;
- Regras de seguranca/aprovacoes/excecoes;
- Agentes preparados;
- Pendencias de Agentes/Fluxos pos-go-live.

Estados:

- pronto agora;
- publicado parcialmente;
- pendente seguro;
- configurar depois;
- bloqueado;
- revisar com Taliya.

### `55B_round-4.1J_onboarding_publish-confirmation-modal.png`

Uso: `/onboarding/revisao` e opcional `/onboarding/publicacao`.

Mostra:

- o que sera publicado;
- o que nao sera publicado;
- pendencias rastreaveis;
- confirmacao do gestor;
- auditoria.

Estados:

- aguardando confirmacao;
- publicando;
- publicado;
- publicado parcialmente;
- falhou.

### `55C_round-4.1J_onboarding_success-state.png`

Uso: modal/estado de conclusao.

Mostra:

- setup publicado;
- CRM pronto;
- pendencias seguras;
- proximos passos;
- abrir CRM;
- ver pendencias pos-go-live;
- agendar ajuda Taliya.

## O Que Precisa De Imagem Propria Antes Das Paginas

Essenciais:

1. `51A` Shell base do onboarding.
2. `51B` Chat lateral do agente de configuracao.
3. `51C` Area central de configuracao guiada.
4. `53A` Seletor de fonte de importacao.
5. `53B` Tabela de confianca por campo.
6. `54A` Card de agente preparado.
7. `55A` Resumo de camadas de revisao/publicacao.

Podem ser gerados depois ou aparecer dentro das paginas finais:

- ajuda Taliya/modal de agendamento;
- `52A` pergunta guiada;
- `52B` card de regra por area;
- `52C` antes/depois;
- `53C` conflito de importacao;
- `54B` linha de pacote recomendado;
- `55B` confirmacao de publicacao;
- `55C` sucesso.

## Reaproveitamento Por Pagina

| Pagina | Assets obrigatorios |
|---|---|
| `/onboarding` | 51A, 51B, ajuda Taliya quando necessario |
| `/onboarding/diagnostico` | 51A, 51B, 52A |
| `/onboarding/setup` | 51A, 51B, 51C, 52A, 54A |
| `/onboarding/configuracoes/[area]` | 51A, 51B, 51C, 52A, 52B |
| `/onboarding/configuracoes/consumo-aulas` | 51A, 51B, 51C, 52B, 52C |
| `/onboarding/importacao` | 51A, 51B, 53A, 53B, 53C |
| `/onboarding/revisao` | 51A, 51B, 54A, 54B, 55A, 55B |
| Conclusao/modal | 51A, 51B, 55C |

## Prompt Base Para Gerar Assets

Todo prompt deve dizer:

- isto e um asset reutilizavel, nao uma pagina final;
- usar shell proprio de onboarding;
- nao usar sidebar operacional do CRM;
- nao mostrar agente ativo/rodando;
- nao mostrar builder de fluxo;
- nao mostrar logs/incidentes/control planes;
- usar linguagem operacional simples;
- deixar espaco para variacoes futuras;
- manter DNA visual Taliya.

## Sequencia Recomendada No ChatGPT

1. Usar o `51B` aprovado como referencia do comportamento do agente.
2. Revisar ou regerar `51A` shell base para encaixar o chat lateral contextual, sem painel de cards do agente.
3. Gerar `51C` Area central de configuracao guiada usando `51A` e `51B`.
4. Gerar assets de importacao `53A` e `53B`, usando `51A` e `51B`.
5. Gerar `54A` agente preparado.
6. Gerar `55A` revisao/publicacao.
7. So depois gerar as paginas finais `51-57`.

## Criterio De Aceite

Os assets estao prontos quando:

- o shell de onboarding nao parece o CRM operacional;
- o agente parece guia, nao executor;
- pendencias sao rastreaveis;
- importacao fisica/informal mostra confianca por campo;
- agentes aparecem como preparados, nao ativos;
- revisao separa claramente pronto agora, parcial, pendente e configurar depois;
- qualquer pagina final consegue reutilizar os assets sem redesenhar a arquitetura.
