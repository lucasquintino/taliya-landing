# Contrato do dataset

## Versionamento

`meta.version` identifica a especificação. `meta.activeMode` seleciona o modo de publicação. `modes` define CTAs, avisos e visibilidade. Não avaliar readiness pela existência de copy de lançamento.

## Estrutura

| Chave | Conteúdo | Renderizar? |
|---|---|---|
| `sections` | 14 slots com ordem, IDs, âncoras e finalidade | IDs/âncoras; não publicar o plano interno |
| `navigation`, `hero`, `trust` | Textos da primeira dobra e navegação | Sim, respeitando modo |
| `selector` | 5 casos com conversa e resultado | Sim; contexto fictício em nota legível |
| `comparison` | 7 frentes, antes/depois, exemplo e destino | Sim |
| `how` | 6 tabs, itens internos e estados | Copy e itens; não guardrails |
| `messageWall` | 84 mensagens e 24 IDs iniciais | Seleção, não todos simultaneamente |
| `fronts` | 7 frentes, 39 subtipos | Campos de copy conforme abaixo |
| `flows` | 5 cenários com 4 passos cada | Conversa e snapshot de cada passo |
| `onboarding`, `offer`, `proof` | Caminho inicial, oferta e prova | Condicionado a modo/gates |
| `faq` | 14 perguntas com resposta por modo | Somente resposta do modo ativo |
| `forms`, `footer` | Fields, estados e links | Sim, após integração real |
| `runtime` | URLs/endpoint externos | Configuração, nunca imprimir `null` |
| `implementation`, `assets`, `qa`, `sources` | Instruções, insumos e aceite | Não publicar |

## Subtipo de uma frente

`id`, `label`, `when`, `message`, `organizes`, `reply`, `next`, `result` são os campos de UI. `demoContext` e `guardrail` descrevem as condições do cenário e a regra de produto; não são textos de propaganda. O contexto pode ser resumido numa label de exemplo, mas nunca tratado como dados reais do visitante.

`result` é texto de especificação e pode ser separado em pares label/valor para reutilizar o componente aprovado. Não converter esse texto em chamadas ao produto real. Algumas respostas pedem confirmação; nesse caso a UI não pode mostrar a alteração como concluída antes da confirmação ilustrada.

## Referências cruzadas

`messageWall.messages[].targetSubtype`, `selector[].detailTarget` e `comparison[].detailTarget` apontam para `fronts[].subtypes[].id`. Exemplo: `AG04` identifica a demonstração de remarcação. `#o-que-resolve?frente=AG&caso=AG04` é um fragmento interpretado localmente; não é endpoint de backend.

`how[].target` pode ser âncora de seção ou ID de FAQ. Para FAQ, localizar a pergunta, abri-la e mover o foco de forma acessível. Mensagem clicada no mural abre demonstração; nunca envia WhatsApp nem executa comando de negócio.

## Fluxos

`steps[]` guarda o estado acumulado do cenário. Selecionar o passo 3 deve exibir o resultado após os passos 1–3, mesmo se o visitante não clicou neles. Ao trocar cenário, não carregar dados do anterior. O simulador da landing não cria registros reais.

## Datas e valores

Usar o relógio fictício da especificação. Ao adaptar a data para uma publicação futura, mudar mensagens, resultados, dias da semana e limites do pacote juntos. Centavos e quantidade nos exemplos devem ser tratados deterministicamente, sem pedir a um modelo para recalcular na landing.

## Formulários

`waitlist` recebe nome, e-mail e pedido de avisos; `fit` recebe rotina e e-mail. O segundo não se inscreve automaticamente na lista. Estados: idle → validating → submitting → success/error/unknown. Endpoints, mensagens e política de tratamento precisam ser reais antes da captura. As mensagens já estão prontas, mas isto não implementa o servidor.
