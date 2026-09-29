# 013 — Fundação, governança e contratos da Taliya

**Status:** em execução local; aceite integrado parcial, bloqueios externos registrados.
**Responsável:** Liderança técnica + responsável pelo produto.
**Dependências:** nenhuma.

## Resultado
Registrar o estado real, retirar conflitos de autoridade e fixar as interfaces existentes e a construir. O app e sua autenticação são reutilizados; billing Asaas ainda não existe, conforme correção do usuário em 2026-09-29.

## Requisitos verificáveis
### R013-01
Registrar commit, repositórios e donos dos contratos atuais de app, billing, landing, Internal e agente.

**Aceite:** O mapa contém endpoints reais, autenticação, IDs, estados, payloads sanitizados e responsáveis; nenhuma rota inventada é aprovada.
**Verificação:** C013-01.

### R013-02
Substituir regras de copy-only apenas no escopo desta nova entrega, preservando identidade visual e históricos.

**Aceite:** AGENTS/constituição/pointer não direcionam novas tarefas ao projeto Pilates e não autorizam redesign ou deploy automático.
**Verificação:** C013-02.

### R013-03
Preservar app e autenticação existentes; definir a fonte e os contratos do billing Asaas que será construído.

**Aceite:** O mapa distingue app/Auth observados de pagamento ainda inexistente, identifica dono dos dados e contrato-alvo para oferta, checkout, webhooks e acesso, e direciona a implementação à 015. Nenhum endpoint não implementado é apresentado como publicado.
**Verificação:** C013-03.

### R013-04
Fixar uma versão operacional do Spec Kit e um método de scripts compatível com a máquina.

**Aceite:** A integração Codex e as invocações disponíveis são verificadas; nenhum --force apaga customizações e o ponteiro aponta à spec ativa.
**Verificação:** C013-04.

### R013-05
Registrar fontes, baselines e disponibilidade dos serviços.

**Aceite:** Há inventário de materiais disponíveis, ambientes, credenciais necessárias sem valores, baseline visual e gates por dependência.
**Verificação:** C013-05.

## Limites
Não reconstruir app/Auth, não implantar sem autorização, não criar outro CRM/BI, não ampliar poderes do agente. Construir billing dentro do programa sem ativar cobrança sem conta, condições e homologação reais. Preservar a aparência aprovada. Escopo não resolvido é registrado como bloqueio da tarefa dependente; não inventar endpoints publicados, credenciais, materiais ou resultado de testes.

## Definição de conclusão
Todos os requisitos desta spec possuem evidência de implementação e teste; artefatos estão coerentes; nenhuma restrição de segurança/comercial foi afrouxada silenciosamente. Checklist de requisitos aprovada não é sinônimo de implementação concluída.

## Histórias e esclarecimentos desta execução
- US1 (P1): mantenedor encontra fonte/SHA e contrato verdadeiro de cada serviço sem reconstruir produto. C013-01/C013-03.
- US2 (P1): implementador retoma a spec correta com regras atuais e scripts executáveis, preservando histórico. C013-02/C013-04.
- US3 (P1): equipe distingue baseline real, material sem aprovação e integração bloqueada. C013-05.
- Pedidos sem fonte de oferta: registrar bloqueio, sem preço ou endpoint substituto.
- Branch do hook `015-fundacao-e-contratos` não renumera a spec 013: resolução explícita por feature.json, conforme skill instalada.
- Correção do usuário em 2026-09-29: não existe pagamento/Asaas; o serviço deverá ser implementado. A premissa anterior de assinatura pronta não governa mais este programa. Ver `../../docs/taliya-sdd/DECISAO_BILLING_2026-09-29.md`.
- Critério de sucesso: todos os cinco casos aprovados com evidência e contratos externos resolvidos. Encerrar o recorte local não encerra a spec.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
