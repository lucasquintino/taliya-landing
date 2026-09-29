# 014 — Identidade, dados e segurança de base

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Backend + segurança.
**Dependências:** 013.

## Resultado
Garantir que cada escrita pertença ao contato/negócio correto e que a operação administrativa seja autenticada.

## Requisitos verificáveis
### R014-01
Usar identidade autenticada e papéis de staff; remover token compartilhado de URL/frontend.

**Aceite:** Auth existente valida issuer/audience/expiração e papéis; actor_id vem da sessão, nunca de x-operator-id arbitrário.
**Verificação:** C014-01.

### R014-02
Separar sessão anônima, contato, pessoa autenticada, negócio e assinatura.

**Aceite:** E-mail/telefone declarado não abre conta nem permite merge global; vínculo exige prova apropriada e auditoria.
**Verificação:** C014-02.

### R014-03
Derivar autorizações no servidor e validar cada parâmetro das ferramentas.

**Aceite:** Requests cruzados entre usuários/negócios, replay de tokens e histórico fabricado não alteram registros.
**Verificação:** C014-03.

### R014-04
Evoluir dados com migrações versionadas, privilégios mínimos e persistência obrigatória em produção.

**Aceite:** Sem DDL em request de produção, fallback de memória comercial ou TLS com verificação desativada no perfil publicado.
**Verificação:** C014-04.

### R014-05
Definir minimização, consentimentos e exclusão correlacionada.

**Aceite:** Contato para suporte não vira opt-in; política de retenção e exclusão cobre app, chat, analytics e sessões remotas com exceções justificadas.
**Verificação:** C014-05.

## Limites
Não reconstruir app/billing, não implantar sem autorização, não criar outro CRM/BI, não ampliar poderes do agente. Preservar a aparência aprovada. Escopo não resolvido é registrado como bloqueio da tarefa dependente; não inventar endpoints, credenciais, materiais ou resultado de testes.

## Definição de conclusão
Todos os requisitos desta spec possuem evidência de implementação e teste; artefatos estão coerentes; nenhuma restrição de segurança/comercial foi afrouxada silenciosamente. Checklist de requisitos aprovada não é sinônimo de implementação concluída.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
