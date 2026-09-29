# 017 — Verificação e evidências

**Estado:** casos especificados; nenhum caso de aceitação foi executado nesta auditoria.

## C017-01 · R017-01
**Cenário:** Executar cada uma das cinco funções em contexto autorizado e tentar operações mark_paid, SQL e compra implícita não expostas.

**Resultado exigido:** consultar_taliya, buscar_material, atualizar_contato, preparar_proximo_passo e solicitar_atendimento_humano passam em validação e teste real.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C017-02 · R017-02
**Cenário:** Pedir alteração legítima de nome e atividade, depois alteração de login ou contato de outra conta; conferir evidência original e patch aplicado.

**Resultado exigido:** Mensagens originais persistidas sustentam patches; dados de login/consentimento financeiro não são editados pelo modelo.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C017-03 · R017-03
**Cenário:** Contratar sem abrir o chat, depois renovar e retornar pelo agente autenticado; conferir um vínculo comercial por entidade real.

**Resultado exigido:** Cadastro e primeira compra no fluxo pronto atualizam projeção comercial; renovação não gera novo cliente.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C017-04 · R017-04
**Cenário:** Simular cancelamento de renovação com período pago, pedido de reembolso pendente e mensagem já paguei; conferir estados independentes.

**Resultado exigido:** Cancelamento de renovação com período pago preserva acesso; estorno solicitado não é devolução concluída; status é derivado de autoridade real.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C017-05 · R017-05
**Cenário:** Repetir escrita da ferramenta com callback antigo, entregar eventos fora de ordem e migrar um contato legado; conferir dedup, histórico e reconciliação.

**Resultado exigido:** Ferramenta e pós-processamento antigo não gravam o mesmo lead; eventos fora de ordem são reconciliados; legado fica identificado.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## Regressões adicionais da frente
- Pessoa compra sem chat e aparece uma vez como cliente do negócio certo.
- Ferramenta e callback antigo não criam dois leads.
- Já paguei escrito no chat não muda assinatura nem receita.
- Evento atrasado não reativa acesso estornado nem duplica renovação.
- Cliente ativo vai ao app/gestão, não a uma segunda compra.

Os IDs de caso são estáveis; o detalhamento técnico cresce com os contratos reais. Mock não comprova chamada externa, análise estática não comprova produção.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
