# 016 — Runtime Agents API com Luna Max

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Backend/IA.
**Dependências:** 014, 015.

## Resultado
Trocar o núcleo comercial antigo por execução gerenciada com um agente único e continuidade confiável.

## Requisitos verificáveis
### R016-01
Executar gpt-6-luna com esforço max, ambiente none e subagentes desativados.

**Aceite:** Smoke test real registra modelo/esforço, formato e versão do cliente; erro de compatibilidade não muda modelo silenciosamente.
**Verificação:** C016-01.

### R016-02
Usar uma configuração versionada e sessões remotas isoladas.

**Aceite:** Mapeamento conversa-versão-sessão é persistido e protegido; versões antigas recebem migração controlada.
**Verificação:** C016-02.

### R016-03
Processar turnos de modo durável, ordenado e recuperável.

**Aceite:** Fechar navegador ou reiniciar worker não perde operação aceita; locks/lease e dedup impedem concorrência incorreta.
**Verificação:** C016-03.

### R016-04
Executar required_actions pelo backend e reconciliar desconexões.

**Aceite:** Resultado já salvo é reutilizado; itens e eventos são reconciliados por IDs; não há execução dupla por stream + webhook.
**Verificação:** C016-04.

### R016-05
Controlar timeout, abuso, custo e resposta pública.

**Aceite:** Limites por contexto/conta/canal e kill switch existem; usuário vê espera honesta e somente resposta validada, sem traces internos.
**Verificação:** C016-05.

## Limites
Não reconstruir app/billing, não implantar sem autorização, não criar outro CRM/BI, não ampliar poderes do agente. Preservar a aparência aprovada. Escopo não resolvido é registrado como bloqueio da tarefa dependente; não inventar endpoints, credenciais, materiais ou resultado de testes.

## Definição de conclusão
Todos os requisitos desta spec possuem evidência de implementação e teste; artefatos estão coerentes; nenhuma restrição de segurança/comercial foi afrouxada silenciosamente. Checklist de requisitos aprovada não é sinônimo de implementação concluída.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
