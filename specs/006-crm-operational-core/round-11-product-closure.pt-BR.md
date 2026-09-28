# Rodada 11 - Fechamento funcional v0.1

> Status: fechamento funcional v0.1 por autonomia. As decisoes abaixo congelam premissas suficientes para gerar telas e prompts finais, mas continuam reversiveis se aparecer uma inconsistencia real de produto.

## Veredito

O Taliya deve seguir como CRM operacional completo para studios de Pilates com agentes de IA integrados.

O produto nao deve ser pensado como "agentes no WhatsApp". WhatsApp e canal. Os agentes vivem dentro do CRM, aparecem no web, no app e no WhatsApp, mas o CRM continua operavel no plano Base com 0 agentes ativos.

Com esta rodada, as decisoes abertas D001-D037 deixam de ser bloqueios de definicao de telas. Elas viram premissas v0.1 para design, prototipo e prompts.

## Decisoes fechadas

| ID | Decisao v0.1 |
| --- | --- |
| D001 | Primeira semana do novo aluno fica como subfluxo de retencao/onboarding do aluno, nao como agente separado. Aparece em Retencao, Aluno, Hoje e tarefas. |
| D002 | Anamnese, consentimento e contato de emergencia viram gate obrigatorio de historico/aula/setup, nao fluxo isolado. Bloqueiam ou restringem acoes quando faltam. |
| D003 | MVP mostra uma unidade por studio. O modelo guarda `unitId` interno para futuro, mas nao expõe multi-unidade na interface inicial. |
| D004 | Financeiro do MVP usa status canonico do Taliya com entrada manual, importacao e integracao opcional. Status: aberto, pago, atrasado, falhou, em disputa, reembolsado, cancelado. |
| D005 | Agenda nativa do Taliya e fonte da verdade. Calendario externo entra como importacao/consulta, sem sincronizacao bidirecional no MVP. |
| D006 | Historico operacional fica separado de dado sensivel de saude. Agentes nao usam dado sensivel bruto; podem usar apenas resumo permitido e auditado. |
| D007 | Conversas ficam visiveis operacionalmente por 24 meses. Depois disso, manter resumo operacional, auditoria e documentos conforme politica configurada e validacao juridica. |
| D008 | App permite setup essencial, pausar/ativar, mudar modo, limite simples e teste de fluxo. Configuracao avancada, politica versionada, permissao e rollback ficam no web. |
| D009 | Tela de cotas suporta pacotes +2k e +5k como produtos configuraveis. Preco nao fica hard-coded nos prompts; vem do billing. |
| D010 | MVP nao tem agente de marketing amplo separado. Comunicados, reativacao e indicacoes cobrem o necessario; marketing amplo fica como evolucao. |
| D011 | Suporte Taliya admin interno e D035 foram unificados. MVP tem console interno minimo: tenants, grants, incidentes, billing de suporte e auditoria. |
| D012 | Relatorios do MVP: semana, financeiro, vendas, ocupacao, retencao, agentes e uso/cotas. Sem BI customizado no primeiro desenho. |
| D013 | Prioridade do Hoje usa score explicavel: severidade, prazo, dinheiro, aula do dia, aluno em risco, humano aguardando, bloqueio de dados/cota e impacto operacional. |
| D014 | Busca global fica acessivel no topo do app como icone/campo compacto em todas as abas principais. Nao fica enterrada apenas em Mais. |
| D015 | Tipos canonicos de caso: atendimento, agenda, reposicao, aula, venda, matricula, financeiro, contrato, retencao, reclamacao, dados, integracao, agente, privacidade, suporte. |
| D016 | Telefone compartilhado exige validar pessoa, relacao com aluno e contexto antes de historico, financeiro, cadastro ou resposta de agente. Acao sensivel pede confirmacao. |
| D017 | Professor ve agenda, chamada, presenca, objetivo resumido, restricao operacional permitida, notas e handoff. Nao ve financeiro, conversa completa ou documento sensivel por padrao. |
| D018 | Midia no MVP tem classificacao manual com sugestao de IA. OCR/transcricao podem sugerir resumo, mas comprovante, documento e dado sensivel exigem revisao humana. |
| D019 | Contexto compartilhado com aluno/responsavel usa resumo seguro. Conteudo sensivel, financeiro delicado ou historico clinico exige aprovacao humana. |
| D020 | Reposicao padrao: falta avisada com 12h gera credito; no-show nao gera credito; credito vale 30 dias; limite padrao de 2 creditos ativos por aluno; excecao humana. |
| D021 | Encaixe e programatico: elegibilidade obrigatoria, conflito de horario, validade do credito, prioridade, tempo de espera, perfil da turma, consentimento e ordem de convite. IA so explica/redige/trata excecao. |
| D022 | Disponibilidade de professor no MVP tem agenda recorrente basica, indisponibilidade pontual e substituicao. Planejamento avancado fica fora. |
| D023 | Eventos/workshops entram como aula especial com capacidade, inscritos, comunicacao e status de pagamento simples. Nao vira modulo completo de eventos no MVP. |
| D024 | Pipeline padrao: Novo, Contato feito, Qualificado, Experimental marcado, Experimental feito, Proposta/matricula, Ganho, Perdido/Sem vaga. |
| D025 | Pre-matricula exige contato validado, aluno/responsavel quando aplicavel, plano, consentimentos, contrato/status, pagamento/status e primeira aula ou pendencia assumida. |
| D026 | Cadencia comercial automatica tem ate 5 tentativas em 14 dias, horario permitido, opt-out respeitado, limite de tom e handoff quando houver objeção sensivel. |
| D027 | Comunicados se dividem em operacional, comercial segmentado, reativacao e marketing amplo. MVP cobre os tres primeiros com consentimento, custo/cota e aprovacao. |
| D028 | Contratos no MVP sao upload/modelo/status/envio manual ou link externo. Assinatura digital nativa nao entra como obrigatoria no primeiro desenho. |
| D029 | Retencao usa score explicavel por queda de frequencia, faltas/no-show, atraso financeiro, reclamacao, primeira semana, inatividade, satisfacao e resposta a contatos. |
| D030 | Cancelamento/reclamacao pausa automacao, cria caso com dono, severidade, SLA e resposta revisada. Beneficio/desconto exige permissao e auditoria. |
| D031 | LGPD no produto cobre solicitacao, validacao de identidade, exportacao, exclusao/anonimizacao, opt-out, prazo, responsavel e auditoria. Validacao juridica externa segue obrigatoria. |
| D032 | Autonomia so libera por fluxo depois de piloto em copiloto, qualidade >= 95%, handoff controlado, 0 incidente severo recente, cota dentro do limite e pausa de emergencia visivel. |
| D033 | Reprocessamento exige idempotencia. Sugestao/read-only pode repetir; mensagem, pagamento, agenda e alteracao sensivel exigem nova aprovacao antes de executar de novo. |
| D034 | Incidentes usam severidade S1 a S4: S1 bloqueia automacao e exige resposta imediata; S2 exige dono e prazo; S3 vira fila; S4 vira melhoria/observacao. |
| D035 | Unificado com D011: suporte interno Taliya so por grant escopado, com prazo, motivo, trilha e visibilidade para o gestor. Sem impersonar sem registro. |
| D036 | Presets iniciais obrigatorios: Conservador, Equilibrado e Crescimento. O usuario escolhe um e pode ajustar depois. |
| D037 | Navegacao final: web com 12 entradas principais; app com 5 abas fixas mais busca global e Mais. Superficies raras entram por contexto, nao por menu principal. |

## Efeito nas telas

- Telas finais podem ser geradas com estas premissas.
- Decisoes sensiveis continuam aparecendo como estados, confirmacoes, permissao e auditoria.
- Nenhuma tela deve depender de IA para funcionar.
- Onde o sistema souber calcular com regra, calcular programaticamente primeiro.
- IA entra para redigir, explicar, resumir, priorizar, sugerir ou executar somente quando governanca permitir.

## Fontes que continuam mandando

| Fonte | Papel |
| --- | --- |
| `page-case-coverage.pt-BR.csv` | Linha a linha dos 157 casos para pagina dona. |
| `web-screen-map.pt-BR.md` | Superficies e rotas web. |
| `mobile-screen-map.pt-BR.md` | Telas e profundidade mobile. |
| `final-navigation-web-app.pt-BR.md` | Navegacao final fechada. |
| `studio-operational-presets.pt-BR.md` | Presets iniciais fechados. |
| `final-screen-contract-matrix.pt-BR.md` | Contrato final por superficie. |

## Proximo uso correto

Usar estes documentos para gerar prompts finais por tela. O prompt deve dizer que o ChatGPT nao pode inventar regra nova, tela nova ou autonomia sensivel fora destas premissas.
