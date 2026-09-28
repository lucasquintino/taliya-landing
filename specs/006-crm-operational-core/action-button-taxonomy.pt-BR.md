# Taxonomia de acoes e botoes - PT-BR

> Status: Rodada 0 v0.1. Este documento padroniza acoes para web, app, manual, copiloto e autonomo.

## Tipos de botao

| Tipo | Uso | Exemplos |
| --- | --- | --- |
| Primario | Acao principal da tela ou do estado atual. | Salvar, Aprovar, Enviar, Abrir chamada. |
| Secundario | Acao util sem concluir o fluxo. | Editar, Ver detalhes, Filtrar. |
| Destrutivo/sensivel | Pode causar perda, bloqueio, cancelamento ou risco. | Cancelar plano, Reembolsar, Excluir, Revogar acesso. |
| Contextual | Acao no item/lista/card. | Abrir aluno, Criar tarefa, Assumir. |
| IA/copiloto | Pede sugestao ou prepara acao. | Sugerir resposta, Preparar cobranca, Simular encaixe. |
| Autonomia | Liga, pausa ou executa fluxo permitido. | Ativar fluxo, Pausar automacao, Executar agora. |
| Pedido de revisao | Usuario sem permissao solicita alguem autorizado. | Pedir aprovacao, Pedir acesso, Solicitar revisao. |

## Verbos padrao

| Verbo | Significado |
| --- | --- |
| Abrir | Navegar para detalhe. |
| Criar | Novo objeto manual. |
| Editar | Alterar dado existente. |
| Salvar | Persistir rascunho/alteracao. |
| Publicar | Tornar politica/fluxo/template ativo. |
| Simular | Ver impacto sem executar. |
| Preparar | IA ou sistema monta proposta sem executar. |
| Aprovar | Autorizar proposta. |
| Rejeitar | Negar proposta com motivo. |
| Enviar | Mandar mensagem/documento aprovado. |
| Assumir | Humano passa a ser responsavel. |
| Pausar | Interromper automacao/fluxo/caso. |
| Retomar | Reativar item pausado. |
| Resolver | Encerrar caso/tarefa com resultado. |
| Reabrir | Voltar item encerrado para operacao. |
| Arquivar | Tirar da operacao sem apagar. |
| Reativar | Voltar registro arquivado/inativo. |

## Regras para acoes com IA

| Label | Modo | Regra |
| --- | --- | --- |
| Sugerir resposta | Copiloto | Nunca envia sem aprovacao. |
| Preparar acao | Copiloto | Mostra antes/depois, risco, custo e motivo. |
| Simular impacto | Manual/copiloto | Nao altera dado real. |
| Executar agora | Autonomo permitido | Exige preflight, cota, permissao e auditoria. |
| Pausar agente | Manual | Sempre disponivel para dono/admin e operadores em emergencia contextual. |
| Reprocessar seguro | Manual/copiloto | Exige idempotencia e explicacao do que sera refeito. |

## Confirmacoes obrigatorias

| Acao | Confirmacao deve mostrar |
| --- | --- |
| Envio externo | destinatario, canal, template, custo/cota, consentimento. |
| Aprovacao financeira | valor, aluno, impacto, motivo, auditoria. |
| Alteracao de agenda em massa | aulas/alunos afetados, mensagem, reposicoes e rollback. |
| Mudanca de politica | versao atual, nova versao, vigencia, simulacao e rollback. |
| Ativar autonomia | fluxo, limite, cota, riscos, exemplos e fallback. |
| Exclusao/anonimizacao | identidade validada, objetos afetados, irreversibilidade e auditoria. |
| Acesso de suporte | escopo, prazo, motivo, pessoa/time Taliya e revogacao. |

## Estados de botao

| Estado | Comportamento |
| --- | --- |
| Ativo | Pode executar. |
| Desabilitado | Mostra tooltip/motivo. |
| Bloqueado por permissao | Mostra permissao necessaria e opcao pedir revisao. |
| Bloqueado por cota | Mostra cota, alternativa manual e pacote/upgrade quando permitido. |
| Bloqueado por dado | Mostra dado faltante e rota para corrigir. |
| Aguardando aprovacao | Mostra status e quem decide. |
| Executando | Evita duplo clique; usa idempotencia. |

## Regra de UX

Acao sensivel nunca deve ficar escondida sem explicacao quando for relevante para o trabalho do usuario. O produto deve dizer por que nao pode e qual o proximo caminho seguro.
