# Verificação — Produção com anexos

Data: 2026-10-07.

## Executado

- `git diff --check`: passou.
- `npx tsc --noEmit --incremental false`: passou, sem erros.
- ESLint nos quatro arquivos alterados da seção/contrato/mockup: passou, sem erros ou warnings.
- Configuração comparada ao snapshot anterior: somente a opção Produção mudou; outras intenções, demais seções e preços iguais.
- Roteiro com 16 mensagens, orçamento/aprovação primeiro, cinco cartões de PDF e aviso exemplo ilustrativo preservado.
- Renderização estática do componente real de mensagem: anexos com nome/metadados dentro dos balões de ambos os participantes, fundo claro/verde conforme remetente, sem links/botões de download real. As 50 mensagens das outras cinco demonstrações produziram HTML igual ao componente anterior.
- Landing local na porta 3001: HTTP 200.

## Atualização — ficha e registro para prontuário

Em 2026-10-07, o usuário pediu remover a troca de guardar e incluir ficha/prontuário. Roteiro atualizado para 18 mensagens e oito anexos, com entrada e saída nos novos exemplos. Verificação do catálogo confirmou ausência de pedido de guardar e preservação de todas as outras demonstrações e preços; diff sem erros; HTTP 200. Conferência visual continua pendente.

## Limites atuais

Inspeção visual desktop/mobile e da animação não executada pelo bloqueio da ferramenta de navegador nesta conversa. Tamanhos relativos, quebra de nome, smartphone, lógica de rolagem e redução de movimento preservados no código; isso não substitui conferência visual.

Arquivos e metadados são ilustrativos, sem geração, upload ou download reais. Disponibilidade do produto pendente; conteúdo da demonstração aprovado em 2026-10-07 com “ok, proximo”, após os exemplos de ficha/registro para prontuário. As tarefas visuais do recorte de celular proporcional permanecem independentes. Sem publicação.

## Celular proporcional e WhatsApp — 2026-10-07

- TypeScript completo e ESLint dos dois componentes alterados: passaram.
- CSS do módulo compilado pelo servidor local, com aspect-ratio 72/150 e container units presentes. As regras que liberam a altura do cartão estão restritas a #intencoes.
- Renderização estática dos seis mockups e das 68 mensagens atuais: passou. Os oito anexos de Produção mantêm nomes/metadados dentro do balão de seu remetente, sem ações reais de download. Cabeçalho e aviso exemplo ilustrativo presentes; área da conversa pode receber foco para rolagem pelo teclado.
- Lógica de revelação, contato, rolagem e redução de movimento comparada ao snapshot anterior: igual. Animações de entrada e flutuação foram mantidas no módulo, com desativação em redução de movimento.
- Todas as outras intenções e demais dados/preços comparados ao snapshot: iguais. O roteiro de Produção recebeu edição concorrente de conteúdo durante esta etapa (18 mensagens e oito anexos); essa edição foi preservada, sem alteração de roteiro por esta implementação visual.
- Fórmulas de escala verificadas em 12 combinações de largura/altura, de 320×568 até 1920×1080, incluindo tablet e desktop de 480 px de altura. A largura calculada não excede o espaço estimado da coluna e a fonte da conversa fica entre 13 e 16 px. Exemplos calculados: 254×529 em 320×568; 324×675 em 390×844; 320×667 em 1366×768; 420×875 em 1920×1080. Esses números usam estimativas da coluna e não são medições de layout de navegador.
- Servidor local na porta 3001: HTTP 200; dois stylesheets publicados localmente incluem o módulo e as correções do cartão.
- git diff --check: passou.

### Limite visual desta etapa

Não houve inspeção visual desktop/mobile nem comparação pixel a pixel com o WhatsApp. O acesso local foi rejeitado pela política da ferramenta de navegador nesta conversa; não foi usado outro navegador, Playwright ou renderização alternativa para contornar essa rejeição. A revisão humana permanece pendente em http://localhost:3001/#intencoes . Em telas baixas, o cartão pode ultrapassar a janela e a página rola normalmente para manter o aparelho legível. Nenhuma publicação.
