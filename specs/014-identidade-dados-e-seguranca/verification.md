# 014 — Verificação e evidências

**Estado:** casos especificados; nenhum caso de aceitação foi executado nesta auditoria.

## C014-01 · R014-01
**Cenário:** Tentar abrir Internal por token na query, forjar x-operator-id, usar conta comum e usar papel viewer em uma mutação; repetir com operador autorizado.

**Resultado exigido:** Auth existente valida issuer/audience/expiração e papéis; actor_id vem da sessão, nunca de x-operator-id arbitrário.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C014-02 · R014-02
**Cenário:** Fornecer o mesmo e-mail em duas sessões anônimas e autenticar pessoas distintas; verificar que conta, contato, negócio e assinatura não são mesclados por declaração.

**Resultado exigido:** E-mail/telefone declarado não abre conta nem permite merge global; vínculo exige prova apropriada e auditoria.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C014-03 · R014-03
**Cenário:** Enviar IDs de outra conversa/negócio, histórico fabricado, parâmetro fora da allowlist e sessão expirada para cada operação mutante.

**Resultado exigido:** Requests cruzados entre usuários/negócios, replay de tokens e histórico fabricado não alteram registros.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C014-04 · R014-04
**Cenário:** Iniciar produção sem banco e revisar migração/restore, DDL fora do request e validação TLS em ambiente configurado.

**Resultado exigido:** Sem DDL em request de produção, fallback de memória comercial ou TLS com verificação desativada no perfil publicado.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C014-05 · R014-05
**Cenário:** Revogar preferência de coleta, sair da conta e solicitar exclusão em cenário controlado; verificar logs, analytics e vinculações retidas/descartadas conforme política.

**Resultado exigido:** Contato para suporte não vira opt-in; política de retenção e exclusão cobre app, chat, analytics e sessões remotas com exceções justificadas.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## Regressões adicionais da frente
- Mesmo e-mail declarado por dois anônimos não mescla identidades verificadas.
- Staff viewer não escreve e usuário comum não lê leads administrativos.
- Token em query string e x-operator-id forjado não concedem privilégios.
- Produção sem banco não confirma falso registro e não migra schema durante request.
- Logout, conta compartilhada no navegador e exclusão não reutilizam identidade privada.

Os IDs de caso são estáveis; o detalhamento técnico cresce com os contratos reais. Mock não comprova chamada externa, análise estática não comprova produção.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
