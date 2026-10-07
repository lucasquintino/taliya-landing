# S07 — Frentes do negócio: Produção

Data: 2026-10-07. Autoridade: pedido direto do usuário nesta conversa.

## Escopo aprovado

Remover o subtítulo “Veja como a Taliya organiza clientes, agenda, serviços, recebimentos, lembretes, listas, resumos e documentos.” de `agentsIntro` em `data/landing/niches/pilates.ts`. O componente compartilhado já omite o parágrafo quando o subtítulo está vazio.

Preservar título, frentes, seis abas de Produção, demais fluxos, seletores, carrossel, callbacks, estilos e preços. A remoção do subtítulo continua vigente.

## Ajuste de nomenclatura aprovado em 2026-10-07

O usuário aprovou renomear a frente de “Documentos” para “Produção”, com descrição curta “Documentos e materiais de trabalho”. A aba “Versões do orçamento” passa a “Versões do documento”; ajustar também a referência ao documento no resumo, no contexto e no caminho de documento não identificado do fluxo G4. Preservar IDs, versões salvas, identificação da versão atual, demais abas e comportamento. A aprovação deste recorte não confirma disponibilidade das outras capacidades propostas de criação e leitura de arquivos.

## Ampliação autorizada em 2026-10-07

O usuário autorizou implementar o restante da proposta desta seção e revisar o resultado ao final. Este pedido substitui a pendência de aprovação da implementação local, sem confirmar a disponibilidade real de capacidades do produto.

- G1 — Preparar documento: transformar informações e anotações em fichas, relatórios, roteiros e orçamentos para revisão. Exemplos de fotógrafo, profissional de estética e técnico de manutenção. Preservar orçamento com itens/total e perguntas sobre dados ausentes.
- G2 — Guardar arquivo: preservar arquivo anexado, vínculo ao cliente/serviço e confirmação quando o vínculo for ambíguo.
- G3 — Encontrar e entender: preservar busca e escolha entre arquivos; incluir resumo do pedido do cliente para um designer e perguntas baseadas no material fornecido. Avisar quando não houver informação ou o conteúdo não puder ser lido.
- G4 — Versões do documento: consultar versões e aprovações registradas, distinguindo atual de aprovada sem inferir aprovação.
- G5 — Documentos do cliente: preservar listagem por tipo/data; incluir rascunho de resposta de consultora usando proposta e observações do serviço, com revisão e envio pelo profissional.
- G12 — Histórico do serviço: preservar registros por data/tipo e lacunas explícitas.

Alterar apenas o conteúdo ativo de Produção em `data/landing/agentFlowCatalog.ts` e dois rótulos de abas em `components/landing/sections/AgentsDemoSection.tsx`. Preservar IDs e seleção dos seis fluxos, canais, estilos, componentes e interações. Não alterar a demonstração de Quero que a Taliya cuide de, Como funciona, app, preços ou outras frentes. Não restaurar o subtítulo removido.

## Revisão de linguagem solicitada em 2026-10-07

Usar frases comuns no dia a dia dos prestadores de serviço. Nos textos alterados de Produção, substituir expressões como “conteúdo fornecido”, “completar lacunas por suposição”, “materiais vinculados” e “aprovação registrada” por explicações diretas: “suas anotações”, “o arquivo que você enviar”, “os documentos do cliente” e “qual foi aprovada, quando essa informação estiver salva”. Manter exemplos concretos, informações ausentes explícitas e conferência/envio pelo profissional.

## Disponibilidade e limites do produto

Criação de fichas/relatórios/roteiros, leitura/perguntas sobre arquivos, respostas com contexto e versões/aprovações de documentos além de orçamentos não foram verificadas no produto. A implementação é um preview editorial local para revisão do usuário; não é prova de capacidades disponíveis e não autoriza publicação. Esses itens devem ser confirmados ou retirados antes de publicação. Não prometer decisões profissionais autônomas, envio automático, prontuário ou prescrição completos.

## Aceitação

- O subtítulo removido não é renderizado.
- Os seis fluxos aprovados apresentam os exemplos e limites acima, com orçamento, armazenamento, busca, versões, aprovações e histórico preservados.
- Nenhum conteúdo de outra frente ou controle da seção é alterado.
- Verificação de resposta local e diff; inspeção visual desktop/mobile pendente, pois o navegador integrado bloqueou o acesso ao preview nesta conversa.

## Ajuste de vocabulário — 2026-10-07

O usuário apontou que “briefing” não é um termo do dia a dia. Retirar o termo da copy ativa de Produção: usar “roteiro do ensaio” no exemplo do fotógrafo e “pedido do cliente” no exemplo do designer. Preservar fluxos, controles e capacidades.
