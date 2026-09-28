# Governanca de mensagens, templates e notificacoes - PT-BR

> Status: Rodada 0 v0.1. Este documento define como mensagens e notificacoes devem ser controladas.

## Regra central

Toda mensagem externa automatica ou em massa precisa de canal, consentimento, template/regra, cota, aprovacao quando necessario e auditoria.

## Tipos de comunicacao

| Tipo | Exemplo | Regra |
| --- | --- | --- |
| Resposta individual | Aluno pergunta no WhatsApp. | Pode ser manual, copiloto ou autonomo se permitido. |
| Lembrete operacional | aula, reposicao, pagamento. | Precisa template/canal/janela e cota. |
| Cobranca | mensalidade, link, comprovante. | Financeiro controla; risco e tom importam. |
| Comunicado de turma | aula cancelada, feriado, sala. | Pode exigir aprovacao se afeta muitos. |
| Campanha/reativacao | ex-alunos, inativos, oferta. | Aprovacao, consentimento, cota e template. |
| Mensagem sensivel | reclamacao, privacidade, historico. | Preferir humano/copiloto; nunca autonomo sem regra clara. |
| Notificacao interna | tarefa, aprovacao, falha, cota. | Roteada por papel/preferencia. |

## Estados de template

```text
rascunho
  -> em revisao
  -> aprovado internamente
  -> aprovado pelo provedor quando necessario
  -> ativo
  -> pausado
  -> rejeitado
  -> arquivado
```

## Campos de template

- nome;
- canal;
- categoria;
- area;
- texto;
- variaveis permitidas;
- publico permitido;
- consentimento necessario;
- custo/categoria WhatsApp;
- aprovacao necessaria;
- versao;
- status;
- dono.

## Notificacoes internas

Devem respeitar:

- papel;
- fila;
- horario;
- prioridade;
- preferencia do usuario;
- risco;
- mobile vs web;
- nao duplicar alerta inutil.

## Bloqueios obrigatorios

| Bloqueio | Resultado |
| --- | --- |
| Opt-out | Nao enviar; registrar motivo. |
| Sem consentimento | Pedir validacao ou usar canal permitido. |
| Template rejeitado/pausado | Bloquear envio automatico. |
| Cota 100% | Criar tarefa manual ou pedir pacote. |
| Janela WhatsApp fechada | Usar template aprovado ou bloquear. |
| Publico invalido | Revisar segmento. |
| Mensagem sensivel | Pedir aprovacao/humano. |

## Aceite

Cada tela com envio deve mostrar:

- destinatario/publico;
- canal;
- template;
- custo/cota;
- consentimento;
- aprovacao se necessaria;
- status de envio;
- falha e retry seguro.
