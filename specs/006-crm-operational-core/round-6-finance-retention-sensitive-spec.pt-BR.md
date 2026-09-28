# Rodada 6 - Financeiro, contratos, retencao e casos sensiveis - PT-BR

> Status: v0.2. Esta rodada define a base funcional e a primeira especificacao profunda das telas de Financeiro, Movimentacoes, Contratos, Retencao, Cancelamentos, Reclamacoes e Privacidade. Casos financeiros sensiveis nao terao pagina propria no MVP.

## Objetivo operacional

Cobrir dinheiro, contrato, risco, cancelamento, reclamacao e LGPD com clareza de permissao, impacto, auditoria, fallback manual e limites fortes para agentes.

## Limite desta v0.1

Esta versao orienta produto, rotas, objetos, estados e acoes principais. Ainda falta, em passada posterior:

- definir provedor financeiro/assinatura de contratos do MVP;
- fechar status financeiros oficiais;
- definir formula de risco de retencao;
- fechar politicas de desconto, cortesia, bloqueio, pausa e reembolso;
- definir SLA e playbook de reclamacao sensivel;
- fechar prazos e operacao LGPD;
- transformar esta rodada em prompts finais de UI.

## Usuarios envolvidos

| Usuario | Papel na rodada |
| --- | --- |
| Dono/gestor | Decide excecoes, descontos, cancelamentos, reembolsos, reclamacoes e privacidade. |
| Admin | Opera financeiro permitido, contratos, retencao e casos sensiveis. |
| Financeiro | Controla pagamentos, cobrancas, comprovantes, conciliacao, contratos e acordos. |
| Recepcao/operacao | Ve financeiro essencial, cria tarefa/aprovacao quando permitido, registra promessa e acompanha aluno em risco. |
| Professor | Nao ve financeiro; pode gerar sinais de retencao e reclamacao conforme permissao. |
| Agente/runtime | Sugere, resume, cria tarefas/aprovacoes/itens operacionais e envia mensagens permitidas; nunca decide excecao sensivel sozinho. |
| Suporte Taliya | Acessa apenas com grant, escopo, prazo e auditoria. |

## Objetos de negocio

- Plano do studio;
- Plano do aluno;
- Modelo de cobranca;
- Modelo de consumo de aula;
- Direito de aula;
- Evento de consumo de aula;
- Pagamento;
- Cobranca;
- Comprovante;
- Acordo financeiro;
- Excecao financeira;
- Estorno/disputa;
- Contrato;
- Documento financeiro;
- Aluno;
- Ex-aluno;
- Conversa;
- Mensagem;
- Segmento;
- Comunicado;
- Caso operacional;
- Tarefa;
- Aprovacao;
- Solicitacao LGPD;
- Acesso de suporte;
- Evento de auditoria;
- Politica operacional;
- Execucao de fluxo;
- Lancamento de cota.

## Jornadas cobertas

| Jornada | Resultado esperado |
| --- | --- |
| Criar/atualizar plano do aluno | Plano tem vigencia, valor, status, impacto e auditoria. |
| Revisar financeiro geral | Gestor ve previsto, recebido, atrasado, falhas e dinheiro em risco. |
| Enviar lembrete de vencimento | Mensagem respeita consentimento, template, cota, tom e politica. |
| Tratar pagamento atrasado | Atraso vira contato, tarefa, acordo, aprovacao ou bloqueio operacional conforme regra. |
| Enviar Pix/link de pagamento | Link/template mostra valor, vencimento, canal e tentativa. |
| Confirmar pagamento recebido | Confirmacao manual/provedor/comprovante respeita permissao e evidencia. |
| Conciliar pagamento nao identificado | Valor sem dono vira fila, tarefa ou aprovacao ate ser vinculado. |
| Tratar pagamento com falha | Falha mostra motivo, proxima acao e fallback manual. |
| Emitir/guardar recibo e nota | Documento fica vinculado, protegido e auditavel. |
| Gerenciar contrato e termos | Status de contrato fica claro: pendente, enviado, assinado, vencido, cancelado. |
| Tratar excecao financeira | Desconto, cortesia, pausa, bloqueio, acordo e estorno exigem impacto/aprovacao. |
| Pausar/congelar plano | Pausa afeta agenda, cobranca, comunicacao e reativacao. |
| Bloquear/liberar acesso | Acao de alto risco exige motivo, impacto e aprovacao. |
| Registrar credito/cortesia | Beneficio tem motivo, valor, validade, aprovador e auditoria. |
| Alterar/encerrar plano com data correta | Data efetiva e impacto financeiro/agenda ficam visiveis. |
| Fechar financeiro do mes | Fechamento mostra pendencias, divergencias e exportacoes. |
| Revisar retencao | Gestor ve alunos em risco, queda de frequencia, inativos, primeira semana e satisfacao. |
| Tratar cancelamento | Pedido vira fluxo/tarefa com motivo, plano de salvamento, impacto e comunicacao. |
| Reativar ex-aluno | Elegibilidade, consentimento, plano, horario e pendencias sao revisados. |
| Abrir/resolver reclamacao | Caso sensivel pausa automacao, define dono, prazo, resposta e recuperacao. |
| Atender LGPD/privacidade | Solicitacao valida identidade, prazo, aprovacao, execucao e auditoria. |

## Regras de negocio

1. Nenhuma acao financeira, reputacional ou sensivel ocorre sem permissao, impacto e auditoria.
2. Financeiro do aluno e billing Taliya sao dominios separados.
3. Provedor confirmado vence comprovante nao validado; divergencia vira conciliacao/caso.
4. Confirmacao manual de pagamento exige evidencia e permissao financeira.
5. Desconto, cortesia, reembolso, disputa, bloqueio e liberacao nunca sao autonomos por agente.
6. Mensagem de cobranca exige tom, template, consentimento, cota, limite de tentativas e fallback.
7. Contrato assinado e documento financeiro sensivel devem ser protegidos e auditaveis.
8. Pausa/cancelamento afeta agenda, financeiro, contrato, comunicacao e retencao.
9. Retencao precisa explicar o sinal de risco, nao apenas mostrar score.
10. Reclamacao sensivel pausa automacoes relacionadas ate decisao humana.
11. Pedido LGPD exige validacao de identidade, prazo, escopo, execucao controlada e auditoria.
12. Suporte Taliya nunca acessa dados sensiveis sem grant ativo.
13. Plano Base opera financeiro, retencao, contratos e excecoes sensiveis manualmente.
14. Agente pode sugerir, resumir e preparar, mas nao aprovar excecao sensivel.
15. Mensalidade, pacote, aula avulsa, contrato parcelado e creditos seguem o contrato configuravel em `billing-lesson-consumption-models.pt-BR.md`; financeiro nao deve presumir como uma aula e consumida.

## Modos de execucao

| Modo | Como funciona nesta rodada |
| --- | --- |
| Manual | Usuario confirma pagamentos, envia cobrancas, cria tarefas/aprovacoes, aprova excecoes, registra cancelamento e resolve LGPD. |
| Copiloto | Agente resume divida/risco, redige cobranca, sugere acordo, explica impacto e prepara aprovacao. |
| Autonomo | Apenas lembretes simples e tarefas permitidas; acoes financeiras/sensiveis ficam bloqueadas ou exigem aprovacao. |

## Telas web desta rodada

1. Financeiro.
2. Financeiro - kanban.
3. Financeiro - movimentacoes.
4. Contratos e documentos financeiros.
5. Retencao.
6. Cancelamentos e reativacao.
7. Reclamacoes e casos sensiveis.
8. Privacidade e solicitacoes.

## Telas mobile desta rodada

1. Financeiro essencial.
2. Pagamento/cobranca.
3. Contratos/documentos.
4. Retencao.
5. Cancelamentos e reativacao.
6. Reclamacao/caso sensivel.
7. Privacidade/solicitacoes.

## Tela web: Financeiro

| Campo | Definicao |
| --- | --- |
| Tipo | Web visao geral; mobile consulta + acao controlada. |
| Rotas | `/app/financeiro`. |
| Objetivo | Mostrar saude financeira operacional e filas principais para o gestor agir rapido sem entrar na tabela completa. |
| Blocos | KPIs de recebido, previsto, vencido, atraso e conciliacao; filas de vencem hoje, atrasados, comprovantes pendentes, falhas, promessas e excecoes; prioridades financeiras; drawer de item selecionado. |
| Acoes | abrir cobranca, enviar lembrete, abrir conversa, confirmar pagamento com evidencia, criar tarefa, abrir aluno, exportar quando permitido. |
| Estados | normal, atraso alto, conciliacao pendente, falha, excecao aberta, fechamento pendente. |
| Permissoes | financeiro/dono/admin; operacao ve resumo limitado quando necessario. |
| IA/agentes | resumir risco e priorizar filas; nao decide ajuste financeiro. |
| Cotas | analise/resumo com IA consome; indicadores simples nao. |
| Auditoria | exportacao, fechamento, excecao, alteracao de plano e acao financeira sensivel. |
| 0 agentes | visao, filtros, tarefas e registros manuais funcionam. |

## Tela web: Financeiro - kanban

| Campo | Definicao |
| --- | --- |
| Tipo | Web operacao visual por estagio; mobile consulta simples ou herdado de lista. |
| Rotas | `/app/financeiro/kanban`. |
| Objetivo | Operar cobrancas e pendencias financeiras por etapa quando ha volume. |
| Blocos | colunas a vencer, vence hoje, em atraso, promessa de pagamento, comprovante enviado, conciliacao pendente e resolvido; cards com aluno, valor, vencimento, atraso, canal, responsavel, risco e ultima acao; drawer de card. |
| Acoes | mover etapa, enviar lembrete, abrir conversa, registrar promessa, pedir comprovante, confirmar pagamento, criar tarefa e encaminhar excecao para aprovacao/operacao quando sensivel. |
| Estados | aberto, vence hoje, atrasado, falhou, promessa ativa, comprovante pendente, conciliacao pendente, resolvido. |
| Permissoes | operacao financeira exige papel autorizado; acoes sensiveis continuam bloqueadas. |
| IA/agentes | prioriza cards, resume historico e redige mensagens; autonomia apenas para lembretes simples permitidos. |
| Auditoria | mudanca de etapa, confirmacao, conciliacao, promessa e mensagem externa. |

## Tela web: Financeiro - movimentacoes

| Campo | Definicao |
| --- | --- |
| Tipo | Web fila financeira; mobile acao controlada. |
| Rotas | `/app/financeiro/movimentacoes`, `/app/financeiro/movimentacoes/[id]` como drawer ou deep-link futuro. |
| Objetivo | Consultar, filtrar, auditar e operar mensalidades, cobrancas, parcelas, pagamentos recebidos, comprovantes, conciliacao, promessas, falhas, estornos, descontos e ajustes financeiros. |
| Blocos | busca, filtros superiores, filtros rapidos laterais, tipo de movimentacao, tabela/lista, detalhe, aluno, plano, conversa, comprovante, tentativas, conciliacao, acordo/promessa, historico e auditoria. |
| Campos exibidos | aluno, valor, vencimento, status, metodo, comprovante, link, tentativas, responsavel, risco, consentimento. |
| Filtros de tipo | mensalidade, cobranca avulsa, parcela, pagamento recebido, promessa, falha, estorno, desconto, ajuste, conciliacao e comprovante. |
| Filtros rapidos | todas, a vencer, recebidos/pagos hoje, atrasadas, promessas, falhas, conciliacao pendente, comprovantes, estornos, ajustes, descontos, criados por agente e exigem acao humana. |
| Outros filtros | periodo, status, aluno, plano, turma, metodo, origem, responsavel, valor, vencimento, data de pagamento, conciliacao, comprovante e risco/permissao. |
| Acoes | enviar lembrete, enviar link, confirmar comprovante, conciliar, registrar promessa, abrir acordo permitido, criar tarefa, pedir aprovacao e exportar. |
| Estados | previsto, aberto, pago, atrasado, falhou, sem identificacao, comprovante em analise, promessa ativa. |
| Permissoes | confirmacao, conciliacao e acordo exigem financeiro/dono/admin. |
| IA/agentes | redigir lembrete, resumir historico e sugerir prioridade; confirmacao exige evidencia. |
| Cotas | lembrete automatico e mensagem WhatsApp consomem cota. |
| Auditoria | confirmacao, conciliacao, promessa, link enviado, cobranca sensivel e falha relevante. |
| Fallback | sem cota/canal, criar tarefa de contato manual. |

## Excecoes financeiras no MVP

| Campo | Definicao |
| --- | --- |
| Tipo | Conceito operacional sem pagina propria no MVP. |
| Rotas | Sem rota dedicada. Usar `/app/financeiro`, `/app/financeiro/kanban`, `/app/financeiro/movimentacoes`, `/app/aprovacoes`, `/app/tarefas`, `/app/alunos/[id]` e `/app/operacao`. |
| Objetivo | Resolver desconto, cortesia, pausa, bloqueio, acordo, disputa, reembolso e alteracao de plano sem criar uma central separada. |
| Blocos | Drawer do item financeiro, aprovacao quando exigida, tarefa com dono/prazo, historico do aluno, auditoria e origem operacional. |
| Acoes | simular impacto quando necessario, pedir aprovacao, rejeitar, pedir dados, executar alteracao autorizada, registrar motivo, escalar para Operacao. |
| Estados | aguardando aprovacao, risco alto, acordo ativo, disputa, reembolso pendente, executado, rejeitado. |
| Permissoes | dono/admin/financeiro conforme politica; agente nunca aprova sozinho. |
| IA/agentes | preparar resumo e proposta; decisao humana obrigatoria. |
| Cotas | resumo/proposta com IA consome; decisao manual nao. |
| Auditoria | toda decisao e execucao gera antes/depois, motivo e impacto. |

## Tela web: Contratos e documentos financeiros

| Campo | Definicao |
| --- | --- |
| Tipo | Web documentos dentro da familia Financeiro; mobile consulta + acao simples. |
| Rotas | MVP: `/app/financeiro/documentos`. Rotas profundas como `/app/contratos/[id]` ficam como deep-link futuro/contextual se a implementacao exigir. |
| Imagem | Rota herdada; sem imagem nova nesta rodada. Usa componentes aprovados de documentos, tabela, drawer e auditoria. |
| Objetivo | Gerenciar contratos, termos, recibos, notas, comprovantes, status de assinatura/envio e anexos sem misturar documento com cobranca. |
| Blocos | busca, filtros, lista/tabela, detalhe, preview, aluno, status, assinatura/envio, anexos, recibos/notas, permissoes, auditoria. |
| Acoes | ver, enviar, reenviar, anexar, baixar quando permitido, cancelar rascunho, arquivar, abrir aluno, abrir movimentacao relacionada, criar tarefa, auditar. |
| Estados | rascunho, enviado, visualizado, assinado, vencido, cancelado, arquivado, pendente. |
| Permissoes | documento financeiro sensivel exige financeiro/dono/admin; suporte so com grant. |
| IA/agentes | lembrar pendencia e resumir status; nao altera contrato assinado. |
| Auditoria | envio, assinatura, download sensivel, cancelamento, retificacao e anexo. |

## Tela web: Retencao

| Campo | Definicao |
| --- | --- |
| Tipo | Web painel/fila; mobile consulta + acao. |
| Rotas | `/app/retencao`, `/app/retencao/riscos`. |
| Objetivo | Detectar e tratar risco: queda de frequencia, inatividade, retorno, primeira semana, satisfacao e marcos. |
| Blocos | alunos em risco, sinais, tarefas, historico curto, segmentos, primeira semana, retorno, satisfacao, proximas acoes. |
| Acoes | criar tarefa, preparar mensagem, abrir aluno, abrir caso, acompanhar retorno, segmentar risco. |
| Estados | risco baixo, risco medio, risco alto, inativo, retorno pendente, novo aluno, tarefa aberta. |
| Permissoes | operacao/dono/admin; professor apenas sinais permitidos. |
| IA/agentes | explicar risco, sugerir acao e redigir contato; decisao sensivel com humano. |
| Cotas | analise de risco com IA e mensagem consomem cota; regras simples nao. |
| Auditoria | caso sensivel, mensagem externa e mudanca de status relevante. |

## Tela web: Cancelamentos e reativacao

| Campo | Definicao |
| --- | --- |
| Tipo | Web central de relacionamento; mobile acao controlada. |
| Rotas | `/app/cancelamentos`, `/app/retencao/reativacoes`. |
| Objetivo | Tratar pedido de cancelamento, salvamento, pausa, pos-cancelamento, ex-aluno e reativacao. |
| Blocos | fila, aluno, motivo, impacto, plano de salvamento, elegibilidade, comunicacoes, tarefas, historico. |
| Acoes | registrar motivo, abrir plano de salvamento, pausar automacao, converter em pausa, iniciar reativacao aprovada, reservar vaga com validacao, criar tarefa, marcar nao contatar. |
| Estados | risco, pedido aberto, salvamento, cancelado, ex-aluno elegivel, retorno pendente, nao contatar. |
| Permissoes | cancelamento e reativacao com impacto financeiro exigem aprovacao conforme politica. |
| IA/agentes | sugerir resposta, plano de salvamento e oportunidade de retorno; nao promete beneficio/desconto autonomo e nao ignora `nao contatar`. |
| Auditoria | cancelamento, motivo, beneficio, reativacao, opt-out e mensagem sensivel. |

## Tela web: Reclamacoes e casos sensiveis

| Campo | Definicao |
| --- | --- |
| Tipo | Web central sensivel; mobile acompanhamento/aprovacao. |
| Rotas | `/app/reclamacoes`, `/app/reclamacoes/[caseId]`. |
| Objetivo | Resolver reclamacoes, eventos sensiveis e recuperacao de confianca com dono, prazo e automacoes pausadas. |
| Blocos | severidade, resumo, aluno/contato, dono, prazo, plano de resposta, timeline, mensagens, automacoes pausadas, auditoria. |
| Acoes | classificar, pausar automacao, responder, escalar, criar tarefa, resolver, reabrir, acompanhar recuperacao. |
| Estados | novo, severo, aguardando dono, resposta pendente, resolvido, reaberto, confianca pendente. |
| Permissoes | acesso restrito por papel; mensagem sensivel preferencialmente humana/copiloto. |
| IA/agentes | resumir e sugerir resposta; autonomia bloqueada por padrao. |
| Auditoria | classificacao, pausa, resposta, escalonamento, resolucao e reabertura. |

## Tela web: Privacidade e solicitacoes

| Campo | Definicao |
| --- | --- |
| Tipo | Web governanca sensivel; mobile aprovacao. |
| Rotas | `/app/privacidade/solicitacoes`, `/app/privacidade/solicitacoes/[requestId]`, `/app/suporte/acessos`, `/app/suporte/acessos/[grantId]`. |
| Objetivo | Resolver LGPD, opt-out, exportacao, exclusao/anonimizacao e acesso de suporte. |
| Blocos | solicitacoes, identidade, escopo, prazo, dados afetados, aprovacao, execucao, grants de suporte, auditoria. |
| Acoes | validar identidade, aprovar, executar, negar, exportar, anonimizar, expirar acesso, auditar. |
| Estados | pendente, validando, aprovado, executando, executado, negado, acesso ativo, expirado. |
| Permissoes | dono/admin; suporte Taliya apenas com grant escopado. |
| IA/agentes | ajudar a resumir escopo; nunca executa exclusao/anonimizacao sozinho. |
| Auditoria | tudo nesta tela e sensivel e auditavel. |

## Telas mobile

### Financeiro essencial

| Campo | Definicao |
| --- | --- |
| Profundidade | Consulta + acao controlada. |
| Conteudo | atrasos, comprovantes, links, cobrancas, promessas, excecoes pendentes. |
| Acoes | enviar link, confirmar se permitido, registrar promessa, abrir aprovacao. |
| Estados | atrasado, falha, sem comprovante, risco financeiro. |

### Pagamento/cobranca

| Campo | Definicao |
| --- | --- |
| Profundidade | Acao controlada. |
| Conteudo | aluno, valor, vencimento, status, historico curto, conversa, comprovante. |
| Acoes | enviar lembrete, reenviar link, confirmar comprovante, criar tarefa. |
| Estados | pago, aberto, atrasado, falhou, comprovante em analise. |

### Excecoes financeiras no mobile

| Campo | Definicao |
| --- | --- |
| Profundidade | Aprovacao ou tarefa contextual, sem tela propria. |
| Conteudo | excecao, impacto, contrato/pagamento afetado, risco, motivo, origem e historico curto. |
| Acoes | aprovar, rejeitar, pedir mais dados, registrar motivo, abrir aluno ou abrir movimentacao. |
| Estados | aguardando aprovacao, risco alto, disputa, acordo ativo. |

### Contratos/documentos

| Campo | Definicao |
| --- | --- |
| Profundidade | Consulta + acao simples. |
| Conteudo | contrato, recibo, termo, status, assinatura/envio, aluno. |
| Acoes | ver, reenviar, anexar quando permitido, abrir aluno. |
| Estados | pendente, enviado, assinado, vencido. |

### Retencao

| Campo | Definicao |
| --- | --- |
| Profundidade | Consulta + acao. |
| Conteudo | alunos em risco, queda de frequencia, inativos, primeira semana, retorno pendente. |
| Acoes | abrir aluno, criar tarefa, preparar contato, acompanhar retorno. |
| Estados | risco baixo/medio/alto, inativo, retorno pendente. |

### Cancelamentos e reativacao

| Campo | Definicao |
| --- | --- |
| Profundidade | Acao controlada. |
| Conteudo | pedido de cancelamento, motivo, aluno, plano, risco, elegibilidade. |
| Acoes | registrar motivo, abrir plano de salvamento, iniciar reativacao aprovada. |
| Estados | risco, pedido aberto, cancelado, ex-aluno elegivel, nao contatar. |

### Reclamacao/caso sensivel

| Campo | Definicao |
| --- | --- |
| Profundidade | Acao controlada. |
| Conteudo | severidade, dono, prazo, historico curto, resposta, automacao pausada. |
| Acoes | responder, escalar, pausar automacao, acompanhar recuperacao. |
| Estados | severo, aguardando dono, resolvido, confianca pendente. |

### Privacidade/solicitacoes

| Campo | Definicao |
| --- | --- |
| Profundidade | Aprovacao sensivel. |
| Conteudo | solicitacao LGPD, opt-out, acesso de suporte, prazo, identidade. |
| Acoes | aprovar, negar, expirar acesso, abrir detalhe. |
| Estados | pendente, validando, acesso ativo, executado. |

## Cobertura de contratos da Rodada 0

| Contrato | Aplicacao nesta rodada |
| --- | --- |
| Dados | Usa pagamento, cobranca, contrato, acordo, excecao, aluno, caso, solicitacao LGPD e suporte. |
| Ciclo de vida | Pagamento, cobranca, contrato, caso, aluno/ex-aluno, solicitacao e grant. |
| Fonte da verdade | Provedor confirmado vence comprovante; CRM controla casos, contratos, retencao e privacidade. |
| Permissoes | Financeiro e sensiveis exigem papel, contexto e aprovacao. |
| Botoes | Confirmar, conciliar, enviar, aprovar, rejeitar, pausar, bloquear, liberar, cancelar, exportar. |
| Estados | Atrasado, falhou, em analise, aguardando aprovacao, risco alto, cancelado, severo, validando. |
| Cotas | Cobrancas, mensagens e analises de IA mostram custo, bloqueio e fallback manual. |
| Auditoria | Dinheiro, contrato, retencao sensivel, reclamacao, privacidade e suporte. |
| 0 agentes | Financeiro, contratos, retencao e casos sensiveis funcionam manualmente. |

## Decisoes abertas encontradas

| Tema | Encaminhamento |
| --- | --- |
| Provedor financeiro e status | Detalhar quais status virao de integracao no MVP e quais serao manuais. |
| Modelo de cobranca e consumo | Usar `billing-lesson-consumption-models.pt-BR.md` como fonte para mensalidade, pacote, aula avulsa, contrato, consumo de aulas, creditos e impacto em reposicao. |
| Assinatura de contrato | Definir se contrato sera upload/manual, assinatura integrada ou apenas controle de status. |
| Formula de retencao | Definir sinais e pesos de risco sem esconder explicacao do score. |
| Playbook de cancelamento/reclamacao | Definir limites de beneficio, tom, SLA e quando escalar. |
| Operacao LGPD | Definir prazos, exportacao, exclusao/anonimizacao e responsavel legal. |

## Criterio de aceite da rodada

Rodada 6 esta pronta para revisao quando:

- financeiro mostra previsto, recebido, atrasado, falhas, excecoes e fechamento;
- pagamento/cobranca tem comprovante, conciliacao, link, promessa e fallback manual;
- desconto, cortesia, bloqueio, pausa, reembolso e disputa exigem aprovacao/auditoria;
- contrato/documento tem status, envio, anexo, permissao e auditoria;
- retencao mostra risco explicavel e proxima acao;
- cancelamento/reativacao preserva motivo, impacto e comunicacao;
- reclamacao sensivel pausa automacoes e tem dono/prazo/resposta;
- LGPD e acesso de suporte tem identidade, escopo, prazo e auditoria;
- plano Base opera tudo sem agentes ativos.
