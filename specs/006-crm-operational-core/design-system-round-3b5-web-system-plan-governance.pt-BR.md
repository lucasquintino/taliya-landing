# Design System Web - Rodada 3B.5 - Sistema, Plano E Governanca

> Status: biblioteca visual v0.1 aprovada. Esta rodada documenta componentes administrativos de plano, cotas, permissoes, billing, integracoes, auditoria, politicas e configuracoes.

## Objetivo

Definir os componentes administrativos do Taliya CRM web sem transformar governanca em sistema separado.

Esta rodada cobre:

- plano e agentes;
- plano base com 0 agentes;
- cotas e limites;
- barra de progresso de uso;
- fallback manual;
- permissoes e acesso;
- integracoes;
- billing e pagamento;
- auditoria e logs;
- politicas e guardrails;
- configuracoes gerais;
- estado CRM ativo com 0 agentes configurados.

## Decisao

A imagem da Rodada 3B.5 fica aprovada como v0.1.

Ela acertou:

- incluiu explicitamente plano base com 0 agentes;
- mostrou que CRM continua ativo sem agentes;
- cobriu cotas, limites e fallback manual;
- trouxe permissoes em formato operacional;
- integrou billing, pagamento e faturas sem virar checkout;
- mostrou integracoes conectadas e com erro;
- incluiu auditoria, politicas e configuracoes;
- manteve linguagem administrativa clara.

## Ressalvas

- A prancha e densa e branca; em paginas reais precisa de mais cinza frio e hierarquia.
- Upgrade nao deve parecer obrigatorio no estado 0 agentes.
- Cotas em vermelho devem indicar proximidade real de limite, nao ansiedade visual.
- Politicas e guardrails precisam ser legiveis para gestor, nao so tecnico.
- Billing deve ser claro, mas nao deve assumir fluxo completo de checkout nesta camada.

## Regras De Uso

- Estado 0 agentes deve sempre manter o CRM manual utilizavel.
- Card de plano deve separar "CRM ativo" de "agentes contratados".
- Cota deve mostrar uso, limite, status e fallback.
- Bloqueio por permissao deve explicar motivo e caminho de solicitacao.
- Integracao com erro deve oferecer reconectar e ver detalhes.
- Auditoria deve registrar ator, origem, objeto, horario e status.
- Politicas devem mostrar autonomia, aprovacao humana, risco e versao.
- Configuracoes devem usar inputs, selects e toggles da 3B.1.

## Nao Fazer

- Nao criar landing page de pricing.
- Nao bloquear CRM por ausencia de agentes.
- Nao esconder fallback manual.
- Nao transformar governanca em tela tecnica pesada.
- Nao usar billing como centro da experiencia operacional.
- Nao usar cores novas dominantes para planos.

