# Taxonomia De Itens Acionaveis Do Hoje - PT-BR

> Status: v0.1. Este documento resolve a duvida central da pagina Hoje: nem tudo que aparece ali e uma tarefa. Hoje e uma mesa de comando que agrega demandas do dia vindas de varias origens do CRM.

## Decisao Central

A pagina **Hoje** nao e uma lista de tarefas.

Ela e uma **mesa de comando do dia**.

Ela mostra aquilo que precisa de atencao hoje para o studio nao travar:

- tarefas humanas;
- conversas aguardando pessoa;
- bloqueios de agenda, dados, recurso, professor, cota ou integracao;
- aprovacoes pendentes;
- pendencias financeiras com impacto hoje;
- itens de checklist;
- prioridades calculadas por regra, agente ou operacao.

Uma parte desses itens ja nasce como tarefa. Outra parte nasce como conversa, bloqueio, aprovacao, caso, pagamento, reposicao, incidente ou alerta.

## Regra Principal

```text
Tarefa e a unidade de trabalho humano.
Hoje e a unidade de priorizacao do dia.
```

Portanto:

- todo item de Hoje precisa ter origem;
- nem todo item de Hoje precisa virar tarefa;
- um item vira tarefa somente quando exige trabalho humano separado, com dono, prazo e acompanhamento;
- se o item puder ser resolvido diretamente na origem, ele abre a origem;
- se o item cruzar areas ou tiver varias etapas, ele abre ou cria um caso operacional;
- se exigir decisao, ele abre ou cria uma aprovacao.

## Tipos De Item Do Hoje

| Tipo no Hoje | O que e de verdade | Origem canonica | Quando vira tarefa | Quando nao vira tarefa |
| --- | --- | --- | --- | --- |
| Agora | Ranking de prioridades do dia | Agregador do Hoje | Quando a proxima acao humana precisa ser acompanhada | Quando o item abre uma origem e e resolvido ali |
| Checklist do dia | Rotina operacional recorrente | Checklist | Quando um item precisa de dono fora da rotina | Quando e apenas marcar etapa feita |
| Aulas de hoje | Recorte da agenda do dia | Agenda/Aulas | Quando exige preparacao, chamada, ajuste ou contato | Quando e apenas consulta da aula |
| Fila humana | Intervencao aguardando pessoa | Inbox, Operacao ou Agente | Quando a intervencao precisa de retorno, prazo ou dono | Quando a pessoa responde e resolve na propria origem |
| Bloqueios de hoje | Impedimento que trava acao | Operacao, Agenda, Dados, Integracoes, Cotas | Quando existe uma acao humana especifica para remover o bloqueio | Quando o melhor caminho e abrir caso operacional ou corrigir na origem |
| Tarefas de hoje | Trabalho humano com dono/prazo | Tarefas | Ja e tarefa | Nao se aplica |
| Aprovacoes de hoje | Decisao pendente | Aprovacoes | Quando a decisao pede trabalho posterior | Enquanto for apenas aprovar, editar, rejeitar ou pedir dados |
| Dinheiro hoje | Pendencia financeira com impacto hoje | Financeiro/Cobrancas/Pagamentos | Quando alguem precisa validar, ligar, cobrar ou revisar | Quando e apenas status financeiro ou pagamento confirmado |
| Alertas/notificacoes | Aviso roteado por papel/prioridade | Notificacoes | Quando o alerta exige acompanhamento humano | Quando e somente informativo |
| Incidentes | Falha tecnica ou falha de agente/integracao | Operacao/Incidentes ou Agentes/Execucoes | Quando precisa de acao manual ou suporte | Quando pode ser reprocessado com seguranca na origem |
| Problemas de dados | Dado ausente, conflito ou baixa confianca | Qualidade de dados/Operacao | Quando alguem precisa corrigir ou validar dado | Quando a correcao e feita diretamente no cadastro |

## Fontes De Criacao

Um item pode aparecer no Hoje por cinco caminhos.

| Caminho | Quem cria | Exemplos |
| --- | --- | --- |
| Manual | Usuario | tarefa criada pelo gestor, item de checklist, caso aberto pela recepcao |
| Programatico | Regra do CRM | aula sem professor, chamada pendente, pagamento vencido, reposicao sem encaixe |
| Copiloto | Agente sugere e aguarda pessoa | sugestao de mensagem, proposta de encaixe, resumo com proxima acao |
| Autonomo | Agente executa ou gera fallback | handoff humano, tarefa criada por falha, aprovacao por acao sensivel |
| Integracao/importacao | WhatsApp, financeiro, CSV, agenda externa | conversa recebida, comprovante enviado, conflito de importacao |

## Quando Criar Tarefa

Criar tarefa quando houver:

- uma pessoa responsavel;
- um prazo ou janela de execucao;
- uma acao humana concreta;
- necessidade de acompanhar conclusao;
- trabalho que nao sera resolvido no mesmo clique;
- continuidade fora da origem original.

Exemplos:

| Situacao | Tarefa criada |
| --- | --- |
| Conversa precisa de retorno mais tarde | Retornar Ana Paula as 16:00 |
| Professor indisponivel | Confirmar substituto para aula das 14:00 |
| Pagamento vencido exige contato | Ligar para Gustavo sobre mensalidade vencida |
| Comprovante pendente | Validar comprovante enviado por Mariana |
| Reposicao sem encaixe exige avaliacao | Encontrar encaixe manual para Ana Paula |
| Dado bloqueia automacao | Corrigir telefone do responsavel |

## Como Uma Tarefa Nasce

Uma tarefa pode nascer de modo manual, programatico, copiloto ou autonomo. O que muda e quem propôs, quem confirmou e qual nivel de auditoria/seguranca precisa existir.

| Forma de criacao | Quem cria | Exemplo | Estado inicial recomendado | Observacao |
| --- | --- | --- | --- | --- |
| Manual direta | Usuario | Gestor cria "Confirmar reposicao com Ana Paula" | Aberta ou atribuida | Caminho sempre disponivel, inclusive no plano 0 agentes. |
| Manual a partir de origem | Usuario clicando em "Criar tarefa" numa conversa, aula, pagamento ou bloqueio | Recepcao abre conversa e cria tarefa de retorno | Aberta com origem vinculada | A tarefa herda aluno, conversa, aula, pagamento ou caso. |
| Programatica por regra | Sistema CRM | Reposicao sem confirmacao ate 10:30 gera tarefa | Aberta, sem IA | Nao consome agente; funciona no plano Base. |
| Fallback de bloqueio | Sistema CRM | Agente/cota/integracao nao conseguiu seguir e cria caminho manual | Aberta ou sem dono | Deve explicar o motivo do fallback. |
| Copiloto sugerida | Agente sugere, humano confirma | Agente sugere "criar tarefa para confirmar reposicao" | Rascunho ou pendente de confirmacao | So vira tarefa depois de clique humano. |
| Copiloto assistida | Humano pede ajuda para criar | Usuario clica "Criar tarefa com IA" e revisa titulo/prazo/dono | Rascunho revisavel | IA preenche, humano salva. |
| Autonoma segura | Agente cria dentro de politica permitida | Agente cria tarefa de follow-up interno apos conversa sem resposta | Aberta com origem e justificativa | Permitido apenas para tarefa segura, sem decisao sensivel. |
| Autonoma por falha | Agente cria porque nao pode executar | Agente nao pode enviar mensagem por cota/opt-out e cria tarefa manual | Aberta com motivo de bloqueio | Deve mostrar cota, politica ou permissao que impediu. |
| Checklist recorrente | Regra de rotina | "Abrir o estudio", "Conferir agenda" | Pendente no checklist, nao tarefa comum | So vira tarefa se sair da rotina simples. |
| Caso operacional | Usuario, sistema ou agente cria tarefa dentro de um caso | Caso de reposicoes cria tarefa para recepcao | Aberta vinculada ao caso | Ajuda a quebrar problema grande em trabalho humano. |

## Modos De Criacao De Tarefa

### Manual

O usuario decide criar a tarefa.

Pode acontecer em:

- Hoje;
- Tarefas;
- Inbox/conversa;
- Agenda/aula/reposicao;
- Financeiro;
- Operacao/caso;
- Aluno/perfil;
- Bloqueio ou problema de dados.

Regras:

- precisa de titulo;
- precisa de dono ou fila;
- precisa de prazo quando impacta o dia;
- deve guardar origem;
- pode ser criada sem agente ativo.

### Copiloto

O agente nao cria sozinho como decisao final. Ele prepara uma sugestao.

Pode sugerir:

- titulo;
- resumo;
- prazo;
- responsavel;
- checklist;
- prioridade;
- origem vinculada;
- proxima acao.

Regras:

- usuario revisa antes de salvar;
- se envolver area sensivel, pedir confirmacao;
- se faltar dado, virar rascunho ou pedir complemento;
- deve mostrar "sugerido por agente".

### Autonomo

O agente pode criar tarefa sem clique humano apenas quando a tarefa for segura e operacional.

Permitido:

- criar lembrete interno;
- criar follow-up sem envio externo;
- criar tarefa de fallback quando automacao nao pode continuar;
- criar tarefa de triagem;
- criar tarefa de corrigir dado nao sensivel;
- criar tarefa vinculada a caso/incidente.

Nao permitido como autonomia simples:

- concluir tarefa humana sensivel;
- aprovar decisao;
- alterar agenda estrutural;
- confirmar pagamento;
- aplicar desconto;
- enviar comunicacao sensivel sem politica;
- marcar chamada/presenca sem evidencia permitida.

Em autonomia, toda tarefa precisa registrar:

- agente/fluxo que criou;
- motivo;
- origem;
- politica usada;
- cota/custo se aplicavel;
- fallback manual disponivel.

## Como Uma Tarefa E Concluida

Concluir tarefa significa encerrar a unidade de trabalho humano. Isso nao significa necessariamente que o problema raiz foi resolvido, a menos que a tarefa tenha esse escopo.

Toda conclusao deve registrar:

- ator que concluiu;
- horario;
- resultado;
- comentario obrigatorio quando houver impacto;
- mudancas feitas na origem, quando houver;
- evidencias/anexos quando necessario;
- auditoria quando sensivel.

## Formas De Conclusao

| Forma de conclusao | Quem conclui | Exemplo | Resultado esperado |
| --- | --- | --- | --- |
| Manual simples | Usuario | Mariana confirma reposicao e conclui tarefa | Tarefa concluida; origem pode ser atualizada manualmente. |
| Manual com resultado | Usuario escolhe resultado | Aluna aceitou/recusou horario | Tarefa concluida com resultado estruturado. |
| Manual com atualizacao da origem | Usuario conclui e atualiza objeto | Reservar vaga e marcar reposicao como confirmada | Tarefa concluida + reposicao atualizada. |
| Manual parcial | Usuario nao resolveu tudo | Aluna nao respondeu | Tarefa reagendada ou nova tarefa criada. |
| Copiloto assistido | Agente sugere fechamento, humano confirma | IA resume conversa e sugere "concluir como aceito" | Humano confirma; tarefa conclui. |
| Autonomo seguro | Agente conclui tarefa que ele mesmo pode validar | Agente enviou lembrete permitido e registrou entrega | Tarefa concluida com evidencia automatica. |
| Conclusao por origem | Origem muda e fecha tarefa vinculada | Reposicao foi confirmada na agenda | Tarefa fecha automaticamente ou pede confirmacao. |
| Cancelamento | Usuario cancela porque nao faz mais sentido | Aula cancelada, tarefa de confirmar reposicao nao e mais necessaria | Tarefa cancelada com motivo. |
| Conversao | Tarefa vira caso/aprovacao | Problema maior que uma tarefa simples | Tarefa encerrada como convertida e vinculada ao novo objeto. |

## Modos De Conclusao Da Tarefa

### Manual

O usuario executa e conclui.

Pode concluir com:

- feito;
- nao foi possivel;
- reagendado;
- delegado;
- cancelado;
- convertido em caso;
- convertido em aprovacao;
- aguardando resposta.

### Copiloto

O agente ajuda, mas nao decide sozinho.

Pode:

- resumir contexto;
- sugerir resultado;
- preencher comentario de conclusao;
- detectar se a origem ja mudou;
- sugerir proxima tarefa;
- preparar mensagem de confirmacao.

O usuario precisa confirmar a conclusao quando:

- envolve aluno;
- envolve agenda;
- envolve financeiro;
- envolve comunicacao externa;
- envolve dado sensivel;
- muda status de objeto importante.

### Autonomo

O agente so conclui automaticamente quando houver evidencia objetiva e baixo risco.

Pode concluir automaticamente:

- tarefa criada pelo proprio fluxo para registrar uma execucao segura;
- lembrete interno enviado;
- tentativa de contato registrada sem decisao sensivel;
- tarefa tecnica de reprocessamento seguro concluida;
- tarefa de triagem cujo resultado foi "sem acao necessaria" por regra.

Nao deve concluir automaticamente:

- tarefa atribuida a humano sem regra explicita;
- tarefa financeira sensivel;
- tarefa de aprovacao;
- tarefa de alteracao de agenda estrutural;
- tarefa que exige julgamento humano;
- tarefa que depende de resposta ambigua de aluno/responsavel.

## Exemplo: Confirmar Reposicao Com Ana Paula

### Como a tarefa pode nascer

| Modo | Fluxo |
| --- | --- |
| Manual | Recepcao abre `Agenda > Reposicoes`, ve Ana Paula sem confirmacao e cria tarefa. |
| Programatico | Sistema detecta reposicao sugerida sem confirmacao ate 10:30 e cria tarefa para a fila Recepcao. |
| Copiloto | Agente de Agenda sugere criar tarefa com horario recomendado; humano revisa e salva. |
| Autonomo seguro | Agente nao pode enviar convite por cota/consentimento/janela e cria tarefa manual de confirmacao. |
| Caso operacional | Caso "Reposicoes sem encaixe" cria uma tarefa filha para confirmar Ana Paula. |

### Como pode concluir

| Resultado | O que acontece |
| --- | --- |
| Aluna aceitou | Tarefa conclui; reposicao vira reservada/confirmada; origem fica atualizada. |
| Aluna recusou | Tarefa conclui com resultado recusado; reposicao volta para buscar nova opcao. |
| Aluna nao respondeu | Tarefa nao deve concluir como sucesso; pode reagendar ou criar follow-up. |
| Horario ficou indisponivel | Tarefa converte/abre bloqueio de agenda ou caso operacional. |
| Responsavel errado/contato invalido | Tarefa cria problema de dados ou tarefa de correcao. |
| Gestor delegou | Tarefa muda dono/fila, nao conclui. |

### Botoes ideais no drawer dessa tarefa

| Botao | Funcao |
| --- | --- |
| Abrir conversa | Vai para a conversa da aluna/responsavel para confirmar. |
| Concluir | Fecha com resultado estruturado: aceitou, recusou, sem resposta, nao aplicavel. |
| Reagendar | Muda o prazo da tarefa/follow-up. |
| Delegar | Troca responsavel ou fila. |
| Abrir origem | Abre `Agenda > Reposicoes` na reposicao da Ana Paula. |

## Quando Abrir Origem Sem Criar Tarefa

Nao criar tarefa quando a pessoa consegue resolver direto na origem.

Exemplos:

| Situacao | Abre |
| --- | --- |
| Conversa aguardando humano e operador vai responder agora | Inbox/conversa |
| Reposicao com sugestao clara de vaga | Agenda/reposicoes |
| Pagamento ja identificado no provedor | Financeiro/pagamento |
| Aprovacao de mensagem | Aprovacoes |
| Dado faltante simples no cadastro | Perfil do aluno/contato |

## Quando Criar Caso Operacional

Criar ou abrir caso operacional quando o problema:

- cruza mais de uma area;
- tem varias etapas;
- pode gerar mais de uma tarefa;
- envolve impacto em alunos, aulas, financeiro, agente ou integracao;
- precisa de timeline e dono operacional;
- pode reabrir ou escalar.

Exemplos:

| Situacao | Caso operacional |
| --- | --- |
| Professor indisponivel impacta 2 aulas | Caso "Resolver aulas afetadas" |
| WhatsApp caiu e deixou conversas presas | Caso "Falha de canal WhatsApp" |
| Cota 100% bloqueou automacoes do dia | Caso "Operacao em economia/bloqueio de cota" |
| Importacao criou duplicidade em alunos ativos | Caso "Resolver duplicidades de alunos" |

## Quando Criar Aprovacao

Criar aprovacao quando o sistema, agente ou usuario propuser uma decisao que precisa de autorizacao.

Exemplos:

| Situacao | Aprovacao |
| --- | --- |
| Enviar mensagem externa sensivel | Aprovar mensagem |
| Alterar agenda de varios alunos | Aprovar alteracao de agenda |
| Aplicar desconto ou excecao financeira | Aprovar desconto |
| Reprocessar agente com custo/cota | Aprovar reprocessamento |
| Enviar comunicado em massa | Aprovar comunicado |

Aprovacao nao e tarefa. Ela pode gerar tarefa depois, mas enquanto o objetivo for decidir, editar, rejeitar ou aprovar, ela vive em Aprovacoes.

## Regra Por Bloco Da Pagina Hoje

### Agora

Mostra os itens mais importantes do dia, vindos de qualquer origem.

Cada item deve exibir:

- titulo;
- origem;
- impacto;
- prazo;
- responsavel/fila quando existir;
- indicacao de abertura.

Ao clicar, abre drawer com:

- origem canonica;
- motivo da prioridade;
- proxima acao recomendada;
- opcoes: resolver agora, abrir origem, delegar, criar tarefa, criar caso ou aprovar, conforme tipo.

### Fila Humana

Mostra coisas aguardando pessoa.

Pode vir de:

- Inbox;
- agente pausado;
- handoff humano;
- atendimento aguardando recepcao;
- agenda aguardando coordenacao;
- financeiro aguardando validacao.

Nao e automaticamente tarefa. Vira tarefa apenas se precisar acompanhar fora da origem.

### Bloqueios De Hoje

Mostra impedimentos que travam o dia.

Pode vir de:

- professor indisponivel;
- sala em conflito;
- turma sem vaga;
- reposicao sem encaixe;
- dado obrigatorio ausente;
- integracao falhando;
- cota em limite;
- permissao insuficiente.

Bloqueio e o problema raiz. Ele pode abrir origem, caso operacional ou tarefa, dependendo do impacto.

### Tarefas De Hoje

Mostra somente tarefas reais.

Uma tarefa precisa ter:

- titulo claro;
- dono ou fila;
- prazo;
- status;
- origem;
- objeto afetado quando houver.

### Aprovacoes De Hoje

Mostra decisoes pendentes que vencem ou impactam hoje.

Nao misturar com tarefa. A acao principal e decidir.

### Dinheiro Hoje

Mostra apenas financeiro que exige atencao hoje.

Nao e lista completa do financeiro. Entram aqui:

- cobranca vencida que impacta aula;
- comprovante aguardando validacao;
- pagamento falhou e precisa acao;
- desconto/excecao pendente;
- contrato financeiro bloqueando matricula ou continuidade.

Vira tarefa quando alguem precisa cobrar, validar, ligar ou revisar.

## Regra De Interface

Na imagem principal da pagina Hoje:

- itens sao selecionaveis;
- itens nao devem ter botoes de acao internos;
- cada item deve indicar abertura por chevron, seta ou affordance visual;
- a acao detalhada aparece no drawer/painel apos clique.

No drawer:

- mostrar tipo real do item;
- mostrar origem canonica;
- mostrar porque apareceu no Hoje;
- mostrar proxima acao;
- oferecer apenas acoes coerentes com o tipo.

## Mapa De Acoes Do Drawer

| Tipo | Acoes possiveis |
| --- | --- |
| Prioridade do Agora | abrir drawer do tipo real, abrir origem, criar tarefa/caso/aprovacao conforme necessidade |
| Checklist do dia | marcar feito, comentar, delegar item, abrir origem, criar tarefa se sair da rotina |
| Aula de hoje | abrir aula, chamada, ver alunos, registrar ocorrencia, criar tarefa, abrir agenda |
| Conversa/fila humana | responder agora, assumir, criar tarefa, abrir conversa |
| Bloqueio | resolver agora, abrir origem, criar caso, criar tarefa, delegar |
| Tarefa | assumir, concluir, reagendar, delegar, abrir origem |
| Aprovacao | aprovar, editar, rejeitar, pedir dados, abrir origem |
| Financeiro | validar, cobrar, abrir pagamento, criar tarefa ou pedir aprovacao |
| Alerta/cota contextual | abrir origem, ajustar economia, criar tarefa, pausar baixa prioridade |
| Incidente | reprocessar se seguro, criar tarefa, abrir incidente, pausar fluxo |
| Problema de dados | corrigir dado, pedir revisao, criar tarefa, abrir perfil |

## Contrato De Drawer Por Tipo

Cada tipo de item do Hoje deve abrir um drawer especifico. A estrutura visual pode ser parecida, mas o conteudo, a prioridade das informacoes e as acoes mudam conforme a natureza do item.

### Drawer De Prioridade Do Agora

Usar quando o item foi aberto a partir do bloco **Agora**.

O bloco Agora e um agregador. Ele nao cria um tipo novo de objeto. Ao clicar em um item do Agora, o drawer deve revelar o **tipo real** daquele item: tarefa, fila humana, bloqueio, aprovacao, financeiro, aula, incidente, problema de dados ou alerta de cota.

Deve responder:

> Por que isto subiu para Agora e qual e o caminho mais rapido para resolver hoje?

Conteudo obrigatorio:

- titulo da prioridade;
- tipo real do item;
- motivo de estar no Agora;
- origem canonica;
- impacto no dia;
- prazo ou janela critica;
- responsavel/fila;
- proxima acao recomendada;
- resumo curto do contexto;
- link visual para a origem.

Acoes principais:

- executar a acao primaria do tipo real;
- abrir origem;
- delegar quando houver trabalho humano;
- criar tarefa, caso ou aprovacao quando o item ainda nao tiver uma unidade de resolucao.

Regra:

- se o item do Agora for uma tarefa, usar o drawer de tarefa;
- se for bloqueio, usar o drawer de bloqueio;
- se for fila humana, usar o drawer de fila humana;
- se for financeiro, usar o drawer financeiro;
- se for aprovacao, usar o drawer de aprovacao.

O drawer do Agora deve deixar claro que ele e uma entrada priorizada, nao uma lista generica.

### Drawer De Checklist Do Dia

Usar quando o item vem do bloco **Checklist do dia**.

Deve responder:

> Esta etapa da rotina diaria foi feita, esta atrasada ou precisa virar trabalho acompanhado?

Conteudo obrigatorio:

- nome do item do checklist;
- checklist de origem;
- status;
- horario esperado;
- responsavel/fila;
- evidencia esperada quando existir;
- dependencias;
- impacto se nao for concluido;
- historico curto;
- observacoes/comentarios.

Acoes principais:

- marcar como feito;
- reabrir item;
- comentar;
- delegar item;
- abrir origem relacionada.

Acoes secundarias:

- criar tarefa se a rotina nao puder ser concluida agora;
- anexar evidencia;
- pular com justificativa se permitido;
- ver checklist completo.

Checklist nao deve parecer tarefa por padrao. Ele so vira tarefa quando sai da rotina simples e precisa de acompanhamento.

### Drawer De Aula De Hoje

Usar quando o item vem do bloco **Aulas de hoje**.

Deve responder:

> O que precisa ser visto ou feito nesta aula de hoje?

Conteudo obrigatorio:

- nome da aula/turma;
- horario;
- sala;
- professor;
- capacidade e ocupacao;
- alunos esperados;
- status da chamada;
- alertas da aula;
- reposicoes/lista de espera relacionadas;
- pendencias de professor, sala, recurso ou aluno;
- proxima acao operacional.

Acoes principais:

- abrir aula;
- fazer chamada;
- ver lista de alunos;
- registrar ocorrencia;
- criar tarefa;
- abrir agenda/turma.

Acoes secundarias:

- avisar alunos se permitido;
- solicitar substituicao;
- resolver conflito;
- abrir reposicoes relacionadas;
- abrir perfil do professor.

Aula de hoje e consulta operacional com acao contextual. So vira tarefa se alguem precisar acompanhar algo fora da tela da aula.

### Drawer De Tarefa

Usar quando o item ja e uma tarefa humana.

Deve responder:

> Quem precisa fazer o que, ate quando, e de onde isso veio?

Conteudo obrigatorio:

- titulo da tarefa;
- status;
- prioridade;
- dono ou fila;
- prazo;
- origem;
- objeto afetado;
- descricao curta;
- checklist/subpassos quando existir;
- comentarios ou ultima atividade;
- relacao com caso, aprovacao, aluno, aula, conversa ou pagamento.

Acoes principais:

- iniciar/assumir;
- marcar como concluida;
- reagendar;
- delegar;
- abrir origem.

Acoes secundarias:

- comentar;
- anexar evidência;
- cancelar;
- criar subtarefa simples.

Nao deve parecer aprovacao. Nao deve pedir decisao sensivel como acao principal.

### Drawer De Fila Humana

Usar quando algo esta aguardando uma pessoa, mas ainda nao necessariamente e tarefa.

Deve responder:

> Quem esta esperando, ha quanto tempo, por qual motivo e onde eu resolvo?

Conteudo obrigatorio:

- origem da fila;
- pessoa/cliente/aluno afetado;
- tempo aguardando;
- canal;
- motivo do handoff;
- responsavel/fila atual;
- resumo do contexto;
- ultima mensagem ou ultimo evento;
- risco de espera.

Acoes principais:

- abrir conversa/origem;
- assumir atendimento;
- responder agora;
- criar tarefa se precisar acompanhar depois.

Acoes secundarias:

- delegar fila;
- marcar como resolvido;
- pausar automacao relacionada;
- abrir aluno/interessado.

### Drawer De Bloqueio

Usar quando existe um impedimento que trava uma acao do dia.

Deve responder:

> O que esta bloqueado, qual impacto, qual causa e qual caminho remove o bloqueio?

Conteudo obrigatorio:

- tipo de bloqueio;
- objeto bloqueado;
- causa raiz;
- impacto;
- prazo/urgencia;
- areas afetadas;
- dono sugerido;
- origem do bloqueio;
- dependencias;
- recomendacao de resolucao.

Acoes principais:

- resolver agora;
- abrir origem;
- criar caso operacional;
- criar tarefa;
- delegar.

Acoes secundarias:

- ignorar hoje com justificativa;
- pausar fluxo;
- notificar responsavel;
- ver historico.

Bloqueio nao deve parecer uma tarefa simples quando o problema cruza areas.

### Drawer De Aprovacao

Usar quando a proxima acao e uma decisao.

Deve responder:

> O que sera aprovado, qual impacto, qual risco e o que muda antes/depois?

Conteudo obrigatorio:

- tipo de aprovacao;
- proposta;
- solicitante;
- objeto afetado;
- antes/depois quando existir;
- risco;
- impacto;
- custo/cota quando aplicavel;
- politica usada;
- prazo de decisao;
- auditoria que sera gerada.

Acoes principais:

- aprovar;
- editar e aprovar;
- rejeitar;
- pedir mais dados.

Acoes secundarias:

- abrir origem;
- criar tarefa de revisao;
- ver historico.

Aprovacao nao deve ser apresentada como tarefa.

### Drawer Financeiro

Usar quando o item e uma pendencia financeira com impacto hoje.

Deve responder:

> Qual pendencia financeira exige acao hoje e o que ela impacta?

Conteudo obrigatorio:

- tipo financeiro;
- aluno/responsavel;
- valor;
- vencimento;
- status;
- impacto operacional;
- origem;
- metodo/provedor quando aplicavel;
- historico curto;
- politica de bloqueio/liberacao quando existir.

Acoes principais:

- validar pagamento/comprovante;
- cobrar;
- abrir pagamento/cobranca;
- criar tarefa;
- pedir aprovacao ou escalar para Operacao quando for excecao sensivel.

Acoes secundarias:

- enviar lembrete aprovado;
- registrar observacao;
- aplicar excecao com aprovacao;
- abrir aluno/responsavel.

### Drawer De Alerta Ou Cota Contextual

Usar quando o item e um aviso acionavel que impacta o dia, mas ainda nao e tarefa, aprovacao ou incidente.

Inclui:

- cota em 70%, 90% ou 100%;
- modo economia afetando uma acao de hoje;
- notificacao urgente;
- alerta de limite;
- alerta de politica operacional.

Deve responder:

> Este alerta muda o que pode ser feito hoje?

Conteudo obrigatorio:

- tipo do alerta;
- origem;
- nivel;
- impacto no dia;
- recurso afetado;
- limite ou politica relacionada;
- comportamento atual;
- fallback manual;
- recomendacao.

Acoes principais:

- abrir origem;
- ajustar economia;
- pausar baixa prioridade;
- criar tarefa;
- abrir uso/cotas ou configuracao relacionada.

Acoes secundarias:

- marcar como visto;
- silenciar tipo permitido;
- ver historico;
- pedir suporte quando aplicavel.

Alerta sem proxima acao nao deve aparecer como item principal do Hoje.

### Drawer De Incidente

Usar quando a demanda vem de falha tecnica, agente, integracao ou execucao.

Deve responder:

> O que falhou, qual impacto no dia e o que ainda pode ser feito com seguranca?

Conteudo obrigatorio:

- sistema/agente/integracao afetada;
- falha;
- impacto;
- objeto afetado;
- tentativa anterior;
- seguranca de reprocessamento;
- fallback manual;
- dono tecnico/operacional;
- horario;
- trace resumido.

Acoes principais:

- reprocessar se seguro;
- criar tarefa;
- abrir incidente;
- pausar fluxo.

Acoes secundarias:

- abrir execucao;
- ver detalhes;
- notificar responsavel;
- escalar suporte.

### Drawer De Problema De Dados

Usar quando um dado ausente, conflitante ou de baixa confianca trava uma acao.

Deve responder:

> Qual dado esta impedindo a acao e como corrigir com seguranca?

Conteudo obrigatorio:

- objeto afetado;
- dado faltante/conflitante;
- fonte do dado;
- confianca;
- impacto;
- sugestao de correcao;
- responsavel;
- historico curto;
- regra de conflito quando existir.

Acoes principais:

- corrigir dado;
- confirmar valor;
- pedir revisao;
- criar tarefa;
- abrir perfil/origem.

Acoes secundarias:

- manter separado;
- marcar como duplicidade;
- abrir qualidade de dados.

## Exemplos Praticos

| Item visto no Hoje | Tipo real | Origem | Acao primaria |
| --- | --- | --- | --- |
| Abrir o estudio | Checklist do dia | Checklist | Marcar feito ou abrir detalhe |
| Pilates Solo 08:00 10/12 | Aula de hoje | Agenda/Aula | Abrir aula/chamada |
| 3 conversas aguardando humano | Fila humana | Inbox | Abrir conversas |
| Reposicoes sem encaixe hoje | Bloqueio de agenda | Agenda/Reposicoes | Encontrar encaixe |
| Professor precisa confirmar substituicao | Bloqueio/tarefa candidata | Agenda/Recursos | Abrir detalhe e criar/delegar tarefa |
| Confirmar substituicao 10:30 | Tarefa | Tarefas | Concluir ou delegar |
| Mensagem do agente risco baixo | Aprovacao | Aprovacoes/Agentes | Aprovar, editar ou rejeitar |
| Mensalidade vencida aula 18:00 | Financeiro acionavel | Financeiro | Cobrar, validar ou criar tarefa |
| Cota 82% em comunicado | Alerta contextual de uso | Uso/Cotas | Abrir uso ou ajustar prioridade |

## Criterio Para Entrar No Hoje

Um item entra no Hoje se cumprir pelo menos uma regra:

- vence hoje;
- impacta aula, aluno, pagamento, atendimento ou agente hoje;
- esta bloqueando uma acao prevista para hoje;
- aguarda humano acima do limite;
- exige decisao antes de seguir;
- virou fallback por cota, agente, dado ou integracao;
- pertence ao checklist operacional do dia.

Um item nao entra no Hoje se:

- e apenas historico;
- nao exige acao hoje;
- pertence a relatorio semanal/mensal;
- e lista completa de modulo;
- nao tem dono, origem, impacto ou proxima acao.

## Implicacao Para As Proximas Imagens

A imagem `17_round-4.1A_hoje_01_acima-da-dobra.png` deve mostrar os blocos como fontes diferentes de demanda do dia, nao como uma unica lista de tarefas.

A imagem `18_round-4.1A_hoje_02_resolver-prioridade.png` deve deixar explicito que, ao clicar em um item, o drawer mostra:

- tipo real;
- origem canonica;
- motivo de aparecer no Hoje;
- proxima acao;
- se vai resolver na origem, criar tarefa, criar caso ou pedir aprovacao.

Essa regra deve guiar todos os prompts da pagina Hoje.

## Cobertura Final Dos Drawers Da Pagina Hoje

Para a pagina Hoje, todos os blocos da imagem principal devem ter comportamento de clique mapeado:

| Bloco da pagina Hoje | Drawer esperado |
| --- | --- |
| Agora | Drawer do tipo real, com cabecalho de prioridade |
| Checklist do dia | Drawer de checklist do dia |
| Aulas de hoje | Drawer de aula de hoje |
| Fila humana | Drawer de fila humana |
| Bloqueios de hoje | Drawer de bloqueio |
| Tarefas de hoje | Drawer de tarefa |
| Aprovacoes de hoje | Drawer de aprovacao |
| Dinheiro hoje | Drawer financeiro |
| Alerta/cota contextual | Drawer de alerta ou cota contextual |
| Incidente/problema tecnico | Drawer de incidente |
| Problema de dados | Drawer de problema de dados |

## Ciclos Dos Drawers

Os ciclos completos de criacao, entrada no Hoje, resolucao e comportamento em
0, 1, 3 e 7 agentes estao documentados em
`drawer-lifecycle-contracts.pt-BR.md`.

Este arquivo de taxonomia define **o que cada item e**. O contrato de ciclos
define **como cada item nasce, muda, resolve, vira tarefa, vira aprovacao ou
vira caso operacional**.
