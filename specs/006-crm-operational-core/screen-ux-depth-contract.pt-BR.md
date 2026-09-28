# Contrato de UX, estados e acoes por tela - PT-BR

> Status: contrato final v0.1 de profundidade visual-funcional. Complementa as referencias visuais e impede que telas sejam geradas sem estados, botoes e bloqueios.

## Regra central

Toda tela precisa mostrar:

- objetivo operacional;
- contexto do objeto ou jornada;
- acao primaria;
- acoes secundarias;
- estado atual;
- permissao;
- cota quando IA participa;
- fallback manual;
- auditoria quando a acao e sensivel.

## Hierarquia visual base

| Superficie | Web | App |
| --- | --- | --- |
| Hoje/Operacao | Dashboard denso com jornada, filas e painel lateral. | Lista priorizada com cards acionaveis. |
| Inbox/Conversas | Lista + conversa + painel de contexto. | Conversa com resumo compacto e acoes fixas. |
| Perfil/Aluno | Workspace com abas e timeline. | Perfil resumido com acoes rapidas. |
| Agenda/Turmas | Calendario/grade + detalhes laterais. | Agenda do dia, turma e chamada com toque rapido. |
| Vendas | Pipeline por etapas + painel do interessado. | Lista quente + detalhes e proxima acao. |
| Financeiro | Tabelas/fila + detalhes e impacto. | Fila essencial + aprovacoes. |
| Agentes/Cotas | Console operacional + graficos de uso. | Alertas, pausa, status e acoes simples. |
| Configuracoes | Formulario por secao + impacto/auditoria. | Essencial guiado; avancado envia ao web. |

## Estados globais obrigatorios

| Estado | Mensagem de produto | Acoes |
| --- | --- | --- |
| Vazio | Ainda nao ha itens para esta area. | Criar, importar, configurar ou voltar ao Hoje. |
| Carregando | Buscando dados atualizados. | Skeleton, sem bloquear navegacao. |
| Erro | Nao foi possivel carregar. | Tentar novamente, abrir suporte, ver status. |
| Sem permissao | Seu papel nao permite esta acao. | Pedir acesso, voltar, abrir responsavel. |
| Bloqueado por plano | Este recurso precisa de agente/plano incluido. | Operar manualmente, ver planos, trocar slot quando permitido. |
| Agente nao configurado | O agente existe, mas ainda precisa setup. | Configurar, testar, manter manual. |
| Agente pausado | Automacao pausada por usuario, incidente ou cota. | Ver motivo, retomar se permitido, manter manual. |
| Cota 70% | Uso alto. | Ver origem, ativar economia. |
| Cota 90% | Economia ativa. | Pausar baixa prioridade, comprar pacote. |
| Cota 100% | Automacao paga bloqueada. | Caminho manual, pacote/upgrade. |
| Dado incompleto | Falta dado para executar. | Corrigir dado, criar tarefa, continuar manual. |
| Integracao falhou | Provedor indisponivel ou erro de canal. | Reprocessar seguro, criar incidente, acao manual. |
| Acao sensivel | Impacto precisa confirmacao. | Revisar antes/depois, aprovar/rejeitar. |

## Acoes por tipo

| Tipo | Exemplos | Posicao | Confirmacao |
| --- | --- | --- | --- |
| Primaria operacional | Responder, fazer chamada, aprovar, encontrar encaixe | Topo ou footer fixo no app | Quando externa/sensivel |
| Secundaria | Criar tarefa, comentar, abrir origem, filtrar | Contextual | Normalmente nao |
| Copiloto | Pedir sugestao, resumir, explicar, redigir | Perto da acao humana | Mostra cota/preview |
| Autonoma | Executar fluxo seguro, enviar lembrete permitido | Fluxo publicado/acao explicita | Preflight antes de ativar |
| Destrutiva/sensivel | Estornar, alterar permissao, apagar/anonimizar, pausar automacao | Separada visualmente | Sempre |
| Upgrade/plano | Ver planos, trocar agente, comprar pacote | Estado bloqueado/uso | Billing confiavel |

## Contrato por familia de tela

| Familia | Acao primaria | Copiloto | Autonomo | Estados criticos |
| --- | --- | --- | --- | --- |
| Onboarding | Continuar setup | Sugerir preset/config | Nao | incompleto, importacao com erro, agente nao configurado |
| Hoje | Abrir item prioritario | Explicar prioridade | Criar tarefa segura | cota, risco, aguardando humano |
| Inbox | Responder/assumir | Rascunho/resumo | Resposta segura se permitido | opt-out, identidade, falha envio |
| Alunos | Abrir perfil/acao rapida | Resumo permitido | Nao | sem permissao, dado sensivel |
| Agenda | Abrir aula/turma | Explicar conflito | Lembrete seguro | conflito, vaga, professor indisponivel |
| Chamada | Marcar presenca | Sugerir observacao | Nao | chamada pendente, no-show |
| Reposicao | Encontrar encaixe | Redigir convite | Convite seguro | credito vencido, sem vaga |
| Vendas | Proxima acao | Rascunho/objecao | Follow-up seguro | opt-out, sem vaga |
| Financeiro | Abrir cobranca/caso | Rascunho controlado | Lembrete simples | atraso, disputa, permissao |
| Retencao | Abrir caso/tarefa | Sugestao de abordagem | Contato seguro | reclamacao, cancelamento |
| Operacao | Assumir/mover caso | Priorizar/resumir | Tarefa segura | sem dono, bloqueado |
| Agentes | Configurar/pausar | Sugerir config | Fluxo seguro | bloqueado por plano, incidente |
| Uso/cotas | Ver consumo/pacote | Explicar origem | Nao | 70, 90, 100 |
| Configuracoes | Salvar/testar | Sugerir impacto | Nao | mudanca sensivel |
| Privacidade/auditoria | Validar/filtrar | Checklist permitido | Nao | LGPD, grant ativo |

## Regra de referencia visual

As referencias Dribbble devem influenciar composicao:

- cards por jornada;
- linha do tempo;
- paineis laterais;
- indicadores compactos;
- visual premium de CRM.

Elas nao podem mudar:

- regra de negocio;
- permissoes;
- cotas;
- autonomia;
- fluxo manual;
- nomenclatura dos objetos.

## Aceite

Uma tela esta pronta para prompt final quando:

- tem estado vazio, loading, erro, sem permissao e bloqueado por plano;
- tem botao manual equivalente;
- tem botao/copiloto apenas se agente e cota permitirem;
- tem confirmacao para acao externa ou sensivel;
- mostra de forma discreta mas clara por que algo esta bloqueado.
