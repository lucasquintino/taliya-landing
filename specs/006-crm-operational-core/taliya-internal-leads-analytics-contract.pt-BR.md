# Contrato - Leads, Landing E Analise Comercial Interna - PT-BR

> Status: v0.1. Complementa `taliya-internal-backoffice-contract.pt-BR.md` para a primeira fase do CRM interno focada em leads comerciais da Taliya, analise da landing, conversas do agente comercial e melhoria controlada do agente.

## Decisao Central

A Taliya vai usar ferramentas externas para ajudar a analisar leads, conversas e performance comercial.

Essas ferramentas sao apoio de analise, alerta, digest, julgamento, priorizacao e sugestao.

Elas nao sao a fonte de verdade dos leads e nao podem alterar o agente comercial automaticamente.

Fonte de verdade:

- Sales Inbox/Postgres para lead, mensagens seguras, status, operador e funil comercial;
- `agent_runtime_*` para conversa completa, estado do agente, mensagens, execucoes, custo, guardrails, traces e uso de modelo;
- product knowledge versionado para fatos oficiais de preco, plano, demo, disponibilidade, links e promessas comerciais;
- auditoria interna para acoes sensiveis e mudancas aprovadas.

Ferramentas externas podem ler uma visao segura desses dados e devolver analises estruturadas.

## Escopo Desta Fase

Foco:

- leads da landing `/pilates`;
- conversas do widget comercial;
- conversas do WhatsApp comercial da propria Taliya;
- eventos da landing;
- origem, CTA, secao e campanha;
- analise de qualidade das conversas;
- analise de qualidade do lead;
- sugestoes de melhoria para prompt, templates, validadores, product knowledge e copy comercial.

Fora desta fase:

- CRM dos studios em `/app/*`;
- alunos, interessados e vendas dos studios;
- WhatsApp dos studios clientes;
- checkout/billing definitivo;
- multi-tenant operacional;
- alteracao automatica do agente sem aprovacao humana.

## Superficies Internas

### `/internal/leads`

Lista/pipeline oficial dos leads comerciais da Taliya.

Substitui a leitura mental de `/internal/sales-inbox` como pagina principal, mantendo `/internal/sales-inbox` como alias ou modo legado.

Deve permitir analisar:

- lead;
- canal;
- origem;
- campanha/UTM quando disponivel;
- secao/CTA de entrada;
- etapa comercial;
- prioridade;
- status;
- dor principal;
- plano ou interesse;
- diagnostico;
- waitlist;
- handoff humano;
- ultima atividade;
- proxima acao;
- dono interno;
- qualidade da conversa;
- qualidade/completude do lead.

### `/internal/leads/[leadId]`

Detalhe do lead comercial.

Deve mostrar:

- resumo comercial;
- dados do studio e contato;
- origem completa da landing;
- eventos de funil;
- transcript completo ou link para transcript completo;
- mensagens recentes;
- diagnostico;
- demo;
- waitlist;
- recomendacao;
- objecoes;
- proxima acao;
- status de humano/IA;
- runtime/trace/custo;
- analise de qualidade da conversa;
- sugestoes geradas por ferramentas externas;
- acoes do operador;
- auditoria.

### `/internal/commercial-metrics`

Pode ser aba de `/internal/leads` ou bloco dentro de `/internal`.

Deve mostrar:

- visitas e eventos por origem;
- leads criados;
- primeira mensagem enviada;
- diagnosticos oferecidos;
- diagnosticos concluidos;
- perguntas de preco/plano;
- demo solicitada;
- waitlist oferecida/aceita;
- handoff humano;
- ganhos/perdidos;
- principais objecoes;
- principais dores;
- conversas com problema;
- custo estimado do agente por lead/conversa;
- taxa de fallback/guardrail;
- falhas de WhatsApp/n8n.

## Ferramentas Externas Permitidas

### n8n

Uso permitido:

- alerta de lead quente;
- digest diario ou periodico;
- alerta de guardrail/fallback;
- alerta de falha operacional;
- lembrete de follow-up permitido;
- notificacao de acao de operador;
- envio de snapshot seguro para ferramentas de analise.

Uso proibido:

- ser banco de leads;
- receber lead-upsert obrigatorio;
- guardar transcript bruto completo por padrao;
- decidir preco, plano, checkout, desconto ou promessa;
- alterar status pago/assinatura;
- burlar opt-out, pausa humana, janela do WhatsApp ou template aprovado;
- alterar prompt, template, validador ou product knowledge automaticamente.

### Codex Automation

Uso permitido:

- rodar rotina diaria de leitura segura;
- gerar relatorio de conversas;
- identificar problemas de qualidade;
- comparar conversas novas contra contratos/evals;
- sugerir patches;
- criar plano de correcao;
- preparar PR/diff para revisao;
- gerar novas fixtures/evals a partir de falhas reais, com dados sensiveis removidos.

Uso proibido:

- aplicar mudanca em producao sem revisao;
- mudar comportamento comercial baseado em uma unica conversa sem evidencias;
- transformar entendimento comercial em regex/state-machine;
- criar atalhos deterministas para preco, demo, plano, diagnostico, waitlist ou mensagens ambiguas;
- expor prompts, segredos, tokens, payloads sensiveis ou dados pessoais desnecessarios.

### LLM/Judge Externo

Uso permitido:

- classificar qualidade de conversa;
- detectar resposta confusa;
- detectar promessa indevida;
- detectar vazamento interno;
- detectar problema de PT-BR/pontuacao;
- detectar se a resposta respondeu a pergunta do lead;
- classificar objecoes;
- sugerir melhoria de template/copy;
- sugerir novo caso de teste.

Uso proibido:

- decidir sozinho que uma conversa e aprovada para producao;
- substituir revisao humana em mudancas de alto impacto;
- gerar mensagem direta para lead sem passar pelo runtime oficial;
- alterar product knowledge oficial;
- marcar lead como ganho/perdido sem operador;
- mudar plano/preco/oferta.

### Analytics Externo

Uso permitido:

- agregados de funil;
- eventos de landing;
- origem/UTM/campanha;
- taxa de conversao por CTA/secao;
- dashboards de performance.

Uso proibido:

- receber transcript bruto completo por padrao;
- armazenar dados sensiveis de lead sem necessidade;
- virar fonte de verdade do lead;
- operar a conversa.

## Pipeline De Dados

Fluxo minimo:

```text
landing/widget/WhatsApp
  -> runtime comercial
  -> Sales Inbox/Postgres
  -> agent_runtime_*
  -> eventos seguros de funil
  -> ferramentas externas analisam snapshots seguros
  -> relatorio/sugestoes voltam para /internal/leads
  -> operador/Codex revisa
  -> mudanca aprovada vira patch/eval/template/prompt/product knowledge
```

Regra:

- nenhuma ferramenta externa deve ser necessaria para o lead aparecer no CRM interno;
- se uma ferramenta externa falhar, o lead, a conversa e a acao do operador continuam funcionando;
- snapshots externos devem ser suficientes para analise, mas minimizados para privacidade.

## Snapshot Seguro Para Analise

Um snapshot enviado para ferramenta externa pode conter:

- lead id interno;
- conversation id;
- canal;
- origem;
- CTA/secao;
- etapa comercial;
- prioridade;
- status;
- mensagens visiveis da conversa, quando necessario para qualidade;
- resumo comercial;
- diagnostico;
- template ids;
- guardrail flags;
- custo estimado;
- fonte de produto usada;
- proxima acao;
- resultado atual da conversa.

Deve remover ou mascarar:

- tokens;
- secrets;
- system prompts;
- assinatura HMAC;
- payload bruto de provedor;
- cartao, CVV, senha ou credencial;
- dados sensiveis de saude;
- telefone/email quando nao forem necessarios para a analise;
- identificadores externos desnecessarios.

## Analise De Qualidade Da Conversa

Cada conversa analisada deve poder receber:

- status: `aprovada`, `atenção`, `reprovada`, `precisa_revisao_humana`;
- severidade: `P0`, `P1`, `P2`, `P3`;
- resumo do problema;
- trecho ou turnos afetados;
- categoria;
- causa provavel;
- solucao sugerida;
- se precisa mudar prompt, template, validador, product knowledge, fixture ou UI;
- se precisa virar incidente;
- se precisa virar novo eval.

Categorias minimas:

- nao respondeu pergunta direta;
- diagnostico sem aceite;
- diagnostico robotico;
- pergunta desalinhada com resposta do lead;
- contexto velho/stale context;
- vazamento interno;
- linguagem tecnica demais;
- PT-BR/pontuacao ruim;
- promessa indevida;
- preco/plano/link sem fonte;
- checkout/desconto/disponibilidade sem base;
- uso indevido de CRM para lead leigo;
- handoff humano mal aplicado;
- waitlist mal aplicada;
- lead salvo incompleto;
- origem/CTA ausente;
- custo alto;
- fallback/guardrail.

## Analise Do Lead

Cada lead deve poder ter:

- fit: `alto`, `medio`, `baixo`, `fora_de_perfil`, `desconhecido`;
- temperatura: `quente`, `morno`, `frio`, `manual`;
- dor principal;
- urgencia;
- objecao principal;
- tamanho/sinal de escala;
- contexto operacional;
- plano ou faixa sugerida;
- proxima melhor acao;
- dados faltantes;
- risco de perda;
- motivo de perda, quando aplicavel.

Essa analise ajuda o operador, mas nao substitui decisao humana em fechamento, checkout, desconto ou marcacao de ganho.

## Analise Da Landing

Eventos minimos para cruzar com leads:

- `page_view_niche`;
- `landing_viewed`;
- `cta_click`;
- `consultor_cta_clicked`;
- `whatsapp_cta_clicked`;
- `faq_item_opened`;
- `faq_doubt_cta_clicked`;
- `floating_agent_opened`;
- `first_meaningful_chat_message`;
- `plan_asked`;
- `guided_demo_started`;
- `custom_agent_diagnostic_started`;
- `custom_agent_diagnostic_submitted`;
- `checkout_intent`;
- `lead_won`;
- `lead_lost`.

Campos desejados:

- session id;
- lead id quando existir;
- source page;
- source section;
- entry path;
- CTA id/variant;
- UTM source/medium/campaign/content/term;
- referrer;
- device class;
- timestamp.

Perguntas que o admin deve responder:

- de onde vieram os leads;
- qual CTA gerou conversa;
- quais secoes geram lead qualificado;
- onde o lead abriu widget e desistiu;
- quais origens trazem pergunta de preco;
- quais origens trazem dor real;
- quais origens geram handoff;
- quais conversas viram waitlist;
- quais conversas viram ganho/perda.

## Ciclo De Melhoria Do Agente

Rotina recomendada:

```text
diariamente
  -> coletar conversas novas
  -> gerar analise automatica
  -> marcar problemas por severidade
  -> gerar sugestoes de correcao
  -> operador/Codex revisa
  -> aprovadas viram patch + teste/eval
  -> rodar suite sem custo quando possivel
  -> rodar teste pago apenas quando necessario/aprovado
  -> publicar mudanca somente depois de revisao
```

Regra critica:

- ferramenta externa ensina por sugestao, nao por mutacao automatica;
- toda melhoria de comportamento precisa deixar rastro: conversa origem, problema, decisao, patch, teste/eval e resultado;
- se a correcao muda comportamento comercial, preservar o principio LLM-first.

## O Que Nao Fazer

- nao criar CRM paralelo fora do Postgres/Sales Inbox;
- nao voltar para Airtable/planilha como fonte de verdade;
- nao deixar n8n decidir lead, preco, checkout ou status;
- nao deixar ferramenta externa editar prompt/template automaticamente;
- nao usar regex como cerebro comercial;
- nao enviar transcript bruto completo para ferramenta externa sem necessidade;
- nao expor dados sensiveis;
- nao misturar leads da Taliya com interessados dos studios;
- nao misturar analise da landing com billing pago.

## Implementacao Recomendada

Ordem segura:

1. Formalizar `/internal/leads` como superficie principal, usando a Sales Inbox atual como base.
2. Garantir que cada conversa da Spec 012 alimente `sales_leads` e `agent_runtime_*` com ids cruzaveis.
3. Persistir eventos de landing/funil com `sessionId`, `leadId`, `entryPath`, `sourceSection`, `CTA` e UTM.
4. Criar export/snapshot seguro para analise externa.
5. Criar rotina de analise diaria por ferramenta externa.
6. Exibir resultado da analise no detalhe do lead.
7. Criar fila de melhorias do agente.
8. Transformar falhas recorrentes em fixtures/evals antes de mudar comportamento.

## Aceite

Esta fase e aceitavel quando:

- todo lead comercial aparece em `/internal/leads` ou alias atual;
- cada lead mostra origem da landing e transcript suficiente;
- eventos de landing conseguem ser cruzados com leads;
- conversas novas podem ser analisadas por ferramenta externa;
- analises voltam como registros revisaveis, nao como mudancas automaticas;
- problemas recorrentes geram sugestoes, testes e patches rastreaveis;
- n8n/ferramentas externas podem falhar sem perder lead ou conversa;
- nenhuma ferramenta externa vira fonte de verdade ou altera o agente sozinha.
