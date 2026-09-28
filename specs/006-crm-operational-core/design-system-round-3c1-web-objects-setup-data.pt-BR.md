# Design System Web - Rodada 3C.1 - Objetos, Setup E Dados

> Status: biblioteca visual v0.1 aprovada. Esta rodada cobre componentes compostos de onboarding, setup, importacao, qualidade de dados, perfis e relacionamentos.

## Objetivo

Fechar lacunas de dominio que nao estavam cobertas pelas rodadas 3A e 3B:

- setup inicial;
- checklist de ativacao;
- importacao;
- mapeamento de campos;
- duplicidades;
- conflitos de dados;
- cabecalho de perfil;
- abas internas;
- relacoes e familia;
- consentimento e preferencias;
- timeline sensivel.

## Decisao

A imagem da Rodada 3C.1 fica aprovada como v0.1.

Ela acertou:

- transformou onboarding e importacao em componentes reais, nao apenas formularios soltos;
- cobriu duplicidade com comparacao lado a lado e decisao de merge;
- criou fila de conflitos de dados com severidade, objeto, acao e responsavel;
- resolveu a base visual de perfil de aluno/contato/responsavel;
- incluiu relacoes familiares, telefone compartilhado e alerta de conflito;
- incluiu consentimento, opt-out e preferencias de contato;
- trouxe timeline sensivel com dado restrito, dado mascarado e pedido de acesso.

## Ressalvas

- A prancha continua mais branca do que a referencia original; em telas finais deve voltar ao cinza frio.
- O cabecalho de perfil ficou bom, mas paginas reais podem precisar de mais hierarquia para status criticos.
- A resolucao de duplicidade precisa deixar claro quais campos vencem no merge.
- Timeline sensivel deve sempre respeitar permissao e mascaramento por papel.
- Consentimento nao deve ser tratado como toggle simples quando houver exigencia legal ou historico.

## Componentes Aprovados

| Componente | Uso principal |
| --- | --- |
| Wizard / stepper de setup | Onboarding, configuracao inicial e etapas obrigatorias. |
| Checklist de ativacao | Pendencias de setup e abertura operacional. |
| Progresso de importacao | Jobs de importacao, pausas, erros e retomada. |
| Mapeamento de campos | Importacao e saneamento de dados. |
| Resolucao de duplicidade | Merge ou separacao de registros. |
| Fila de conflitos de dados | Dados bloqueantes, ausentes ou divergentes. |
| Cabecalho de perfil | Aluno, contato, responsavel, professor ou interessado. |
| Abas internas de perfil | Resumo, agenda, financeiro, historico, documentos e permissoes. |
| Relacoes e familia | Responsaveis, dependentes, telefones compartilhados e conflitos. |
| Consentimento e preferencias | Canal, opt-out, horarios e historico de consentimento. |
| Timeline sensivel | Historico permitido, mascarado ou restrito. |

## Regras De Uso

- Setup deve sempre permitir continuar depois quando a etapa nao for bloqueante.
- Importacao deve mostrar progresso, erro, duplicidade e o que falta resolver.
- Merge de duplicidade exige confirmacao e auditoria.
- Perfil deve mostrar a proxima acao de forma clara.
- Consentimento deve mostrar historico, origem e responsavel.
- Dados sensiveis devem suportar mascaramento e pedido de acesso.

## Nao Fazer

- Nao transformar setup em landing page.
- Nao esconder conflitos de dados que bloqueiam agentes ou fluxos.
- Nao permitir merge silencioso.
- Nao mostrar historico sensivel sem permissao contextual.
- Nao tratar opt-out como preferencia leve.

