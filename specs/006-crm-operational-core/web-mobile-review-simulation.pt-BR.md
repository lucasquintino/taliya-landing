# Revisao web + mobile com simulacao de uso - PT-BR

> Status: revisao consolidada depois dos ajustes de mobile. Este documento lista as paginas web, telas do app e simula o uso como gestor/equipe de studio de Pilates.

## Veredito

Agora o mapa esta coerente.

O ajuste importante desta rodada foi alinhar:

- setup inicial tambem no app;
- configuracao essencial de agentes tambem no app;
- configuracao avancada, auditoria longa e simulacao profunda no web.

Decisao final:

```text
web = completo, profundo, governanca e configuracao avancada
mobile = ativa o studio e opera o dia a dia
```

## Paginas/superficies web

Total: 38.

1. Onboarding e configuracao inicial
2. Hoje
3. Inbox e conversas
4. Contatos
5. Qualidade de dados
6. Alunos e perfil do aluno
7. Historico do aluno
8. Professor e notas
9. Agenda
10. Grade, turmas e eventos
11. Aula e chamada
12. Reposicoes e lista de espera
13. Interessados e vendas
14. Aulas experimentais
15. Matriculas
16. Vendas e origens
17. Financeiro
18. Movimentacoes financeiras
19. Excecoes financeiras sensiveis sem pagina propria
20. Contratos e documentos financeiros
21. Retencao
22. Cancelamentos e reativacao
23. Reclamacoes e casos sensiveis
24. Jornadas e operacao
25. Tarefas e operacao
26. Aprovacoes
27. Agentes e fluxos
28. Execucoes e incidentes de agentes
29. Uso, cotas e economia
30. Relatorios e exportacoes
31. Configuracoes
32. Politicas operacionais
33. Recursos, feriados e disponibilidade
34. Segmentos e comunicados
35. Integracoes
36. Auditoria
37. Privacidade e solicitacoes
38. Assinatura e billing

## Telas/visoes do app mobile

Total: 51.

### Setup e configuracao essencial

1. Setup inicial
2. Importacao assistida
3. Configuracao inicial de agentes
4. Configuracao rapida de fluxo
5. Configuracoes essenciais

### Comando e navegacao

6. Hoje
7. Checklist do dia
8. Notificacoes
9. Busca global

### Atendimento

10. Inbox
11. Conversa
12. Contato rapido
13. Falhas de envio

### Agenda, turmas e aulas

14. Agenda
15. Turmas
16. Aula
17. Chamada
18. Reposicoes
19. Lista de espera
20. Eventos/workshops
21. Recursos e disponibilidade

### Alunos, professor e historico

22. Alunos
23. Perfil do aluno
24. Historico permitido
25. Professor

### Vendas e matriculas

26. Interessados
27. Experimental
28. Matricula rapida
29. Origens e indicacoes
30. Segmentos e comunicados

### Financeiro

31. Financeiro essencial
32. Pagamento/cobranca
33. Excecoes financeiras via aprovacao/tarefa contextual
34. Contratos/documentos

### Operacao, retencao e casos

35. Tarefas
36. Aprovacoes
37. Caso operacional
38. Jornadas prioritarias
39. Qualidade de dados
40. Retencao
41. Cancelamentos e reativacao
42. Reclamacao/caso sensivel

### Agentes, cotas e governanca leve

43. Agentes/alertas
44. Agentes e fluxos
45. Execucao de agente
46. Cotas
47. Relatorios resumidos
48. Auditoria resumida
49. Privacidade/solicitacoes
50. Integracoes/status
51. Assinatura/billing

## Simulacao como gestor de studio

### Cenario 1 - Compra e ativacao

O gestor compra o plano e abre o celular.

Precisa conseguir:

- ativar conta;
- preencher dados do studio;
- definir horarios basicos;
- conectar/testar canal essencial;
- importar dados simples ou continuar depois;
- resolver duplicidade basica;
- convidar equipe;
- configurar agente inicial;
- testar exemplo;
- abrir o CRM.

Status: coberto.

Telas usadas:

- Setup inicial;
- Importacao assistida;
- Configuracoes essenciais;
- Configuracao inicial de agentes;
- Configuracao rapida de fluxo;
- Agentes e fluxos.

### Cenario 2 - Inicio de um dia comum

O gestor abre o app antes das aulas.

Precisa ver:

- aulas de hoje;
- turmas com vaga/conflito;
- chamadas pendentes;
- reposicoes sem resposta;
- conversas aguardando humano;
- interessados quentes;
- pagamentos urgentes;
- aprovacoes pendentes;
- agentes bloqueados;
- cota perto do limite;
- checklist de abertura.

Status: coberto.

Telas usadas:

- Hoje;
- Checklist do dia;
- Agenda;
- Turmas;
- Reposicoes;
- Inbox;
- Aprovacoes;
- Cotas;
- Agentes/alertas.

### Cenario 3 - Rotina de aula

Professor/recepcao precisa operar aula sem computador.

Precisa conseguir:

- abrir turma;
- abrir aula;
- ver alunos esperados;
- consultar contexto permitido;
- fazer chamada;
- registrar falta/no-show;
- gerar reposicao;
- registrar observacao;
- ver sala/professor indisponivel;
- avisar turma quando permitido.

Status: coberto.

Telas usadas:

- Agenda;
- Turmas;
- Aula;
- Chamada;
- Perfil do aluno;
- Historico permitido;
- Professor;
- Recursos e disponibilidade.

### Cenario 4 - Atendimento no WhatsApp

Recepcao recebe mensagem.

Precisa conseguir:

- ver conversa;
- assumir do agente;
- responder;
- editar sugestao;
- abrir aluno/interessado;
- criar tarefa;
- abrir caso;
- registrar opt-out;
- tratar falha de envio simples.

Status: coberto.

Telas usadas:

- Inbox;
- Conversa;
- Contato rapido;
- Falhas de envio;
- Perfil do aluno;
- Interessados;
- Tarefas;
- Caso operacional.

### Cenario 5 - Turma com vaga e reposicao

Uma turma tem vaga e existem alunos com credito de reposicao.

Precisa conseguir:

- ver turma com vaga;
- ver candidatos;
- encontrar encaixe;
- convidar aluno;
- reservar vaga;
- consumir credito;
- acompanhar resposta;
- criar tarefa se nao resolver.

Status: coberto.

Telas usadas:

- Hoje;
- Turmas;
- Reposicoes;
- Lista de espera;
- Conversa;
- Tarefas.

### Cenario 6 - Lead e experimental

Interessado responde no WhatsApp e quer aula experimental.

Precisa conseguir:

- abrir interessado;
- qualificar rapidamente;
- agendar experimental;
- enviar lembrete;
- registrar falta/remarcacao;
- fazer pos-aula;
- converter ou criar tarefa.

Status: coberto.

Telas usadas:

- Inbox;
- Conversa;
- Interessados;
- Experimental;
- Matricula rapida;
- Tarefas.

### Cenario 7 - Financeiro urgente

Aluno esta atrasado ou mandou comprovante.

Precisa conseguir:

- ver atraso;
- abrir pagamento/cobranca;
- enviar link;
- confirmar comprovante;
- registrar promessa;
- abrir aprovacao para excecao;
- ver contrato/documento se necessario.

Status: coberto.

Telas usadas:

- Hoje;
- Financeiro essencial;
- Pagamento/cobranca;
- Excecoes financeiras via aprovacao/tarefa contextual;
- Contratos/documentos;
- Aprovacoes.

### Cenario 8 - Retencao, cancelamento e reclamacao

Aluno em risco ou reclamacao sensivel aparece fora do escritorio.

Precisa conseguir:

- ver risco;
- abrir aluno;
- criar tarefa;
- preparar contato;
- registrar motivo de cancelamento;
- abrir plano de salvamento;
- pausar automacao;
- responder/escala reclamacao;
- acompanhar recuperacao.

Status: coberto.

Telas usadas:

- Retencao;
- Cancelamentos e reativacao;
- Reclamacao/caso sensivel;
- Perfil do aluno;
- Tarefas;
- Aprovacoes.

### Cenario 9 - Agente falha ou cota trava

Um fluxo falha, a cota chega a limite ou automacao precisa ser pausada.

Precisa conseguir:

- ver alerta;
- abrir execucao;
- entender erro;
- pausar emergencia;
- abrir incidente;
- reprocessar se seguro;
- ver cota e motivo do bloqueio;
- ajustar modo/limite simples;
- abrir web para regra avancada.

Status: coberto.

Telas usadas:

- Agentes/alertas;
- Execucao de agente;
- Agentes e fluxos;
- Cotas;
- Caso operacional.

### Cenario 10 - Solicitacao sensivel

Pedido de privacidade, opt-out ou acesso de suporte surge.

Precisa conseguir:

- ver solicitacao;
- validar contexto;
- aprovar/negar;
- expirar acesso de suporte;
- abrir auditoria resumida;
- deixar trilha.

Status: coberto para decisao mobile controlada.

Telas usadas:

- Privacidade/solicitacoes;
- Auditoria resumida;
- Aprovacoes.

## Lacunas restantes

Nao encontrei uma area grande faltando depois da revisao.

O que ainda falta nao e mais "tem tela ou nao tem tela". Agora falta especificacao fina:

- campos por tela;
- botoes por estado;
- permissao por papel;
- estados vazios/erro/carregando;
- regras de cota por acao;
- detalhes de auditoria por acao sensivel;
- limites exatos do que o app permite publicar sem abrir o web.

## Conclusao

Com a revisao atual:

```text
web tem 38 paginas/superficies;
mobile tem 51 telas/visoes;
simulacao de uso diario nao encontrou lacuna grande de cobertura.
```

O produto esta no caminho certo para cobrir a rotina real do studio.

Proxima etapa:

```text
especificar tela a tela: campos, botoes, estados, permissoes, cotas, IA e auditoria.
```
