# 016 — Verificação e evidências

**Estado:** casos especificados; nenhum caso de aceitação foi executado nesta auditoria.

## C016-01 · R016-01
**Cenário:** Executar um turno real em homologação e inspecionar modelo/esforço, ambiente e ferramentas efetivamente usados.

**Resultado exigido:** Smoke test real registra modelo/esforço, formato e versão do cliente; erro de compatibilidade não muda modelo silenciosamente.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C016-02 · R016-02
**Cenário:** Criar duas conversas independentes, editar o agente salvo e migrar uma sessão; verificar isolamento e versões, sem importar instruções antigas.

**Resultado exigido:** Mapeamento conversa-versão-sessão é persistido e protegido; versões antigas recebem migração controlada.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C016-03 · R016-03
**Cenário:** Repetir mensagem/webhook e reiniciar worker antes e depois da gravação de um efeito; verificar ordem por conversa e recuperação sem dupla escrita.

**Resultado exigido:** Fechar navegador ou reiniciar worker não perde operação aceita; locks/lease e dedup impedem concorrência incorreta.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C016-04 · R016-04
**Cenário:** Simular chamada pendente, perda de stream e repetição de callback; recuperar itens persistidos e devolver o mesmo recibo da ferramenta.

**Resultado exigido:** Resultado já salvo é reutilizado; itens e eventos são reconciliados por IDs; não há execução dupla por stream + webhook.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C016-05 · R016-05
**Cenário:** Acionar limite de entrada, abuso, falha de provedor e timeout; verificar entrega pública sanitizada, custo observado e acesso às ações estáticas.

**Resultado exigido:** Limites por contexto/conta/canal e kill switch existem; usuário vê espera honesta e somente resposta validada, sem traces internos.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## Regressões adicionais da frente
- Turno real confirma Luna/max e nenhuma permissão de shell/MCP amplo.
- Request repetido e webhook repetido retornam um único resultado comercial.
- Worker reiniciado após gravação da ferramenta retoma sem nova escrita.
- Sessão salva em versão antiga é migrada sem carregar oferta obsoleta.
- Timeout ou indisponibilidade deixa contratação e atendimento humano acessíveis.

Os IDs de caso são estáveis; o detalhamento técnico cresce com os contratos reais. Mock não comprova chamada externa, análise estática não comprova produção.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
