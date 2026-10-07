# Verificação — 2026-10-07

TypeScript completo e ESLint dos quatro arquivos alterados passaram. `git diff --check` passou. Landing na porta 3001 respondeu HTTP 200.

Verificação isolada em Node, sem navegador/IA: seleção do modo pausado, abertura pelo botão, fechar/reabrir, abertura pelo evento de CTA com mensagem comercial ignorada, uma única mensagem assistant com intent answer_question, callbacks de interação inertes, zero chamadas à API e zero leituras/escritas de histórico. Remover temporaryPause selecionou o componente ativo; enabled false continuou ocultando o widget.

Renderização estática do painel real: mensagem no balão normal floating-message-consultor, textarea e Enviar com disabled, apenas dois botões (fechar e enviar desabilitado), sem balão de erro, sugestões ou indicação de agente ativo. O aviso não é banner.

Inspeção visual e interação real em desktop/mobile não executadas: o navegador local foi bloqueado pela ferramenta nesta conversa. Os checks isolados não substituem essa revisão. Nenhuma publicação, alteração de API, runtime ou canal WhatsApp.

Handlers reais do painel verificados isoladamente: submit e Enter não chamam onSend durante a pausa, mesmo com texto preenchido programaticamente. Sem a pausa, submit mantém o envio existente.
