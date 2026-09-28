# Design System Web - Rodada 3B.4 - Comunicacao E Agentes

> Status: biblioteca visual v0.1 aprovada. Esta rodada documenta componentes de comunicacao, WhatsApp, copiloto e agentes integrados ao CRM.

## Objetivo

Definir como comunicacao e agentes aparecem dentro do Taliya CRM web, sem parecer produto separado de chat ou IA.

Esta rodada cobre:

- inbox/lista de conversas;
- conversa selecionada;
- status de canal WhatsApp;
- bolhas de mensagem;
- nota interna;
- composer;
- painel de copiloto;
- sugestao de agente;
- aprovacao de acao;
- execucao autonoma;
- falha de agente;
- handoff humano;
- card de confianca.

## Decisao

A imagem da Rodada 3B.4 fica aprovada como v0.1.

Ela acertou:

- tratou agentes como parte nativa do CRM;
- nao criou mascote nem visual de IA separado;
- manteve WhatsApp como canal, nao como produto inteiro;
- mostrou copiloto com resumo, proxima acao e sugestao;
- cobriu aprovacao, execucao autonoma, falha e handoff;
- trouxe card de confianca sem exagerar em grafismo.

## Ressalvas

- O visual de conversa esta mais proximo de tela final do que de componente, mas e util como referencia.
- Verde do WhatsApp deve ser usado como cor semantica de canal, nao cor dominante.
- Elementos de agente precisam ser discretos; evitar brilho, roxo ou gradientes de IA.
- O card de confianca precisa sempre explicar base e contexto, nao so mostrar numero.
- Aprovacao de acao deve deixar claro impacto, risco e possibilidade de editar.

## Regras De Uso

- Inbox deve priorizar conversas acionaveis e nao lidas.
- Composer deve suportar mensagem, nota interna, anexos, templates e envio.
- Sugestao do copiloto deve ser editavel antes de enviar.
- Acao autonoma deve mostrar status, etapa e opcao de pausar ou assumir manualmente.
- Falha de agente deve oferecer fallback manual.
- Handoff humano deve registrar responsavel e horario.
- Confianca do agente deve ser apoio de decisao, nao autorizacao automatica.

## Nao Fazer

- Nao transformar o CRM em app de chat generico.
- Nao esconder a responsabilidade humana.
- Nao mostrar agente como personagem ou mascote.
- Nao usar visual futurista, roxo ou neon para IA.
- Nao executar acao sensivel sem confirmacao quando politica exigir.

