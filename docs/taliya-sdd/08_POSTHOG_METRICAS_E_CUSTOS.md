# PostHog: instrumentação, métricas e custo
## Delimitação
PostHog é a superfície analítica e de segmentação. Internal é operação humana. Backend é autoridade das contas, assinaturas e acesso. Não instalar outro CRM/GA4/Mixpanel paralelamente sem necessidade explícita. Não migrar atendimento ao PostHog Support nesta entrega.

## Configuração inicial proposta
Usar a conta/projeto já disponível, região adequada à política de dados e SDKs suportados. O plano free informa um projeto; não planejar gratuitamente dois projetos de staging/prod. Desenvolvimento usa mock/log sanitizado e feature flag de coleta off. Homologação real pode usar projeto isolado já autorizado; não misturar dados fictícios em métricas de produção. [P1]

Analytics com eventos explícitos primeiro. Replay desativado em chat/login/billing e, inicialmente, off globalmente até seleção/privacy QA. Group Analytics não é habilitado automaticamente. Workflows só após contrato de eventos e consentimento. Logs/AI observability não capturam transcrições privadas por padrão. [P3]

## Evento confiável
Envelope lógico: event_id; event_name; event_version; occurred_at UTC; producer; environment; schema_version; user_id verificado opcional; business_id opcional; conversation_id opcional; correlation_id; consent_scope quando aplicável; propriedades allowlist. IDs analíticos não conferem permissão. Timestamp de UI não redefine tempo de confirmação financeira.

Origem/UTM/referrer são contexto de marketing, não prova de identidade. Preservar primeiro toque e último toque elegível com janela proposta de 30 dias quando medição autorizada; `agent_assisted` usa janela proposta de 7 dias e significa associação observada. Não usar fingerprinting para recuperar usuários sem consentimento. Informar cobertura e desconhecidos.

## Produtores e deduplicação
Browser: navegação, clique e player observado. Auth: cadastro/identificação verificados. Billing: início financeiro, confirmação, renovação, falha/cancelamento/reembolso. App: ação de valor persistida. Runtime: turno, ferramenta, latência/falha/custo. Operação: takeover/envio humano confirmado. Modelos não decidem se o evento aconteceu.

Dedup antes do envio com outbox/IDs estáveis; confirmar comportamento de ingestão PostHog por teste. Dados financeiros oficiais para relatórios vêm de export/snapshot canônico e conciliação; um cliente pode fabricar eventos com a chave pública de coleta e isso não deve inflar a receita oficial. Não confiar somente em uma propriedade `source=backend` fornecida no browser.

## Seis painéis
| Painel | Perguntas/medidas | Unidade e cautela |
|---|---|---|
| Aquisição | visitas elegíveis, fontes/campanhas/criativos, páginas/CTAs | sessões e pessoas separadas; cobertura de consentimento |
| Conversão | visita → checkout iniciado → primeiro pagamento → primeiro valor; abandono e tempo | negócio/conta canônica no pós-cadastro; chat/vídeo opcionais |
| Conteúdo | sugerido/exibido/clicado/iniciado/25-50-75%/concluído, por material/versão | reprodução só com player observável; sem evento por segundo |
| Atendimento | conversa útil, handoff, sucesso de tools, erros, p50/p95, custo | distinguir input aceito, resposta gerada e entrega real |
| Ativação/retenção | primeiro valor, tempo de ativação, atividade útil posterior, D7/W4 | definição de valor do app, coorte madura e n explícito |
| Assinatura/receita | negócios pagantes, MRR normalizado, recebido, atrasos, cancelado efetivo, reembolso | conciliar ao billing; pedido de estorno não é devolução |

O dashboard dedicado Revenue Analytics foi removido; construir insights/queries apropriados no PostHog, não BI próprio nem promessa de painel universal pronto. [P5]

## Regras de cálculo propostas
Primeiro valor = primeira operação útil real persistida no negócio dentro de uma allowlist aprovada, excluindo demos/testes e simples abertura de tela. Usar definição vigente do app quando existente. Emitir marco uma vez por negócio e guardar data.

Retenção D7/W4: proporção dos negócios da coorte de ativação com nova atividade de valor na janela acordada. A janela e timezone precisam ser escritos no dashboard; coorte sem tempo suficiente não recebe taxa. Unidades de usuário e negócio nunca se misturam.

MRR operacional = soma de mensalidades equivalentes das assinaturas qualificadas por política versionada; anual/12. Recibos/caixa são outra medida. Decidir explicitamente o tratamento de descontos e inadimplência com o billing real. Cancelamento agendado aparece separado e só entra no churn de acesso/assinatura quando efetivo segundo definição. Pagante não é automaticamente ativo no produto.

CAC = gastos elegíveis de aquisição divididos por novos clientes na janela/coorte escolhida; sem gasto importado, não publicar CAC. LTV observado exige coortes e margem; projeção só com premissas visíveis. Atribuição não prova efeito causal do agente ou do vídeo.

## Dados por negócio sem addon obrigatório
Armazenar business_id no domínio e em eventos pertinentes. Usar distinct counts/SQL e export de projeções analíticas por negócio para métricas canônicas. Não substituir distinct_id da pessoa indiscriminadamente pelo ID do negócio. Group Analytics pode facilitar UI/coortes por organização, mas só após avaliação de custo/necessidade. [P4]

## Sincronização de banco
Preferir export/sync agendado de poucas tabelas analíticas sanitizadas, chaves primárias e updated_at/tombstones onde necessário. Não dar SELECT em todo public. Postgres source permite estratégias diferentes; CDC acrescenta privilégios de replicação/publication/slots e requisitos operacionais. Não ativar CDC nem conceder superuser para simplificar um dashboard. Validar se o conector aceita views; caso contrário usar pequenas tabelas/projeções permitidas, não presumir suporte. [P6]

## Custos
Franquia básica publicada: 1M eventos/mês. Free tem limites e o excedente pode ser descartado. Preços/addons variam conforme módulo e identificação. Não reproduzir tarifa de evento anônimo como custo de todo o SaaS, nem multiplicar base + identified sem verificar regra da calculadora/conta. [P1/P3]

Orçamento inicial proposto: zero cobrança até medir; depois teto agregado de até US$50/mês sujeito à autorização e distribuído por produto. Não é mensalidade nem garantia de escala. Registrar projeção após uma semana representativa e alertas de 70/85/95% antes do teto. Todos os módulos somados devem caber no orçamento aprovado. Não ativar pacote de plataforma/Group Analytics/replay/Workflows por padrão.

Exemplo apenas de volume: 20 mil visitas × 10 eventos + 500 usuários × 20 dias × 40 eventos + 50 mil eventos de backend = 650 mil eventos. Não prevê usuários reais nem inclui todos os possíveis adicionais. Custos de OpenAI, canais, vídeo, infra e impostos não são PostHog.

## Retenção/exclusão e saúde
Remover transcrições, documento financeiro, contato de cliente final, token e dados de cartão das propriedades por padrão. Replays exigem revisão de masking e coleta; não confiar só no nome da rota. Exclusão cobre perfil/eventos conforme capacidades e política de cada serviço; manter tombstone/reconciliação sem reimportar pessoa apagada inadvertidamente.

Relatório de saúde: último evento/relay, outbox pendente, sincronização, registros rejeitados, duplicação, gaps por limite/consentimento, diferenças com billing. Lacuna conhecida aparece no dashboard, não é escondida como queda de conversão.
