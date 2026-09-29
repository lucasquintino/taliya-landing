# 021 — Instrumentação confiável e integração PostHog

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Backend/frontend + analytics.
**Dependências:** 017, 018, 019, 020.

## Resultado
Registrar acontecimentos canônicos uma vez e conectar a jornada sem depender do modelo.

## Requisitos verificáveis
### R021-01
Adotar contrato de eventos com IDs, versões, origem e tempo.

**Aceite:** Cada evento tem produtor, ocorrência e chave de dedup; marcos de conta/negócio não usam identidade analítica como credencial.
**Verificação:** C021-01.

### R021-02
Emitir acontecimentos financeiros/de valor pelo serviço responsável.

**Aceite:** Pagamento/ativação não derivam de clique ou retorno de checkout; ferramentas da IA não incluem track_event.
**Verificação:** C021-02.

### R021-03
Instrumentar web, app e backend com identidade consistente.

**Aceite:** ID estável após auth, reset no logout e business_id separado; visitantes não viram leads identificados automaticamente.
**Verificação:** C021-03.

### R021-04
Controlar privacidade, ambientes e consumo.

**Aceite:** Autocapture desnecessário/replay sensível estão off; testes não contaminam produção e nenhum texto completo de chat/PII sensível é enviado por padrão.
**Verificação:** C021-04.

### R021-05
Garantir entrega recuperável e reconciliação.

**Aceite:** Outbox reenvia de forma idempotente; dashboards financeiros conferem fonte canônica; quota perdida é registrada como lacuna, não venda inexistente.
**Verificação:** C021-05.

## Limites
Não reconstruir app/billing, não implantar sem autorização, não criar outro CRM/BI, não ampliar poderes do agente. Preservar a aparência aprovada. Escopo não resolvido é registrado como bloqueio da tarefa dependente; não inventar endpoints, credenciais, materiais ou resultado de testes.

## Definição de conclusão
Todos os requisitos desta spec possuem evidência de implementação e teste; artefatos estão coerentes; nenhuma restrição de segurança/comercial foi afrouxada silenciosamente. Checklist de requisitos aprovada não é sinônimo de implementação concluída.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
