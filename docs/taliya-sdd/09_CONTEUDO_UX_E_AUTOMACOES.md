# Conteúdo, UX e relacionamento
## Catálogo de lançamento proposto
Um explicativo geral; demonstrações dos fluxos prioritários realmente disponíveis (ex.: organizar serviço/agenda, registrar recebimento, usar lembrete e alternar app/WhatsApp), com a lista final derivada do produto pronto; UGCs fornecidos e autorizados; uma orientação de começo/assinatura/garantia. Não afirmar quantidade entregue antes do inventário.

Campos: asset_id, tipo, título, resumo, transcrição/legenda, URL/thumbnail aprovadas, duração real, capability_ids, contexto profissional amplo, versão de produto, situação de publicação, classificação de evidência, direitos/responsável/revisão. Não cadastrar nomes de clientes, resultados e depoimentos fictícios.

Seleção: explicativo para visão geral; demo para como fazer; UGC para contexto/uso; depoimento verificado somente quando houver evidência. Um card por resposta e opção de começar sem assistir. Fonte de preço/garantia continua no billing, mesmo se um vídeo citar outra oferta.

## Landing
Manter estrutura e tokens. CTA principal `Começar agora` → fluxo pronto; CTA secundário `Tirar dúvidas` → agente; demonstração → material/fluxo real; `Já sou cliente` → app/login/gestão. Não fazer o visitante conversar para contratar. Saudações e chips vazios podem ser determinísticos; compreensão da pergunta é do LLM, não regex comercial rígida.

Garantia pode ser apresentada de modo comercial simples: experimentar com possibilidade de reembolso, sem insistência visual em cartão obrigatório. Porém oferta/contratação devem deixar claros cobrança inicial, valor, renovação e garantia. Não dizer grátis/sem cobrança se há cobrança imediata. O agente explica com clareza ao ser perguntado.

No chat: português natural, resposta direta, uma pergunta necessária por vez, sem diagnóstico obrigatório, sem coleta repetida e sem pressão. Fora do escopo: declarar limite e encaminhar. Suporte de conta exige login antes de informação privada.

## Três automações propostas
| Fluxo | Gatilho | Espera inicial | Supressões | Ação |
|---|---|---|---|---|
| Retomar contratação | checkout realmente abandonado/expirado | 2 h após elegibilidade confirmada | pago, pendência financeira legítima, opt-out, humano ativo, sem permissão/canal | um convite com destino de retomada seguro |
| Chegar ao primeiro valor | pagamento confirmado sem ativação útil | 24 h | ativado, sem acesso, suporte aberto/pausa, opt-out aplicável | um tutorial curto contextual |
| Recuperar uso | negócio elegível sem atividade útil | 7 dias | sem assinatura/acesso válido, contato recente, opt-out, atendimento ativo | uma ajuda prática, sem ameaça/urgência falsa |

Prazos são propostas operacionais, não obrigações legais nem características prontas do produto. Uma mensagem por gatilho e limite global proposto de uma mensagem de relacionamento por sete dias. Ajustar após dados sem criar cadência agressiva. O emissor financeiro existente continua dono de confirmações/renovação/estorno.

Workflows pode orquestrar e solicitar envio, mas o backend confere elegibilidade no momento e usa o provedor transacional/canal já existente quando apropriado. Se forem usados e-mails nativos do PostHog, validar domínio, reputação, opt-out e limites diários/horários — franquia mensal não basta. [P7/P8]

Não presumir acesso direto nativo ao WhatsApp nem copiar política de janela de memória; validar provedor atual na 020. Não enviar campanha real durante teste. Fluxos ficam em dry-run até autorização.
