# Setup Inicial - Escopo Real De Configuracao

Status: contrato v0.1.
Data: 2026-05-14.

## Objetivo

Definir o que o cliente pode configurar durante o Setup Inicial e, principalmente, o que ele **nao** deve configurar nesse momento.

O Setup Inicial nao e uma versao menor de todas as Configuracoes do CRM.

Ele e um caminho guiado para deixar o studio apto a operar com seguranca, com o minimo de decisoes necessarias antes do primeiro uso.

## Decisao Principal

O Setup Inicial deve expor apenas configuracoes que atendem pelo menos um destes criterios:

- sem isso o CRM nao consegue abrir a operacao basica;
- sem isso a agenda, alunos, cobranca ou consumo ficam incoerentes;
- sem isso dados importados nao podem ser revisados/publicados com seguranca;
- sem isso uma acao sensivel ficaria sem responsavel humano;
- sem isso o sistema nao consegue separar `pronto agora` de `configurar depois`.

Todo o resto deve virar:

- preset seguro;
- default automatico;
- pendencia pos-go-live;
- configuracao avancada dentro do CRM;
- configuracao de Agentes/Fluxos;
- control plane;
- ou item removido do caminho principal.

## Regra De Ouro

O cliente nao deve ver tudo que o produto sabe configurar.

Ele deve ver apenas o que precisa decidir para comecar a operar.

## Uso Correto Do Inventario

O arquivo `setup-configuration-inventory.pt-BR.md` e um inventario interno completo.

Ele serve para mapear fonte da verdade, impacto, dono e classificacao das configuracoes.

Ele nao deve ser lido como lista de telas, etapas ou campos expostos ao cliente no onboarding.

Antes de uma configuracao aparecer no Setup Inicial, ela precisa passar pela pergunta:

> "Se o cliente nao decidir isso agora, o CRM fica inseguro, incoerente ou inutil para operar no primeiro dia?"

Se a resposta for nao, ela nao entra no Setup Inicial.

## O Que O Setup Inicial Deve Configurar

### 1. Identidade operacional minima

Entra:

- nome do studio, como primeira pergunta do `/onboarding`;
- unidade principal;
- mais de uma unidade apenas se o studio realmente tiver;
- horario geral de funcionamento;
- responsavel principal;
- equipe minima para operar;
- papeis padrao.

Nao entra:

- identidade visual profunda;
- campos customizados;
- permissoes finas;
- notificacoes detalhadas;
- preferencias pessoais por usuario;
- estrutura avancada de unidades.

### 2. Agenda minima para operar

Entra:

- tipos principais de aula;
- grade inicial ou forma de importar a grade;
- turmas/aulas iniciais;
- professor por turma/aula quando houver;
- capacidade por turma/aula;
- regra base de presenca;
- regra base de falta/no-show apenas no nivel necessario para consumo e reposicao.

Nao entra:

- otimizacao de grade;
- analise de capacidade;
- lista de espera avancada;
- encaixe automatico;
- bloqueios complexos;
- regras especificas por professor;
- regras especificas por sala;
- rotinas operacionais avancadas.

### 3. Alunos e dados iniciais

Entra:

- importar alunos, agenda, turmas, contatos, planos ou financeiro basico quando o studio ja tiver dados;
- uma importacao por vez, sempre com dominio claro;
- cadastrar manualmente o minimo quando nao houver arquivo;
- revisar dados extraidos de fontes digitais ou fisicas;
- resolver duplicidades e conflitos que bloqueiam publicacao;
- vincular aluno a plano/turma quando isso for necessario para operar.

Nao entra:

- historico completo;
- dados clinicos profundos;
- segmentacoes avancadas;
- campos customizados;
- enriquecimento de dados;
- saneamento perfeito de toda a base.

### 4. Planos, cobranca e consumo de aulas

Entra:

- default do studio para novos planos: mensalidade, pacote, hibrido ou avulso;
- varios planos vendidos;
- configuracao individual de cada plano;
- quantidade de aulas/direito de aula por plano;
- ciclo ou validade basica por plano;
- regra base de consumo por plano;
- regra base de reposicao por plano;
- vencimento/recorrencia basica;
- tolerancia simples de inadimplencia quando impactar agenda/consumo.

Nao entra:

- descontos complexos;
- cortesias detalhadas;
- estornos;
- contratos personalizados;
- regras financeiras raras;
- quebra-galhos financeiros sensiveis como configuracao aberta.

Regra: planos definem o que o aluno compra e quais direitos de aula ele tem. Pagamento nao deve ficar misturado neste bloco.

### 5. Pagamento basico

Entra:

- meios de pagamento aceitos no setup inicial: Pix, dinheiro e cartao;
- dados minimos para operar no inicio, como chave/instrucao Pix quando houver Pix;
- se o studio aceita dinheiro;
- se o studio aceita cartao presencial/maquininha;
- regra inicial de baixa: marcar manualmente, anexar comprovante quando aplicavel ou registrar pagamento confirmado pela equipe;
- responsavel inicial por confirmar pagamentos quando necessario;
- pendencia informativa para ativar `Pagamentos Taliya` depois do go-live.

Nao entra:

- conciliacao bancaria;
- split/repasse;
- nota fiscal;
- antifraude;
- gateway financeiro completo quando exigir configuracao operacional profunda;
- cobranca automatica sofisticada;
- Pix automatico/conectado;
- cartao online;
- recorrencia automatica;
- boleto;
- link de pagamento como meio principal;
- KYC/cadastro financeiro de provedor;
- regras financeiras raras;
- quebras-galho financeiros sensiveis como configuracao aberta.

Regra: pagamento vem depois de planos. Primeiro o usuario define o que vende; depois define como registra pagamentos no Taliya. O setup deve coletar somente o minimo para operar; `Pagamentos Taliya`, baixa automatica, cartao online, recorrencia automatica, conciliacao e regras financeiras avancadas ficam para Configuracoes Pos-Go-Live.

Contrato conceitual: ver `payment-membership-flow-contract.pt-BR.md`.

### 6. Canais basicos

Entra:

- canal principal de contato;
- WhatsApp principal do studio, assumindo que o studio usa WhatsApp como canal comum;
- conexao do WhatsApp apenas como decisao da etapa, nao como pergunta de diagnostico;
- email quando necessario;
- modelos essenciais com preset seguro;
- consentimento/opt-out basico quando houver envio externo.

Nao entra:

- editor completo de templates;
- tom de voz detalhado;
- comunicados em massa;
- campanhas;
- segmentacoes;
- janelas por fluxo de agente;
- automacoes de envio.

### 7. Agentes apenas preparados

Entra:

- agentes existentes no plano, lidos de Billing/Entitlements;
- status informativo dos agentes no setup, quando isso ajudar o usuario a entender o que vem depois;
- responsavel humano padrao como dono/admin do studio, ajustavel depois;
- pacotes recomendados de fluxos criados como rascunho/pendencia pos-go-live quando aplicavel.

Regra: o usuario nao deve responder se o plano tem agentes. Isso ja vem do plano contratado.

Regra: o usuario nao deve configurar agentes no Setup Inicial. No maximo, revisa uma preparacao default ou entende que a configuracao profunda fica para depois.

Nao entra:

- ativar fluxo;
- modo manual/copiloto/autonomo;
- cota por fluxo;
- fallback por fluxo;
- aprovador por fluxo;
- limite de tentativa;
- simulacao;
- publicacao de automacao;
- logs;
- incidentes;
- control planes.

### 8. Revisao e publicacao segura

Entra:

- resumo do que esta pronto;
- resumo do que esta pendente;
- bloqueios reais;
- publicacao parcial segura;
- registro/auditoria inicial;
- destino correto para ajustes pos-go-live.

Nao entra:

- simulacao operacional profunda;
- auditoria avancada;
- analise de risco detalhada;
- governanca de execucao;
- investigacao de falhas.

## O Que Deve Virar Default

Sempre que possivel, usar defaults/presets em vez de perguntas.

Exemplos:

- permissoes padrao por papel;
- filas operacionais basicas;
- tarefas/checklists padrao;
- notificacoes basicas para o gestor;
- politica de auditoria ativa;
- versao inicial das regras;
- templates essenciais quando envio externo for usado;
- status padrao de aluno importado;
- regras de seguranca conservadoras.

O usuario pode ajustar depois no CRM, mas nao precisa decidir tudo antes do primeiro uso.

## O Que Deve Virar Pos-Go-Live

Vai para Configuracoes do CRM depois do go-live:

- ajustes finos de agenda;
- ajustes financeiros avancados;
- templates completos;
- permissoes detalhadas;
- notificacoes;
- campos personalizados;
- regras por unidade, professor, sala ou grupo;
- relatorios e indicadores customizados.

Vai para Agentes/Fluxos depois do go-live:

- configuracao profunda de fluxo;
- modo manual/copiloto/autonomo;
- fallback;
- aprovacao por acao;
- limites;
- cotas por fluxo;
- simulacao;
- publicacao de automacoes.

Vai para Control Planes depois do go-live:

- execucoes;
- traces;
- incidentes;
- logs;
- auditoria operacional;
- cotas em uso;
- risco;
- pausas emergenciais.

## Criterio Para Uma Pergunta Entrar No Setup

Uma pergunta entra no Setup Inicial se:

- a resposta muda uma regra necessaria para operar;
- a resposta evita erro operacional no primeiro dia;
- a resposta decide uma publicacao ou bloqueio;
- a resposta define responsavel humano;
- a resposta permite importar/revisar dados reais.

Uma pergunta nao entra se:

- so melhora personalizacao;
- so atende caso raro;
- so existe para agente autonomo;
- pode ser default seguro;
- pode ser ajustada depois sem quebrar operacao;
- exige que o gestor entenda detalhe tecnico.

## Implicacao Para As Paginas

As paginas do Setup Inicial devem ser poucas e sequenciais.

O usuario nao escolhe livremente configurar tudo.

Ele segue uma trilha orientada:

1. entrada/retomada;
2. diagnostico curto;
3. Studio;
4. Equipe;
5. Canais;
6. Planos;
7. Pagamento;
8. Alunos;
9. Turmas;
10. Agenda;
11. Revisao/publicacao.

Observacao: dentro de `/onboarding/setup`, o stepper operacional mostra os 9 blocos configuraveis: `Studio`, `Equipe`, `Canais`, `Planos`, `Pagamento`, `Alunos`, `Turmas`, `Agenda` e `Revisao`.

Areas avancadas podem aparecer como pendencia ou proximo passo, mas nao como configuracao aberta no onboarding.

## Diagnostico Nao Configura

O diagnostico nao deve perguntar nada que:

- ja vem do plano contratado;
- ja e default do sistema;
- sera decidido naturalmente quando a tela da etapa aparecer;
- nao muda uma decisao imediata do setup.

Exemplos que nao devem entrar no diagnostico:

- perguntar se o plano tem agentes;
- perguntar se o usuario quer importar dados agora;
- perguntar se o studio trabalha com horarios fixos quando isso ja e comportamento padrao do sistema;
- perguntar quais agentes quer configurar;
- perguntar preferencias finas de agenda, canais ou permissoes.

## Aceite

Este contrato esta correto quando:

- o Setup Inicial nao parece o hub completo de Configuracoes;
- o usuario nao consegue abrir dezenas de ajustes antes do go-live;
- cada etapa tem uma decisao clara;
- a maioria das regras nao essenciais vira default ou pendencia;
- o CRM consegue operar manualmente com 0 agentes;
- planos com 1/3/7 agentes preparam agentes sem configurar fluxos;
- o usuario entende que ajustes profundos vem depois, sem ser bombardeado por avisos.
