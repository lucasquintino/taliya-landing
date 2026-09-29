# 025 — Verificação e evidências

**Estado:** casos especificados; nenhum caso de aceitação foi executado nesta auditoria.

## C025-01 · R025-01
**Cenário:** Ensaiar migração de contatos/sessões e restore de backup; conferir IDs, permissões, eventos e reconciliar estado financeiro sem duplicação.

**Resultado exigido:** Registros legados permanecem marcados; não há merge automático por e-mail; backup/restore e contagens são verificados.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C025-02 · R025-02
**Cenário:** Revisar autorização e liberar coortes internas/limitadas; tentar avanço com gate pendente e conferir bloqueio.

**Resultado exigido:** Interno → 5% → 25% → 100% conforme evidência; não confundir percentual de tráfego com conclusão da entrega.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C025-03 · R025-03
**Cenário:** Desligar geração e fazer rollback de configuração; confirmar ausência de agente/promessas de Pilates e manutenção do acesso à contratação.

**Resultado exigido:** Kill switch desliga geração e preserva assinar/entrar/ajuda/handoff; schemas compatíveis e eventos continuam íntegros.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C025-04 · R025-04
**Cenário:** Entregar runbook a operador e simular incidentes de OpenAI, PostHog, banco e canal; verificar alertas, permissões e responsáveis.

**Resultado exigido:** Há dono de fila, mídia, fonte comercial, financeiro e analytics; problemas de custo, privacidade e entrega têm resposta definida.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C025-05 · R025-05
**Cenário:** Percorrer matriz final requisito → código/config → teste → evidência → operação; verificar que bloqueador crítico ou conteúdo inexistente impede declaração de 100%.

**Resultado exigido:** Todos os gates obrigatórios aprovados, estabilização observada, documentação alinhada e nenhuma pendência escondida de segurança/contratação/dados.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## Regressões adicionais da frente
- Rollback não retorna promessa/fluxo de Pilates e contratação segue disponível.
- Backup restaurado mantém vínculos, permissões e eventos sem duplicação.
- Deploy não publica segredos, ambiente de teste ou material não aprovado.
- Operador resolve atendimento pendente usando só runbook e permissões próprias.
- Declaração de 100% referencia evidências reais; reprovação crítica bloqueia avanço.

Os IDs de caso são estáveis; o detalhamento técnico cresce com os contratos reais. Mock não comprova chamada externa, análise estática não comprova produção.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
