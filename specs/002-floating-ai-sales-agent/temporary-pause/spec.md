# Pausa temporária do agente da landing

Data: 2026-10-07. Autoridade: pedido direto do usuário nesta conversa. Este adendo operacional não altera o comportamento comercial histórico nem o programa de integração em andamento.

Ao clicar no agente, abrir o painel existente e mostrar uma mensagem comum da Taliya no balão de resposta: “Estou temporariamente indisponível. Tente novamente mais tarde.” O usuário esclareceu que não deseja banner ou aviso separado. Desabilitar o campo de mensagem e Enviar; bloquear também Enter e sugestões de conversa. Fechar e reabrir continua funcionando, incluindo aberturas acionadas por CTAs existentes.

Controlar a pausa por `floatingAgent.temporaryPause.message`. Manter `enabled: true` para preservar o botão. Enquanto configurada, a pausa deve usar uma apresentação isolada que não monta o atendimento ativo, não consulta a IA, não solicita abertura comercial e não lê nem sobrescreve a conversa salva. Remover `temporaryPause` reativa o fluxo existente. O aviso é uma mensagem operacional local do participante assistant, não uma resposta gerada pelo modelo.

Escopo: somente widget e configuração da landing, incluindo as páginas que reutilizam essa configuração. Preservar componentes, layout, fechamento, histórico salvo, preços, app, APIs, WhatsApp e runtime. Sem publicação. A inspeção visual no navegador segue limitada pelo bloqueio de acesso registrado nesta conversa.
