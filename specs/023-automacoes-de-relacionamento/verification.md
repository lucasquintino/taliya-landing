# 023 — Verificação e evidências

**Estado:** casos especificados; nenhum caso de aceitação foi executado nesta auditoria.

## C023-01 · R023-01
**Cenário:** Executar dry-run dos fluxos de contratação abandonada, primeiro valor e recuperação de uso com fixtures elegíveis.

**Resultado exigido:** Abandono elegível, pagamento sem primeiro valor e inatividade elegível possuem templates, limites e destino útil.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C023-02 · R023-02
**Cenário:** Pagar, ativar produto, manter Pix pendente legítimo ou revogar consentimento imediatamente antes do envio agendado; conferir revalidação.

**Resultado exigido:** Pagamento, acesso, opt-out, humano ativo e canal são conferidos no backend no instante da entrega; dado desatualizado no PostHog não decide sozinho.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C023-03 · R023-03
**Cenário:** Executar confirmação, renovação e estorno existentes enquanto Workflows está ativo em sandbox; verificar um emissor por notificação.

**Resultado exigido:** Confirmação/cobrança/estorno não migram sem motivo nem são enviados duas vezes por PostHog + n8n + app.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C023-04 · R023-04
**Cenário:** Repetir gatilho e manter pessoa em coorte desatualizada após opt-out; verificar limite global e supressão.

**Resultado exigido:** No máximo uma mensagem por gatilho e teto global proposto de uma mensagem de relacionamento por sete dias; opt-out impede novos envios dessa categoria.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C023-05 · R023-05
**Cenário:** Manter configuração em dry-run e depois autorizar uma coorte de teste; conferir canal, reputação, destinatários e kill switch sem envio público não autorizado.

**Resultado exigido:** Fluxos estão testados em dry-run, modelos/domínio/canais validados e desligados até autorização específica de campanha/produção.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## Regressões adicionais da frente
- Pessoa paga um instante antes do envio: recuperação de abandono é suprimida.
- Pix pendente legítimo não recebe falsa cobrança/compra nova para recuperar abandono.
- Opt-out vale mesmo que a pessoa continue numa coorte antiga.
- App, n8n e PostHog não enviam confirmação duplicada.
- Gatilho repetido não gera várias mensagens e dry-run não contata usuários reais.

Os IDs de caso são estáveis; o detalhamento técnico cresce com os contratos reais. Mock não comprova chamada externa, análise estática não comprova produção.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
