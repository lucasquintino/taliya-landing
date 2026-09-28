# Plano 100% - Setup, Configuracoes E Integracao Com CRM/Agentes

Status: plano ajustado.
Data: 2026-05-13.

## Objetivo final

Sair com uma arquitetura de setup/configuracoes que seja:

- precisa;
- sem duplicidade de regra;
- sem conflito de precedencia;
- simples para o studio;
- integrada ao CRM;
- integrada aos agentes;
- segura para 0, 1, 3 e 7 agentes;
- compativel com modo manual, copiloto e autonomo;
- pronta para orientar as telas/imagens de onboarding e configuracoes.

## Resultado esperado

Ao final deste plano, devemos saber:

1. O que precisa ser configurado.
2. Quem e dono de cada regra.
3. Como cada regra e salva pelo sistema.
4. Como cada regra e consumida pelo CRM e pelos agentes.
5. Como o agente de setup guia o studio.
6. Quais perguntas aparecem para o usuario.
7. Quais caminhos o setup pode seguir.
8. O que pode ser publicado parcialmente.
9. O que bloqueia autonomia.
10. Quais telas/imagens precisam existir.

## Plano ajustado

### 1. Congelar principios

Validar os principios que nao podem mudar:

- humano guia;
- agente guia;
- gestor decide;
- sistema configura;
- auditoria registra;
- CRM funciona com 0 agentes;
- autonomia e sempre ultima camada;
- regra sensivel exige validacao.

Entrega:

- principios consolidados nos docs de onboarding/setup.

### 2. Inventario de configuracoes

Levantar todas as configuracoes possiveis:

- studio;
- unidades;
- equipe;
- permissoes;
- agenda;
- aulas;
- turmas;
- reposicoes;
- no-show;
- financeiro;
- cobranca;
- consumo de aulas;
- alunos;
- canais;
- modelos de mensagem;
- agentes;
- fluxos;
- regras de seguranca/aprovacoes;
- cotas;
- integracoes;
- auditoria;
- billing;
- privacidade.

Entrega:

- lista completa de configuracoes candidatas.

### 3. Contrato tecnico das configuracoes

Definir o formato que toda configuracao precisa ter:

- identificador;
- nome de negocio;
- descricao simples;
- tipo;
- dono;
- fonte da verdade;
- default;
- preset;
- obrigatoriedade;
- escopo;
- validade;
- versao;
- dependencias;
- impacto;
- permissao;
- auditoria;
- rollback;
- estado de publicacao.

Entrega:

- contrato padrao para representar configuracoes.

### 4. Corte de complexidade

Classificar cada configuracao como:

- setup obrigatorio;
- setup recomendado;
- default automatico;
- avancada;
- pos-MVP;
- removida.

Entrega:

- lista enxuta do que realmente entra no MVP.

### 5. Fonte da verdade

Definir onde cada regra mora.

Exemplos:

- reposicao mora em Agenda/Reposicoes;
- consumo de aulas mora em Consumo de Aulas;
- cobranca mora em Financeiro;
- autonomia mora em Fluxos;
- cota mora em Uso/Cotas;
- regra sensivel mora em Politicas, mas aparece para o gestor como regra de seguranca/aprovacao/excecao;
- permissao mora em Permissoes.

Entrega:

- matriz regra -> fonte da verdade.

### 6. Precedencia e conflito

Definir ordem de prioridade entre regras:

1. privacidade/legal;
2. permissao;
3. plano Taliya;
4. cota;
5. politica operacional;
6. excecao do aluno;
7. regra do plano do aluno;
8. regra da turma/aula;
9. regra padrao do studio;
10. default seguro do sistema.

Entrega:

- regras de conflito e exemplos.

### 7. Camada de consumo pelo CRM e agentes

Definir como o sistema usa configuracoes publicadas:

- snapshot publicado;
- versao da regra usada em cada execucao;
- leitura centralizada;
- fallback seguro;
- comportamento quando regra muda;
- impacto em fluxos ativos;
- registro em auditoria.

Entrega:

- contrato de consumo das configuracoes pelo CRM e pelos agentes.

### 8. Perguntas do setup

Traduzir configuracoes tecnicas em perguntas simples.

Exemplo:

- Configuracao: `reposicao_exige_credito_disponivel`.
- Pergunta: "Aluno precisa ter aula disponivel para repor?"

Entrega:

- mapa pergunta -> configuracao gerada.

### 9. Arvore adaptativa

Definir desvios:

- se nao usa pacote, pular credito;
- se tem 0 agentes, pular ativacao;
- se WhatsApp nao conectou, bloquear automacao externa;
- se financeiro incompleto, reposicao com impacto financeiro fica manual;
- se regra sensivel nao foi publicada, autonomia fica bloqueada.

Entrega:

- arvore de decisoes do setup.

### 10. Matriz de impacto

Para cada configuracao, mapear impacto em:

- paginas;
- casos de uso;
- fluxos do CRM;
- agentes;
- tarefas;
- checklists;
- aprovacoes;
- cotas;
- auditoria;
- relatorios.

Entrega:

- matriz configuracao -> impacto.

### 11. Publicacao parcial

Definir criterios para publicar:

- CRM manual;
- Agenda;
- Financeiro;
- Canais/modelos de mensagem;
- Regras de seguranca/aprovacoes;
- Agentes preparados;
- rascunhos/pendencias para Agentes/Fluxos pos-go-live.

Entrega:

- regras de publicacao parcial.

### 12. Reconfiguracao pos-setup

Mapear mudancas depois do go-live:

- alterar modelo de cobranca;
- alterar consumo de aulas;
- alterar reposicao;
- alterar permissao;
- alterar template;
- alterar modo de fluxo;
- alterar politica;
- alterar cota/plano.

Entrega:

- regra de diff, simulacao pos-go-live, publicacao, impacto e rollback.

### 13. Testes de conflito

Simular regras brigando:

- reposicao permitida vs aluno inadimplente;
- automacao permitida vs consentimento ausente;
- agente ativo vs cota estourada;
- usuario sem permissao vs acao sensivel;
- modelo de mensagem aprovado vs canal desconectado;
- fluxo autonomo vs politica nao publicada.

Entrega:

- suite de conflitos esperados e resultado correto.

### 14. Cenarios de teste

Simular studios reais:

- studio simples com 0 agentes;
- studio com 1 agente;
- studio com 3 agentes;
- studio com 7 agentes;
- mensalidade fixa;
- pacote de aulas;
- modelo hibrido;
- WhatsApp desconectado;
- financeiro incompleto;
- cota em 90%;
- regra contraditoria.

Entrega:

- cenarios completos com caminho esperado.

### 15. Criterios de aceite

Definir quando cada artefato esta pronto.

Exemplos:

- inventario so fecha se cada configuracao tiver dono e decisao MVP;
- matriz so fecha se cobrir todas as rotas e agentes;
- arvore so fecha se tiver desvios e bloqueios;
- cenarios so fecham se cobrem 0/1/3/7 agentes.

Entrega:

- checklist de aceite por etapa.

### 16. Blueprint das telas

Somente depois da logica validada, definir telas:

- inicio do setup;
- entrevista com agente;
- checklist de progresso;
- configuracao por area;
- painel de impacto;
- previa de impacto;
- revisao;
- publicacao parcial;
- reconfiguracao posterior.

Entrega:

- blueprint de telas de onboarding/configuracoes.

### 17. Plano de imagens

Decidir quais imagens precisam existir:

- setup inicial;
- conversa guiada;
- checklist;
- configuracao de area;
- cobranca/consumo;
- agentes/fluxos;
- regras de seguranca/aprovacoes;
- uso/cotas;
- revisao/publicacao.

Entrega:

- lista de imagens novas e rotas que herdam imagens existentes.

### 18. Auditoria final

Cruzar tudo contra:

- fluxos de IA;
- casos de uso;
- paginas web;
- app mobile depois;
- 0/1/3/7 agentes;
- manual/copiloto/autonomo;
- cotas;
- permissoes;
- auditoria.

Entrega:

- decisao final do que entra no MVP e o que fica fora.

## Papel do agente de IA de setup

O agente de setup nao e o motor de configuracao.

Ele e a camada conversacional que ajuda o gestor a configurar corretamente, sem precisar entender termos tecnicos.

### O que ele faz

- conduz a entrevista;
- faz perguntas simples;
- explica opcoes;
- recomenda presets;
- lembra respostas anteriores;
- identifica contradicoes;
- pede confirmacao;
- mostra impacto;
- ajuda a simular cenarios;
- prepara rascunhos;
- orienta proximos passos;
- resume o setup para humano Taliya quando houver chamada.

### O que ele nao faz

- nao e fonte da verdade;
- nao salva regra sozinho;
- nao publica configuracao;
- nao ativa autonomia;
- nao ignora permissao;
- nao ignora politica;
- nao ignora cota;
- nao cria regra fora do sistema;
- nao configura por fora da interface oficial.

### Fluxo correto

1. Agente pergunta.
2. Gestor responde.
3. Sistema transforma resposta em rascunho estruturado.
4. Sistema valida.
5. Agente explica impacto.
6. Gestor aprova.
7. Sistema publica.
8. Auditoria registra.

### Papel durante suporte humano

Quando o studio agenda chamada com humano Taliya, o agente continua sendo util:

- resume respostas ja dadas;
- lista pendencias;
- mostra decisoes sensiveis;
- prepara contexto para o especialista;
- registra recomendacoes feitas durante a chamada;
- ajuda o gestor a revisar antes de publicar.

Mesmo nesse modo, o humano nao configura por fora. Ele orienta o gestor dentro do mesmo fluxo.

## Risco que este plano evita

- Criar telas bonitas sem motor claro.
- Criar configuracoes duplicadas.
- Deixar agente e CRM usando regras diferentes.
- Travar o CRM por falta de agente.
- Automatizar fluxo sem politica/cota/permissao.
- Confundir financeiro do studio com billing Taliya.
- Deixar reconfiguracao pos-go-live sem impacto.

## Proxima entrega

Comecar pela etapa 2:

`setup-configuration-inventory.pt-BR.md`

Esse inventario deve ser criado ja aplicando o contrato de integridade:

- se nao tiver impacto, nao entra;
- se for duplicado, consolidar;
- se for avancado demais, mover para pos-MVP;
- se for regra sensivel, marcar validacao obrigatoria.
