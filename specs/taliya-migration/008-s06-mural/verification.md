# Verificação — seis exemplos de Produção

Data: 2026-10-07.

- Comparação com snapshot imediatamente anterior: somente os seis registros aprovados foram alterados; os outros 78 registros e os campos externos à lista permaneceram iguais.
- IDs e ordem da seleção inicial preservados: 24 mensagens, três faixas de oito. As seis mensagens usam a categoria AR, cujo handler existente seleciona Produção (`historico-evolucao`).
- O componente mudou apenas o rótulo acessível da categoria AR. Estrutura, duplicação visual, handlers, destinos, controles e CSS permaneceram iguais.
- ESLint de `MessageWallSection.tsx`: passou. `git diff --check`: passou.
- GET da landing local na porta 3001: HTTP 200.
- Inspeção visual desktop/mobile pendente: acesso ao preview pelo navegador bloqueado nesta conversa, sem contorno por outra superfície.
- Revisão do usuário e confirmação das capacidades antes da publicação pendentes. Nenhuma modificação do app ou publicação.

## Quatro linhas e respiro vertical — 2026-10-07

- Texto servido localmente confirma quatro faixas, duas com direção reversa e 48 balões contando a duplicação de loop das 24 mensagens.
- Espaçamento entre título e mural: 40px no mobile, 48px no tablet e 56px no desktop. Entre faixas: 16px no mobile e 20px a partir de 640px. Padding vertical da seção: 56–96px, limitado por clamp e isolado pelo ID do mural.
- ESLint do componente e `git diff --check`: passaram. HTTP local: 200.
- Inspeção visual desktop/mobile e revisão do usuário pendentes pelo bloqueio de acesso do navegador ao preview nesta conversa. Nenhuma publicação deste ajuste.
