# Decisao De Escopo - Alunos, Contatos E Responsaveis

> Status: decisao aprovada v0.1. Esta decisao remove responsaveis/familia e consentimentos como modulos proprios da familia Alunos para manter o CRM operacional e direto para studios de Pilates.

## Decisao

Na familia **Alunos**, nao teremos modulo proprio de:

- responsaveis/familia;
- relacoes familiares;
- permissoes familiares;
- consentimentos como secao propria;
- perfil de responsavel como superficie principal.

## Motivo

Para o MVP do Taliya CRM, esses blocos aumentam complexidade de produto sem melhorar o trabalho diario principal do gestor de studio.

O foco da pagina de aluno deve ser:

```text
Quem e esse aluno, qual e o estado dele no studio e qual acao precisa acontecer agora?
```

Nao:

```text
Como modelar familia, responsaveis legais e consentimentos formais?
```

## O Que Permanece

Continuam permitidos como campos simples quando forem uteis:

- telefone/WhatsApp;
- e-mail;
- contato principal;
- contato de emergencia, opcional;
- preferencia simples de contato;
- status simples de canal, como `WhatsApp permitido`, se necessario para envio.

Esses campos nao viram modulo, aba ou rota propria.

## O Que Sai Do MVP

| Item | Decisao |
| --- | --- |
| `/app/responsaveis` | Fora do MVP web atual. |
| `/app/responsaveis/[id]` | Fora do MVP web atual. |
| Relacoes familiares | Fora do MVP web atual. |
| Consentimentos como aba/secao | Fora do MVP web atual. |
| Permissoes familiares | Fora do MVP web atual. |

## Contatos

`Contatos` pode continuar existindo como conceito operacional simples, mas nao como modulo familiar.

Uso esperado:

- contato que veio de WhatsApp;
- contato antes de virar aluno/interessado;
- contato incompleto;
- contato duplicado;
- contato associado a conversa.

Se a rota `/app/contatos` existir, ela deve herdar lista/perfil simples e qualidade de dados. Nao precisa imagem propria agora.

## Impacto Na Topbar Da Familia Alunos

Topbar recomendada:

- `Alunos`;
- `Contatos`;
- `Segmentos`;
- `Linha do tempo`.

Remover:

- `Responsaveis`.

## Impacto No Perfil Do Aluno

O perfil do aluno nao deve ter:

- aba `Responsaveis`;
- bloco `Familia`;
- bloco `Consentimentos`;
- bloco de permissoes familiares.

Abas recomendadas:

- `Resumo`;
- `Agenda`;
- `Financeiro`;
- `Documentos`;
- `Historico`;
- `Tarefas`.

## Regra Para Prompts Visuais

Todo prompt da familia Alunos deve evitar:

- responsaveis/familia;
- permissoes familiares;
- consentimentos como secao;
- relacionamento familiar;
- cadastro juridico pesado.

Pode usar:

- contato principal;
- WhatsApp;
- telefone;
- e-mail;
- contato de emergencia simples, se necessario.
