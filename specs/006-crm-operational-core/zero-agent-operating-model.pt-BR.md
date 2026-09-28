# Modelo de operacao com 0 agentes - PT-BR

> Status: Rodada 0 v0.1. Este documento garante que o Taliya continua sendo um CRM completo no plano Base, sem automacao ativa de agentes.

## Decisao central

O plano Base nao e um plano "quebrado". Ele e o CRM operacional sem agentes ativos. Tudo que for caminho critico do studio deve ter resolucao manual.

```text
Base = CRM + organizacao + tarefas + registros + aprovacoes manuais + relatorios basicos
Base != automacao ativa de agente
```

## O que funciona no Base

| Area | Deve funcionar sem agente |
| --- | --- |
| Onboarding | Ativar conta, perfil, horarios, importar dados, convidar equipe. |
| Hoje | Ver prioridades, tarefas, alertas e bloqueios. |
| Inbox | Responder conversas manualmente, registrar opt-out, criar tarefas. |
| Alunos | Cadastrar, editar, consultar, registrar nota permitida. |
| Agenda | Ver agenda, turmas, aulas, fazer chamada, registrar faltas. |
| Reposicoes | Controlar creditos, reservar vaga e convidar manualmente. |
| Vendas | Cadastrar interessados, agendar experimental, acompanhar pipeline. |
| Financeiro | Registrar pagamentos, enviar cobranca manual, abrir casos. |
| Retencao | Ver alunos em risco, criar tarefas, registrar contato. |
| Operacao | Criar casos, tarefas, aprovacoes manuais e checklists. |
| Relatorios | Ver relatorios baseados em registros do CRM. |
| Configuracoes | Configurar studio, equipe, permissoes, politicas e templates. |
| Auditoria | Ver eventos gerados por acoes sensiveis. |

## O que nao funciona no Base

| Capacidade | Comportamento |
| --- | --- |
| Resposta automatica por agente | Bloqueada; criar sugestao apenas se nao consumir automacao paga ou se permitido como preview. |
| Execucao autonoma de fluxo | Bloqueada. |
| Envio automatico recorrente | Bloqueado. |
| Classificacao com IA paga | Bloqueada ou limitada a demonstracao/preview se configurado. |
| Resumo com IA de historico longo | Bloqueado quando consumir cota paga. |
| Campanhas automatizadas | Bloqueadas; comunicados manuais com aprovacao podem existir. |

## Downgrade de fluxos no Base

| Fluxo com agente | No Base vira |
| --- | --- |
| Responder conversa | Tarefa ou resposta manual. |
| Confirmar presenca | Tarefa/checklist manual. |
| Encontrar encaixe | Sugestao programatica ou lista de candidatos, sem envio automatico. |
| Cobrar atraso | Tarefa financeira com template manual. |
| Reativar aluno | Segmento + tarefa/comunicado manual aprovado. |
| Detectar risco | Relatorio/lista baseada em regras simples, sem decisao de IA. |
| Resumir historico | Linha do tempo manual/filtrada. |
| Investigar incidente | Caso operacional manual. |

## UI obrigatoria no Base

Toda tela que normalmente teria agente deve mostrar:

- acao manual equivalente;
- estado "agente nao incluido no plano" quando aplicavel;
- CTA de upgrade apenas como contexto, sem bloquear o CRM;
- explicacao do que o agente faria se estivesse ativo;
- registro manual disponivel.

## Cotas no Base

| Origem | Comportamento |
| --- | --- |
| Mensagens manuais pelo WhatsApp conectado | Podem existir se o canal permitir, mas nao contam como automacao de agente. |
| AI/agent automation | 0 mensal. |
| Tarefas, casos, registros | Sem cota de agente. |
| Relatorios derivados | Sem cota de agente, salvo processamento AI futuro. |

## Criterio de aceite

Um gestor no Base deve conseguir:

1. cadastrar alunos;
2. operar agenda e chamada;
3. responder WhatsApp manualmente;
4. controlar reposicoes;
5. acompanhar interessados;
6. registrar pagamentos/cobrancas;
7. abrir tarefas e casos;
8. ver prioridades do dia;
9. configurar equipe/permissoes;
10. ver relatorios essenciais.

Se qualquer uma dessas depender de agente ativo, o desenho esta errado.
