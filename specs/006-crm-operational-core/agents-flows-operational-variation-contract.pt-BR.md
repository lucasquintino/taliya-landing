# Taliya CRM - Contrato Operacional Das Variacoes De Agentes/Fluxos

Status: contrato funcional v1.0.
Data: 2026-05-23.

## Objetivo

Detalhar 100% como as variacoes operacionais de Agentes/Fluxos aparecem e se comportam, sem gerar imagens novas.

Este documento transforma as telas aprovadas em estados implementaveis.

As variacoes usam os mesmos layouts ja aprovados:

- `/app/agentes`;
- `/app/agentes/[agentId]`;
- `/app/agentes/[agentId]/rotinas/[routineId]`;
- `/app/agentes/[agentId]/rotinas/[routineId]/fluxos/[flowId]`;
- `/app/agentes/[agentId]/rotinas/[routineId]/fluxos/[flowId]/simular`;
- `/app/agentes/[agentId]/rotinas/[routineId]/publicar`.

Nao criar imagem nova para cada variacao.

## Variacoes Obrigatorias

Este contrato detalha:

1. rotina bloqueada para publicar;
2. rotina com simulacao desatualizada;
3. fluxo sem integracao;
4. fluxo com cota insuficiente;
5. fluxo com aprovacao pendente;
6. fluxo pausado;
7. rotina publicada;
8. rotina publicada com uma excecao aberta;
9. plano 0 agentes vendo partes bloqueadas/upgrade;
10. plano 1 agente vendo partes bloqueadas/upgrade;
11. plano 3 agentes vendo partes bloqueadas/upgrade;
12. plano 7 agentes como estado completo de referencia.

## Regra De Produto

Agentes/Fluxos nunca pode bloquear o CRM base.

Quando uma automacao nao pode rodar:

- a operacao manual continua;
- a UI explica o motivo;
- a correcao acontece na fonte certa;
- o Agente de Configuracao explica, mas nao publica, retoma ou aprova sozinho;
- auditoria registra o motivo e a decisao.

## Hierarquia De Estados

Quando varios estados acontecem ao mesmo tempo, a UI deve mostrar o motivo mais bloqueante primeiro.

Ordem de prioridade:

| Prioridade | Estado | Por que vem antes |
|---|---|---|
| 1 | Plano nao contratado | Sem entitlement, a automacao nao pode ser configurada como ativa. |
| 2 | Pausado por incidente | Existe risco operacional ou falha aberta que impede retomada comum. |
| 3 | Pausado por usuario | Usuario decidiu parar; respeitar a pausa antes de outros avisos. |
| 4 | Permissao insuficiente | Usuario atual nao pode executar a decisao. |
| 5 | Integracao/canal indisponivel | Fluxo que depende de canal externo nao consegue agir. |
| 6 | Cota insuficiente | Autonomia paga/uso de agente fica bloqueada ou degradada. |
| 7 | Dado obrigatorio ausente | Fluxo nao tem contexto minimo para rodar com seguranca. |
| 8 | Template/regra sem aprovacao | Mensagem/regra ainda nao pode ser usada em operacao. |
| 9 | Simulacao desatualizada | Configuracao mudou depois da ultima simulacao. |
| 10 | Aprovacao pendente | Fluxo pode estar pronto, mas aguarda decisao humana. |
| 11 | Excecao aberta | Algo saiu do caminho comum, mas pode nao bloquear a rotina inteira. |

Se dois estados tiverem a mesma prioridade, mostrar no preflight todos os motivos, mas o chip principal usa o primeiro bloqueio da lista.

## Componentes Reutilizados

### Chips De Header

Chips devem ser curtos e objetivos.

| Estado | Chip principal | Cor sugerida | Onde aparece |
|---|---|---|---|
| pronto | `Pronto` | verde | fluxo, rotina, publicar |
| pronto para publicar | `Pronta para publicar` | verde | publicar |
| publicado | `Publicada` | verde | agente, rotina |
| bloqueado | `Bloqueada` | vermelho/laranja | rotina, publicar |
| simulacao desatualizada | `Simulacao desatualizada` | amarelo/laranja | rotina, publicar |
| integracao pendente | `Integracao pendente` | amarelo/laranja | fluxo, rotina, publicar |
| cota insuficiente | `Cota insuficiente` | vermelho/laranja | fluxo, rotina, publicar |
| aprovacao pendente | `Aprovacao pendente` | amarelo | fluxo, rotina, publicar |
| pausado | `Pausado` | cinza/laranja | fluxo, rotina, agente |
| excecao aberta | `1 excecao aberta` | laranja | rotina, Hoje |
| nao contratado | `Nao contratado` | cinza | catalogo, agente, rotina |
| preview | `Preview` | cinza/azul | plano 0/upgrade |

### Preflight Compacto

Preflight nao e formulario.

Ele mostra somente dependencias e bloqueios.

Itens possiveis:

- plano contratado;
- agente contratado;
- permissao do usuario;
- integracao/canal;
- template/regra aprovada;
- responsaveis/aprovadores definidos;
- cota disponivel;
- dados obrigatorios;
- simulacao valida;
- auditoria ativa;
- ausencia de incidente bloqueante.

### Agente De Configuracao

Aparece somente em paginas onde ha configuracao, simulacao ou publicacao:

- pagina da rotina;
- pagina do fluxo;
- simular fluxo;
- publicar rotina.

Nao aparece em:

- catalogo de agentes;
- pagina do agente.

O painel direito sempre deve responder:

1. por que este estado existe;
2. o que esta bloqueado;
3. o que continua funcionando manualmente;
4. qual o proximo passo seguro;
5. o que ele nao pode fazer sozinho.

### Caminho Manual

Toda variacao bloqueada deve indicar o caminho manual quando existir.

Exemplos:

- falta com aviso sem WhatsApp: `Registrar falta manualmente na aula`;
- cota insuficiente: `Criar tarefa para recepcao`;
- agente nao contratado: `Continuar usando tarefas e agenda manual`;
- aprovacao pendente: `Aguardar aprovacao ou cancelar pedido`.

## Contrato Por Variacao

### 1. Rotina Bloqueada Para Publicar

Estado canonico:

```text
blocked_to_publish
```

Fonte da verdade:

```text
Agentes/Fluxos + preflight consolidado de Billing, Integracoes, Uso/Cotas, Permissoes e Auditoria
```

Pagina principal:

```text
/app/agentes/[agentId]/rotinas/[routineId]/publicar
```

Quando acontece:

- simulacao da rotina esta ausente;
- simulacao ficou desatualizada;
- um ou mais fluxos tem integracao obrigatoria indisponivel;
- cota esta insuficiente para publicar autonomia;
- usuario nao tem permissao de publicacao;
- plano nao inclui agente/rotina/fluxo;
- template/regra exigida nao esta aprovada;
- responsavel por excecao/aprovacao obrigatorio esta ausente;
- existe incidente que pausou a rotina ou fluxo essencial.

Como aparece no header:

```text
[Mais autonomo] [4 fluxos] [Simulacao pendente] [Bloqueada para publicar]
```

Se a causa for uma unica:

```text
[Mais autonomo] [4 fluxos] [Simulacao desatualizada] [Bloqueada para publicar]
```

Bloco de preflight:

Titulo:

```text
Bloqueada para publicar
```

Texto:

```text
Resolva os itens abaixo antes de colocar esta rotina em operacao.
```

Lista:

- item bloqueante;
- fonte da verdade;
- fluxo afetado;
- CTA de correcao.

Exemplo:

| Item | Fonte | Fluxo afetado | CTA |
|---|---|---|---|
| WhatsApp desconectado | Integracoes | Confirmacao de presenca, Falta com aviso | `Abrir integracao` |
| Simulacao desatualizada | Agentes/Fluxos | Falta com aviso | `Simular novamente` |
| Cota insuficiente | Uso/Cotas | Todos autonomos | `Ver cotas` |

Cards dos fluxos:

- fluxo pronto continua mostrando seu resumo;
- fluxo bloqueado mostra chip do motivo;
- fluxo configurado como Manual mostra `Manual planejado`;
- qualquer fluxo bloqueado para o modo configurado mostra `Bloqueia a publicacao`.

CTA principal:

| Condicao | CTA principal |
|---|---|
| qualquer fluxo bloqueado | `Corrigir bloqueios` |
| apenas simulacao desatualizada | `Simular novamente` |
| permissao insuficiente | `Pedir acesso` |

CTAs secundarios:

- `Voltar para ajustes`;
- `Ver fluxo`;
- `Simular fluxo`;
- `Ver cotas`;
- `Abrir integracao`;
- `Cancelar publicacao`.

Agente de Configuracao:

Mensagem base:

```text
Esta rotina ainda nao pode ser publicada. A Taliya encontrou bloqueios que impedem a operacao autonoma. O CRM continua funcionando manualmente enquanto voce corrige esses pontos.
```

Sugestoes:

- `O que esta bloqueando a publicacao?`
- `Posso publicar so os fluxos prontos?`
- `O que continua manual?`
- `Qual bloqueio devo resolver primeiro?`

Manual continua:

- tarefas;
- agenda;
- chamadas;
- aprovacoes manuais;
- registros do CRM.

Auditoria:

Registrar:

- usuario que tentou publicar;
- rotina;
- versao do rascunho;
- bloqueios encontrados;
- CTAs acionados.

Nao pode acontecer:

- publicar rotina com gate obrigatorio vermelho;
- esconder qual fluxo causou bloqueio;
- sugerir ajuste de integracao/cota dentro do fluxo;
- chamar bloqueio de erro generico.

Como sai desse estado:

- bloqueio corrigido na fonte;
- nova simulacao valida;
- preflight fica verde;
- usuario autorizado revisa e publica.

### 2. Rotina Com Simulacao Desatualizada

Estado canonico:

```text
simulation_outdated
```

Fonte da verdade:

```text
Agentes/Fluxos / versao do rascunho / resultado da ultima simulacao
```

Paginas:

- pagina da rotina;
- publicar rotina;
- cards do agente, quando relevante.

Quando acontece:

- usuario muda perfil da rotina depois da simulacao;
- usuario muda modo de um fluxo;
- usuario muda ajuste relevante de fluxo;
- template/tom de mensagem muda;
- responsavel/aprovador/fila muda;
- regra/politica usada pelo fluxo muda;
- integracao volta depois de falhar e precisa novo preflight;
- cota/economia muda o modo permitido.

Como aparece na pagina da rotina:

Header:

```text
[Mais autonomo personalizado] [Simulacao desatualizada]
```

Texto abaixo do status:

```text
Ajustes mudaram depois da ultima simulacao. Simule novamente antes de publicar.
```

Cards dos fluxos:

- fluxos alterados mostram `Alterado depois da simulacao`;
- fluxos nao alterados continuam com status anterior;
- se a rotina tem fluxo personalizado, mostrar `1 fluxo personalizado`.

CTA principal:

```text
Simular rotina
```

CTAs secundarios:

- `Ver alteracoes`;
- `Abrir fluxo alterado`;
- `Descartar rascunho`;
- `Voltar para publicacao`, se veio de publicar.

Como aparece em `Publicar rotina`:

- preflight bloqueado;
- CTA `Simular novamente`;
- cards indicam quais fluxos invalidaram a simulacao.

Agente de Configuracao:

Mensagem base:

```text
A simulacao anterior nao vale mais porque a configuracao mudou. Para publicar com seguranca, a Taliya precisa simular a rotina de novo com os ajustes atuais.
```

Sugestoes:

- `O que mudou desde a ultima simulacao?`
- `Preciso simular todos os fluxos?`
- `Posso descartar as mudancas?`

Manual continua:

- rotina publicada anterior continua rodando, se existir;
- se nao existe rotina publicada, CRM continua manual.

Auditoria:

Registrar:

- campo alterado;
- valor anterior e novo quando permitido;
- usuario;
- horario;
- simulacao invalidada;
- versao de rascunho.

Nao pode acontecer:

- publicar com simulacao antiga;
- mostrar `Pronta para publicar`;
- confundir simulacao de fluxo com simulacao da rotina inteira.

Como sai desse estado:

- `Simular rotina` passa;
- ou usuario descarta rascunho;
- ou usuario volta ajustes para estado previamente simulado.

### 3. Fluxo Sem Integracao

Estado canonico:

```text
flow_missing_integration
```

Fonte da verdade:

```text
Integracoes Tecnicas
```

Paginas:

- pagina do fluxo;
- pagina da rotina;
- publicar rotina;
- Integracoes;
- logs da integracao.

Quando acontece:

- canal externo necessario nao esta conectado;
- provedor esta conectado, mas falhando;
- token expirou;
- webhook esta com erro;
- permissao do provedor nao cobre a acao;
- integracao esta em modo limitado;
- importacao/sincronizacao necessaria nao terminou.

Exemplos:

- WhatsApp desconectado para envio de mensagem;
- Google Agenda indisponivel para sincronizacao;
- provedor financeiro indisponivel para cobranca;
- e-mail desconectado para lembrete.

Como aparece na pagina do fluxo:

Header:

```text
[Autonomo com excecoes] [Precisa ajuste] [Integracao pendente]
```

No bloco `Como funciona neste modo`:

- inicio e meio continuam explicando a operacao normal;
- fim informa que, sem integracao, a acao externa nao roda;
- se o modo permite, mostra caminho manual.

No bloco `Ajustes deste fluxo`:

Nao aparece dropdown de canal/integracao.

Aparece item read-only:

```text
Dependencia: WhatsApp precisa estar conectado em Integracoes.
```

CTA:

```text
Abrir integracao
```

Pagina da rotina:

- card do fluxo mostra chip `Integracao pendente`;
- card explica: `Nao envia mensagem ate WhatsApp voltar`;
- rotina mostra bloqueio se esse fluxo for essencial.

Publicar rotina:

- se a integracao for necessaria para o modo configurado, a rotina fica bloqueada;
- se o fluxo deve operar manualmente, isso precisa estar configurado e simulado como `Manual planejado` antes da publicacao.

Agente de Configuracao:

Mensagem base:

```text
Este fluxo depende de uma integracao externa. Enquanto ela nao estiver funcionando, a Taliya nao executa a parte automatica e mantem a operacao manual.
```

Sugestoes:

- `Qual integracao esta faltando?`
- `O que continua manual?`
- `Posso usar este fluxo em Manual?`
- `Onde vejo os logs?`

Manual continua:

- registrar tarefa;
- criar lembrete interno;
- executar contato fora da automacao;
- registrar resultado no CRM.

Auditoria:

Registrar:

- integracao afetada;
- fluxo afetado;
- tentativa bloqueada;
- erro tecnico resumido;
- link para log tecnico;
- se houve fallback manual.

Nao pode acontecer:

- editar integracao dentro do fluxo;
- mascarar falha como `Pronto`;
- tentar envio autonomo sem canal;
- perder rastro da tentativa.

Como sai desse estado:

- integracao volta a ficar OK;
- preflight revalida;
- se a rotina ja estava publicada, fluxo retoma conforme regra de retomada;
- se mudou configuracao, pode exigir nova simulacao.

### 4. Fluxo Com Cota Insuficiente

Estado canonico:

```text
flow_quota_insufficient
```

Fonte da verdade:

```text
Uso/Cotas + Billing Taliya
```

Paginas:

- pagina do fluxo;
- pagina da rotina;
- publicar rotina;
- Uso/Cotas;
- Hoje, quando critico.

Quando acontece:

- cota mensal acabou;
- cota do agente acabou;
- cota do tipo de acao acabou;
- limite comercial do plano nao permite mais execucao autonoma;
- regra de economia pausou fluxos de baixa prioridade;
- add-on/pacote expirou.

Como aparece na pagina do fluxo:

Header:

```text
[Autonomo com excecoes] [Bloqueado] [Cota insuficiente]
```

No bloco `Como funciona neste modo`:

- explica o comportamento normal;
- acrescenta: `Enquanto a cota estiver insuficiente, este fluxo nao roda em autonomia.`

No bloco de ajustes:

- nao aparece controle de cota fina;
- pode aparecer read-only: `Cota controlada em Uso/Cotas`.

CTA principal:

```text
Ver cotas
```

CTAs secundarios:

- `Usar Manual`;
- `Mudar para Copiloto`, se o plano permitir e se ainda consumir menos;
- `Voltar para rotina`.

Pagina da rotina:

- card do fluxo mostra `Cota insuficiente`;
- rotina pode ficar `Bloqueada para publicar` se os fluxos principais dependem de autonomia;
- se fluxo nao essencial, pode ficar manual.

Publicar rotina:

- preflight mostra `Cota insuficiente`;
- `Publicar rotina` desabilitado quando a promessa publicada seria falsa;
- se a cota for necessaria para o modo configurado, a rotina fica bloqueada;
- fluxos manuais planejados nao dependem de cota de autonomia.

Agente de Configuracao:

Mensagem base:

```text
A cota atual nao permite que este fluxo rode em autonomia. O CRM continua manual e voce pode ver cotas, ajustar economia ou publicar apenas o que ainda pode operar.
```

Sugestoes:

- `O que consumiria cota?`
- `Quais fluxos continuam funcionando?`
- `Como reduzir consumo?`
- `Posso deixar manual por enquanto?`

Manual continua:

- tarefa humana;
- registro manual;
- checklist;
- aprovacao manual.

Auditoria:

Registrar:

- fluxo bloqueado por cota;
- cota restante;
- tipo de cota;
- usuario que tentou publicar/rodar;
- fallback criado;
- decisao de economia.

Nao pode acontecer:

- cobrar/consumir cota em tentativa bloqueada;
- esconder caminho manual;
- rebaixar modo sem explicar;
- vender upgrade dentro de tela tecnica como se fosse erro do usuario.

Como sai desse estado:

- nova cota disponivel;
- pacote extra;
- plano alterado;
- regra de economia ajustada;
- fluxo rebaixado para modo permitido.

### 5. Fluxo Com Aprovacao Pendente

Estado canonico:

```text
flow_pending_approval
```

Fonte da verdade:

```text
Aprovacoes + Agentes/Fluxos
```

Paginas:

- pagina do fluxo;
- pagina da rotina;
- publicar rotina;
- Aprovacoes;
- Hoje, se urgente.

Quando acontece:

- fluxo em `Autonomo com aprovacao` preparou uma acao;
- publicacao exige aprovacao do dono/admin;
- alteracao de regra/politica precisa aprovacao;
- correcao de historico esta aguardando decisao;
- mensagem/template sensivel esta aguardando aprovacao;
- excecao foi escalada para aprovador.

Como aparece na pagina do fluxo:

Header:

```text
[Autonomo com aprovacao] [Aprovacao pendente] [Requisitos OK]
```

Bloco `Como funciona neste modo`:

- inicio explica o gatilho;
- meio explica que a Taliya prepara a acao;
- fim deixa claro que a acao nao conclui antes da aprovacao.

CTA principal:

```text
Abrir aprovacao
```

CTAs secundarios:

- `Cancelar pedido`;
- `Ver execucao`;
- `Voltar para rotina`.

Pagina da rotina:

- card do fluxo mostra `Aprovacao pendente`;
- se outros fluxos independentes estao ativos, eles continuam;
- se a aprovacao e obrigatoria para publicar a rotina, a rotina fica bloqueada.

Publicar rotina:

- se aprovacao e para publicar: CTA `Enviar para aprovacao`;
- se aprovacao e ao executar: pode publicar com chip `Aprovacao ao executar`.

Agente de Configuracao:

Mensagem base:

```text
Este fluxo preparou uma acao, mas nao pode concluir sozinho. Uma pessoa autorizada precisa aprovar, editar ou rejeitar antes de seguir.
```

Sugestoes:

- `Quem precisa aprovar?`
- `O que acontece se rejeitar?`
- `O que a Taliya ja preparou?`
- `Isso bloqueia a rotina inteira?`

Manual continua:

- aprovador pode executar manualmente;
- usuario pode cancelar pedido;
- fluxo pode voltar para Manual/Copiloto se fizer sentido.

Auditoria:

Registrar:

- pedido criado;
- dados usados;
- antes/depois;
- aprovadores;
- prazo;
- decisao;
- quem aprovou/rejeitou;
- execucao posterior.

Nao pode acontecer:

- executar acao sensivel antes da aprovacao;
- esconder antes/depois;
- permitir aprovacao por usuario sem permissao;
- duplicar pedido sem indicar substituicao.

Como sai desse estado:

- aprovado e executado;
- aprovado e agendado;
- rejeitado;
- expirado;
- cancelado.

### 6. Fluxo Pausado

Estado canonico:

```text
flow_paused
```

Fonte da verdade:

```text
Agentes/Fluxos, Incidentes ou Billing/Cotas, conforme motivo da pausa
```

Tipos:

- `pausado_usuario`;
- `pausado_incidente`;
- `pausado_plano`;
- `pausado_cota`;
- `pausado_dependencia`.

Paginas:

- pagina do fluxo;
- pagina da rotina;
- pagina do agente;
- Hoje, se critico;
- incidente, quando aplicavel.

Quando acontece:

- usuario pausou manualmente;
- incidente pausou automaticamente;
- downgrade removeu direito de uso;
- cota zerou e regra pausou automacao;
- integracao ficou indisponivel e regra manda pausar;
- rollback deixou fluxo fora da versao ativa.

Como aparece na pagina do fluxo:

Header:

```text
[Autonomo com excecoes] [Pausado] [Motivo: usuario]
```

Se incidente:

```text
[Autonomo com excecoes] [Pausado por incidente] [Ver incidente]
```

Bloco `Como funciona neste modo`:

- mostra configuracao publicada, mas informa que nao esta executando;
- explica o que acontece se um gatilho chegar durante a pausa.

Texto obrigatorio:

```text
Enquanto pausado, a Taliya nao executa este fluxo. Novos casos seguem pelo caminho manual ou viram tarefa, conforme a regra da rotina.
```

CTA principal:

| Tipo de pausa | CTA |
|---|---|
| usuario | `Retomar fluxo` |
| incidente | `Ver incidente` |
| plano | `Ver planos` |
| cota | `Ver cotas` |
| dependencia | `Abrir integracao` |

CTAs secundarios:

- `Ver execucoes`;
- `Voltar para rotina`;
- `Criar tarefa manual`;
- `Ver auditoria`.

Pagina da rotina:

- card do fluxo mostra `Pausado`;
- rotina mostra quantos fluxos pausados existem;
- se qualquer fluxo publicado estiver pausado, a rotina mostra `Publicada com fluxo pausado` ou `Pausada`, conforme escopo.

Agente de Configuracao:

Mensagem base:

```text
Este fluxo esta pausado. A configuracao continua salva, mas a Taliya nao executa novas acoes ate a retomada autorizada.
```

Sugestoes:

- `Por que este fluxo pausou?`
- `O que acontece com novos casos?`
- `Posso retomar agora?`
- `Precisa simular de novo?`

Manual continua:

- tarefas criadas por fallback;
- equipe executa fora da automacao;
- casos ficam em fila humana.

Auditoria:

Registrar:

- quem pausou;
- motivo;
- escopo;
- execucoes em andamento;
- casos redirecionados;
- tentativa de retomada;
- resultado do preflight de retomada.

Nao pode acontecer:

- agente executar fluxo pausado;
- retomar pausa por incidente sem resolver incidente;
- perder eventos ocorridos durante pausa;
- apagar configuracao publicada.

Como sai desse estado:

- usuario autorizado retoma;
- incidente resolvido;
- preflight passa;
- simulacao e exigida se configuracao mudou ou pausa durou alem do limite definido.

### 7. Rotina Publicada

Estado canonico:

```text
routine_published
```

Fonte da verdade:

```text
Agentes/Fluxos / snapshot versionado / Auditoria
```

Contrato de comportamento pos-publicacao:

```text
agents-flows-post-publication-light-ops-contract.pt-BR.md
```

Pagina principal:

```text
/app/agentes/[agentId]/rotinas/[routineId]
```

Quando acontece:

- rotina foi publicada com sucesso;
- snapshot versionado foi criado;
- preflight estava valido no momento da publicacao;
- auditoria registrou usuario, data e versao.

Como aparece no header:

```text
[Publicada] [v3] [Mais autonomo] [Ultima simulacao valida]
```

Resumo da rotina:

Deve mostrar:

- versao publicada;
- quem publicou;
- quando publicou;
- perfil publicado;
- quantidade de fluxos ativos;
- quantidade de fluxos manuais;
- quantidade de fluxos com aprovacao ao executar;
- ultima simulacao valida;
- proximo check de preflight, se houver.

Cards dos fluxos:

Cada card mostra:

- modo publicado;
- status atual;
- inicio/faz/para ou pede aprovacao resumido;
- ajustes publicados principais;
- onde continua;
- CTA `Ver fluxo`;
- CTA `Simular`;
- CTA contextual `Ver execucoes` quando ja rodou.

CTA principal:

```text
Ver execucoes
```

CTAs secundarios:

- `Pausar rotina`;
- `Simular novamente`;
- `Ajustar rascunho`;
- `Ver auditoria`;
- `Revisar publicacao`.

Agente de Configuracao:

Aparece se a pagina permitir controle/ajuste.

Mensagem base:

```text
Esta rotina esta publicada. A Taliya executa os fluxos conforme a versao ativa e registra execucoes, excecoes e aprovacoes quando acontecerem.
```

Sugestoes:

- `O que esta ativo agora?`
- `Como pausar esta rotina?`
- `Como alterar sem quebrar a versao publicada?`
- `Onde vejo execucoes?`

Manual continua:

- fluxos publicados como Manual;
- excecoes;
- casos que caem em fallback;
- operacao fora do escopo dos agentes.

Auditoria:

Registrar:

- versao publicada;
- snapshot de configuracao;
- simulacao usada;
- preflight;
- usuario publicador;
- diffs contra versao anterior;
- cotas/entitlements no momento.

Nao pode acontecer:

- editar versao publicada direto;
- confundir rascunho com publicado;
- publicar alteracao sem nova simulacao;
- ocultar fluxos manuais/bloqueados.

Como sai desse estado:

- nova versao publicada;
- rotina pausada;
- rotina arquivada;
- downgrade/plano bloqueia;
- incidente pausa.

### 8. Rotina Publicada Com Uma Excecao Aberta

Estado canonico:

```text
routine_published_with_exception
```

Fonte da verdade:

```text
Runtime de Agentes/Fluxos + Tarefas/Aprovacoes/Incidentes
```

Paginas:

- pagina da rotina;
- Hoje;
- Tarefas ou Aprovacoes;
- Incidentes, se excecao virar incidente.

Quando acontece:

- rotina esta publicada e ativa;
- um fluxo encontrou caso fora da regra;
- fluxo chamou humano;
- uma tarefa/aprovacao foi criada;
- o restante da rotina nao necessariamente parou.

Como aparece no header:

```text
[Publicada] [1 excecao aberta]
```

Se a excecao tem severidade:

```text
[Publicada] [1 excecao aberta] [Atencao]
```

Card do fluxo afetado:

- chip `Excecao aberta`;
- texto curto do motivo;
- responsaveis acionados;
- onde continuar.

Exemplo:

```text
Falta com aviso
Excecao aberta
Aluno pediu credito junto com a falta. A Taliya registrou o aviso e chamou a equipe para decidir.
Continua em: Tarefas / Aprovacoes
```

CTA principal:

```text
Resolver excecao
```

CTAs secundarios:

- `Ver execucao`;
- `Abrir tarefa`;
- `Abrir aprovacao`;
- `Pausar fluxo`, se necessario;
- `Ver auditoria`.

Agente de Configuracao:

Mensagem base:

```text
A rotina continua publicada, mas um caso saiu da regra comum. A Taliya parou naquele ponto, chamou a equipe e manteve o restante da rotina operando quando nao havia dependencia.
```

Sugestoes:

- `Por que virou excecao?`
- `Isso pausa a rotina inteira?`
- `Quem precisa resolver?`
- `O que a Taliya ja fez?`

Manual continua:

- responsavel resolve a excecao;
- demais fluxos continuam se independentes;
- se a excecao impedir a promessa da rotina, a rotina mostra `Excecao aberta`; se nao impedir, os demais fluxos continuam.

Auditoria:

Registrar:

- fluxo que gerou excecao;
- runId;
- motivo;
- dados usados;
- responsavel acionado;
- SLA;
- decisao humana;
- retorno para fluxo, se houver.

Nao pode acontecer:

- marcar rotina inteira como falha se a excecao e localizada;
- seguir autonomamente depois de detectar excecao sensivel;
- esconder o que o agente ja fez;
- duplicar tarefas para a mesma excecao.

Como sai desse estado:

- excecao resolvida;
- aprovacao decidida;
- tarefa concluida;
- incidente aberto;
- fluxo/rotina pausado;
- caso expirado com auditoria.

### 9. Plano 0 Agentes Vendo Partes Bloqueadas/Upgrade

Estado canonico:

```text
plan_0_agents
```

Fonte da verdade:

```text
Billing Taliya / entitlements do studio
```

Quando acontece:

- studio esta em plano sem agentes contratados;
- rota de agentes e acessada como catalogo/preview;
- usuario tenta acessar rotina/fluxo por link direto;
- billing informa zero entitlements de agente.

Regra:

Plano 0 nao remove CRM.

O CRM segue manual.

Como aparece:

- catalogo mostra agentes em preview/upgrade;
- agente mostra rotinas em leitura;
- rotina mostra fluxo como sugestao/manual;
- fluxo mostra modos autonomos bloqueados por plano;
- publicacao real nao fica disponivel.

Catalogo `/app/agentes`:

- mostra os 7 agentes como catalogo;
- cards usam `Preview` ou `Disponivel no plano com agentes`;
- CTA principal `Ver como funciona` ou `Ver planos`;
- nao mostra Agente de Configuracao;
- nao mostra cota de agente como se estivesse ativa.

Pagina do agente:

- rotinas aparecem em preview/manual;
- botao `Abrir rotina` pode abrir leitura explicativa;
- nao permite ajustar/publicar automacao;
- pode mostrar exemplos de fluxos e beneficios.

Pagina da rotina:

- perfil pode aparecer bloqueado/read-only;
- cards dos fluxos explicam caminho manual;
- CTA principal deve ser manual/preview, nao publicacao;
- `Simular rotina` pode existir apenas como demonstracao, se ficar claro que nao publica.

Pagina do fluxo:

- modo maximo efetivo e Manual;
- autonomos aparecem bloqueados por plano;
- ajustes de mensagem/agente nao devem parecer ativos.

Publicar rotina:

- nao deve abrir como publicacao real;
- se abrir por link direto, mostra `Plano sem agentes` e CTA `Ver planos`.

Texto base:

```text
Seu CRM esta em modo manual. Os agentes aparecem como preview, mas nenhuma automacao autonoma sera publicada neste plano.
```

Agente de Configuracao:

Nao aparece em catalogo/agente.

Se abrir rotina em modo preview, pode explicar:

```text
Esta rotina esta em preview. Ela mostra como a Taliya poderia operar com agentes, mas neste plano a execucao continua manual.
```

Manual continua:

- agenda;
- tarefas;
- aprovacoes;
- chamadas;
- atendimento manual;
- registros e relatorios do CRM base.

Auditoria:

Registrar apenas acoes reais do CRM manual e cliques de interesse comercial quando necessario. Nao registrar simulacao como execucao de agente.

Nao pode acontecer:

- publicar rotina;
- configurar autonomia real;
- consumir cota de agente;
- bloquear agenda, tarefas, aprovacoes ou CRM base.

Como sai desse estado:

- studio contrata 1, 3 ou 7 agentes;
- entitlements sao atualizados;
- rotinas passam a abrir como configuraveis apenas para os agentes contratados;
- nada e publicado automaticamente apos upgrade.

### 10. Plano 1 Agente Vendo Partes Bloqueadas/Upgrade

Estado canonico:

```text
plan_1_agent
```

Fonte da verdade:

```text
Billing Taliya / agente contratado / entitlements
```

Quando acontece:

- studio contratou exatamente 1 agente;
- usuario abre agente contratado;
- usuario abre agente nao contratado;
- rotina ou fluxo pertence a agente fora do plano;
- encadeamento tenta entrar em area nao contratada.

Regra:

Somente o agente contratado e configuravel.

Como aparece:

- catalogo separa agente contratado de agentes nao contratados;
- agente contratado abre rotinas normalmente;
- agentes nao contratados abrem preview ou tela de upgrade;
- fluxos fora do agente contratado mostram bloqueio por plano;
- publicacao so existe para rotinas do agente contratado.

Catalogo `/app/agentes`:

- agente contratado mostra `Contratado`;
- outros agentes mostram `Nao contratado`;
- CTA do contratado `Abrir agente`;
- CTA dos demais `Ver planos` ou `Trocar agente`, se permitido pelo billing.

Pagina do agente contratado:

- rotinas configuraveis;
- perfil inicial `Mais autonomo`, respeitando teto/preflight;
- publicacao permitida dentro de cota/permissao.

Pagina de agente nao contratado:

- rotinas em preview;
- sem Agente de Configuracao;
- sem CTA de publicacao;
- caminho manual do CRM permanece.

Pagina da rotina de agente nao contratado:

- read-only/preview;
- chips `Nao contratado` e `Manual disponivel`;
- CTA `Ver planos`;
- nao mostrar `Revisar para publicar`.

Fluxos:

- fluxos do agente contratado seguem regras normais;
- fluxos de agentes nao contratados ficam bloqueados por plano;
- se um fluxo encadeia para agente nao contratado, o encadeamento vira tarefa manual/upgrade, nao automacao ativa.

Texto base:

```text
Este agente nao esta no seu plano atual. Voce pode continuar a operacao manualmente e contratar este agente para ativar os fluxos.
```

Agente de Configuracao:

- aparece nas rotinas do agente contratado quando o usuario esta configurando;
- nao aparece nas paginas de agentes nao contratados em preview.

Manual continua:

- areas fora do agente contratado seguem manuais;
- encadeamentos para agente nao contratado viram tarefa/manual;
- operacao do agente contratado segue conforme publicacao e cota.

Auditoria:

Registrar:

- qual agente esta contratado;
- tentativa de abrir/configurar agente nao contratado;
- tentativa de publicar fluxo fora do plano;
- upgrade/troca de agente, se ocorrer.

Nao pode acontecer:

- publicar fluxo de agente nao contratado;
- misturar agentes fora do plano em uma rotina ativa;
- ocultar que o CRM manual continua.

Como sai desse estado:

- studio troca o agente contratado;
- studio faz upgrade para 3 ou 7 agentes;
- agente antes bloqueado passa a abrir rotinas como rascunho, nunca publicado automaticamente.

### 11. Plano 3 Agentes Vendo Partes Bloqueadas/Upgrade

Estado canonico:

```text
plan_3_agents
```

Fonte da verdade:

```text
Billing Taliya / bundle de agentes contratados / entitlements
```

Quando acontece:

- studio contratou exatamente 3 agentes;
- usuario abre agente contratado do bundle;
- usuario abre agente fora do bundle;
- rotina de agente contratado encadeia para agente fora do plano;
- publicacao inclui fluxo fora dos entitlements.

Regra:

Tres agentes contratados funcionam completos; demais ficam preview/upgrade.

Como aparece:

- catalogo permite ver todos ou somente contratados;
- tres agentes contratados tem rotinas configuraveis;
- agentes fora do bundle ficam em preview/upgrade;
- rotinas contratadas podem ter fluxos manuais por encadeamento fora do plano;
- publicacao mostra exatamente o que entra e o que fica manual.

Catalogo `/app/agentes`:

- cards contratados mostram `Contratado`;
- cards nao contratados mostram `Nao contratado`;
- filtro deve permitir `Todos` e `Contratados`;
- nao transformar em painel de cotas complexo.

Pagina dos agentes contratados:

- rotinas configuraveis;
- perfil `Mais autonomo` como padrao, respeitando limites;
- publicacao por rotina.

Pagina dos agentes nao contratados:

- preview/manual;
- CTA `Ver planos`;
- sem configuracao ativa.

Rotinas:

- rotinas dos agentes contratados podem publicar;
- rotinas fora do plano nao publicam;
- se uma rotina contratada depende de fluxo fora do plano, esse trecho vira manual/upgrade e precisa ficar explicito.

Publicacao:

- publicar somente fluxos dentro dos agentes contratados;
- fluxos fora do plano nao entram na publicacao;
- se a rotina depender de fluxo fora do plano, a rotina fica bloqueada ate o plano mudar ou o fluxo ser configurado como Manual planejado dentro do escopo permitido.

Texto base:

```text
Este plano tem agentes ativos em algumas areas. As areas fora do plano continuam manuais e aparecem como preview/upgrade.
```

Agente de Configuracao:

- aparece apenas nas rotinas/fluxos dos tres agentes contratados;
- nao aparece em previews de agentes fora do plano.

Manual continua:

- agentes fora do bundle;
- fluxos encadeados para agente nao contratado;
- rotinas bloqueadas por plano;
- qualquer fluxo que falhar preflight.

Auditoria:

Registrar:

- bundle ativo;
- publicacoes feitas nos agentes contratados;
- fluxos deixados manuais por estarem fora do plano;
- tentativas de publicar fora do plano;
- alteracao de bundle/upgrade.

Nao pode acontecer:

- exigir configuracao dos 96 fluxos;
- publicar fluxo fora do plano;
- esconder fluxos que ficaram manuais;
- mostrar upgrade como erro.

Como sai desse estado:

- upgrade para 7 agentes;
- troca de bundle, se o billing permitir;
- downgrade para 1/0 agente, preservando historico e pausando o que sair do entitlement.

### 12. Plano 7 Agentes Como Estado Completo

Tambem chamado: Plano 7 agentes completo.

Estado canonico:

```text
plan_7_agents
```

Fonte da verdade:

```text
Billing Taliya / entitlements completos
```

Quando acontece:

- studio contratou 7 agentes;
- todos os cards do catalogo estao liberados;
- usuario configura qualquer rotina dentro dos sete agentes;
- bloqueios restantes vem de cota, permissao, integracao, simulacao, aprovacao ou incidente, nao de plano.

Regra:

Todos os agentes estao contratados, mas cada fluxo ainda depende de:

- modo permitido;
- teto;
- permissao;
- integracao;
- cota;
- simulacao;
- publicacao;
- aprovacao;
- fallback;
- auditoria.

Como aparece:

- catalogo mostra os 7 agentes ativos;
- pagina do agente mostra somente rotinas;
- pagina da rotina mostra perfil, fluxos e estados;
- fluxo mostra modo, ajustes e preflight;
- publicacao mostra preflight completo, mesmo com todos os agentes contratados.

Catalogo `/app/agentes`:

- todos os 7 cards ativos;
- sem painel direito;
- sem resumo grande duplicado;
- foco em abrir agente.

Pagina do agente:

- lista de rotinas;
- status por rotina;
- sem configuracao do agente.

Rotina:

- perfil `Mais autonomo` sugerido;
- ajustes individuais por fluxo quando necessario;
- status e bloqueios claros.

Publicacao:

- preflight precisa ser rigoroso;
- todos os bloqueios continuam podendo existir;
- plano 7 nao ignora cota, integracao, permissao ou aprovacao.

Texto base:

```text
Todos os agentes estao contratados. A publicacao ainda depende dos requisitos de cada rotina e fluxo.
```

Agente de Configuracao:

- aparece em rotina, fluxo, simulacao e publicacao;
- nao aparece no catalogo nem na pagina do agente.

Manual continua:

- fluxos configurados como Manual;
- excecoes;
- aprovacoes;
- fallbacks;
- areas do CRM fora de um fluxo publicado.

Auditoria:

Registrar:

- publicacoes por rotina;
- mudancas de modo;
- simulacoes;
- execucoes;
- pausas;
- excecoes;
- cotas;
- incidentes.

Nao pode acontecer:

- assumir que plano 7 publica tudo automaticamente;
- virar control plane tecnico;
- esconder bloqueios por integracao/cota/permissao.

Como sai desse estado:

- downgrade para 3/1/0 agentes;
- agentes removidos ficam pausados/bloqueados por plano;
- historico e auditoria permanecem consultaveis;
- nenhuma rotina removida do plano continua autonoma.

## Simular Rotina Como Resultado Consolidado

`Simular rotina` nao precisa de pagina propria agora.

Ela roda a validacao do conjunto e atualiza o estado da pagina da rotina/publicacao.

Contrato completo:

```text
agents-flows-routine-simulation-result-contract.pt-BR.md
```

Resultado minimo:

| Campo | O que mostra |
|---|---|
| status geral | passou, passou com aviso, bloqueada |
| fluxos prontos | quais podem publicar |
| fluxos manuais | quais ficam manuais |
| fluxos bloqueados | motivo e fonte |
| aprovacoes exigidas | quem aprova e quando |
| integracoes | OK, pendente ou falha |
| cota | disponivel, alerta, insuficiente |
| simulacao valida ate | quando a simulacao perde validade, se aplicavel |

CTAs:

- `Revisar para publicar`;
- `Abrir fluxo`;
- `Corrigir bloqueios`;
- `Simular novamente`.

## Publicacao Sempre Completa

Agentes/Fluxos nao tem publicacao parcial de rotina.

Para publicar, a rotina precisa estar 100% pronta para o estado configurado.

Isso nao significa que todos os fluxos precisam ser autonomos.

Significa:

- fluxos configurados como Autonomo estao prontos para autonomia;
- fluxos configurados como Autonomo com excecoes tem excecoes e fallback definidos;
- fluxos configurados como Autonomo com aprovacao tem aprovadores definidos;
- fluxos configurados como Copiloto tem onde entregar sugestao/rascunho;
- fluxos configurados como Manual tem tarefa/checklist/caminho humano definido;
- nenhum fluxo esta bloqueado por plano, permissao, integracao, cota, dado, template, pausa ou simulacao desatualizada.

Se algum fluxo nao estiver pronto para o modo configurado:

```text
A rotina nao publica.
```

Texto obrigatorio:

```text
Esta rotina ainda nao esta pronta para publicar. Resolva os bloqueios ou ajuste o modo dos fluxos afetados e simule novamente.
```

## Pausa, Retomada E Rollback

### Pausar

Ao pausar fluxo ou rotina, mostrar:

- escopo: fluxo ou rotina;
- motivo obrigatorio;
- impacto em casos novos;
- impacto em execucoes em andamento;
- caminho manual;
- quem pode retomar;
- auditoria.

### Retomar

Retomar exige:

- permissao;
- preflight OK;
- incidente resolvido, se houver;
- cota suficiente;
- integracao OK;
- nova simulacao se configuracao mudou.

### Rollback

Rollback volta a configuracao publicada anterior, quando possivel.

Nao desfaz:

- mensagem ja enviada;
- pagamento confirmado;
- dado compartilhado;
- tarefa humana ja concluida;
- aprovacao ja decidida;
- evento auditado.

Rollback deve mostrar:

- versao atual;
- versao anterior;
- diferenca;
- o que volta;
- o que nao volta;
- simulacao exigida;
- auditoria.

## Execucao E Incidente

### Execucao

Toda execucao de fluxo deve poder explicar:

- rotina;
- fluxo;
- versao publicada;
- modo ativo;
- gatilho;
- dados usados;
- checagens;
- acao tomada;
- canal/ferramenta usada;
- cota consumida;
- fallback;
- aprovacao, se houve;
- auditoria;
- proximo passo.

### Incidente

Incidente pode:

- pausar fluxo;
- pausar rotina;
- gerar tarefa de correcao;
- exigir investigacao;
- impedir retomada.

Incidente nao configura regra permanente.

Regra permanente volta para Agentes/Fluxos ou Configuracoes, conforme o caso.

## Checklist De QA

Uma variacao so esta completa se responder:

1. qual estado canonico e usado;
2. qual pagina mostra o estado;
3. qual chip aparece;
4. qual texto explica o motivo;
5. qual CTA principal aparece;
6. quais CTAs secundarios aparecem;
7. qual fonte da verdade corrige o problema;
8. o que continua manual;
9. o que o Agente de Configuracao diz;
10. o que fica auditado;
11. o que nao pode acontecer;
12. como o usuario sai do estado;
13. se bloqueia a rotina inteira ou so um fluxo;
14. como se comporta nos planos 0, 1, 3 e 7.

## Matriz De Completude

| Variacao | Estado | Paginas | Chip | CTA | Manual | Auditoria | Planos |
|---|---|---|---|---|---|---|---|
| rotina bloqueada para publicar | definido | definido | definido | definido | definido | definido | definido |
| rotina com simulacao desatualizada | definido | definido | definido | definido | definido | definido | definido |
| fluxo sem integracao | definido | definido | definido | definido | definido | definido | definido |
| fluxo com cota insuficiente | definido | definido | definido | definido | definido | definido | definido |
| fluxo com aprovacao pendente | definido | definido | definido | definido | definido | definido | definido |
| fluxo pausado | definido | definido | definido | definido | definido | definido | definido |
| rotina publicada | definido | definido | definido | definido | definido | definido | definido |
| rotina publicada com excecao aberta | definido | definido | definido | definido | definido | definido | definido |
| plano 0 agentes bloqueado/upgrade | definido | definido | definido | definido | definido | definido | definido |
| plano 1 agente bloqueado/upgrade | definido | definido | definido | definido | definido | definido | definido |
| plano 3 agentes bloqueado/upgrade | definido | definido | definido | definido | definido | definido | definido |
| plano 7 agentes completo | definido | definido | definido | definido | definido | definido | definido |

## Rodadas De Revisao Deste Contrato

### Rodada 1 - Lista Obrigatoria

Validado contra a lista pedida:

- rotina bloqueada para publicar;
- rotina com simulacao desatualizada;
- fluxo sem integracao;
- fluxo com cota insuficiente;
- fluxo com aprovacao pendente;
- fluxo pausado;
- rotina publicada;
- rotina publicada com uma excecao aberta;
- plano 0/1/3 agentes vendo partes bloqueadas/upgrade.

Resultado: todos os itens estao documentados em secoes proprias.

### Rodada 2 - Campos Obrigatorios Por Variacao

Cada uma das 12 variacoes foi revisada para conter:

- estado canonico;
- fonte da verdade;
- quando acontece;
- como aparece;
- Agente de Configuracao;
- manual continua;
- auditoria;
- o que nao pode acontecer;
- como sai desse estado.

Resultado: nenhuma secao ficou sem campo obrigatorio.

### Rodada 3 - Sem Imagem Nova

Validado:

- as variacoes usam os layouts aprovados;
- nenhuma variacao exige imagem propria;
- a mudanca acontece por chip, texto, preflight, cards, CTAs, bloqueios e painel direito.

Resultado: variações estao prontas para especificacao/implementacao sem novo prompt visual.

### Rodada 4 - Integracao Com Fontes Certas

Validado:

- plano e upgrade ficam em Billing Taliya;
- cota fica em Uso/Cotas;
- canal e provedor ficam em Integracoes;
- aprovacao fica em Aprovacoes;
- pausa por incidente fica em Control Planes;
- configuracao de fluxo fica em Agentes/Fluxos;
- auditoria registra decisao e execucao.

Resultado: o contrato evita duplicar configuracao na pagina errada.
