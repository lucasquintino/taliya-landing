# Setup Inicial - 51K Bloco 5 Pagamento Aprovado

Status: aprovado v0.1.
Data: 2026-05-20.

Imagem aprovada:

`D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\51K_round-4.1J_onboarding_bloco-5-pagamento-aprovado.png`

## Objetivo

Validar o Bloco 5 do Setup Inicial: `Pagamento`.

Este bloco define quais meios de pagamento o studio aceita no comeco da operacao e explica como o Taliya registra cobrancas, baixas e liberacao de aulas ou saldo.

A tela responde:

`Como o studio aceita pagamentos agora, sem configurar automacao financeira profunda?`

## Decisao Principal

O bloco `Pagamento` no Setup Inicial nao configura detalhes tecnicos por meio.

O usuario apenas seleciona os meios aceitos hoje:

- `Pix`;
- `Dinheiro`;
- `Cartao`.

Os meios sao selecao multipla. O studio pode selecionar um, dois ou os tres.

Nao existe configuracao individual de Pix, dinheiro ou cartao nesta etapa.

## Escopo Do Setup Inicial

O bloco `Pagamento` pode:

- selecionar meios aceitos no inicio;
- explicar como uma cobranca e quitada dentro do Taliya;
- mostrar que a baixa inicial e registrada pela equipe;
- mostrar que comprovante sempre pode ser anexado no registro de baixa;
- explicar que pagamento confirmado libera aulas ou saldo;
- apresentar `Pagamentos Taliya` como automacao pos-go-live.

Nao configurar aqui:

- chave Pix;
- tipo de chave Pix;
- Pix automatico;
- conta bancaria;
- maquininha;
- cartao online;
- link de pagamento;
- boleto;
- gateway/provedor;
- KYC;
- recorrencia automatica;
- conciliacao;
- webhooks;
- instrucoes automaticas para aluno;
- mensagens de cobranca;
- nota fiscal;
- split/repasse;
- antifraude;
- regras avancadas de inadimplencia.

## Estrutura Aprovada Da Tela

A tela usa o shell global aprovado em `51A`, com:

- stepper lateral esquerdo;
- header do onboarding;
- rodape global de rascunho/pendencias;
- painel lateral do Agente de Configuracao no padrao `51B`.

Na area central, a estrutura aprovada tem tres linhas completas:

1. `Meios de pagamento`;
2. `Exemplo da operacao`;
3. `Pagamentos Taliya`.

Nao usar grid 2x2 nem cards concorrentes.

Nao criar card separado de `Como o Taliya vai entender`.

## Linha 1 - Meios De Pagamento

Titulo:

`1. Meios de pagamento`

Subtexto:

`Selecione os meios que o studio aceita hoje. Os detalhes tecnicos e automacoes ficam para depois.`

Cards aprovados:

1. `Pix`
   - subtexto: `Pagamento por Pix`;
   - checkbox marcado.
2. `Dinheiro`
   - subtexto: `Recebido presencialmente`;
   - checkbox marcado.
3. `Cartao`
   - subtexto: `Cartao presencial`;
   - checkbox marcado.

Os cards sao multi-selecao.

Nao usar radio.

Nao destacar apenas um card como meio principal.

## Linha 2 - Exemplo Da Operacao

Titulo:

`2. Exemplo da operacao`

Esta linha deve ser um bloco visual amplo e generico.

Etapas aprovadas:

1. `Plano gera cobranca`;
2. `Aluno paga por um meio aceito`;
3. `Equipe registra a baixa no Taliya`;
4. `Cobranca fica paga`;
5. `Aulas ou saldo sao liberados`.

Texto auxiliar aprovado:

`Funciona para Pix, dinheiro ou cartao. No inicio, a confirmacao e feita pela equipe dentro do Taliya.`

O exemplo nao deve mencionar Pix como caso principal.

## Linha 3 - Pagamentos Taliya

Titulo:

`3. Pagamentos Taliya`

Selo:

`Pos-go-live`

Subtexto:

`Depois que o studio estiver operando, voce podera automatizar cobrancas e confirmacoes sem refazer este setup.`

Modulos aprovados:

1. `Pix automatico`
   - `Identifica pagamentos e baixa cobrancas.`
2. `Cartao online`
   - `Permite cobranca digital pelo Taliya.`
3. `Recorrencia automatica`
   - `Cobra mensalidades recorrentes.`
4. `Conciliacao`
   - `Ajuda a conferir pagamentos recebidos.`

Resumo aprovado:

- `Agora: registro e baixa manual no Taliya.`
- `Depois: automacao financeira em Pagamentos Taliya.`

Acao aprovada:

`Entender Pagamentos Taliya`

Este botao e informativo. Nao abre configuracao profunda no Setup Inicial.

## Acoes Do Bloco

Acoes aprovadas:

- `Salvar rascunho`;
- `Configurar pagamento depois`;
- `Continuar`.

`Configurar pagamento depois` deve significar deixar a decisao/revisao de pagamento para depois, nao abrir automacao financeira.

Na implementacao, se o label gerar ambiguidade, pode ser ajustado para:

- `Revisar depois`;
- `Deixar pagamento para depois`.

## Painel Do Agente

O painel do agente deve reforcar que o bloco e simples no input e forte na explicacao operacional.

Mensagem de impacto aprovada:

`Este bloco define quais meios o studio aceita no comeco da operacao.`

Balao 1:

`Voce so escolhe os meios aceitos agora. Nenhum detalhe tecnico precisa ser configurado neste setup.`

Balao 2:

`O Taliya ja consegue registrar cobrancas, baixas e liberacao de aulas. A automacao financeira vem depois.`

Chips aprovados:

- `O que e obrigatorio?`;
- `Como funciona a baixa?`;
- `O que fica para depois?`.

## Regras De Produto

Plano gera cobranca.

Pagamento quita cobranca.

Baixa confirma pagamento.

Pagamento confirmado libera ou atualiza direito de aula/saldo.

No Setup Inicial, tudo fica pronto para registro manual dentro do Taliya.

Automacao financeira entra depois, em `Pagamentos Taliya`.

## Nao Fazer

Nao mostrar nesta tela:

- configuracao individual por meio;
- chave Pix;
- tipo de chave Pix;
- maquininha;
- conta bancaria;
- boleto;
- link de pagamento como meio;
- gateway/provedor;
- KYC;
- cartao online como meio inicial;
- recorrencia automatica configuravel;
- Pix automatico configuravel;
- campo de instrucao para aluno;
- toggle de comprovante;
- tabela principal;
- card separado de `Como o Taliya vai entender`;
- bloco de planos prontos para cobranca.

## Criterios De Aceite

- A area central tem apenas tres linhas completas.
- Os meios de pagamento sao multi-selecao.
- Nenhum meio abre configuracao propria no Setup Inicial.
- O exemplo da operacao e generico.
- O usuario entende que o Taliya registra cobrancas, baixas e liberacao de aulas/saldo.
- O usuario entende que automacao financeira fica para pos-go-live.
- A tela nao parece configuracao de gateway.
- A tela nao cria complexidade desnecessaria no Setup Inicial.
