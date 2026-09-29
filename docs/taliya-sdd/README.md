# Taliya SDD — execução local

Plano original incorporado por diff em 28/09/2026. Specs ativas estão em ../../specs/013-*…025-*;
o ZIP exato em source/ preserva o snapshot de auditoria. MANIFESTO_SHA256.json e
os relatórios iniciais descrevem exclusivamente esse ZIP, não os arquivos em execução.

Fonte de status atual: STATUS.json, planning/, evals/acceptance-cases.json,
05_MATRIZ_DE_COBERTURA.md e ../../specs/013-fundacao-e-contratos/verification.md.
Continuidade única: ../conversation-handoff-2026-05-14.md.

`python3 scripts/validate_plan.py` extrai o snapshot temporariamente, verifica hashes e
executa o validador original. `python3 scripts/validate_progress.py` valida coerência de
execução, sem afirmar runtime ou homologação. Tests usam cópias temporárias isoladas.

Leia EXECUTION_ADDENDUM.md, contracts/current-contracts.md e environments.md.
Uma única spec ativa: 013. 014–025 incorporadas como propostas, não iniciadas.
Correção de 29/09: billing/Asaas ainda não existe; ver
`DECISAO_BILLING_2026-09-29.md`. O estado atual contém 87 tarefas e 68 casos,
dos quais nenhum resultado de billing em sandbox foi alegado.
