# 024 — QA integrada, segurança, performance e evals

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** QA + backend/frontend + produto.
**Dependências:** 018, 019, 020, 021, 022, 023.

## Resultado
Provar a jornada completa com dados controlados e falhas deliberadas antes da liberação.

## Requisitos verificáveis
### R024-01
Executar suíte automatizada de unidade/contrato/integração/E2E.

**Aceite:** Build, lint, tipos e testes do código tocado passam no CI; testes antigos têm destino explícito: preservar/adaptar/arquivar.
**Verificação:** C024-01.

### R024-02
Avaliar Luna Max com conversas reais de homologação e critérios reproduzíveis.

**Aceite:** Os casos vigentes do plano (68 após a correção de billing) e cenários reutilizáveis anteriores têm resultado; casos críticos repetidos não podem falhar; amostra de linguagem recebe revisão humana.
**Verificação:** C024-02.

### R024-03
Testar todas as combinações da assinatura implementada na 015 como regressão de integração.

**Aceite:** Mensal/anual × cartão/Pix Automático, retorno, falha, cancelamento e reembolso têm evidência sandbox; produção depende de gate próprio.
**Verificação:** C024-03.

### R024-04
Validar falhas, acessibilidade, desempenho e segurança.

**Aceite:** IDOR, injeção, URL arbitrária, repetição, takeover, desconexão, fila, cookies e restauração possuem evidências.
**Verificação:** C024-04.

### R024-05
Concluir critérios sem rebaixar exigência silenciosamente.

**Aceite:** Nenhum P0/P1 de lançamento aberto; metas não atingidas geram correção ou exceção explícita, não marcação verde por criar documentação.
**Verificação:** C024-05.

## Limites
Reutilizar app/Auth e billing construído na 015; não implantar sem autorização, não criar outro CRM/BI, não ampliar poderes do agente. Preservar a aparência aprovada. Escopo não resolvido é registrado como bloqueio da tarefa dependente; não inventar endpoints, credenciais, materiais ou resultado de testes.

## Definição de conclusão
Todos os requisitos desta spec possuem evidência de implementação e teste; artefatos estão coerentes; nenhuma restrição de segurança/comercial foi afrouxada silenciosamente. Checklist de requisitos aprovada não é sinônimo de implementação concluída.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
