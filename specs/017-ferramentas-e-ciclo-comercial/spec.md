# 017 — Cinco ferramentas e ciclo de leads/clientes

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Backend comercial + app/billing.
**Dependências:** 014, 015, 016.

## Resultado
Conectar conversa, cadastro e assinatura com uma autoridade por operação.

## Requisitos verificáveis
### R017-01
Implementar as cinco ferramentas contratadas e nada de SQL/mark_paid genérico.

**Aceite:** consultar_taliya, buscar_material, atualizar_contato, preparar_proximo_passo e solicitar_atendimento_humano passam em validação e teste real.
**Verificação:** C017-01.

### R017-02
Criar/atualizar contato apenas com dados/evidências autorizadas.

**Aceite:** Mensagens originais persistidas sustentam patches; dados de login/consentimento financeiro não são editados pelo modelo.
**Verificação:** C017-02.

### R017-03
Criar/vincular cliente independentemente da existência de chat.

**Aceite:** Cadastro e primeira compra no fluxo pronto atualizam projeção comercial; renovação não gera novo cliente.
**Verificação:** C017-03.

### R017-04
Separar aquisição, billing, acesso e atendimento.

**Aceite:** Cancelamento de renovação com período pago preserva acesso; estorno solicitado não é devolução concluída; status é derivado de autoridade real.
**Verificação:** C017-04.

### R017-05
Eliminar dupla gravação e preservar histórico de modo seguro.

**Aceite:** Ferramenta e pós-processamento antigo não gravam o mesmo lead; eventos fora de ordem são reconciliados; legado fica identificado.
**Verificação:** C017-05.

## Limites
Não reconstruir app/billing, não implantar sem autorização, não criar outro CRM/BI, não ampliar poderes do agente. Preservar a aparência aprovada. Escopo não resolvido é registrado como bloqueio da tarefa dependente; não inventar endpoints, credenciais, materiais ou resultado de testes.

## Definição de conclusão
Todos os requisitos desta spec possuem evidência de implementação e teste; artefatos estão coerentes; nenhuma restrição de segurança/comercial foi afrouxada silenciosamente. Checklist de requisitos aprovada não é sinônimo de implementação concluída.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
