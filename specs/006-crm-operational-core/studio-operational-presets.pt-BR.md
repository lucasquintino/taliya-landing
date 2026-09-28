# Presets iniciais do studio - PT-BR

> Status: decisao D036 fechada v0.1. Este documento evita que o setup inicial vire uma parede de configuracoes.

## Decisao

O onboarding deve oferecer 3 presets iniciais.

O gestor escolhe um caminho e depois ajusta detalhes. Nenhum preset ativa autonomia sensivel por padrao.

| Preset | Para quem | Postura |
| --- | --- | --- |
| Conservador | Studio que quer controle humano forte. | Mais aprovacoes, menos automacao, mensagens mais cuidadosas. |
| Equilibrado | Studio comum que quer ganhar tempo sem perder controle. | Copiloto por padrao, automacao simples onde risco e baixo. |
| Crescimento | Studio com foco comercial e ocupacao. | Mais follow-up, alertas comerciais e automacao em tarefas seguras. |

## Configuracoes por preset

| Area | Conservador | Equilibrado | Crescimento |
| --- | --- | --- | --- |
| Agentes | Manual/copiloto; autonomo desligado. | Copiloto; autonomo apenas em lembretes seguros depois de teste. | Copiloto forte; autonomo em follow-up seguro depois de teste. |
| Reposicao | Falta avisada 12h; credito 30 dias; 2 creditos ativos; aprovacao em excecao. | Mesma regra padrao; sistema sugere encaixe. | Mesma regra padrao; sistema prioriza ocupacao e lista de espera. |
| Encaixe | Sistema calcula; humano envia convite. | Sistema calcula; copiloto sugere mensagem. | Sistema calcula; convite pode ser automatizado em fluxo seguro. |
| Cobranca | Humano aprova mensagens. | Copiloto redige; humano aprova casos delicados. | Lembretes simples podem automatizar; acordo/excecao sempre humano. |
| Vendas | Tarefas manuais e sugestao de resposta. | Cadencia com copiloto e lembretes. | Cadencia mais ativa, ate 5 tentativas em 14 dias. |
| Retencao | Alertas e tarefas humanas. | Copiloto sugere contato. | Alertas mais frequentes; campanhas de reativacao com aprovacao. |
| Comunicados | Sempre aprovacao humana. | Aprovacao humana; custo/cota visivel. | Segmentos sugeridos; envio ainda aprovado. |
| Professor | Historico minimo permitido. | Historico operacional permitido. | Igual Equilibrado; sem dado sensivel bruto. |
| Cotas | Modo economia mais cedo. | Alertas em 70/90/100. | Alertas em 70/90/100 e sugestao de pacote. |
| Notificacoes | Menos alertas, mais resumo. | Alertas acionaveis. | Alertas comerciais e ocupacao mais visiveis. |

## Setup guiado

O onboarding deve perguntar:

1. Qual preset voce quer comecar?
2. Quais horarios e turmas existem?
3. Quem faz atendimento, agenda, financeiro e aulas?
4. WhatsApp/canal esta pronto?
5. Quer importar alunos agora ou cadastrar depois?
6. Quais agentes do plano devem ficar em teste?

## Regras de seguranca

- Autonomia sensivel nunca vem ligada no preset.
- Trocar preset depois do setup mostra impacto antes de aplicar.
- Mudancas em permissao, financeiro, privacidade, contrato e LGPD sempre exigem permissao e auditoria.
- O plano Base pode usar qualquer preset como organizacao do CRM, mas sem agentes ativos.

## Como aparece nas telas

| Tela | Como usar preset |
| --- | --- |
| Onboarding | Escolha visual com resumo de postura e impacto. |
| Hoje | Prioridades e alertas respeitam o preset. |
| Configuracoes | Mostra preset atual, ajustes e impacto. |
| Agentes | Modos iniciais e limites partem do preset. |
| Uso/cotas | Limites e modo economia partem do preset. |
| App mobile | Permite ver preset e fazer ajustes essenciais; configuracao profunda vai para web. |
