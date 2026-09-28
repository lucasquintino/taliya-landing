# Matriz de fonte da verdade - PT-BR

> Status: Rodada 0 v0.1. Este documento define quem manda em cada dado quando existem CRM, WhatsApp, importacao, integracao, agente e edicao manual.

## Regra central

O CRM Taliya e a fonte operacional de verdade depois que o studio esta ativo. Integracoes e importacoes podem alimentar dados, mas nao devem sobrescrever informacoes criticas sem regra de conflito, permissao e auditoria.

## Matriz

| Dado | Fonte da verdade | Fontes de entrada | Regra de conflito |
| --- | --- | --- | --- |
| Status do tenant | Billing Taliya | checkout, pagamento, admin Taliya | Billing vence; CRM apenas reflete. |
| Plano Taliya e agentes incluidos | Billing/entitlements Taliya | assinatura, add-on, admin Taliya | Entitlement vence; fluxo bloqueia quando plano nao cobre. |
| Perfil do studio | CRM configuracoes | onboarding, app, importacao manual | Edicao manual autorizada vence importacao antiga. |
| Membros e papeis | CRM permissoes | convite, admin, suporte autorizado | Dono/admin vence; suporte nao altera sem autorizacao. |
| Contato | CRM contatos | WhatsApp, importacao, formulario, edicao manual | Duplicidade vira Qualidade de dados; nao mesclar automaticamente em baixa confianca. |
| Consentimento/opt-out | CRM privacidade | WhatsApp, formulario, acao manual | Opt-out mais restritivo vence. |
| Responsavel | CRM contatos/alunos | importacao, manual, conversa | Validacao humana vence sugestao de agente. |
| Aluno | CRM alunos | matricula, importacao, edicao manual | CRM vence; importacao cria revisao quando diverge. |
| Interessado | CRM vendas | landing, WhatsApp, formulario, manual, importacao | Strong identifiers podem mesclar; sinais fracos pedem revisao. |
| Plano vendido ao aluno | CRM financeiro | cadastro manual, importacao, checkout do studio | Financeiro autorizado vence; agente apenas sugere. |
| Turma/grade | CRM agenda | configuracao, importacao, edicao manual | Agenda CRM vence; mudanca ampla exige impacto. |
| Aula | CRM agenda | grade recorrente, ajuste manual, integracao calendario | Ajuste manual autorizado vence recorrencia. |
| Presenca/chamada | CRM aula | professor, recepcao, aluno via WhatsApp, agente | Chamada humana/correcao auditada vence classificacao automatica. |
| Reposicao | CRM agenda/reposicoes | falta, pedido WhatsApp, manual | Politica vigente + decisao autorizada vencem sugestao. |
| Pagamento do aluno | CRM financeiro ou provedor financeiro conectado | provedor, comprovante, manual | Provedor confirmado vence; comprovante manual fica em analise. |
| Cobranca | CRM financeiro | agente, manual, provedor | CRM controla status; provedor informa entrega/pagamento. |
| Contrato | CRM documentos/contratos | assinatura, upload, manual | Documento assinado e provedor de assinatura vencem rascunho. |
| Historico do aluno | CRM historico | professor, sistema, documento, agente | Registro auditado nao e sobrescrito; correcao cria novo evento. |
| Restricao/cuidado | CRM historico sensivel | professor, responsavel, documento | Humano autorizado valida; agente nao cria decisao clinica sozinho. |
| Conversa | CRM inbox | WhatsApp, operador, agente | Provedor e CRM compartilham; CRM controla estado operacional. |
| Mensagem enviada | Provedor + CRM SendAttempt | agente, operador, sistema | Idempotencia por providerMessageId/idempotencyKey. |
| Caso operacional | CRM operacao | agente, usuario, sistema, integracao | CRM e fonte; agente pode abrir/atualizar conforme modo. |
| Tarefa | CRM tarefas | usuario, agente, checklist | CRM e fonte; dono/fila obrigatorio. |
| Aprovacao | CRM aprovacoes | agente, usuario, sistema | Decisor humano vence. |
| Politica operacional | CRM politicas | configuracao, importacao inicial | Versao ativa por vigencia vence. |
| Template/modelo | CRM templates/canal | Meta/WhatsApp, usuario, Taliya | Template aprovado pelo provedor vence para envio externo. |
| Fluxo de agente | CRM agentes/fluxos | Taliya base, configuracao studio | Studio configura dentro do entitlement. |
| Execucao de agente | Runtime Taliya + CRM | agente, ferramentas, integracoes | Runtime registra; CRM exibe e audita. |
| Cota/uso | Ledger Taliya | IA, WhatsApp, batch, media, historico | Ledger vence; UI nao recalcula como fonte. |
| Integracao | CRM integracoes + provedor | webhook, teste, admin | Provedor informa estado tecnico; CRM decide impacto operacional. |
| Auditoria | Sistema de auditoria | todas as superficies | Nao editavel; correcao cria evento novo. |

## Regras de entrada por origem

| Origem | Pode criar | Pode atualizar | Precisa revisao |
| --- | --- | --- | --- |
| Importacao inicial | contatos, alunos, turmas, planos, pagamentos historicos | dados nao sensiveis em massa | duplicidades, historico sensivel, financeiro divergente |
| WhatsApp | conversa, mensagem, contato desconhecido, pedido operacional | preferencias, pedidos, sinais de intent | identidade, opt-out ambiguo, comprovante, dados sensiveis |
| Agente | caso, tarefa, proposta, resumo, classificacao | status permitido pelo modo | acao sensivel, baixa confianca, dado conflitante |
| Usuario | qualquer objeto permitido | qualquer objeto permitido | alteracao sensivel conforme permissao |
| Provedor financeiro | status de pagamento, falha, disputa | pagamento/cobranca | divergencia com comprovante/manual |
| Suporte Taliya | diagnostico tecnico com grant ativo | somente escopo autorizado | qualquer dado fora do escopo |

## Regras de conflito

1. Dado mais restritivo de privacidade vence.
2. Confirmacao de provedor financeiro vence comprovante nao validado.
3. Correcao humana auditada vence classificacao de agente.
4. Importacao nunca sobrescreve dado sensivel sem revisao.
5. WhatsApp de telefone compartilhado nao atualiza aluno sem validar identidade.
6. Politica ativa na data do evento deve ser preservada como snapshot.
7. Se a confianca for baixa, abrir Problema de dados ou Aprovacao.

## Decisoes abertas

| Tema | Pendente |
| --- | --- |
| Integracao com agenda externa | Google Agenda entra no MVP como importacao assistida por agente; CRM Agenda vence depois da revisao/publicacao. Escrita e sincronizacao viva ficam fora do MVP. |
| Provedor financeiro do studio | Definir quais status de pagamento virao por integracao real no MVP. |
| Retencao de mensagens | Definir prazo de retencao e resumo seguro por plano/politica. |
