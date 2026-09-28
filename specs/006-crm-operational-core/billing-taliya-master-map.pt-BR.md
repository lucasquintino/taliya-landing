# Taliya CRM - Mapa Mestre De Billing Taliya

Status: mapa mestre v1.
Data: 2026-05-25.

## Objetivo

Definir Billing Taliya como a camada que controla a relacao comercial entre o studio e a Taliya.

Billing Taliya nao e:

- financeiro dos alunos;
- pagamento dos alunos;
- plano vendido pelo studio;
- Pagamentos Taliya/provedor financeiro;
- configuracao de plano, turma, agenda ou reposicao;
- builder de agente.

Billing Taliya responde:

- qual plano Taliya o studio contratou?
- quantos agentes estao inclusos?
- quais add-ons existem?
- quais cotas e limites comerciais existem?
- qual o status da assinatura?
- quais faturas existem?
- existe inadimplencia do studio com a Taliya?
- o que acontece com acesso, agentes e cotas se a assinatura falhar?

## Regra Central

Billing Taliya e fonte da verdade para:

- status do tenant;
- plano Taliya;
- agentes incluidos;
- add-ons;
- cotas contratadas;
- pacotes adicionais;
- faturas da Taliya;
- bloqueios comerciais;
- entitlements.

O CRM do studio apenas reflete isso.

O dono do studio pode visualizar, comprar/solicitar upgrade, ver faturas e resolver pendencias de assinatura, mas nao edita entitlement manualmente.

Decisao atualizada:

- Billing Taliya deve ter pagina propria no CRM web.
- Nao fica dentro de `/app/configuracoes/financeiro/pagamentos`.
- Nao e a mesma coisa que Pagamentos Taliya.
- Pode aparecer como aviso/atalho em Configuracoes, Uso/Cotas e Agentes, mas a fonte visual e `/app/billing`.

## Fronteira Com Outras Areas

| Area | O que responde | O que nao responde |
|---|---|---|
| Billing Taliya | plano contratado com a Taliya, faturas, add-ons, agentes inclusos, cotas comerciais | mensalidade dos alunos |
| Financeiro do studio | cobrancas, pagamentos, inadimplencia e documentos dos alunos | assinatura do studio com a Taliya |
| Pagamentos Taliya | automacao financeira do studio via provedor | cobranca da Taliya ao studio |
| Uso/Cotas | consumo real e restante | preco/plano comercial sozinho |
| Agentes/Fluxos | configuracao de agentes e fluxos dentro do entitlement | comprar plano ou alterar billing |
| Internal Billing | operacao interna Taliya de assinatura e entitlements | tela do dono operar sozinho tudo |

## Rotas Do Studio

### `/app/billing`

Funcao:

- mostrar assinatura Taliya do studio;
- mostrar plano atual;
- mostrar agentes inclusos;
- mostrar status da assinatura;
- mostrar resumo de cotas e add-ons;
- mostrar proxima fatura;
- mostrar alertas de billing;
- encaminhar para faturas, add-ons, upgrade ou suporte.

Deve conter:

- plano atual;
- status: ativo, trial, vencendo, pagamento falhou, suspenso, cancelado;
- agentes inclusos;
- agentes usados;
- add-ons ativos;
- cotas principais;
- proxima fatura;
- metodo de pagamento da assinatura, quando aplicavel;
- CTA de resolver pagamento, trocar plano, ver faturas, comprar add-on, falar com suporte.

Imagem aprovada:

- `65_round-4.1N_billing_01_assinatura-taliya-aprovado.png`.

Contrato visual aprovado para estado ativo:

- breadcrumb `Billing / Assinatura`;
- titulo `Assinatura Taliya`;
- subtitulo `Plano, agentes, cotas e faturas da sua conta Taliya.`;
- chips de status no topo: `Ativo`, plano contratado e data de renovacao;
- card `Plano atual`;
- card `Agentes inclusos`;
- card `Cotas do ciclo`;
- card `Proxima fatura`;
- card `Add-ons ativos`;
- painel direito com `Agente de Suporte Taliya`, nao Agente de Configuracao.

Ajustes aprovados sobre a imagem:

- remover a barra inferior de botoes duplicados na implementacao final;
- trocar `Trocar plano` por `Ver opcoes de plano` ou `Solicitar troca`, para nao sugerir alteracao automatica de entitlement;
- sidebar ativa deve representar Billing/Assinatura, Uso/Cotas ou Configuracoes, nao Agenda;
- manter a cota apenas como resumo; detalhe continua em `/app/uso`.

Nao deve conter:

- cobrancas de alunos;
- Pix/dinheiro/cartao do studio para alunos;
- baixa de aluno;
- comprovante de aluno;
- criacao de plano do aluno;
- configuracao de agente/fluxo.

### `/app/billing/invoices`

Funcao:

- listar faturas da Taliya para o studio.

Deve conter:

- faturas;
- status de cada fatura;
- valor;
- vencimento;
- periodo;
- download/visualizacao;
- link para pagamento/portal quando aplicavel;
- falhas de pagamento.

Imagem aprovada:

- `66_round-4.1N_billing_02_faturas-taliya-aprovado.png`.

Contrato visual aprovado:

- breadcrumb `Billing / Faturas`;
- titulo `Faturas Taliya`;
- subtitulo `Pagamentos da assinatura do studio com a Taliya.`;
- chips de topo: assinatura ativa, fatura em aberto e metodo recorrente;
- card `Fatura atual`;
- historico curto de faturas;
- painel direito com `Agente de Suporte Taliya`, nao Agente de Configuracao.

Regra de recorrencia:

- a assinatura Taliya e recorrente;
- `Pagar agora` nao e CTA padrao para fatura em aberto dentro do prazo;
- fatura em aberto mostra `Abrir fatura`, `Baixar PDF` e, quando necessario, `Atualizar pagamento`;
- `Resolver pagamento` aparece em `pagamento_falhou`, `vencida`, `limitado` ou `suspenso`;
- `Pagar agora` so pode aparecer se a estrategia comercial permitir pagamento manual/portal para regularizacao, nunca como acao normal de uma fatura recorrente saudavel;
- fatura `em_processamento` mostra `Aguardando confirmacao` sem CTA de pagamento.

Nao deve conter:

- recibos dos alunos;
- documentos financeiros do studio;
- notas/recibos de aula;
- conciliacao do financeiro do studio.

### `/app/billing/add-ons`

Funcao:

- mostrar extras comerciais que o studio pode adicionar ou solicitar na assinatura Taliya.

Pode conter:

- pacote extra de cota;
- agente adicional, se o modelo permitir;
- pacote de mensagens/uso, se existir;
- recurso premium, se existir;
- historico de add-ons ativos.

Imagem aprovada:

- `67_round-4.1N_billing_03_add-ons-taliya-aprovado.png`.

Contrato visual aprovado:

- breadcrumb `Billing / Add-ons`;
- titulo `Add-ons Taliya`;
- subtitulo `Extras para ampliar agentes e cotas da sua assinatura.`;
- chips de topo: plano atual, add-ons ativos e uso resumido de cota;
- bloco `Add-ons ativos`, com estado vazio quando nao houver add-on ativo;
- bloco `Disponiveis`, com poucos cards;
- card `Pacote extra de mensagens`;
- card `Mais agentes`, que no Plano 7 aparece como `Plano maximo`;
- card `Cota personalizada`, como `Sob consulta`;
- painel direito com `Agente de Suporte Taliya`.

Regra de ativacao:

- add-on altera entitlement e so entra depois de confirmacao confiavel de billing;
- o botao `Adicionar pacote` nao libera cota imediatamente;
- na implementacao final, o CTA pode ser `Solicitar pacote`, `Adicionar via billing` ou abrir fluxo/portal de confirmacao;
- se o checkout falhar ou ficar pendente, o add-on aparece como `Pendente de confirmacao`, nao como ativo;
- agentes adicionais so aparecem como compra direta se o modelo comercial permitir; no Plano 7, mostrar `Plano maximo` ou suporte comercial.

Nao deve conter:

- configuracao do fluxo do agente;
- detalhamento tecnico de cada execucao;
- desconto comercial manual sem suporte/Taliya.
- checkout completo;
- cupom;
- metodo de pagamento;
- financeiro dos alunos;
- Pagamentos Taliya;
- controle fino de cota por fluxo;

### `/app/uso`

Relacao:

- Uso/Cotas mostra consumo e risco de limite;
- Billing mostra o plano e o que esta contratado;
- ambos precisam se cruzar, mas nao sao a mesma pagina.

Exemplo:

- `/app/uso` mostra que WhatsApp/IA consumiu 85% da cota.
- `/app/billing` mostra qual plano da Taliya inclui aquela cota e quais add-ons existem.

## Rotas Internas Taliya

### `/internal/billing`

Funcao:

- operar billing da Taliya para todos os studios.

Deve conter:

- lista de contas;
- status de assinatura;
- falhas de pagamento;
- trials;
- cancelamentos;
- upgrades/downgrades;
- add-ons;
- faturas;
- alertas de inadimplencia;
- filtros por risco.

### `/internal/billing/[accountId]`

Funcao:

- detalhe de billing de um studio.

Deve conter:

- studio/tenant;
- plano;
- status;
- faturas;
- metodo de pagamento;
- add-ons;
- historico de alteracoes;
- entitlements efetivos;
- falhas;
- notas internas;
- acoes permitidas por permissao interna.

### `/internal/tenants/[tenantId]/entitlements`

Funcao:

- mostrar plano, agentes, cotas, add-ons e limites efetivos do tenant.

Regra:

- essa pagina reflete e audita entitlements;
- alteracao deve vir de billing, checkout, add-on ou acao interna autorizada;
- agente interno nao altera entitlement sozinho.

## Entitlements

Entitlement e o que o studio tem direito de usar.

Campos minimos:

- plano Taliya;
- status da assinatura;
- numero de agentes inclusos;
- agentes ativaveis;
- agentes ativos;
- cotas principais;
- add-ons ativos;
- limites por plano;
- data de inicio;
- data de renovacao;
- origem da alteracao;
- auditTrailRef.

## Planos Taliya

O produto deve continuar suportando:

- 0 agentes;
- 1 agente;
- 3 agentes;
- 7 agentes.

Regra:

- o CRM base funciona com 0 agentes;
- agentes e automacoes dependem de entitlement;
- o numero de agentes contratado nao muda o que o CRM e;
- muda o que pode ser automatizado/copilotado.

Billing Taliya define o direito comercial.

Agentes/Fluxos define a configuracao operacional dentro desse direito.

## Status Da Assinatura

| Status | Significado | Impacto |
|---|---|---|
| `trial` | Studio em teste | Pode ter limite especial |
| `ativo` | Assinatura regular | CRM e entitlements funcionam |
| `pagamento_pendente` | Fatura aberta ou aguardando confirmacao | Aviso ao dono/admin |
| `pagamento_falhou` | Tentativa de cobranca falhou | Aviso forte e prazo de regularizacao |
| `em_graca` | Periodo de tolerancia | CRM segue, automacoes podem ser preservadas por prazo |
| `limitado` | Acesso ou automacoes limitadas | Recursos pagos podem pausar |
| `suspenso` | Assinatura bloqueada | Acesso limitado ao essencial/suporte/billing |
| `cancelado` | Assinatura encerrada | Acesso conforme politica de encerramento |

## Regra De Bloqueio

Billing Taliya nao deve derrubar o CRM operacional de forma opaca.

Se houver problema de assinatura:

1. mostrar aviso claro para Dono/Admin;
2. manter caminho para resolver pagamento;
3. manter acesso a billing/suporte;
4. preservar dados;
5. degradar primeiro recursos pagos/automacoes, quando aplicavel;
6. bloquear apenas conforme politica comercial da Taliya.

Regra simples:

- falha inicial de pagamento nao deve apagar dados nem sumir com o CRM;
- automacoes e agentes pagos podem ser pausados conforme status;
- operacao manual essencial deve ter tratamento seguro definido por politica comercial;
- suporte e faturas continuam acessiveis.

## Faturas Taliya

Fatura Taliya representa cobranca da Taliya para o studio.

Nao confundir com:

- cobranca do studio para aluno;
- mensalidade do aluno;
- recibo do aluno;
- nota/contrato financeiro do aluno.

Campos minimos:

- id;
- tenantId;
- periodo;
- valor;
- moeda;
- status;
- vencimento;
- pagoEm;
- metodo de pagamento;
- link/portal, se aplicavel;
- itens;
- plano;
- add-ons;
- auditTrailRef.

## Add-ons

Add-on e qualquer extra contratado alem do plano base.

Possiveis add-ons:

- pacote extra de cota;
- pacote de mensagens;
- agente adicional, se o modelo comercial permitir;
- recurso premium;
- suporte/servico adicional, se existir.

Regra:

- add-on altera entitlement somente depois de evento confiavel de billing;
- cliente nao altera entitlement diretamente no frontend;
- agente nao compra add-on sozinho.

## Relacao Com Uso/Cotas

Uso/Cotas mostra consumo.

Billing mostra direito contratado.

Exemplo:

- Billing: plano com 3 agentes e 10.000 creditos/mensagens/unidades de uso.
- Uso: 8.700 usados este ciclo.
- Agentes/Fluxos: fluxos pausados quando limite chega.

Rotas relacionadas:

- `/app/uso`;
- `/app/uso/extrato`;
- `/app/billing`;
- `/app/billing/add-ons`.

Decisao MVP:

- `/app/uso` absorve cotas, alertas, previsao, economia, bloqueios e downgrades;
- `/app/uso/extrato` mostra o ledger detalhado;
- pacotes extras ficam em `/app/billing/add-ons`;
- limites por fluxo ficam em Agentes/Fluxos.

## Relacao Com Agentes/Fluxos

Billing Taliya define:

- quantos agentes estao inclusos;
- quais familias de agentes estao liberadas;
- quais cotas comerciais existem;
- se o plano permite automacao especifica.

Agentes/Fluxos define:

- quais agentes estao configurados;
- quais fluxos estao ativos;
- modo manual/copiloto/autonomo;
- aprovacoes;
- fallback;
- limites operacionais por fluxo.

Se o plano nao cobre:

- a tela de Agentes/Fluxos mostra bloqueio por entitlement;
- pode oferecer upgrade;
- nao cria bypass por configuracao manual.

## Relacao Com Configuracoes Pos-Go-Live

Billing Taliya fica fora de Configuracoes Pos-Go-Live comuns.

Configuracoes Pos-Go-Live podem mostrar atalhos ou avisos, mas nao editam:

- plano Taliya;
- fatura;
- add-on;
- status de assinatura;
- entitlement.

## Relacao Com Pagamentos Taliya

Pagamentos Taliya:

- automatiza recebimentos do studio com seus alunos;
- usa provedor financeiro para Pix/cartao/recorrencia dos alunos;
- afeta Financeiro do studio.

Billing Taliya:

- cobra a assinatura do studio com a Taliya;
- define plano, agentes, add-ons e faturas da Taliya;
- afeta acesso e entitlements.

Essas duas areas nao devem compartilhar UI principal, nomes de objetos ou labels ambigua.

## Agente E Billing

O agente pode:

- explicar plano atual;
- explicar cota;
- explicar por que um recurso esta bloqueado;
- encaminhar para upgrade;
- resumir fatura;
- orientar como resolver pagamento falho;
- preparar ticket para suporte.

O agente nao pode:

- alterar plano sozinho;
- comprar add-on sozinho;
- perdoar fatura;
- remover bloqueio;
- alterar entitlement;
- conceder desconto;
- alterar metodo de pagamento;
- acessar billing interno sem permissao.

## Auditoria

Eventos que exigem auditoria:

- checkout confirmado;
- plano criado/alterado/cancelado;
- add-on comprado/cancelado;
- fatura paga/falha/cancelada;
- entitlement alterado;
- cota adicional liberada;
- tenant suspenso/reativado;
- acesso limitado por billing;
- acao interna Taliya em billing.

## Estados De UI

| Estado | Como aparece |
|---|---|
| Plano ativo | card normal com plano, agentes e proxima fatura |
| Trial | aviso de fim do teste e CTA de contratar |
| Pagamento falhou | alerta forte com resolver pagamento |
| Cota alta | aviso cruzado com Uso/Cotas |
| Add-on disponivel | card em `/app/billing/add-ons` |
| Entitlement bloqueado | bloqueio contextual em Agentes/Fluxos ou Uso |
| Suspenso | acesso limitado a resolver assinatura, suporte e dados essenciais conforme politica |

## O Que Nao Entra No MVP

Nao definir agora:

- marketplace complexo de add-ons;
- negociacao comercial customizada no app;
- cupom/desconto self-service avancado;
- billing multi-moeda;
- split/revenue share;
- nota fiscal complexa;
- contrato empresarial customizado;
- billing como central operacional do CRM.

## Mapa Final De Rotas

| Rota | Publico | Funcao |
|---|---|---|
| `/app/billing` | Dono/Admin do studio | Ver assinatura Taliya, plano, agentes, status, proxima fatura |
| `/app/billing/invoices` | Dono/Admin do studio | Ver faturas Taliya |
| `/app/billing/add-ons` | Dono/Admin do studio | Ver/comprar add-ons permitidos |
| `/app/uso` | Dono/Admin e papeis permitidos | Ver consumo e cotas |
| `/internal/billing` | Taliya Billing/Ops | Operar billing de todos os studios |
| `/internal/billing/[accountId]` | Taliya Billing/Ops | Detalhe de billing de um studio |
| `/internal/tenants/[tenantId]/entitlements` | Taliya Ops autorizado | Ver/validar entitlements efetivos |

## Decisao Final

Billing Taliya fica como familia propria:

- separada do financeiro dos alunos;
- separada de Pagamentos Taliya;
- separada das Configuracoes Pos-Go-Live comuns;
- ligada a Uso/Cotas;
- ligada a Agentes/Fluxos por entitlement;
- refletida no CRM do studio;
- operada profundamente no backoffice interno da Taliya.

Isso permite o dono entender o que contratou sem transformar billing em centro da experiencia operacional.
