# Rodada 5 - Vendas, experimental, matricula e comunicados - PT-BR

> Status: v0.1. Esta rodada define a base funcional e a primeira especificacao profunda das telas de Interessados, Vendas, Aulas experimentais e Matriculas. Comunicados ficam como agente/superficie separada pos-MVP.

## Objetivo operacional

Converter interessados em alunos sem quebrar agenda, financeiro, historico do relacionamento e operacao diaria do studio.

## Limite desta v0.1

Esta versao orienta produto, rotas, objetos, estados e acoes principais. Ainda falta, em passada posterior:

- fechar etapas oficiais do pipeline;
- definir campos minimos de pre-matricula;
- fechar contrato/assinatura quando o studio exigir antes da conversao;
- fechar regras de cadencia comercial automatica e limites de canal;
- documentar Comunicados como agente/superficie separada pos-MVP, fora do pipeline comercial diario;
- fechar microcopy de objecao, preco, sem vaga, perdido e converter;
- transformar esta rodada em prompts finais de UI.

## Usuarios envolvidos

| Usuario | Papel na rodada |
| --- | --- |
| Dono/gestor | Supervisiona funil, origens, conversao e descontos permitidos. |
| Admin | Configura etapas, templates e aprovacoes. |
| Recepcao/operacao | Atende interessados, agenda experimental, faz follow-up e cria pre-matricula. |
| Financeiro | Entra quando matricula envolve pagamento, contrato, desconto ou plano. |
| Professor | Participa da experimental e registra pos-aula quando permitido. |
| Agente/runtime | Qualifica, sugere resposta, acompanha cadencia, cria tarefas e envia mensagens permitidas. |

## Objetos de negocio

- Interessado;
- Origem de venda simples;
- Experimental;
- Pre-matricula;
- Contato;
- Responsavel;
- Aluno;
- Conversa;
- Mensagem;
- Template/modelo;
- Turma/aula;
- Lista de espera;
- Plano do studio;
- Plano do aluno;
- Pagamento;
- Contrato;
- Tarefa;
- Caso operacional;
- Aprovacao;
- Problema de dados;
- Evento de auditoria;
- Execucao de fluxo;
- Lancamento de cota.

## Jornadas cobertas

| Jornada | Resultado esperado |
| --- | --- |
| Capturar interessado de varios canais | Lead entra com origem, canal, etapa e proxima acao. |
| Cadastrar interessado manualmente | Equipe cria lead sem depender de WhatsApp ou agente. |
| Qualificar pessoa interessada | Lead recebe perfil, objetivo, horario desejado, nivel de interesse e proxima acao. |
| Responder duvida sobre preco/plano | Resposta usa dados permitidos, template e contexto comercial. |
| Agendar aula experimental | Agenda comercial conecta interessado, horario, professor e disponibilidade. |
| Enviar lembrete da experimental | Lembrete respeita canal configurado, template, janela e cota. |
| Remarcar falta na experimental | Falta vira remarcacao, tarefa ou perda com motivo. |
| Fazer pos-aula experimental | Professor/operacao registra resultado, objecao, interesse e proxima acao. |
| Manter cadencia comercial | Follow-up tem etapa, prazo, limite de tentativas e parada por opt-out. |
| Responder objecoes de venda | Sistema sugere resposta, mas humano decide quando envolve preco/desconto sensivel. |
| Criar pre-matricula | Checklist junta dados minimos, plano escolhido e primeira aula. |
| Lidar com demanda sem horario | Interessado vai para lista de espera futura, filtro `sem vaga` ou tarefa de retorno. |
| Converter interessado em aluno | Conversao cria aluno, agenda/plano inicial e preserva origem/historico. |

## Regras de negocio

1. Todo interessado precisa de etapa, origem, responsavel/fila e proxima acao ou motivo de perda.
2. Origem de venda simples deve ser preservada ate aluno para relatorio basico.
3. WhatsApp e canal de entrada/atendimento, nao substitui pipeline.
4. Lead duplicado vira Qualidade de dados antes de mesclar.
5. Resposta comercial externa respeita canal configurado, opt-out quando existir no canal, template, cota e janela do canal.
6. Preco, desconto, promessa financeira e contrato nao devem ser inventados por agente.
7. Experimental e uma ponte entre vendas e agenda; conflito de horario segue regras da Rodada 4.
8. Falta na experimental deve gerar remarcacao, follow-up ou perda com motivo.
9. Pre-matricula so converte em aluno quando dados minimos, contato e decisoes obrigatorias estiverem resolvidos.
10. Conversao deve criar ou vincular aluno sem apagar interessado, origem, conversa e historico comercial.
11. Demanda sem horario disponivel deve virar filtro `sem vaga`, tarefa de retorno ou lista de espera futura, e nao ser marcada como perdido automaticamente.
12. Comunicados nao pertencem ao pipeline principal de Vendas nesta rodada; ficam como agente/superficie separada pos-MVP.
13. Plano Base permite vender, agendar experimental e matricular manualmente sem agentes ativos.
14. Agente autonomo comercial deve ter limites de cadencia, horario, tom, cota e opt-out.

## Modos de execucao

| Modo | Como funciona nesta rodada |
| --- | --- |
| Manual | Usuario cadastra lead dentro do pipeline, responde, agenda experimental, faz follow-up, cria pre-matricula e converte. |
| Copiloto | Agente sugere qualificacao, resposta, objecao, proxima acao, mensagem e resumo de origem. |
| Autonomo | Agente faz follow-up, lembrete e resposta simples apenas com politica, canal configurado, template, cota e limites de cadencia. |

## Entradas e saidas

| Tipo | Exemplos |
| --- | --- |
| Entradas | formulario, WhatsApp, indicacao, landing, cadastro manual, chamada, experimental, origem, campanha, abandono, demanda sem vaga. |
| Saidas | interessado, tarefa, conversa, experimental, pre-matricula, aluno, aprovacao, caso, auditoria. |

## Fonte da verdade

| Dado | Fonte da verdade |
| --- | --- |
| Interessado | CRM Vendas. |
| Origem simples | CRM Vendas; preservada na conversao. |
| Experimental | CRM Vendas + Agenda. |
| Pre-matricula | CRM Matriculas. |
| Plano/pagamento/contrato | CRM Financeiro/Contratos; detalhamento final na Rodada 6. |
| Mensagem enviada | CRM Tentativa de envio + provedor. |

## Eventos e gatilhos

| Gatilho | Comportamento esperado |
| --- | --- |
| Novo lead | Criar interessado, detectar duplicidade, definir origem e proxima acao. |
| Lead sem resposta | Criar tarefa ou cadencia permitida. |
| Experimental agendada | Criar lembrete e mostrar no dia. |
| Experimental faltou | Remarcar, criar follow-up ou marcar perdido com motivo. |
| Pos-aula concluido | Atualizar etapa, objecao e proposta de conversao. |
| Pre-matricula incompleta | Mostrar pendencias e dono. |
| Pre-matricula abandonada | Criar tarefa/conversa conforme canal permitido e politica do studio. |
| Sem horario disponivel | Enviar para lista de espera/demanda reprimida. |

## Telas web desta rodada

1. Interessados e vendas.
2. Aulas experimentais.
3. Matriculas.

## Telas mobile desta rodada

1. Interessados.
2. Experimental.
3. Matricula rapida.

## Tela web: Interessados e vendas

| Campo | Definicao |
| --- | --- |
| Tipo | Web pipeline comercial; mobile acao parcial/completa. |
| Rotas | `/app/vendas`, `/app/interessados`, `/app/interessados/[id]`. Nao criar `/app/interessados/novo` nesta rodada; cadastro acontece por botao/drawer dentro do pipeline. |
| Objetivo | Operar pipeline de interessados com etapa, origem, conversa, qualificacao e proxima acao. |
| Usuario principal | Recepcao/operacao. |
| Usuarios secundarios | Dono/admin. |
| Blocos | kanban do pipeline, lista/tabela, filtros, detalhe do interessado, conversa, qualificacao, objecoes, tarefas, experimental, origem, proxima acao. |
| Campos exibidos | nome, contato, origem, etapa, interesse, horario desejado, unidade/turma desejada, proxima acao, dono, ultima conversa, canal. |
| Campos editaveis | dados basicos, etapa, qualificacao, objecao, dono, origem revisada, proxima acao, motivo de perda. |
| Acoes | cadastrar lead no pipeline, qualificar, responder, pedir sugestao, criar follow-up, agendar experimental, marcar perdido, converter, abrir conversa, enviar para lista de espera se necessario. |
| Estados | novo, qualificado, quente, sem resposta, experimental agendado, em follow-up, sem vaga, pre-matricula, perdido, convertido. |
| Permissoes | operacao vende; desconto/contrato/pagamento exige permissao apropriada. |
| IA/agentes | sugerir qualificacao, resposta, proxima acao, objecao e resumo. |
| Cotas | sugestao/redacao/resposta automatica consome cota; pipeline manual nao. |
| Auditoria | conversao, perda com motivo, origem alterada, promessa sensivel e envio externo. |
| Operacao sem agentes | pipeline, tarefas, conversas e follow-up manual funcionam. |

Decisoes de escopo:

- Vendas precisa de duas superficies no MVP: `/app/vendas` como Pipeline/Kanban e `/app/vendas/lista` como Lista, no estilo da separacao visual do Financeiro;
- Kanban e a visao principal para operar etapas;
- Lista e a visao de busca, filtros, volume e triagem;
- Pipeline e Lista nao usam toggle interno `Kanban / Lista`; a troca acontece pela navegacao superior da familia ou pela rota;
- ambas as superficies devem herdar os padroes visuais ja aprovados: Kanban segue Financeiro Kanban/Operacao; Lista segue Movimentacoes do Financeiro com barra de filtros, painel esquerdo de filtros rapidos, tabela/lista central e painel direito contextual;
- imagens aprovadas: `37_round-4.1G_vendas_01_pipeline-kanban.png` para `/app/vendas` e `38_round-4.1G_vendas_02_lista-interessados.png` para `/app/vendas/lista`;
- no Kanban, filtros rapidos ficam na barra superior e nao ha painel esquerdo; etapas extras ficam acessiveis por scroll horizontal;
- na Lista, painel esquerdo de filtros rapidos e painel direito contextual seguem o padrao de Movimentacoes do Financeiro;
- ambas compartilham o mesmo drawer/painel de interessado;
- `/app/vendas/perdidos` nao vira pagina propria no MVP; `perdido` e filtro/etapa dentro de `/app/vendas`;
- origem fica como campo simples do interessado, sem `/app/vendas/captura`, `/app/vendas/origens` ou `/app/indicacoes` no MVP;
- segmentos comerciais nao entram no MVP.

## Tela web: Aulas experimentais

| Campo | Definicao |
| --- | --- |
| Tipo | Web agenda comercial; mobile acao completa. |
| Rotas | `/app/experimental`. |
| Objetivo | Gerenciar experimentais agendadas, lembretes, faltas, remarcacoes, pos-aula e conversao, conectando o pipeline comercial com a Agenda. |
| Usuario principal | Recepcao/operacao. |
| Usuarios secundarios | Professor, dono/admin. |
| Blocos | agenda de experimentais, detalhe, interessado, professor, lembretes, presenca/falta, pos-aula, objecoes, conversao. |
| Campos exibidos | interessado, horario, professor, turma/aula, status, lembrete, compareceu, feedback, objecao, proxima acao. |
| Campos editaveis | horario, professor, status, observacao, feedback, objecao, proxima acao. |
| Acoes | agendar, enviar lembrete, remarcar, registrar falta, fazer pos-aula, criar follow-up, converter, marcar perdido. |
| Estados | agendada, lembrete pendente, lembrete enviado, confirmou, faltou, remarcada, concluiu, converter agora, perdido. |
| Permissoes | professor registra pos-aula permitido; conversao/financeiro ficam com operacao/admin. |
| IA/agentes | sugerir lembrete, follow-up e resumo pos-aula; nao promete desconto sozinho. |
| Cotas | lembrete e follow-up automaticos consomem cota; acao manual nao. |
| Auditoria | remarcacao, conversao, perda e envio externo relevante. |
| Fallback | sem canal/cota, criar tarefa de contato manual. |

Integracao com Agenda:

- experimental nasce no pipeline de Vendas quando o interessado agenda uma aula teste;
- ao confirmar horario, o CRM cria uma aula/evento real na Agenda com tipo `experimental`;
- essa aula aparece em `/app/agenda` e pode ser aberta como aula concreta quando chegar o dia;
- a tela `/app/experimental` e a fila comercial dessas aulas teste: lembrete, compareceu/faltou, remarcacao, pos-aula e conversao;
- Agenda cuida de horario/capacidade/conflito; Vendas cuida de interessado, follow-up e conversao.

Imagem aprovada:

- `39_round-4.1G_experimental_01_lista-acompanhamento.png`.

Ciclo de entrada e saida:

- o item de Experimental nao e tarefa solta; e o vinculo `Interessado + Aula Experimental + Status + Proxima acao`;
- entradas principais: agendar pela Vendas, criar/vincular aula experimental pela Agenda ou acionar agendamento pela Inbox;
- a acao `Agendar experimental` deve escolher horario pela Agenda/componente de agenda, nao criar horario isolado;
- saidas principais: iniciar matricula em `/app/matriculas`, remarcar com nova aula vinculada, marcar perdido ou manter em pos-aula/follow-up;
- quando `Iniciar matricula` e acionado, o interessado sai dos filtros ativos de Experimental e entra em Matriculas;
- quando `Remarcar` e acionado, o item permanece em Experimental com nova aula vinculada;
- quando `Marcar perdido` e acionado, a tentativa encerra e permanece no historico de Vendas.

## Tela web: Matriculas

| Campo | Definicao |
| --- | --- |
| Tipo | Web checklist de conversao; mobile consulta + aprovacao. |
| Rotas | `/app/matriculas`. Nao criar `/app/checkout-alunos` como pagina propria nesta rodada. |
| Objetivo | Transformar interessado em aluno com um checklist simples de conversao: dados minimos, plano, primeira aula, pagamento inicial quando exigido e pendencias obrigatorias. |
| Usuario principal | Recepcao/operacao. |
| Usuarios secundarios | Financeiro, dono/admin. |
| Blocos | pre-matricula, dados obrigatorios, plano escolhido, primeira aula, pagamento inicial quando exigido, pendencias, conversao. |
| Campos exibidos | interessado, contato, dados faltantes, plano escolhido, primeira aula, pagamento inicial/status, responsavel, origem. |
| Campos editaveis | dados cadastrais minimos, plano escolhido, primeira aula, observacao, pendencias e acionamento de cobranca inicial quando permitido. |
| Acoes | criar pre-matricula, validar dados, pedir dados, escolher primeira aula, gerar/enviar cobranca inicial quando exigida, abrir cobranca, converter aluno, gerar tarefas. |
| Estados | rascunho, faltando dado, escolher plano, primeira aula pendente, pagamento pendente, pagamento enviado, pagamento falhou, pronto para aluno, convertido, bloqueado por conflito/aprovacao. |
| Permissoes | operacao valida dados e primeira aula; financeiro/dono controlam dinheiro, desconto, promessa, contrato e excecoes sensiveis quando necessario. |
| IA/agentes | sugerir checklist, redigir pedido de dado e resumir pendencias. |
| Cotas | redacao/envio automatico consome cota; checklist manual nao. |
| Auditoria | conversao, plano escolhido, primeira aula e alteracao sensivel. |
| Fallback | se dado financeiro/contrato for obrigatorio para o studio, conversao fica bloqueada ou vira aprovacao/pendencia na familia correta. |

Decisao de escopo:

- Matricula nao e checkout completo no MVP;
- pagamento inicial e relevante no checklist quando a politica do studio exigir pagamento antes da conversao;
- cobranca detalhada, conciliacao, comprovante, falha, desconto, promessa, estorno, contrato e auditoria pertencem a Financeiro/Contratos/Documentos;
- `/app/matriculas` e o checklist operacional para transformar interessado em aluno sem perder origem e historico.

Imagem aprovada:

- `40_round-4.1G_matriculas_01_checklist-conversao.png`.

Regras funcionais:

- converter em aluno so habilita quando o checklist obrigatorio estiver completo;
- se faltar dado obrigatorio, a acao principal deve ser pedir/validar dado;
- se o studio exigir pagamento inicial antes da conversao, Matriculas mostra o item `Pagamento inicial` como obrigatorio e pode acionar `Gerar cobranca`, `Enviar Pix/link`, `Abrir cobranca` ou `Marcar pagamento manual` quando permitido;
- Financeiro continua sendo a fonte da verdade do pagamento, cobranca, conciliacao, comprovante, falha, promessa, desconto, estorno e auditoria;
- se o studio exigir contrato ou assinatura antes da conversao, Matriculas mostra bloqueio/pendencia e abre Documentos ou Aprovacoes para resolver;
- primeira aula deve ser escolhida via Agenda/componente de agenda, nao como texto livre;
- ao converter, o CRM cria/atualiza `/app/alunos/[id]` preservando origem, historico de vendas, experimental e pre-matricula.

Estados de pagamento em Matriculas:

- `Nao obrigatorio`: conversao pode seguir e Financeiro cria cobranca depois, conforme politica;
- `Pendente`: bloqueia conversao quando pagamento inicial for obrigatorio;
- `Link enviado`: aguarda confirmacao do Financeiro/gateway;
- `Pago`: libera item de pagamento no checklist;
- `Falhou`: abre cobranca existente ou permite reenviar link;
- `Prometido`: libera conversao apenas se politica/permissao permitirem; senao vira bloqueio ou aprovacao;
- `Aguardando aprovacao`: desconto, valor especial ou condicao sensivel precisam aprovacao antes de seguir.

Metodos de pagamento disponiveis:

- os metodos disponiveis para o aluno sao configurados em Configuracoes/Financeiro, nao em Matriculas;
- exemplos de metodos: Pix, cartao de credito, cartao de debito, dinheiro, transferencia, boleto, link de pagamento e pagamento manual/externo;
- cada metodo pode ter configuracoes proprias: disponivel para matricula, disponivel para mensalidade, confirmacao automatica ou manual, parcelamento, taxa, exigencia de aprovacao, permissao por perfil e uso permitido por agente;
- Matriculas so deve exibir metodos habilitados para o caso atual;
- se o studio aceita apenas Pix e dinheiro para matricula, cartao nao aparece na pre-matricula;
- se dinheiro exige permissao, usuario sem permissao nao pode marcar como pago;
- se cartao esta habilitado para mensalidade mas nao para matricula, nao aparece no pagamento inicial de Matriculas;
- Copiloto pode sugerir metodo ou redigir mensagem de pagamento;
- Autonomo so pode enviar link/Pix quando metodo, politica, template, cota e risco permitirem;
- Autonomo nunca registra pagamento manual sozinho.

Resumo do fluxo comercial ate aluno pago/matriculado:

1. Interessado entra por Vendas, Inbox, cadastro manual ou origem simples.
2. Vendas define etapa, dono/fila, origem, interesse e proxima acao.
3. Se houver aula teste, o interessado agenda Experimental usando horario real da Agenda.
4. Experimental acompanha confirmacao, falta, remarcacao, pos-aula e decisao de continuar.
5. Quando a pessoa quer fechar, `Iniciar matricula` cria pre-matricula em `/app/matriculas`.
6. Matriculas valida dados minimos, plano, data de inicio, primeira aula e pagamento inicial quando exigido.
7. Se pagamento inicial for obrigatorio, Matriculas aciona cobranca, mas Financeiro registra e confirma o pagamento.
8. Quando checklist obrigatorio esta completo, `Converter em aluno` cria/atualiza `/app/alunos/[id]`.
9. O aluno nasce com origem, historico comercial, conversa, experimental, plano, primeira aula e cobranca vinculada quando houver.
10. Depois da conversao, rotina continua em Alunos, Agenda e Financeiro.

## Comunicados

Comunicados nao fazem parte da familia Vendas / Interessados no MVP. Devem virar agente ou superficie separada pos-MVP, com contrato proprio de publico, canal, template, custo, aprovacao, envio, falhas e auditoria.

## Telas mobile

### Interessados

| Campo | Definicao |
| --- | --- |
| Profundidade | Acao parcial/completa. |
| Conteudo | leads quentes, etapa, origem, proxima acao, conversa, experimental, sem vaga. |
| Acoes | responder, criar follow-up, agendar experimental, qualificar, marcar perdido. |
| Estados | novo, quente, sem resposta, sem vaga, experimental agendado. |

### Experimental

| Campo | Definicao |
| --- | --- |
| Profundidade | Acao completa. |
| Conteudo | experimentais do dia, lembrete, presenca/falta, pos-aula, professor, converter. |
| Acoes | lembrar, remarcar, registrar falta, fazer pos-aula, criar follow-up, converter. |
| Estados | lembrete pendente, faltou, remarcada, concluiu, converter agora. |

### Matricula rapida

| Campo | Definicao |
| --- | --- |
| Profundidade | Consulta + aprovacao. |
| Conteudo | dados pendentes, plano escolhido, responsavel quando houver e primeira aula. |
| Acoes | validar pendencia, pedir dado, aprovar conversao, criar tarefa, abrir web quando complexo. |
| Estados | faltando dado, pronto para aluno, bloqueado por conflito. |

## Cobertura de contratos da Rodada 0

| Contrato | Aplicacao nesta rodada |
| --- | --- |
| Dados | Usa interessado, origem simples, experimental, pre-matricula, conversa e plano escolhido. |
| Ciclo de vida | Interessado, experimental e pre-matricula. |
| Fonte da verdade | CRM Vendas para lead/origem; Agenda para experimental; Financeiro/Contratos apenas quando pagamento/contrato forem exigidos. |
| Permissoes | Operacao vende; financeiro/dono aprovam dinheiro, desconto, contrato e envio em massa. |
| Botoes | Cadastrar, qualificar, responder, agendar, remarcar e converter. |
| Estados | Novo, quente, sem resposta, experimental, pre-matricula, perdido, convertido, aguardando aprovacao. |
| Cotas | Follow-up, lembrete e IA comercial devem mostrar consumo e bloqueio. |
| Auditoria | Conversao, origem simples, envio externo, desconto/promessa sensivel. |
| 0 agentes | Pipeline, experimental e matricula manuais funcionam. |

## Decisoes abertas encontradas

| Tema | Encaminhamento |
| --- | --- |
| Etapas oficiais do pipeline | Definir etapas padrao sem engessar studios diferentes. |
| Minimos de pre-matricula | Definir exatamente quais dados obrigatorios bloqueiam conversao por tipo de studio; pagamento inicial ja entra quando exigido pela politica. |
| Cadencia comercial automatica | Definir limite de tentativas, intervalo, horario, tom e parada por opt-out. |
| Comunicados pos-MVP | Criar contrato proprio quando o agente/superficie de Comunicados entrar no produto. |

## Criterio de aceite da rodada

Rodada 5 esta pronta para revisao quando:

- todo interessado tem origem, etapa, dono/fila e proxima acao;
- experimental conecta vendas e agenda com lembrete, falta, remarcacao e pos-aula;
- pre-matricula mostra pendencias de dados, plano escolhido, primeira aula e pagamento inicial quando exigido;
- conversao cria aluno sem perder origem/historico;
- demanda sem horario vira filtro `sem vaga`, lista futura ou tarefa, nao sumico;
- plano Base vende e matricula manualmente sem agentes ativos.
