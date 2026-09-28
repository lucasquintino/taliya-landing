# Mapa De Perguntas Do Setup

Status: rascunho consolidado.
Data: 2026-05-14.

## Objetivo

Traduzir configuracoes tecnicas em perguntas simples para o gestor.

O usuario nao deve configurar chaves tecnicas. Ele responde apenas o que o sistema nao consegue saber sozinho e o que muda o caminho imediato do setup.

## Regra De Experiencia

Cada pergunta deve:

- usar linguagem operacional do studio;
- evitar termos tecnicos quando possivel;
- ter preset recomendado;
- gerar configuracao estruturada, nao texto solto;
- existir apenas se a resposta muda uma etapa, um default ou uma validacao importante.

Nao perguntar:

- algo que vem do plano contratado;
- algo que ja e default do sistema;
- algo que sera decidido naturalmente quando a tela especifica aparecer;
- algo que so personaliza o CRM, mas nao impede o primeiro uso.

## Inicio Do Setup

| Pergunta para o gestor | Configuracao gerada | Desvio/impacto |
|---|---|---|
| Qual e o nome do studio? | `studio.name` | Primeira pergunta do `/onboarding`; necessaria para criar o workspace operacional. |
| Esse e o studio/unidade principal? | `unit.primary` | Default: sim. So abre unidade extra se o usuario informar que opera mais de uma. |
| Quer agendar uma chamada com a Taliya para acompanhar o setup? | `setup.support_call_requested` | Opcional; nao muda etapas e nao cria fluxo paralelo. |

Depois que o usuario informa o nome do studio, o painel do Agente de Configuracao aparece, da boas-vindas e explica seu papel.

## Diagnostico

O diagnostico existe para definir bons defaults e preparar o caminho. Ele nao configura o CRM profundamente.

Contrato visual e funcional da pagina:

- [setup-diagnostico-page-contract.pt-BR.md](./setup-diagnostico-page-contract.pt-BR.md)

| Pergunta | Configuracao gerada | Desvio/impacto |
|---|---|---|
| Quantos alunos ativos o studio tem hoje? | `diagnostic.active_students_range` | Ajusta volume esperado, importacao, revisao de conflitos e recomendacao de ajuda humana. |
| Onde estao agenda, turmas ou horarios hoje? | `diagnostic.schedule_source` | Prepara defaults para importacao de agenda/turmas sem perguntar se quer importar agora. |
| Onde estao alunos, planos e contatos hoje? | `diagnostic.student_data_source` | Prepara defaults para importacao de alunos/planos sem perguntar se quer importar agora. |
| Quais tipos de planos o studio oferece pro aluno? | `diagnostic.offered_plan_types` | Prepara a criacao de varios planos em Consumo de aulas, sem configurar cada plano ainda. |
| Como o studio lida com reposicoes? | `diagnostic.replacement_handling` | Pre-seleciona defaults de reposicao em Consumo de aulas, sem configurar regras finais. |

Nao perguntar no diagnostico:

- se o plano tem agentes, porque isso vem de Billing/Entitlements;
- se quer importar dados agora, porque essa decisao acontece na pagina `/onboarding/importacao`;
- se trabalha com turmas/horarios fixos, porque agenda/turmas ja sao comportamento padrao do sistema;
- se usa WhatsApp para falar com alunos, porque isso e assumido como canal comum e a conexao aparece no bloco de canais;
- quantas pessoas vao usar o Taliya, porque equipe e convites ficam no setup essencial;
- quais areas quer configurar primeiro, porque o Setup Inicial tem sequencia definida.

## Setup Essencial

Estas perguntas aparecem em `/onboarding/setup`, dentro de blocos curtos.

### Studio

| Pergunta | Configuracao gerada | Desvio/impacto |
|---|---|---|
| Qual e o horario geral de funcionamento? | `studio.business_hours` | Afeta agenda, aulas, tarefas e mensagens. |
| O studio tem mais de uma unidade? | `studio.has_multiple_units` | Se sim, libera unidade adicional minima; detalhes ficam para pos-go-live. |

### Equipe

| Pergunta | Configuracao gerada | Desvio/impacto |
|---|---|---|
| Quais pessoas precisam acessar o Taliya agora? | `team.initial_users` | Cria convites basicos e papeis padrao. |

### Agenda Base

| Pergunta | Configuracao gerada | Desvio/impacto |
|---|---|---|
| Quais tipos de aula o studio oferece? | `agenda.class_types` | Base para turmas e aulas. |
| Quer cadastrar a grade minima agora ou deixar para importacao? | `agenda.setup_source_choice` | Escolha da propria etapa; nao vem do diagnostico. |

### Canais

| Pergunta | Configuracao gerada | Desvio/impacto |
|---|---|---|
| Qual e o WhatsApp principal do studio? | `channels.primary_whatsapp` | Canal principal de contato; conectar envio externo pode ficar para depois. |
| Quer conectar o WhatsApp agora? | `channels.whatsapp_connected` | Opcional. Se nao conectar, CRM segue manual. |

## Importacao

A importacao deve acontecer uma por vez.

| Pergunta | Configuracao gerada | Desvio/impacto |
|---|---|---|
| O que voce quer importar agora? | `data.current_import_domain` | Escolhe um dominio por vez: alunos, agenda, turmas, planos, contatos ou financeiro basico. |
| De onde vem este dado? | `data.import_source_type` | Define planilha, Google Agenda, sistema antigo, foto, PDF, caderno, print ou digitacao manual. |
| O material desta importacao tem quais informacoes? | `data.import_scope` | Define mapeamento e pendencias apenas para a importacao atual. |
| Quer que o agente ajude a transformar foto, PDF ou anotacao em rascunho revisavel? | `data.unstructured_extraction_requested` | Usa extracao assistida, mas exige revisao antes de importar. |

Observacao: dados extraidos de foto, PDF, caderno, print ou anotacao informal devem mostrar origem e confianca por campo. Campo duvidoso nao deve ser publicado sem confirmacao do dono.

## Consumo De Aulas E Planos

A pagina `/onboarding/configuracoes/consumo-aulas` deve permitir criar varios planos e configurar cada plano individualmente.

Perguntas do nivel do studio:

| Pergunta | Configuracao gerada | Desvio/impacto |
|---|---|---|
| Qual modelo o studio usa na maioria dos casos? | `billing.default_model_type` | Pre-seleciona o tipo ao criar novos planos. |
| O studio permite reposicao? | `replacement.enabled_default` | Default aplicado aos planos, editavel por plano. |

Perguntas por plano:

| Pergunta | Configuracao gerada | Desvio/impacto |
|---|---|---|
| Qual e o nome do plano? | `plans[].name` | Exemplo: 2x por semana, 8 aulas, Mensalidade livre. |
| Esse plano e mensalidade, pacote, hibrido ou avulso? | `plans[].model_type` | Define os campos exibidos para aquele plano. |
| Quantas aulas o aluno tem direito neste ciclo/pacote? | `plans[].lesson_entitlement.amount` | Necessario para saldo, chamada e reposicao. |
| Qual e o ciclo ou validade? | `plans[].validity_rule` | Mensal, semanal, por pacote ou data fixa. |
| Quando a aula e consumida? | `plans[].consumption_trigger` | Presenca, reserva, falta sem aviso ou ajuste manual. |
| Este plano permite reposicao? | `plans[].replacement.enabled` | Pode herdar default do studio ou ser diferente por plano. |
| Qual prazo para usar reposicao neste plano? | `plans[].replacement.expiration` | Apenas se reposicao estiver ativa. |

## Defaults Operacionais

Estas regras nao devem virar perguntas no Setup Inicial. O sistema aplica defaults conservadores e deixa ajustes para depois:

- tarefas de agenda ficam com dono/admin ate a equipe ajustar;
- tarefas financeiras ficam com dono/admin ate a equipe ajustar;
- aprovacoes sensiveis ficam com dono/admin;
- checklists diarios usam o pacote padrao;
- permissoes finas ficam para pos-go-live;
- feriados/recessos ficam para ajuste posterior ou importacao;
- salas/equipamentos ficam para ajuste posterior, salvo se aparecerem nos dados importados;
- tom de mensagem, templates completos e campanhas ficam para pos-go-live.

## Agentes E Fluxos

Nao ha perguntas de configuracao de agentes no Setup Inicial.

Agentes disponiveis, slots e entitlements vem do plano contratado. O setup inicial nao pergunta se o plano tem agentes, nao escolhe agentes livremente, nao pergunta modo manual/copiloto/autonomo por fluxo, limite de tentativas, cota por fluxo, condicoes de aprovacao detalhadas ou simulacao final. Esses pontos pertencem a Agentes/Fluxos depois do go-live.

## Revisao

| Pergunta | Configuracao gerada | Desvio/impacto |
|---|---|---|
| Quer publicar o setup inicial agora? | `publish.initial_setup` | Publica apenas camadas prontas e aprovadas. |
| Quer revisar o que ficou para pos-go-live? | `publish.post_go_live_pending_review` | Mostra Agentes/Fluxos, regras finas, cotas, simulacao e control planes como proximos passos quando convem. |

## Aceite

Este mapa esta correto quando:

- cada pergunta gera configuracao estruturada;
- cada pergunta muda uma etapa, default ou validacao real;
- perguntas obvias ou conhecidas pelo sistema foram removidas;
- perguntas avancadas nao travam caminho principal;
- a opcao de chamada humana nao altera a arvore do setup.
