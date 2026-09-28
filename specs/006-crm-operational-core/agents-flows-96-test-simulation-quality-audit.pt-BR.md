# Taliya CRM - Auditoria Das 96 Simulacoes De Fluxos

Status: aprovado v0.1.
Data: 2026-05-22.

## Validacao Executada

```text
rows 96
blank cells 0
ids unique 96
cenarios por fluxo 4
inicio sem checagens embutidas 96
limites explicitos 96
acoes de aprovacao explicitas 42
usa celular 43
nao usa celular 53
visual types 18
pontuacao duplicada 0
aprovacao com celular 5 ids C7, C14, D3, E5, E9
modo Autonomo: 14
modo Autonomo com aprovacao: 42
modo Autonomo com excecoes: 40
visual aprovacao: 37
visual capacidade: 1
visual celular_conversa: 43
visual dinheiro_na_mesa: 1
visual fechamento_financeiro: 1
visual ficha_lead: 1
visual fila_humana: 1
visual gargalo_operacional: 1
visual historico_aluno: 1
visual hoje_prioridades: 1
visual incidente_execucao: 1
visual integracao_logs: 1
visual linha_tempo: 1
visual performance_agentes: 1
visual qualidade_dados: 1
visual resumo_semanal: 1
visual simulador_fluxo: 1
visual uso_cotas: 1
resultado do teste 0
dados do teste 0
celular fake 0
previsao 0
dashboard 0
json 0
ativar rotina 0
dentro da regra 0
nao decide fora do escopo 0
pode aparecer 0
pede algo 0
somente se 0
pedido de aprovacao para aprovar 0
```

## Decisoes Validadas

- Os 96 fluxos estao mapeados.
- Todos possuem 4 cenarios de teste.
- Todos possuem visual central definido.
- Celular e usado apenas quando existe mensagem/conversa/canal externo.
- Fluxos internos usam objeto do CRM: aprovacao, agenda, financeiro, incidente, auditoria, historico ou uso/cotas.
- Todos informam o que o agente nao faz naquele fluxo.
- Nenhum fluxo usa limite generico; cada limite foi escrito para aquele caso.
- As 42 acoes de aprovacao usam rotulo especifico do fluxo.
- Fluxos com aprovacao nao fingem execucao autonoma.
- Fluxos sem aprovacao informam se chamam humano por excecao ou se apenas aplicam fallback.
- Fluxos com aprovacao podem usar celular quando a simulacao mostra a mensagem pronta/preview, mas a execucao para no pedido de aprovacao.
- Fluxos autonomos com excecoes mostram quando chamam humano.
- Nao ha cards separados de `Dados do teste` ou `Resultado do teste` no contrato da tela.

## Artefatos

- `agents-flows-96-test-simulation-matrix.pt-BR.csv`
- `agents-flows-96-test-simulation-review.pt-BR.md`
- `agents-flows-test-simulation-page-contract.pt-BR.md`
