# Taliya CRM - Agente Atendimento: Paginas, Conteudo E Dinamicas

Status: contrato funcional v0.1.
Data: 2026-05-21.

## Objetivo

Mapear as paginas, rotinas, fluxos, perfis, ajustes visiveis e dinamicas do Agente Atendimento.

Segue:

- `agents-flows-routines-pages-final-contract.pt-BR.md`
- `agents-flows-routine-profile-map.pt-BR.md`

## Regra Central

```text
Agente Atendimento nao tem configuracoes proprias.
Rotina organiza conversas/privacidade.
Perfil da rotina aplica modos nos fluxos.
Fluxo so abre para personalizacao quando necessario.
```

Responsaveis, aprovadores e filas humanas sao herdados da rotina.
O fluxo so mostra esses campos quando precisa trocar o padrao ou quando a aprovacao/excecao exige alguem especifico.

## Rotinas

| Rotina | Fluxos |
|---|---|
| Conversas e triagem | A1 Nova conversa; A2 Duvidas permitidas; A3 Aluno existente; A4 Fora do escopo; A5 Chamada humana; A10 Ciclo de vida/SLA |
| Identidade e privacidade | A6 Consentimento/opt-out; A7 Identidade/midias; A8 Privacidade/dados; A9 Telefone compartilhado e identidade |

Total: 2 rotinas, 10 fluxos.

## Paginas Do Agente

### Visao Geral

Rota:

```text
/app/agentes/atendimento
```

Mostra:

- status do agente;
- rotinas;
- conversas em andamento;
- excecoes abertas;
- aprovacoes de privacidade;
- bloqueios por plano, cota, permissao ou canal;
- execucoes recentes;
- atalhos para inbox, tarefas e auditoria.

Cards de rotina mostram:

- perfil atual;
- status;
- versao ativa;
- conversas afetadas;
- chamadas humanas pendentes;
- bloqueios;
- CTA principal.

Dinamicas:

- sem agente contratado: preview e upgrade, sem publicar IA;
- opt-out detectado: envio automatico bloqueado e auditoria registrada;
- baixa confianca: card mostra excecao/chamada humana;
- privacidade pendente: CTA vira "Revisar aprovacao";
- rascunho: CTA vira "Continuar ajuste".

### Pagina Da Rotina

Rota:

```text
/app/agentes/atendimento/rotinas/[routineId]
```

Mostra:

- nome e objetivo da rotina;
- perfil: Mais manual, Equilibrado, Mais autonomo ou Personalizado;
- explicacao do impacto do perfil;
- fluxos e modos aplicados;
- conversas/excecoes/aprovacoes;
- bloqueios;
- acoes: Ajustar, Simular, Publicar, Ver execucoes, Pausar, Voltar versao.

Dinamicas:

- trocar perfil recalcula modos, mostra antes/depois e exige nova simulacao;
- personalizar fluxo marca rotina como "perfil personalizado";
- aplicar perfil a todos remove personalizacoes;
- bloqueio de canal/cota/plano rebaixa ou impede modos autonomos.

### Ajustar Rotina E Fluxos

Rota:

```text
/app/agentes/atendimento/rotinas/[routineId]/ajustar
```

Mostra:

- perfil atual;
- fluxos da rotina;
- modo de cada fluxo;
- origem do modo: perfil ou ajuste individual;
- comportamento real por modo;
- ajustes visiveis quando necessario;
- dependencias fixas;
- fallback;
- simulacao rapida.

Nao mostra:

- prompt;
- modelo;
- payload;
- canal como escolha solta;
- configuracoes tecnicas do provedor.

### Simular Rotina

Rota:

```text
/app/agentes/atendimento/rotinas/[routineId]/simular
```

Mostra:

- cenario;
- conversa simulada;
- inbox/CRM ao vivo;
- linha de execucao;
- ponto de humano;
- auditoria que seria gerada.

Cenarios de Conversas e triagem:

- nova conversa simples;
- pergunta com resposta permitida;
- aluno identificado pede algo simples;
- conversa fora do escopo;
- baixa confianca chama humano;
- SLA estourado.

Cenarios de Identidade e privacidade:

- opt-out claro;
- opt-out ambiguo;
- midia/documento recebido;
- telefone compartilhado;
- pedido de dados/LGPD;
- identidade incerta.

### Publicar Versao

Rota:

```text
/app/agentes/atendimento/rotinas/[routineId]/publicar
```

Mostra:

- perfil;
- fluxos que seguem o perfil;
- fluxos personalizados;
- o que responde sozinho;
- o que chama humano;
- o que pede aprovacao;
- o que continua manual/copiloto;
- preflight.

Bloqueia se faltar:

- simulacao valida;
- template/tom quando houver resposta;
- fila humana quando houver excecao;
- aprovador quando houver privacidade;
- fallback;
- permissao;
- cota;
- canal/integracao quando houver envio.

### Execucoes Da Rotina

Rota:

```text
/app/agentes/atendimento/rotinas/[routineId]/execucoes
```

Mostra:

- periodo;
- conversa;
- contato/aluno;
- fluxo;
- perfil publicado na epoca;
- modo;
- status;
- humano chamado;
- cota;
- link para detalhe.

### Detalhe Da Execucao

Rota global:

```text
/app/fluxos/execucoes/[runId]
```

Mostra:

- agente Atendimento;
- rotina;
- perfil;
- fluxo;
- modo;
- mensagem/conversa;
- decisao do agente;
- humano chamado;
- aprovacao;
- fallback;
- auditoria.

## Perfis Por Rotina

### Conversas E Triagem

| Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|
| A1 Nova conversa | Copiloto | Excecoes | Excecoes |
| A2 Duvidas permitidas | Copiloto | Direto | Direto |
| A3 Aluno existente | Copiloto | Excecoes | Excecoes |
| A4 Fora do escopo | Copiloto | Direto | Direto |
| A5 Chamada humana | Direto | Direto | Direto |
| A10 Ciclo de vida/SLA | Copiloto | Direto | Direto |

Explicacao:

- Mais manual: agente organiza e sugere, equipe responde.
- Equilibrado: duvidas permitidas e fora de escopo rodam sozinhas; casos ambiguos chamam humano.
- Mais autonomo: tudo dentro da base aprovada segue automaticamente, com chamada humana quando sair do escopo.

### Identidade E Privacidade

| Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|
| A6 Consentimento/Opt-Out | Direto | Direto | Direto |
| A7 Identidade/Midias | Copiloto | Excecoes | Excecoes |
| A8 Privacidade/Dados | Manual | Aprovacao | Aprovacao |
| A9 Telefone Compartilhado E Identidade | Manual | Aprovacao | Aprovacao |

Explicacao:

- Mais manual: opt-out continua automatico; identidade e privacidade ficam com humano.
- Equilibrado: opt-out roda sozinho; midias incertas chamam humano; privacidade pede aprovacao.
- Mais autonomo: triagens sao adiantadas, mas dados/identidade ambigua continuam com aprovacao.

## Ajustes Visiveis Por Fluxo

| Fluxo | Ajustes visiveis quando necessario | Fixo/dependencia |
|---|---|---|
| A1 Nova conversa | limite de respostas; fila de excecao se diferente do padrao; template/tom se houver resposta automatica | canal recebido; opt-out; identidade minima; sinais de risco; auditoria |
| A2 Duvidas permitidas | limite por conversa; template/tom | respostas permitidas vem da base aprovada; bloqueio fora da base; auditoria |
| A3 Aluno existente | fila de excecao se diferente do padrao; template/tom se houver resposta; botao de ajuda manual | dados sensiveis protegidos; identidade validada; permissao |
| A4 Fora do escopo | resposta padrao; destino da tarefa/caso; tom | politica de escopo; bloqueio de promessa fora do CRM; auditoria |
| A5 Chamada humana | fila destino se diferente do padrao; prioridade | campos do resumo; criterio de risco/baixa confianca; auditoria |
| A10 Ciclo de vida/SLA | tempo de SLA; prioridade; texto interno do alerta | origem da conversa; fila natural; auditoria |
| A6 Consentimento/Opt-Out | responsavel de revisao se ambiguo; texto de confirmacao; tom | opt-out sempre bloqueia envio; auditoria; canal de origem |
| A7 Identidade/Midias | responsavel de revisao; campos de identificacao pedidos | tipos aceitos definidos pelo produto; permissao; auditoria |
| A8 Privacidade/Dados | aprovador de privacidade; prazo do caso; texto de recebimento | pedido LGPD/dados sensiveis exige caso e auditoria |
| A9 Telefone Compartilhado E Identidade | responsavel de revisao; prazo do caso | regra de validacao do produto; identidade validada antes de expor dado |

## Modais E Drawers

- Pausar rotina;
- Pausar fluxo;
- Voltar versao;
- Resolver excecao;
- Revisar aprovacao;
- Ver conversa original.

## Resumo De UX

```text
1. Usuario escolhe perfil da rotina.
2. Entende o que responde sozinho, chama humano ou pede aprovacao.
3. Personaliza fluxo apenas se precisar.
4. Simula conversa real.
5. Publica versao.
6. Acompanha inbox, excecoes, aprovacoes e execucoes.
```
