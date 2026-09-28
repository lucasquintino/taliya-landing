# Matriz de Conformidade - Contratos de Comportamento -> Arquitetura - 2026-06-11

Cada regra dos contratos binding mapeada para seu dono na arquitetura
action-first (design-lock-v2) e seu status. Esta matriz é o checklist da
Fase 3: nenhuma task fecha deixando uma linha sem evidência.

Status: **Provado** = já demonstrado no spike pago | **Portar** = existe
implementado/testado na Spec 011, é portar | **Novo** = construir.

## A. behavior-contract.md (010)

| Regra | Dono na arquitetura | Status / Task |
| --- | --- | --- |
| LLM-first; zero regex/keyword comercial | Agentes SDK + auditoria estática | Provado / T012-040 |
| Turno normal = 1 operação (+1 repair); custo nunca cortado evitando o LLM | Budget meter + trace de usage | Provado / T012-036 |
| Decisão estruturada auditável (estados, intents, policy_checks) | `ConductorActionDecision` + trace | Novo / T012-030A, 034 |
| Voz: frases banidas, sem hype, sem saudação repetida, sem parroting | Voice validators + juiz | Portar+Novo / T012-032, 039 |
| Cold greeting: sem diagnóstico/waitlist/nome/telefone/planos | Validator + fixtures canônicas | Portar / T012-032, 038 |
| Política de nome (perfil confiável/não; pergunta na entrada do diagnóstico) | Situation builder + templates `*_named` + validator | Novo / T012-032B |
| Widget opening: exatamente 3 mensagens definidas | Compiler (determinismo operacional permitido) | Novo / T012-030C |
| Aberturas por fonte (Instagram/site/CTA diagnóstico) | Ação do LLM + templates de entry | Provado / T012-038 |
| Pergunta direta respondida primeiro, COM a resposta (adequação) | Obrigações derivadas + adequacy validator (`price_question_missing_price_answer`) | Portar / T012-032 |
| Objeção de preço: validar preocupação, próximo passo por estado | Ação LLM + contexto salvo + juiz | Novo / T012-032B, 038B |
| Plan-fit: recomendação cautelosa ou diagnóstico | Menu de ações | Provado / T012-038 |
| Demo: responder primeiro, link oficial por canal, estado persistido | Compiler injeta link oficial + demo state | Provado parcial / T012-030C |
| Waitlist só com intenção clara de contratar | Validator + do-not-do fixtures | Portar / T012-032, 038 |
| Handoff pausa IA em estado até resume explícito | Turn gate | Provado / T012-036 |
| Conversa não-linear (multi-pergunta, correção, contradição, irritação) | LLM + fixtures novas | Novo / T012-038B |
| Lista completa de validators (linhas 424-451) | Port do conjunto 011 | Portar / T012-032 |
| Gate: juiz >= 4.2/5, nenhum P1 < 4.0, sem mock como evidência final | Judge harness | Novo / T012-039 |
| Custo por lead: alvo $0.05, revisão $0.10, teto $0.20-0.30 | Per-conversation cost cap | Novo / T012-036 |

## B. diagnostic-contract.md (010)

| Regra | Dono | Status / Task |
| --- | --- | --- |
| Ledger com 6 chaves, status, evidência, confiança | Schema + compiler merge | Provado parcial / T012-030C |
| Ordem oficial das 6 perguntas (wording bate com os templates) | Situation builder (pending key) + sequence guardrail | Provado / T012-030B |
| No-repeat; pré-respondidas viram `inferred_from_prior_message` | Ledger + validator | Provado / T012-030B |
| Orientação antes da 1ª pergunta; feedback grounded entre perguntas (não parroting, não filler) | Variável de composição obrigatória + anti-parrot validator + juiz | Novo / T012-032 |
| Entrega só com 6/6; sem fake certainty; parcial honesto se recusar | Compiler + validator | Provado parcial / T012-030C |
| Entrega staged completa: hold -> contexto -> CRM -> passo -> agentes 1 a 1 -> plano -> demo | **Compiler deriva (nunca o modelo)** | Novo / T012-030C |
| Linha de plano e linha de demo com significado fixo; formatos antigos rejeitados | Templates + validator | Portar / T012-032 |
| Demo bridge conforme `demo_status` persistido | Compiler lê estado | Novo / T012-030C |
| Pergunta de produto durante diagnóstico: responde e retoma | Ação `answer_direct_question_then_continue_diagnostic` | Provado parcial / T012-038B |

## C. conversation-state-contract.md (010)

| Regra | Dono | Status / Task |
| --- | --- | --- |
| 25 estados canônicos + transições permitidas | Compiler (execução de estado, não interpretação) | Novo / T012-030C |
| previous/current/next + razão + evidência em todo turno | Trace | Novo / T012-034 |
| Transições high-impact exigem validator antes de persistir/entregar | Validator gate | Portar / T012-032 |
| Pós-diagnóstico: contexto compacto salvo, nunca reinicia diagnóstico | Situation builder injeta contexto | Novo / T012-032B |

## D. message-template-contract.md (010)

| Regra | Dono | Status / Task |
| --- | --- | --- |
| Catálogo (~63 templates) com shape completo (estados, canal, variáveis, exemplos) | Registry (existe) + validator de allowed-state | Portar / T012-032 |
| 1-3 mensagens curtas; staged é a única exceção; sem text wall | Renderer/chunking | Portar / T012-033 |
| Botões só no widget; WhatsApp usa links oficiais; nunca pedir telefone | Renderer por canal + validator | Portar / T012-033 |
| Variáveis adaptativas nunca inventam fatos/datas/links | Grounding validators | Provado / T012-032 |
| Fallback unmapped curto, sem side effect, máx. 1 clarificação | Template + validator | Portar / T012-032 |

## E. product-followup-delta-contract.md (010)

| Regra | Dono | Status / Task |
| --- | --- | --- |
| 9 chaves novas de product knowledge (how_it_works, routine_areas, whatsapp_scope, integration_scope, comparison_*, security_and_data, availability_and_onboarding, out_of_profile) | Fonte oficial | Novo / T012-032B |
| 5 templates novos do delta | Registry | Novo / T012-032B |
| Intents novos escolhidos pelo LLM (comparison, security, out_of_profile, resume, objection, refusal) | Menu de ações | Novo / T012-032B |
| Controle "CRM" + linguagem de dono de studio | Voice validator + juiz | Novo / T012-032 |
| Recusa de diagnóstico respeitada (não reoferecer no mesmo turno) | Ação `respect_diagnostic_refusal` + fixture | Novo / T012-032B |
| Retrieval seletivo por intenção (nunca tudo em todo prompt) | Context builder | Provado parcial / T012-031 |
| Objeções gerais via LLM, sem branch determinístico por objeção | Política + juiz | Novo / T012-032B |

## F. action-contract.md (011) - a arquitetura em si

| Regra | Dono | Status / Task |
| --- | --- | --- |
| Situation builder: entradas/saídas permitidas e proibidas | T012-030B | Novo |
| `ConductorActionDecision`: campos exigidos; proibido template plan/estado/texto final | T012-030A | Novo |
| Compiler: deveres (staged, variáveis oficiais, merge) e proibições (não sobrepor intenção do LLM) | T012-030C | Novo |
| Menus de ação por modo (entry/diagnostic/post/product/waitlist/handoff) | T012-030A | Novo |
| Anti-determinism boundary (forbidden: `if "demo" in text` etc.) | Auditoria estática | Portar / T012-040 |
| Ação sem variável de composição obrigatória FALHA (não vira fallback genérico) | Validator (lição T011-105) | Portar / T012-032 |

## G. eval-contract.md (010) - a régua

| Regra | Dono | Status / Task |
| --- | --- | --- |
| Layer 1: invariantes determinísticos bloqueiam release | Eval harness + fixtures | Portar / T012-038, 041 |
| Layer 2: ~32 cenários multi-turno obrigatórios | Fixtures canônicas + células novas | Portar+Novo / T012-038, 038B |
| Layer 2B: transcripts reais, mock nunca é evidência final | Paid gate | Provado (método) / T012-043 |
| Layer 3: juiz >= 4.2/5, nenhum P1 < 4.0 | Judge harness | Novo / T012-039 |
| Budget controls no runner (dry-run, caps, stop reason) | Harness do spike | Provado / reuso |

## Leitura executiva

- **Provado no spike:** ~25% das linhas (motor, interpretação, sequência do
  diagnóstico, segurança de fatos, custo, handoff).
- **Portar da 011:** ~40% (validators, fixtures, renderer, regras de canal -
  código existente e testado em produção).
- **Novo:** ~35% (situation builder, compiler, decisão compacta, delta de
  produto, juiz) - concentrado em T012-030A-C, 032B e 039.

Toda regra dos contratos tem exatamente um dono e uma task. Se durante a
Fase 3 surgir uma regra sem linha aqui, a matriz é atualizada ANTES do código.
