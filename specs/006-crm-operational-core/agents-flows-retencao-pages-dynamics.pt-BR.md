# Taliya CRM - Agente Retencao: Paginas, Conteudo E Dinamicas

Status: contrato funcional v0.1.
Data: 2026-05-21.

## Objetivo

Mapear as paginas, rotinas, fluxos, perfis, ajustes visiveis e dinamicas do Agente Retencao.

Segue:

- `agents-flows-routines-pages-final-contract.pt-BR.md`
- `agents-flows-routine-profile-map.pt-BR.md`

## Regra Central

```text
Retencao automatiza prevencao simples.
Casos sensiveis pedem aprovacao.
Saude, reclamacao e cancelamento nao viram acao livre.
```

Responsaveis, aprovadores e filas humanas sao herdados da rotina.
O fluxo so mostra esses campos quando precisa trocar o padrao ou quando a aprovacao/excecao exige alguem especifico.

## Rotinas

| Rotina | Fluxos |
|---|---|
| Retencao preventiva | E1 Queda frequencia; E2 Aluno inativo; E3 Retorno; E6 Satisfacao; E7 Retorno apos pausa; E10 Marco engajamento |
| Casos sensiveis | E4 Risco cancelamento; E5 Reativacao ex-aluno; E8 Risco por perfil; E9 Pos-cancelamento; E11 Saude/evento pessoal; E12 Segmentacao risco; E13 Reclamacao e recuperacao de confianca |

Total: 2 rotinas, 13 fluxos.

## Paginas Do Agente

### Visao Geral

Rota:

```text
/app/agentes/retencao
```

Mostra:

- status do agente;
- rotinas;
- alunos em risco;
- alunos inativos;
- casos sensiveis;
- reclamacoes;
- aprovacoes pendentes;
- excecoes;
- execucoes recentes.

Dinamicas:

- risco alto: CTA para caso humano;
- reclamacao: pode pausar automacoes relacionadas;
- opt-out: contato automatico bloqueado;
- falta historico/dado: fluxo vira tarefa ou copiloto;
- rascunho: CTA "Continuar ajuste".

### Pagina Da Rotina

Rota:

```text
/app/agentes/retencao/rotinas/[routineId]
```

Mostra:

- perfil;
- impacto do perfil;
- fluxos e modos;
- alunos/casos afetados;
- aprovacoes;
- excecoes;
- bloqueios;
- acoes: Ajustar, Simular, Publicar, Ver execucoes, Pausar, Voltar versao.

Dinamicas:

- trocar perfil exige simulacao;
- casos sensiveis continuam com aprovacao;
- risco/reclamacao pode auto-pausar automacoes da pessoa/caso;
- personalizacao marca perfil personalizado.

### Ajustar Rotina E Fluxos

Rota:

```text
/app/agentes/retencao/rotinas/[routineId]/ajustar
```

Mostra:

- perfil;
- modos dos fluxos;
- comportamento por modo;
- ajustes visiveis;
- dependencias fixas;
- roteamento humano;
- simulacao rapida.

Nao mostra:

- segmento livre de IA;
- promessa de desconto/beneficio;
- dado sensivel sem permissao;
- regra clinica;
- campanha livre.

### Simular Rotina

Rota:

```text
/app/agentes/retencao/rotinas/[routineId]/simular
```

Cenarios de Retencao preventiva:

- queda de frequencia;
- aluno inativo;
- aluno quer retornar;
- satisfacao negativa;
- retorno apos pausa;
- marco de engajamento.

Cenarios de Casos sensiveis:

- risco de cancelamento;
- ex-aluno elegivel;
- risco por perfil;
- pos-cancelamento;
- evento pessoal/saude;
- reclamacao;
- pausa automatica de automacoes.

Mostra:

- contexto do aluno;
- conversa/tarefa/caso;
- ponto de aprovacao;
- ponto de humano;
- auditoria.

### Publicar Versao

Rota:

```text
/app/agentes/retencao/rotinas/[routineId]/publicar
```

Mostra:

- perfil;
- fluxos personalizados;
- o que vira contato/tarefa;
- o que pede aprovacao;
- o que chama humano;
- o que fica manual/copiloto;
- preflight.

Bloqueia se faltar:

- simulacao;
- consentimento;
- template/tom;
- aprovador para casos sensiveis;
- dono do caso;
- fallback;
- permissao de historico;
- cota/canal.

### Execucoes E Detalhe

Rotas:

```text
/app/agentes/retencao/rotinas/[routineId]/execucoes
/app/fluxos/execucoes/[runId]
```

Mostram:

- aluno/caso;
- perfil publicado;
- fluxo;
- modo;
- contato/tarefa;
- aprovacao;
- humano chamado;
- pausa automatica;
- auditoria.

## Perfis Por Rotina

### Retencao Preventiva

| Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|
| E1 Queda frequencia | Copiloto | Excecoes | Excecoes |
| E2 Aluno inativo | Copiloto | Copiloto | Excecoes |
| E3 Retorno | Copiloto | Copiloto | Excecoes |
| E6 Satisfacao | Copiloto | Copiloto | Excecoes |
| E7 Retorno apos pausa | Copiloto | Copiloto | Excecoes |
| E10 Marco engajamento | Copiloto | Copiloto | Excecoes |

Explicacao:

- Mais manual: agente mostra sinais e sugere abordagem.
- Equilibrado: queda de frequencia roda com excecoes; demais casos preventivos viram sugestao.
- Mais autonomo: cadencias preventivas rodam dentro dos limites e chamam humano em risco/contexto sensivel.

### Casos Sensiveis

| Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|
| E4 Risco cancelamento | Manual | Aprovacao | Aprovacao |
| E5 Reativacao ex-aluno | Copiloto | Aprovacao | Aprovacao |
| E8 Risco por perfil | Manual | Aprovacao | Aprovacao |
| E9 Pos-cancelamento | Manual | Aprovacao | Aprovacao |
| E11 Saude/evento pessoal | Manual | Aprovacao | Aprovacao |
| E12 Segmentacao risco | Manual | Aprovacao | Aprovacao |
| E13 Reclamacao e recuperacao de confianca | Manual | Aprovacao | Aprovacao |

Explicacao:

- Mais manual: agente organiza caso e contexto.
- Equilibrado: agente prepara acao e pede aprovacao.
- Mais autonomo: agente adianta o seguro, mas casos sensiveis continuam parando em aprovacao.

## Ajustes Visiveis Por Fluxo

| Fluxo | Ajustes visiveis quando necessario | Fixo/dependencia |
|---|---|---|
| E1 Queda frequencia | regra de queda; responsavel; cadencia; template/tom | presenca historica; limite de contato; auditoria |
| E2 Aluno inativo | dias de inatividade; responsavel; limite de contato; template/tom | status do aluno; opt-out; historico |
| E3 Retorno | responsavel se diferente; quando chamar humano; template/tom | disponibilidade real; regra de agenda do CRM |
| E6 Satisfacao | janela; responsavel; quando abrir reclamacao; template/tom | feedback protegido; limite de contato |
| E7 Retorno apos pausa | antecedencia; responsavel se diferente; template/tom | pausa registrada; impacto financeiro/agenda |
| E10 Marco engajamento | responsavel; limite de contato; template/tom | tipos de marco do produto; historico; opt-out |
| E4 Risco cancelamento | dono do caso; aprovador; quando pausar automacoes; template/tom | risco alto vira caso; sem oferta livre |
| E5 Reativacao ex-aluno | aprovador; cadencia; template/tom | segmento vem do CRM; consentimento; opt-out |
| E8 Risco por perfil | aprovador; responsavel; acao permitida | segmento sensivel vem do CRM; auditoria |
| E9 Pos-cancelamento | aprovador; quando contatar; responsavel; template/tom | cancelamento concluido; limite de contato |
| E11 Saude/evento pessoal | dono do caso; aprovador; tarefa humana | visibilidade por permissao; dado sensivel |
| E12 Segmentacao risco | aprovador; acao permitida; responsavel | segmento vem do CRM; sem campanha livre |
| E13 Reclamacao e recuperacao de confianca | dono do caso; aprovador; pausa automatica; resposta/tom | reclamacao vira caso; compensacao exige aprovacao |

## Modais E Drawers

- Pausar rotina;
- Pausar fluxo;
- Voltar versao;
- Resolver excecao;
- Revisar aprovacao;
- Abrir caso sensivel;
- Pausar automacoes do aluno/caso.

## Resumo De UX

```text
1. Usuario escolhe perfil da rotina.
2. Entende o que previne, sugere ou pede aprovacao.
3. Personaliza fluxo so se precisar.
4. Simula aluno/caso.
5. Publica versao.
6. Acompanha riscos, casos, aprovacoes e excecoes.
```
