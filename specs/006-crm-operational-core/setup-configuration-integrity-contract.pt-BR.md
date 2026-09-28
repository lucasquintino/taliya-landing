# Contrato De Integridade Das Configuracoes

Status: rascunho obrigatorio antes das telas de onboarding/configuracoes.
Data: 2026-05-13.

## Objetivo

Garantir que o setup do Taliya seja preciso, simples e integrado.

Este contrato existe para evitar:

- regra duplicada;
- regra contraditoria;
- configuracao perdida que nao afeta o produto;
- complexidade desnecessaria para o studio;
- fluxo de agente usando regra diferente do CRM;
- configuracao sensivel publicada sem validacao;
- mudanca posterior quebrando alunos, aulas, cobrancas ou agentes ativos.

## Principio principal

Toda configuracao precisa ter um dono claro, uma fonte da verdade e uma lista de impactos.

Se uma configuracao nao tiver impacto real em tela, fluxo, agente, tarefa, aprovacao, relatorio ou auditoria, ela nao entra no MVP.

## Regras de integridade

### 1. Uma regra, uma fonte da verdade

Cada regra deve existir em um unico lugar canonico.

Exemplos:

- Regra de reposicao mora na configuracao de Agenda/Reposicoes.
- Regra de consumo de aulas mora em Consumo de Aulas.
- Regra de cobranca mora em Financeiro.
- Regra de autonomia mora no Fluxo do Agente.
- Regra sensivel/versionada mora em Politicas.
- Limite de uso mora em Uso/Cotas.
- Permissao mora em Permissoes.

Outras telas podem exibir ou usar essa regra, mas nao devem criar outra copia.

### 2. Configuracao nao pode ser apenas texto

O agente pode conversar em linguagem simples, mas o sistema deve salvar respostas como dados estruturados.

Exemplo ruim:

- "O studio costuma quebrar galho para aluno antigo."

Exemplo correto:

- permitir_excecao_manual_de_reposicao: sim;
- exige_justificativa: sim;
- exige_auditoria: sim;
- permitido_para_papeis: dono, admin, recepcao;
- agente_pode_executar: nao;
- agente_pode_sugerir: sim.

### 3. Toda configuracao precisa declarar impacto

Cada configuracao deve dizer:

- quais paginas usam;
- quais fluxos do CRM usam;
- quais agentes usam;
- quais casos de uso mudam;
- quais tarefas podem ser criadas;
- quais aprovacoes podem aparecer;
- quais cotas podem ser consumidas;
- qual auditoria sera registrada.

Se nao for possivel responder isso, a configuracao esta mal definida.

### 4. Toda regra sensivel precisa de validacao antes de publicar

Regra sensivel inclui:

- cobranca;
- consumo de aulas;
- reposicao;
- inadimplencia;
- desconto;
- estorno;
- cancelamento;
- autonomia de agente;
- mensagem externa automatica;
- permissao;
- politica operacional;
- cota/economia;
- privacidade.

Essas regras precisam de:

- resumo de impacto;
- exemplo real;
- confirmacao do gestor;
- auditoria;
- possibilidade de revisao posterior.

### 5. O setup publica em camadas

O Taliya nao deve exigir que tudo esteja perfeito para o CRM funcionar.

Camadas de publicacao:

1. CRM manual.
2. Agenda.
3. Financeiro.
4. Canais/modelos de mensagem.
5. Regras de seguranca, aprovacoes e excecoes.
6. Agentes preparados.
7. Pendencias de Agentes/Fluxos pos-go-live.

Cada camada tem criterios proprios.

### 6. Autonomia e sempre a ultima camada

No setup inicial, um fluxo autonomo nao e publicado. O setup apenas registra rascunho/pendencia para Agentes/Fluxos.

Depois do go-live, um fluxo autonomo so pode ser publicado se:

- a regra operacional existe;
- a politica esta publicada;
- o canal esta conectado;
- o template esta aprovado;
- a permissao permite;
- a cota permite;
- o fallback manual existe;
- o simulador passou;
- o gestor aprovou.

Se faltar algo, o fluxo pode ficar manual ou copiloto, mas nao autonomo.

### 7. 0 agentes nunca pode quebrar o CRM

Com 0 agentes:

- CRM manual funciona;
- tarefas funcionam;
- checklists funcionam;
- aprovacoes funcionam;
- agenda funciona;
- financeiro funciona;
- configuracoes continuam uteis;
- agentes aparecem apenas como upgrade/preparacao futura.

Nenhuma configuracao essencial do CRM deve depender da existencia de agente.

### 8. Configuracao avancada nao entra no caminho principal

O setup deve perguntar pouco.

Configuracoes avancadas ficam em:

- "ajustes avancados";
- "editar regra";
- "ver detalhes";
- "configurar excecao";
- suporte Taliya;
- reconfiguracao posterior.

O caminho principal usa presets, perguntas simples e previa de impacto.

### 9. Mudanca depois do go-live precisa de impacto

Se o studio muda uma regra publicada, o sistema deve mostrar:

- o que muda daqui para frente;
- se afeta dados antigos;
- se afeta alunos com reposicoes abertas;
- se afeta cobrancas ja geradas;
- se afeta fluxos ativos;
- se algum agente precisa pausar;
- se existe rollback.

### 10. Nenhuma regra deve ser inferida sem confirmacao

O agente pode sugerir.
O sistema pode inferir um rascunho.
O gestor precisa confirmar antes de publicar.

## Precedencia de regras

Quando duas regras parecem se sobrepor, a ordem deve ser:

1. Restricao legal/privacidade.
2. Permissao do usuario.
3. Plano/entitlement Taliya.
4. Cota/limite de uso.
5. Politica operacional publicada.
6. Regra especifica do aluno.
7. Regra do plano do aluno.
8. Regra da turma/aula.
9. Regra padrao do studio.
10. Default seguro do sistema.

Essa ordem evita conflito.

Exemplo:

- Studio permite reposicao automatica.
- Mas aluno esta sem consentimento de WhatsApp.
- Resultado: nao envia mensagem automatica.

## Tipos de configuracao

### Configuracao estrutural

Define base do studio.

Exemplos:

- unidade;
- horario;
- equipe;
- papel;
- permissao;
- sala;
- professor;
- canal.

### Configuracao operacional

Define como o studio trabalha.

Exemplos:

- regra de falta;
- reposicao;
- no-show;
- cobranca;
- consumo de aula;
- inadimplencia;
- vendas;
- retencao.

### Configuracao de agente

Define como um agente pode participar.

Exemplos:

- fluxo ativo;
- modo manual/copiloto/autonomo;
- responsavel;
- aprovador;
- limite de tentativas;
- fallback;
- template usado;
- janela de envio.

### Configuracao de controle

Define seguranca, custo e governanca.

Exemplos:

- politica;
- cota;
- economia;
- auditoria;
- billing;
- privacidade;
- integracao.

## Perguntas que toda configuracao precisa responder

Antes de entrar no produto, cada configuracao precisa responder:

1. Qual problema do studio ela resolve?
2. Ela e obrigatoria para o MVP?
3. Quem e a fonte da verdade?
4. Qual tela edita?
5. Quais telas exibem?
6. Quais fluxos usam?
7. Quais agentes usam?
8. O que acontece com 0 agentes?
9. O que muda com 1, 3 ou 7 agentes?
10. Pode ser manual?
11. Pode ser copiloto?
12. Pode ser autonomo?
13. Precisa aprovacao?
14. Precisa previa de impacto agora ou simulacao pos-go-live?
15. Precisa auditoria?
16. Pode ser publicada parcialmente?
17. Tem rollback?
18. O que acontece se faltar dado?

Se a resposta nao for clara, a configuracao nao deve ir para tela ainda.

## Validacoes obrigatorias do sistema

Antes de publicar, o sistema deve validar:

- campos obrigatorios;
- dependencias;
- conflito entre regras;
- permissao do usuario;
- plano contratado;
- cota disponivel;
- canal conectado;
- modelo de mensagem aprovado;
- politica publicada;
- fallback manual;
- impacto em fluxos ativos;
- risco de autonomia;
- necessidade de auditoria.

## Como evitar duplicidade

Para cada nova configuracao proposta, verificar:

1. Ja existe uma regra equivalente?
2. Ela e apenas uma variacao de uma regra existente?
3. Pode ser representada por preset?
4. Pode ser excecao em vez de regra nova?
5. Pode ficar como campo avancado?
6. Precisa mesmo aparecer no setup inicial?

Se a resposta for "sim" para 1, 2, 3 ou 4, nao criar configuracao nova.

## Como evitar complexidade desnecessaria

Uma configuracao so entra no caminho principal se:

- for usada por muitos studios;
- for necessaria para operar;
- evitar erro grave;
- desbloquear automacao;
- afetar dinheiro, aula, aluno, mensagem ou permissao.

Caso contrario:

- vira default seguro;
- vai para avancado;
- fica para pos-MVP;
- ou e removida.

## Integracao obrigatoria com o sistema

Toda configuracao publicada deve alimentar pelo menos uma destas areas:

- Hoje;
- Agenda;
- Aulas;
- Reposicoes;
- Alunos;
- Financeiro;
- Vendas;
- Retencao;
- Inbox/Conversas;
- Tarefas;
- Checklists;
- Aprovacoes;
- Agentes/Fluxos;
- Uso/Cotas;
- Politicas;
- Auditoria;
- Relatorios.

Configuracao que nao alimenta nada vira ruido e nao entra.

## Resultado esperado do setup

Ao final do setup, o sistema deve conseguir dizer:

- CRM manual esta pronto ou nao;
- quais areas estao publicadas;
- quais areas estao pendentes;
- quais agentes ficaram preparados;
- quais pacotes de fluxos ficaram como rascunho/pendencia;
- quais configuracoes profundas devem ir para Agentes/Fluxos pos-go-live;
- quais regras, politicas ou dados impedem autonomia futura;
- quais cotas podem limitar execucao depois;
- quais configuracoes precisam revisao.

Toda pendencia deve ser persistida como objeto rastreavel com area, motivo, responsavel, destino, prioridade, status e indicacao se bloqueia publicacao. Pendencia sem destino claro vira ruido e nao deve ser criada.

## Checklist de seguranca antes de desenhar telas

Antes de criar imagens/telas de onboarding, precisamos ter:

- inventario de configuracoes;
- fonte da verdade de cada regra;
- precedencia entre regras;
- matriz de impacto;
- arvore adaptativa;
- regras de publicacao parcial;
- cenarios de teste;
- estados de erro/bloqueio;
- estrategia de reconfiguracao pos-go-live.

Sem isso, a UI pode parecer bonita, mas o produto fica fragil.
