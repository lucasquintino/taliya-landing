# Auditoria ponta a ponta do produto - PT-BR

> Status: rodada de revisao completa, partindo dos fluxos iniciais e passando por agentes, casos de uso, modos de execucao, cotas, paginas, mobile e direcao visual.

## Veredito curto

Estamos no caminho.

Mas a documentacao nao estava 100% coerente antes desta rodada: a cobertura dos casos citava "Qualidade de dados" como pagina dona de 2 casos, enquanto o mapa oficial de paginas ainda nao tinha essa superficie.

Correcao feita nesta rodada:

- "Qualidade de dados" entrou como superficie funcional sem menu proprio.
- O mapa oficial passou de 37 para 38 paginas/superficies.
- O menu principal continua com 12 entradas.
- A cobertura dos 157 casos continua fechada.

## Numeros consolidados depois da revisao

| Tema | Numero atual | Leitura correta |
| --- | ---: | --- |
| Fluxos base de agentes | 91 | Baseline minimo defensavel. |
| Fluxos fortes adicionados | 5 | Devem entrar no catalogo candidato. |
| Fluxos fortes atuais | 96 | Numero canonico de trabalho. |
| Fluxos opcionais | 2 | E14 e G13 ainda precisam decisao. |
| Casos de uso do gestor | 157 | Universo candidato atual. |
| Linhas na matriz de execucao | 157 | Todos os casos tem caminho de execucao mapeado. |
| Linhas de cobertura pagina/caso | 157 | Todos os casos tem pagina dona. |
| Menus principais web | 12 | Nao precisa aumentar agora. |
| Paginas/superficies funcionais | 38 | Inclui qualidade de dados sem menu proprio. |
| Zonas de layout mapeadas | 38 | Toda pagina tem topo, esquerda, centro, direita e mobile definidos. |

## Cadeia revisada desde o comeco

### 1. Oferta e landing

A landing e os documentos de entrada continuam coerentes com a promessa: reduzir perda operacional em studios de Pilates usando CRM, agenda, WhatsApp, acompanhamento e agentes.

Risco: a landing antiga puxa a percepcao para "agente comercial/WhatsApp". Para o produto principal, precisamos manter a mensagem:

```text
Taliya e um CRM operacional completo com agentes integrados.
WhatsApp e canal, nao o produto inteiro.
```

### 2. Agente comercial flutuante

O material do agente comercial continua util, mas ele deve ser tratado como:

- canal de captacao;
- demonstracao de valor;
- frente comercial;
- entrada para o CRM.

Ele nao pode ser confundido com o produto inteiro.

### 3. Proposta central do CRM

A proposta esta correta:

```text
CRM operacional para studios de Pilates, com agentes de IA integrados ao sistema.
```

Ponto essencial que deve permanecer:

- plano Base funciona com 0 agentes ativos;
- agentes operam sobre registros, casos, tarefas, permissoes, cotas e auditoria;
- o gestor pode agir manualmente, pedir ajuda ou permitir automacao.

### 4. Fluxos de agentes

O caminho atual esta bom:

- 91 fluxos eram o baseline;
- 5 fluxos fortes foram adicionados;
- 96 e o numero canonico atual;
- E14 e G13 ficam sob decisao, podendo levar o catalogo para 97 ou 98.

Nao recomendo reduzir abaixo de 96 agora.

Tambem nao recomendo transformar todo subpasso em agente proprio. O criterio certo e: se tem gatilho, dono, configuracao, limite, cota, estados finais e avaliacao, pode ser fluxo. Se for so uma etapa, dado ou tela, deve ficar absorvido.

### 5. Casos de uso do gestor

Os 157 casos fazem sentido como universo candidato.

Importante: 157 casos nao significam 157 telas. Eles significam que o gestor precisa conseguir executar, revisar, aprovar, corrigir, delegar ou acompanhar 157 caminhos operacionais.

O modelo atual esta certo porque separa:

- caso manual;
- caso com copiloto;
- caso autonomo;
- caso que nao precisa de IA;
- caso que precisa de trava humana.

### 6. Execucao manual, copiloto e autonoma

O desenho esta no caminho correto:

| Modo | Papel no produto |
| --- | --- |
| Manual | Garante que o CRM existe mesmo sem agentes. |
| Copiloto | Prepara resposta, plano, analise ou acao para aprovacao. |
| Autonomo | Executa somente dentro de regra, cota, permissao, janela e risco permitido. |

Essa arquitetura evita o erro de vender "IA magica" e depois descobrir que o gestor ainda precisa de controle.

### 7. Cotas e economia

A parte de cotas esta conceitualmente correta.

Ela nao deve aparecer so em billing. Ela precisa aparecer dentro da operacao:

- no cartao do caso;
- no painel lateral;
- na aprovacao;
- no historico da execucao;
- quando uma automacao pausa;
- quando um fluxo muda de autonomo para tarefa.

Regra que deve ficar inegociavel:

```text
Se a cota acaba, o CRM continua. O que para e a automacao paga.
```

### 8. Paginas e rotas

Depois desta rodada, o mapa ficou coerente:

- 12 menus principais;
- 38 paginas/superficies;
- 157 casos cobertos;
- nenhuma pagina citada pela cobertura ficou fora do mapa;
- nenhuma pagina oficial ficou sem zona de layout.

A correcao importante foi adicionar:

```text
Qualidade de dados
```

Essa superficie e necessaria porque dados ruins bloqueiam atendimento, agenda, financeiro, agentes, historico e auditoria.

### 9. Direcao visual

A direcao visual agora esta certa:

```text
CRM por jornadas, cartoes, etapas, responsaveis e painel de contexto.
```

Nao devemos desenhar o Taliya como uma colecao de tabelas. Tabelas entram onde fazem sentido, principalmente financeiro, auditoria, exportacoes e relatorios.

As paginas principais precisam parecer mesa de operacao:

- topo com filtros;
- centro com jornada, calendario, pipeline, lista priorizada ou chamada;
- painel direito com contexto e acao;
- cartoes com pessoa, risco, etapa, dono, prazo e proxima acao.

### 10. App mobile

O app mobile esta no caminho se continuar focado no dia a dia:

- Hoje;
- Inbox;
- Agenda;
- Chamada;
- Aluno;
- Professor;
- Tarefas;
- Aprovacoes;
- alertas financeiros essenciais;
- reclamacoes/casos;
- agentes/alertas;
- uso/cotas.

Nao recomendo levar configuracao pesada para o app no primeiro desenho.

### 11. Dados, permissoes e seguranca

Este e o maior bloco que ainda precisa detalhe antes de implementacao.

As ideias estao certas, mas ainda precisam ficar exatas:

- permissao por papel;
- visibilidade do historico sensivel;
- quem pode aprovar financeiro;
- quem pode ver dados de saude/anamnese;
- quem pode dar acesso ao suporte Taliya;
- quando o agente deve parar e pedir humano;
- quais acoes exigem auditoria obrigatoria.

## O que eu adicionaria

Ja adicionado nesta rodada:

- Qualidade de dados como superficie funcional.

Ainda precisa detalhar, mas nao necessariamente virar pagina nova:

- matriz de permissao por papel;
- texto dos principais botoes de acao;
- estados de cada cartao de jornada;
- regras exatas de autonomia por fluxo;
- criterio final de E14 e G13;
- profundidade final do mobile por tela.

## O que eu ajustaria

1. Tratar os documentos antigos do agente comercial como camada de entrada, nao como definicao do produto inteiro.
2. Atualizar qualquer conversa de "37 paginas" para "38 superficies".
3. Usar "Jornadas e operacao" como centro visual da operacao.
4. Manter "Qualidade de dados" sem menu proprio, acessada por alertas, configuracoes, onboarding, importacao, contatos e operacao.
5. Reforcar que toda automacao importante tem equivalente manual.

## O que eu removeria ou evitaria

Nao removeria nenhum bloco grande agora.

Eu evitaria:

- criar mais menus principais;
- criar pagina para cada fluxo;
- vender o produto como WhatsApp bot;
- deixar cotas escondidas em billing;
- permitir autonomia financeira/sensivel sem aprovacao;
- levar configuracao pesada para mobile;
- deixar "Agentes" parecerem produto separado.

## Pendencias reais

Estas pendencias nao invalidam o caminho. Elas sao as proximas decisoes de produto:

| Pendencia | Por que importa |
| --- | --- |
| E14 vira fluxo proprio? | Define se primeira semana do aluno e agente standalone ou parte de retencao/onboarding. |
| G13 vira fluxo proprio? | Define se anamnese/consentimento e agente standalone ou trava de dados/historico. |
| Permissoes por papel | Bloqueia implementacao segura. |
| Autonomia por fluxo | Bloqueia automacao real. |
| Profundidade mobile | Evita app grande demais. |
| Botoes e microcopy | Necessario para desenhar UI real. |
| Estados dos cartoes | Necessario para UI por jornadas. |

## Conclusao

O caminho esta correto.

A proposta que emerge dos documentos e forte:

```text
Taliya e a mesa de operacao de um studio de Pilates.
O CRM organiza tudo.
Os agentes atuam dentro do CRM, WhatsApp e app quando permitido.
O gestor sempre consegue ver, corrigir, aprovar ou assumir.
```

O principal cuidado daqui para frente e nao deixar a ambicao virar bagunca de tela.

Produto certo:

```text
12 menus, 38 superficies, 157 casos, 96 fluxos fortes, IA contextual e controle humano claro.
```

Produto errado:

```text
um bot de WhatsApp com varias telas em volta.
```
