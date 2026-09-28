# Auditoria de profundidade do produto - Taliya CRM

> Status: auditoria de produto. Este documento usa a matriz de 157 casos para decidir profundidade: o que vira tela grande, caso, botao, painel, configuracao, relatorio, app mobile, automacao ou trava.

## Veredito executivo

O produto deve ser profundo, mas nao deve ser espalhado.

A tese correta nao e:

```text
157 casos = 157 telas
```

A tese correta e:

```text
157 casos = CRM completo
organizado em poucos workspaces fortes
com muitas acoes contextuais
e agentes atuando dentro desses workspaces
```

O mapa atual mostra que Taliya deve ter profundidade real em operacao diaria, agenda, atendimento, financeiro, aluno/historico, retencao e agentes. Mas deve controlar profundidade em administracao, relatorios, exportacoes, recursos, disponibilidade de professor e configuracoes avancadas.

## Resumo da matriz

Fonte: `product-depth-matrix.pt-BR.csv`.

| Visao | Resultado |
| --- | ---: |
| Casos totais avaliados | 157 |
| Incluir completo o suficiente para operar | 104 |
| Incluir com trava forte | 32 |
| Incluir enxuto | 16 |
| Incluir como caso/trava; agente depois | 2 |
| Incluir absorvido por outro fluxo | 3 |

## Visao 1 - Profundidade de navegacao

| Tipo de profundidade | Total | Leitura de produto |
| --- | ---: | --- |
| Dentro de outra tela | 58 | A maioria dos casos deve viver como botao, painel ou acao contextual. Isso e bom. |
| Painel ou relatorio | 20 | Relatorios devem ser acionaveis, nao um BI pesado no inicio. |
| Configuracao web | 16 | Configuracao precisa existir, mas deve ser web-first. |
| Central de casos | 13 | Casos operacionais evitam criar uma tela separada para cada excecao. |
| Fila ou lista propria | 13 | Filas precisam ser escaneaveis e filtraveis. |
| Revisao/aprovacao | 12 | Aprovacoes sao um produto central, nao detalhe. |
| Tela propria | 10 | Poucos fluxos merecem tela propria. |
| Menu ou subarea propria | 6 | O menu principal deve ficar enxuto. |
| Sem tela propria | 5 | Bastidor com log, alerta ou tarefa. |
| Sem menu proprio | 3 | Casos absorvidos por outros fluxos. |
| Tela de simulacao | 1 | Simulacao de fluxo e essencial para agentes. |

### Decisao

O CRM web deve nascer com workspaces fortes, nao com menu enorme.

Menu principal recomendado:

| Item | Profundidade |
| --- | --- |
| Hoje | Profundo: prioridades, dinheiro, alertas e tarefas. |
| Inbox | Profundo: conversas, contatos, handoff e WhatsApp. |
| Alunos | Profundo: perfil, plano, agenda, historico permitido. |
| Agenda | Profundo: grade, aula, chamada, reposicao, espera. |
| Vendas | Profundo: interessados, experimental, matricula, origens. |
| Financeiro | Profundo, mas via casos/filtros: pagamentos, cobrancas, acordos, excecoes. |
| Operacao | Profundo: casos, tarefas, aprovacoes, incidentes. |
| Retencao | Medio/profundo: riscos, reclamacoes, cancelamento, reativacao. |
| Agentes | Profundo para configuracao, simulacao, execucao e incidentes. |
| Uso e cotas | Medio: cota, custos, alertas, limites. |
| Relatorios | Enxuto no inicio: paineis acionaveis, nao BI amplo. |
| Configuracoes | Web-first, agrupada, nao espalhada no menu. |

## Visao 2 - Profundidade de tela

### Telas profundas

Devem ter estado, filtros, detalhes, historico, permissoes e acoes:

- Hoje;
- Inbox/conversas;
- Aluno;
- Agenda/aula/chamada;
- Interessado/vendas;
- Financeiro/pagamentos/cobrancas;
- Operacao/casos/tarefas/aprovacoes;
- Reclamacoes;
- Agentes/fluxos/execucoes;
- Uso/cotas.

### Telas medias

Precisam existir, mas podem comecar compactas:

- Retencao;
- Relatorios;
- Integracoes;
- Auditoria;
- Segmentos;
- Comunicados;
- Checklists;
- Politicas operacionais.

### Telas enxutas

Devem nascer simples ou embutidas:

- faturas da Taliya;
- assinatura da Taliya;
- exportacoes;
- previsao de caixa;
- exportacao contabilidade;
- recursos/salas/equipamentos;
- disponibilidade de professores;
- relatorios administrativos avancados.

## Visao 3 - Profundidade por objeto de negocio

| Objeto | Profundidade recomendada |
| --- | --- |
| Aluno | Alta. E o centro do CRM. |
| Conversa | Alta. WhatsApp e atendimento dependem disso. |
| Aula/turma/presenca | Alta. Pilates vive da agenda. |
| Pagamento/plano/contrato | Alta, com travas. |
| Caso operacional | Alta. Une manual, sugestao e automacao. |
| Tarefa | Alta. Base plan e operacao humana dependem disso. |
| Aprovacao | Alta. E a trava central do copiloto. |
| Fluxo/agente/execucao | Alta. Sem isso nao existe agente confiavel. |
| Historico do aluno | Alta, mas com permissao forte. |
| Reclamacao | Alta, por reputacao e retencao. |
| Segmento/comunicado | Media. Importante, mas controlar profundidade. |
| Recurso/sala/equipamento | Enxuta no inicio, aprofundar se virar dor real. |
| Relatorio/metrica | Derivado e acionavel, nao BI independente agora. |
| Exportacao/backup | Enxuto, com permissao e auditoria. |

## Visao 4 - Profundidade de automacao

| Profundidade de automacao | Total | Decisao |
| --- | ---: | --- |
| Automacao simples permitida | 56 | Pode executar quando regra, cota, janela, consentimento e permissao estiverem ok. |
| Limitada com revisao | 34 | Pode preparar, mas envio externo, dinheiro ou mudanca operacional pede revisao. |
| Bloqueada para decisao sensivel | 33 | So pode detectar, alertar, bloquear, criar caso ou preparar revisao humana. |
| Manual + sugestao | 23 | Agente ajuda, humano decide. |
| Manual | 9 | Sem IA necessaria. |
| Manual com registro de auditoria | 1 | Exportacao/backup exige trilha. |
| Regra simples do sistema | 1 | Preferencia de notificacao nao precisa de agente. |

### Decisao

O produto deve vender agentes, mas a arquitetura deve vender confianca.

Autonomia profunda so deve existir para:

- lembretes de baixo risco;
- classificacao;
- resumo;
- alerta;
- criacao de tarefa;
- deteccao de bloqueio;
- respostas aprovadas e simples;
- atualizacoes internas reversiveis.

Autonomia nao deve decidir sozinha:

- reembolso;
- disputa;
- desconto/cortesia;
- bloqueio/liberacao;
- compartilhamento de historico sensivel;
- exclusao/anomimizacao LGPD;
- mudanca de permissao;
- mudanca de politica operacional;
- reclamacao sensivel;
- comunicacao em massa de risco.

## Visao 5 - Profundidade mobile

| Profundidade mobile | Total | Leitura |
| --- | ---: | --- |
| Mobile acao completa | 64 | Alto. Precisa ser agrupado em poucos fluxos de app. |
| Mobile aprovacao/consulta | 37 | Bom uso para gestor. |
| Mobile parcial | 12 | Adequado para apoio. |
| Web primeiro | 44 | Configuracao e administracao ficam no computador. |

### Decisao

O app mobile nao deve ter 64 telas completas. Ele deve ter 64 acoes possiveis agrupadas em poucos lugares:

- Hoje;
- Inbox;
- Agenda;
- Aula/chamada;
- Aluno;
- Professor/notas;
- Tarefas;
- Aprovacoes;
- Financeiro essencial;
- Reclamacoes/casos;
- Alertas de agente;
- Cotas/uso.

Mobile deve evitar:

- configuracao avancada de agentes; configuracao essencial entra no app;
- simulacao profunda de fluxo;
- politicas operacionais;
- integracoes;
- campos customizados;
- exportacoes;
- relatorios pesados.

## Visao 6 - Profundidade por area

| Area | Profundidade recomendada |
| --- | --- |
| Configuracao inicial | Profunda o suficiente para ativar o studio sem suporte constante. |
| Rotina diaria | Profunda. E a tela que vende recorrencia de uso. |
| Atendimento e contatos | Profunda. E onde WhatsApp e CRM se encontram. |
| Vendas e matriculas | Profunda. Precisa converter interessados em alunos. |
| Agenda e aulas | Muito profunda. E o core operacional do Pilates. |
| Financeiro | Profunda, mas organizada por casos/filtros. |
| Retencao e satisfacao | Media/profunda. Forte em risco, reclamacao e reativacao. |
| Historico do aluno | Profunda com permissao forte. |
| Agentes e automacoes | Profunda, mas web-first em configuracao. |
| Administracao e relatorios | Enxuta no inicio. Deve existir, mas sem virar ERP/BI. |
| Pontos a decidir | Em geral enxutos, absorvidos ou travas ate prova de uso. |

## Visao 7 - Profundidade de MVP

Como o objetivo declarado e incluir tudo no MVP, a forma correta de reduzir risco nao e tirar casos. E controlar profundidade.

| Camada | O que significa | Exemplos |
| --- | --- | --- |
| Completo o suficiente para operar | Fluxo principal funciona de ponta a ponta. | Inbox, agenda, vendas, pagamentos, casos. |
| Com trava forte | Existe no produto, mas nao automatiza decisao sensivel. | Historico, privacidade, reclamacao, suporte, financeiro sensivel. |
| Enxuto | Existe como tela simples, filtro, exportacao ou configuracao basica. | Relatorios, integracoes, recursos, exportacoes. |
| Caso/trava; agente depois | Existe como regra/caso, mas nao vira agente proprio ainda. | Primeira semana, anamnese/consentimento. |
| Absorvido | Nao vira item proprio. | Substituicao de professor, celebracao, revisao periodica. |

## Ajustes recomendados

### Adicionar

- Uma decisao de menu principal final.
- Uma matriz de workspaces: quais telas agregam quais casos.
- Uma matriz de estados por tela: vazio, carregando, bloqueado, sem permissao, erro, conflito, aguardando aprovacao.
- Uma matriz de permissoes por papel.
- Uma matriz de autonomia por fluxo.

### Ajustar

- Tratar 64 acoes mobile como acoes agrupadas, nao telas.
- Tratar financeiro como workspace de casos financeiros, nao muitas paginas soltas.
- Tratar relatorios como paineis acionaveis ligados a fluxo.
- Tratar recursos/salas/equipamentos como enxuto ate provar necessidade de profundidade.
- Tratar administracao como necessaria, mas nao como centro da experiencia.

### Remover ou evitar

- Evitar menu principal com mais de 10-12 entradas.
- Evitar tela propria para todo caso.
- Evitar modulo de BI pesado no MVP.
- Evitar app mobile administrativo.
- Evitar agente standalone para primeira semana e anamnese antes de provar configuracao independente.

## Proxima decisao

O proximo artefato deve ser:

```text
workspace-depth-map.pt-BR.md
```

Ele deve responder:

- quais sao os workspaces principais;
- quais casos entram dentro de cada workspace;
- quais viram abas;
- quais viram botoes;
- quais viram filtros;
- quais viram paineis laterais;
- quais aparecem no mobile;
- quais ficam so no web.

## Conclusao

Estamos no caminho certo de profundidade.

O produto nao parece raso demais. O risco agora e o oposto: ficar espalhado demais.

Recomendacao final desta auditoria:

```text
manter os 157 casos
mas consolidar em poucos workspaces profundos
com acoes contextuais e centrais de caso
```

Isso entrega um CRM completo com agentes integrados sem transformar o MVP em 157 telas.
