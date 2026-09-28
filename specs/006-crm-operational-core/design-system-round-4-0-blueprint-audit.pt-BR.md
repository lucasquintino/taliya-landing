# Auditoria - Rodada 4.0 - Blueprint Web

> Status: auditoria tecnica e de usuario apos blueprint v0.1. Objetivo: validar se as paginas web conseguem suportar os casos de uso, fluxos, documentos e componentes ja definidos para o CRM web.

## Resultado

O blueprint web esta coerente para gerar as paginas v0.1 do CRM web.

Validado contra:

- 38 superficies funcionais do contrato final;
- 157 casos de uso mapeados;
- modos manual, copiloto e autonomo;
- variacoes de plano com 0, 1, 3 e 7 agentes;
- componentes das rodadas 1, 2B, 3A, 3B.1-3B.5 e 3C.1-3C.3;
- necessidades de gestor de studio no uso diario.

## Checks Tecnicos

| Check | Resultado |
| --- | --- |
| 38 paginas/superficies no blueprint | OK |
| Todas as paginas tem componentes definidos | OK |
| Todas as paginas tem estados definidos | OK |
| Todas as paginas tem regra de IA/plano/cota | OK |
| App shell web consistente com referencia aprovada | OK |
| Componentes compostos cobrem dominio operacional | OK |
| Cotas, permissao, auditoria e fallback aparecem nas areas sensiveis | OK |
| CRM continua usavel com 0 agentes | OK |
| Manual/copiloto/autonomo aparecem nas paginas onde fazem sentido | OK |

## Checks Como Gestor De Studio

| Necessidade do gestor | Cobertura |
| --- | --- |
| Comecar o sistema sem agentes | Coberto por Onboarding, Hoje, Agenda, Alunos, Financeiro, Configuracoes e Billing. |
| Configurar ou reconfigurar agentes depois do setup | Coberto por Agentes/Fluxos, Politicas, Uso/Cotas, Execucoes/Incidentes e Auditoria. |
| Resolver o dia a dia sem IA | Coberto: todas as paginas mantem acao manual. |
| Pedir ajuda da IA sem perder controle | Coberto: copiloto aparece em conversa, aprovacao, fluxo, agenda, financeiro, retencao e operacao. |
| Permitir autonomia somente com seguranca | Coberto: areas sensiveis exigem politica, permissao, cota, auditoria e fallback. |
| Ver ocupacao, vagas, turmas e recursos | Coberto por Agenda, Grade/Turmas/Eventos, Aula/Chamada, Reposicoes e Recursos. |
| Controlar dinheiro, cobrancas e contratos | Coberto por Financeiro, Pagamentos, Casos Financeiros e Contratos. |
| Enxergar problemas e excecoes | Coberto por Hoje, Operacao, Tarefas, Aprovacoes, Incidentes, Auditoria e Relatorios. |
| Proteger dados sensiveis | Coberto por Historico, Privacidade, Permissoes, Auditoria e LGPD. |

## Ajustes Aplicados Nesta Auditoria

1. Clarificada a propriedade de paginas para evitar duplicidade:
   - `/app/recursos` agora pertence formalmente a Recursos/Feriados/Disponibilidade.
   - Grade/Turmas/Eventos usa recurso apenas como contexto, filtro, conflito e impacto.
   - `/app/importacao` pertence a Integracoes no uso recorrente e aparece no Onboarding apenas como etapa guiada.
   - Segmentos/Comunicados, Aprovacoes, Tarefas, Auditoria, Uso e Privacidade foram declaradas como superficies proprias.

2. Ajustado Inbox/Conversas:
   - adicionada dependencia explicita de anexos/upload de `3C.2`.

3. Ajustado Pagamentos/Cobrancas:
   - adicionada permissao financeira de `3B.5`.

4. Ajustado Segmentos/Comunicados:
   - adicionados filtros/forms de `3B.1`, porque construtor de publico e template precisam de controles de entrada.

## Lacunas Que Nao Bloqueiam A Geracao Web V0.1

Esses pontos podem virar rodadas futuras de refinamento, mas nao impedem gerar as paginas web:

- busca global agrupada com resultado por aluno, conversa, aula, pagamento, tarefa e fluxo;
- central de notificacoes completa, alem dos alertas/topbar/Hoje;
- editor mais profundo de comunicados com variaveis, preview multi-canal e validacao avancada;
- matriz visual de permissoes em nivel mais granular;
- biblioteca final de microcopy por estado vazio, erro, bloqueio e acao sensivel.

## Decisao

Podemos seguir para prompts de geracao das paginas web por familia.

Nao devemos gerar todas as 38 paginas de uma vez. A ordem recomendada e:

1. App shell + Hoje + Operacao;
2. Inbox + Conversas + Agentes em contexto;
3. Agenda + Grade + Turmas + Aula + Reposicoes + Recursos;
4. Alunos + Contatos + Historico + Qualidade de Dados;
5. Financeiro + Pagamentos + Contratos + Excecoes;
6. Vendas + Interessados + Experimental + Matriculas + Retencao;
7. Agentes + Fluxos + Execucoes + Incidentes + Politicas;
8. Relatorios + Auditoria + Privacidade + Configuracoes + Billing.

