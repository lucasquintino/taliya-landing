# 020 — Taliya Internal mínimo e operação humana

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Frontend/backend + operação.
**Dependências:** 014, 017.

## Resultado
Entregar duas áreas operacionais, sem duplicar CRM analítico ou financeiro.

## Requisitos verificáveis
### R020-01
Definir uma implantação autoritativa do Internal.

**Aceite:** Rewrite e rotas locais estão conciliados com a implantação atual; não existem dois painéis editando estados divergentes.
**Verificação:** C020-01.

### R020-02
Entregar fila de atendimento e ficha de contato/cliente.

**Aceite:** Fila filtra espera/humano/erro e ficha mostra conta/negócio/status oficiais; atalhos abrem PostHog e billing autorizado.
**Verificação:** C020-02.

### R020-03
Permitir resposta humana no canal original suportado.

**Aceite:** Web e WhatsApp possuem prova de entrega ou falha explícita; enviar WhatsApp não substitui silenciosamente resposta ao webchat.
**Verificação:** C020-03.

### R020-04
Aplicar pausa/retomada atômicas e auditáveis.

**Aceite:** Assumir bloqueia novos turnos/ações/entregas atrasadas; só operador autorizado retoma; recibo de handoff é único.
**Verificação:** C020-04.

### R020-05
Restringir ações administrativas e remover controles antigos inadequados.

**Aceite:** mark_won não concede assinatura nem receita; nenhum operador altera custo/status financeiro diretamente; trilha do ator é verificável.
**Verificação:** C020-05.

## Limites
Não reconstruir app/billing, não implantar sem autorização, não criar outro CRM/BI, não ampliar poderes do agente. Preservar a aparência aprovada. Escopo não resolvido é registrado como bloqueio da tarefa dependente; não inventar endpoints, credenciais, materiais ou resultado de testes.

## Definição de conclusão
Todos os requisitos desta spec possuem evidência de implementação e teste; artefatos estão coerentes; nenhuma restrição de segurança/comercial foi afrouxada silenciosamente. Checklist de requisitos aprovada não é sinônimo de implementação concluída.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
