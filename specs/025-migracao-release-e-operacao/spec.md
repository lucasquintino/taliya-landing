# 025 — Migração, publicação controlada e operação

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Liderança técnica + operação/produto.
**Dependências:** 024.

## Resultado
Encerrar com serviço operável, rollback seguro e indicadores confiáveis, não apenas código compilando.

## Requisitos verificáveis
### R025-01
Migrar dados/sessões com ensaio e reconciliação.

**Aceite:** Registros legados permanecem marcados; não há merge automático por e-mail; backup/restore e contagens são verificados.
**Verificação:** C025-01.

### R025-02
Publicar por gates com autorização explícita.

**Aceite:** Interno → 5% → 25% → 100% conforme evidência; não confundir percentual de tráfego com conclusão da entrega.
**Verificação:** C025-02.

### R025-03
Manter rollback sem agente Pilates.

**Aceite:** Kill switch desliga geração e preserva assinar/entrar/ajuda/handoff; schemas compatíveis e eventos continuam íntegros.
**Verificação:** C025-03.

### R025-04
Entregar responsáveis, alertas e procedimentos.

**Aceite:** Há dono de fila, mídia, fonte comercial, financeiro e analytics; problemas de custo, privacidade e entrega têm resposta definida.
**Verificação:** C025-04.

### R025-05
Fechar 100% por aceite operacional.

**Aceite:** Todos os gates obrigatórios aprovados, estabilização observada, documentação alinhada e nenhuma pendência escondida de segurança/contratação/dados.
**Verificação:** C025-05.

## Limites
Não reconstruir app/billing, não implantar sem autorização, não criar outro CRM/BI, não ampliar poderes do agente. Preservar a aparência aprovada. Escopo não resolvido é registrado como bloqueio da tarefa dependente; não inventar endpoints, credenciais, materiais ou resultado de testes.

## Definição de conclusão
Todos os requisitos desta spec possuem evidência de implementação e teste; artefatos estão coerentes; nenhuma restrição de segurança/comercial foi afrouxada silenciosamente. Checklist de requisitos aprovada não é sinônimo de implementação concluída.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
