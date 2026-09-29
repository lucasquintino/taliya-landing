# Preparação das tarefas para implementação

Base: landing `b09c4d39d0151822ab1a43f95edd68b9d4730df2`, em `main`, com diff local da fundação preservado. Preparado em 2026-09-28 e corrigido em 2026-09-29. **Somente 013 ativa.** A preparação atual contém 87 tarefas, 68 requisitos e 68 casos; os números originais de 81/65 permanecem apenas no snapshot de planejamento. Preparação não é implementação, homologação ou autorização de publicação.

O plano de produto está definido. O usuário corrigiu a premissa de pagamento: não existe billing/Asaas e ele será implementado. A 013 fixa o contrato-alvo; a 015 construirá oferta, checkout, webhooks e projeção de acesso sobre o app/Auth existentes. Ver `DECISAO_BILLING_2026-09-29.md`. Contratos externos e ambiente abaixo ainda precisam de confirmação para ativação e testes. Não existe autorização genérica para produção ou recursos pagos.

## Por onde executar

1. **T013-02/T013-07 foram concluídas localmente**: correção, valores documentados e contrato-alvo Asaas constam no [handoff de integração](contracts/integration-handoff.md). A próxima tarefa é T013-08/T013-01, confirmar a implantação do Internal; T013-09 homologa somente o ambiente autorizado da fundação. T013-06 fecha G0 depois dessas evidências. O billing funcional é entrega da 015.
2. Concluir a 013 antes de ativar a 014. Na execução sequencial, seguir 014 → 015 → 016 → 017 → 018 → 019 → 020 → 021 → 022 → 023 → 024 → 025. As dependências mínimas do plano foram preservadas; a ordem numérica é uma ordem válida de trabalho, sem agentes paralelos.
3. Ao ativar cada spec, revalidar seus arquivos contra o SHA/diff atual, ler `execution.md` e resolver os contratos pendentes indicados. Preparar esclarecimentos, modelo de dados e teste específico antes do código. Não repetir auditoria geral.
4. Implementar por tarefa, executar os testes aplicáveis e registrar resultados em `verification.md`. Revisar/convergir; atualizar checkboxes, JSON, matriz e status juntos. Só avançar com o aceite da spec anterior aplicável comprovado.

| Spec | Recorte | Dependências mínimas |
|---|---|---|
| 013 | [Fundação e contratos](../../specs/013-fundacao-e-contratos/execution.md) | — |
| 014 | [Identidade e segurança](../../specs/014-identidade-dados-e-seguranca/execution.md) | 013 |
| 015 | [Produto, oferta, billing e catálogo](../../specs/015-produto-oferta-e-catalogo/execution.md) | 013, 014 |
| 016 | [Runtime Agents API](../../specs/016-runtime-agents-api-luna/execution.md) | 014, 015 |
| 017 | [Ferramentas e ciclo comercial](../../specs/017-ferramentas-e-ciclo-comercial/execution.md) | 014, 015, 016 |
| 018 | [Landing e jornada](../../specs/018-landing-widget-e-jornada/execution.md) | 015, 017 |
| 019 | [Mídia](../../specs/019-midia-e-demonstracoes/execution.md) | 015 |
| 020 | [Internal](../../specs/020-internal-minimo/execution.md) | 014, 017 |
| 021 | [Eventos e PostHog](../../specs/021-eventos-e-posthog/execution.md) | 017–020 |
| 022 | [Painéis, métricas e custos](../../specs/022-paineis-metricas-e-custos/execution.md) | 021 |
| 023 | [Relacionamento](../../specs/023-automacoes-de-relacionamento/execution.md) | 017, 020–022 |
| 024 | [Homologação](../../specs/024-qualidade-e-homologacao/execution.md) | 018–023 |
| 025 | [Migração e publicação](../../specs/025-migracao-release-e-operacao/execution.md) | 024 |

Cada recorte contém fontes existentes verificadas, arquivos propostos, interfaces, dados/migrações, falhas, dependências por tarefa, teste esperado e evidência exigida. A 015 foi expandida com T015-07–12 para construir billing; as novas rotas/migrations são propostas, não instaladas. `planning/execution.json` é o índice verificável dessa preparação; não substitui `planning/tasks.json` como estado de execução. Hashes registram a inspeção, não impedem mudanças legítimas posteriores.

## Pendências que não podem ser preenchidas por suposição

| ID | O que falta | Trabalho afetado |
|---|---|---|
| B013-01 | Conta Asaas sandbox, elegibilidade Pix Automático, credencial segura, oferta vigente e URLs de ambiente | Implementação/homologação da 015 e publicação de oferta/checkout; trabalho local da 013 prossegue |
| B013-02 | Deployment/SHA ativo do Internal e mecanismo real de staff | Fechamento da fundação, auth e corte das rotas locais/remotas |
| B013-03 | Ambiente/contas sintéticas, permissões por operação, canais e orçamento autorizado | Homologação integrada, Luna/max real, PostHog e release |
| B013-04 | Mídias reais aprovadas, direitos, classificação e responsável editorial | Publicação do catálogo e aceite da 019 |

Nomes humanos dos responsáveis, políticas de retenção/exclusão, frescor da oferta e limites operacionais devem ser confirmados no serviço dono antes das respectivas implementações. As metas de latência, amostragem, orçamento e rollout do pacote continuam **propostas**, sem redução silenciosa ou interpretação como gasto aprovado. Escolha de SDK/payload Agents API e configuração PostHog depende de documentação oficial vigente e conta real; nenhum endpoint novo foi inventado.

## Comandos existentes e seguros para esta preparação

Executar da raiz da landing:

```sh
bash .specify/scripts/bash/check-prerequisites.sh --json --require-spec --require-tasks --include-tasks
python3 docs/taliya-sdd/scripts/validate_plan.py
python3 docs/taliya-sdd/scripts/validate_progress.py
python3 docs/taliya-sdd/scripts/check_readiness.py
python3 docs/taliya-sdd/scripts/check_readiness.py --spec 014 --require-unblocked
python3 -m unittest discover -s docs/taliya-sdd/tests -v
git diff --check
```

`validate_plan` valida somente o ZIP inicial. `validate_progress` valida a coerência do progresso. `check_readiness` valida a preparação e lista os impedimentos; sem `--require-unblocked`, exit 0 significa **documentos coerentes**, não tarefas liberadas. Com a opção, exit 2 significa pendência legítima de execução; exit 1 indica erro estrutural. Nenhum desses comandos chama serviços, altera pointer ou executa tarefas automaticamente.

O Spec Kit 1.0.7 e seus scripts Bash estão disponíveis. Skills de chat não são comandos de shell; não alegar execução de `/speckit.*` por escrever documentos. O pointer continua em 013 durante a preparação de 014–025. Hooks de commit são opcionais e foram dispensados, preservando o diff local; não estão globalmente desativados no YAML.

## Verificações de implementação previstas

- `npm run lint` e `npm run build` existem. Executar no recorte/ambiente local apropriado quando houver mudança de aplicação; build pode carregar configurações e não deve apontar a serviços de produção. Ainda falta adicionar comando explícito de typecheck na 024, usando o compilador local, sem instalar dependência via `npx` implicitamente.
- Os testes propostos em `scripts/tests/sdd/` e `test_sdd_managed_runtime.py` **ainda não existem**. Cada tarefa cria o teste pertinente e registra seu comando real. Não há uma suíte v2 completa executável nesta entrega de preparação.
- `test:agent-runtime:production-gate` existe, mas usa suíte legada com exclusões antigas. Não equivale à homologação nova. Inspecionar/classificar cada teste antes do reuso. Não executar todos os `eval:*`: parte chama provedores ou pressupõe Pilates.
- Testes de DB usam banco descartável e credenciais isoladas; rede desabilitada nos testes offline. Integração sandbox, modelo real e operação de canais têm grupo e autorização próprios. Mocks nunca fecham casos que exigem o serviço real.
- G0–G6, 68 casos vigentes (65 originais mais 3 de billing), testes negativos, restauração e evidência operacional mantêm os critérios do plano. Catálogo vazio e ausência de faturamento real não podem virar aceite fictício.

## Responsabilidade pelos arquivos e continuidade

Um executor por vez cuida de `storage/postgres.ts`, `route.ts`, contratos compartilhados, `planning/*.json`, status, matriz e pointer. Alterações em outro repositório exigem confirmar checkout de trabalho e instruções daquele repo; clones em `/tmp` são referências de leitura. Reutilizar Auth e implementar billing conforme a 015.

O checkpoint único permanece em [conversation-handoff-2026-05-14.md](../conversation-handoff-2026-05-14.md). Este arquivo é o índice de execução, não um segundo histórico de continuidade. Não houve commit, push, migração, ativação de cobrança ou deploy por esta preparação.
