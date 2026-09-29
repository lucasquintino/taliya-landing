# 015 — Fonte única de produto, oferta, billing e materiais

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Produto + frontend/backend.
**Dependências:** 013, 014.

## Abordagem técnica
Construir oferta e billing Asaas no backend do app que já possui Auth, negócio e gate de acesso; landing e agente consomem a oferta publicada. Ver `../../docs/taliya-sdd/DECISAO_BILLING_2026-09-29.md`.

A abordagem de domínio e as interfaces propostas estão em `../../docs/taliya-sdd/03_ARQUITETURA_E_CONTRATOS.md`. A implementação deve referenciar as interfaces reais descobertas na 013; os caminhos abaixo pertencem ao ZIP inspecionado e são candidatos de integração, não prova da árvore atual.

## Pontos de integração observados
- `data/landing/niches/pilates.ts`
- `lib/landing/ai-attendant/commercial-knowledge.ts`
- `services/taliya-agent-runtime/app/shared/product_knowledge/source.py`
- `docs/landing-migration/shared-contracts.md`

## Ordem de execução
1. Consolidar capacidades reais por integração/documento aprovado e remover catálogo comercial de Pilates do caminho v2.
2. Implementar fonte server-side de oferta com versão/data/preço em centavos e leitor para landing/agente; impedir oferta sem aprovação vigente.
3. Definir schema do catálogo compartilhado e pasta/serviço já existente para armazenamento.
4. Importar somente vídeos/demos/UGCs entregues e autorizados; preparar transcrição/resumo/caption.
5. Implementar validação de publicação, URL, revisão e expiração de material; não criar CMS novo.
6. Definir ledger de tentativas, IDs canônicos, vínculo com cliente do provedor e migrações aditivas no backend do app.
7. Implementar checkout hospedado de cartão recorrente e autorização Pix Automático em caminhos distintos, sem efeito na IA.
8. Implementar inbox de webhook, worker/reconciliação, projeção de acesso e estados de cancelamento/reembolso.
9. Homologar as quatro combinações e falhas em sandbox autorizado; testar mudança de oferta/material durante conversa ativa e publicar guia de edição.

## Dados, permissões e observabilidade
Cada mudança de estado material deve ter ator, autorização, recibo persistido e evento de domínio. Fronteiras entre bancos/serviços usam outbox e reconciliação, não uma transação distribuída presumida. Métricas públicas de browser não comprovam dinheiro ou acesso. Não registrar segredos ou dados de terceiros em prompts/analytics.

## Testes e rollback
Executar os casos `C015-01` a `C015-08` e a regressão dos contratos afetados. Testes locais verificam contratos, autorização, replay e resultados desconhecidos; integração Asaas exige conta sandbox e limite autorizados. Usar feature flag da capacidade e migrações compatíveis para rollback; nenhuma volta ao roteiro Pilates. Registrar em `verification.md`.

## Esforço de referência
A estimativa antiga de 2–3 dias não cobre construir billing. Reestimar após a 013 e a verificação da conta Asaas; nenhuma duração do snapshot é compromisso de entrega.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
