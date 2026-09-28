# Taliya CRM - Contrato De Regras Detalhadas Por Modo

Status: contrato funcional v0.1.
Data: 2026-05-22.

## Objetivo

Definir o conteudo do bloco `Como funciona neste modo` para os 96 fluxos de Agentes/Fluxos.

Fonte autoritativa das regras detalhadas:

```text
agents-flows-detailed-mode-rules-matrix.pt-BR.csv
```

Fonte legivel para revisao:

```text
agents-flows-detailed-mode-rules-review.pt-BR.md
```

Fonte reprodutivel:

```text
scripts/generate-taliya-detailed-mode-rules.py
```

Este contrato complementa:

- `agents-flows-final-flow-contract-matrix.pt-BR.csv`
- `agents-flows-final-flow-page-contract.pt-BR.md`

## Regra Principal

O bloco `Como funciona neste modo` e dinamico e muda quando o usuario seleciona outro modo.

Nao usar frases vagas como `se estiver dentro da regra`.

A tela deve mostrar as regras concretas do fluxo:

- o que permite seguir sozinho;
- o que chama equipe;
- o que pede aprovacao;
- o que faz parar;
- qual fallback continua a operacao.

## Como Renderizar Por Modo

| Modo selecionado | Colunas usadas |
|---|---|
| Manual | `manual_como_funciona` |
| Copiloto | `copiloto_como_funciona` |
| Autonomo com aprovacao | `autonomo_aprovacao_como_funciona` + `se_parar` |
| Autonomo com excecoes | `autonomo_excecoes_segue_sozinho_quando` + `autonomo_excecoes_chama_equipe_quando` + `se_parar` |
| Autonomo | `autonomo_conclui_sozinho_quando` + `autonomo_para_quando` + `se_parar` |

Se uma coluna disser `bloqueado`, o modo deve aparecer desabilitado.

## Exemplo Para A Imagem Atual

Fluxo: `Falta com aviso`.

Modo selecionado: `Autonomo com excecoes`.

### Segue sozinho quando

- aluno foi identificado;
- aula existe na agenda;
- aviso chegou ate o prazo configurado;
- falta ainda nao foi registrada;
- destino da reposicao esta definido;
- mensagem usa template aprovado.

### Chama equipe quando

- aviso chega fora do prazo;
- nao encontra aluno ou aula;
- ja existe reposicao pendente;
- nao ha vaga compativel;
- aluno pede excecao, credito, cancelamento ou reclama;
- WhatsApp, cota ou permissao bloqueiam o envio.

### Se parar

- cria tarefa/caso em Reposicoes, aula ou tarefa;
- registra auditoria do motivo.

## Relacao Com Ajustes

O texto deve refletir os ajustes visiveis do fluxo.

Exemplo: se `Prazo para falta avisada` estiver em `2 horas antes da aula`, a regra renderizada deve dizer `aviso chegou ate 2 horas antes da aula`.

## Uso Em Imagens

Para prompt visual, usar esta matriz para preencher o bloco `Como funciona neste modo`.

A matriz final de fluxos define modo, teto e ajustes. Esta matriz define as regras explicativas do bloco dinamico.

## Qualidade Validada

A matriz detalhada foi auditada com estes resultados:

```text
96 fluxos
0 campos vazios
0 ocorrencias de `ajuste "`
0 ocorrencias de `pedido sai da base`
0 ocorrencias de `nao esta definido ou conflita`
0 ocorrencias de `esta configurado`
0 ocorrencias de `dentro da regra`
0 ocorrencias de `confere os dados, executa a acao`
96 textos unicos para Manual
96 textos unicos para Copiloto
96 textos unicos para Autonomo com aprovacao
```

Isso significa que a UI pode usar esta matriz para o bloco `Como funciona neste modo` sem cair em frases genericas.
