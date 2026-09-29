# 015 — Fonte única de produto, oferta, billing e materiais

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Produto + frontend/backend.
**Dependências:** 013, 014.

## Tarefas
- [ ] **T015-01** — Consolidar capacidades reais por integração/documento aprovado e remover catálogo comercial de Pilates do caminho v2. Requisitos: R015-01. Recorte: [execution.md#t015-01](execution.md#t015-01).
- [ ] **T015-02** — Implementar fonte server-side e leitor da oferta versionada, com valores aprovados em centavos e disponibilidade explícita. Requisitos: R015-02, R015-05. Recorte: [execution.md#t015-02](execution.md#t015-02).
- [ ] **T015-03** — Definir schema do catálogo compartilhado e pasta/serviço já existente para armazenamento. Requisitos: R015-03. Recorte: [execution.md#t015-03](execution.md#t015-03).
- [ ] **T015-04** — Importar somente vídeos/demos/UGCs entregues e autorizados; preparar transcrição/resumo/caption. Requisitos: R015-03. Recorte: [execution.md#t015-04](execution.md#t015-04).
- [ ] **T015-05** — Implementar validação de publicação, URL, revisão e expiração de material; não criar CMS novo. Requisitos: R015-03, R015-04, R015-05. Recorte: [execution.md#t015-05](execution.md#t015-05).
- [ ] **T015-06** — Convergir oferta, billing e catálogo; testar mudança de versão/material em conversa e registrar guia de operação. Requisitos: R015-01 a R015-08. Recorte: [execution.md#t015-06](execution.md#t015-06).
- [ ] **T015-07** — Criar modelo/migrações de tentativas, vínculo Asaas por negócio e fatos financeiros sem alterar Auth. Requisitos: R015-06, R015-07. Recorte: [execution.md#t015-07](execution.md#t015-07).
- [ ] **T015-08** — Implementar checkout hospedado para cartão recorrente mensal/anual com idempotência e retorno sem concessão de acesso. Requisitos: R015-06. Recorte: [execution.md#t015-08](execution.md#t015-08).
- [ ] **T015-09** — Implementar Pix Automático mensal/anual com QR inicial e estado de autorização separado do pagamento. Requisitos: R015-06, R015-07. Recorte: [execution.md#t015-09](execution.md#t015-09).
- [ ] **T015-10** — Implementar webhook autenticado, inbox, processamento idempotente, reconciliação e projeção de acesso. Requisitos: R015-07. Recorte: [execution.md#t015-10](execution.md#t015-10).
- [ ] **T015-11** — Implementar consulta/gestão de assinatura, cancelamento e solicitação de reembolso com estados explícitos. Requisitos: R015-08. Recorte: [execution.md#t015-11](execution.md#t015-11).
- [ ] **T015-12** — Homologar no sandbox autorizado as quatro combinações, falhas, replay, cancelamento e garantia. Requisitos: R015-06, R015-07, R015-08. Recorte: [execution.md#t015-12](execution.md#t015-12).

Não marcar uma tarefa porque o arquivo existe. Acrescentar caminho do diff, comando e resultado verificável ao concluí-la. Se o código atual já atende, comprovar por teste e registrar reuso em vez de reimplementar.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
