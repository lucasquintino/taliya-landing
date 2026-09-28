# Reconfiguracao Pos-Setup

Status: rascunho consolidado.
Data: 2026-05-13.

## Objetivo

Definir como o studio muda configuracoes depois do go-live sem quebrar alunos, aulas, cobrancas, reposicoes, fluxos e agentes ativos.

## Principio

Toda mudanca pos-go-live precisa mostrar impacto antes de publicar.

## Tipos de mudanca

| Mudanca | Risco | Precisa simular | Pode aplicar imediatamente |
|---|---|---|---|
| Nome/endereco do studio | Baixo | Nao | Sim |
| Horario comercial | Medio | Sim se afeta mensagens/aulas | Sim ou futura |
| Permissao | Alto | Sim | Sim com auditoria |
| Turma/capacidade | Medio/alto | Sim | Depende de aulas futuras |
| Regra de reposicao | Alto | Sim | Preferir data futura |
| Modelo de cobranca | Critico | Sim | Raramente imediato |
| Consumo de aulas | Critico | Sim | Preferir proximo ciclo |
| Inadimplencia | Alto | Sim | Depende de politica |
| Template | Medio | Preview | Sim se aprovado |
| Modo de fluxo | Alto | Sim | Manual/copiloto sim; autonomo so preflight |
| Politica operacional | Critico | Sim | Nova versao |
| Cota/plano | Alto | Billing decide | Sim conforme entitlement |

## Fluxo de reconfiguracao

```text
usuario altera regra
  -> sistema cria nova versao em rascunho
  -> calcula diff antes/depois
  -> identifica objetos afetados
  -> simula casos relevantes
  -> mostra impacto e risco
  -> pede aprovacao se sensivel
  -> publica agora ou agenda vigencia
  -> pausa fluxos afetados se necessario
  -> grava auditoria
```

## Impacto obrigatorio

Antes de publicar, mostrar:

- paginas afetadas;
- alunos afetados;
- turmas/aulas afetadas;
- cobrancas afetadas;
- reposicoes abertas;
- tarefas/aprovacoes pendentes;
- fluxos de agentes afetados;
- se algum fluxo ficara pausado;
- se regra aplica a historico ou apenas futuro;
- como reverter.

## Aplicacao imediata vs futura

| Tipo | Recomendacao |
|---|---|
| Regra simples de UI/rotina | Pode aplicar imediata. |
| Regra de agenda futura | Aplicar em aulas futuras. |
| Regra financeira | Preferir proximo ciclo/vencimento. |
| Regra de consumo | Preferir novo ciclo ou novos creditos. |
| Politica de agente | Nova versao; execucoes antigas mantem snapshot. |

## Regras por area

### Agenda/reposicao

- Reposicoes ja abertas mantem politica de origem.
- Novas reposicoes usam nova regra.
- Se mudar prazo/credito, mostrar alunos afetados.
- Se fluxo de Agenda autonomo dependia da regra, reexecutar preflight.

### Financeiro/consumo

- Cobrancas ja geradas mantem regra original, salvo ajuste auditado.
- Mudanca de plano pode valer no proximo ciclo.
- Consumo ja registrado nao e apagado; correcao cria evento novo.
- Quebra-galho exige motivo e antes/depois.

### Agentes/fluxos

- Mudar manual -> copiloto exige fallback e permissao.
- Mudar copiloto -> autonomo exige politica, cota, template, canal e simulacao.
- Mudar autonomo -> manual pode aplicar imediatamente e pausar execucoes futuras.
- Execucoes em andamento guardam snapshot.

### Permissoes

- Reduzir permissao aplica imediatamente para novas acoes.
- Aprovacoes pendentes devem revalidar decisor.
- Acesso suporte Taliya sempre tem escopo/prazo.

## Rollback

Rollback deve:

- restaurar regra anterior para novas acoes;
- nao apagar auditoria;
- nao reescrever execucoes antigas;
- mostrar objetos que foram criados durante a versao revertida;
- pausar agentes se houver incerteza.

## Aceite

Reconfiguracao esta segura quando:

- nenhuma regra sensivel muda sem diff;
- historico nao e sobrescrito;
- execucoes guardam snapshot;
- impacto em alunos/aulas/cobrancas aparece;
- rollback existe para regra sensivel;
- agentes pausam quando preflight deixa de passar.
