# Auditoria Completa - Spec 012 - 2026-06-10

Auditoria de estado, qualidade e caminho até produção do agente comercial
Taliya sobre OpenAI Agents SDK. Base verificada nesta data: 71 testes no-cost
verdes, ruff limpo, 23 execuções pagas documentadas (~$2.20 total), endpoint
público intocado.

---

## 1. O estado final que queremos alcançar

**Para o lead:** um atendente no widget e no WhatsApp da Taliya que responde
qualquer pergunta em qualquer fase da conversa, conduz o diagnóstico gratuito
no fluxo controlado (6 perguntas na ordem, feedback a cada resposta, entrega
ao completar), recomenda plano com preço oficial, envia a demo oficial,
converte intenção clara em waitlist e passa para humano com graça.

**Para o negócio:**
- Zero preço/promessa/link inventado - garantia estrutural por código, não
  por confiança no modelo;
- Visibilidade total: trace por turno, projeção no Sales Inbox, custo medido;
- Custo operacional ~R$0,05-0,10 por conversa completa (~$0.01-0.02);
- Botão de rollback que desliga o agente sem reativar nenhum cérebro
  determinístico antigo;
- Handoff humano que pausa a IA de verdade (estado, não palavra).

**Critérios numéricos de "pronto" (proposta de aceite para T012-048):**
- 15 cenários congelados: 15/15 estrutural em 3 execuções consecutivas;
- Conversa ideal: 12/12 em 3 execuções consecutivas;
- Matriz de interrupções (~40 células): >= 90% de células verdes, zero
  violação de regra dura em qualquer célula;
- Do-not-do fixtures do Spec 011: 100%;
- Shadow mode: qualidade igual ou superior ao Spec 011 em amostra real,
  julgada por revisão manual do product owner;
- Custo por conversa dentro do teto definido.

## 2. O que está certo (provado com evidência paga)

| Item | Evidência |
| --- | --- |
| Arquitetura LLM-first + guardrails determinísticos | 23 runs: entendimento comercial correto desde o run 1; nenhuma regressão a regex |
| Zero texto livre entregue; só templates aprovados | Nenhum vazamento em nenhum run; adapter bloqueia estruturalmente |
| Zero fato inventado | Preços sempre de fonte oficial com fact_refs; validator bloqueou as 2 tentativas não-grounded |
| Roteamento | 100% correto desde o roteador puro (tool_choice required); decisão de especialista continua semântica |
| Diagnóstico controlado | 6/6 chaves na ordem exata com feedback por resposta, no gpt-5.4-mini, sem modelo forte |
| Funil completo | Run 15: 12/12 da abertura Instagram até waitlist qualificada ($0.116) |
| Repair de 1 operação | Recuperou ~40% dos turnos com falha; custo marginal ~$0.005 |
| Processo de engenharia | 0/15 -> 15/15 em 7 tentativas; conversa 0 -> 12/12 em 15 runs; cada classe de falha morta não retornou |
| Controles | Budget meter parou antes de qualquer estouro; tracing local-only; isolamento do endpoint público testado |

**O princípio que funcionou (e é a resposta de "como garantir"):** a catraca.
Cada falha descoberta foi movida de "o modelo precisa se comportar" para
"o código torna o mau comportamento impossível ou reparável". Classes mortas
nesta sessão que nunca voltaram: plano de template vazio, auto-atestação de
resposta, chave de diagnóstico inventada, estouro de turnos por releitura de
estado, pergunta-fantasma ressuscitada, entrega prematura de diagnóstico.

## 3. O que está errado (defeitos abertos, em ordem de gravidade)

1. **Adequação de resposta não verificada (P0 de qualidade):** o lead
   perguntou "quanto custa?" e o validator aceitou como respondido um template
   sem o número (run 15, msg 3). O check verifica pertencimento ao plano, não
   conteúdo. Correção: mapa determinístico pergunta->família de template
   adequada (preço só conta com `product.price_direct`/`price_complete_direct`).
2. **3 regressões abertas** (attempt-8: price_first, whatsapp_scope,
   demo_request) sob o conjunto final de regras - diagnósticos gravados,
   não analisados.
3. **Variância sem política:** o mesmo cenário passa num run e falha no
   seguinte. Falta definir aceite por repetição (3/3) em vez de run único.
4. **Bug do harness de transcript:** linhas duplicadas e um glitch de
   encoding na gravação - polui a revisão manual.
5. **Fragmento de abertura fora de lugar** ("Oi, tudo bem?" no turno da demo,
   run 15) - escorregão de template do modelo, não capturado por validator.
6. **Entrega final com 1 template** em vez do conjunto staged completo -
   completude de conteúdo da entrega sem regra.
7. **Spec defasada do código:** design-lock descreve triage que responde
   aberturas, cap de 3 operações, tools com state_snapshot_json - tudo
   revisado na prática e não documentado formalmente.

## 4. O que falta (lacunas, nada implementado ainda)

**No agente/harness (curto prazo, barato):**
- Matriz de interrupções (~10 tipos de pergunta x 4 fases) - a resposta
  definitiva para "ele interpreta tudo em qualquer fase";
- Cenário de objeção ("tá caro", "vou pensar") - a conversa mais comum de
  vendas está fora da bateria;
- Correção de resposta anterior ("na verdade são 80, não 120");
- Múltiplas respostas numa mensagem;
- Retomada após dias (resume) no caminho SDK.

**Na produção (Fase 3-5 da spec, o grosso restante):**
- Módulo SDK production-ready atrás de feature flag no endpoint real
  (T012-030/031);
- Conjunto COMPLETO de validators do Spec 011 (timing de waitlist, vazamento
  de labels, etc. - o spike usa subconjunto) (T012-032);
- Guardrails de segurança no caminho SDK: prompt injection, mídia não
  suportada, dados sensíveis (adiados por D-012-010, nunca testados);
- Sales Inbox persistido de verdade (hoje só proposto) (T012-035);
- Teto de custo por conversa no runtime;
- Golden transcripts e do-not-do do Spec 011 contra o caminho SDK (Fase 4);
- Shadow mode + prova de rollback + ativação (Fase 5).

**Na spec (passada de documentação, sem custo):**
- design-lock, eval-plan, coverage-map, tool-catalog, rag-policy e tasks
  atualizados conforme levantamento já feito (mensagem de 2026-06-10 no
  histórico da sessão; itens listados na seção 3.7 e no ledger).

## 5. Como garantir que chegamos lá

Com LLM não existe garantia de resultado por promessa - existe garantia por
**processo que converge**. Os quatro mecanismos:

1. **A catraca (já provada):** toda falha vira guardrail determinístico ou
   contrato de schema. Progresso é monotônico: classe morta não ressuscita.
   O custo de cada ciclo é baixo (~$0.10) e o diagnóstico é preciso (evidência
   por turno).
2. **Gates com critério numérico:** nenhuma fase avança sem o critério de
   aceite da seção 1 cumprido com evidência gravada. O ledger já impõe isso;
   falta fixar os números.
3. **Repetição contra variância:** aceite por 3 execuções consecutivas, não
   por run único. Custa ~$0.60 por bateria tripla - irrelevante perto do
   risco.
4. **Shadow mode como juiz final:** antes de qualquer lead real, o agente
   roda em paralelo ao Spec 011 com tráfego real sem responder ninguém, e a
   comparação é julgada por revisão humana. Se não for melhor, não corta.

O que NÃO fazer (anti-padrões que quase aconteceram nesta sessão):
- Confiar em pass estrutural como qualidade (run 1 da conversa: 12/12 com
  conversa péssima);
- Consertar comportamento por prompt quando o erro é de processo (3
  tentativas falharam até o roteador estrutural);
- Regredir entendimento para regex (o erro oposto - o spike provou que o
  modelo entende; o que ele precisa é trilho de processo).

## 6. Plano sequenciado até o estado final

| Etapa | Conteúdo | Custo | Gate de saída |
| --- | --- | --- | --- |
| 1. Consolidação (no-cost) | Bug do transcript, mapa de adequação, passada de specs, fixtures de objeção/interrupções/correção | $0 | 71+ testes verdes; spec descreve o sistema real |
| 2. Bateria completa | Fechar 3 regressões; matriz de interrupções; 3x repetição dos 15 + conversa ideal | ~$1.50 | Critérios numéricos da seção 1 (parte eval) |
| 3. Julgamento | Revisão manual sua dos transcripts; T012-028 comparação com Spec 011; T012-029 decisão | $0 | Decisão registrada: continuar/adaptar/abortar |
| 4. Produção (Fase 3) | Módulo production-ready, flag, validators completos, guardrails, Sales Inbox, teto de custo | eval ~$2-5 | Static audit + contract tests + goldens verdes |
| 5. Prova final (Fase 4-5) | Goldens 3x, do-not-do, shadow mode, rollback, preflight | shadow ~$5-20 | Sua aprovação formal de ativação |

Estimativa honesta: etapas 1-3 cabem em 1-2 sessões de trabalho; a Fase 3 é o
maior bloco de engenharia restante (semelhante em esforço a tudo feito até
aqui); shadow depende de volume de tráfego real.

## 7. Decisões que continuam sendo suas

1. Aprovar os critérios numéricos de aceite da seção 1 (ou ajustá-los);
2. Orçamento da etapa 2 (~$1.50) e, adiante, das fases 4-5;
3. A revisão manual de qualidade (gate que só o product owner fecha);
4. A decisão T012-029 quando a evidência estiver completa.
