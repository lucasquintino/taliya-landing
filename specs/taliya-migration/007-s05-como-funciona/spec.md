# S05 — Como funciona: remoção mobile e revisão de duas abas

Data: 2026-10-07.

## Escopo aprovado — remoção mobile anterior

Remover a orientação mobile “Escolha um tópico e navegue pelas etapas para ver como a Taliya organiza cada parte da rotina.” em `components/landing/sections/HowItWorksSection.tsx`.

Preservar títulos, abas, exemplos, seletores, carrossel, callbacks, estilos e preços. A remoção do parágrafo foi autorizada no recorte anterior.

## Escopo aprovado — conteúdo de duas abas

Alterar somente “O que você pode fazer” e “Feita para o seu negócio”. Preservar a composição, seletores, navegação, demais cartões, preços e funcionalidades existentes.

### O que você pode fazer

- Manter o título e os quatro pontos principais da aba.
- Descrição: “Por voz ou texto, pelo app ou WhatsApp, organize sua rotina, prepare materiais de trabalho e tire dúvidas sobre os arquivos que você enviar.”
- Renomear o cartão “Documentos” para “Produção”. Ele terá exatamente quatro pontos:
  1. Transforme suas anotações em documentos e materiais de trabalho.
  2. Resuma arquivos e tire dúvidas sobre o conteúdo.
  3. Prepare respostas com as informações do cliente e do serviço.
  4. Guarde e encontre arquivos; consulte versões e aprovações.
- Preservar os outros sete cartões e suas capacidades.

### Feita para o seu negócio

- Preservar o título, a ilustração e o loop.
- Descrição: “Pelo WhatsApp ou no app, a Taliya usa suas anotações, arquivos e informações do cliente e do serviço para ajudar a organizar sua rotina e preparar seu trabalho.”
- Os pontos mantêm a conexão entre serviços, horários e clientes; ampliam o histórico para retomar conversas e preparar respostas; mantêm documentos e arquivos organizados; e dizem que a pessoa confere materiais e respostas antes de usar.
- Frase abaixo da ilustração: “A Taliya ajuda a organizar sua rotina e a preparar seu trabalho.”

## Aceitação e limites

- O cartão Produção contém exatamente quatro pontos e mantém a referência a armazenamento, busca, versões e aprovações.
- Não alterar outras abas, cartões, componentes, layout, responsividade, navegação, preços ou telas do app.
- A disponibilidade real das capacidades de leitura e preparação de materiais deve ser confirmada antes da publicação.
- Conferir diff e resposta local. Fazer inspeção visual desktop/mobile quando o preview estiver acessível.
