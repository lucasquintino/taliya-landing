# Conclusão de Conformidade com os Contratos Binding - 2026-06-10

Leitura completa dos contratos binding congelados pela Spec 012 (T012-002):
`010/behavior-contract.md`, `010/conversation-state-contract.md`,
`010/diagnostic-contract.md`, `010/message-template-contract.md`,
`010/product-followup-delta-contract.md`, e `011/action-contract.md`.

Confronto contra o que foi construído no spike Spec 012.

---

## Resposta direta às três perguntas

**1. Temos todos os comportamentos mapeados?** Sim. Os contratos cobrem
exaustivamente: aberturas (fria, widget, Instagram, site, CTA diagnóstico),
pergunta direta (preço, plano, demo, WhatsApp, integração, segurança),
objeção de preço, diagnóstico completo (6 chaves, ordem, cadência, feedback,
entrega staged), demo, waitlist, handoff, pós-diagnóstico consultivo,
comparação com ferramentas, fora-de-perfil, recusa de diagnóstico, resume,
estados não-lineares (múltiplas perguntas, correções, contradições, irritação).
Nada de comportamento está faltando nos contratos. O mapa existe e é binding.

**2. Temos todos os templates mapeados?** Sim. `message-template-contract.md`
define ~60 templates por categoria; o `template_registry` do runtime tem 63.
Mais 5 templates novos do delta (`how_it_works`, `comparison_current_tool`,
`integration_scope_direct`, `security_data_direct`, `out_of_profile_redirect`).
A voz oficial está catalogada, com regras de variáveis, estados permitidos,
canal, e exemplos de aceite/rejeição.

**3. Teremos um agente LLM que entrega isso ao final da spec?** Pode-se sim,
MAS o spike Spec 012 está construído sobre a arquitetura ERRADA para isso.
Esta é a descoberta central abaixo.

## A descoberta central: arquitetura divergente

A Spec 011 (`action-contract.md`) existe porque **deixar o LLM escolher
templates e preencher todas as variáveis diretamente FALHOU nos testes pagos
T011-105**. A correção binding é uma arquitetura **action-first**:

- Um **Turn Situation Builder** (código determinístico) calcula o tabuleiro a
  partir do estado persistido e entrega ao LLM um menu: `allowed_actions`,
  `pending_question_key`, `eligible_template_groups`, `missing_diagnostic_keys`.
- O LLM retorna uma decisão PEQUENA (`ConductorActionDecision`): escolhe UMA
  ação do menu, interpreta intenção, captura slots. O LLM **NÃO** retorna
  template_plan final, variáveis-resposta inteiras, nem texto final.
- Um **Decision Compiler** (código determinístico) deriva: transição de
  estado, merge do ledger, **a entrega staged final do diagnóstico**,
  expansão do grupo de templates, e **as variáveis cujo source é
  conhecimento oficial ou estado de runtime**.

O que eu construí no spike Spec 012 é o oposto: o LLM escolhe os
`template_ids` diretamente e preenche TODAS as variáveis. Isso é mais próximo
do `010/behavior-contract.md` (linha 13), mas o `011/action-contract.md`
**corrige e supera** a 010 exatamente nesse ponto (linhas 88-94: "The LLM must
not return final template_plan, whole-response variables").

**Eu re-descobri, em 15+ runs pagos, o mesmo modo de falha que a Spec 011 já
tinha resolvido** - e resolvi com um mecanismo diferente (validators + repair)
em vez do mecanismo prescrito (menu de ações + compiler).

## Por que isso explica todos os nossos defeitos

| Defeito observado no spike | Causa pela lente do contrato binding |
| --- | --- |
| Entrega final com 1 template (run 15) viola ordem staged | A entrega staged é responsabilidade do **Decision Compiler** (011 linha 104), não do LLM. Eu pus o LLM para lembrar de emitir 7 templates na ordem - ele esquece. O compiler nunca esqueceria. |
| Repair em ~40% dos turnos | No design action-first, o compiler deriva o que eu estou fazendo o LLM adivinhar e reparar. Menos a derivar = menos a falhar. |
| Feedback repete o lead mecanicamente (proibido, diag-contract linha 89) | Variável `answer_feedback` sem a regra anti-paródia do contrato. |
| Estouro de turnos por releitura de estado | Resolvido pelo Turn Situation Builder, que entrega o tabuleiro pronto. |
| Plano antes de operacional, "Para plano eu compararia" | Ordem e frases banidas explicitadas em diag-contract e msg-template-contract; meu validator não tinha o conjunto completo. |

A conclusão honesta: o spike provou que o SDK funciona como motor e que o
modelo entende - mas a forma como liguei LLM aos templates é a forma que a
própria casa já tinha aposentado por falhar.

## Conformidade item a item (resumo)

**Conforme:** chaves do diagnóstico e redação exata das 6 perguntas; linha
final de plano; metas de custo; topologia de agentes; LLM-first sem regex;
isolamento de escopo; handoff pausa estado; preço/fato sempre oficial.

**Divergente (arquitetura):** LLM escolhe template+variáveis (deveria escolher
ação; compiler deriva); sem Turn Situation Builder; sem Decision Compiler;
schema de decisão simplificado sem os campos canônicos de estado
(`previous/current/next_state`, `opening_type`, `policy_checks`).

**Faltando:** entrega staged derivada pelo compiler; mensagem de hold;
política de nome; estados canônicos (25 estados do state-contract); 5 templates
do delta; conhecimento de produto `how_it_works`/`routine_areas`/
`whatsapp_scope`/etc.; contexto pós-diagnóstico compacto; objeção, comparação,
fora-de-perfil, recusa de diagnóstico, resume; juiz de qualidade >= 4.2/5
(o gate de eval real, nunca rodado - medi "passed_structural").

**Violando (precisa correção antes de produção):** feedback com repetição
literal; entrega final não-staged; saudação repetida no meio da conversa.

## O estado final correto (reconciliado com os contratos)

Um agente onde:
- o LLM é o cérebro de interpretação e escolhe UMA ação por turno de um menu
  que o código preparou;
- o Decision Compiler deriva deterministicamente a entrega staged, as
  variáveis de fonte oficial, e a transição de estado - tornando as classes de
  falha do spike IMPOSSÍVEIS, não reparadas;
- os ~60 templates + 5 do delta são a voz, com as regras de voz (sem CRM para
  leigo, linguagem de dono de studio, frases banidas) aplicadas por validator;
- os 25 estados canônicos governam a jornada;
- o gate é juiz de qualidade >= 4.2/5 em transcripts reais, não pass estrutural.

## Recomendação

O trabalho do spike NÃO é perdido: o motor SDK, o output estruturado estrito,
o budget meter, o tracing local, o harness de conversa, os validators de
segurança - tudo reaproveita. O que precisa mudar é a **fronteira LLM-template**:
migrar de "LLM escolhe template+variáveis" para "LLM escolhe ação +
compiler deriva", que é a arquitetura binding da Spec 011.

Próximo passo proposto (no-cost): reescrever o `design-lock.md` da Spec 012
para adotar o pipeline action-first do `011/action-contract.md` como alvo de
produção, com o `TaliyaSdkTurnOutput` reduzido a um `ConductorActionDecision`
e um Decision Compiler novo. Depois, portar as fixtures reais de
`011/regression-cases.md` e `011/do-not-do-static-fixtures.json` no lugar dos
15 cenários reconstruídos. Só então uma rodada paga de validação.

## Documentos ainda não lidos (Tier 2/3, para a próxima passada)

`011/contract-schema-map.md`, `011/template-variable-registry.md`,
`011/governance-metadata-contract.md`, `010/sales-inbox-contract.md`,
`010/contracts/eval-contract.md`, `009/conversation-policy.md` e
`009/contracts/*`. Nenhum deve mudar a descoberta central, mas precisam ser
confrontados antes de fechar o design-lock action-first.
