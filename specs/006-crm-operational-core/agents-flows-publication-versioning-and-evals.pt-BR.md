# Taliya CRM - Publicacao, Versionamento E Evals De Agentes/Fluxos

Status: contrato funcional v0.1.
Data: 2026-05-21.

## Objetivo

Definir como um fluxo sai de rascunho, passa por simulacao, vira configuracao publicada, pode ser pausado, pode voltar para versao anterior e pode manter ou perder autonomia.

Este documento complementa:

- `agents-flows-routines-pages-final-contract.pt-BR.md`;
- `agents-flows-routine-profile-map.pt-BR.md`;
- `agents-flows-functional-architecture.pt-BR.md`.

Ele nao cria Control Plane novo, nao mexe em Billing Taliya e nao transforma integracao tecnica em regra de agente.

Nota de vocabulario:

```text
Na UI final, o usuario publica rotina, nao pacote.
Perfil da rotina substitui o termo antigo preset.
Quando docs antigos falarem pacote, leia rotina.
```

## Principio Central

Autonomia no Taliya nunca e "ligar IA".

Autonomia e uma configuracao publicada, versionada, simulada, limitada, auditada e reversivel no que ainda nao saiu para o mundo.

```text
rascunho -> simulacao -> aprovacao -> publicacao -> execucao monitorada
```

## Estados De Configuracao

| Estado | O que significa | Pode executar? |
|---|---|---|
| rascunho | Configuracao editavel, ainda sem simulacao valida. | Nao. |
| pendente_dados | Falta dado, canal, template, permissao ou integracao. | Nao. |
| pronto_para_simular | Tem minimo para testar. | Nao. |
| simulado | Simulacao recente existe. | Ainda nao, salvo modo manual sem automacao. |
| aguardando_aprovacao | Precisa decisao humana antes de publicar. | Nao. |
| publicado | Snapshot valido foi aprovado. | Ainda depende de status operacional. |
| ativo | Pode executar conforme modo e limites. | Sim. |
| degradado | Continua em manual/copiloto porque autonomia foi bloqueada. | Parcial. |
| pausado | Parado por usuario, incidente, cota, risco ou integracao. | Nao. |
| bloqueado | Nao pode rodar ate requisito critico ser corrigido. | Nao. |
| arquivado | Nao e mais usado, mas historico fica consultavel. | Nao. |

## O Que E Versionado

Cada publicacao cria um snapshot imutavel.

| Item | Versionar | Por que |
|---|---|---|
| Perfil da rotina aplicado | sim | Para saber qual postura sugeriu limites e modos. |
| Rotina publicada | sim | Para comparar publicacao por rotina e por fluxo. |
| Fluxo | sim | Para saber gatilho, condicao, acao, modo e fallback vigentes. |
| Template/regra usada | sim | Para provar qual mensagem ou politica estava aprovada. |
| Limites | sim | Para saber tentativas, janelas, custo e frequencia. |
| Simulacao | sim | Para provar que o fluxo foi testado antes da publicacao. |
| Aprovacao | sim | Para saber quem aprovou e quando. |
| Entitlement | referencia | Billing e fonte da verdade, mas a publicacao registra o entitlement verificado. |
| Cota | referencia | Uso/Cotas e fonte da verdade, mas a publicacao registra estimativa. |
| Integracao | referencia | Integracoes e fonte da verdade, mas a publicacao registra status checado. |

Regra:

- editar rascunho nao muda versao publicada;
- publicar cria nova versao;
- rollback aponta para uma versao anterior e cria novo evento;
- auditoria antiga nunca e editada.

## Gates De Publicacao

Um fluxo so pode ser publicado quando todos os gates obrigatorios passam.

| Gate | Pergunta simples | Dono da verdade |
|---|---|---|
| Entitlement | O plano inclui esse agente/fluxo? | Billing Taliya. |
| Permissao | Este usuario pode publicar? | Permissoes do CRM. |
| Dados | Os dados minimos existem? | CRM. |
| Canal | O canal necessario esta disponivel? | CRM/Integracoes. |
| Integracao | O provedor tecnico esta saudavel? | Integracoes Tecnicas. |
| Template/regra | A mensagem ou regra foi aprovada? | Fluxo/contexto do CRM. |
| Cota | Existe cota para executar? | Uso/Cotas. |
| Risco | O risco permite o modo escolhido? | Agentes/Fluxos. |
| Fallback | Existe caminho manual seguro? | Agentes/Fluxos/CRM. |
| Simulacao | A simulacao e recente e valida? | Agentes/Fluxos. |
| Auditoria | Eventos obrigatorios estao definidos? | Auditoria. |

Se qualquer gate critico falhar, o fluxo nao publica autonomia. Ele pode ficar manual, copiloto, pendente ou bloqueado.

## Publicacao Por Rotina

Publicar rotina nao significa publicar tudo.

A rotina deve separar:

- fluxos que entram ativos;
- fluxos que entram em copiloto;
- fluxos que ficam manuais;
- fluxos bloqueados por plano;
- fluxos bloqueados por dado/canal/integracao;
- fluxos bloqueados por risco;
- fluxos fora do agente contratado.

O usuario confirma a rotina sabendo:

- o que muda agora;
- o que continua manual;
- o que pode consumir cota;
- o que exige aprovacao;
- o que ficou pendente;
- como pausar tudo se algo der errado.

## Simulacao Obrigatoria

A simulacao deve usar casos simples e casos de borda.

Todo fluxo autonomo precisa simular pelo menos:

- caso que executa;
- caso que vira tarefa;
- caso que pede aprovacao;
- caso que bloqueia por dado;
- caso que bloqueia por canal/integracao;
- caso que bloqueia por opt-out ou permissao;
- caso que estoura limite/cota;
- caso que cai no fallback.

Estados finais da simulacao:

| Estado | Decisao |
|---|---|
| aprovada | Pode publicar se aprovador confirmar. |
| aprovada_com_avisos | Pode publicar, mas mostra pendencias nao bloqueantes. |
| bloqueada | Nao publica ate corrigir. |
| exige_aprovacao | Publica ou executa somente com aprovador. |
| degrada_para_copiloto | Autonomia nao e segura, mas sugestao humana e permitida. |
| degrada_para_manual | Nem copiloto resolve com seguranca suficiente. |

## Evals Para Autonomia

Evals sao casos de teste de comportamento. Eles nao substituem auditoria, mas ajudam a decidir se autonomia continua permitida.

| Familia | Evals minimos |
|---|---|
| FAQ/resposta permitida | Responde so com base aprovada; recusa tema fora de escopo; nao inventa politica; detecta baixa confianca. |
| Opt-out/consentimento | Detecta pedido de parar contato; nao envia apos opt-out; registra preferencia; pede revisao quando ambiguo. |
| Handoff | Escala quando ha risco, reclamacao, baixa confianca, identidade incerta ou pedido humano. |
| Lembrete de presenca | Envia dentro da janela; respeita canal e opt-out; nao insiste; cria tarefa se falhar. |
| Experimental/vendas | Nao promete vaga/preco fora da regra; nao converte matricula sozinho; cria tarefa comercial quando necessario. |
| Financeiro simples | Nao negocia desconto, estorno ou acordo; usa template aprovado; cria aprovacao em atraso sensivel. |
| Professor/historico | Resume apenas dado permitido; nao compartilha historico sensivel; cria tarefa quando falta permissao. |
| Cota/economia | Alerta em 70%; degrada em 90%; bloqueia automacao paga em 100%; preserva manual. |
| Integracao/falha | Nao reconecta provedor sozinho; nao reprocessa sem idempotencia; abre incidente/tarefa. |

Criterio simples:

- erro baixo e previsivel: pode manter autonomia estreita;
- erro recorrente ou ambiguidade: degrada para copiloto;
- risco sensivel: manual/copiloto com aprovacao;
- erro com impacto real: pausa e abre incidente.

## Severidade E Auto-Pausa

| Severidade | Exemplo | Acao |
|---|---|---|
| informativa | Bloqueio esperado por falta de dado. | Mostra pendencia. |
| baixa | Uma execucao virou tarefa por fallback. | Mantem fluxo. |
| media | Falhas repetidas, custo acima do previsto ou handoff excessivo. | Degrada ou pede revisao. |
| alta | Mensagem errada enviada, risco sensivel, conflito de agenda com impacto ou falha financeira. | Pausa fluxo e abre incidente. |
| critica | Vazamento de dado, envio apos opt-out, acao financeira sensivel indevida ou risco legal. | Pausa agente/rotina, alerta Hoje e exige revisao autorizada. |

Auto-pausa deve acontecer quando:

- opt-out foi desrespeitado;
- cota chegou a 100%;
- integracao critica ficou indisponivel;
- template foi rejeitado/pausado;
- erro de seguranca ou privacidade apareceu;
- o fluxo excedeu limite de falhas configurado;
- uma execucao gerou incidente alto ou critico.

## Rollback

Rollback volta para uma configuracao anterior.

Pode reverter:

- modo;
- limite;
- template/regra futura;
- fallback;
- rotina publicada;
- gatilho e condicao futuros.

Nao pode desfazer sozinho:

- mensagem ja enviada;
- comprovante ja processado;
- pagamento confirmado;
- alteracao de agenda ja comunicada;
- compartilhamento de dado ja ocorrido.

Quando algo ja teve impacto externo, rollback deve abrir tarefa ou incidente de correcao.

## Eventos De Auditoria

Auditar sempre:

- rascunho criado;
- preflight executado;
- simulacao executada;
- simulacao aprovada/bloqueada;
- aprovacao solicitada;
- aprovacao concedida/rejeitada;
- rotina publicada;
- fluxo publicado;
- modo alterado;
- limite alterado;
- fallback alterado;
- fluxo pausado/retomado;
- rollback executado;
- autonomia degradada;
- execucao bloqueada por cota, plano, permissao, opt-out, integracao ou risco;
- incidente aberto a partir de execucao.

Cada evento deve guardar:

- tenant;
- usuario/ator;
- agente;
- fluxo;
- versao;
- objeto afetado;
- motivo;
- antes/depois seguro, quando aplicavel;
- cota estimada ou real;
- link para execucao, aprovacao ou incidente.

## Relacao Com Outras Familias

| Familia | Como conversa com Agentes/Fluxos |
|---|---|
| Setup Inicial | Pode preparar rascunho de rotina recomendado, mas nao publica autonomia. |
| Configuracoes | Fornece CRM base, equipe, canais comuns, notificacoes e regras contextuais. |
| Integracoes | Diz se provedor esta conectado e mostra logs tecnicos; nao define regra de agente. |
| Billing Taliya | Define plano, agentes inclusos e cotas comerciais. |
| Uso/Cotas | Mede consumo real, aplica 70/90/100 e mostra extrato. |
| Auditoria | Guarda trilha imutavel de publicacao, execucao e correcao. |
| Control Planes | Investigam execucao/incidente e podem pausar emergencialmente, mas nao publicam configuracao permanente. |

## Criterios De Aceite

Este contrato esta correto quando:

- publicacao autonoma exige entitlement, permissao, dados, canal, integracao, template/regra, cota, risco, fallback, simulacao e auditoria;
- rotina pode publicar somente o que passou nos gates;
- rollback nao promete desfazer impacto externo;
- auto-pausa existe para risco alto/critico;
- evals cobrem as familias que podem ter autonomia no MVP;
- Control Planes continuam distribuidos e sem `/app/controle/*`;
- Billing, Integracoes e Uso/Cotas continuam fontes de verdade das suas areas.
