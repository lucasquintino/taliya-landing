# Auditoria De Cobertura Dos Componentes Do Design System

> Status: auditoria v0.1 apos Rodadas 1, 2B, 3A e 3B.1-3B.5. Objetivo: verificar se os componentes aprovados cobrem as 38 superficies, os 157 casos de uso e os modos manual/copiloto/autonomo.

## Veredito

Os componentes aprovados sao suficientes para iniciar a geracao das paginas web v0.1 com boa consistencia visual.

Eles ainda nao sao suficientes para considerar o design system 100% fechado para todo o produto.

O que falta nao e mais "botao", "input" ou "card" generico. O que falta sao **componentes compostos de dominio**, ou seja, componentes que juntam regras de negocio reais com interface:

- importacao e duplicidades;
- perfil completo de aluno/contato;
- turma, chamada, reposicao e lista de espera;
- documentos, contratos e comprovantes;
- simulacao financeira;
- fluxo/configuracao profunda de agente;
- execucao/trace/incidente de agente;
- auditoria antes/depois;
- privacidade/LGPD;
- relatorios avancados;
- comunicados/segmentos;
- mobile design system.

## O Que Ja Esta Bem Coberto

| Area | Cobertura atual | Rodadas |
| --- | --- | --- |
| DNA visual, cores, radius, sombras, tipografia | Coberto | 1, 1.1 |
| App shell web | Coberto | 2B |
| Botoes, nav, sidebar, avatares, badges, cards, conectores | Coberto | 3A |
| Inputs, formularios, filtros, busca | Coberto | 3B.1 |
| Modal, drawer, popover, toast, empty/loading/error | Coberto | 3B.2 |
| Tabela, lista, kanban, calendario compacto, timeline, atividade | Coberto | 3B.3 |
| Inbox, conversa, composer, copiloto, aprovacao, execucao, handoff | Coberto | 3B.4 |
| Plano, cotas, permissoes, integracoes, billing, auditoria, politicas | Coberto no nivel componente | 3B.5 |

## Cobertura Por Familia De Produto

| Familia | Componentes suficientes? | Observacao |
| --- | --- | --- |
| Hoje / comando diario | Sim para v0.1 | Usa cards, listas, resumo, atividade, alertas, cotas e aprovacoes. |
| Inbox / conversas | Sim para v0.1 | 3B.4 cobre bem. Falta aprofundar anexos/templates em rodada futura se necessario. |
| Alunos / contatos | Parcial | Falta componente de perfil operacional e timeline sensivel; responsaveis/familia e consentimentos como modulos proprios ficaram fora do MVP. |
| Agenda / turmas / aulas / chamada | Parcial | Calendario compacto existe, mas faltam turma, roster de chamada, capacidade, vagas e encaixe. |
| Reposicoes / lista de espera | Parcial | Falta matcher visual de candidatos, ranking, conflito e convite. |
| Vendas / interessados / experimental | Sim para v0.1 | Kanban, lista, conversa, formulario e timeline cobrem. Falta detalhe de funil por origem/campanha. |
| Matriculas | Parcial | Falta checklist de matricula com contrato, pagamento e primeira aula. |
| Financeiro / pagamentos / cobrancas | Parcial | Tabelas e billing existem, mas faltam comprovante, conciliacao, simulacao e impacto financeiro. |
| Retencao / cancelamento / reclamacoes | Sim para v0.1 | Cards, timeline, conversa, aprovacao e risco cobrem. Falta playbook/salvamento detalhado. |
| Operacao / tarefas / aprovacoes | Sim para v0.1 | Jornada, kanban, lista, modal, aprovacao e status cobrem bem. |
| Agentes / fluxos / execucoes | Parcial | 3B.4 cobre agente na comunicacao; falta console tecnico-operacional de fluxo, trace e simulacao. |
| Uso / cotas / economia | Sim para v0.1 | 3B.5 cobre plano, cota, limite e fallback. Falta extrato detalhado de uso. |
| Relatorios / exportacoes | Parcial | Cards e tabela cobrem, mas faltam graficos avancados e job de exportacao/agendamento. |
| Configuracoes / politicas | Parcial | Formularios, toggles e politicas cobrem base. Falta diff/versionamento e impacto antes/depois. |
| Integracoes | Sim para v0.1 | 3B.5 cobre conectado/erro/reconectar. Falta log tecnico detalhado. |
| Auditoria / privacidade | Parcial | Existe tabela/log basico. Falta diff antes/depois, mascaramento, grant temporario e fluxo LGPD. |
| Assinatura / billing | Sim para v0.1 | 3B.5 cobre plano, fatura, pagamento, 0 agentes e upgrade. |

## Lacunas Obrigatorias Antes De Gerar Todas As Paginas Web

### 1. Onboarding, Importacao E Qualidade De Dados

Faltam componentes:

- stepper/wizard de setup;
- checklist de ativacao;
- progresso de importacao;
- mapeamento de colunas/campos;
- resolucao de duplicidade;
- comparador de registros;
- fila de conflitos de dados;
- estado "pode continuar depois".

Superficies afetadas:

- Onboarding e configuracao inicial;
- Qualidade de dados;
- Integracoes/importacao;
- Contatos;
- Alunos.

### 2. Perfil De Objeto E Relacionamentos

Faltam componentes:

- cabecalho de perfil de aluno/contato/professor/interessado;
- abas internas de perfil;
- faixa de status: plano, risco, inadimplencia, proxima aula;
- relacoes operacionais: telefone compartilhado, aluno vinculado e origem do contato;
- consentimento/preferencias de contato;
- timeline sensivel com bloqueio/permissao;
- resumo lateral do objeto.

Superficies afetadas:

- Alunos e perfil;
- Contatos;
- Historico do aluno;
- Professor e notas;
- Interessados.

### 3. Agenda, Turmas, Chamada E Reposicoes

Faltam componentes:

- calendario semanal completo;
- grade de turma;
- card de aula;
- roster/lista de chamada;
- marcador de presenca/falta/no-show;
- capacidade/vaga;
- lista de espera;
- matcher de encaixe/reposicao;
- conflito de sala/professor/recurso;
- simulacao de impacto de mudanca de horario.

Superficies afetadas:

- Agenda;
- Grade, turmas e eventos;
- Aula e chamada;
- Reposicoes e lista de espera;
- Recursos, feriados e disponibilidade.

### 4. Documentos, Contratos E Financeiro Profundo

Faltam componentes:

- viewer de documento/contrato;
- upload/anexo/dropzone;
- card de comprovante;
- linha de conciliacao;
- input de valor/moeda;
- status de assinatura/envio;
- simulador antes/depois financeiro;
- resumo de impacto;
- aprovacao financeira com motivo.

Superficies afetadas:

- Matriculas;
- Financeiro;
- Pagamentos e cobrancas;
- Excecoes financeiras sensiveis sem pagina propria;
- Contratos e documentos financeiros.

### 5. Agentes, Fluxos, Execucoes E Incidentes

Faltam componentes:

- builder de fluxo;
- cards de etapa de fluxo;
- configuracao de modo manual/copiloto/autonomo por fluxo;
- simulador de fluxo;
- preflight/checklist antes de publicar;
- trace de execucao;
- timeline de tool calls;
- custo/cota por execucao;
- incidente com causa, impacto e reprocessamento seguro;
- painel de qualidade/evals do agente;
- editor de template/prompt;
- matriz de ferramentas permitidas.

Superficies afetadas:

- Agentes e fluxos;
- Execucoes e incidentes de agentes;
- Uso, cotas e economia;
- Politicas operacionais;
- Aprovacoes.

### 6. Auditoria, Privacidade E Permissoes Sensibles

Faltam componentes:

- diff antes/depois;
- log detalhado por evento;
- mascaramento/revelar dado sensivel;
- grant de suporte com expiracao;
- solicitacao LGPD;
- checklist de validacao de identidade;
- estado de acesso temporario ativo;
- revisao juridica/privacidade.

Superficies afetadas:

- Auditoria;
- Privacidade e solicitacoes;
- Configuracoes;
- Historico do aluno;
- Excecoes financeiras sensiveis sem pagina propria;
- Reclamacoes e casos sensiveis.

### 7. Relatorios E Exportacoes

Faltam componentes:

- grafico de linha;
- grafico de barra;
- funil;
- ranking/lista comparativa;
- heatmap de ocupacao/capacidade;
- drilldown para origem;
- job de exportacao;
- exportacao agendada;
- estado exportando/pronto/falhou.

Superficies afetadas:

- Relatorios e exportacoes;
- Vendas e origens;
- Financeiro;
- Retencao;
- Uso/cotas;
- Agenda/capacidade.

### 8. Segmentos, Comunicados E Templates

Faltam componentes:

- construtor de segmento;
- audiencia elegivel/inelegivel;
- contador de consentimento;
- preview de mensagem;
- template editor;
- custo estimado de envio;
- aprovacao de comunicado;
- painel de falhas de envio por publico.

Superficies afetadas:

- Segmentos e comunicados;
- Vendas;
- Retencao;
- Inbox/conversas;
- Uso/cotas.

### 9. Busca Global, Command Palette E Notificacoes

Faltam componentes:

- busca global expandida;
- command palette;
- resultado agrupado por tipo;
- acoes rapidas dentro da busca;
- notification center;
- agrupamento por urgencia;
- marcar lida/priorizar;
- abrir origem.

Superficies afetadas:

- Todas as entradas principais;
- Hoje;
- Inbox;
- Operacao;
- Mobile.

## Lacuna Separada: Mobile Ainda Nao Esta Coberto

As rodadas atuais sao web.

O app mobile precisa de design system proprio. Nao basta adaptar os componentes web.

Faltam componentes mobile:

- mobile app shell;
- bottom tab bar;
- top bar compacta;
- busca global mobile;
- cards de Hoje;
- lista mobile densa;
- bottom sheet;
- action sheet;
- swipe actions;
- FAB/acao rapida;
- mobile filters;
- mobile form;
- mobile modal/confirmacao;
- mobile chat;
- composer mobile;
- mobile calendar/day agenda;
- turma mobile;
- chamada mobile;
- aprovacao mobile;
- cota/alerta mobile;
- configuracao rapida de agente mobile;
- offline/erro/retry mobile se aplicavel.

Sem isso, nao devemos dizer que o design system completo web+app esta fechado.

## Componentes Que Nao Precisam De Nova Rodada Agora

Nao parece necessario criar novas rodadas para:

- botao;
- nav;
- sidebar;
- card basico;
- input;
- select;
- filtro;
- modal;
- toast;
- tabela generica;
- kanban generico;
- chat basico;
- card de plano/cota basico.

Eles ja estao cobertos.

## Recomendacao

Antes de gerar paginas web finais, fazer mais 3 rodadas curtas:

1. **Rodada 3C.1 - Objetos, Setup E Dados**
   - onboarding, importacao, duplicidades, perfil, relacoes, consentimento.

2. **Rodada 3C.2 - Agenda, Financeiro E Documentos**
   - turmas, chamada, reposicoes, documentos, comprovantes, simulacao financeira.

3. **Rodada 3C.3 - Agentes Avancados, Auditoria E Relatorios**
   - flow builder, simulacao, trace, incidentes, diff, LGPD, relatorios e exportacoes.

Depois disso:

4. **Rodada 4 - Paginas Web Por Familia**
   - gerar as paginas reais usando os componentes aprovados.

5. **Rodada 5 - Design System Mobile**
   - criar base visual mobile separada.

6. **Rodada 6 - Telas Mobile Por Familia**
   - gerar telas do app para rotina diaria.

## Conclusao

O kit atual cobre aproximadamente:

- componentes web genericos: alto;
- componentes web operacionais: bom;
- componentes web de agentes basicos: bom;
- componentes web administrativos basicos: bom;
- componentes compostos de dominio: parcial;
- mobile: ainda nao coberto.

Portanto:

```text
Suficiente para comecar paginas web v0.1: sim.
Suficiente para dizer que todas as paginas/telas/fluxos/casos estao 100% cobertos: ainda nao.
```
