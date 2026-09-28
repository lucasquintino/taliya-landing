# Prompt Standalone - 51C Area Central De Configuracao Guiada

Status: prompt v0.1 para nova conversa no ChatGPT/Gemini.
Data: 2026-05-14.

## Objetivo

Gerar o asset:

`51C_round-4.1J_onboarding_asset_configuration-workspace.png`

Este asset deve mostrar como a **area central de configuracao guiada** funciona dentro do shell global do Setup Inicial.

Nao e shell vazio.
Nao e checklist/progresso.
Nao e previa de impacto.
Nao e drawer de pendencia.

Ele define o padrao de conteudo central usado em paginas como:

- `/onboarding/configuracoes/[area]`;
- `/onboarding/configuracoes/consumo-aulas`;
- partes do `/onboarding/setup`;
- partes da revisao quando houver configuracao editavel.

## Anexos Necessarios

Enviar estes anexos:

1. `D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/02_round-1_visual-dna-tokens_duplicata.png`
   - Uso: design system Taliya, cores, tipografia, radius, sombras, cards e espacamento.

2. `D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/16_round-4.1S_app-shell_01_base-web.png`
   - Uso: referencia de acabamento e linguagem visual do shell/dashboard aprovado.

3. `D:/Downloads/ChatGPT Image May 14, 2026, 02_39_08 PM.png`
   - Uso: 51A shell global do onboarding aprovado.
   - Manter topbar, stepper, chat lateral e rodape.

4. `D:/Downloads/ChatGPT Image May 14, 2026, 02_19_10 PM.png`
   - Uso: 51B chat lateral aprovado.
   - Manter o agente como chat contextual, sem transformar o chat em area principal.

5. `D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/08_round-3b1_inputs-formularios-filtros_aprovada.png`
   - Uso: campos, seletores, botoes, inputs, toggles e componentes de formulario.

6. `D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/09_round-3b2_overlays-feedback_aprovada.png`
   - Uso: validacoes, avisos inline, estados de feedback e erros leves.

Opcional:

7. `D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/12_round-3b5_sistema-plano-governanca_aprovada.png`
   - Uso: status, badges, pronto agora, pendente seguro e governanca simples.

## Prompt Para Colar No ChatGPT/Gemini

```text
Quero gerar uma imagem para o Taliya CRM.

Nome do arquivo final:
51C_round-4.1J_onboarding_asset_configuration-workspace.png

Objetivo:
Criar a area central de configuracao guiada dentro do shell do Setup Inicial.

Esta imagem deve mostrar como o usuario configura uma area no centro da tela.

Importante:
- Use o shell 51A aprovado.
- Mantenha o chat 51B na lateral direita.
- O foco da imagem e a area central.
- Nao gere shell vazio.
- Nao gere checklist/progresso.
- Nao gere previa de impacto ainda.
- Nao gere drawer de pendencia.

Contexto da pagina:
O dono do studio esta configurando a area "Consumo de aulas".

Essa configuracao inicial deve pedir apenas o necessario para colocar o CRM em operacao com seguranca.
Excecoes complexas, automacoes, cotas, modos de agente e configuracao profunda de fluxos ficam para depois do go-live.

Layout esperado:

1. Manter shell global 51A
- topbar do onboarding;
- stepper lateral esquerdo;
- rodape global;
- chat lateral direito do agente;
- pendencias globais no rodape, nao dentro do chat.

2. Area central preenchida com workspace de configuracao

Cabecalho da area:
- titulo: "Consumo de aulas";
- subtitulo: "Defina como mensalidades, pacotes e reposicoes funcionam no setup inicial.";
- status discreto: "Rascunho";
- texto curto: "Ajustes finos podem ficar para depois do go-live."

3. Bloco "Modelo principal"
Mostrar escolha clara entre:
- "Mensalidade";
- "Pacote de aulas";
- "Hibrido".

O estado selecionado deve ser "Pacote de aulas".

4. Bloco "Pacote base"
Campos/controles:
- "Aulas por mes": valor 8;
- "Validade": "mensal";
- "Renova automaticamente": toggle ligado;
- "Saldo expira no fim do ciclo": toggle ligado ou estado selecionado.

5. Bloco "Reposicoes"
Campos/controles:
- "Permitir reposicao": toggle ligado;
- "Prazo para usar reposicao": 7 dias;
- "Aviso minimo para gerar reposicao": 12h;
- "Reposicao consome vaga da turma": toggle ligado.

6. Bloco "Excecoes simples"
Mostrar uma lista curta com estados inline:
- "Feriados": badge "Pode ficar para depois";
- "Contratos antigos": badge "Revisar depois";
- "Faltas sem aviso": valor "Nao gera reposicao".

Essas excecoes devem aparecer como linhas leves dentro da propria pagina, nao como drawer.

7. Bloco de validacao inline
Mostrar um aviso leve, nao alarmista:
"Esta regra base pode ser salva como rascunho. Feriados e contratos antigos podem ficar como pendencia segura."

8. Acoes da etapa
Mostrar botoes:
- botao primario: "Salvar rascunho";
- botao secundario: "Continuar";
- botao discreto: "Configurar depois".

9. Slot reservado para impacto
Incluir uma area discreta abaixo ou ao lado dizendo:
"Previa de impacto entra aqui"

Esse slot deve indicar onde o 51D sera encaixado depois, mas nao deve mostrar ainda a previa completa.

Direcao visual:
- seguir design system Taliya;
- usar shell 51A aprovado;
- manter chat 51B integrado na direita;
- area central clara, densa e escaneavel;
- componentes de formulario com bom espacamento;
- cards leves, bordas finas, sombras discretas;
- preto suave para texto;
- azul apenas como acento;
- verde com moderacao para estados ok;
- amarelo/laranja leve para "pode ficar para depois";
- nao usar vermelho forte;
- nao parecer dashboard;
- nao parecer landing page;
- nao parecer formulario tecnico demais.

Nao mostrar:
- palavra "Simulacao";
- checklist/progresso de setup no centro;
- drawer de pendencia;
- previa de impacto completa;
- logs;
- traces;
- incidentes;
- Control Planes;
- builder de fluxo;
- modo manual/copiloto/autonomo por fluxo;
- cotas;
- agente ativo/rodando;
- publicacao automatica;
- upload dentro do chat;
- pendencias dentro do chat;
- pergunta "Por onde voce quer comecar?".

Resultado esperado:
Uma tela 16:9 usando o shell de onboarding aprovado, com a area central mostrando uma configuracao guiada de "Consumo de aulas" pronta para ser salva como rascunho. A imagem deve deixar claro como o usuario configura, onde aparecem validacoes inline, como excecoes simples ficam na propria tela e onde a futura Previa de impacto sera encaixada.
```

## Criterios De Aprovacao

A imagem pode ser aprovada se:

- mostra o 51A com centro preenchido, nao shell vazio;
- o centro mostra configuracao guiada realista;
- o chat 51B continua lateral e contextual;
- nao vira checklist/progresso;
- nao mostra previa de impacto completa;
- pendencias simples aparecem inline;
- acoes da etapa estao claras;
- existe slot para o futuro 51D;
- a configuracao parece inicial e segura, nao pos-go-live avancada.
