# S03 — Quero que a Taliya cuide de: Produção

Data: 2026-10-07. Autoridade: aprovação direta do usuário nesta conversa.

## Escopo

Renomear o rótulo e o título da opção Documentos para Produção em `data/landing/niches/pilates.ts`. Preservar o ID `documentos`, vínculos, controles e layout. A aprovação inicial de nomenclatura foi ampliada pelo pedido descrito abaixo; não comprova novas capacidades do produto.

## Demonstração aprovada em 2026-10-07

O usuário aprovou a proposta da demonstração e pediu orçamento no começo e arquivos dentro dos balões, como no WhatsApp, tanto nas respostas da Taliya quanto nos anexos do usuário.

Conversa de manutenção para Marina: orçamento com preço/retorno definidos pelo profissional; aprovação informada pelo profissional; relatório a partir das notas; nova versão com horário; proposta anexada pelo usuário; resumo do arquivo e pergunta sobre retorno; resposta para o profissional conferir/enviar. Em seguida, exemplos de ficha de atendimento da Júlia e registro do atendimento do Roberto para uso no prontuário, usando arquivos anexados pelo profissional. Valores são exemplos do serviço, não preços da assinatura.

O arquivo aparece como cartão dentro do balão existente, com ícone de documento, nome, formato PDF, páginas e tamanho ilustrativos. Usar cor clara na resposta da Taliya e verde no balão do usuário. A mensagem acompanha o anexo no mesmo balão. A representação é ilustrativa: não faz upload, geração real ou download e não cria botões que prometem essas ações.

Adicionar `attachment` opcional somente ao tipo message em `AutonomousFlowStep` e renderização condicional em `AutonomousWhatsAppFlowMockup.tsx`. Sem anexo, a árvore da mensagem permanece igual. Usar dimensões relativas à fonte do balão para acompanhar os estilos responsivos existentes. Preservar seletores, smartphone, animação a cada dois segundos, indicação de digitação, rolagem e redução de movimento. O roteiro passa a 18 mensagens, incluindo orçamento/aprovação e os exemplos adicionais.

## Correção solicitada: guardar e exemplos de atendimento — 2026-10-07

O usuário esclareceu que os documentos são guardados sem um pedido separado. Remover a última troca de guardar e mencionar que a primeira versão continua salva na resposta de atualização do relatório. No lugar, incluir ficha de atendimento e registro para prontuário, com anexos de entrada e documentos de saída dentro dos balões. O exemplo de prontuário limita-se a organizar as anotações do profissional em um registro para conferência; não promete prontuário completo, diagnóstico, prescrição ou decisão clínica autônoma.

Atualizar somente a opção Produção e sua descrição no seletor; demais cinco demonstrações e Frentes do negócio permanecem iguais. Linguagem comum, sem briefing. Manter “exemplo ilustrativo”. A disponibilidade real de geração/leitura de arquivos e versões ainda precisa ser confirmada antes de publicação.

## Aceitação

- O seletor desktop/mobile apresenta Produção na opção existente.
- A opção mantém vínculos e identidade técnica e mostra as 18 mensagens aprovadas, sem pedido separado de guardar.
- Documentos produzidos e proposta anexada aparecem dentro dos balões de ambos os participantes, sem links de download reais.
- A landing local responde na porta 3001.
- Inspeção visual pendente pelo bloqueio de acesso do navegador integrado registrado nesta conversa.

## Celular e WhatsApp — ajuste visual autorizado em 2026-10-07

O usuário pediu que o celular desta seção aproveite melhor o espaço em desktop/mobile, em diferentes larguras e alturas, mantenha proporção de um aparelho normal e tenha aparência de iPhone atual com WhatsApp. Esta autorização amplia o escopo visual somente do mockup e do espaço necessário para acomodá-lo em S03.

Usar proporção externa constante de 72:150, moldura escura fina, ilha dinâmica, indicadores de status e de início. Reproduzir o chat claro do WhatsApp no iPhone: cabeçalho claro, ícones de ligação/vídeo, balões brancos e verdes, horários, confirmação visual de leitura e cartão de documento dentro da mensagem. O remetente fica identificado de forma acessível, sem repetir seu nome visivelmente em cada balão de uma conversa individual. As representações de ligação, envio e arquivo continuam ilustrativas. Referência pública: https://about.fb.com/br/news/2024/05/mantendo-o-whatsapp-moderno-simples-e-acessivel/ . Não afirmar igualdade pixel a pixel ou uma versão específica do aplicativo.

Dimensionar o aparelho pela largura disponível e pela altura da janela, sem deformar sua proporção e sem reduzir as mensagens abaixo de 13 px. Em telas baixas, permitir rolagem normal da página e crescimento do cartão, em vez de cortar ou miniaturizar o aparelho. A conversa conserva rolagem própria, animação de entrada, revelação a cada dois segundos e redução de movimento. Manter duas colunas a partir de 1024 px e seletor acima do celular abaixo disso, com as seis opções existentes.

Estilos do aparelho em módulo CSS para evitar as regras antigas de miniaturização. As correções do cartão no CSS global devem estar restritas a #intencoes. Não alterar textos do roteiro, preços ou outras seções nesta etapa.
