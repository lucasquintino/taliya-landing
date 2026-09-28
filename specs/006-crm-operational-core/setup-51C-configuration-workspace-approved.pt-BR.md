# Setup Inicial - 51C Area Central De Configuracao Guiada Aprovada

> Status: aprovado v0.2. Imagem de referencia: `51C_round-4.1J_onboarding_workspace-configuracao-aprovado.png`.

## Arquivo

Arquivo canonico:

`D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\51C_round-4.1J_onboarding_workspace-configuracao-aprovado.png`

Arquivo local observado:

`D:\Downloads\ChatGPT Image May 14, 2026, 04_03_12 PM.png`

Arquivo consolidado em pasta nomeada:

`D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\51C_round-4.1J_onboarding_workspace-configuracao-aprovado.png`

## Objetivo Da Imagem

Validar como a **area central de configuracao guiada** funciona dentro do shell global do Setup Inicial.

Esta imagem nao define todas as configuracoes do produto. Ela usa **Consumo de aulas** como exemplo visual para provar o padrao de configuracao no centro da tela.

O inventario funcional completo continua em:

- [setup-configuration-inventory.pt-BR.md](./setup-configuration-inventory.pt-BR.md)
- [setup-onboarding-question-map.pt-BR.md](./setup-onboarding-question-map.pt-BR.md)
- [setup-configuration-plan-100.pt-BR.md](./setup-configuration-plan-100.pt-BR.md)

## Decisao Principal

O 51C define o padrao de conteudo central usado dentro do shell 51A.

Ele deve mostrar:

- cabecalho da area configurada;
- status de rascunho;
- blocos de configuracao;
- campos, seletores, toggles e opcoes;
- validacoes inline;
- excecoes simples na propria tela;
- acoes da etapa;
- espaco para impacto quando a pagina precisar.

Ele nao deve virar:

- checklist/progresso do setup;
- drawer de pendencia;
- dashboard;
- tela de publicacao final;
- configuracao pos-go-live avancada.

## Estrutura Aprovada

### Shell

A imagem usa corretamente:

- 51A como shell global;
- stepper lateral esquerdo;
- topbar de setup;
- rodape global;
- 51B como chat lateral contextual.

### Area Central

O exemplo aprovado usa a area `Consumo de aulas`.

Conteudos aprovados:

- titulo `Consumo de aulas`;
- status `Rascunho`;
- texto curto explicando que ajustes finos podem ficar para depois do go-live;
- bloco `Modelo principal`;
- bloco `Pacote base`;
- bloco `Reposicoes`;
- bloco `Excecoes simples`;
- bloco `Validacao da configuracao`;
- acoes da etapa.

### Modelo Principal

Padrao aprovado:

- `Mensalidade`;
- `Pacote de aulas`;
- `Hibrido`;
- estado selecionado destacado.

### Campos E Controles

Padrao aprovado:

- campos numericos;
- selects;
- toggles;
- cards selecionaveis;
- badges leves;
- validacao inline.

### Excecoes Simples

As excecoes simples devem aparecer na propria tela, perto da configuracao.

Exemplos aprovados:

- `Feriados` com `Pode ficar para depois`;
- `Contratos antigos` com `Revisar depois`;
- `Faltas sem aviso` com valor direto.

Regra: excecoes simples nao precisam abrir drawer proprio neste momento.

### Validacao Inline

Padrao aprovado:

> "Esta regra base pode ser salva como rascunho. Feriados e contratos antigos podem ficar como pendencia segura."

Essa validacao deve ser clara, calma e acionavel, sem parecer erro critico.

### Acoes Da Etapa

Acoes aprovadas:

- `Salvar rascunho`;
- `Continuar`;
- `Configurar depois`.

Regra: `Salvar rascunho` nao significa publicar.

## Relacao Com Previa De Impacto

A imagem incluiu um slot para `Previa de impacto`, mas a decisao atual e **nao gerar uma previa de impacto standalone como asset separado**.

Motivo:

- o 51C ja prova como a configuracao acontece no centro;
- a previa de impacto pode ser desenhada dentro das paginas finais quando for necessaria;
- gerar uma imagem intermediaria so para impacto criaria mais uma referencia sem necessidade;
- o comportamento de impacto ja esta representado como espaco/slot e validacao inline no 51C.

Decisao:

- a previa de impacto standalone nao sera gerada agora;
- `51D` passou a identificar outra referencia aprovada: o Bloco 1 Studio, documentado em `setup-51D-bloco-1-studio-approved.pt-BR.md`;
- impactos devem ser tratados dentro das paginas finais ou dentro de componentes especificos quando a pagina pedir;
- o 51C continua sendo o padrao central para areas de configuracao.

## Ajustes Registrados Para Proximas Imagens

- No chat lateral, para `Consumo de aulas`, preferir mensagem mais especifica: `Esta etapa afeta agenda, saldo de aulas e reposicoes.`
- Em paginas finais, substituir `Configuracoes` no stepper pela macroetapa correta quando fizer sentido.
- Manter pendencias globais no rodape/drawer, nao no chat.
- Manter excecoes simples inline quando nao exigirem detalhe.
- Nao tratar este exemplo como contrato unico de Consumo de aulas.

## O Que Foi Rejeitado

Nao usar no 51C:

- checklist/progresso de setup no centro;
- previa de impacto completa como asset separado obrigatorio;
- drawer de pendencia;
- logs;
- traces;
- incidentes;
- Control Planes;
- builder de fluxo;
- modo manual/copiloto/autonomo por fluxo;
- cotas;
- agente ativo/rodando;
- publicacao automatica.

## Criterio De Aceite

O 51C esta correto quando:

- mostra como o usuario configura no centro;
- usa o shell 51A corretamente;
- mantem o agente 51B como apoio lateral;
- apresenta campos e controles claros;
- permite salvar rascunho;
- mostra validacao inline;
- trata excecoes simples sem complexidade desnecessaria;
- deixa claro que configuracoes profundas ficam para depois.
