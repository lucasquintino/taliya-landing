# Contexto e estado da continuidade

Data de preparação: 24/09/2026. Este documento registra somente o contexto
necessário para a migração desta landing, sem importar decisões de outros
projetos ou conversas como requisitos adicionais.

## Decisões do usuário

A marca continua **Taliya**. A landing existente usa o código e a narrativa
Taliya Pilates; o produto foi pivotado para o projeto Copiloto. O pedido é
criar um **novo projeto usando o mesmo código-fonte**, preservando a base
visual/técnica e alterando o conteúdo conforme os dois pacotes fornecidos.

O usuário acrescentou o uso de **SDD, preferencialmente uma spec por seção**.
O prompt mestre v2 detalha isso em 17 recortes: 001 fundação, 002 SEO,
003–016 correspondentes a S01–S14, e 017 integração. A divisão não exige
reorganizar o código nem criar um componente por documento.

O pedido atual é reunir os materiais em ZIP porque o download do MD não
funcionou. Este pacote transfere os materiais disponíveis, não representa
uma nova rodada de implementação ou aprovação de funcionalidades extras.

## Fontes incluídas

| Fonte | Onde está | Papel |
|---|---|---|
| Prompt mestre SDD v2 | `02_PROMPT_MESTRE_SDD.md` e `.txt` | Regras de escopo, preservação, SDD e execução |
| Landing v1, de 18/09/2026 | `05_PACOTES_EXTRAIDOS/landing/Taliya_Landing_v1/` | Copy, cenários, especificação e QA da landing |
| SEO v1.1, de 19/09/2026 | `05_PACOTES_EXTRAIDOS/seo/` | Adendo de arquitetura pública, SEO e aceitação |
| ZIPs de origem | `06_ZIPS_ORIGINAIS/` | Preservação integral dos anexos recebidos |

O prompt mestre foi copiado sem alteração de conteúdo; apenas seu nome no
pacote foi abreviado para facilitar a ordem de leitura. O TXT é uma cópia
idêntica e pode ser usado quando o editor não abrir Markdown.

## O que foi feito e o que não foi feito

| Item | Estado nesta conversa |
|---|---|
| Direção da migração | Definida pelo usuário |
| Prompt completo de execução com SDD | Preparado na versão v2 |
| Catálogo dos 17 recortes | Definido no prompt e reproduzido no mapa auxiliar |
| Reunião dos dois pacotes | Concluída, com originais e conteúdo extraído |
| Código-fonte original | Não fornecido entre os anexos desta conversa |
| Inspeção de componentes, rotas e scripts reais | Não executada |
| Cópia independente da aplicação | Não criada aqui |
| Inicialização/configuração do Spec Kit | Não executada aqui |
| 17 specs detalhadas e planos baseados no código | Ainda a produzir no ambiente de implementação |
| Mudanças na landing | Não implementadas aqui |
| Testes funcionais, visuais e SEO da aplicação | Não executados aqui |
| Publicação e alterações no projeto original | Não realizadas; não autorizadas por este pacote |

A verificação de integridade do ZIP comprova que os documentos foram
transportados sem corrupção. Ela não comprova a qualidade/implementação
da landing nem atualiza automaticamente resultados históricos dos pacotes.

## Limites a manter

A tarefa é a landing, não a implementação do aplicativo. A versão inicial
continua em pré-lançamento. Preserve o código original e trabalhe numa cópia
independente. Não transforme a migração em redesign, upgrade de stack,
reorganização de arquitetura ou criação de infraestrutura não solicitada.

Não acrescente recursos citados em outros projetos ou discussões sem uma
nova instrução expressa para esta landing. Respeite os limites, gates e
estados presentes no prompt e no dataset. Não invente preço, prova social,
integração, destino de CTA ou uma oferta já disponível.

O adendo SEO altera pontos específicos do pacote da landing, inclusive o
tratamento do legado. Não aplique um redirect antigo só porque ele aparece
num arquivo anterior. Use a hierarquia do prompt e registre bloqueios reais.

## Dependências externas

A implementação requer acesso ao código-fonte e a um ambiente apropriado.
A leitura dos documentos pode avançar sem eles, mas nomes de arquivos,
componentes, scripts e testes não devem ser inventados. Se o código já foi
fornecido no novo ambiente, a próxima conversa deve utilizá-lo.

Configurações de formulário, destinos externos, políticas revisadas e
credenciais autorizadas são dependências separadas, quando aplicáveis.
Não envie segredos no pacote documental. Não simule sucesso de formulário
nem publique políticas jurídicas não revisadas para eliminar uma pendência.

## Retomada exata

Começar pela leitura integral do prompt, identificação das fontes e inspeção
da base real. Preparar a cópia independente e o baseline; estabelecer a
Constitution e as instruções do agente conforme o projeto; iniciar 001 e
os contratos de 002; definir as specs de seção e executar segundo suas
dependências. Manter `specs/README.md` com os estados reais e a próxima tarefa.

As instruções completas e os critérios estão em `02_PROMPT_MESTRE_SDD.md`.
Este resumo não os substitui.
