# Taliya CRM - Agente Financeiro: Paginas, Conteudo E Dinamicas

Status: contrato funcional v0.1.
Data: 2026-05-21.

## Objetivo

Mapear as paginas, rotinas, fluxos, perfis, ajustes visiveis e dinamicas do Agente Financeiro.

Segue:

- `agents-flows-routines-pages-final-contract.pt-BR.md`
- `agents-flows-routine-profile-map.pt-BR.md`

## Regra Central

```text
Agente Financeiro nao decide financeiro sensivel sozinho.
Rotina organiza cobrancas, plano e excecoes.
Perfil aplica modos nos fluxos.
Fluxo so abre para personalizacao quando necessario.
```

Responsaveis, aprovadores e filas humanas sao herdados da rotina.
O fluxo so mostra esses campos quando precisa trocar o padrao ou quando a aprovacao/excecao exige alguem especifico.

## Rotinas

| Rotina | Fluxos |
|---|---|
| Lembretes e pagamentos | D1 Lembrete vencimento; D2 Pagamento atrasado; D3 Pix/link; D7 Falha pagamento; D8 Recibo/nota; D10 Conciliacao interna |
| Ciclo do plano do aluno | D5 Renovacao plano; D9 Pausa/trancamento; D15 Encerramento ou alteracao efetiva de plano |
| Excecoes e documentos financeiros | D4 Confirmacao pagamento; D6 Excecoes financeiras; D11 Contrato/termos; D12 Bloqueio/liberacao; D13 Creditos/cortesias; D14 Fechamento mensal |

Total: 3 rotinas, 15 fluxos.

## Paginas Do Agente

### Visao Geral

Rota:

```text
/app/agentes/financeiro
```

Mostra:

- status do agente;
- rotinas;
- cobrancas proximas;
- atrasos;
- falhas de pagamento;
- aprovacoes financeiras;
- excecoes;
- bloqueios por provedor/cota/permissao;
- execucoes recentes.

Dinamicas:

- sem provedor financeiro: links/confirmacoes ficam bloqueados;
- sem cota/canal: mensagens automaticas ficam bloqueadas;
- pedido de desconto/acordo/cortesia: vira aprovacao/caso;
- comprovante incerto: pede aprovacao;
- rascunho: CTA "Continuar ajuste".

### Pagina Da Rotina

Rota:

```text
/app/agentes/financeiro/rotinas/[routineId]
```

Mostra:

- perfil;
- impacto do perfil;
- fluxos e modos;
- cobrancas/planos afetados;
- aprovacoes pendentes;
- excecoes;
- falhas;
- acoes: Ajustar, Simular, Publicar, Ver execucoes, Pausar, Voltar versao.

Dinamicas:

- trocar perfil exige nova simulacao;
- acoes financeiras sensiveis continuam com aprovacao em qualquer perfil;
- falta de provedor/cota/canal rebaixa ou bloqueia modos autonomos;
- personalizacao vira "perfil personalizado".

### Ajustar Rotina E Fluxos

Rota:

```text
/app/agentes/financeiro/rotinas/[routineId]/ajustar
```

Mostra:

- perfil atual;
- modos dos fluxos;
- comportamento por modo;
- ajustes visiveis;
- dependencias fixas;
- roteamento humano;
- simulacao rapida.

Nao mostra:

- regra de billing Taliya;
- payload financeiro;
- retry tecnico;
- alteracao livre de valor/plano;
- provedor como configuracao do fluxo.

### Simular Rotina

Rota:

```text
/app/agentes/financeiro/rotinas/[routineId]/simular
```

Cenarios de Lembretes e pagamentos:

- vencimento proximo;
- pagamento atrasado simples;
- aluno pede acordo;
- envio de Pix/link;
- falha de pagamento;
- recibo/nota solicitado;
- conciliacao incerta.

Cenarios de Ciclo do plano:

- renovacao;
- pausa/trancamento;
- encerramento;
- alteracao de plano;
- aprovador rejeita.

Cenarios de Excecoes financeiras:

- comprovante incerto;
- desconto/cortesia;
- contrato pendente;
- bloqueio/liberacao;
- fechamento mensal com anomalia.

Mostra:

- mensagem/cobranca;
- estado financeiro no CRM;
- aprovacao/excecao;
- linha de execucao;
- auditoria.

### Publicar Versao

Rota:

```text
/app/agentes/financeiro/rotinas/[routineId]/publicar
```

Mostra:

- perfil;
- fluxos personalizados;
- o que envia sozinho;
- o que fica como sugestao;
- o que exige aprovacao;
- o que chama humano;
- preflight.

Bloqueia se faltar:

- permissao financeira;
- aprovador;
- simulacao;
- template/tom;
- provedor quando houver link/confirmacao;
- cota/canal;
- fallback;
- auditoria.

### Execucoes E Detalhe

Rotas:

```text
/app/agentes/financeiro/rotinas/[routineId]/execucoes
/app/fluxos/execucoes/[runId]
```

Mostram:

- aluno/cobranca/plano;
- perfil publicado;
- fluxo;
- modo;
- acao;
- aprovacao;
- excecao;
- cota;
- auditoria.

## Perfis Por Rotina

### Lembretes E Pagamentos

| Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|
| D1 Lembrete vencimento | Copiloto | Direto | Direto |
| D2 Pagamento atrasado | Copiloto | Copiloto | Excecoes |
| D3 Pix/link | Manual | Aprovacao | Aprovacao |
| D7 Falha pagamento | Copiloto | Copiloto | Excecoes |
| D8 Recibo/nota | Copiloto | Copiloto | Excecoes |
| D10 Conciliacao interna | Manual | Aprovacao | Aprovacao |

Explicacao:

- Mais manual: financeiro recebe sugestoes, mas envia/confirma manualmente.
- Equilibrado: lembrete simples roda sozinho; atraso, falha e documento ficam como sugestao; link e conciliacao pedem aprovacao.
- Mais autonomo: agente conduz cobrancas simples e casos claros; acordo/disputa/match incerto chama humano.

### Ciclo Do Plano Do Aluno

| Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|
| D5 Renovacao plano | Manual | Aprovacao | Aprovacao |
| D9 Pausa/trancamento | Manual | Aprovacao | Aprovacao |
| D15 Encerramento ou alteracao efetiva de plano | Manual | Aprovacao | Aprovacao |

Explicacao:

- Mais manual: agente organiza casos e impacto.
- Equilibrado: agente prepara a mudanca e para em aprovacao.
- Mais autonomo: agente adianta comunicacao/checklist, mas mudanca efetiva de plano exige aprovacao.

### Excecoes E Documentos Financeiros

| Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|
| D4 Confirmacao pagamento | Manual | Aprovacao | Aprovacao |
| D6 Excecoes financeiras | Manual | Aprovacao | Aprovacao |
| D11 Contrato/termos | Manual | Aprovacao | Aprovacao |
| D12 Bloqueio/liberacao | Manual | Aprovacao | Aprovacao |
| D13 Creditos/cortesias | Manual | Aprovacao | Aprovacao |
| D14 Fechamento mensal | Copiloto | Copiloto | Excecoes |

Explicacao:

- Mais manual: financeiro recebe organizacao e rascunhos.
- Equilibrado: fechamento vira resumo sugerido; acoes sensiveis pedem aprovacao.
- Mais autonomo: agente antecipa analise e preparo, mas decisoes financeiras sensiveis continuam com aprovacao.

## Ajustes Visiveis Por Fluxo

| Fluxo | Ajustes visiveis quando necessario | Fixo/dependencia |
|---|---|---|
| D1 Lembrete vencimento | quando lembrar; template; tom; limite por cobranca; acao se nao responder | cobranca existente; opt-out; canal; auditoria |
| D2 Pagamento atrasado | tentativas; fila financeira; sinais que chamam humano; template/tom | valor/vencimento do CRM; sem acordo livre |
| D3 Pix/link | aprovador; template/tom; limite de valor para aprovacao; prazo | provedor financeiro; pagamento existente; link idempotente |
| D7 Falha pagamento | tentativas; fila financeira; quando abrir caso; template/tom | status do provedor; cobranca vinculada |
| D8 Recibo/nota | responsavel se exigir revisao; template/tom; fallback | documento vem do CRM/provedor; documentos permitidos do produto |
| D10 Conciliacao interna | aprovador; responsavel; prazo | confianca minima do produto; conciliacao auditavel |
| D5 Renovacao plano | aprovador; antecedencia; template/tom | plano vigente; preco do CRM |
| D9 Pausa/trancamento | aprovador; prazo; responsavel se diferente | impacto calculado pelo CRM; motivo obrigatorio |
| D15 Encerramento/alteracao de plano | aprovador; comunicacao; responsavel se diferente | checklist do produto; plano/cobranca vinculados |
| D4 Confirmacao pagamento | aprovador; responsavel se exigir revisao; prazo | evidencia exigida; webhook/evidencia auditavel |
| D6 Excecoes financeiras | aprovador obrigatorio; prazo; responsavel | tipos definidos pelo produto; sem desconto/acordo livre |
| D11 Contrato/termos | aprovador; template; tom; prazo | contrato aprovado; aceite auditavel |
| D12 Bloqueio/liberacao | aprovador; motivo; texto interno; fallback | exige permissao e auditoria |
| D13 Creditos/cortesias | aprovador; limite de valor; motivo; responsavel | credito/cortesia exige motivo e auditoria |
| D14 Fechamento mensal | responsavel; frequencia; quando abrir tarefa | secoes do produto; dados financeiros do CRM |

## Modais E Drawers

- Pausar rotina;
- Pausar fluxo;
- Voltar versao;
- Resolver excecao financeira;
- Revisar aprovacao;
- Ver cobranca/plano.

## Resumo De UX

```text
1. Usuario escolhe perfil da rotina.
2. Entende o que envia, sugere ou pede aprovacao.
3. Personaliza fluxo so se precisar.
4. Simula cobranca/plano/documento.
5. Publica versao.
6. Acompanha aprovacoes, excecoes e execucoes.
```
