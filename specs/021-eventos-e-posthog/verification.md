# 021 — Verificação e evidências

**Estado:** casos especificados; nenhum caso de aceitação foi executado nesta auditoria.

## C021-01 · R021-01
**Cenário:** Validar cada nome de evento, versão, IDs, produtor e timestamp; repetir a mesma operação lógica nos transportes disponíveis.

**Resultado exigido:** Cada evento tem produtor, ocorrência e chave de dedup; marcos de conta/negócio não usam identidade analítica como credencial.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C021-02 · R021-02
**Cenário:** Fabricar payment_confirmed no browser e comparar com evento/registro financeiro canônico; verificar que não altera acesso nem a apuração oficial.

**Resultado exigido:** Pagamento/ativação não derivam de clique ou retorno de checkout; ferramentas da IA não incluem track_event.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C021-03 · R021-03
**Cenário:** Acompanhar visita anônima, login, troca de conta, compra e app com dois membros no mesmo negócio; verificar correlação sem duplicar assinante.

**Resultado exigido:** ID estável após auth, reset no logout e business_id separado; visitantes não viram leads identificados automaticamente.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C021-04 · R021-04
**Cenário:** Negar coleta opcional, testar ambiente de desenvolvimento e atingir limite de gravação; conferir ausência de PII bruta e separação de dados.

**Resultado exigido:** Autocapture desnecessário/replay sensível estão off; testes não contaminam produção e nenhum texto completo de chat/PII sensível é enviado por padrão.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C021-05 · R021-05
**Cenário:** Desligar PostHog/relay, produzir acontecimentos reais e retomar; verificar recuperação, dedup, lacuna visível e conciliação com fonte de origem.

**Resultado exigido:** Outbox reenvia de forma idempotente; dashboards financeiros conferem fonte canônica; quota perdida é registrada como lacuna, não venda inexistente.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## Regressões adicionais da frente
- Visita anônima, login, compra e app mantêm jornada válida sem expor credenciais.
- Duas pessoas no mesmo negócio não contam dois assinantes.
- Bloquear cookies analíticos não impede compra nem gera reconstrução invasiva do visitante.
- PostHog indisponível não perde pagamento e mostra atraso quando o relay retorna.
- Evento payment_confirmed fabricado no navegador não altera acesso nem a fonte da receita oficial.

Os IDs de caso são estáveis; o detalhamento técnico cresce com os contratos reais. Mock não comprova chamada externa, análise estática não comprova produção.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
