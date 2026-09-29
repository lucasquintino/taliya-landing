# Adendo de escopo — billing Taliya — 2026-09-29

Fonte da mudança: o usuário esclareceu nesta conversa que ainda não há pagamentos nem integração Asaas e que esta implementação deve ser feita agora. Esta decisão substitui somente a premissa anterior de billing pronto nos artefatos executáveis do programa 013–025. App e autenticação existentes continuam sendo reutilizados. O plano v3 original permanece preservado como proveniência; nenhuma evidência antiga de busca por serviço publicado prova que ele exista.

## Estado observado e fonte comercial

- A landing contém valores de R$ 59,90/mês e R$ 599/ano em `data/landing/niches/pilates.ts` e o documento aprovado do app `Contrato_Assinatura_Acesso_Midia_Suporte_v1_1.md` contém os mesmos valores. O usuário informou que os valores estão documentados. A confirmação de que estes dois valores são os vigentes foi solicitada antes de ativar cobrança; o trial sem cartão e a oferta founders no documento antigo não são herdados automaticamente.
- A landing ainda anuncia teste grátis e garantia de 30 dias em pontos distintos. A decisão atual do usuário é cobrança na contratação e garantia de reembolso em 14 dias. O código comercial será ajustado quando a fonte única de oferta e o caminho de contratação estiverem implementados.
- No app Copiloto foram observados Auth, `business_members`, `access_entitlements` e a decisão de acesso `e01_access_decision`. Não foi encontrado serviço de checkout/webhook Asaas. `access_entitlements.state = trial` é legado de acesso e não autoriza anunciar teste grátis.
- Não há conta/ambiente Asaas disponibilizado nesta execução, nem elegibilidade de Pix Automático comprovada. Nenhuma chamada financeira ou teste remoto foi feito.

## Dono e interfaces a implementar

O backend do app, que já possui a identidade autenticada, o negócio e o gate de acesso, será o dono dos fatos financeiros e do vínculo `business_id` ↔ cliente/assinatura do provedor. A landing e o agente consumirão uma oferta pública versionada e solicitarão a abertura de contratação ao backend, sem criar contas paralelas nem decidir acesso. A implementação deve manter a contratação direta disponível sem conversa com a IA. Escolhas de caminho físico, schema e autenticação serão detalhadas na spec de execução antes do código, a partir do checkout atual do app; isto não declara endpoint implantado.

1. **Oferta:** um registro publicável com versão, centavos BRL, periodicidade, garantia de 14 dias, disponibilidade de cada forma de pagamento e data de vigência. Sem valor/URL válido, a opção correspondente permanece indisponível; nenhum preço é gerado pelo modelo.
2. **Cartão recorrente:** Asaas Checkout hospedado com `chargeTypes=RECURRENT`, `billingTypes=[CREDIT_CARD]`, `subscription` mensal/anual e primeira cobrança na contratação. Associar tentativa a pessoa/negócio autenticados por ID interno e `externalReference`; receber `CHECKOUT_PAID`, assinatura e cobrança por webhook. O retorno `successUrl` serve apenas à navegação.
3. **Pix Automático:** criar cliente Asaas vinculado ao negócio e autorização com QR de pagamento inicial, frequência mensal/anual e `paymentCreationMode=SUBSCRIPTION` quando a conta for elegível. Pagamento inicial e ativação da autorização são fatos distintos. Se o pagamento inicial for recebido mas a recorrência recusada, registrar ambos e encaminhar o próximo ciclo a uma resolução explícita; a política exata de acesso ao ciclo já pago precisa ser fixada antes do efeito.
4. **Confirmação e acesso:** webhook autenticado é persistido em inbox com chave única `event.id` antes do HTTP 200; worker/reconciliação atualizam fatos e `access_entitlements` de forma idempotente e auditável. Timeout após criação de checkout/autorização exige busca e reconciliação, não nova criação cega. Analytics recebe eventos do billing depois do fato; não controla acesso.
5. **Gestão:** cancelamento, falha, reembolso solicitado/confirmado e renovação têm estados próprios. Nenhuma operação financeira é disparada por ferramenta da IA, clique de retorno ou fala do usuário. A garantia de 14 dias é política de produto; a interface de solicitação e o ato de reembolso exigem contrato e autorização específicos.

## Sequência e gates

A 013 registra a correção da premissa, fonte dos valores, dono dos dados, contratos-alvo e dependências. A 014 estabelece vínculo/autorização. A 015 passa a construir a fonte de oferta e billing Asaas com testes locais e, quando existir conta sandbox autorizada, homologação das quatro combinações. As specs 016–025 consomem os contratos resultantes. Uma spec permanece ativa por vez. O aceite de G0 não representará billing implementado; a 015 só será aceita com código, integração e evidências aplicáveis, sem mocks convertidos em aceite remoto.

Pendências externas para ativação: confirmação da oferta vigente; conta Asaas sandbox, credencial pelo mecanismo seguro, elegibilidade de Pix Automático; domínio/URLs de retorno aprovados; ambiente e limite de gasto para testes remotos; depois autorização separada para produção. A pendência de deployment/staff do Internal permanece independente.

## Documentação oficial consultada em 2026-09-29

- Checkout recorrente com cartão e `successUrl` sem valor de confirmação: https://docs.asaas.com/docs/checkout-com-assinatura-recorrente
- Criação do checkout, `externalReference` e cliente: https://docs.asaas.com/reference/criar-novo-checkout e https://docs.asaas.com/docs/como-informar-os-dados-do-cliente
- Pix Automático, elegibilidade, `SUBSCRIPTION`, pagamento inicial e autorização: https://docs.asaas.com/docs/pix-automatico-implementacao e https://docs.asaas.com/reference/criar-uma-autorizacao-pix-automatico
- Fluxos de webhook e entrega idempotente: https://docs.asaas.com/docs/fluxos-de-webhook e https://docs.asaas.com/docs/how-to-implement-idempotence-in-webhooks

Essas referências descrevem a API pública, não disponibilidade ou habilitação na conta Taliya.
