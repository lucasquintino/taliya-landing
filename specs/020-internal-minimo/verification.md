# 020 — Verificação e evidências

**Estado:** casos especificados; nenhum caso de aceitação foi executado nesta auditoria.

## C020-01 · R020-01
**Cenário:** Inspecionar rota /internal e /api/internal nos ambientes reais e registrar qual deploy valida identidade e executa cada ação.

**Resultado exigido:** Rewrite e rotas locais estão conciliados com a implantação atual; não existem dois painéis editando estados divergentes.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C020-02 · R020-02
**Cenário:** Operador localiza atendimento e abre ficha vinculada à conta correta, filtra pendências e acessa o atalho analítico sem duplicar cadastro.

**Resultado exigido:** Fila filtra espera/humano/erro e ficha mostra conta/negócio/status oficiais; atalhos abrem PostHog e billing autorizado.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C020-03 · R020-03
**Cenário:** Responder humano em conversa web e no WhatsApp comercial; comparar entrega original, timestamp do último inbound e permissão do provedor.

**Resultado exigido:** Web e WhatsApp possuem prova de entrega ou falha explícita; enviar WhatsApp não substitui silenciosamente resposta ao webchat.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C020-04 · R020-04
**Cenário:** Dois operadores assumem enquanto a IA está concluindo; verificar lock/versão, bloqueio de resposta tardia e retomada apenas autorizada.

**Resultado exigido:** Assumir bloqueia novos turnos/ações/entregas atrasadas; só operador autorizado retoma; recibo de handoff é único.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C020-05 · R020-05
**Cenário:** Tentar modificar cobrança por anotação de oportunidade ganha, escrever como viewer e usar controle legado de diagnóstico; verificar restrições e auditoria.

**Resultado exigido:** mark_won não concede assinatura nem receita; nenhum operador altera custo/status financeiro diretamente; trilha do ator é verificável.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## Regressões adicionais da frente
- Dois operadores tentam assumir: apenas um estado final coerente é aceito.
- Resposta da IA pronta antes do takeover não é enviada após a pausa.
- Humano responde visitante web no webchat, não em outro canal implícito.
- Alteração de ficha não estende indevidamente janela de envio do WhatsApp.
- Marcar oportunidade ganha não cria cliente pago nem altera o billing.

Os IDs de caso são estáveis; o detalhamento técnico cresce com os contratos reais. Mock não comprova chamada externa, análise estática não comprova produção.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
