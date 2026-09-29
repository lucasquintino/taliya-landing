# Dados necessários para fechar as integrações da 013

Formulário de contrato, não especificação de API inventada. Para billing, preencher primeiro o contrato-alvo da 015 e depois substituir pendências por evidência da implementação e da sandbox; para Internal, obter evidência da implantação ativa. Referências e nomes de variáveis são suficientes aqui; valores de segredos ficam no mecanismo seguro do ambiente. Campos desconhecidos permanecem `pendente`.

## B013-01 — billing Asaas a construir

Correção do usuário em 2026-09-29: não existe pagamento/Asaas. O app Copiloto foi encontrado e sua identidade/negócio/acesso devem ser reutilizados. A tabela abaixo passou a ser **contrato-alvo de implementação na 015**, não busca de API publicada. Ver `../DECISAO_BILLING_2026-09-29.md`.

| Contrato | Evidência a extrair | Estado |
|---|---|---|
| Fonte e autoridade | app/backend dono, repo/SHA, oferta versionada, ambiente e responsável | desenho local em curso; publicação pendente |
| Identidade e vínculo | issuer/audience/expiração ou mecanismo equivalente, person/user/business/subscription IDs, prova de membership | app observado; vínculo comercial/billing pendente |
| Oferta | valores aprovados em centavos/moeda, mensal/anual, cartão/Pix Automático, cobrança inicial, garantia 14 dias, URLs, versão e frescor | valores documentados encontrados; confirmação atual solicitada |
| Checkout/retomada | auth, seleção de plano, idempotência, request/response sanitizados, retorno seguro, conflito de contratação ativa | pendente |
| Assinatura/acesso | estados distintos e períodos, acesso durante cancelamento, regras de primeira confirmação/renovação/falha | gate do app observado; relação com billing pendente |
| Gestão/reembolso | destino autenticado, solicitado versus confirmado, erros e responsável; sem executar operação financeira | pendente |
| Eventos | assinatura/auth do webhook, event_id, origem, versão/ordem, replay, retries, reconciliação e payload sanitizado | pendente |
| Erros | auth/forbidden, validação, conflito, rate limit, indisponibilidade, timeout antes/depois do aceite; códigos reais | pendente |

Não tratar o entitlement `trial` do clone Copiloto como a oferta aprovada. Resolver a divergência na construção da fonte única. Não pedir chaves em texto nem enviar dinheiro para testar disponibilidade. A conta sandbox e a elegibilidade Pix Automático deverão ser verificadas antes de ativar o fluxo. T013-07 fecha o desenho local; as células `pendente` são requisitos de implementação/homologação da 015, não prova de API existente.

## B013-02 — Internal autoritativo

Confirmar URL atendida, deployment ID, SHA ativo, fonte de dados/contrato, mecanismo de staff e dono de operação. A fonte `taliya-internal` em `7cbe9e9` e o Sales Inbox da landing coexistem; HTTP 401 e deploys falhados não escolhem o vencedor.

A evidência deve incluir: consulta autenticada sanitizada; papel/ator derivado no servidor; mapeamento rewrite/rota física; recibo de ação; fonte de pausa/fila; entrega humana web/WhatsApp. Não passar token por URL para fabricar evidência nem editar ambas as caixas.

## B013-03 — homologação e permissões

Registrar ambiente, proprietário, IDs sintéticos, serviços/canais liberados, operações permitidas, janela de uso, limite monetário e volume máximo, mecanismo seguro das credenciais e responsável por limpeza. Separar leitura sem custo, inferência paga, envio a canal de teste e operações financeiras. Uma autorização não implica as demais. Produção permanece fora do escopo até decisão específica.

Ratificar metas propostas antes de usá-las como gate: latência/qualidade, retenção/privacidade, orçamento PostHog/Agents, periodicidade de relacionamento e rollout. Falha de homologação deve produzir evidência/ação corretiva; não autoriza outro modelo ou esforço.

## B013-04 — catálogo

Para cada material: arquivo/URL real, ID/versão, capacidade demonstrada, direitos, natureza da evidência (ilustração/demo/depoimento comprovado), aprovação e dono, legenda/transcrição, thumbnail e revisão/retirada. O inventário de arquivos existentes é reaproveitável; não comprova aprovação editorial.

## Fechamento

Anexar evidência ao `verification.md` da spec correspondente, atualizar `current-contracts.md`, tasks/status/matriz e os bloqueios de `planning/execution.json` com referência verificável. Não marcar G0 porque este formulário existe. T013-07 foi concluída localmente; T013-08/09 continuam abertas até as respectivas condições de saída.
