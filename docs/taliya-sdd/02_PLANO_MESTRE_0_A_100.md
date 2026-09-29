# Plano integral: de baseline a operação pronta
**Taliya · v3.0 · 2026-09-28**

## 1. Objetivo de negócio
Entregar uma aquisição SaaS integrada: uma pessoa entende a oferta, vê material útil, conversa quando precisa, contrata diretamente, recebe acesso no produto já pronto e tem seu relacionamento acompanhado sem registros paralelos. A equipe consegue agir sobre atendimentos; o PostHog mostra o desempenho de aquisição, atendimento, conteúdo, ativação, retenção e receita.

A proposta é um atendente simples conectado a uma operação confiável. Não uma equipe autônoma de vendedores, não um CRM novo, não um projeto de BI customizado e não uma reimplementação da assinatura.

## 2. Decisões preservadas
- App e assinatura estão prontos conforme o usuário; a entrega integra e faz regressão dos pontos tocados.
- Agents API, modelo `gpt-6-luna`, esforço `max`; sem fallback silencioso para outro modelo/esforço. [O1]
- Um agente, cinco funções pequenas, sem shell, navegação livre, SQL ou subagentes. Ambiente `none`. [O2]
- PostHog concentra análises; Internal concentra atendimento e ficha operacional. Backend é autoridade de identidade, dados, assinatura e acesso.
- Mensal/anual com Asaas, cartão recorrente/Pix Automático, cobrança na contratação e garantia em 14 dias. Não chamar de teste sem cobrança. Oferta/URLs vêm do billing publicado, não de preço hardcoded do ZIP. [L3/L4]
- Preservar design system, estrutura, tabs, carrosséis e hierarquia aprovados; adaptar somente o necessário ao comportamento definido. [L5]
- Desenvolvimento por specs rastreáveis. Um arquivo escrito não equivale a uma capacidade entregue.

## 3. Escopo final e limites
**Incluído:** fonte comercial; catálogo de mídia; agente e ferramentas; sessão/identidade; leads e projeção de cliente; integração à contratação pronta; webchat e canal comercial WhatsApp existente; fila/ficha Internal; instrumentação de landing/app/backend; seis dashboards; três automações controladas; privacidade; performance/acessibilidade; testes; migração; rollout; treinamento e runbooks.

**Não construir:** novo app, novo billing, segundo auth, CRM de vendas amplo, Kanban sem demanda, BI próprio, CMS próprio, segunda caixa de atendimento PostHog Support, agente de prospecção ativa, funções financeiras do LLM, suporte privado sem autenticação, novos recursos operacionais como equipes/booking por inferência. Não redesenhar toda a landing.

A produção de vídeos/UGCs é tratada como fornecimento de conteúdo com QA e publicação. O plano não presume que arquivos ainda não entregues existem nem exige montar uma produtora antes de integrar a biblioteca.

## 4. Arquitetura de responsabilidades
| Camada | Faz | Não faz |
|---|---|---|
| Landing | Explicar, demonstrar, assinar, entrar, pedir ajuda | Obrigar chat para contratar |
| Agente | Entender, responder, selecionar material e solicitar ações permitidas | Autorizar acesso, cobrar, confirmar pagamento por texto |
| Backend comercial | Contato, conversa, permissões, tools, pausa humana e projeções | Criar um billing paralelo |
| Backend do app/billing | Conta, negócio, assinatura, acesso e eventos de domínio | Depender de PostHog para uma venda funcionar |
| Internal | Fila e ficha; ação humana, auditoria e atalhos | Duplicar relatórios ou painel financeiro |
| PostHog | Funis, segmentos, comportamento, conteúdo, receita analítica e Workflows | Ser fonte de autorização/identidade financeira |

A sessão remota ajuda a continuidade, mas o backend guarda os recibos reais. Atualizar agente salvo não atualiza automaticamente suas sessões já criadas; a integração prevê versionamento e migração. [O3]

## 5. Jornadas que precisam funcionar
**Direta:** anúncio/visita → oferta → contratação existente → confirmação do billing → projeção de cliente → primeira ação útil no app. A IA pode estar desligada.

**Assistida:** visita → dúvida → resposta/ferramenta → um material relevante → CTA seguro → mesmo fluxo de contratação. Nada obriga telefone antes da dúvida.

**Cliente autenticado:** identidade verificada → contexto mínimo de conta/negócio → app/gestão/suporte; não oferecer segunda assinatura ativa.

**Pedido humano:** registrar solicitação e pausar de forma atômica → fila → operador autorizado → entrega no canal original → retomada explícita. Resposta tardia da IA não pode furar a pausa.

**Recuperação:** evento elegível → espera → verificação atual de permissão/assinatura → uma comunicação útil → supressão após compra/opt-out. Não duplicar as notificações financeiras já prontas.

**Falha:** serviço indisponível → status honesto e recuperação por ID; nenhuma confirmação falsa de cadastro ou pagamento; assinatura direta continua possível quando a IA/analytics caem.

## 6. Sequência concreta de execução
| Spec | Entrega | Dependências | Dias de engenharia* |
|---|---|---|---|
| 013 | Fundação, governança e contratos do produto pronto | — | 1–2 |
| 014 | Identidade, dados e segurança de base | 013 | 3–4 |
| 015 | Fonte única de produto, oferta e materiais | 013 | 2–3 |
| 016 | Runtime Agents API com Luna Max | 014, 015 | 3–5 |
| 017 | Cinco ferramentas e ciclo de leads/clientes | 014, 015, 016 | 3–5 |
| 018 | Landing, widget e integração à assinatura | 015, 017 | 2–4 |
| 019 | Vídeos, demonstrações e UGCs na experiência | 015 | 1–3 |
| 020 | Taliya Internal mínimo e operação humana | 014, 017 | 3–4 |
| 021 | Instrumentação confiável e integração PostHog | 017, 018, 019, 020 | 2–4 |
| 022 | Painéis SaaS, definições e limites de custo | 021 | 2–3 |
| 023 | Automações enxutas de relacionamento | 017, 020, 021, 022 | 1–2 |
| 024 | QA integrada, segurança, performance e evals | 018, 019, 020, 021, 022, 023 | 3–5 |
| 025 | Migração, publicação controlada e operação | 024 | 1–2 |

*Estimativas propostas para um profissional experiente, com auxílio de agentes de código e revisão. Somar não equivale a duração calendário: algumas frentes podem avançar em paralelo. Reestimar após mapear o commit atual e as interfaces prontas na 013. Nenhum valor é compromisso contratual.

## 7. Ondas e paralelismo
**Onda 0 — 013:** fechar autoridade e integrações. Saída: mapa real e proteção contra sobrescrever progresso.

**Onda 1 — 014 + 015:** identidade/dados e fonte/mídia podem evoluir em paralelo, com um contrato compartilhado.

**Onda 2 — 016 + 019:** runtime e publicação da mídia progridem com mocks explícitos de ferramenta, sem integração falsa.

**Onda 3 — 017:** provar a conexão entre conversa, contato, cadastro e billing.

**Onda 4 — 018 + 020:** integrar experiência pública e operação interna. Evitar dois agentes de implementação editando simultaneamente o mesmo widget/contrato.

**Onda 5 — 021 + 022:** instalar/adaptar instrumentação e configurar os painéis; o envelope e os produtores já são preparados nas specs anteriores.

**Onda 6 — 023:** adicionar relacionamento após a verdade dos dados existir.

**Onda 7 — 024 + 025:** homologar tudo, corrigir gaps, migrar e liberar por gates. Testes são feitos em cada spec, não deixados todos para esta onda.

## 8. O que significa 100% pronto
Não significa desempenho comercial garantido, CAC/LTV maduros ou ausência eterna de bugs. Significa que todo o escopo obrigatório foi entregue, testado e está operável:

1. Contratação direta e assistida funcionam sem segunda conta/assinatura.
2. Agente Luna/max usa fontes atuais e somente ferramentas autorizadas, com resposta natural e breve.
3. Contatos/clientes são vinculados corretamente; pagamento e acesso vêm da autoridade real.
4. Mídia real está publicada, classificada e mensurável, com fallback honesto.
5. Internal usa identidade de staff e responde/pausa/retoma sem corrida ou vazamento.
6. PostHog mostra as seis análises com definições, fontes, consentimento e orçamento controlados.
7. Automações estão implementadas e testadas; ativação real só ocorre onde há autorização/canal elegível. Um fluxo legitimamente desativado aparece explicitamente, não como defeito oculto.
8. CI, casos críticos, testes conversacionais reais e regressão de assinatura estão aprovados.
9. Rollback, reconciliação, restauração, exclusão e runbooks foram ensaiados.
10. Responsáveis receberam operação e evidências; não há bloqueador P0/P1 de lançamento aberto.

Uma capacidade é concluída com requisito + código/config + teste + evidência + operação. Nenhum percentual global foi inferido do tamanho do ZIP. O estado de requisitos em `planning/requirements.json` muda para verificado somente depois da prova.

## 9. Gates de liberação
**G0 — base:** 013 aprovada e autoridade real mapeada.
**G1 — segurança/dados:** 014/015; sem token público, merge inseguro ou oferta ambígua.
**G2 — vertical slice:** 016/017; conversa real com leitura, atualização permitida, ação segura e pausa.
**G3 — experiência/operação:** 018/019/020; contratar diretamente e atender humano funciona.
**G4 — dados/relacionamento:** 021/022/023; números reconciliados e envios elegíveis.
**G5 — homologação:** 024; todos os requisitos críticos comprovados.
**G6 — produção estabilizada:** 025; rollout autorizado e observado, rollback ensaiado, documentação fechada.

## 10. Dependências que faltam comprovar, sem reabrir o produto
O mapa da 013 precisa do commit/repositório atual do app/billing e do Internal, contratos de identidade/assinatura, acesso autorizado à conta OpenAI/PostHog, mídias aprovadas e responsável pelas mensagens/políticas. Esses itens podem ser obtidos nas fontes/repositórios disponíveis durante a execução; só pedir ao usuário o que não puder ser resolvido por leitura. Ausência de um acesso não autoriza inventar endpoint nem reimplementar tudo.

## 11. Custos e simplicidade
O PostHog inicia nas franquias; a reserva de US$50/mês discutida é orçamento proposto, não mensalidade e não autorização de gasto. Cada módulo tem limite próprio. Free possui 1 projeto e o teto pode descartar eventos. Usar mocks de analytics no desenvolvimento, sem poluir produção, ou projeto adicional já autorizado. [P1]

Group Analytics e replay amplo ficam desativados por padrão. A identidade de negócio e métricas por business_id existem mesmo sem o addon. Receita usa consultas/insights adequados ao billing, não pressupõe dashboard SaaS universal pronto. [P4/P5]

Custo Luna deve ser medido por conversa completa, incluindo raciocínio, contexto e tentativas; não transformar exemplo de tarifa em previsão. Não reduzir esforço max silenciosamente. Infra/banco/canal/vídeo e mão de obra não estão no orçamento PostHog.

## 12. Próxima ação exata
Iniciar `013-fundacao-e-contratos`: ler este pacote, comparar com o commit atual, registrar diferenças, mapear endpoints e resolver AGENTS/constituição/pointer. Em seguida executar o ciclo SDD dessa spec. Não começar pela tela do agente na OpenAI nem por gráficos antes de definir a verdade do domínio.
