# Rastreabilidade — Fundação

| Requisito/critério | Fonte | Artefato/evidência |
|---|---|---|
| FR-001 / SC-001: cópia do commit correto | URL fornecida pelo usuário + Git | `baseline.md`; `verification.md` |
| FR-002: origem intocada, cópia sem remote e sem publicação | Pedido do usuário + `00_COMECE_AQUI.txt` | `baseline.md`; `verification.md` |
| FR-003: preservar componentes e interações nas etapas de copy | Correção direta do usuário | Constitution; `shared-contracts.md`; `source-map.md` |
| FR-004: preservar rotas legadas até decisão | `route_plan.json` SEO v1.1 | `decisions.md`; spec 002 futura |
| FR-005: fonte canônica de textos | README e schema do pacote landing | Constitution; plano; spec por seção |
| FR-006: Mural como única nova seção | Pedido do usuário + pacote landing | Constitution; spec S06 futura |
| FR-007: faixa S02/fluxos S08 fora do limite atual | Pedido mais recente contra composição do pacote | `plan.md`; `decisions.md` |
| FR-008: 18 recortes com arquitetura final | Prompt mestre + solicitação posterior | `specs/taliya-migration/README.md` |
| FR-009: estados e evidências separados | Prompt mestre SDD | `verification.md`; índice |
| FR-010: refatoração após integração | Solicitação posterior do usuário | Constituição; etapa 018 do plano |
| FR-011: mudanças apenas na cópia | Prompt mestre e pedido atual | branch local, ausência de remote; `baseline.md` |

## Evidências ainda pendentes

- Baseline desktop e mobile de `/pilates`.
- Comportamento e compatibilidade da fonte canônica nos slots reais.
- Todos os testes/runtime e validações de SEO da landing migrada.
- Todos os checks que dependem de um host e decisão de legado.
