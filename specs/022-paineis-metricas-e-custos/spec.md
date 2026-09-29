# 022 — Painéis SaaS, definições e limites de custo

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Analytics + produto.
**Dependências:** 021.

## Resultado
Entregar seis painéis utilizáveis com definições explícitas, sem construir BI no Internal.

## Requisitos verificáveis
### R022-01
Configurar aquisição, conversão, conteúdo, atendimento, ativação/retenção e receita.

**Aceite:** Cada painel tem perguntas, denominadores, filtros, unidade, janela, timezone e fonte; negócios e usuários não se confundem.
**Verificação:** C022-01.

### R022-02
Usar funil principal com chat/vídeo opcionais.

**Aceite:** Compra direta permanece no denominador correto; agent_assisted indica associação, não ganho causal comprovado.
**Verificação:** C022-02.

### R022-03
Definir MRR, caixa, churn, garantia e retenção de modo reproduzível.

**Aceite:** Anual é normalizado; cancelamento pedido difere do acesso encerrado; reembolso pedido/concluído é separado; coortes imaturas não recebem taxa inventada.
**Verificação:** C022-03.

### R022-04
Controlar orçamento sem prometer gratuidade universal.

**Aceite:** Estimativa usa volume real e addons; teto US$50 é proposta sujeita à aprovação; Group Analytics/replay/Workflows não são ativados automaticamente.
**Verificação:** C022-04.

### R022-05
Habilitar métricas por negócio sem forçar addon pago.

**Aceite:** business_id existe na origem; consultas/exports canônicos fornecem agregação por negócio; Group Analytics só entra após teste de necessidade/custo.
**Verificação:** C022-05.

## Limites
Não reconstruir app/billing, não implantar sem autorização, não criar outro CRM/BI, não ampliar poderes do agente. Preservar a aparência aprovada. Escopo não resolvido é registrado como bloqueio da tarefa dependente; não inventar endpoints, credenciais, materiais ou resultado de testes.

## Definição de conclusão
Todos os requisitos desta spec possuem evidência de implementação e teste; artefatos estão coerentes; nenhuma restrição de segurança/comercial foi afrouxada silenciosamente. Checklist de requisitos aprovada não é sinônimo de implementação concluída.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
