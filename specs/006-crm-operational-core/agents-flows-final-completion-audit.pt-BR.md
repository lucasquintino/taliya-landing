# Taliya CRM - Auditoria Final De Agentes/Fluxos

Status: auditoria de conclusao v0.1.
Data: 2026-05-22.

## Objetivo Auditado

Definir e documentar a arquitetura final de Agentes/Fluxos do Taliya CRM, incluindo matriz dos 96 fluxos com:

- modos permitidos;
- defaults;
- ajustes minimos;
- requisitos fixos;
- aprovacoes;
- handoffs;
- fallbacks;
- simulacao;
- orientacao para paginas e imagens.

## Arquivos Autoritativos

### Matriz Final

```text
specs/006-crm-operational-core/agents-flows-final-flow-contract-matrix.pt-BR.csv
```

Este e o arquivo autoritativo para os 96 fluxos.

### Contrato Da Pagina De Fluxo

```text
specs/006-crm-operational-core/agents-flows-final-flow-page-contract.pt-BR.md
```

Define como a pagina `Ver e ajustar fluxo` deve funcionar.

### Regras Detalhadas Por Modo

```text
specs/006-crm-operational-core/agents-flows-detailed-mode-rules-matrix.pt-BR.csv
specs/006-crm-operational-core/agents-flows-detailed-mode-rules-contract.pt-BR.md
specs/006-crm-operational-core/agents-flows-detailed-mode-rules-quality-audit.pt-BR.md
scripts/generate-taliya-detailed-mode-rules.py
```

Define o conteudo dinamico do bloco `Como funciona neste modo`.

### Contrato Visual Da Pagina De Rotina

```text
specs/006-crm-operational-core/agents-flows-routine-page-visual-contract.pt-BR.md
```

Define como a pagina de rotina usa a matriz final para montar cards de fluxo.

### Mapa De Perfis Por Rotina

```text
specs/006-crm-operational-core/agents-flows-routine-profile-map.pt-BR.md
```

Define como `Mais manual`, `Equilibrado` e `Mais autonomo` aplicam modos aos fluxos.

## Arquivos Historicos

```text
specs/006-crm-operational-core/agents-flows-configuration-matrix.pt-BR.csv
```

Este arquivo foi usado como insumo historico.

Ele ainda pode conter nomes antigos como:

- `Automatico direto`;
- `Automatico com excecoes`;
- `Automatico com aprovacao`.

Esses nomes nao devem ser usados em produto, UI, prompt visual ou imagem.

Em caso de conflito, a matriz final vence.

## Evidencia De Cobertura

### Contagem Por Agente

Resultado validado na matriz final:

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

### Distribuicao De Tetos

Resultado validado na matriz final:

| Teto | Fluxos |
|---|---:|
| Autonomo com aprovacao | 42 |
| Autonomo com excecoes | 40 |
| Autonomo | 14 |
| **Total** | **96** |

## Campos Obrigatorios Da Matriz Final

Cada uma das 96 linhas possui:

- `id`;
- `agente`;
- `rotina`;
- `fluxo`;
- `teto`;
- `modos_permitidos`;
- `modos_bloqueados`;
- `mais_manual`;
- `equilibrado`;
- `mais_autonomo`;
- `modo_padrao_pagina`;
- `status_padrao_card`;
- `explicacao_card`;
- `manual_na_pagina`;
- `copiloto_na_pagina`;
- `autonomo_aprovacao_na_pagina`;
- `autonomo_excecoes_na_pagina`;
- `autonomo_na_pagina`;
- `ajustes_do_studio`;
- `requisitos_fixos`;
- `quando_chama_equipe`;
- `quando_pede_aprovacao`;
- `fallback`;
- `simulacao_obrigatoria`;
- `nota_para_pagina_do_fluxo`;
- `onde_continua`.

## Regras Validadas

### Cada Fluxo Tem Seu Proprio Modo

Validado.

A matriz final traz modo por fluxo em:

- `mais_manual`;
- `equilibrado`;
- `mais_autonomo`;
- `modo_padrao_pagina`.

### Teto Controla Modos Permitidos

Validado.

Exemplo:

```text
B2 Falta com aviso
Teto: Autonomo com excecoes
Permitidos: Manual; Copiloto; Autonomo com aprovacao; Autonomo com excecoes
Bloqueado: Autonomo
```

### Ajuste Real Nao E Requisito Fixo

Validado na matriz final.

Os ajustes do studio nao usam como configuracao livre:

- canal;
- auditoria;
- permissao;
- cota;
- integracao.

Esses itens aparecem como requisitos fixos/read-only.

### Simulacao Simula O Fluxo Real

Validado.

Toda linha possui `simulacao_obrigatoria`, com obrigacao de mostrar:

- gatilho;
- dados usados;
- decisao do modo escolhido;
- mensagem/acao;
- aprovacao ou chamada humana quando houver;
- fallback;
- cota;
- auditoria.

### Como Funciona Neste Modo Tem Regras Detalhadas

Validado.

A matriz detalhada possui 96 linhas e cobre:

- Manual;
- Copiloto;
- Autonomo com aprovacao;
- Autonomo com excecoes;
- Autonomo;
- fallback `se_parar`;
- ajustes relacionados;
- requisitos read-only.

Para `Falta com aviso`, a matriz detalhada define explicitamente quando a Taliya segue sozinha, quando chama equipe e o que acontece se parar.

A auditoria de qualidade confirmou:

```text
96 linhas
0 campos vazios
0 frases com `ajuste "`
0 frases com `pedido sai da base`
0 frases com `nao esta definido ou conflita`
0 frases com `esta configurado`
0 frases com `dentro da regra`
```

### Paginas E Imagens Tem Fonte De Verdade

Validado.

Para gerar pagina ou imagem:

1. usar o shell aprovado;
2. usar pagina de agente/rotina ja documentada;
3. para card de fluxo, buscar `explicacao_card`, modo e status na matriz final;
4. para pagina de fluxo, buscar textos `*_na_pagina`, ajustes, requisitos, fallback e simulacao na matriz final;
5. para o bloco `Como funciona neste modo`, buscar as regras na matriz detalhada por modo;
6. nunca mostrar IDs internos como `B1`, `C3`, `D10` ao dono do studio.

## Comando De Validacao Executado

Resumo do verificador executado:

```text
ok final matrix: 96 rows, required columns, final mode names, no fixed deps in ajustes
```

O verificador confirmou:

- 96 linhas;
- colunas obrigatorias preenchidas;
- nomes finais de modo na matriz final;
- nenhuma dependencia fixa listada como ajuste do studio.

## Conclusao

Arquitetura final de Agentes/Fluxos esta documentada para orientar paginas e imagens.

A proxima etapa de produto nao e redefinir arquitetura, e sim usar estes contratos para:

- gerar a pagina individual de fluxo;
- gerar a pagina de simulacao;
- gerar a pagina de publicacao;
- atualizar prompts visuais quando necessario.
