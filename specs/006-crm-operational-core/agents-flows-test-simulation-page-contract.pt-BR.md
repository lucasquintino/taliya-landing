# Taliya CRM - Contrato Da Pagina Simular Fluxo

Status: aprovado v0.1.
Data: 2026-05-22.

## Imagem Aprovada

```text
D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/58_round-4.1L_agentes_05_teste-fluxo-falta-com-aviso-aprovado.png
```

Observacao: a imagem aprovada acima esta correta em estrutura e layout. Para a versao final de produto, aplicar apenas os ajustes de nomenclatura definidos em `Ajustes De Nomenclatura Da Imagem Aprovada`.

Rota exemplo:

```text
/app/agentes/agenda/rotinas/presenca-e-faltas/fluxos/falta-com-aviso/simular
```

## Objetivo Da Pagina

Mostrar como um fluxo executaria antes de salvar, publicar ou alterar configuracao.

A pagina nao deve prever resultado de negocio. Ela deve simular a operacao do fluxo:

- gatilho;
- checagens;
- decisao;
- acao ou preparacao;
- chamada humana, aprovacao ou parada quando houver;
- fim do fluxo atual;
- continuidade criada para outra area quando existir.

## Layout Base

Todas as paginas `Simular fluxo` usam o mesmo esqueleto:

1. `Cenarios`
2. visual do caso simulado
3. `Execucao da simulacao`
4. `Agente de Configuracao` lateral

Nao usar cards extras de `Dados da simulacao` ou `Resultado da simulacao`. Essas informacoes devem aparecer dentro dos cenarios, do visual do caso ou da execucao.

## Ajustes De Nomenclatura Da Imagem Aprovada

A imagem aprovada deve ser mantida em layout, hierarquia e componentes. Ajustar somente a linguagem:

| Onde aparece | Trocar | Para |
|---|---|---|
| URL | `/teste` | `/simular` |
| Breadcrumb | `Teste` | `Simular` |
| Titulo | `Testar Falta com aviso` | `Simular Falta com aviso` |
| Subtitulo | `Veja como a Taliya executa este fluxo antes de salvar ou publicar mudancas.` | `Veja como a Taliya executaria este fluxo antes de salvar ou publicar mudancas.` |
| Chip | `Teste seguro` | `Simulacao segura` |
| Painel direito | `Explicando o teste` | `Explicando a simulacao` |
| Texto do painel direito | `Neste teste...` | `Nesta simulacao...` |
| Card de execucao | `Execucao do teste` | `Execucao da simulacao` |
| Botao principal | `Rodar teste novamente` | `Rodar simulacao novamente` |
| Campo do agente | `Pergunte sobre este teste...` | `Pergunte sobre esta simulacao...` |
| Sugestao do agente | `Testar aviso fora do prazo` | `Simular aviso fora do prazo` |
| Sugestao do agente | `Testar aluno pedindo credito` | `Simular aluno pedindo credito` |

Nao criar segunda pagina de teste. `Testar fluxo` e `Simular fluxo` sao a mesma superficie; o nome de produto e `Simular fluxo`.

## Cenarios

O bloco de cenarios fica na esquerda.

Cada fluxo deve ter poucos cenarios, normalmente 3 ou 4:

- um cenario feliz;
- uma excecao que chama equipe;
- uma excecao de regra/aprovacao;
- uma falha de canal, integracao, permissao ou cota quando fizer sentido.

Exemplo para `Falta com aviso`:

- `Aluno avisou no prazo`: registra falta e cria tarefa de reposicao.
- `Aviso fora do prazo`: chama equipe antes de registrar.
- `Aluno pede credito`: chama equipe antes de decidir.
- `WhatsApp falha`: para e cria pendencia.

## Visual Do Caso Simulado

Nem todo fluxo usa celular.

O visual central deve representar onde o caso acontece:

| Tipo de fluxo | Visual principal |
|---|---|
| Conversa, WhatsApp, lembrete, cobranca, follow-up, satisfacao | Celular/conversa |
| Agenda, presenca, aula, reposicao, grade, capacidade | Aula, agenda, lista de alunos ou celular se houver mensagem externa |
| Financeiro interno, conciliacao, fechamento, contrato, excecao financeira | Card financeiro, movimentacao, documento ou aprovacao |
| Vendas sem conversa direta, qualificacao, perda, indicacao, matricula | Ficha de lead, pipeline ou checklist |
| Retencao sensivel, reclamacao, risco, saude/evento pessoal | Caso de retencao, fila sensivel ou aprovacao |
| Gestao/Governanca, incidentes, cotas, permissoes, importacao | Painel operacional, incidente, execucao, uso/cotas ou auditoria |
| Historico/Evolucao, professor, documentos, permissao | Perfil do aluno, historico, aula ou documento |

Regra:

- usar celular apenas quando o fluxo realmente envolve mensagem/conversa/canal externo;
- nao forcar celular em fluxo interno;
- nao esconder a acao real atras de um mock visual bonito.

## Execucao Da Simulacao

O bloco `Execucao da simulacao` deve explicar exatamente o que o agente faria naquele cenario.

Estrutura padrao:

1. `Inicio`
2. `Checagens`
3. `Decisao`
4. `Acao`
5. `Fim`

Para fluxos com aprovacao, trocar `Acao` por `Pedido de aprovacao` quando a acao principal nao e aplicada ainda.

Para fluxos em copiloto, trocar `Acao` por `Sugestao` quando o agente apenas prepara uma recomendacao.

Para fluxos manuais, trocar `Acao` por `Tarefa criada` quando o humano executa.

## Todos Os Fluxos Fazem Acao?

Todos os 96 fluxos produzem algum resultado operacional, mas nem todos executam uma acao final sozinhos.

Tipos de resultado:

- `acao executada`: envia mensagem, registra falta, atualiza status, cria tarefa, organiza fila;
- `pedido de aprovacao`: prepara dados, impacto e proximo passo para humano aprovar;
- `sugestao`: prepara resumo, rascunho ou recomendacao para humano decidir;
- `tarefa manual`: organiza o caso para humano executar;
- `parada/fallback`: cria pendencia, incidente, aprovacao vencida ou chamada humana.

A simulacao precisa mostrar o tipo correto. Nunca deve fingir autonomia maior do que o modo permite.

## Exemplo Aprovado: Falta Com Aviso

No cenario `Aluno avisou no prazo`, a tela deve deixar claro:

- a Taliya recebeu o aviso;
- conferiu aluno, aula, prazo, falta anterior e mensagem;
- decidiu seguir sem equipe;
- registrou a falta na aula;
- enviou a mensagem aprovada;
- criou tarefa em Reposicoes;
- nao escolheu vaga, credito ou horario neste fluxo.

Essa ultima frase e obrigatoria em fluxos que apenas encaminham para outra rotina decidir.

## Agente De Configuracao

O painel direito explica a simulacao e os limites do fluxo.

Ele deve explicar:

- por que a simulacao passou;
- quando chamaria humano;
- o que o fluxo nao decidiu;
- como o resultado mudaria em outro modo ou cenario.

Exemplo aprovado:

```text
Nesta simulacao, a Taliya registrou a falta e criou uma tarefa em Reposicoes. Ela nao decidiu a reposicao. Se o aviso estivesse fora do prazo, chamaria a equipe.
```

## Regras De Simplicidade

- Nao mostrar grafico.
- Nao mostrar dashboard.
- Nao mostrar JSON.
- Nao mostrar logs tecnicos longos.
- Nao mostrar card separado de resultado.
- Nao mostrar card separado de dados da simulacao.
- Nao chamar simulacao de previsao.
- Nao criar drawer.
- A simulacao deve mostrar o fluxo real, nao uma metrica de sucesso.
