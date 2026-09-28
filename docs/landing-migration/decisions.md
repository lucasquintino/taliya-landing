# Decisões e pendências

## Decisões aplicadas nesta retomada

| ID | Decisão | Origem |
|---|---|---|
| D-001 | Reiniciar em clone limpo do commit do GitHub; manter a tentativa anterior em diretório separado sem a usar como base. | Pedido atual e confirmação Git |
| D-002 | Preservar a landing antiga em `/pilates`; construir a home Copiloto em `/` conforme etapa SEO, sem redirecionar `/pilates` por suposição. | Preservação do código + política de legado do SEO |
| D-003 | Troca de copy não autoriza mudanças de componentes, layout ou interação. | Correção explícita do usuário |
| D-004 | SEO, Mural S06, integração final e arquitetura/reuso após integração são exceções autorizadas e delimitadas. | Pedido atual |
| D-005 | Não adicionar faixa S02, converter a calculadora S08 em fluxos ou criar controles/subtabs/forms durante as etapas de copy. | Aplicação do limite atual sobre o pacote |
| D-006 | Usar o JSON da landing como autoridade de copy e manter o SEO separado como autoridade técnica de descoberta. | Fontes do ZIP |
| D-007 | Considerar o app pronto conforme a atualização direta do usuário em 25/09/2026; o estado `prelaunch` dos documentos de 18–19/09 é um registro anterior. Usar a variante de conteúdo compatível com o produto pronto, sem presumir que trial, preço, checkout ou URL de onboarding estejam ativos. | Atualização direta do usuário; gates comerciais remanescentes do pacote |

## Pendências que não bloqueiam a fundação

- Baseline visual executável da rota `/pilates` (desktop/mobile).
- Em S02, identificar textos Copiloto que cabem em slots existentes; se não houver, não inserir a faixa.
- Em S08, verificar se existe copy segura que possa substituir textos da calculadora sem sugerir um cálculo novo. A lógica não pode mudar sem autorização específica.
- Confirmar em S06 a menor composição para Mural usando os mockups/balões existentes.
- Em S002, documentar decisão local de canonical e o destino legado antes de publicação; produção não será alterada.

## Bloqueios de publicação

Nenhum deploy está autorizado. Domínio canônico, redirecionamentos de legado, política jurídica, configuração de robôs e acesso a Search Console/Bing/CDN são validações externas ou decisões de lançamento, não presumidas aqui.
