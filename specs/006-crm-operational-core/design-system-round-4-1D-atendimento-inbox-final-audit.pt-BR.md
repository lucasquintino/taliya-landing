# Auditoria Final - Rodada 4.1D - Atendimento / Inbox

> Status: auditoria v0.1. Escopo restrito ao que foi decidido nesta conversa: `/app/inbox`, `/app/conversas/[id]`, `/app/envios`, `/app/envios/[sendId]` e simplificacao de Contatos/Responsaveis/Grupos.

## Resultado

A parte de Atendimento/InBox esta fechada para web nesta rodada.

## Imagem Aprovada

| Imagem | Arquivo canonico | Status | Cobre |
| --- | --- | --- | --- |
| 24 | `24_round-4.1D_inbox_01_conversa-aberta.png` | Aprovada | `/app/inbox` e `/app/conversas/[id]`. |

Origem local conhecida:

`D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/24_round-4.1D_inbox_01_conversa-aberta.png.png`

Observacao:

O pacote tambem contem um arquivo antigo com prefixo `24_round-4.1C_checklists...`. Para Atendimento/InBox, o nome canonico correto e `24_round-4.1D_inbox_01_conversa-aberta.png`.

## Cobertura Por Rota

| Rota | Decisao | Imagem |
| --- | --- | --- |
| `/app/inbox` | Imagem propria aprovada. | 24 |
| `/app/conversas/[id]` | Herdada; abre conversa selecionada por URL. | 24 |
| `/app/envios` | Contrato textual; lista densa + detalhe lateral. | Sem imagem propria. |
| `/app/envios/[sendId]` | Contrato textual; detalhe de tentativa/envio. | Sem imagem propria. |
| `/app/contatos` | Removida como superficie principal nesta rodada. | Sem imagem. |
| `/app/contatos/[id]` | Removida como superficie principal nesta rodada. | Sem imagem. |
| `/app/responsaveis` | Removida como superficie principal nesta rodada. | Sem imagem. |
| `/app/grupos` | Removida como superficie principal nesta rodada. | Sem imagem. |

## Papel Da Pagina Inbox

Inbox responde:

> Quem esta falando com o studio, qual contexto eu preciso para responder bem, e quem controla essa conversa agora?

Nao deve virar:

- kanban;
- dashboard;
- lista de tarefas;
- CRM completo do aluno;
- pagina de contatos;
- console de agentes.

## Ciclo Coerente

1. Mensagem chega por canal.
2. CRM cria/atualiza conversa.
3. Sistema tenta identificar aluno ou interessado.
4. Conversa entra em fila/status.
5. Humano responde manualmente ou usa sugestao do copiloto.
6. Se precisar acompanhar, cria tarefa.
7. Se travar fluxo ou cruzar areas, aparece em Operacao.
8. Se for sensivel, vira aprovacao ou exige permissao.
9. Conversa encerra, reabre ou aguarda retorno.

## Modos E Agentes

| Contexto | Cobertura |
| --- | --- |
| 0 agentes | Manual completo: responder, assumir, criar tarefa, abrir perfil, registrar opt-out. |
| 1 agente | Copiloto somente se Atendimento estiver ativo. |
| 3 agentes | Atendimento normalmente ativo no bundle; sugestao e resumo aparecem. |
| 7 agentes | Todos os dominios podem enriquecer contexto, respeitando permissao, cota, politica e risco. |
| Manual | Caminho principal sempre existe. |
| Copiloto | Sugere resposta, resumo e proxima acao. |
| Autonomo | So responde se identidade, consentimento, cota, politica, canal e risco estiverem OK. |

## Variacoes Cobertas Sem Nova Imagem

A imagem 24 cobre a arquitetura. As variacoes abaixo mudam badges, banners, disabled states e acoes, mas nao exigem nova imagem agora:

- manual puro;
- copiloto sugeriu;
- autonomo ativo;
- autonomo bloqueado;
- aguardando humano;
- agente pausado;
- sem consentimento/opt-out;
- identidade incerta;
- telefone compartilhado;
- falha de envio;
- conversa financeira;
- conversa sensivel.

## Simplificacao De Contatos

Decisao fechada nesta conversa:

- nao criar pagina principal de Contatos;
- nao criar pagina propria de Responsaveis;
- nao criar pagina propria de Grupos/familias;
- nao modelar relacionamento entre alunos;
- manter apenas aluno, responsavel do aluno, interessado e canal de contato.

Regra operacional:

- aluno matriculado: resolver em Alunos;
- pessoa ainda nao matriculada: resolver em Interessados/Vendas;
- pessoa falando agora: resolver no Inbox;
- erro de dado: tratar como problema de dados.

## Pendencias E Riscos

| Item | Impacto | Encaminhamento |
| --- | --- | --- |
| A imagem 24 ainda mostra `Contatos` na navegacao superior. | Baixo para esta rodada, porque a tela ja foi aprovada visualmente. | Documento define `Contatos` como atalho temporario/contextual, nao pagina principal. Em implementacao, preferir remover ou trocar por atalho para Alunos/Interessados conforme decisao final. |
| `/app/envios` nao tem imagem propria. | Baixo agora. | Gerar imagem apenas se falhas/tentativas de envio virarem fluxo visual central. |
| Historico, Alunos e Professores nao foram auditados aqui. | Fora de escopo desta auditoria. | Resolver nas outras conversas/familias correspondentes. |

## Conclusao

Para esta rodada web, Atendimento/InBox esta suficientemente coberto com 1 imagem aprovada e contratos textuais para rotas derivadas. Nao ha necessidade de gerar imagens adicionais para `/app/conversas/[id]`, `/app/envios`, `/app/envios/[sendId]`, Contatos, Responsaveis ou Grupos.
