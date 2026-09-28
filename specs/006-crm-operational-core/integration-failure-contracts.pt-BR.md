# Contratos de integracao e falha - PT-BR

> Status: Rodada 0 v0.1. Este documento define comportamento quando canais, provedores e jobs falham.

## Regra central

Falha de integracao nunca pode sumir. Deve virar estado, log, tarefa, caso ou incidente com proxima acao clara.

## Integracoes criticas

| Integracao | Uso | Falha deve fazer |
| --- | --- | --- |
| WhatsApp | conversas, envios, handoff, comunicados. | Registrar tentativa, mostrar falha, evitar duplicidade, criar tarefa manual se preciso. |
| Pagamentos | status de pagamento, link, conciliacao. | Marcar em analise/falha, evitar confirmacao falsa, criar tarefa/aprovacao ou escalar para Operacao quando sensivel. |
| Billing Taliya | plano, entitlement, cota, fatura. | Limitar com cuidado, mostrar status, abrir suporte Taliya se necessario. |
| Importacao | entrada inicial de dados. | Parar lote, mostrar erros, preservar parcial seguro, revisar duplicidades. |
| Exportacao | backup, contabilidade, LGPD. | Mostrar job falho, permitir retry, auditar solicitacao. |
| IA/provedor de modelo | sugestao, resumo, classificacao. | Usar fallback, criar tarefa, nao executar acao incerta. |
| Webhooks/n8n | sincronizacao e alertas. | Registrar falha, retry seguro, nao bloquear operacao principal quando possivel. |
| Calendario externo futuro | leitura/escrita de agenda. | Nao sobrescrever agenda CRM sem confianca; abrir conflito. |

## Estados padrao

| Estado | Significado |
| --- | --- |
| conectado | Integracao pronta. |
| degradado | Parcialmente funcional. |
| falhou | Ultima acao falhou. |
| aguardando provedor | Sem confirmacao ainda. |
| credencial invalida | Precisa reconectar. |
| rate limited | Provedor limitou. |
| reprocessando | Retry seguro em andamento. |
| bloqueado | Nao pode continuar sem acao humana. |

## Regras de retry

- Toda tentativa externa precisa idempotencyKey.
- Retry automatico so para erro temporario.
- Erro de permissao/credencial vira tarefa/configuracao.
- Erro que pode duplicar cobranca, mensagem ou registro exige revisao humana.

## Fallback por area

| Area | Fallback |
| --- | --- |
| WhatsApp falhou | tarefa manual, novo canal se permitido, aviso no Inbox. |
| Pagamento sem confirmacao | status em analise, nao marcar pago, pedir comprovante/revisao. |
| IA indisponivel | modo manual/copiloto simples, sem executar acao autonoma. |
| Importacao falhou | relatorio de erros, continuar com dados validos, revisar pendencias. |
| Exportacao falhou | retry, suporte, manter pedido auditado. |
| Billing falhou | nao liberar recurso pago sem confirmacao; exibir estado seguro. |

## Telas obrigatorias

- Integracoes/status;
- logs de integracao;
- Hoje para falhas criticas;
- Operacao/incidentes;
- Inbox/falhas de envio;
- Financeiro/casos;
- Importacao/exportacao;
- mobile Integracoes/status.

## Aceite

Toda integracao critica deve definir:

- como testar;
- como detectar falha;
- como exibir no web;
- como exibir no app;
- qual fallback manual;
- se pode retry automatico;
- se gera incidente;
- se gera auditoria.
