# Setup Inicial - 51F Bloco 3 Canais Aprovado

> Status: aprovado v0.1. Imagem de referencia: `51F_round-4.1J_onboarding_bloco-3-canais-aprovado.png`.

## Arquivo

Arquivo canonico:

`D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\51F_round-4.1J_onboarding_bloco-3-canais-aprovado.png`

Arquivo local observado:

`D:\Downloads\ChatGPT Image May 15, 2026, 09_43_48 AM.png`

## Objetivo Da Imagem

Validar o terceiro bloco real de configuracao dentro de `/onboarding/setup`: **Canais**.

Esta imagem representa o cadastro dos canais oficiais e publicos do studio no Setup Inicial. Ela nao representa configuracao tecnica profunda de WhatsApp, provedor, templates, automacao, inbox social ou campanha.

## Decisao Principal

O Bloco 3 registra canais.

Ele pode preparar a conexao oficial do WhatsApp Business, mas o CRM pode continuar mesmo que o WhatsApp fique pendente.

Regra central:

- WhatsApp Business e e-mail sao canais principais;
- Instagram, Facebook, TikTok, X e site sao canais publicos opcionais;
- redes sociais opcionais nao ativam automacoes neste setup inicial;
- WhatsApp pendente bloqueia apenas recursos que dependem de WhatsApp, nao o CRM inteiro.

## Estrutura Aprovada

### Shell

A imagem usa corretamente:

- 51A como shell global do onboarding;
- stepper lateral esquerdo com `Studio` e `Equipe` concluidos e `Canais` em andamento;
- 51B como chat lateral do Agente de Configuracao;
- rodape global com ambiente, autosave e pendencias.

### Area Central

Conteudos aprovados:

- titulo `Canais`;
- badge `Bloco 3 de 8`;
- subtitulo explicando que o WhatsApp Business pode ser conectado oficialmente agora ou ficar como pendencia;
- card `WhatsApp Business`;
- card `E-mail do studio`;
- card `Canais publicos opcionais`;
- card/resumo `Status dos canais`;
- acoes da etapa.

Recomendacao de nomenclatura para produto:

- `Status dos canais` pode virar `Resumo dos canais`, para soar menos tecnico.

### WhatsApp Business

Campos e opcoes aprovados:

- `WhatsApp Business do studio`;
- pergunta `Esse numero esta no WhatsApp Business?`;
- opcoes:
  - `Sim, ja esta no WhatsApp Business`;
  - `Ainda esta no WhatsApp pessoal`;
  - `Nao sei`;
  - `Ainda nao tenho numero do studio`.

Estados aprovados:

- `Pronto para conexao oficial`;
- `Pendente de conexao oficial`.

Acao aprovada:

- `Conectar WhatsApp Business`.

Regras:

- nao mostrar termos tecnicos como WABA, token, webhook, API, BSP, Cloud API ou Phone Number ID;
- nao fazer o usuario configurar provedor neste bloco;
- deixar claro que o dono continua usando WhatsApp Business no celular;
- conexao oficial libera atendimento pelo CRM/agentes quando tudo estiver publicado e pronto.

### E-mail Do Studio

Campo aprovado:

- `E-mail do studio`.

Texto aprovado:

- usado para avisos, convites e comunicacao administrativa;
- pode ser o e-mail do dono no comeco.

Estado aprovado:

- `Pronto`.

### Canais Publicos Opcionais

Campos opcionais aprovados:

- `Instagram`;
- `Facebook`;
- `TikTok`;
- `X`;
- `Site`.

Regra:

- esses canais ajudam a registrar onde o studio aparece;
- nao ativam automacoes neste setup inicial;
- nao prometem inbox social, resposta de DM, captura de leads sociais, campanhas ou publicacao de conteudo.

### Resumo Dos Canais

Resumo aprovado:

- `WhatsApp Business` - pendente de conexao oficial;
- `E-mail` - pronto;
- `Canais publicos` - quantidade adicionada.

Aviso aprovado:

- o CRM pode seguir;
- mensagens e agentes pelo WhatsApp so serao ativados apos conexao oficial.

### Acoes Da Etapa

Acoes aprovadas:

- `Salvar rascunho`;
- `Configurar canais depois`;
- `Continuar`.

`Continuar` e a acao primaria.

`Configurar canais depois` e permitido porque canais publicos e conexao oficial podem ficar como pendencia segura.

## Papel Do Agente Nesta Tela

O agente deve explicar que este bloco define canais, sem transformar a tela em configuracao tecnica.

Mensagens aprovadas:

- `Este bloco define os canais que o Taliya pode usar para falar com alunos e equipe.`
- `O CRM pode continuar mesmo se o WhatsApp ainda nao estiver conectado.`
- `Para agentes responderem alunos no WhatsApp, o numero precisa estar no WhatsApp Business e passar pela conexao oficial.`
- `As redes sociais aqui sao so referencia do studio. Elas nao ativam automacoes neste setup inicial.`

Chips aprovados, com ajuste de nomenclatura:

- `Preciso conectar agora?`
- `Meu numero e pessoal`;
- `Vou perder meu WhatsApp?`

Recomendacao: trocar o titulo `Duvidas frequentes` por `Perguntas sugeridas` nas proximas imagens/implementacao.

## Pendencias

Pendencias deste bloco aparecem no rodape global ou no resumo dos canais.

Exemplo aprovado:

- `Pendencias do setup (1)`;
- WhatsApp com `Pendente de conexao oficial`.

## O Que Foi Rejeitado

Nao usar no Bloco 3:

- templates de mensagem;
- campanhas;
- opt-out avancado;
- provedor/BSP;
- tokens;
- webhooks;
- numeros multiplos;
- regras de automacao;
- modos de agente;
- cotas de mensagens;
- logs de integracao;
- inbox social;
- responder DM do Instagram;
- capturar lead do Facebook;
- automatizar TikTok;
- publicar conteudo;
- configuracao profunda de agentes;
- alunos, planos, turmas ou agenda.

## Criterio De Aceite

O Bloco 3 esta correto quando:

- registra WhatsApp Business e e-mail como canais principais;
- permite redes sociais opcionais sem prometer automacao;
- deixa WhatsApp como pendencia segura quando necessario;
- nao expõe complexidade tecnica de provedor/API;
- mantem o agente como apoio lateral;
- segue o design system Taliya e o shell 51A.
