# Design System Web - Rodada 3C.3 - Agentes Avancados, Auditoria E Relatorios

> Status: biblioteca visual v0.1 aprovada. Esta rodada cobre componentes compostos de fluxos, execucoes, governanca, privacidade, relatorios e exportacoes.

## Objetivo

Fechar lacunas de dominio ligadas a agentes avancados, auditoria e relatorios:

- builder de fluxo;
- configuracao de modo por fluxo;
- simulador de fluxo;
- preflight antes de publicar;
- trace de execucao;
- incidente de agente;
- painel de qualidade/evals;
- diff antes/depois;
- log detalhado/auditoria;
- privacidade/LGPD;
- grant de suporte;
- relatorios avancados;
- exportacoes;
- segmentos e comunicados.

## Decisao

A imagem da Rodada 3C.3 fica aprovada como v0.1.

Ela acertou:

- criou builder de fluxo com gatilho, condicao, acao, aprovacao e fallback manual;
- diferenciou modo manual, copiloto, autonomo e bloqueios por politica/plano/cota;
- incluiu simulador de fluxo com entrada, resultado, risco, custo e tempo;
- criou preflight antes de publicar;
- trouxe trace de execucao com ferramenta, status, duracao, custo e erro;
- incluiu incidente com causa, impacto, objeto afetado, fallback e reprocessamento seguro;
- incluiu qualidade/evals com sucesso, falhas, revisao humana e confianca;
- cobriu diff antes/depois e log detalhado;
- incluiu LGPD, grant de suporte, relatorios, exportacoes, segmentos e comunicados.

## Ressalvas

- A prancha e muito densa; paginas finais devem separar fluxo, auditoria, relatorio e privacidade.
- O builder de fluxo precisa de versao focada em legibilidade quando houver muitos passos.
- "Aprovar publicacao" e acao sensivel: sempre exige preflight, permissao e auditoria.
- Trace de execucao deve evitar linguagem tecnica demais para gestor.
- Relatorios avancados nao devem virar dashboard generico; precisam abrir origem e acao.
- Segmentos/comunicados exigem consentimento, custo estimado e aprovacao.
- Ainda pode faltar, em rodada futura, uma matriz especifica de ferramentas permitidas por agente/fluxo e um editor profundo de template/prompt.

## Componentes Aprovados

| Componente | Uso principal |
| --- | --- |
| Builder de fluxo | Configuracao visual de automacoes e jornadas. |
| Modo por fluxo | Manual, copiloto, autonomo e bloqueios. |
| Simulador de fluxo | Teste antes de publicar ou alterar. |
| Preflight | Dados, permissao, cota, politica e status geral. |
| Trace de execucao | Passos, ferramentas, custo, duracao e erro. |
| Incidente de agente | Causa, impacto, fallback e reprocessamento. |
| Qualidade/evals | Sucesso, falhas, revisao humana e confianca. |
| Diff antes/depois | Mudancas sensiveis e reversao. |
| Log detalhado/auditoria | Ator, objeto, acao, origem, horario e status. |
| Privacidade/LGPD | Validar, exportar, anonimizar, negar e acompanhar. |
| Grant de suporte | Acesso temporario, escopo, expiracao e revogacao. |
| Relatorios avancados | Linha, barra, funil, ranking e heatmap. |
| Exportacoes | Job, agendamento, progresso, pronto/falha e download. |
| Segmentos/comunicados | Audiencia, consentimento, preview, custo e aprovacao. |

## Regras De Uso

- Fluxo autonomo deve mostrar por que esta permitido ou bloqueado.
- Toda publicacao de fluxo precisa de preflight.
- Reprocessamento deve ser seguro e idempotente.
- Incidente precisa mostrar fallback manual.
- Diff antes/depois deve aparecer em acao sensivel.
- Relatorio precisa abrir origem, caso, aluno, turma ou fluxo relacionado.
- Segmento/comunicado precisa validar consentimento antes de envio.
- Grant de suporte deve expirar e ser revogavel.

## Nao Fazer

- Nao criar agente como produto separado.
- Nao publicar fluxo sem mostrar risco/cota/politica.
- Nao esconder custo ou cota de execucao.
- Nao mostrar auditoria como log tecnico incompreensivel.
- Nao deixar LGPD parecendo tarefa comum.
- Nao usar relatorio como decoracao sem acao operacional.

