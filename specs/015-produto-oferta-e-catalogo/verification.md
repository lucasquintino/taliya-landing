# 015 — Verificação e evidências de oferta, billing e catálogo

**Estado:** casos especificados; nenhum caso de aceitação foi executado nesta auditoria.

## C015-01 · R015-01
**Cenário:** Perguntar sobre capacidades atuais, recursos indisponíveis e funcionamento antigo de Pilates; comparar resposta e FAQ com a fonte aprovada.

**Resultado exigido:** Somente recursos confirmados entram; equipes/booking e outros recursos antigos não são presumidos por aparecer em documento histórico.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C015-02 · R015-02
**Cenário:** Comparar página, resposta do agente e oferta de contratação em mensal/anual; perguntar sobre teste sem cartão e garantia vigente.

**Resultado exigido:** Mensal/anual, cobrança inicial e garantia de 14 dias são coerentes; nenhum teste sem cartão é vendido.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C015-03 · R015-03
**Cenário:** Importar creator demonstrando produto e depoimento verificado; tentar publicar um arquivo sem aprovação ou direitos registrados.

**Resultado exigido:** Cada material publicado possui ID, tipo, URL autorizada, versão, resumo/transcrição, direitos e status; UGC encenado não vira depoimento.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C015-04 · R015-04
**Cenário:** Desativar a fonte de produto e retirar o vídeo solicitado; verificar que o agente informa o limite sem oferecer link, preço ou acesso inventado.

**Resultado exigido:** A informação ausente é explicitada; o agente não inventa preço, link, prazo ou mídia e o CTA depende de destino válido.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C015-05 · R015-05
**Cenário:** Atualizar oferta, FAQ e situação de material durante uma sessão existente; conferir invalidação e versão usada em cada nova resposta.

**Resultado exigido:** Oferta nova é consultada no momento relevante; material retirado não é emitido em sessão antiga; compatibilidade e freshness ficam registradas.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C015-06 · R015-06
**Cenário:** Iniciar contratação direta sem chat em mensal/anual × cartão/Pix Automático; repetir a intenção, forjar business_id e simular timeout após aceitação pelo provedor.

**Resultado exigido:** Oferta/versão e negócio vêm do servidor; cada tentativa tem recibo único e vínculo canônico; cartão usa checkout recorrente hospedado; Pix exige autorização elegível e QR inicial. Nenhuma forma de pagamento indisponível é anunciada como ativa.

**Evidência a produzir:** testes de contrato/integração locais e ensaio Asaas sandbox autorizado, com IDs sanitizados, SHA, conta/ambiente, esperado/obtido e custo.

## C015-07 · R015-07
**Cenário:** Entregar webhook duplicado/fora de ordem, chamar URL de sucesso sem webhook, receber pagamento Pix inicial seguido de recusa de autorização e repetir após reinício.

**Resultado exigido:** Inbox única por evento, HTTP 200 somente após persistência, efeitos e acesso idempotentes; redirect não concede acesso; pagamento do ciclo e autorização da recorrência preservados como fatos distintos.

**Evidência a produzir:** testes com banco descartável e sandbox autorizado, recibos e transições sanitizados, replay e reconciliação observados.

## C015-08 · R015-08
**Cenário:** Consultar assinatura, solicitar cancelamento/reembolso dentro da garantia, simular falha/timeout e receber confirmação financeira tardia.

**Resultado exigido:** Solicitação e confirmação são estados distintos; nenhum reembolso é declarado antes do evento do billing; acesso/renovação refletem fatos pagos e política aprovada, com recuperação após timeout.

**Evidência a produzir:** teste de estado local e ensaio sandbox autorizado; nenhuma operação financeira real sem autorização específica.

## Regressões adicionais da frente
- Preço na página e resposta comercial vêm da mesma versão publicada pelo novo billing.
- Contratação direta, replay de webhook e retorno sem confirmação não liberam acesso indevido.
- Pergunta sobre teste sem cartão recebe explicação da garantia atual.
- Vídeo removido/privado não gera card quebrado nem URL inventada.
- Creator contratado não é apresentado como cliente comprovado.
- Fonte indisponível produz fallback honesto sem retornar planos de Pilates.

Os IDs de caso são estáveis; o detalhamento técnico cresce com os contratos reais. Mock não comprova chamada externa, análise estática não comprova produção.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
