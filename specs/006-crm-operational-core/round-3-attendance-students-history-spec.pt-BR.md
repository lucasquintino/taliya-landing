# Rodada 3 - Atendimento, alunos, historico e professor - PT-BR

> Status: v0.2 ajustado. Esta rodada define a base funcional e a primeira especificacao profunda das telas de Inbox, Conversas, Contatos, Alunos, Historico permitido e Professor. Responsaveis/familia e consentimentos como modulos proprios ficaram fora do MVP.

## Objetivo operacional

Fazer o Taliya sustentar o relacionamento diario do studio com alunos, contatos e interessados sem depender dos agentes, mas permitindo que agentes ajudem no WhatsApp, dentro do CRM web e no app quando houver permissao, cota, contexto e modo configurado.

## Limite desta v0.1

Esta versao orienta produto, rotas, objetos, estados e acoes principais. Ainda falta, em passada posterior:

- amarrar cada bloco aos IDs finais da matriz de casos;
- fechar campos obrigatorios finais por objeto;
- definir microcopy de consentimento, opt-out, historico sensivel e identidade;
- fechar a granularidade exata do que professor pode ver;
- definir retencao de mensagens e resumo seguro;
- desenhar responsividade final das telas;
- transformar esta rodada em prompts finais de UI.

## Usuarios envolvidos

| Usuario | Papel na rodada |
| --- | --- |
| Dono/gestor | Supervisiona atendimento, decide privacidade, define visibilidade de historico e resolve casos sensiveis. |
| Admin | Opera inbox, contatos, alunos, permissoes e ajustes de dados. |
| Recepcao/operacao | Atende conversas, organiza contatos, vincula aluno/interessado, cria tarefas e abre casos. |
| Professor | Ve aulas/alunos permitidos, registra notas e consulta contexto autorizado. |
| Financeiro | Entra em conversas e perfis quando o assunto e pagamento, comprovante, cobranca ou contrato. |
| Agente/runtime | Sugere resposta, classifica intent, resume conversa, cria tarefas/casos e executa conforme modo. |
| Suporte Taliya | Diagnostica problemas apenas com grant, escopo, prazo e auditoria. |

## Objetos de negocio

- Conversa;
- Mensagem;
- Tentativa de envio;
- Contato;
- Telefone compartilhado;
- Preferencia de contato;
- Aluno;
- Interessado;
- Ex-aluno;
- Evento de historico;
- Nota de professor;
- Restricao/cuidado;
- Documento do aluno;
- Gate de anamnese;
- Tarefa;
- Caso operacional;
- Aprovacao;
- Problema de dados;
- Solicitacao LGPD;
- Evento de auditoria;
- Execucao de fluxo;
- Lancamento de cota.

## Jornadas cobertas

| Jornada | Resultado esperado |
| --- | --- |
| Atender nova conversa | Conversa entra na fila certa, e vinculada ou marcada para triagem, e recebe resposta manual/copiloto/autonoma conforme modo. |
| Responder aluno atual | Usuario ve contexto do aluno, evita resposta indevida e registra continuidade. |
| Resolver pergunta sem resposta pronta | Sistema prepara sugestao, tarefa ou caso sem fingir certeza. |
| Assumir conversa do agente | Humano pausa ou assume o atendimento com historico e motivo auditavel. |
| Registrar preferencia/opt-out | Preferencia mais restritiva vence e bloqueia envios quando necessario. |
| Resolver telefone compartilhado | Contatos e alunos vinculados ficam claros antes de acao sensivel. |
| Atualizar contato com seguranca | Alteracao tem origem, permissao e resolucao de conflito. |
| Confirmar identidade do contato | A identidade fica validada antes de expor dado ou tomar decisao sensivel. |
| Classificar midia/documento/audio | Midia vira comprovante, documento, nota, tarefa, caso ou descarte seguro. |
| Resolver duplicidade | Contato/aluno duplicado vira problema de dados com mescla segura ou separacao. |
| Atender pedido de privacidade | Pedido vira solicitacao/caso com identidade validada e prazo. |
| Reabrir conversa parada | Conversa atrasada volta para fila, dono ou agente conforme regra. |
| Abrir perfil do aluno | Equipe entende plano, agenda, riscos, tarefas e historico permitido. |
| Professor abre contexto | Professor ve apenas o que precisa para a aula e para o aluno permitido. |
| Registrar nota pos-aula | Nota entra no historico com autor, aula, visibilidade e auditoria quando sensivel. |
| Registrar restricao/cuidado | Dado sensivel exige permissao, motivo, origem e visibilidade controlada. |
| Revisar objetivo/evolucao | Gestor/professor autorizado acompanha progresso sem transformar o CRM em prontuario clinico. |
| Guardar documento/anamnese | Documento entra com tipo, origem, visibilidade, consentimento e revisao quando sensivel. |
| Corrigir historico | Correcao cria novo evento; nao apaga rastro sem politica. |
| Compartilhar contexto seguro | Aluno/responsavel recebe apenas resumo permitido, aprovado e auditado. |
| Ver linha do tempo unificada | Usuario autorizado entende a sequencia de aulas, notas, documentos, conversas e casos sem acessar o que nao pode ver. |

## Regras de negocio

1. WhatsApp e canal; o CRM e a fonte operacional de atendimento.
2. Toda conversa deve ter estado, responsavel/fila, origem, objeto vinculado ou motivo de nao vinculo.
3. Conversa pode existir sem aluno vinculado; acao sensivel nao pode depender de identidade incerta.
4. Handoff humano pausa ou limita o agente na conversa ate regra de retomada.
5. Opt-out e preferencia mais restritiva vencem qualquer template, campanha ou automacao.
6. Telefone compartilhado exige confirmar quem esta falando antes de atualizar dado sensivel.
7. Telefone compartilhado ou identidade ambigua nao cria modulo de familia/responsavel no MVP; vira verificacao de contato, problema de dados ou tarefa antes de acao sensivel.
8. Professor so ve alunos, aulas e historico permitido das turmas/aulas autorizadas.
9. Dado sensivel nao aparece completo no painel de conversa, no app ou para agente por padrao.
10. Historico auditado nao e sobrescrito; correcao cria novo evento com antes/depois seguro.
11. Classificacao de midia por IA e sugestao; comprovante, documento sensivel e restricao exigem revisao quando houver risco.
12. Falha de envio deve explicar motivo, origem, tentativa e proxima acao manual segura.
13. Plano Base mantem inbox, contatos, alunos, historico permitido e notas sem automacao ativa.
14. Agente pode sugerir, resumir e classificar conforme cota; envio externo autonomo exige modo, politica e consentimento.
15. Pedido LGPD pode nascer no atendimento, mas sua execucao pertence a governanca de privacidade.

## Modos de execucao

| Modo | Como funciona nesta rodada |
| --- | --- |
| Manual | Usuario responde, vincula, registra nota, cria tarefa/caso, corrige dados e resolve falhas sem agente ativo. |
| Copiloto | Agente sugere resposta, resumo, classificacao, vinculo provavel, proxima acao ou rascunho de nota. Humano decide. |
| Autonomo | Agente pode responder ou criar atualizacoes permitidas quando identidade, consentimento, cota, politica e risco estiverem OK. |

## Entradas e saidas

| Tipo | Exemplos |
| --- | --- |
| Entradas | mensagem WhatsApp, anexo, audio, contato importado, cadastro manual, aula do dia, nota do professor, opt-out, pedido LGPD, falha de provedor. |
| Saidas | resposta enviada, tarefa, caso operacional, aprovacao, problema de dados, nota, documento classificado, preferencia atualizada, evento de auditoria. |

## Fonte da verdade

| Dado | Fonte da verdade |
| --- | --- |
| Conversa | CRM Inbox + provedor de canal para entrega. |
| Mensagem enviada | CRM Tentativa de envio + providerMessageId/idempotencia. |
| Contato | CRM Contatos. |
| Opt-out/consentimento | CRM Privacidade; regra mais restritiva vence. |
| Aluno/interessado | CRM Alunos/Vendas. |
| Historico do aluno | CRM Historico; correcao cria evento novo. |
| Nota de professor | CRM Historico com aula/professor como origem. |
| Restricao/cuidado | CRM Historico sensivel com permissao forte. |

## Eventos e gatilhos

| Gatilho | Comportamento esperado |
| --- | --- |
| Nova mensagem | Criar/atualizar conversa, tentar identificar contato e rotear fila. |
| Mensagem sem resposta em SLA | Criar tarefa/caso ou priorizar no Hoje. |
| Agente com baixa confianca | Solicitar revisao humana ou criar tarefa. |
| Usuario assume conversa | Pausar agente, registrar handoff e mostrar motivo. |
| Opt-out recebido | Atualizar preferencia, bloquear envios e auditar. |
| Anexo recebido | Classificar com regra/IA permitida e pedir revisao se sensivel. |
| Telefone compartilhado detectado | Abrir problema de dados ou pedir confirmacao de identidade. |
| Nota pendente apos aula | Criar lembrete/tarefa para professor. |
| Historico sensivel alterado | Auditar e atualizar visibilidade. |
| Falha de envio | Registrar tentativa, mostrar acao segura e criar tarefa se necessario. |

## Telas web desta rodada

1. Inbox e conversas.
2. Contatos.
3. Alunos e perfil do aluno.
4. Historico do aluno.
5. Professor e notas.
6. Falhas de envio como subarea de Inbox/envios.

## Telas mobile desta rodada

1. Inbox.
2. Conversa.
3. Contato rapido.
4. Falhas de envio.
5. Alunos.
6. Perfil do aluno.
7. Historico permitido.
8. Professor.

## Tela web: Inbox e conversas

| Campo | Definicao |
| --- | --- |
| Tipo | Web workspace profundo; mobile acao completa. |
| Rotas | `/app/inbox`, `/app/conversas/[id]`, `/app/envios`, `/app/envios/[sendId]`. |
| Objetivo | Atender conversas com contexto, controle de agente, identidade, consentimento e proxima acao. |
| Usuario principal | Recepcao/operacao. |
| Usuarios secundarios | Dono, admin, financeiro em conversas financeiras. |
| Blocos | lista/fila, conversa, painel do contato/aluno, sugestao do agente, anexos, tarefas/casos, tentativas de envio, auditoria resumida. |
| Campos exibidos | canal, contato, aluno/interessado vinculado, status, dono/fila, ultima mensagem, SLA, agente, consentimento, risco, anexos, origem. |
| Campos editaveis | dono/fila, vinculo, status, tags operacionais, observacao interna, preferencia permitida, classificacao de anexo. |
| Acoes | responder, enviar, salvar rascunho, assumir do agente, pausar agente, pedir sugestao, editar sugestao, criar tarefa, abrir caso, vincular aluno/interessado, registrar opt-out, abrir perfil, classificar anexo. |
| Posicao dos botoes | resposta no rodape da conversa; acoes de agente no topo da conversa; contexto e vinculo no painel direito. |
| Estados | novo, aguardando humano, agente respondendo, agente pausado, sem consentimento, identidade incerta, telefone compartilhado, mensagem falhou, encerrado, reaberto. |
| Permissoes | inbox geral para operacao; financeiro ve apenas conversas financeiras; professor nao ve por padrao. |
| IA/agentes | sugerir resposta, resumo, intent, prioridade, classificacao e proxima acao. Envio autonomo somente com politica/cota/consentimento. |
| Cotas | sugestao, resumo, classificacao de midia e resposta de agente podem consumir cota; em 90% vira aprovacao/tarefa; em 100% vira manual. |
| Auditoria | handoff, pausa de agente, envio externo, opt-out, vinculo sensivel, falha relevante. |
| Fallback | sem cota, sem canal ou sem consentimento: resposta manual/tarefa/caso. |
| Operacao sem agentes | usuario responde manualmente, usa templates permitidos, cria tarefas/casos e registra preferencia. |
| Fora de escopo | campanhas e comunicados em massa; ficam na Rodada 5/7. |

## Tela web: Contatos

| Campo | Definicao |
| --- | --- |
| Tipo | Web lista + detalhe; mobile acao rapida. |
| Rotas | `/app/contatos`, `/app/contatos/[id]`. |
| Objetivo | Organizar identidade, telefones, preferencias de contato e problemas de telefone compartilhado sem criar modulo proprio de responsaveis/familia no MVP. |
| Usuario principal | Recepcao/operacao. |
| Blocos | lista, filtros, detalhe, alunos vinculados, telefones, preferencias, duplicidades, timeline curta. |
| Campos exibidos | nome, telefone, canal, alunos vinculados, preferencia, opt-out, risco de duplicidade, ultima conversa, origem. |
| Campos editaveis | nome, telefone, email, aluno vinculado, preferencia, observacao, status de validacao. |
| Acoes | editar contato, validar identidade, vincular aluno, separar/mesclar duplicado, resolver telefone compartilhado, registrar opt-out, abrir conversa, criar tarefa. |
| Estados | valido, pendente validacao, duplicado, telefone compartilhado, opt-out, dados incompletos, sem permissao. |
| Permissoes | operacao edita dados basicos; dados sensiveis podem exigir admin/dono. |
| IA/agentes | sugerir duplicidade, vinculo provavel e dados ausentes. |
| Cotas | sugestoes com IA consomem cota; revisao manual sempre disponivel. |
| Auditoria | mescla, separacao, opt-out, validacao de identidade e alteracao sensivel. |
| Fallback | baixa confianca vira Problema de dados. |
| Operacao sem agentes | busca, edicao, mescla revisada e vinculos manuais continuam completos. |

## Tela web: Alunos e perfil do aluno

| Campo | Definicao |
| --- | --- |
| Tipo | Web workspace profundo; mobile consulta + acao. |
| Rotas | `/app/alunos`, `/app/alunos/[id]`. |
| Objetivo | Dar visao operacional do aluno para atendimento, agenda, financeiro, historico permitido e tarefas. |
| Usuario principal | Dono/admin/operacao. |
| Usuarios secundarios | Financeiro parcial; professor apenas alunos permitidos. |
| Blocos | lista, filtros, perfil, plano, agenda, proxima aula, presencas, reposicoes, pagamentos resumidos, contatos, riscos, tarefas, timeline resumida, notas permitidas. |
| Campos exibidos | status, turma, professor, plano, proxima aula, frequencia, inadimplencia resumida quando permitido, reposicoes, contatos, preferencias, riscos, tarefas abertas. |
| Campos editaveis | dados cadastrais, status permitido, vinculos, plano/agenda conforme permissao, observacao, tarefa, preferencia. |
| Acoes | abrir conversa, criar tarefa, agendar, alterar plano permitido, abrir pagamento, abrir historico permitido, registrar observacao, abrir caso, pedir revisao de dado. |
| Estados | ativo, pausado, inadimplente, risco, sem turma, dados incompletos, permissao restrita, historico sensivel oculto. |
| Permissoes | cada bloco respeita papel; professor nao ve financeiro completo nem dados sensiveis fora do permitido. |
| IA/agentes | resumo operacional, riscos, proxima melhor acao, sugestao de tarefa e explicacao de bloqueio. |
| Cotas | resumos longos e analises de risco com IA consomem cota; dados/regras simples nao. |
| Auditoria | mudancas de status/plano/responsavel/historico sensivel e acoes financeiras. |
| Fallback | perfil incompleto mostra checklist/problema de dados. |
| Operacao sem agentes | perfil, tarefas, agenda, registros e filtros continuam completos. |

## Tela web: Historico do aluno

| Campo | Definicao |
| --- | --- |
| Tipo | Web subarea sensivel; mobile consulta restrita + nota. |
| Rotas | `/app/alunos/[id]/linha-do-tempo`, `/app/historico`, `/app/historico/documentos`, `/app/historico/permissoes`. |
| Objetivo | Registrar e consultar linha do tempo do aluno sem expor dado sensivel indevido. |
| Usuario principal | Dono/admin; professor apenas no recorte permitido. |
| Blocos | linha do tempo unificada, documentos, anamnese, consentimentos, restricoes/cuidados, objetivos, evolucao, permissoes, correcoes, compartilhamentos. |
| Campos exibidos | tipo de evento, data, autor, origem, aula, visibilidade, sensibilidade, resumo permitido, documento/anexo, status de revisao. |
| Campos editaveis | nova nota, visibilidade, correcao, anexo, objetivo, revisao de permissao, compartilhamento seguro. |
| Acoes | adicionar nota, anexar documento, registrar restricao, revisar objetivo/evolucao, corrigir historico, revisar permissao, compartilhar contexto seguro, abrir caso, pedir aprovacao. |
| Estados | sem permissao, dado sensivel, aguardando consentimento, revisao necessaria, documento pendente, historico corrigido, compartilhado. |
| Permissoes | historico sensivel exige permissao contextual; suporte so com grant; agente so acessa resumo permitido. |
| IA/agentes | resumir historico permitido, sugerir classificacao e lembrar pendencia; nao cria decisao clinica sozinho. |
| Cotas | resumo longo, OCR/transcricao e classificacao de midia consomem cota. |
| Auditoria | nota sensivel, restricao, documento, correcao, visibilidade e compartilhamento. |
| Fallback | se houver duvida de sensibilidade, ocultar detalhe e criar revisao. |
| Operacao sem agentes | linha do tempo, upload, notas e permissoes funcionam manualmente. |
| Fora de escopo | prontuario clinico completo; Taliya trata historico operacional seguro. |

## Tela web: Professor e notas

| Campo | Definicao |
| --- | --- |
| Tipo | Web e mobile operacional; mobile e essencial para dia a dia. |
| Rotas | `/app/professores`, `/app/professores/[teacherId]`. |
| Objetivo | Dar ao professor contexto permitido para aula e capturar notas/handoff sem expor dados indevidos. |
| Usuario principal | Professor. |
| Usuarios secundarios | Gestor/admin para supervisao. |
| Blocos | aulas do dia, alunos da aula, contexto permitido, notas pendentes, lembretes, handoff, restricoes permitidas, historico resumido. |
| Campos exibidos | aula, horario, turma, aluno, status de chamada, nota pendente, cuidado permitido, objetivo, ultimo handoff, tarefa ligada. |
| Campos editaveis | nota pos-aula, lembrete, handoff, observacao permitida, status de nota. |
| Acoes | registrar nota, abrir contexto, criar handoff, marcar lembrete, abrir aluno permitido, pedir revisao, sinalizar cuidado. |
| Estados | nota pendente, contexto restrito, aula sem chamada, aluno sem consentimento, sem permissao, lembrete vencido. |
| Permissoes | professor so ve contexto dos alunos/aulas permitidos; gestor decide visibilidade padrao. |
| IA/agentes | lembrar nota pendente, sugerir resumo permitido e detectar lacuna; nao inventa evolucao. |
| Cotas | lembrete por regra nao consome IA; sugestao/resumo com IA consome. |
| Auditoria | nota, restricao, correcao, handoff sensivel e mudanca de visibilidade. |
| Operacao sem agentes | professor registra notas, consulta contexto permitido e faz handoff manualmente. |

## Tela web/mobile: Falhas de envio

| Campo | Definicao |
| --- | --- |
| Tipo | Subarea de Inbox/envios; mobile acao parcial. |
| Rotas | `/app/envios`, `/app/envios/[sendId]`. |
| Objetivo | Explicar mensagens nao entregues e oferecer acao segura. |
| Blocos | fila de falhas, detalhe, conversa origem, motivo tecnico/operacional, proxima tentativa, politica, opt-out, janela de envio. |
| Campos exibidos | contato, canal, mensagem, origem, tentativa, erro, status do provedor, idempotencia, cota, consentimento. |
| Acoes | tentar de novo quando seguro, enviar manual, cancelar, criar tarefa, abrir conversa, abrir canal, abrir caso. |
| Estados | falhou, aguardando provedor, janela fechada, opt-out, cota esgotada, canal desconectado, duplicidade evitada. |
| Auditoria | falha relevante, reenvio, cancelamento, envio externo e reprocessamento. |
| Fallback | quando reenvio nao for seguro, criar tarefa com contexto. |

## Telas mobile

### Inbox

| Campo | Definicao |
| --- | --- |
| Profundidade | Acao completa. |
| Conteudo | conversas por prioridade, status, dono/fila, contato, aluno/interessado, consentimento, ultima mensagem, risco. |
| Acoes | abrir conversa, assumir, filtrar, criar tarefa, abrir caso, priorizar. |
| Estados | novo, aguardando humano, agente pausado, sem consentimento, identidade incerta. |

### Conversa

| Campo | Definicao |
| --- | --- |
| Profundidade | Acao completa. |
| Conteudo | mensagens, resposta, sugestao, contato, aluno vinculado, anexos essenciais, historico permitido resumido, falha de envio. |
| Acoes | responder, editar sugestao, enviar, assumir, pausar agente, registrar opt-out, abrir perfil/caso. |
| Estados | falha de envio, opt-out, sem permissao, agente respondendo, cota bloqueada. |

### Contato rapido

| Campo | Definicao |
| --- | --- |
| Profundidade | Consulta + acao. |
| Conteudo | telefones, alunos vinculados, preferencia de contato, bloqueios e duplicidade. |
| Acoes | ligar/abrir WhatsApp, editar essencial, vincular, validar responsavel, criar tarefa. |
| Estados | duplicado, telefone compartilhado, pendente validacao, sem permissao. |

### Falhas de envio

| Campo | Definicao |
| --- | --- |
| Profundidade | Acao parcial. |
| Conteudo | mensagem, contato, canal, motivo, tentativa, origem, consentimento, cota. |
| Acoes | tentar de novo quando seguro, enviar manual, criar tarefa, abrir conversa. |
| Estados | falhou, aguardando provedor, opt-out, janela fechada, cota esgotada. |

### Alunos

| Campo | Definicao |
| --- | --- |
| Profundidade | Consulta + acao rapida. |
| Conteudo | busca, filtros, status, risco, plano resumido, turma, proxima aula, tarefa aberta. |
| Acoes | abrir perfil, iniciar conversa, criar tarefa, filtrar por risco/turma/status. |
| Estados | inadimplente, risco, pausado, sem permissao, dados incompletos. |

### Perfil do aluno

| Campo | Definicao |
| --- | --- |
| Profundidade | Acao parcial/completa conforme permissao. |
| Conteudo | dados essenciais, contatos, agenda, turma, plano resumido, reposicoes, riscos, tarefas, historico permitido. |
| Acoes | abrir conversa, criar tarefa, registrar observacao, abrir agenda, abrir historico permitido, pedir revisao. |
| Estados | ativo, pausado, inadimplente, historico restrito, sem turma, dados incompletos. |

### Historico permitido

| Campo | Definicao |
| --- | --- |
| Profundidade | Consulta restrita + nota. |
| Conteudo | notas recentes, restricoes permitidas, objetivos, documentos essenciais, consentimentos, linha do tempo filtrada. |
| Acoes | adicionar nota, anexar quando permitido, pedir revisao, compartilhar contexto seguro se permitido. |
| Estados | sem permissao, dado sensivel, aguardando consentimento, revisao necessaria. |

### Professor

| Campo | Definicao |
| --- | --- |
| Profundidade | Acao completa. |
| Conteudo | aulas do dia, alunos, chamada relacionada, notas pendentes, contexto permitido, handoff, lembretes. |
| Acoes | registrar nota, abrir contexto, criar handoff, marcar lembrete, pedir revisao. |
| Estados | nota pendente, contexto restrito, aula sem chamada, lembrete vencido. |

## Cobertura de contratos da Rodada 0

| Contrato | Aplicacao nesta rodada |
| --- | --- |
| Dados | Usa conversa, mensagem, tentativa, contato, responsavel, aluno, historico, nota, documento, tarefa e caso. |
| Ciclo de vida | Conversa, contato, aluno, nota, documento, falha de envio, tarefa/caso e pedido de privacidade. |
| Fonte da verdade | CRM vence para operacao; provedor confirma entrega; opt-out restritivo vence. |
| Permissoes | Historico, professor, responsavel e conversa sensivel usam permissao contextual. |
| Botoes | Responder, assumir, pausar, vincular, validar, registrar nota, corrigir, compartilhar e tentar de novo. |
| Estados | Aguardando humano, agente pausado, sem consentimento, identidade incerta, dado sensivel, falha de envio. |
| Cotas | Sugestao, resumo, classificacao de midia e resposta de agente devem mostrar bloqueio/downgrade. |
| Auditoria | Handoff, opt-out, mescla, historico sensivel, visibilidade, envio externo e reprocessamento. |
| 0 agentes | Inbox, perfis, contatos, notas, historico permitido e falhas continuam manuais. |

## Decisoes abertas encontradas

| Tema | Encaminhamento |
| --- | --- |
| Identidade em telefone compartilhado | Definir quao forte deve ser a validacao antes de expor historico, alterar cadastro ou responder assunto sensivel. |
| Visibilidade de historico para professor | Definir campos exatos por padrao: objetivo, cuidado, observacao, documento, anamnese e financeiro. |
| Classificacao de audio/imagem/documento | Definir escopo do MVP: apenas classificar manualmente, usar OCR/transcricao, ou permitir IA com revisao. |
| Compartilhamento seguro com aluno/responsavel | Definir quais resumos podem sair do CRM e quais exigem aprovacao. |

## Criterio de aceite da rodada

Rodada 3 esta pronta para revisao quando:

- atendimento tem caminho manual, copiloto e autonomo com limites claros;
- conversa tem identidade, consentimento, dono/fila, estado e proxima acao;
- contato, responsavel e telefone compartilhado nao atualizam dado sensivel sem validacao;
- aluno tem perfil operacional suficiente para recepcao, gestor e professor;
- historico sensivel tem visibilidade, permissao, correcao e auditoria;
- professor consegue operar o dia pelo app sem ver dado indevido;
- falha de envio tem explicacao e acao segura;
- plano Base continua completo sem agentes ativos.
