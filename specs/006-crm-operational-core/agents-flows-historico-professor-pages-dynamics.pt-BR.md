# Taliya CRM - Agente Historico/Professor: Paginas, Conteudo E Dinamicas

Status: contrato funcional v0.1.
Data: 2026-05-21.

## Objetivo

Mapear as paginas, rotinas, fluxos, perfis, ajustes visiveis e dinamicas do Agente Historico/Professor.

Segue:

- `agents-flows-routines-pages-final-contract.pt-BR.md`
- `agents-flows-routine-profile-map.pt-BR.md`

## Regra Central

```text
Historico/Professor apoia aula, nota e repasse.
Historico protegido exige permissao e aprovacao.
O agente nao expoe dado sensivel sem escopo permitido.
```

Responsaveis, aprovadores e filas humanas sao herdados da rotina.
O fluxo so mostra esses campos quando precisa trocar o padrao ou quando a aprovacao/excecao exige alguem especifico.

## Rotinas

| Rotina | Fluxos |
|---|---|
| Aula com contexto | G1 Contexto antes aula; G2 Observacao pos-aula; G4 Objetivo/evolucao; G8 Repasse entre professores; G9 Lembrete professor; G12 Linha do tempo |
| Historico protegido | G3 Restricao/cuidado; G5 Contexto para agente; G6 Documentos/anamnese; G7 Correcao historico; G10 Compartilhar contexto; G11 Permissao historico |

Total: 2 rotinas, 12 fluxos.

## Paginas Do Agente

### Visao Geral

Rota:

```text
/app/agentes/historico-professor
```

Mostra:

- status do agente;
- rotinas;
- aulas proximas com contexto;
- notas pendentes;
- repasses entre professores;
- documentos/anamnese pendentes;
- aprovacoes de historico;
- excecoes;
- bloqueios por permissao.

Dinamicas:

- permissao ausente: contexto fica bloqueado;
- dado sensivel: exige aprovacao/caso;
- nota pendente: lembrete/tarefa;
- professor troca: repasse sugerido;
- documento faltando: tarefa/checklist.

### Pagina Da Rotina

Rota:

```text
/app/agentes/historico-professor/rotinas/[routineId]
```

Mostra:

- perfil;
- impacto;
- fluxos e modos;
- aulas/professores/alunos afetados;
- aprovacoes;
- excecoes;
- bloqueios;
- acoes: Ajustar, Simular, Publicar, Ver execucoes, Pausar, Voltar versao.

Dinamicas:

- trocar perfil exige simulacao;
- historico protegido continua com aprovacao;
- permissoes podem bloquear contexto;
- personalizacao marca perfil personalizado.

### Ajustar Rotina E Fluxos

Rota:

```text
/app/agentes/historico-professor/rotinas/[routineId]/ajustar
```

Mostra:

- perfil;
- modos dos fluxos;
- comportamento por modo;
- ajustes visiveis;
- dependencias fixas;
- visibilidade/permissao como leitura/bloqueio;
- simulacao rapida.

Nao mostra:

- dados sensiveis livres;
- regra clinica;
- permissao real editavel;
- prompt;
- payload;
- anamnese como configuracao livre.

### Simular Rotina

Rota:

```text
/app/agentes/historico-professor/rotinas/[routineId]/simular
```

Cenarios de Aula com contexto:

- aula proxima com contexto permitido;
- aula com restricao sensivel;
- nota pos-aula pendente;
- professor precisa repasse;
- lembrete de professor;
- linha do tempo com dado sensivel.

Cenarios de Historico protegido:

- restricao/cuidado;
- contexto para agente;
- documento/anamnese;
- correcao historico;
- compartilhar contexto;
- permissao de historico.

Mostra:

- professor/aula;
- resumo permitido;
- bloqueio de dado sensivel;
- aprovacao;
- tarefa;
- auditoria.

### Publicar Versao

Rota:

```text
/app/agentes/historico-professor/rotinas/[routineId]/publicar
```

Mostra:

- perfil;
- fluxos personalizados;
- o que vira lembrete/resumo;
- o que pede aprovacao;
- o que chama humano;
- o que fica manual/copiloto;
- preflight.

Bloqueia se faltar:

- simulacao;
- permissao de historico;
- aprovador;
- professor/destinatario quando necessario;
- fallback;
- auditoria.

### Execucoes E Detalhe

Rotas:

```text
/app/agentes/historico-professor/rotinas/[routineId]/execucoes
/app/fluxos/execucoes/[runId]
```

Mostram:

- aula/aluno/professor;
- perfil publicado;
- fluxo;
- modo;
- resumo/nota/tarefa;
- aprovacao;
- bloqueio de permissao;
- auditoria.

## Perfis Por Rotina

### Aula Com Contexto

| Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|
| G1 Contexto antes aula | Copiloto | Copiloto | Excecoes |
| G2 Observacao pos-aula | Copiloto | Copiloto | Excecoes |
| G4 Objetivo/evolucao | Copiloto | Copiloto | Excecoes |
| G8 Repasse entre professores | Copiloto | Copiloto | Excecoes |
| G9 Lembrete professor | Copiloto | Direto | Direto |
| G12 Linha do tempo | Copiloto | Copiloto | Excecoes |

Explicacao:

- Mais manual: agente prepara contexto e lembretes.
- Equilibrado: lembretes rodam; contexto, notas, linha do tempo e repasses ficam como apoio do professor.
- Mais autonomo: agente conduz resumos e lembretes permitidos, respeitando visibilidade e permissao.

### Historico Protegido

| Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|
| G3 Restricao/cuidado | Manual | Aprovacao | Aprovacao |
| G5 Contexto para agente | Manual | Aprovacao | Aprovacao |
| G6 Documentos/anamnese | Manual | Aprovacao | Aprovacao |
| G7 Correcao historico | Manual | Aprovacao | Aprovacao |
| G10 Compartilhar contexto | Manual | Aprovacao | Aprovacao |
| G11 Permissao historico | Manual | Aprovacao | Aprovacao |

Explicacao:

- Mais manual: historico protegido fica com humano.
- Equilibrado: agente prepara contexto/documento/correcao e pede aprovacao.
- Mais autonomo: agente adianta revisao e bloqueios, mas historico protegido continua exigindo aprovacao.

## Ajustes Visiveis Por Fluxo

| Fluxo | Ajustes visiveis quando necessario | Fixo/dependencia |
|---|---|---|
| G1 Contexto antes aula | professor se diferente; quando chamar humano | secoes do resumo do produto; permissao; dado sensivel protegido |
| G2 Observacao pos-aula | lembrete; professor; template/tom interno | tipos de nota do produto; aula finalizada; autor da nota |
| G4 Objetivo/evolucao | professor/responsavel; frequencia; tarefa | secoes do produto; sem avaliacao clinica livre |
| G8 Repasse entre professores | professor destino; quando chamar humano | campos do resumo do produto; visibilidade permitida |
| G9 Lembrete professor | horario; frequencia; destino; texto interno | professor/aula existentes; tarefa interna |
| G12 Linha do tempo | filtro padrao; responsavel por revisao | tipos de evento do produto; historico protegido |
| G3 Restricao/cuidado | aprovador; dono do caso; tarefa humana | visibilidade por permissao; dado sensivel |
| G5 Contexto para agente | aprovador; escopo; prazo | dados permitidos por permissao; auditoria |
| G6 Documentos/anamnese | aprovador; responsavel; checklist | documentos exigidos pelo produto/setup; permissao |
| G7 Correcao historico | aprovador; motivo; prazo; fallback | evento original preservado; auditoria |
| G10 Compartilhar contexto | aprovador; destinatario; template/tom | dados permitidos por permissao; auditoria |
| G11 Permissao historico | aprovador; prazo | papel/escopo real em Configuracoes/Permissoes |

## Modais E Drawers

- Pausar rotina;
- Pausar fluxo;
- Voltar versao;
- Resolver excecao;
- Revisar aprovacao;
- Ver contexto permitido;
- Bloqueio por permissao.

## Resumo De UX

```text
1. Usuario escolhe perfil da rotina.
2. Entende o que vira lembrete, resumo, tarefa ou aprovacao.
3. Personaliza fluxo so se precisar.
4. Simula aula, professor, nota ou historico.
5. Publica versao.
6. Acompanha notas, repasses, documentos e aprovacoes.
```
