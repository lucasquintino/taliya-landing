# Verificação — seis exemplos de Produção

Data: 2026-10-07.

- Comparação com snapshot imediatamente anterior: somente os seis registros aprovados foram alterados; os outros 78 registros e os campos externos à lista permaneceram iguais.
- IDs e ordem da seleção inicial preservados: 24 mensagens, três faixas de oito. As seis mensagens usam a categoria AR, cujo handler existente seleciona Produção (`historico-evolucao`).
- O componente mudou apenas o rótulo acessível da categoria AR. Estrutura, duplicação visual, handlers, destinos, controles e CSS permaneceram iguais.
- ESLint de `MessageWallSection.tsx`: passou. `git diff --check`: passou.
- GET da landing local na porta 3001: HTTP 200.
- Inspeção visual desktop/mobile pendente: acesso ao preview pelo navegador bloqueado nesta conversa, sem contorno por outra superfície.
- Revisão do usuário e confirmação das capacidades antes da publicação pendentes. Nenhuma modificação do app ou publicação.
