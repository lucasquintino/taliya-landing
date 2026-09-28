# Decisoes de produto - PT-BR

> Status: fechadas v0.1 na Rodada 11. Este documento centraliza decisoes que nao devem ficar escondidas nos textos; a justificativa completa esta em `round-11-product-closure.pt-BR.md`.

## Regras

- Toda nova decisao aberta precisa ter impacto.
- Se uma rodada encontrar problema fora da sua area, registra aqui.
- Quando houver decisao aberta, ela nao bloqueia tudo, mas impede chamar aquela parte de fechada.
- Na Rodada 11, D001-D037 foram fechadas como premissas v0.1 para design e prompts. Se uma premissa for revista, registrar nova decisao com novo ID.

## Decisoes atuais

| ID | Tema | Pergunta original | Impacto | Rodada dona | Status |
| --- | --- | --- | --- | --- | --- |
| D001 | E14 primeira semana do novo aluno | Virar fluxo de agente proprio ou subfluxo de retencao/B15? | Afeta contagem de fluxos, telas de retencao e onboarding do aluno. | 6 | Fechada v0.1 |
| D002 | G13 gate de anamnese/consentimento/emergencia | Virar fluxo proprio ou gate de historico/setup? | Afeta historico, professor, aula e mobile. | 3/4/6 | Fechada v0.1 |
| D003 | Multi-unidade | MVP assume uma unidade por studio ou prepara unidade sem expor? Premissa provisoria: operar uma unidade e manter objeto preparado. | Afeta dados, permissoes, relatorios e agenda. | 0/1 | Fechada v0.1 |
| D004 | Provedor financeiro do studio | Quais status de pagamento virao de integracao no MVP? | Afeta fonte da verdade, financeiro e cobrancas. | 6 | Fechada v0.1 |
| D005 | Agenda externa | MVP tera integracao de calendario real, importacao ou apenas agenda nativa? | Afeta fonte da verdade e falhas de integracao. | 4/7 | Fechada v0.1 |
| D006 | Dados clinicos/sensiveis | Qual limite entre historico operacional e dado de saude sensivel? | Afeta permissoes, professor, IA e LGPD. | 3/6 | Fechada v0.1 |
| D007 | Retencao de mensagens | Quanto tempo guardar mensagens e resumos? | Afeta privacidade, auditoria, custos e historico. | 3/6/7 | Fechada v0.1 |
| D008 | App mobile e configuracao avancada | Quais configuracoes de agente/politica ficam proibidas no app? | Afeta mobile e seguranca. | 1/7 | Fechada v0.1 |
| D009 | Precos de add-on de cota | Quanto custam pacotes +2k e +5k? | Afeta billing e cotas. | 7 | Fechada v0.1 |
| D010 | Marketing amplo | Comunicados/reativacao bastam no MVP ou ha agente de marketing separado? | Afeta escopo de agentes e custom agent. | 5/6/7 | Fechada v0.1 |
| D011 | Suporte Taliya admin interno | Quais telas internas entram no MVP alem de Sales Inbox? | Afeta operacao interna e suporte. | 7 | Fechada v0.1 |
| D012 | Relatorios do MVP | Quais relatorios profundos entram no primeiro design? | Afeta Rodada 7 e menus. | 7/10 | Fechada v0.1 |
| D013 | Formula de prioridade do Hoje | Quais pesos finais ordenar por risco, prazo, dinheiro, aula do dia, cota e impacto operacional? | Afeta Hoje, mobile, notificacoes e filas. | 2/10 | Fechada v0.1 |
| D014 | Busca global no app | Busca global fica fixa no topo do app ou dentro de Mais/navegacao secundaria? | Afeta navegacao mobile e velocidade operacional. | 2/10 | Fechada v0.1 |
| D015 | Tipos canonicos de caso operacional | Quais tipos de caso viram taxonomia oficial sem criar menus demais? | Afeta Operacao, relatorios, agentes e tela de caso. | 2-7 | Fechada v0.1 |
| D016 | Identidade em telefone compartilhado | Quais validacoes sao obrigatorias antes de expor historico, alterar cadastro, tratar assunto financeiro ou permitir agente responder? | Afeta Inbox, contatos, responsaveis, alunos, historico e agentes. | 3/6/7 | Fechada v0.1 |
| D017 | Visibilidade do historico para professor | Quais campos o professor ve por padrao e quais exigem permissao extra? | Afeta app, aulas, notas, historico sensivel e LGPD. | 3/4/6 | Fechada v0.1 |
| D018 | Classificacao de midia no MVP | MVP tera OCR/transcricao/IA para audio, imagem e documento, ou apenas classificacao manual com sugestao limitada? | Afeta Inbox, documentos, comprovantes, historico, cotas e qualidade de agente. | 3/6/7 | Fechada v0.1 |
| D019 | Compartilhamento seguro de contexto | Quais resumos do historico podem ser enviados ao aluno/responsavel e quais exigem aprovacao? | Afeta historico, WhatsApp, responsaveis, privacidade e auditoria. | 3/6 | Fechada v0.1 |
| D020 | Politica padrao de reposicao | Qual validade, limite mensal, regra de falta avisada, regra de no-show e excecoes entram no MVP? | Afeta agenda, chamada, creditos, lista de espera, financeiro e retencao. | 4/6 | Fechada v0.1 |
| D021 | Formula de encaixe | Qual ranking oficial combina horario, perfil, prioridade, validade do credito, conflito, consentimento e ordem de convite? | Afeta reposicoes, lista de espera, agentes, cotas e experiencia do aluno. | 4/7/10 | Fechada v0.1 |
| D022 | Disponibilidade de professor | MVP tera disponibilidade recorrente completa ou apenas indisponibilidades pontuais e substituicoes? | Afeta agenda, turmas, recursos, app do professor e conflitos. | 4/10 | Fechada v0.1 |
| D023 | Escopo de eventos/workshops | Eventos entram como aula especial simples ou modulo completo com inscricao, lista, pagamento e comunicacao? | Afeta agenda, vendas, financeiro, comunicados e mobile. | 4/5/6 | Fechada v0.1 |
| D024 | Etapas oficiais do pipeline | Quais etapas comerciais padrao entram no MVP sem engessar studios diferentes? | Afeta vendas, automacoes, relatorios, mobile e prompts de tela. | 5/10 | Fechada v0.1 |
| D025 | Minimos de pre-matricula | Quais dados, contrato, pagamento, responsavel e primeira aula bloqueiam converter interessado em aluno? | Afeta matricula, financeiro, agenda, contratos e qualidade de dados. | 5/6 | Fechada v0.1 |
| D026 | Cadencia comercial automatica | Quais limites de tentativa, intervalo, horario, tom e opt-out controlam follow-up autonomo? | Afeta agentes, cotas, WhatsApp, consentimento e vendas. | 5/7 | Fechada v0.1 |
| D027 | Comunicados no MVP | Qual diferenca pratica entre comunicado operacional, campanha, reativacao e marketing amplo? | Afeta segmentos, consentimento, cotas, aprovacoes e escopo do agente. | 5/6/7 | Fechada v0.1 |
| D028 | Assinatura de contrato | Contratos serao upload/manual, assinatura integrada ou apenas controle de status no MVP? | Afeta matricula, financeiro, documentos, mobile e auditoria. | 6/10 | Fechada v0.1 |
| D029 | Formula de retencao | Quais sinais e pesos geram risco sem esconder explicacao do score? | Afeta retencao, Hoje, agentes, relatorios e notificacoes. | 6/7/10 | Fechada v0.1 |
| D030 | Playbook de cancelamento/reclamacao | Quais limites de beneficio, tom, SLA, escalonamento e automacao pausada entram no MVP? | Afeta retencao, financeiro, comunicacao, reputacao e agentes. | 6/7 | Fechada v0.1 |
| D031 | Operacao LGPD | Quais prazos, formato de exportacao, escopo de exclusao/anonimizacao e responsavel legal entram no MVP? | Afeta privacidade, historico, mensagens, auditoria e suporte. | 6/7 | Fechada v0.1 |
| D032 | Qualidade minima para autonomia | Quais thresholds de acerto, erro, handoff, reclamacao e custo liberam modo autonomo por fluxo? | Afeta agentes, evals, incidentes, cotas e confianca do gestor. | 7/10 | Fechada v0.1 |
| D033 | Reprocessamento seguro | Quais execucoes podem ser reprocessadas com idempotencia e quais nunca podem repetir? | Afeta incidentes, integracoes, pagamentos, mensagens e auditoria. | 7/10 | Fechada v0.1 |
| D034 | Severidade de incidente | Quais niveis, SLA, comunicacao, bloqueio automatico e pos-mortem entram no MVP? | Afeta suporte, agentes, integracoes, reputacao e operacao interna. | 7/10 | Fechada v0.1 |
| D035 | Suporte interno Taliya | Quais telas, papeis e limites de acao do admin interno entram no MVP? | Afeta tenants, grants, billing, incidentes, suporte e auditoria. | 7/10 | Fechada v0.1 |
| D036 | Presets iniciais do studio | Quais regras padrao de agenda, reposicao, cobranca, vendas, retencao, mensagens e agentes entram prontas para evitar setup pesado? | Afeta ativacao, primeira semana, entendimento do gestor, seguranca e velocidade de implantacao. | 1/10/11 | Fechada v0.1 |
| D037 | Navegacao final web/app | Como agrupar muitas telas no web e no app sem virar menu infinito, mantendo as rotas completas disponiveis? | Afeta arquitetura de informacao, app mobile, prompts de tela e capacidade do gestor operar no dia a dia. | 2/10/11 | Fechada v0.1 |

## Decisoes resolvidas

| Tema | Decisao |
| --- | --- |
| WhatsApp | Canal do sistema, nao produto inteiro. |
| Plano Base | CRM completo sem agentes ativos. |
| Agentes | Atuam no WhatsApp e dentro do CRM web/app. |
| Referencias visuais | Usar depois do produto fechado para gerar telas no ChatGPT. |
| CRM web vs app | Web aprofunda/governa; app ativa e opera o dia a dia. |
