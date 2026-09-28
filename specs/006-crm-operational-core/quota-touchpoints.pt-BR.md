# Pontos de contato de cotas - PT-BR

> Status: Rodada 0 v0.1. Cotas sao governanca operacional, nao apenas billing.

## Regra central

Toda automacao paga deve saber se pode rodar antes de executar. Quando nao puder, o CRM deve manter caminho manual.

## Limites de lancamento

| Plano | Automacao ativa de IA |
| --- | ---: |
| Base | 0 mensagens/execucoes ativas de agente por mes |
| 1 Agente | 1.500 mensagens de IA/mes |
| 3 Agentes | 5.000 mensagens de IA/mes |
| 7 Agentes | 15.000 mensagens de IA/mes |

## Origens de consumo

| Origem | Exemplos |
| --- | --- |
| IA | classificar, resumir, sugerir, redigir, detectar risco. |
| WhatsApp service | resposta dentro de janela iniciada pelo contato. |
| WhatsApp utility | lembrete, confirmacao, agenda, pagamento. |
| WhatsApp marketing | reativacao, campanha, comunicacao comercial. |
| Batch job | processamento em massa, segmento, campanha. |
| Midia | audio, imagem, documento, transcricao. |
| Historico | resumo longo, compressao de linha do tempo. |

## Telas onde cota precisa aparecer

| Tela | Como aparece |
| --- | --- |
| Hoje | Alerta 70/90/100 e tarefas criadas por downgrade. |
| Agentes e fluxos | Estimativa por fluxo, limite mensal, limite por tentativa. |
| Simulacao de fluxo | Custo estimado antes de ativar. |
| Execucao de agente | Cota consumida e origem. |
| Aprovacoes | Custo previsto antes de aprovar envio/acao. |
| Inbox/conversa | Aviso se sugestao/envio do agente esta bloqueado por cota. |
| Comunicados | Estimativa de custo por publico/canal. |
| Cobrancas | Origem de WhatsApp utility/service e limite. |
| Retencao/campanhas | Downgrade em 90%, bloqueio em 100%. |
| Uso e cotas | Visao completa, extrato, alertas, pacotes e economia. |
| Billing/add-ons | Compra/solicitacao de pacote extra. |
| Mobile Cotas | Consulta, alerta, motivo do bloqueio e acao simples. |

## Comportamento por limite

| Uso | Comportamento |
| --- | --- |
| 0-69% | Fluxos rodam conforme configuracao. |
| 70% | Alerta preventivo com previsao de consumo. |
| 90% | Modo economia: baixo valor vira tarefa ou aprovacao. |
| 100% | Automacao paga para; CRM manual segue. |
| Pacote ativo | Fluxos elegiveis retomam conforme regra. |

## Acao depois do limite

Cada fluxo deve escolher uma acao:

- parar;
- criar tarefa;
- pedir aprovacao;
- chamar fila responsavel;
- mover para fluxo manual;
- seguir apenas interno, sem envio externo.

## Aceite

Nenhuma tela com IA/agente esta pronta se nao disser:

- se consome cota;
- origem do consumo;
- estimativa antes da acao quando possivel;
- comportamento em 90%;
- comportamento em 100%;
- alternativa manual.
