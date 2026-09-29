# 023 — Automações enxutas de relacionamento

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Operação + backend/analytics.
**Dependências:** 017, 020, 021, 022.

## Resultado
Recuperar jornadas elegíveis com regras previsíveis e um único responsável por cada mensagem.

## Requisitos verificáveis
### R023-01
Implementar apenas três fluxos de relacionamento propostos.

**Aceite:** Abandono elegível, pagamento sem primeiro valor e inatividade elegível possuem templates, limites e destino útil.
**Verificação:** C023-01.

### R023-02
Revalidar elegibilidade e consentimento antes de enviar.

**Aceite:** Pagamento, acesso, opt-out, humano ativo e canal são conferidos no backend no instante da entrega; dado desatualizado no PostHog não decide sozinho.
**Verificação:** C023-02.

### R023-03
Preservar notificações transacionais existentes.

**Aceite:** Confirmação/cobrança/estorno não migram sem motivo nem são enviados duas vezes por PostHog + n8n + app.
**Verificação:** C023-03.

### R023-04
Suprimir spam e reclamações.

**Aceite:** No máximo uma mensagem por gatilho e teto global proposto de uma mensagem de relacionamento por sete dias; opt-out impede novos envios dessa categoria.
**Verificação:** C023-04.

### R023-05
Configurar antes de ativar.

**Aceite:** Fluxos estão testados em dry-run, modelos/domínio/canais validados e desligados até autorização específica de campanha/produção.
**Verificação:** C023-05.

## Limites
Não reconstruir app/billing, não implantar sem autorização, não criar outro CRM/BI, não ampliar poderes do agente. Preservar a aparência aprovada. Escopo não resolvido é registrado como bloqueio da tarefa dependente; não inventar endpoints, credenciais, materiais ou resultado de testes.

## Definição de conclusão
Todos os requisitos desta spec possuem evidência de implementação e teste; artefatos estão coerentes; nenhuma restrição de segurança/comercial foi afrouxada silenciosamente. Checklist de requisitos aprovada não é sinônimo de implementação concluída.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
