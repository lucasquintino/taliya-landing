# Taliya CRM - Contrato Da Pagina Execucao De Fluxo

Status: aprovado.
Data: 2026-05-25.

## Decisao

`/app/fluxos/execucoes/[runId]` existe no MVP, mas como pagina de apoio simples.

Ela nao e:

- nova familia de produto;
- hub de control plane;
- pagina de incidente;
- log tecnico;
- auditoria completa;
- configuracao de fluxo;
- simulacao;
- publicacao.

Ela e um recibo operacional de uma execucao real.

## Para Que Serve

Responder, em linguagem simples:

- o que aconteceu neste caso?
- qual fluxo rodou?
- qual aluno, aula, conversa, cobranca ou caso foi afetado?
- o que a Taliya fez?
- por que seguiu, parou, pediu aprovacao ou chamou humano?
- quanto consumiu de cota?
- onde a operacao continua?

## Imagem Aprovada

Referencia visual aprovada:

- `70_round-4.1P_execucoes_01_fluxo-falta-com-aviso-aprovado.png`

Estado representado na imagem:

- fluxo `Falta com aviso`;
- aluna `Julia Martins`;
- aula `Pilates Solo hoje 18h30`;
- modo `Autonomo com excecoes`;
- status `Concluida`;
- cota `1 mensagem consumida`;
- continuidade em `Tarefas / Reposicoes`.

## O Que A Pagina Guarda

Registro minimo por execucao:

- `runId`;
- agente;
- rotina;
- fluxo;
- modo ativo no momento da execucao;
- versao/snapshot da regra usada;
- objeto afetado: aluno, aula, conversa, cobranca, tarefa, aprovacao ou caso;
- horario de inicio;
- horario de fim, se houver;
- status final;
- acao principal feita;
- motivo resumido;
- cota usada;
- continuidade operacional;
- responsavel chamado, se houver;
- auditoria vinculada, se sensivel.

## O Que A Pagina Mostra

### Header

- breadcrumb do contexto;
- titulo `Execucao: [nome do fluxo]`;
- subtitulo com objeto principal;
- chips:
  - status final;
  - modo;
  - cota consumida;
  - continuidade.

### Resumo Da Execucao

Card simples com:

- fluxo;
- agente;
- caso;
- inicio;
- frase curta explicando o resultado.

Exemplo:

`A Taliya registrou a falta avisada, enviou a mensagem aprovada e criou uma tarefa de reposicao.`

### O Que Aconteceu

Timeline operacional curta.

Para `Falta com aviso`:

1. Aluna avisou falta.
2. Taliya conferiu as regras.
3. Taliya executou.
4. Continuidade criada.

Cada etapa usa linguagem de CRM, nao linguagem tecnica.

### Por Que Seguiu Sem Chamar Equipe

Lista de checks humanos e legiveis.

Para `Falta com aviso`:

- aluna identificada;
- aula encontrada;
- aviso dentro do prazo configurado;
- falta ainda nao registrada;
- template aprovado;
- WhatsApp conectado;
- cota disponivel.

Se algum check falhar, a execucao deve explicar onde parou e qual humano/area foi chamado.

### Continuidade

Mostra onde o trabalho segue:

- tarefa;
- aprovacao;
- conversa;
- cobranca;
- aluno;
- aula;
- nada, quando a execucao terminou sem pendencia.

CTA principal deve abrir a continuidade.

No exemplo aprovado:

- CTA principal: `Abrir tarefa`;
- CTAs secundarios: `Abrir aluna`, `Ver fluxo`.

## Painel Direito

Usa `Agente de Configuracao`, mas apenas para explicar a execucao.

Ele pode:

- explicar por que a execucao seguiu;
- explicar onde a tarefa foi criada;
- explicar consumo de cota;
- comparar com o que mudaria em outro modo.

Ele nao pode:

- configurar fluxo;
- publicar;
- alterar modo;
- alterar cota;
- reexecutar sozinho.

## O Que Nao Mostrar

Nao mostrar:

- prompt;
- pensamento interno do agente;
- JSON;
- payload do WhatsApp;
- stack trace;
- tokens;
- custo interno de provedor;
- logs tecnicos;
- grafico;
- simulacao;
- configuracao do fluxo;
- botao de publicar;
- reprocessamento tecnico.

## Ajustes Obrigatorios Da Imagem Aprovada

- A pagina pertence a Agentes/Fluxos. O topo pode destacar `Agentes`; a lateral pode destacar Agentes ou ficar sem destaque especifico, conforme a regra final do shell.
- O chip `1 mensagem consumida` deve usar icone neutro de cota/uso, nao icone que pareca apenas chat.
- O botao `Ver fluxo` nao deve aparecer duplicado na implementacao. Manter no card de continuidade ou no rodape, nao nos dois.
- `Agente de Configuracao` deve explicar, nao configurar.

## Relacao Com Outras Paginas

| Origem | Como chega na execucao |
|---|---|
| `/app/uso/extrato` | `Abrir execucao` |
| pagina do fluxo | historico de execucoes, quando existir |
| tarefa criada por agente | link para origem da tarefa |
| aprovacao criada por agente | link para execucao que preparou a aprovacao |
| auditoria | link para execucao sensivel, quando aplicavel |

## Decisao Final

Execucao de fluxo fica no MVP porque torna a automacao explicavel.

Ela deve continuar pequena, legivel e operacional.
