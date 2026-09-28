# Rodada 4.1F - Financeiro Web - Plano De Imagens

> Status: rascunho operacional. Decisao registrada em 12/05/2026 para orientar a geracao das proximas imagens web do Taliya CRM.

## Decisao De Arquitetura Visual

A familia Financeiro sera desenhada com quatro superficies no MVP: tres com imagem propria aprovada e uma herdada.

1. `/app/financeiro` - visao geral + filas principais.
2. `/app/financeiro/kanban` - operacao visual por estagio.
3. `/app/financeiro/movimentacoes` - tabela/lista completa de movimentacoes financeiras com filtros por tipo.
4. `/app/financeiro/documentos` - contratos, recibos, comprovantes e documentos financeiros, herdando componentes ja aprovados, sem imagem nova.

Cobrancas, conciliacao, promessas, falhas, comprovantes pendentes, estornos e excecoes financeiras sensiveis nao viram paginas soltas no MVP. Elas aparecem como filtros, filas, colunas, drawers, aprovacoes, tarefas ou encaminhamentos para Operacao/Aluno quando necessario.

Topbar final da familia Financeiro: `Visao geral`, `Kanban`, `Movimentacoes`, `Documentos`. A aba `Casos` nao existe no MVP.

## `/app/financeiro`

Objetivo: permitir que o gestor entenda a saude financeira do dia/semana e aja rapido, sem precisar abrir a tabela completa.

Conteudo principal:

- KPIs financeiros: recebido, previsto, vencido, em atraso e conciliacao pendente.
- Filas principais: vencem hoje, atrasados, comprovantes pendentes, falhas, promessas e excecoes.
- Lista curta de prioridades financeiras.
- Drawer contextual ao selecionar uma cobranca, pagamento ou pendencia.
- Acoes seguras: enviar lembrete, abrir conversa, confirmar pagamento com evidencia, criar tarefa, abrir aluno e exportar quando permitido.

Regra do drawer/painel direito:

- por padrao, `/app/financeiro` carrega com visao geral e filas, sem drawer obrigatoriamente aberto;
- imagem com drawer aberto representa estado selecionado, nao carregamento inicial da rota;
- o drawer muda conforme o item financeiro clicado;
- o drawer nao substitui Movimentacoes completas, Contratos, Alunos, Inbox ou Aprovacoes.

Modos principais do drawer financeiro:

| Item clicado | Drawer deve mostrar |
| --- | --- |
| Cobranca a vencer/vencida | Aluno, valor, vencimento, canal, historico curto, risco e acoes de lembrete, conversa, tarefa ou abrir aluno. |
| Pagamento confirmado | Evidencia, provedor/origem, conciliacao, recibo e acoes restritas de auditoria. |
| Comprovante pendente | Imagem/arquivo, valor esperado, divergencia, responsavel e acao humana de validar/rejeitar/pedir dados. |
| Falha de pagamento | Motivo, tentativa, proxima tentativa permitida, canal alternativo e criacao de tarefa se necessario. |
| Promessa de pagamento | Data prometida, conversa relacionada, risco, lembrete e proxima acao. |
| Excecao sensivel | Desconto, acordo, estorno, disputa ou liberacao; deve pedir aprovacao quando politica exigir. |

Imagens necessarias:

| Imagem | Nome | Objetivo |
| --- | --- | --- |
| 1 | `30_round-4.1F_financeiro_01_visao-geral-filas.png` | Estado normal da visao geral acima da dobra. Aprovada como central de filas financeiras. |
| 2 | `32_round-4.1F_financeiro_02_drawer-cobranca-selecionada.png` | Mesma pagina com drawer aberto para uma cobranca selecionada. Aprovada como estado selecionado da visao geral. |

### Decisao Da Imagem Aprovada

A imagem `30_round-4.1F_financeiro_01_visao-geral-filas.png` consolida a rota `/app/financeiro` como uma central operacional de filas, nao como dashboard gerencial.

Elementos aprovados:

- Topbar interna com `Visao geral`, `Kanban`, `Movimentacoes` e `Documentos`.
- Filtros de periodo com `Hoje`, `Esta semana` e `Este mes`.
- Filtros de unidade, status e responsavel.
- Bloco grande de `Prioridades financeiras` antes das filas.
- Filas com contadores e valores integrados no proprio bloco, sem linha separada de KPIs.
- Oito filas principais: a vencer, vencem hoje, pagos recentes, atrasados, falhas de pagamento, conciliacao pendente, promessas de pagamento e excecoes financeiras.
- Cada item de fila exibe aluno, valor, data/status, tipo/origem e seta para detalhe.

Nao pertence a esta imagem:

- Kanban completo.
- Tabela completa.
- Drawer aberto.
- Graficos, previsao avancada, fechamento financeiro ou analise gerencial.

### Decisao Da Imagem Com Drawer Aprovada

A imagem `32_round-4.1F_financeiro_02_drawer-cobranca-selecionada.png` documenta o comportamento de selecao dentro de `/app/financeiro`.

Ela cobre:

- clique em item de prioridade ou fila financeira;
- abertura de drawer lateral direito;
- detalhe de cobranca selecionada;
- resumo financeiro do item;
- contexto e historico recente;
- sugestao do copiloto quando Financeiro IA estiver disponivel;
- acoes seguras: enviar lembrete, abrir conversa, registrar promessa, marcar como pago, criar tarefa e abrir aluno.

Regras aprovadas para o drawer:

- o drawer nao e tela propria;
- o drawer deve preservar a pagina de filas como contexto;
- confirmacao de pagamento exige evidencia e permissao;
- acordo, desconto, estorno ou excecao sensivel devem encaminhar para aprovacao, tarefa, aluno, movimentacao ou operacao, conforme o tipo de decisao;
- com 0 agentes, o drawer continua manual e sem sugestao de IA;
- com agente Financeiro ativo, o copiloto pode resumir e redigir mensagem, mas nao aprova excecao sozinho.

## `/app/financeiro/kanban`

Objetivo: operar cobrancas e pendencias financeiras por etapa quando houver volume.

Colunas esperadas:

- A vencer.
- Vence hoje.
- Em atraso.
- Promessa de pagamento.
- Comprovante enviado.
- Conciliacao pendente.
- Resolvido.

Cada card deve mostrar aluno, valor, vencimento, atraso, canal, responsavel, risco, origem e ultima acao. O detalhe abre em drawer.

Imagem necessaria depois de fechar `/app/financeiro`:

- `33_round-4.1F_financeiro_03_kanban-financeiro.png`. Aprovada como kanban financeiro horizontal.

### Decisao Da Imagem Kanban Aprovada

A imagem `33_round-4.1F_financeiro_03_kanban-financeiro.png` documenta a rota `/app/financeiro/kanban`.

Ela cobre:

- board horizontal com colunas financeiras;
- cards unitarios por aluno/cobranca/pagamento;
- colunas com contador e valor total;
- cards compactos empilhados;
- area `+ Adicionar` por coluna;
- scroll horizontal do board;
- nenhum drawer aberto.

Filtros aprovados para o kanban:

| Filtro | Funcao |
| --- | --- |
| Hoje | Mostra itens com vencimento, pagamento, promessa, falha, comprovante ou resolucao relacionados ao dia atual. |
| Esta semana | Mostra itens financeiros com data de acao, vencimento, promessa ou resolucao dentro da semana atual. |
| Este mes | Mostra a operacao financeira do mes corrente, incluindo pendencias em aberto e eventos resolvidos no mes. |
| Unidade | Filtra por unidade/studio quando a conta tiver mais de uma unidade. Em conta de unidade unica, pode aparecer como filtro desabilitado ou com valor fixo. |
| Responsavel | Filtra pelo usuario/time responsavel por acompanhar a cobranca ou pendencia. Inclui Financeiro, Recepcao, Gestor, Sistema ou Agente quando aplicavel. |
| Tipo | Filtra a origem/natureza do item: mensalidade, plano trimestral, aula avulsa, Pix, cartao, boleto, WhatsApp, importacao, agente ou manual. |
| Status | Filtra o estado operacional sem mudar a coluna: agendado, hoje, atrasado, prometido, aguardando validacao, em conciliacao, resolvido, falhou. |

Regra de comportamento:

- os filtros reduzem os cards visiveis no board, mas nao mudam o significado das colunas;
- colunas vazias permanecem visiveis para preservar a leitura do fluxo;
- contadores e valores de cada coluna recalculam conforme filtros ativos;
- limpar filtros volta para o board completo do periodo selecionado;
- mover card entre colunas altera o status operacional do item e deve gerar auditoria.

## `/app/financeiro/movimentacoes`

Objetivo: consultar, filtrar, auditar e operar todos os registros e compromissos financeiros dos alunos. Esta pagina nao e somente pagamentos; ela cobre mensalidades, cobrancas, parcelas, pagamentos recebidos, falhas, promessas, comprovantes, conciliacao, estornos, descontos e ajustes.

Regra de produto: movimentacoes financeiras precisam respeitar o contrato `billing-lesson-consumption-models.pt-BR.md`. A pagina deve deixar claro se o item veio de mensalidade, pacote de aulas, aula avulsa, contrato parcelado, pagamento recebido, ajuste ou excecao, sem misturar credito operacional sem valor com dinheiro cobrado.

Filtros obrigatorios:

- Periodo: hoje, esta semana, este mes e personalizado.
- Tipo de movimentacao: mensalidade, cobranca avulsa, parcela, pagamento recebido, promessa, falha, estorno, desconto, ajuste, conciliacao e comprovante.
- Status: previsto, a vencer, vence hoje, pago, atrasado, falhou, aguardando comprovante, aguardando conciliacao, prometido, estornado e cancelado.
- Aluno.
- Plano: mensal, trimestral, pacote, experimental e aula avulsa.
- Modelo de cobranca/consumo quando aplicavel: mensalidade fixa, frequencia, pacote, recorrente com creditos, aula avulsa, contrato parcelado ou customizado.
- Turma.
- Metodo: Pix, cartao, boleto, dinheiro, transferencia e manual.
- Origem: sistema, importacao, WhatsApp, agente, usuario e integracao.
- Responsavel.
- Valor.
- Vencimento.
- Data de pagamento.
- Conciliacao: conciliado, pendente, divergente e sem identificacao.
- Comprovante: sem comprovante, enviado, em analise, aprovado e rejeitado.
- Risco/permissao: normal, exige revisao, bloqueado por politica e sensivel.

Filtros rapidos:

- A vencer.
- Vence hoje.
- Atrasados.
- Pagos.
- Falhas.
- Promessas.
- Comprovantes pendentes.
- Conciliacao pendente.
- Excecoes.
- Criados por agente.
- Exigem acao humana.

Imagem necessaria depois do kanban:

- `34_round-4.1F_financeiro_04_movimentacoes-filtros-drawer.png`. Aprovada como lista completa de movimentacoes com filtros rapidos e drawer contextual.

### Decisao Da Imagem Movimentacoes Aprovada

A imagem `34_round-4.1F_financeiro_04_movimentacoes-filtros-drawer.png` documenta a rota `/app/financeiro/movimentacoes`.

Ela cobre:

- busca ampla por aluno, ID, telefone, cobranca ou movimentacao;
- filtros superiores por periodo, tipo de movimentacao, status, plano, metodo, responsavel e mais filtros;
- coluna lateral esquerda de filtros rapidos;
- tabela central de movimentacoes;
- drawer direito aberto com detalhe de uma mensalidade a vencer;
- acoes seguras no drawer.

Filtros rapidos aprovados na lateral:

| Filtro | Funcao |
| --- | --- |
| Todas | Mostra todas as movimentacoes dentro dos filtros ativos. |
| A vencer | Mensalidades, parcelas, cobrancas ou aulas avulsas futuras. |
| Recebidos hoje | Pagamentos recebidos no dia atual. Microcopy final recomendada: `Pagos hoje` ou `Recebidos hoje`. |
| Atrasadas | Movimentacoes vencidas sem pagamento confirmado. |
| Promessas | Promessas de pagamento ativas. |
| Falhas | Falhas de cartao, Pix, boleto, gateway ou envio. |
| Conciliacao pendente | Pagamentos/comprovantes que precisam vinculo ou validacao. |
| Comprovantes | Comprovantes enviados ou em analise. |
| Estornos | Reembolsos, estornos ou disputas. |
| Ajustes | Ajustes manuais financeiros. |
| Descontos | Descontos aprovados ou pendentes. |

Filtros que permanecem previstos mesmo sem aparecer na primeira imagem:

- Criados por agente;
- Exigem acao humana;
- Sensivel/bloqueado por politica;
- Divergente;
- Sem identificacao.

Tabela aprovada:

| Coluna | Papel |
| --- | --- |
| Aluno | Pessoa ligada a movimentacao. |
| Tipo | Mensalidade, pagamento recebido, cobranca atrasada, falha de cartao, promessa, conciliacao, comprovante, estorno, desconto ou ajuste. |
| Status | A vencer, pago, em atraso, falha, prometido, pendente, em analise, estornado, aprovado ou ajustado. |
| Valor | Valor financeiro da movimentacao. |
| Vencimento | Data de vencimento ou marco relevante. |
| Plano | Plano mensal, premium, trimestral, aula avulsa ou outro modelo configurado. |
| Metodo | Pix, cartao, WhatsApp, manual, importacao ou gateway. |
| Origem | Sistema, WhatsApp, agente, importacao, coordenacao ou financeiro. |
| Responsavel | Time ou pessoa responsavel pela tratativa. |
| Ultima atividade | Ultima acao relevante. |
| Acoes | Menu contextual. |

Drawer aprovado para mensalidade a vencer:

- tipo e status;
- aluno;
- resumo com valor, vencimento, plano, metodo, origem, responsavel e canal sugerido;
- contexto;
- historico recente;
- sugestao do copiloto quando permitido;
- acoes: enviar lembrete, copiar link Pix, abrir conversa, criar tarefa, marcar como pago e abrir aluno.

Regras de comportamento:

- a pagina pode abrir sem drawer; a imagem representa estado com item selecionado;
- cada tipo de movimentacao pode abrir um drawer proprio;
- confirmar pagamento exige permissao e evidencia quando aplicavel;
- desconto, estorno, acordo, ajuste sensivel e excecao financeira podem encaminhar para aprovacao, tarefa, aluno, movimentacao ou operacao;
- a coluna lateral nao substitui os filtros superiores: filtros rapidos definem fila, filtros superiores refinam a consulta;
- creditos operacionais sem valor financeiro nao devem aparecer como dinheiro cobrado, exceto quando houver ajuste financeiro relacionado.

## `/app/financeiro/documentos`

Objetivo: consultar, anexar, auditar e operar documentos financeiros vinculados a alunos, planos, cobrancas, pagamentos e contratos, sem criar uma tela visual nova nesta rodada.

Esta rota e uma aba herdada da familia Financeiro. Ela usa o App Shell aprovado, a mesma topbar da familia e componentes ja aprovados em `3C.2`, `3B.3`, `3B.2` e `3C.3`.

Conteudo esperado:

- busca por aluno, documento, contrato, recibo, nota, comprovante, ID ou telefone;
- filtros por tipo, status, aluno, plano, origem, periodo, assinatura/envio e permissao;
- lista/tabela de documentos financeiros;
- detalhe contextual em drawer ou painel lateral;
- preview quando o arquivo permitir;
- historico curto de envio, assinatura, download, anexo, erro e auditoria;
- vinculo com aluno, movimentacao financeira, contrato ou tarefa;
- permissao clara para baixar, reenviar, anexar, solicitar assinatura, cancelar rascunho ou arquivar.

Tipos cobertos:

- contrato;
- termo;
- recibo;
- nota;
- comprovante;
- anexo financeiro;
- documento de ajuste ou acordo aprovado;
- arquivo importado/manual.

Estados:

- rascunho;
- enviado;
- visualizado;
- assinado;
- pendente;
- vencido;
- cancelado;
- arquivado;
- erro de envio;
- sem permissao.

Acoes:

- ver;
- reenviar;
- anexar;
- baixar quando permitido;
- abrir aluno;
- abrir movimentacao relacionada;
- criar tarefa;
- solicitar assinatura ou revisao;
- cancelar rascunho;
- arquivar;
- auditar.

Nao pertence a esta rota:

- resolver cobranca em aberto;
- aprovar desconto, acordo, estorno ou excecao sensivel;
- operar kanban financeiro;
- substituir a tabela completa de movimentacoes;
- virar pagina propria de casos financeiros.

Decisao visual: nao gerar imagem nova para `/app/financeiro/documentos` no MVP. A rota herda:

- viewer/upload/anexo/comprovante de `3C.2`;
- tabela/lista de `3B.3`;
- drawer/modal/confirmacao de `3B.2`;
- auditoria/log/diff de `3C.3`;
- shell e topbar final da familia Financeiro.

## Excecoes Financeiras Sensiveis No MVP

Casos de desconto, acordo, estorno, disputa, pausa, cortesia, bloqueio/liberacao e alteracao de plano nao terao pagina propria no MVP.

Nao gerar imagem nem rota dedicada de `Casos financeiros` nesta rodada. A resolucao deve acontecer nas superficies existentes:

- `/app/financeiro`: prioridades, filas e drawer contextual;
- `/app/financeiro/kanban`: card movido por etapa e drawer do card;
- `/app/financeiro/movimentacoes`: tabela completa, filtros rapidos, auditoria e drawer;
- `/app/aprovacoes`: decisoes que exigem revisao humana;
- `/app/tarefas`: trabalho humano com prazo/dono;
- `/app/alunos/[id]`: contexto do aluno, plano e historico;
- `/app/operacao`: incidente ou bloqueio operacional que cruza areas.

## Regras De IA E Permissao

- Plano com 0 agentes: financeiro continua manual e programatico.
- Financeiro com agente: IA pode priorizar, resumir, redigir lembretes e preparar aprovacoes.
- Modo copiloto: sugere acao e aguarda revisao.
- Modo autonomo: apenas lembretes simples permitidos por politica.
- Sempre humano: desconto, acordo, estorno, disputa, bloqueio/liberacao, cortesia, perdao de divida e alteracao sensivel de plano.
