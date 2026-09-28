# Taliya CRM - Mapa De Estados E Variacoes De Agentes/Fluxos

Status: contrato funcional v0.1.
Data: 2026-05-23.

## Objetivo

Definir como as paginas de Agentes/Fluxos mudam quando a operacao nao esta no caminho feliz.

Este documento cobre:

- plano 0/1/3/7 agentes;
- agente contratado, nao contratado, pausado ou bloqueado;
- rotina em rascunho, simulada, publicada, bloqueada ou pausada;
- fluxo pronto, pendente, bloqueado, pausado, personalizado ou com aprovacao;
- simulacao valida, desatualizada ou bloqueada;
- publicacao pronta ou bloqueada;
- cota, integracao, permissao, dado ausente, incidente, downgrade e rollback.

Ele complementa:

- `agents-flows-routines-pages-final-contract.pt-BR.md`;
- `agents-flows-final-flow-page-contract.pt-BR.md`;
- `agents-flows-test-simulation-page-contract.pt-BR.md`;
- `agents-flows-publish-routine-page-contract.pt-BR.md`;
- `agents-flows-operational-variation-contract.pt-BR.md`;
- `agents-flows-publication-versioning-and-evals.pt-BR.md`;
- `agent-plan-entitlements.pt-BR.md`.

Detalhamento 100% das variacoes:

```text
agents-flows-operational-variation-contract.pt-BR.md
```

Resultado consolidado de `Simular rotina`:

```text
agents-flows-routine-simulation-result-contract.pt-BR.md
```

Operacao leve pos-publicacao nas mesmas paginas:

```text
agents-flows-post-publication-light-ops-contract.pt-BR.md
```

## Regra Central

O CRM nunca quebra por falta de agente.

```text
Sem agente ou com bloqueio = caminho manual/programatico continua.
Agente ativo = copiloto/autonomia so dentro do plano, preflight, cota, permissao, simulacao e publicacao.
```

Agentes/Fluxos deve explicar:

- o que pode rodar agora;
- o que ficou manual;
- o que esta bloqueado;
- onde corrigir;
- como simular de novo;
- como publicar, pausar, retomar ou investigar.

## Variacoes Obrigatorias Sem Nova Imagem

Estas variacoes devem ficar documentadas e implementaveis usando os mesmos layouts ja aprovados.

Nao gerar imagem separada para cada variacao. A tela muda por estado, chip, texto, bloqueio, CTA e conteudo do Agente de Configuracao.

| Variacao | Pagina principal | Como aparece | O que o usuario pode fazer | O que nao pode acontecer |
|---|---|---|---|---|
| Rotina bloqueada para publicar | `Publicar rotina` | Header troca `Pronta para publicar` por `Bloqueada para publicar`; preflight mostra itens vermelhos/amarelos; cards dos fluxos indicam quais impedem a publicacao. | Corrigir bloqueio na origem, simular novamente ou voltar para ajustes. | Botao `Publicar rotina` ativo sem resolver gates obrigatorios. |
| Rotina com simulacao desatualizada | Pagina da rotina e `Publicar rotina` | Chip `Simulacao desatualizada`; texto: `Ajustes mudaram depois da ultima simulacao`; cards afetados indicam o que mudou. | Rodar `Simular rotina` novamente; abrir fluxo alterado; descartar alteracao se existir rascunho. | Publicar usando simulacao antiga. |
| Fluxo sem integracao | Pagina do fluxo, rotina e publicacao | Chip/preflight `Integracao pendente`; detalhe mostra qual integracao/canal falta, por exemplo WhatsApp ou Google Agenda. | Abrir Integracoes, reduzir modo para Manual/Copiloto quando fizer sentido, manter operacao manual. | Transformar canal/integracao em campo editavel do fluxo. |
| Fluxo com cota insuficiente | Pagina do fluxo, rotina, publicacao e Uso/Cotas | Chip `Cota insuficiente`; explicacao simples do impacto: autonomia bloqueada, manual continua. | Ver cotas, comprar pacote/ajustar economia se disponivel, rodar manualmente ou rebaixar modo. | Travar CRM base ou esconder o caminho manual. |
| Fluxo com aprovacao pendente | Pagina da rotina, fluxo, publicacao e Aprovacoes | Chip `Aprovacao pendente`; card mostra quem precisa aprovar e o que sera decidido. | Abrir aprovacao, reenviar para aprovador, cancelar pedido, continuar outros fluxos se independentes. | Executar a acao sensivel antes da aprovacao. |
| Fluxo pausado | Pagina do fluxo e rotina | Chip `Pausado`; ajustes podem ficar read-only; mostra motivo, quem pausou e desde quando. | Retomar se tiver permissao e preflight OK, ver execucoes, ver incidente se a pausa veio de incidente. | Rodar autonomo enquanto pausado. |
| Rotina publicada | Pagina da rotina | Header mostra `Publicada`; inclui versao, data, usuario, ultima simulacao valida, fluxos ativos e fluxos manuais/bloqueados. | Ver execucoes, pausar rotina, simular novamente, ajustar rascunho sem mexer na versao publicada. | Editar a versao publicada diretamente sem novo rascunho/simulacao/publicacao. |
| Rotina publicada com uma excecao aberta | Pagina da rotina, Hoje, Incidentes/Tarefas quando aplicavel | Header continua `Publicada`, mas adiciona chip `1 excecao aberta`; card do fluxo afetado mostra `Resolver excecao`. | Resolver excecao, abrir tarefa/aprovacao/incidente, manter outros fluxos ativos se nao dependem dela. | Marcar rotina inteira como quebrada se a excecao for localizada. |
| Plano 0 agentes vendo partes bloqueadas/upgrade | Catalogo, agente e rotina | Cards de agentes como catalogo/preview; rotinas em leitura/manual; CTAs de plano sem impedir operacao manual. | Operar CRM manualmente, ver como funcionaria, acessar planos. | Configurar/publicar automacao autonoma. |
| Plano 1 agente vendo partes bloqueadas/upgrade | Catalogo, agente e rotina | Agente contratado abre; outros agentes mostram `Nao contratado`; fluxos fora do agente ficam preview/upgrade. | Configurar rotinas do agente contratado; operar demais areas manualmente; ver planos. | Misturar fluxos de agente nao contratado em publicacao ativa. |
| Plano 3 agentes vendo partes bloqueadas/upgrade | Catalogo, agente e rotina | Tres agentes contratados abrem; demais ficam como upgrade/preview; filtros deixam claro o que esta contratado. | Configurar rotinas dos tres agentes; operar demais areas manualmente; trocar/expandir plano. | Obrigar configuracao dos 96 fluxos ou publicar fluxo de agente nao contratado. |

## Estados Canonicos

| Estado | Significado | Quem e fonte da verdade | UI principal |
|---|---|---|---|
| `nao_contratado` | Agente/fluxo fora do plano atual. | Billing Taliya | Card bloqueado com caminho manual e upgrade/troca. |
| `manual_disponivel` | CRM opera sem agente/autonomia. | CRM | CTA de operacao manual. |
| `rascunho` | Configuracao editada, sem simulacao valida. | Agentes/Fluxos | Pode ajustar e simular; nao publica autonomia. |
| `pronto_para_simular` | Preflight minimo passou. | Agentes/Fluxos | CTA `Simular`. |
| `simulado` | Simulacao valida existe. | Agentes/Fluxos | Pode revisar para publicar. |
| `simulacao_desatualizada` | Ajuste mudou depois da simulacao. | Agentes/Fluxos | Publicacao bloqueada ate simular de novo. |
| `pronto_para_publicar` | Gates passaram. | Agentes/Fluxos + fontes externas | CTA `Publicar rotina`. |
| `publicado` | Snapshot versionado existe. | Agentes/Fluxos/Auditoria | Rotina pode ficar ativa se gates operacionais continuarem OK. |
| `ativo` | Pode executar conforme modo publicado. | Runtime + Agentes/Fluxos | Mostra pausar, simular, ver execucoes. |
| `pendente_aprovacao` | Precisa decisao humana para publicar ou executar. | Aprovacoes | CTA para Aprovacoes; agente explica. |
| `bloqueado_plano` | Entitlement nao permite. | Billing Taliya | Manual continua; upgrade/troca de agente. |
| `bloqueado_cota` | Cota insuficiente/100%. | Uso/Cotas | Manual continua; economia/pacote. |
| `bloqueado_integracao` | Provedor/canal necessario falhou. | Integracoes | CTA para integracao/logs; manual continua. |
| `bloqueado_permissao` | Usuario ou papel sem permissao. | Permissoes | CTA para pedir acesso ou trocar responsavel. |
| `bloqueado_dado` | Falta dado do CRM. | CRM de origem | CTA para corrigir aluno/aula/plano/template. |
| `pausado_usuario` | Usuario pausou. | Agentes/Fluxos/Auditoria | CTA retomar se permitido. |
| `pausado_incidente` | Incidente pausou fluxo/rotina/agente. | Control Plane | CTA ver incidente; retomar so apos resolucao. |
| `degradado` | Autonomia caiu para copiloto/manual. | Runtime/Agentes/Fluxos | Explica motivo e modo atual. |
| `arquivado` | Nao usado, historico consultavel. | Agentes/Fluxos/Auditoria | Sem execucao; leitura apenas. |

## Paginas E Variacoes

### 1. Catalogo De Agentes - `/app/agentes`

Imagem aprovada:

```text
52_round-4.1L_agentes_01_catalogo-agentes-aprovado.png
```

Variacoes:

| Cenario | O que muda | CTA |
|---|---|---|
| Plano 0 agentes | Cards mostram agentes disponiveis como preview/upgrade; sem Agente de Configuracao. | `Ver preview` ou `Ver planos` |
| Plano 1 agente | Agente contratado abre; demais aparecem bloqueados por plano. | `Abrir agente` / `Ver planos` |
| Plano 3 agentes | Bundle ativo abre; demais aparecem como upgrade/troca. | `Abrir agente` |
| Plano 7 agentes | Todos os 7 cards ativos. | `Ver agente` |
| Agente pausado | Card mostra `Pausado`; usuario pode abrir para entender motivo. | `Ver agente` |
| Downgrade | Agentes removidos aparecem bloqueados/pausados por plano, historico preservado. | `Ver motivo` |

Nao mostrar nesta pagina:

- painel direito;
- cota detalhada;
- atividade recente;
- configuracao;
- fluxo solto.

### 2. Pagina Do Agente - `/app/agentes/[agentId]`

Imagem aprovada:

```text
53_round-4.1L_agentes_02_agente-agenda-rotinas-aprovado.png
```

Variacoes:

| Cenario | O que muda | CTA |
|---|---|---|
| Agente contratado | Rotinas abrem normalmente. | `Abrir rotina` |
| Agente nao contratado | Rotinas em preview; nao publica. | `Ver planos` |
| Agente pausado | Status do agente `Pausado`; rotinas indicam pausa quando aplicavel. | `Abrir rotina` |
| Agente bloqueado | Chip de motivo no agente e nas rotinas afetadas. | `Ver bloqueio` |
| Rotina publicada | Card mostra `Publicada`. | `Abrir rotina` |
| Rotina em rascunho | Card mostra `Rascunho`. | `Abrir rotina` |
| Rotina simulada | Card mostra `Rascunho simulado`. | `Abrir rotina` |
| Rotina com excecao | Card mostra `Excecao aberta`. | `Abrir rotina` |
| Rotina com cota/canal/dado pendente | Card mostra motivo resumido; correcao fica na rotina/origem. | `Abrir rotina` |

Sem Agente de Configuracao nesta pagina, porque ainda nao esta configurando nada.

### 3. Pagina Da Rotina - `/app/agentes/[agentId]/rotinas/[routineId]`

Imagem aprovada:

```text
54_round-4.1L_agentes_03_rotina-presenca-faltas-aprovado.png
```

Variacoes:

| Cenario | O que muda | CTA principal |
|---|---|---|
| Rascunho nunca simulado | Perfil selecionavel; cards mostram modos sugeridos; publicacao ainda bloqueada. | `Simular rotina` |
| Simulada e pronta | Mostra `Rascunho simulado` ou `Pronta para publicar`. | `Revisar para publicar` |
| Simulacao desatualizada | Chip `Simulacao desatualizada`; publicar bloqueado. | `Simular novamente` |
| Publicada | Mostra versao publicada, data e opcoes de controle. | `Ver execucoes` / `Pausar rotina` |
| Alteracao nao publicada | Mostra `Rascunho com alteracoes`; compara publicado vs rascunho. | `Simular novamente` |
| Um fluxo personalizado | Perfil mostra `Mais autonomo personalizado`; card indica fluxo diferente do perfil. | `Revisar fluxo` |
| Bloqueada por preflight | Lista bloqueios reais no topo. | `Corrigir bloqueios` |
| Pausada por usuario | Cards ficam read-only; mostra motivo e ator. | `Retomar rotina` |
| Pausada por incidente | Mostra incidente vinculado; retomar bloqueado ate resolver. | `Ver incidente` |
| Plano nao cobre agente | Rotina em preview/manual. | `Ver planos` |

Agente de Configuracao aparece nesta pagina porque o usuario esta escolhendo perfil e entendendo a rotina.

### 4. Pagina Ver E Ajustar Fluxo

Imagem aprovada:

```text
56_round-4.1L_agentes_04_fluxo-falta-com-aviso-v2-aprovado.png
```

Variacoes:

| Cenario | O que muda | CTA |
|---|---|---|
| Fluxo herdado da rotina | Texto informa que herdou perfil. | `Simular este fluxo` |
| Fluxo personalizado | Texto informa que nao segue mais automaticamente o perfil. | `Salvar ajuste` |
| Modo acima do teto | Modo aparece bloqueado, com motivo claro. | nenhum |
| Preflight OK | Chip `7 requisitos OK`. | `Simular este fluxo` |
| Preflight com pendencias | Chip `2 pendencias`; lista read-only ao clicar. | `Corrigir pendencias` |
| Integracao faltando | Mostra dependencia fixa, nao ajuste solto. | `Abrir integracao` |
| Cota insuficiente | Mostra bloqueio e caminho manual. | `Ver cotas` |
| Permissao faltando | Mostra quem pode publicar/alterar. | `Pedir acesso` |
| Fluxo pausado | Ajustes podem ficar read-only conforme permissao. | `Retomar fluxo` |
| Incidente aberto | Banner de incidente vinculado. | `Ver incidente` |

Regra: a pagina de fluxo ajusta somente o necessario para aquele fluxo. Canal, integracao, permissao e cota sao dependencias, nao configuracoes livres.

### 5. Simular Fluxo

Imagem aprovada como estrutura:

```text
58_round-4.1L_agentes_05_teste-fluxo-falta-com-aviso-aprovado.png
```

Decisao de nomenclatura:

```text
Nome oficial: Simular fluxo.
Rota: /app/agentes/[agentId]/rotinas/[routineId]/fluxos/[flowId]/simular
```

Variações:

| Cenario | O que muda |
|---|---|
| Fluxo com mensagem | Visual central usa celular/conversa. |
| Fluxo interno | Visual central usa objeto do CRM, nao celular fake. |
| Simulacao aprovada | Linha de execucao conclui e mostra continuidade. |
| Simulacao com excecao | Mostra onde chama equipe/aprovacao. |
| Simulacao bloqueada | Mostra gate que falhou e CTA para corrigir. |
| Simulacao desatualizada | Banner indica que ajuste mudou e precisa rodar novamente. |
| Plano 0 agentes | Simula preview/manual; nao permite publicar autonomia. |

Nao existe pagina separada `Testar fluxo`.

### 6. Publicar Rotina

Imagem aprovada:

```text
59_round-4.1L_agentes_06_publicar-rotina-presenca-faltas-aprovado.png
```

Variações:

| Cenario | O que muda | CTA principal |
|---|---|---|
| Pronta para publicar | Preflight verde, cards dos fluxos resumem configuracao. | `Publicar rotina` |
| Bloqueada por simulacao desatualizada | Topo mostra bloqueio e fluxo afetado. | `Simular novamente` |
| Bloqueada por integracao | Mostra integracao/canal afetado. | `Abrir integracao` |
| Bloqueada por cota | Mostra cota insuficiente. | `Ver cotas` |
| Bloqueada por permissao | Mostra quem pode publicar. | `Pedir acesso` |
| Bloqueada por plano | Mostra agente/rotina fora do plano. | `Ver planos` |
| Publicacao bloqueada | Qualquer fluxo nao pronto para o modo configurado impede a rotina de publicar. | `Corrigir bloqueios` |
| Aprovacao exigida para publicar | CTA cria aprovacao, nao publica direto. | `Enviar para aprovacao` |

Regra: publicacao principal e por rotina. `Publicar fluxo` e excecao contextual, nao CTA principal.

### 7. Rotina Publicada

Ainda sem imagem aprovada.

Deve mostrar:

- versao publicada;
- data/usuario;
- fluxos ativos;
- fluxos manuais ou bloqueados;
- ultima simulacao valida;
- atalhos para execucoes, pausar, simular novamente e ajustar rascunho.

CTA principal recomendado:

```text
Ver execucoes
```

CTAs secundarios:

```text
Pausar rotina
Simular novamente
Ajustar rascunho
```

### 8. Pausar, Retomar E Rollback

Ainda sem imagem aprovada.

Superficies esperadas:

| Acao | Onde acontece | Deve mostrar |
|---|---|---|
| Pausar fluxo | Pagina do fluxo, rotina ou incidente | motivo, impacto, continuidade manual, auditoria. |
| Pausar rotina | Pagina da rotina/publicada | fluxos afetados, mensagens futuras, execucoes em andamento. |
| Pausa emergencial | Incidente/Hoje | severidade, quem pausou, como investigar. |
| Retomar | Fluxo/rotina pausada | preflight novo, simulacao se necessario, ator autorizado. |
| Rollback | Rotina publicada ou politica | versao atual, versao anterior, o que nao pode desfazer, auditoria. |

Rollback nunca promete desfazer mensagem enviada, pagamento confirmado, dado compartilhado ou comunicacao externa ja realizada.

### 9. Execucao E Incidente

Ainda sem imagem aprovada para Agentes/Fluxos.

Rotas:

```text
/app/fluxos/execucoes/[runId]
/app/operacao/incidentes
/app/operacao/incidentes/[incidentId]
```

Deve mostrar:

- qual fluxo/rotina/versao rodou;
- modo publicado;
- entrada;
- checagens;
- ferramenta/canal usado;
- acao;
- custo/cota;
- auditoria;
- fallback;
- erro, se houver;
- reprocessamento seguro, se permitido.

Control Plane investiga o que aconteceu. Nao configura regra permanente.

## Matriz De Bloqueios

| Bloqueio | Aparece onde | Texto simples | CTA |
|---|---|---|---|
| Plano nao inclui agente | Catalogo, agente, rotina, publicar | `Este agente nao esta no plano atual.` | `Ver planos` |
| Cota 70% | Rotina, fluxo, uso | `Uso alto; automacao continua com alerta.` | `Ver cotas` |
| Cota 90% | Rotina, publicar, Hoje | `Economia ativa; baixa prioridade vira tarefa.` | `Ajustar economia` |
| Cota 100% | Rotina, fluxo, publicar | `Automacao paga bloqueada; manual continua.` | `Ver cotas` |
| WhatsApp desconectado | Fluxo, rotina, publicar | `WhatsApp precisa estar conectado.` | `Abrir integracao` |
| Template nao aprovado | Fluxo, rotina, publicar | `Template precisa de aprovacao.` | `Revisar template` |
| Responsavel ausente | Rotina, fluxo, publicar | `Defina quem recebe excecoes.` | `Definir responsavel` |
| Permissao insuficiente | Fluxo, publicar | `Voce nao pode publicar esta rotina.` | `Pedir acesso` |
| Simulacao desatualizada | Rotina, publicar | `Ajustes mudaram depois da ultima simulacao.` | `Simular novamente` |
| Incidente aberto | Hoje, rotina, fluxo | `Automacao pausada por incidente.` | `Ver incidente` |
| Dado ausente | Fluxo, publicar | `Falta dado no CRM para rodar.` | `Corrigir dado` |

## Proximas Variacoes A Fechar Em Documento

Nao gerar imagens novas para estas variacoes.

Usar os layouts aprovados e documentar:

1. textos exatos de chip/banner;
2. CTAs por estado;
3. bloqueios por fonte da verdade;
4. o que continua manual;
5. o que o Agente de Configuracao explica;
6. quando a rotina inteira bloqueia e quando so um fluxo fica pendente;
7. como cada variacao aparece no plano 0, 1, 3 e 7 agentes.
