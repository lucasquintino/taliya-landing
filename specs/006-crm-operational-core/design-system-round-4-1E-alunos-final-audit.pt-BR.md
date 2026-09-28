# Auditoria Final - Rodada 4.1E - Alunos

> Status: aprovada v0.1. Esta auditoria fecha a familia Alunos web apos as imagens 27 e 28 e a decisao de escopo que remove responsaveis/familia e consentimentos como modulos proprios.

## Veredito

A familia **Alunos** esta suficientemente coberta para web nesta rodada.

As duas imagens aprovadas cobrem:

1. `/app/alunos` como lista operacional da base de alunos com resumo lateral acionavel;
2. `/app/alunos/[id]` como perfil completo do aluno com a aba `Resumo` ativa.

Nao e necessario gerar novas imagens da familia Alunos agora.

## Imagens Aprovadas

| Imagem | Arquivo | Rota principal | Status |
| --- | --- | --- | --- |
| 27 | `27_round-4.1E_alunos_01_lista-perfil-resumido.png` | `/app/alunos` | Aprovada |
| 28 | `28_round-4.1E_aluno-perfil_01_resumo-operacional.png` | `/app/alunos/[id]` | Aprovada |

## Cobertura De Rotas

| Rota | Cobertura | Decisao |
| --- | --- | --- |
| `/app/alunos` | Imagem 27 | Coberta. |
| `/app/alunos/[id]` | Imagem 28 | Coberta com aba `Resumo` ativa. |
| `/app/alunos/[id]/linha-do-tempo` | Herdada | Herda linha do tempo curta da imagem 28 + componentes de historico/auditoria. |
| `/app/contatos` | Contrato textual | Herda lista simples, Inbox e Qualidade de Dados. Sem imagem propria agora. |
| `/app/contatos/[id]` | Contrato textual | Herda perfil simples de contato e Qualidade de Dados. |
| `/app/responsaveis` | Fora do MVP web atual | Removida pela decisao de escopo. |
| `/app/responsaveis/[id]` | Fora do MVP web atual | Removida pela decisao de escopo. |

## Fronteiras De Produto

| Superficie | Pergunta que responde | Nao deve virar |
| --- | --- | --- |
| Alunos | Como encontro um aluno e tomo acao rapida? | Perfil completo, dashboard ou agenda. |
| Perfil do aluno | Quem e o aluno, qual seu estado e o que fazer agora? | Lista, financeiro completo, agenda completa ou modulo familiar. |
| Contatos | Quem e este contato simples/incompleto/duplicado? | Responsavel/familia. |
| Linha do tempo | O que aconteceu com este aluno? | Auditoria juridica pesada ou consentimentos. |
| Tarefas | Que trabalho humano existe sobre o aluno? | Pendencia generica. |
| Inbox | Qual conversa existe com o aluno? | Perfil completo. |

## Escopo Removido

Conforme `alunos-scope-decision.pt-BR.md`, a familia Alunos nao inclui:

- responsaveis/familia;
- relacoes familiares;
- permissoes familiares;
- consentimentos como secao propria;
- perfil de responsavel como superficie principal.

Campos simples continuam permitidos:

- telefone/WhatsApp;
- e-mail;
- contato de emergencia opcional;
- preferencia simples de contato;
- status simples de canal quando necessario.

## Abas Do Perfil

| Aba | Cobertura | Decisao |
| --- | --- | --- |
| Resumo | Imagem 28 | Coberta. |
| Agenda | Herdada | Herda familia Agenda/Aulas. |
| Financeiro | Herdada | Herda familia Financeiro. |
| Documentos | Herdada | Herda componentes de documentos/anexos. |
| Historico | Herdada | Herda linha do tempo da imagem 28 + Auditoria/Historico. |
| Tarefas | Herdada | Herda pagina Tarefas. |

Nao gerar imagem propria de cada aba agora.

## Acoes Sensiveis

| Acao | Regra |
| --- | --- |
| `Alterar plano` | Abre fluxo com impacto financeiro; nao edita direto. |
| `Pausar aluno` | Exige confirmacao, motivo e registro. |
| `Atualizar dados` | Pode ser direto para dados simples; dados sensiveis exigem auditoria. |
| `Enviar mensagem` | Respeita status do canal e politica de envio. |
| `Criar tarefa` | Cria trabalho humano vinculado ao aluno. |

## Estados Cobertos E Pendentes

| Estado | Cobertura |
| --- | --- |
| aluno ativo | Coberto |
| pagamento pendente | Coberto |
| boa frequencia | Coberto |
| proxima aula marcada | Coberto |
| reposicao pendente | Coberto |
| tarefas abertas | Coberto |
| ultima conversa | Coberto |
| aluno em risco | Parcialmente coberto por risco/alerta; sem imagem propria agora. |
| aluno pausado | Contrato textual; sem imagem propria agora. |
| aluno inativo | Coberto na lista; detalhe pode herdar perfil. |
| aluno sem turma | Coberto na lista; detalhe pode herdar perfil. |
| aluno experimental | Coberto na lista; detalhe pode herdar perfil. |

## Agentes, Planos E Modos

| Contexto | Comportamento |
| --- | --- |
| 0 agentes | Alunos e perfil funcionam completos com filtros, acoes manuais, agenda, financeiro, notas, tarefas e historico. |
| 1 agente | Sugestoes aparecem apenas em dominios cobertos pelo agente ativo. |
| 3 agentes | Dominios ativos podem sugerir proxima acao, mensagem, tarefa e alerta. |
| 7 agentes | Todos os dominios podem apoiar triagem, respeitando cota, permissao, risco e auditoria. |
| Manual | Usuario filtra, abre perfil, envia mensagem, cria tarefa, registra nota, atualiza dados, altera plano e pausa aluno. |
| Copiloto | Pode resumir historico permitido, sugerir texto, explicar risco e recomendar proxima acao. |
| Autonomo | Nao altera plano, pausa aluno, muda dados sensiveis ou toma decisao sensivel sozinho. |

## Pontos Corrigidos Nesta Auditoria

1. `Historico do aluno` foi ajustado para linha do tempo operacional simples, sem consentimentos como tipo principal.
2. A estrategia de cobertura foi atualizada para marcar `/app/alunos/[id]` como coberta pela imagem 28.
3. Contatos ficou como contrato textual sem responsaveis/familia.
4. Responsaveis saiu do MVP web atual.

## Pontos Abertos Nao Bloqueantes

| Ponto | Decisao para agora |
| --- | --- |
| Estado de aluno em risco no perfil | Pode ser gerado no futuro se virar fluxo central de Retencao. |
| Aba Financeiro detalhada | Herdar familia Financeiro. |
| Aba Agenda detalhada | Herdar familia Agenda. |
| Linha do tempo completa | Herdar Historico/Auditoria. |
| Contatos | Contrato textual; imagem so se virar superficie central. |
| Mobile | Rodada propria. |

## Proxima Familia Recomendada

Proxima familia recomendada:

**Agenda / Aulas / Turmas / Reposicoes**

Motivo:

- aparece no Hoje;
- aparece no perfil do aluno;
- conecta aulas, chamada, reposicoes, turma, recursos e conflitos;
- provavelmente exige imagem propria por ter modelo mental diferente de lista/perfil.

## Referencias

- `alunos-scope-decision.pt-BR.md`
- `design-system-round-4-1E-alunos-lista-approved.pt-BR.md`
- `design-system-round-4-1E-aluno-perfil-approved.pt-BR.md`
- `design-system-round-4-0-web-page-blueprints.pt-BR.md`
- `design-system-round-4-image-coverage-strategy.pt-BR.md`
