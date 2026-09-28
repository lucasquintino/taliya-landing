# Taliya CRM - Contrato De Pagamento, Mensalidade E Baixa

Status: decisao aprovada v0.1.
Data: 2026-05-19.

## Objetivo

Definir a arquitetura conceitual de pagamento e mensalidade para o Taliya CRM, separando claramente:

- plano;
- matricula/assinatura do aluno;
- cobranca;
- pagamento;
- baixa;
- liberacao de aulas/saldo.

Este contrato evita misturar meio de pagamento, recorrencia, link, baixa automatica e direito de aula.

## Decisao Principal

O modelo correto e:

`Plano gera cobranca.`

`Pagamento quita cobranca.`

`Baixa confirma pagamento.`

`Pagamento confirmado libera ou atualiza direito de aula/saldo.`

## 1. Plano

Plano define o que o aluno compra.

Exemplos:

- `Pilates 2x por semana`;
- `Pacote 8 aulas`;
- `Aula avulsa`;
- `Aula experimental`.

Plano pode definir:

- valor;
- recorrencia comercial;
- vencimento padrao;
- quantidade/frequencia de aulas;
- validade;
- regra de reposicao;
- se gera cobranca recorrente ou pontual.

Plano nao define:

- se o aluno paga com Pix, dinheiro ou cartao;
- se a baixa e manual ou automatica;
- se existe provedor conectado;
- se a cobranca sera automatizada.

## 2. Matricula Ou Assinatura Do Aluno

Matricula/assinatura liga um aluno a um plano.

Exemplo:

`Ana Martins esta no plano Pilates 2x por semana, com vencimento todo dia 10.`

Ela pode ajustar para um aluno especifico:

- data de inicio;
- dia de vencimento;
- plano escolhido;
- responsavel financeiro;
- status do vinculo;
- excecoes simples quando permitido.

No Setup Inicial, esse vinculo pode ser preparado quando alunos e planos ja existirem, mas detalhes avancados ficam para depois.

## 3. Cobranca

Cobranca e o valor que o Taliya espera receber.

Exemplo de mensalidade:

`Cobranca de junho - Ana Martins - R$ 360 - vence 10/06 - em aberto.`

Exemplo de pacote:

`Pacote 8 aulas - Ana Martins - R$ 420 - vence hoje - em aberto.`

Tipos:

- cobranca recorrente gerada por plano mensal;
- cobranca pontual gerada por pacote, aula avulsa ou ajuste;
- cobranca em rascunho antes de publicacao/confirmacao.

Status recomendados:

- `Rascunho`;
- `Em aberto`;
- `Vence hoje`;
- `Vencida`;
- `Pendente de confirmacao`;
- `Paga`;
- `Cancelada`.

## 4. Pagamento

Pagamento e o registro de como uma cobranca foi quitada.

Meios de pagamento do MVP:

- `Pix`;
- `Dinheiro`;
- `Cartao`.

Observacoes:

- `Link de pagamento` nao e meio de pagamento. E uma forma futura de cobrar por um meio online.
- `Recorrencia automatica` nao e meio de pagamento. E uma capacidade futura de gerar e baixar cobrancas recorrentes.
- `Boleto`, se existir futuramente, fica fora do Setup Inicial e depende de Pagamentos Taliya/pos-go-live.
- `Comprovante` nao e meio de pagamento. E evidencia anexada quando a equipe registra uma baixa manual ou quando precisa justificar uma confirmacao.

## 5. Baixa

Baixa e como o Taliya confirma que o pagamento aconteceu.

Modos:

- baixa manual pela equipe;
- baixa com comprovante anexado;
- baixa automatica via Pagamentos Taliya quando houver conexao/provedor/webhook.

Importante:

- Pix nao e "manual" por natureza. Pix pode ter baixa manual ou automatica, dependendo de conexao.
- Cartao nao e "manual" por natureza. Cartao presencial tende a baixa manual; cartao online conectado tende a baixa automatica.
- Dinheiro tende a baixa manual.

No Setup Inicial, a baixa automatica nao deve ser configurada profundamente.

## 6. Liberacao De Aulas E Saldo

Depois que a cobranca e paga:

- mensalidade paga mantem ou libera o direito do ciclo;
- pacote pago libera o saldo de aulas;
- aula avulsa paga libera uma aula;
- regras de reposicao continuam vindo do plano.

Regra ja aprovada:

`A aula prevista consome saldo normalmente. Quando a regra permitir, o sistema gera uma reposicao para compensar a falta.`

## Setup Inicial

No Setup Inicial, o bloco `Pagamento` deve configurar apenas o minimo para operar, mas precisa explicar bem a operacao.
Ele nao deve parecer uma tabela tecnica de metodos nem uma configuracao por meio.
A pagina deve ser organizada em tres linhas completas, com hierarquia limpa:
meios aceitos, exemplo da operacao e Pagamentos Taliya.

### Estrutura Do Bloco Pagamento

O bloco deve ter tres linhas completas:

1. `Meios de pagamento`
   - linha completa no topo da area central;
   - cards fixos para `Pix`, `Dinheiro` e `Cartao`;
   - selecao multipla: o studio pode marcar um, dois ou os tres meios;
   - nenhum card abre configuracao propria no Setup Inicial;
   - nao existe criar meio personalizado no Setup Inicial;
   - nao mostrar boleto, transferencia, link de pagamento, "outro" ou gateway nesta tela.

2. `Exemplo da operacao`
   - segunda linha completa;
   - bloco visual obrigatorio mostrando o que acontece com uma cobranca real, de forma generica;
   - exemplo: `Plano gera cobranca. Aluno paga por um meio aceito. Equipe registra a baixa no Taliya. Cobranca fica paga. Aulas ou saldo sao liberados.`;
   - nao deve mencionar um meio especifico como Pix, dinheiro ou cartao;
   - a simulacao serve para o dono entender como o CRM vai funcionar no dia seguinte.

3. `Depois: Pagamentos Taliya`
   - terceira linha completa;
   - bloco explicativo, nao configuravel;
   - explica que baixa automatica, Pix conectado, cartao online, recorrencia automatica e webhooks entram depois em `Pagamentos Taliya`;
   - deve deixar claro que Pagamentos Taliya nao faz parte do Setup Inicial;
   - deve deixar claro que isso nao bloqueia o inicio da operacao;
   - deve mostrar o caminho: `Entender Pagamentos Taliya`, sem abrir KYC/provedor no Setup Inicial.

No Setup Inicial, o bloco `Pagamento` deve configurar:

- meios aceitos no inicio: Pix, dinheiro e cartao;
- comprovante sempre permitido no registro de baixa, sem precisar configurar isso no Setup Inicial;
- pendencia informativa para ativar Pagamentos Taliya depois, fora do Setup Inicial.

O Setup Inicial nao deve pedir mensagem/instrucao para o aluno.
Textos como "envie o comprovante pelo WhatsApp" pertencem a comunicacao, automacoes e mensagens de cobranca configuradas depois do go-live.

O Setup Inicial nao configura profundamente:

- baixa automatica;
- Pix automatico/conectado;
- cartao online;
- recorrencia automatica;
- mensagens automaticas de cobranca;
- instrucoes enviadas ao aluno;
- provedor;
- KYC;
- conciliacao;
- split/repasse;
- nota fiscal;
- antifraude;
- regras avancadas de inadimplencia;
- contratos financeiros;
- descontos/cupons/comissoes.

## Pagamentos Taliya Pos-Go-Live

Depois do go-live, em Configuracoes Financeiras, o studio pode ativar:

`Pagamentos Taliya`

Pagamentos Taliya nao e etapa do Setup Inicial.

Pagamentos Taliya e a integracao com provedor financeiro que permite automacoes como baixa automatica, Pix automatico, cartao online, recorrencia e webhooks.

Decisao de produto:

- Taliya deve expor uma experiencia propria, nao uma escolha de provedores;
- o studio nao deve precisar escolher Asaas, Mercado Pago, Stripe etc.;
- por tras, a Taliya escolhe um provedor principal e pode usar subcontas/recebedores.

Pagamentos Taliya pode habilitar:

- Pix com baixa automatica;
- cartao online;
- recorrencia automatica;
- link/checkout quando fizer sentido;
- webhooks de pagamento;
- futuras rotinas de conciliacao.

Depois que Pagamentos Taliya estiver ativo:

- os planos continuam gerando cobrancas do mesmo jeito;
- os planos nao passam a escolher meio de pagamento;
- Pix Taliya, cartao online e recorrencia online viram capacidades disponiveis para cobrancas compativeis;
- baixa automatica acontece quando o provedor confirma pagamento online;
- meios manuais continuam existindo para dinheiro, cartao presencial, excecoes e falhas do online;
- recorrencia online depende da cobranca ser recorrente, normalmente vinda de plano mensal ou assinatura do aluno.

## Fluxo Da Mensalidade

1. Aluno esta vinculado a um plano mensal.
2. O Taliya gera uma cobranca do ciclo.
3. A cobranca fica em aberto ate ser paga.
4. O aluno paga por Pix, dinheiro ou cartao.
5. O pagamento e baixado manualmente/com comprovante ou automaticamente se Pagamentos Taliya estiver ativo.
6. O Taliya atualiza financeiro, aluno e direito de aula.

## Fluxo Do Pacote

1. Aluno compra um pacote.
2. O Taliya gera uma cobranca pontual.
3. Depois do pagamento confirmado, o saldo de aulas e liberado.
4. As aulas previstas consomem saldo.
5. Reposicao segue a regra do plano.

## Regra Para UI

A UI nao deve perguntar:

`Esse plano e Pix ou cartao?`

A UI deve trabalhar com:

`Esse plano gerou uma cobranca. Como essa cobranca foi paga/baixada?`

## Aceite

Esta arquitetura esta correta quando:

- meio de pagamento nao e confundido com recorrencia;
- link de pagamento nao aparece como meio principal no Setup Inicial;
- Pix pode ser manual ou automatico dependendo de conexao;
- recorrencia automatica fica fora do Setup Inicial;
- Pagamentos Taliya e pos-go-live;
- o Setup Inicial ainda permite o studio operar manualmente com controle no Taliya.
