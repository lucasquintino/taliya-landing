# Taliya CRM - Auditoria De Qualidade Das Regras Detalhadas

Status: auditoria de qualidade v0.1.
Data: 2026-05-22.

## Objetivo

Garantir que os 96 fluxos tenham regras explicativas no mesmo padrao de clareza usado em `Falta com aviso`.

## Problema Encontrado Na Versao Anterior

A matriz `agents-flows-detailed-mode-rules-matrix.pt-BR.csv` estava completa em estrutura, mas ainda tinha frases geradas a partir de ajustes, como:

- `ajuste "fila" esta configurado`;
- `ajuste "limite de respostas" nao esta definido ou conflita com a regra publicada`;
- `pedido sai da base aprovada`.

Essas frases nao sao boas para a UI final porque o dono do studio nao entende a regra real do fluxo.

## Regua De Qualidade

Cada fluxo deve explicar, em linguagem de produto:

1. o que permite a Taliya seguir;
2. o que chama equipe;
3. o que pede aprovacao;
4. o que faz o fluxo parar;
5. para onde a operacao continua;
6. quais ajustes realmente mudam esse comportamento.

## Regra De Escrita

Nao usar:

- `ajuste "..."`;
- `dentro da regra`;
- `regra publicada` sem dizer qual regra;
- `configurado` como substituto de regra concreta;
- linguagem tecnica de engine.

Usar:

- aluno, aula, lead, pagamento, professor, fila, responsavel, prazo, limite, credito, vaga, documento, permissao;
- situacoes concretas: `aviso chegou fora do prazo`, `nao ha vaga compativel`, `pagamento nao conciliou`, `telefone pertence a mais de um aluno`;
- acao clara: `cria tarefa`, `pede aprovacao`, `chama recepcao`, `abre caso`, `pausa automacao`.

## Criterio De Conclusao

A matriz detalhada so fica pronta quando:

- possui 96 linhas;
- nao possui campos vazios;
- nao possui `ajuste "`;
- nao possui frase vaga `dentro da regra`;
- cada fluxo possui texto especifico para os modos permitidos;
- os modos bloqueados continuam claramente marcados como bloqueados.

## Resultado Da Auditoria

Status: aprovado.

Validacao executada:

```text
rows 96
blank cells 0
ajuste " 0
pedido sai da base 0
nao esta definido ou conflita 0
esta configurado 0
dentro da regra 0
confere os dados, executa a acao 0
Automatico direto 0
Automatico com excecoes 0
Automatico com aprovacao 0
manual_como_funciona unique 96 repeated 0
copiloto_como_funciona unique 96 repeated 0
autonomo_aprovacao_como_funciona unique 96 repeated 0
review flow sections 96
```

Cobertura por agente:

| Agente | Fluxos |
|---|---:|
| Atendimento | 10 |
| Agenda | 16 |
| Vendas | 15 |
| Financeiro | 15 |
| Retencao | 13 |
| Gestao/Governanca | 15 |
| Historico/Evolucao | 12 |
| **Total** | **96** |

## Fonte Reprodutivel

As regras revisadas ficam em:

```text
scripts/generate-taliya-detailed-mode-rules.py
```

A matriz gerada fica em:

```text
specs/006-crm-operational-core/agents-flows-detailed-mode-rules-matrix.pt-BR.csv
```

Se um fluxo precisar mudar, editar a entrada correspondente no script e regenerar a matriz.
