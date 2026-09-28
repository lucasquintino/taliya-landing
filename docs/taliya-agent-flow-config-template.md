# Taliya Agent Flow Config Template

## Uso

Este template deve ser usado para cada fluxo da matriz de configuracao. Ele define o minimo que o produto precisa saber antes de permitir que um studio ative ou ajuste um fluxo.

## Template

```text
Agente:
Fluxo:
Codigo:

Objetivo:
Canal onde nasce:
Canal onde roda:
Canal onde registra:
Canal onde aprova/acompanha:

Autonomia padrao:
Autonomias permitidas:

Trigger:
Dados obrigatorios:
Se faltar dado:

Subfluxos principais:
Subfluxos criticos:
Estados finais:
Transicoes permitidas:

Configuracoes do studio:
  - ativo/inativo:
  - modo_operacao:
  - alcance_autonomo:
  - depois_do_limite:
  - tom:
  - templates:
  - limite de tentativas:
  - limite de creditos:
  - janela de envio:
  - responsavel:
  - aprovacao obrigatoria:
  - custo_estimado:
  - origem_do_custo:
  - criterios de handoff:
  - criterios de pausa:
  - proximos fluxos permitidos:

Economia de creditos:
Handoff obrigatorio quando:
Auditoria obrigatoria:

Testes minimos:
  - sucesso:
  - falta de dado:
  - excecao:
  - custo/limite:
  - transicao:
```

## Valores Permitidos

### Canais

- `whatsapp`
- `sistema`
- `hibrido`

### Modos De Operacao Do Fluxo

- `manual`: Taliya organiza, registra e cria tarefas. A equipe executa.
- `copiloto`: Taliya prepara a acao/mensagem e pede aprovacao antes de executar.
- `autonomo`: Taliya executa sozinha dentro das regras do fluxo. Ao selecionar este modo, abre a configuracao de limitacao.

### Alcance Do Autonomo

Todo fluxo em modo autonomo deve explicar ate onde o agente vai antes de parar, pedir aprovacao ou chamar humano:

- quantidade maxima de tentativas;
- custo/creditos maximos do fluxo;
- se pode responder apenas conversa aberta ou iniciar conversa paga;
- se pode seguir ate a resposta do contato, ate a primeira excecao ou ate fechar o fluxo;
- quais palavras, pedidos, riscos ou duvidas interrompem a automacao;
- para onde vai depois: parar, criar tarefa, pedir aprovacao, chamar responsavel ou mover para outro fluxo.

### Origem Do Custo Por Fluxo

Cada fluxo deve mostrar ao studio de onde o custo pode vir:

- IA para interpretar, resumir, classificar ou escrever mensagens;
- WhatsApp Service quando aplicavel a conversa aberta pelo contato;
- WhatsApp Utility para aviso operacional, agenda, pagamento ou confirmacao;
- WhatsApp Marketing para campanha, reativacao, promocao ou comunicacao comercial;
- jobs/rotinas em lote;
- armazenamento/processamento de midias ou historico.

Quanto mais autonomo for o modo escolhido, maior tende a ser o consumo, porque o fluxo pode chamar IA, iniciar mensagens pagas e executar mais etapas sem esperar a equipe.

### Estados Finais

- `resolvido`
- `aguardando_contato`
- `aguardando_equipe`
- `acao_registrada`
- `tarefa_criada`
- `handoff_humano`
- `proximo_fluxo`
- `sem_acao`
- `pausado`

## Configuracoes Padrao Por Risco

| Risco | Autonomia maxima permitida |
| --- | --- |
| Saude, dor, lesao, gravidez ou orientacao clinica | `manual` |
| Desconto, reembolso, cortesia ou bloqueio | `manual` |
| Campanha, lote ou reativacao em massa | `copiloto` |
| Dado pessoal em grupo ou responsavel nao validado | `manual` |
| Conflito de agenda/capacidade/professor | `copiloto` |
| Duvida publica simples | `autonomo` com limites do fluxo |
| Classificacao e roteamento | `autonomo` com limites do fluxo |
| Reposicao com regra clara | `autonomo` com limites do fluxo |
| Pagamento com link configurado | `autonomo` com limites do fluxo |

## Gates De Ativacao

Um fluxo nao pode ser ativado se:

- nao houver responsavel para handoff;
- nao houver dados obrigatorios;
- nao houver janela de envio para WhatsApp externo;
- nao houver criterio de opt-out para WhatsApp;
- o fluxo autonomo nao explicar ate onde vai e o que acontece depois;
- o fluxo puder gerar custo sem mostrar a origem do custo ao studio;
- o fluxo puder iniciar WhatsApp pago sem limite proprio de tentativas e creditos;
- campanha, lote ou reativacao estiverem em autonomo sem aprovacao/limite;
- nao houver limite de tentativas para fluxo recorrente;
- nao houver limite de creditos para fluxo caro;
- houver risco sensivel sem manual/handoff humano;
- a simulacao minima falhar.

