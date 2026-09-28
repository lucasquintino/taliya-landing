# Inventario De Configuracoes Do Setup

Status: rascunho consolidado.
Data: 2026-05-13.

## Objetivo

Listar tudo que pode ser configurado no setup e decidir o que entra no MVP, o que vira default, o que fica avancado e o que sai.

Importante: este documento e um inventario interno de configuracoes candidatas e fontes da verdade. Ele **nao** e uma lista de campos, telas ou opcoes que o cliente deve ver no onboarding.

O escopo visivel do Setup Inicial e definido por:

- [setup-initial-configuration-scope.pt-BR.md](./setup-initial-configuration-scope.pt-BR.md)

Regra: uma configuracao so aparece para o cliente no Setup Inicial se for necessaria para operar com seguranca no primeiro uso. Caso contrario, deve virar default, preset, pendencia rastreavel ou configuracao pos-go-live.

Este inventario segue o contrato:

- uma regra, uma fonte da verdade;
- se nao tem impacto real, nao entra;
- se e sensivel, exige validacao;
- se e avancado demais, nao aparece no caminho principal;
- CRM precisa funcionar com 0 agentes.

## Legenda

| Campo | Significado |
|---|---|
| Setup | `Setup essencial`, `Setup se aplicavel`, `Default`, `Pos-go-live`, `Avancado`, `Pos-MVP`, `Remover` |
| Sensivel | Exige impacto, permissao, confirmacao e auditoria |
| Publicacao | Camada onde a regra entra: CRM, Agenda, Financeiro, Canais, Politicas, Agentes |

Leitura dos status:

- `Setup essencial`: aparece no caminho principal porque sem isso o CRM nao opera com seguranca.
- `Setup se aplicavel`: aparece apenas se uma resposta anterior tornar a decisao necessaria.
- `Default`: o sistema define sozinho com preset seguro; o usuario ajusta depois se precisar.
- `Pos-go-live`: nao aparece no onboarding; fica em Configuracoes, Agentes/Fluxos ou Control Planes depois que o CRM estiver rodando.
- `Avancado`: existe no produto, mas nao deve ser parte do caminho principal.
- `Pos-MVP`: nao entra agora.
- `Remover`: nao deve virar superficie dedicada.

## Base Do Studio

| Configuracao | Fonte da verdade | Setup | Sensivel | Publicacao | Impacto |
|---|---|---|---|---|---|
| Nome do studio/workspace | Configuracoes/Studio | Setup essencial | Nao | CRM | App shell, documentos, mensagens, relatorios |
| Unidades | Configuracoes/Studio | Setup se aplicavel | Medio | CRM | Agenda, financeiro, relatorios, equipe |
| Horario comercial | Configuracoes/Studio | Setup essencial | Medio | CRM | Agenda, WhatsApp, agentes, tarefas |
| Feriados/recessos simples | Configuracoes/Agenda | Default | Medio | Agenda | Agenda, aulas, reposicoes, comunicados |
| Salas/recursos basicos | Configuracoes/Agenda | Default | Medio | Agenda | Turmas, aulas, conflitos |
| Equipe inicial | Configuracoes/Equipe | Setup essencial | Medio | CRM | Tarefas, responsaveis, permissoes |
| Papeis padrao | Configuracoes/Permissoes | Default | Sim | CRM | Todas as acoes sensiveis |
| Permissoes finas | Configuracoes/Permissoes | Pos-go-live | Sim | Politicas | Financeiro, agentes, auditoria |
| Notificacoes de gestor | Configuracoes/Notificacoes | Default | Nao | CRM | Hoje, aprovacoes, cotas, incidentes |
| Tags/campos simples | Configuracoes/Campos | Pos-go-live | Nao | CRM | Alunos, vendas, filtros |
| Campos customizados profundos | Configuracoes/Campos | Pos-MVP | Depende | CRM | Relatorios, importacao |

## Agenda, Aulas E Reposicoes

| Configuracao | Fonte da verdade | Setup | Sensivel | Publicacao | Impacto |
|---|---|---|---|---|---|
| Tipos de aula | Configuracoes/Agenda | Setup essencial | Nao | Agenda | Agenda, turmas, alunos |
| Turmas iniciais | Agenda/Turmas | Setup essencial | Medio | Agenda | Agenda, alunos, chamada |
| Professor por turma/aula | Agenda/Turmas | Setup se aplicavel | Medio | Agenda | Chamada, substituicao, tarefas |
| Capacidade por turma | Agenda/Turmas | Setup essencial | Medio | Agenda | Vagas, lista de espera, reposicao |
| Capacidade analitica/gargalos | Relatorios/Operacao | Remover do MVP como rota | Nao | N/A | Pode aparecer como indicador |
| Chamada/presenca | Configuracoes/Agenda | Default | Medio | Agenda | Consumo, historico, aluno |
| Falta avisada | Configuracoes/Agenda | Default | Sim | Agenda | Reposicao, consumo, financeiro |
| Falta fora do prazo | Configuracoes/Agenda | Default | Sim | Agenda | Reposicao, no-show, aprovacao |
| No-show | Configuracoes/Agenda | Default | Sim | Agenda | Consumo, retencao, financeiro |
| Reposicao | Configuracoes/Agenda | Setup essencial | Sim | Agenda | Hoje, agenda, aluno, agentes |
| Lista de espera | Configuracoes/Agenda | Pos-go-live | Medio | Agenda | Encaixe, vendas, reposicao |
| Encaixe automatico/programatico | Configuracoes/Agenda | Pos-go-live | Medio | Agenda | Reposicoes, Hoje, agente Agenda |
| Bloqueios de agenda | Configuracoes/Agenda | Pos-go-live | Medio | Agenda | Aula, turma, professor, sala |

## Financeiro, Cobranca E Consumo

| Configuracao | Fonte da verdade | Setup | Sensivel | Publicacao | Impacto |
|---|---|---|---|---|---|
| Modelo de cobranca | Configuracoes/Financeiro/Modelos | Setup essencial | Sim | Financeiro | Financeiro, aluno, agenda |
| Direito de aula | Configuracoes/Agenda/Consumo | Setup essencial | Sim | Financeiro/Agenda | Chamada, reposicao, aluno |
| Regra de consumo | Configuracoes/Agenda/Consumo | Setup essencial | Sim | Financeiro/Agenda | Presenca, falta, credito |
| Politica de reposicao | Configuracoes/Agenda | Setup essencial | Sim | Agenda | Reposicao, agentes, aprovacoes |
| Planos vendidos | Financeiro/Planos do studio | Setup essencial | Sim | Financeiro | Alunos, cobrancas, contrato |
| Vencimentos e recorrencia | Configuracoes/Financeiro | Setup essencial | Sim | Financeiro | Hoje, movimentacoes, cobrancas |
| Metodos de pagamento MVP | Configuracoes/Financeiro | Setup essencial | Medio | Financeiro | Pix, dinheiro, cartao |
| Dados minimos de recebimento inicial | Configuracoes/Financeiro | Setup essencial | Sim | Financeiro | Meios aceitos: Pix, dinheiro, cartao |
| Baixa manual/comprovante | Financeiro/Movimentacoes | Default do sistema | Medio | Financeiro | Comprovante sempre permitido; operacao inicial sem automacao profunda |
| Simulacao operacional de pagamento | Onboarding/Pagamento | Setup essencial | Sim | Financeiro | Mostra cobranca gerada por plano, pagamento, baixa e liberacao de aula/saldo |
| Explicacao de automacao financeira futura | Configuracoes/Financeiro/Pagamentos | Setup orientativo | Sim | Integracoes/Financeiro | Explica Pix conectado, cartao online, recorrencia automatica e webhooks sem configurar no setup |
| Pagamentos Taliya | Configuracoes/Financeiro/Pagamentos | Pos-go-live | Sim | Integracoes/Financeiro | Pix conectado, cartao online, recorrencia automatica, webhooks |
| Conexao de provedor de pagamento | Integracoes/Financeiro | Pos-go-live | Sim | Integracoes/Financeiro | Subconta/recebedor, KYC, webhook, baixa automatica |
| Inadimplencia/tolerancia | Configuracoes/Financeiro | Default | Sim | Financeiro | Agenda, reposicao, agente Financeiro |
| Promessa de pagamento | Configuracoes/Financeiro | Pos-go-live | Medio | Financeiro | Kanban, tarefas, agente Financeiro |
| Desconto/cortesia/estorno | Politicas + Financeiro | Avancado | Sim | Politicas | Aprovacoes, auditoria |
| Quebra-galho financeiro | Politicas + Financeiro | Pos-go-live | Sim | Politicas | Aprovacoes, tarefas, aluno |
| Gateway financeiro completo | Integracoes/Financeiro | Pos-MVP se nao houver provedor | Sim | Integracoes | Conciliacao e pagamentos |

## Alunos E Dados

| Configuracao | Fonte da verdade | Setup | Sensivel | Publicacao | Impacto |
|---|---|---|---|---|---|
| Importacao de alunos | Importacao | Setup se aplicavel | Medio | CRM | Alunos, agenda, financeiro |
| Importacao de agenda/turmas | Importacao/Agenda | Setup se aplicavel | Medio | Agenda | Agenda, turmas, vinculos |
| Fonte digital estruturada | Importacao | Setup se aplicavel | Medio | CRM | Planilhas, CSV, exportacao de sistema |
| Fonte digital integrada | Integracoes/Importacao | Setup se aplicavel | Sim | CRM/Agenda | Google Agenda ou fonte externa conectada |
| Fonte fisica/informal | Importacao assistida | Setup se aplicavel | Medio/Sim | CRM | Foto de caderno/ficha, PDF, print, anotacao |
| Confianca por campo extraido | Importacao assistida | Setup essencial quando fonte nao estruturada | Sim | CRM | Revisao antes de publicar |
| Revisao obrigatoria do dono | Importacao assistida | Setup essencial quando fonte nao estruturada | Sim | CRM | Evita chute do agente |
| Mapeamento de campos | Importacao | Default | Medio | CRM | Qualidade de dados |
| Duplicidades | Qualidade de dados | Setup se aplicavel | Medio | CRM | Alunos, responsaveis, financeiro |
| Status inicial do aluno | Alunos | Default | Medio | CRM | Retencao, financeiro, agenda |
| Vinculo aluno-plano | Financeiro/Alunos | Setup essencial | Sim | Financeiro | Consumo, cobranca, reposicao |
| Vinculo aluno-turma | Agenda/Alunos | Setup essencial | Medio | Agenda | Chamada, vagas, reposicao |
| Historico importado | Historico | Pos-go-live | Sim | CRM | Perfil, professor, retencao |
| Dados clinicos/sensiveis profundos | Historico sensivel | Pos-MVP | Sim | CRM | Permissao, privacidade |

## Canais, Modelos De Mensagem E Comunicacao

| Configuracao | Fonte da verdade | Setup | Sensivel | Publicacao | Impacto |
|---|---|---|---|---|---|
| WhatsApp conectado | Integracoes/Canais | Setup se aplicavel | Sim | Canais | Inbox, agentes, mensagens |
| E-mail | Integracoes/Canais | Setup se aplicavel | Medio | Canais | Documentos, billing, comunicados |
| Janela de envio | Configuracoes/Canais | Default | Sim | Canais | Agentes, mensagens, cotas |
| Tom de voz | Configuracoes/Templates | Pos-go-live | Medio | Canais | Sugestoes, modelos de mensagem |
| Modelos de mensagem principais | Configuracoes/Templates | Default | Sim | Canais | Atendimento, agenda, financeiro |
| Opt-out/consentimento | Privacidade | Setup se aplicavel | Sim | Politicas | WhatsApp, comunicados, agentes |
| Comunicados em massa | Segmentos/Comunicados | Pos-MVP como rotina avancada | Sim | Politicas | Vendas, retencao, cotas |

## Rotinas Operacionais Sem Agente

| Configuracao | Fonte da verdade | Setup | Sensivel | Publicacao | Impacto |
|---|---|---|---|---|---|
| Tarefas padrao | Configuracoes/Operacao | Default | Nao | CRM | Hoje, tarefas, operacao |
| Checklists padrao | Configuracoes/Operacao | Default | Nao | CRM | Hoje, checklists |
| Aprovacoes sensiveis | Politicas/Aprovacoes | Default | Sim | Politicas | Aprovacoes, agentes, financeiro |
| Filas operacionais | Configuracoes/Operacao | Default | Nao | CRM | Hoje, operacao, relatorios |

## Agentes E Fluxos

| Configuracao | Fonte da verdade | Setup | Sensivel | Publicacao | Impacto |
|---|---|---|---|---|---|
| Agentes disponiveis no plano | Billing/Entitlements | Default | Sim | Agentes | Todas as areas com IA |
| Slot de agente escolhido | Agentes | Default | Sim | Agentes | Rotas por dominio |
| Responsavel humano por dominio | Agentes | Default | Medio | Agentes | Tarefas, handoff e caminho manual |
| Pacotes de fluxos recomendados | Agentes/Fluxos | Default como rascunho/pendencia | Medio | Agentes | Proxima configuracao pos-go-live |
| Fluxo ativo/inativo | Fluxos | Pos-go-live | Sim | Agentes | Agentes, operacao, cotas |
| Modo manual/copiloto/autonomo | Fluxos | Pos-go-live | Sim | Agentes | Autonomia, aprovacoes |
| Responsavel/fila de fallback por fluxo | Fluxos | Pos-go-live | Medio | Agentes | Tarefas, incidentes |
| Aprovador por acao/fluxo | Politicas/Aprovacoes | Pos-go-live em fluxo sensivel | Sim | Politicas | Aprovacoes |
| Limite de tentativas | Fluxos | Pos-go-live | Medio | Agentes | Cotas, incidentes |
| Janela por fluxo | Fluxos/Canais | Pos-go-live | Medio | Agentes | Mensagens |
| Simulacao de fluxo | Fluxos/Simulador | Pos-go-live antes de autonomia | Sim | Agentes | Publicacao |
| Execucao/trace | Execucoes/Control Planes | Default pos-go-live | Sim | Auditoria | Incidentes, auditoria |

## Politicas, Cotas, Integracoes E Governanca

| Configuracao | Fonte da verdade | Setup | Sensivel | Publicacao | Impacto |
|---|---|---|---|---|---|
| Regra de seguranca/politica operacional ativa | Politicas | Default | Sim | Politicas | Agentes, CRM, auditoria |
| Versao de politica | Politicas | Default | Sim | Politicas | Execucoes, rollback |
| Limite de uso/cota | Uso/Cotas | Default | Sim | Agentes | Cotas, economia |
| Economia 70/90/100 | Uso/Cotas | Default | Sim | Agentes | Hoje, agentes, execucoes |
| Billing Taliya | Billing | Fora do setup operacional | Sim | Billing | Entitlement |
| Integracoes tecnicas | Integracoes | Setup se aplicavel | Sim | Integracoes | Canais, importacao, financeiro |
| Auditoria | Auditoria | Default obrigatorio | Sim | Auditoria | Todas as acoes sensiveis |
| Privacidade/LGPD | Privacidade | Default | Sim | Politicas | Mensagens, dados, exportacao |

## Corte MVP Do Inventario

Este corte descreve o que o produto precisa suportar no MVP. Ele nao significa que tudo deve ser configuravel pelo cliente durante o Setup Inicial.

Para a superficie visivel do onboarding, aplicar sempre o contrato:

- `Setup essencial`: perguntar/configurar no caminho principal.
- `Setup se aplicavel`: mostrar apenas se o diagnostico indicar necessidade.
- `Default`: salvar com preset seguro sem perguntar.
- `Pos-go-live`: encaminhar para Configuracoes, Agentes/Fluxos ou Control Planes depois que o CRM estiver operando.

### Entra no caminho principal

- base do studio;
- unidade apenas se houver mais de uma;
- horario geral;
- equipe minima;
- papeis padrao por default;
- agenda/turmas/professores/capacidade por turma;
- regra base de reposicao;
- falta/no-show apenas como preset necessario para consumo;
- modelo de cobranca;
- metodos de pagamento iniciais;
- dados minimos de recebimento;
- registro manual de pagamento ou provedor conectado quando aplicavel;
- direito e consumo de aula;
- varios planos por studio, com configuracao individual por plano;
- importacao e vinculo aluno-plano/turma;
- canal principal e WhatsApp apenas quando aplicavel;
- opt-out apenas quando houver envio externo;
- modelos de mensagem essenciais como preset;
- agentes apenas informados/preparados por default quando o plano incluir agente;
- responsaveis humanos e pacotes recomendados como default/rascunho/pendencia;
- regras de seguranca/aprovacoes como default conservador.

### Entra como default ou preset

- permissoes por papel;
- notificacoes basicas;
- filas operacionais;
- tarefas/checklists padrao;
- chamada/presenca;
- falta avisada;
- no-show;
- tolerancia simples de inadimplencia;
- janela de envio;
- modelos essenciais de mensagem;
- politicas/auditoria/privacidade basicas;
- cotas/limites iniciais quando houver agente.

### Entra como pos-go-live ou avancado

- tags/campos simples;
- campos customizados profundos;
- permissoes finas;
- ajustes financeiros complexos;
- quebras-galho sensiveis;
- historico importado detalhado;
- lista de espera;
- encaixe automatico;
- bloqueios complexos de agenda;
- tom de voz e templates completos;
- simulacoes detalhadas por fluxo;
- modo, limite, cota por fluxo, fallback detalhado e publicacao de fluxo;
- configuracao granular de modelos de mensagem.

### Fica pos-MVP ou sem rota dedicada

- gargalos/capacidade como rota dedicada;
- comunicados em massa avancados;
- campanhas complexas;
- gateway financeiro completo se nao houver provedor no MVP;
- dado clinico/sensivel profundo;
- relatorios customizados.

## Aceite

Este inventario esta correto quando:

- toda configuracao tem dono;
- toda configuracao tem impacto;
- nenhuma configuracao essencial depende de agente;
- regras sensiveis foram marcadas;
- configuracoes sem impacto foram removidas ou movidas para pos-MVP;
- 0/1/3/7 agentes continuam cobertos.
