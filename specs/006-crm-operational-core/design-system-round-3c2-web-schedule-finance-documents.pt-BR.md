# Design System Web - Rodada 3C.2 - Agenda, Financeiro E Documentos

> Status: biblioteca visual v0.1 aprovada. Esta rodada cobre componentes compostos de agenda, turmas, chamada, reposicoes, documentos e financeiro profundo.

## Objetivo

Fechar lacunas de dominio ligadas a operacao diaria de aulas e rotinas financeiras:

- calendario semanal completo;
- card de aula;
- grade/turma;
- roster de chamada;
- matcher de reposicao;
- lista de espera;
- conflito de recurso;
- viewer de documento/contrato;
- upload/anexo/comprovante;
- conciliacao;
- input de valor/moeda;
- simulador financeiro antes/depois.

## Decisao

A imagem da Rodada 3C.2 fica aprovada como v0.1.

Ela acertou:

- criou calendario semanal de verdade, com aulas, capacidade, professor, conflito e vaga aberta;
- separou card de aula, turma e roster de chamada;
- incluiu presenca, falta, no-show, observacao e credito de reposicao;
- criou matcher de reposicao com vagas, candidatos, conflito e melhor encaixe;
- incluiu lista de espera e conflito de recurso;
- trouxe viewer de contrato/documento com status e acoes;
- incluiu upload, anexo, comprovante pendente/aprovado e erro;
- criou conciliacao financeira e input de moeda;
- trouxe simulador financeiro antes/depois com impacto, risco e aprovacao.

## Ressalvas

- A prancha e densa; paginas reais precisam priorizar agenda ou financeiro, nao tudo junto.
- O calendario semanal exige tratamento responsivo e scroll claro.
- Status de presenca/falta/no-show nao pode depender apenas de cor.
- Matcher de reposicao deve ser programatico primeiro; IA apenas auxilia mensagem ou explicacao.
- Simulador financeiro precisa mostrar regras, permissao e motivo antes de aprovar.
- Documentos financeiros e comprovantes exigem auditoria e controle de acesso.

## Componentes Aprovados

| Componente | Uso principal |
| --- | --- |
| Calendario semanal completo | Agenda web, grade, disponibilidade e capacidade. |
| Card de aula | Aula, turma, professor, sala, capacidade e chamada. |
| Grade / turma | Turma, alunos, vagas, lista de espera e proxima aula. |
| Roster de chamada | Presenca, falta, no-show, observacao e reposicao. |
| Matcher de reposicao | Encaixe, reserva, convite e conflito. |
| Lista de espera | Prioridade, disponibilidade, origem e status de convite. |
| Conflito de recurso | Sala, professor, aulas afetadas e acao sugerida. |
| Viewer de documento/contrato | Contratos, termos, recibos e comprovantes. |
| Upload/anexo/comprovante | Arquivos, aprovacao, pendencia e erro. |
| Linha de conciliacao | Pagamento esperado, recebido, diferenca e acao. |
| Input de valor/moeda | Valor, desconto, multa, parcela e erro. |
| Simulador financeiro | Antes/depois, impacto, risco e aprovacao. |

## Regras De Uso

- Agenda deve mostrar conflito, vaga e capacidade sem exigir abrir cada aula.
- Chamada precisa ser rapida, auditavel e corrigivel.
- Reposicao deve mostrar credito, validade, encaixe e conflito.
- Conflito de recurso deve sempre mostrar impacto.
- Documento deve mostrar status e historico curto.
- Conciliacao deve mostrar diferenca e acao segura.
- Simulacao financeira deve separar proposta, impacto e risco.

## Nao Fazer

- Nao usar calendario compacto quando a decisao exige grade semanal.
- Nao permitir alteracao estrutural de agenda sem auditoria.
- Nao aprovar excecao financeira sem impacto visivel.
- Nao misturar financeiro do aluno com billing Taliya.
- Nao esconder comprovante, contrato ou status de assinatura.

