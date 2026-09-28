# Plano de migracao e importacao inicial - PT-BR

> Status: Rodada 0 v0.1. Este documento define como um studio real entra no Taliya vindo de planilha, sistema antigo, agenda manual ou base incompleta.

## Regra central

Importacao nao e so upload. Ela precisa transformar dados externos em CRM operavel sem criar automacoes perigosas.

## Fontes de entrada

| Fonte | Dados provaveis |
| --- | --- |
| Planilha | alunos, telefones, planos, horarios, pagamentos, observacoes. |
| Sistema antigo | alunos, contratos, financeiro, agenda, historico. |
| Agenda manual | turmas, horarios, professores, reposicoes. |
| WhatsApp | contatos, conversas, grupos, pedidos. |
| Cadastro manual | dados minimos para comecar. |

## Etapas

```text
escolher fonte
  -> enviar arquivo/conectar
  -> mapear colunas/campos
  -> validar dados
  -> detectar duplicidades
  -> revisar dados sensiveis
  -> importar rascunho
  -> resolver bloqueios
  -> abrir CRM
  -> liberar agentes somente apos preflight
```

## Dados minimos para operar

| Area | Minimo |
| --- | --- |
| Studio | nome, cidade/estado, horarios, WhatsApp/canal principal. |
| Alunos | nome, contato ou responsavel, status. |
| Agenda | turmas/aulas ou horarios principais. |
| Financeiro | plano do aluno ou status financeiro basico, se o studio usar financeiro no MVP. |
| Equipe | pelo menos dono/admin. |
| Agentes | agente escolhido, modo inicial e limites basicos se plano > Base. |

## Bloqueios comuns

| Problema | Resultado |
| --- | --- |
| Contato duplicado | Qualidade de dados. |
| Telefone compartilhado | Revisao de responsavel/grupo. |
| Aluno sem contato | Pode operar aula, mas bloqueia mensagem automatica. |
| Aluno sem plano | Financeiro limitado. |
| Turma sem capacidade | Bloqueia encaixe/lista de espera automatica. |
| Historico sensivel em campo livre | Revisao antes de expor a professor/agente. |
| Pagamento divergente | Caso financeiro em analise. |

## Telas

- Onboarding/importacao;
- Importacao assistida no app para fluxo simples;
- Qualidade de dados;
- Duplicidades;
- Revisao final do setup;
- Agentes/preflight;
- Integracoes/logs.

## Aceite

Um studio deve conseguir entrar de tres formas:

1. rapido/manual com poucos dados;
2. planilha simples;
3. importacao assistida com revisao.

Agentes so podem ativar depois de preflight de dados obrigatorios por fluxo.
