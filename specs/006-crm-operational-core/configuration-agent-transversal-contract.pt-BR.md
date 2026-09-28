# Agente De Configuracao - Contrato Transversal

Status: contrato v0.1.
Data: 2026-05-14.

## Decisao

O agente de IA de configuracao acompanha todos os momentos de configuracao do Taliya, mas nao e a fonte da verdade e nao aplica regra sensivel por fora do sistema.

Ele guia, explica, compara, simula, prepara rascunhos e ajuda o gestor a entender impacto. O sistema valida, estrutura, versiona, publica e audita.

Ele deve explicar a fronteira entre setup inicial, configuracao pos-go-live e control planes quando isso ajudar a decisao do usuario. Nao deve repetir esse aviso em toda tela; a explicacao deve aparecer no contexto certo, como agente preparado, fluxo pendente, publicacao parcial, falha de execucao ou mudanca que exige Agentes/Fluxos.

## Modelo De Interacao

O agente de configuracao deve aparecer como chat/copiloto contextual, nao como produto paralelo.

O chat e a superficie de explicacao, duvida, alerta e sugestao. A configuracao oficial continua em componentes estruturados do sistema: formularios, tabelas, drawers, revisoes, simulacoes, validacoes e publicacao.

Regra transversal:

- o usuario pode perguntar livremente ao agente;
- o agente responde usando o contexto da tela atual;
- quando houver decisao estruturada, o agente deve levar o usuario para o campo, drawer ou acao correta;
- rascunhos gerados pelo agente precisam passar pelo sistema;
- nenhuma conversa vira configuracao publicada sem validacao e revisao.

## Onde Ele Aparece

### 1. Setup inicial

Papel: guia de implantacao.

Ajuda o studio a:

- entender o passo atual;
- responder perguntas em linguagem simples;
- escolher presets;
- detectar contradicoes;
- preparar rascunhos de configuracao;
- entender o que fica pronto, parcial, bloqueado ou pendente;
- agendar ajuda humana Taliya quando necessario.

Limite: no setup inicial, ele nao configura profundamente fluxos de agente. Ele apenas prepara agentes, responsaveis e pacotes de fluxos recomendados como rascunho/pendencia.

No setup inicial, a ordem principal das etapas e definida pelo produto. O agente nao deve oferecer um menu livre de "por onde comecar". Ele pode explicar a etapa atual, responder duvidas, sugerir presets e oferecer acoes rapidas dentro do passo em andamento.

### 2. Configuracoes pos-go-live

Papel: copiloto de mudanca operacional.

Ajuda o gestor a:

- alterar regras de um sistema que ja esta rodando;
- comparar regra atual versus regra nova;
- entender impacto em alunos, turmas, cobrancas, canais, tarefas e agentes;
- escolher data de vigencia;
- criar rascunhos de alteracao;
- configurar profundamente fluxos de agente em Agentes/Fluxos.

Aqui ficam configuracoes como:

- gatilho;
- condicao;
- acao;
- canal;
- mensagem;
- modo manual/copiloto/autonomo;
- aprovacao humana;
- limites;
- cotas por fluxo;
- fallback;
- simulacao;
- teste;
- publicacao.

### 3. Control planes

Papel: explicador e investigador.

Ajuda o usuario a entender:

- por que uma execucao falhou;
- qual politica bloqueou uma acao;
- quanto de cota foi consumido;
- qual fluxo gerou incidente;
- quem aprovou uma acao;
- qual ajuste precisa ser feito e em qual tela.

Limite: Control Plane nao e builder de fluxo. Quando houver mudanca de regra, o agente deve levar o usuario para a tela correta de configuracao pos-go-live.

## Regras De Segurança

O agente de configuracao nao pode:

- publicar configuracao sozinho;
- alterar regra sensivel sem confirmacao;
- mudar modo de fluxo sem simulacao/impacto;
- ignorar permissao, plano, cota, politica, canal ou consentimento;
- transformar conversa em fonte da verdade;
- substituir auditoria;
- aplicar configuracao fora da interface estruturada.

## Regra De Produto

Toda configuracao sensivel deve seguir o ciclo:

1. Usuario informa ou escolhe.
2. Agente explica e sugere.
3. Sistema gera rascunho estruturado.
4. Sistema valida impacto, permissao, plano, cota, politica e risco.
5. Usuario revisa.
6. Usuario aprova quando necessario.
7. Sistema publica, versiona e audita.

## Criterio De Aceite

O agente de configuracao esta correto quando o gestor consegue configurar com menos duvida, mas o produto continua previsivel, controlado e auditavel.
