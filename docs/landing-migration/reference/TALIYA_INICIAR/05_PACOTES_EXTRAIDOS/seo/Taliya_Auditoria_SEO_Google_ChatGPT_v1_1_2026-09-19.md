# TALIYA
# SEO, Google e descoberta no ChatGPT
## Auditoria técnica e plano de aquisição orgânica

**19 de setembro de 2026 • versão 1.1 — revisão da estratégia de rotas**

Adendo à Especificação Definitiva da Landing v1, de 18/09/2026.

**Decisão central**
Preservar a experiência da landing, corrigir a identidade pública do pivot e fazer da própria home uma fonte semanticamente completa, rastreável e citável. Rotas extras de recursos ficam condicionadas a evidência de necessidade; não entram no lançamento por padrão.

**Escopo**
Site público atual + especificação da nova landing + documentação oficial de Google, OpenAI e Bing. A Taliya continua em pré-lançamento. Este relatório não altera o site nem comprova funcionamento do produto.

**Não é uma promessa de posição.** Ser rastreável, indexado, bem posicionado, citado e recomendado são resultados diferentes. O plano define o trabalho e como medir cada um.

<!--PAGE-->
# 01. Conclusão executiva

**Revisão da decisão:** depois de confrontar a Especificação Definitiva da Landing com as intenções de busca que queremos atender, **não recomendo criar agora `/recursos/agenda`, `/recursos/orcamentos` e `/recursos/recebimentos`**. A home aprovada já contém profundidade suficiente para representar essas necessidades, desde que o conteúdo essencial seja entregue como texto semanticamente claro e rastreável, e não dependa de cliques para existir.

O problema mais evidente continua sendo outro: a informação pública ainda apresenta a Taliya como produto de Pilates. A raiz leva à página antiga, os metadados descrevem studios e a busca de marca consultada reproduz esse posicionamento. Uma pessoa ou sistema que encontra essas fontes recebe a definição anterior do produto. [L01, L02, L05]

| Prioridade | Decisão recomendada | Resultado verificável |
|---|---|---|
| P0 | Publicar o pivot de forma coerente | Home, descrição, legado, oferta e políticas representam o mesmo produto |
| P0 | Fazer a `/` responder às intenções centrais | Agenda, orçamento, recebimentos, clientes, serviços, lembretes e arquivos têm texto explícito e recuperável |
| P0 | Garantir leitura sem interação obrigatória | Conteúdo essencial das tabs, frentes e fluxos existe sem o crawler precisar clicar |
| P0 | Definir rastreamento e URLs canônicas | Respostas HTTP, robots, sitemap e canônicas testados; nenhuma exclusão acidental |
| P1 | Criar páginas institucionais úteis | Sobre, Segurança e políticas atualizadas aumentam clareza e confiança sem fragmentar features |
| P1 | Construir evidências do produto | Demonstrações fiéis agora; casos e resultados reais depois |
| P1 | Medir busca e IA separadamente | Indexação, impressões, citações, visitas e leads não se confundem |
| P2 | Criar novas rotas somente quando houver motivo | Busca distinta, conteúdo novo, dados de demanda ou necessidade de campanha/backlink justificam a URL |

**Para o Google:** conteúdo alinhado à intenção, acessível, útil e tecnicamente consistente. **Para o ChatGPT:** acesso para busca, informação pública clara e atual e razões verificáveis para apresentar a Taliya naquele contexto. Nenhuma das plataformas oferece garantia de inclusão, posição ou recomendação. [G01, O03]

Não recomendo refazer o layout, comprar links, gerar centenas de páginas por profissão, criar uma URL para cada feature ou transformar `llms.txt` no projeto principal. **Mais URLs não são, por si só, mais SEO.**

**Próxima ação concreta:** incorporar os requisitos P0 deste adendo à implementação da landing e publicar uma `/` semanticamente completa. Depois da indexação, usar Search Console, Bing, analytics e testes controlados de IA para decidir se alguma intenção merece uma página própria.

<!--PAGE-->
# 02. O que foi auditado — e o que não foi

A auditoria combinou leitura de páginas oficiais, navegação pública em navegador, consultas de descoberta e conferência do material aprovado. As conclusões abaixo não dependem de acesso a contas privadas inexistente nesta sessão.

| Fonte ou teste | Cobertura real | Limite |
|---|---|---|
| Taliya pública | Raiz, landing /pilates, planos legados e privacidade | Não houve login nem mudança de conteúdo |
| Arquivos técnicos | Fetch de robots.txt, sitemap.xml e llms.txt | Testados os caminhos indicados, não toda URL possível |
| Navegador | Head, títulos visuais, duas FAQs e links; 23 passos | Alguns resultados conflitantes não foram aceitos como fatos confirmados |
| Busca pública | Amostra de marca e de intenções de uso | Não é medição de posição fixa no Google |
| Benchmark | Meu Assessor e páginas de fornecedores encontradas | Oferta publicada não comprova performance ou funcionamento |
| Especificação v1 | Metadados, rotas, pré-lançamento e aceite | Documento não é código executado |
| Fontes oficiais | Google, OpenAI, Bing e web.dev | Conferidas em 19/09/2026 |

**Não medido:** Search Console da Taliya, Bing Webmaster Tools da Taliya, analytics, backlinks completos, logs de servidor, rastreamento real por IP de robô, headers brutos, renderização do Google, pontuação Lighthouse, Core Web Vitals e conversão. A integração de analytics encontrada no diretório não estava conectada à propriedade.

O navegador não permitiu validar uma viewport mobile real de 390 × 844. Portanto, não há aprovação de responsividade móvel nesta auditoria. A extração de texto renderizado também não prova que todos os 39 subtipos estejam no HTML inicial.

Uma tentativa de inspeção HTTP no ambiente local falhou por resolução de rede desse ambiente. Como a leitura externa do site funcionou, isso **não foi classificado como falha de DNS da Taliya**.

**Legenda do relatório:** observado = evidência pública recuperada; pendente = precisa de instrumento ou conta; recomendado = decisão proposta; planejado = consta da especificação, sem teste de produto.

<!--PAGE-->
# 03. Achados públicos confirmados

| ID | Evidência observada | Implicação e ação |
|---|---|---|
| A01 | A raiz consultada termina em /pilates | Publicar a home horizontal na raiz; eliminar a dependência da URL vertical |
| A02 | Title: “Taliya &#124; IA para studios de Pilates” | Corrigir a identidade que acompanha resultados e compartilhamentos |
| A03 | OG e Twitter ainda descrevem Pilates | Atualizar o conjunto, não apenas a headline visível |
| A04 | /pilates/planos continua apresentando planos antigos, incluindo Base de R$197 | Definir destino e mensagem do legado; não deixá-lo concorrer com a nova oferta |
| A05 | /robots.txt e /sitemap.xml retornaram 404 no fetch externo | Publicar arquivos deliberados e testar; sitemap alternativo não foi descartado |
| A06 | /llms.txt retornou 404 | Não é bloqueador nem falha de SEO por si só |
| A07 | Navegação extraída é dominada por âncoras; /privacidade aparece como rota separada | A home pode concentrar as features; rotas adicionais devem existir por função real, não por contagem de URLs |
| A08 | Política pública, datada de 27/05/2026, descreve atendimento comercial e alunos/studios | Revisar o texto para a nova operação e coleta; não tratar isso como auditoria jurídica |
| A09 | Busca “Taliya” + “WhatsApp” apresentou a marca com descrição de Pilates | A presença encontrada ainda ensina a categoria antiga |

Fontes dos achados: leitura pública e amostra de busca [L01–L05, L12]. O 404 dos arquivos técnicos foi retornado pelo fetcher e corroborado por página de erro no navegador; cabe confirmar o status bruto no deploy.

**Duas correções de interpretação são essenciais.** Para o Google, um robots.txt com 404 não equivale a bloquear rastreamento. Já um sitemap facilita a descoberta, mas não garante indexação e não é a única forma de localizar páginas. [G04, G05]

A ausência de `llms.txt` não deve receber a mesma prioridade de uma home errada ou de um `noindex` acidental. A documentação atual do Google diz que esse arquivo não altera sua visibilidade ou ranking. [G12]

**Também não foi encontrada evidência de que uma página de recurso seja necessária para cada capacidade.** O ponto crítico é se a `/` responde de forma explícita e recuperável à intenção. A decisão sobre rotas extras passa a ser orientada por necessidade distinta e dados, não por uma regra abstrata de SEO.

<!--PAGE-->
# 04. Itens que precisam de confirmação técnica

Algumas saídas de ferramentas entraram em conflito. Em vez de convertê-las em uma lista alarmista de erros, esta auditoria registra a incerteza e o teste que a resolve.

| Item | O que ocorreu | Como fechar o diagnóstico |
|---|---|---|
| Canonical atual | Fetch anterior indicou /pilates; navegador relatou raiz sem www | Comparar head bruto, DOM e URL escolhida pelo Google na inspeção |
| Quantidade de H1 | Navegador relatou 11; não entregou prova bruta suficiente na conferência | Enumerar tags reais no código/DOM, não títulos visuais |
| JSON-LD | Navegador relatou Organization | Extrair todos os scripts, validar JSON e conferir as URLs/perfis |
| Conteúdo de abas | FAQ foi recuperável; presença integral dos subtipos não foi comprovada | Comparar texto antes/depois de interação e HTML renderizado pelo Google |
| Alt e dimensões | Relato do navegador não foi consistente o bastante | Verificar atributos e espaço reservado de cada mídia no código |
| Noindex e bloqueios | Não foi encontrado bloqueio na extração; headers não inspecionados | Testar meta robots, X-Robots-Tag, robots e CDN/WAF |
| Velocidade | Nenhuma medição de laboratório ou campo concluída | Executar testes reais; manter campo sem nota enquanto não houver dados |

**Não concluo que existem 11 H1 problemáticos, que o canonical está definitivamente errado ou que falta Open Graph.** O OG foi recuperado e está desatualizado; é outro diagnóstico. Uma organização pode corretamente apontar para a raiz em seu JSON-LD mesmo quando está presente numa subpágina.

Recomendação sem depender dessas dúvidas: adotar um H1 principal e hierarquia lógica, manter metadados consistentes e usar o domínio canônico aprovado. Isso melhora entendimento e manutenção; não é uma alegação de penalidade automática por múltiplos H1. O Google usa várias fontes da página para compor o título do resultado. [G07]

A entrega de implementação deve anexar essas evidências reais. Uma ferramenta que resume a tela não substitui a inspeção do HTML e dos resultados da propriedade.

<!--PAGE-->
# 05. O que significa “aparecer e ser sugerido”

| Camada | Pergunta correta | Evidência necessária |
|---|---|---|
| Acesso | O robô consegue ler a URL? | HTTP, permissões, robots e logs |
| Indexação | A URL entrou na base do buscador? | Inspeção da URL e relatórios da propriedade |
| Relevância | A página responde à intenção pesquisada? | Consulta, conteúdo e público compatíveis |
| Ranking | Em que posição apareceu naquele contexto? | Medição com data, país, dispositivo e consulta |
| Citação | A resposta de IA usou/linkou a página? | Link e trecho na resposta ou relatório do provedor |
| Recomendação | O produto foi sugerido como opção adequada? | Resposta completa e contexto, não mera menção |
| Resultado comercial | A visita gerou interesse ou uso? | Lead real; ativação e receita somente no produto funcional |

Uma página pode ser indexada sem ranquear bem; pode ser citada por explicar um conceito sem que o produto seja recomendado. Uma resposta pode recomendar outra solução porque ela atende a autoagendamento, emissão fiscal ou equipes — necessidades fora da V1 atual da Taliya.

**A meta não deve ser ser recomendado para qualquer pedido.** Deve ser aparecer de forma correta quando o usuário procura uma rotina que a Taliya realmente atende. Isso reduz aquisição de pessoas frustradas por uma promessa incompatível.

No pré-lançamento, a meta plausível é descoberta da marca, entendimento da proposta e cadastro de interesse. Não vamos construir uma aparência de software disponível para ganhar uma recomendação de “melhor app para usar hoje”.

O Google exige elegibilidade técnica e indexação para suas experiências de IA; a OpenAI orienta acesso ao seu robô de busca. Nenhum desses requisitos assegura a seleção final. [G01, O01, O03]

**Resultado esperado deste plano:** remover obstáculos controláveis, oferecer informação melhor e criar uma medição confiável. Não há prazo ou posição garantida.

<!--PAGE-->
# 06. Busca: quais intenções a Taliya deve disputar

A tabela é uma priorização editorial proposta, não um estudo de volume ou dificuldade. “Alta” significa proximidade com a proposta e capacidade de produzir uma resposta útil; não previsão de tráfego. **Nesta revisão, cada intenção é primeiro mapeada para uma seção da própria home.**

| Grupo de intenção | Exemplo de busca | Prioridade | Cobertura inicial recomendada |
|---|---|---|---|
| Organização de serviços | app para organizar clientes e serviços | Alta | Hero + definição + frentes Clientes/Serviços + fluxos |
| Agenda operada pelo dono | agenda pelo WhatsApp para autônomo | Alta | Demo + frente Agenda + fluxo agendar/remarcar/cancelar |
| Orçamentos | fazer orçamento em PDF para cliente | Alta | Frente Orçamentos + fluxo orçamento→aprovação→agenda |
| Recebimentos | controlar entrada e saldo de serviço | Alta | Frente Recebimentos + mural + fluxo entrada→saldo→lembrete |
| Mudanças de agenda | como remarcar atendimento sem perder histórico | Alta | Frente Agenda + demonstração de mesma ocorrência atualizada |
| Sessões | controle de pacote de aulas ou sessões | Média-alta | Serviços + Agenda + fluxo Pacote |
| Lembretes | lembrar de cobrar cliente | Média | Frente Lembretes + exemplo condicional/contextual |
| Arquivos | organizar orçamento e fotos por cliente | Média | Frente Arquivos/Docs + fluxo de recuperação contextual |
| Produtividade genérica | melhor app de produtividade | Baixa no início | Não orientar a home por uma categoria ampla demais |

**Cuidado com as palavras que parecem perfeitas, mas atraem o problema errado.** “Agendamento automático no WhatsApp” pode significar bot atendendo clientes ou link de autoagendamento. “Cobrança pelo WhatsApp” pode significar emissão de link, régua automática ou recebimento bancário.

A solução não é criar uma nova URL para corrigir a ambiguidade. É explicitar o mecanismo dentro do conteúdo: “Você pede para marcar”, “Acompanhe o que falta receber”, “Peça um lembrete para cobrar”. Orçamento não deve aparecer como nota fiscal; mensalidade do cliente não é assinatura do SaaS.

Produtividade continua sendo um território relevante de distribuição e creators. Isso não obriga a home a disputar a expressão mais genérica de produtividade. O conteúdo deve partir da rotina de serviço.

<!--PAGE-->
# 07. O que o benchmark de busca acrescenta

A amostra pública encontrou fornecedores com páginas diretamente ligadas a problemas e também homepages amplas que cobrem várias rotinas. O benchmark serve para entender linguagem e competição por intenção, **não para concluir que uma feature precisa obrigatoriamente de URL própria**.

| Página observada | O que representa | Aplicação à Taliya |
|---|---|---|
| Meu Assessor /funcionalidades | Explicação pública aprofundada | Profundidade pode existir fora da home, mas não é pré-requisito de descoberta |
| Cotte | Orçamentos com entrada pelo WhatsApp | Demonstrar documento e mecanismo, não só “IA” |
| Interaup | Orçamentos em PDF e compartilhamento | Diferenciar criar, revisar, aprovar e compartilhar |
| Tramppo | Organização de prestadores | Explicar claramente o profissional e o trabalho atendidos |
| AgendaBot | Agenda e atendimento automatizado ao cliente | Evitar competir com uma promessa que a V1 não cumpre |

Fontes: páginas dos próprios fornecedores [L06–L10]. Não foi testada assinatura, qualidade, retenção ou conversão dessas soluções.

Também foi localizada uma página de benefício de sindicato profissional apresentando o Meu Assessor. Esse é um exemplo concreto de distribuição por entidade externa ligada a um público, não de comprovação independente das capacidades anunciadas. [L11]

**O aprendizado corrigido:** a Taliya precisa publicar conteúdo que explique com precisão sinal versus saldo, mudança de horário sem duplicação, pacote versus plano e limites do uso parcial. **Esse conteúdo pode começar na própria `/`**, porque a landing aprovada já possui componentes e profundidade suficientes.

A consulta de marca da Taliya já retornou a categoria antiga. Isso reforça a necessidade de atualizar site, perfil social e referências controladas conjuntamente. Não é evidência de que o domínio esteja penalizado nem de que precisemos multiplicar URLs para corrigir a entidade.

Não precisamos copiar a arquitetura inteira do concorrente. Precisamos deixar de depender exclusivamente de balões animados e garantir que a home tenha uma camada textual inequívoca, rastreável e útil.

<!--PAGE-->
# 08. Home: preservar a promessa e melhorar o contexto

A especificação atual usa o slogan como title. Recomendo manter o slogan no H1 visual e tornar o title mais descritivo para quem encontra a página fora de contexto. Isso não garante que o Google reproduza exatamente o texto enviado. [I01, G07]

**Title recomendado**  
Taliya | Organize serviços, agenda e recebimentos pelo WhatsApp

**H1 preservado**  
Seu negócio organizado. É só falar.

**Identificação acima do H1**  
Para quem trabalha por conta e presta serviços.

**Apoio — versão de lançamento**  
Registre o que combinou com seus clientes, organize horários e acompanhe o que falta receber. Fale com a Taliya no WhatsApp ou use o app para consultar e corrigir os mesmos registros.

**Apoio — versão pública de pré-lançamento**  
Estamos criando a Taliya para organizar os combinados, horários e recebimentos de quem presta serviços. Conheça a experiência planejada pelo WhatsApp e app e acompanhe os primeiros testes.

**Definição curta, dentro do conteúdo da página**  
A Taliya é um copiloto para organizar a rotina administrativa de quem presta serviços. Sua proposta conecta clientes, serviços, agenda, orçamentos, recebimentos, lembretes e arquivos. O profissional conversa com o número da Taliya e pode consultar e editar os mesmos registros no app.

Essa definição pode ficar na primeira aba de funcionamento ou em texto introdutório, sem acrescentar um bloco visual pesado. No pré-lançamento, manter o aviso de estágio próximo e visível.

Não usar uma lista de cinquenta profissões no rodapé como “texto de SEO”. Não trocar cada ocorrência de “Taliya” por uma sequência de palavras-chave. O visitante precisa reconhecer o produto, e os mecanismos de busca precisam receber a mesma descrição.

**Navegação interna:** usar âncoras HTML reais e descritivas para levar diretamente a Agenda, Orçamentos, Recebimentos e demais frentes dentro da `/`. Elas melhoram navegação e compartilhamento sem criar páginas artificiais. Rotas específicas só entram depois se houver motivo editorial/comercial próprio.

<!--PAGE-->
# 09. Requisitos por componente da landing

| Componente preservado | O que acrescentar para descoberta | Critério de aceite |
|---|---|---|
| Hero | H1 claro, categoria e definição em texto | A proposta existe mesmo sem ler a imagem |
| Seletor de 5 casos | Título, pedido e resultado textual de cada caso | Conteúdo não depende exclusivamente de interação |
| Sem/Com | Frases comparáveis e contexto real | Nenhuma promessa de ROI sem evidência |
| Seis abas | Resumo editorial por tópico | A informação principal existe no HTML/renderização sem novo fetch após clique |
| Mural de mensagens | Exemplos textuais selecionados e acessíveis | Sem centenas de repetições para robôs |
| Sete frentes | H2 da seção; H3 por frente/subtipo conforme hierarquia | Cada intenção central tem definição + exemplo + limite |
| Fluxos completos | Sequência textual acompanhando a animação | Orçamento, aprovação, data e pagamento não se confundem |
| Oferta | Preço e condições coerentes com o estágio | Sem oferta comprável inventada no pré-lançamento |
| FAQ | Perguntas e respostas reais em HTML | Abrir/fechar não dispara carregamento exclusivo do conteúdo essencial |
| Rodapé | Sobre, segurança, políticas e ajuda quando existirem | Links reais para páginas publicadas, sem rotas de recurso vazias |

**As 39 subcategorias não precisam virar 39 páginas.** Use-as como conteúdo da biblioteca da landing. As 84 mensagens também não precisam de uma URL cada. Nesta revisão, **nem mesmo as 7 frentes precisam de rotas próprias no lançamento**.

Para clones de um carrossel infinito, a apresentação não deve duplicar centenas de falas na árvore de acessibilidade. A implementação pode manter uma lista semântica única e tornar cópias decorativas não interativas e ocultas para tecnologias assistivas. Testar foco e leitura, não simplesmente aplicar `aria-hidden` em controles utilizáveis.

As âncoras continuam úteis para a navegação. `#agenda`, `#orcamentos` e `#recebimentos` continuam sendo partes da mesma página e não entram no sitemap como documentos independentes.

**Não há necessidade de redesenhar a home nem fragmentá-la para que ela seja legível.** O ajuste principal está na forma como o conteúdo é entregue, nomeado e relacionado.

<!--PAGE-->
# 10. Abas, JavaScript e conteúdo que exige clique

A pergunta técnica importante não é “o site usa React?”. É: **o conteúdo necessário aparece para quem carrega a página, ou só nasce depois de uma sequência de cliques?** O Google processa JavaScript, mas não interage com a página para revelar conteúdo essencial. [G02, G03]

Recomendação para a implementação da Taliya: entregar os textos essenciais de seções, casos e perguntas em HTML renderizável sem ação humana. A interface pode continuar exibindo uma aba por vez. Renderização no servidor ou geração estática são bons caminhos de implementação; não são um requisito mágico de ranking.

**Não confundir quatro coisas:** texto no HTML; texto que só aparece após execução de JavaScript; texto guardado em JSON dentro de um script; texto que só é requisitado ao clicar. Uma ferramenta encontrar palavras em um pacote de dados não prova que o mecanismo de busca as viu como conteúdo de página.

### Teste obrigatório

1. Salvar resposta HTTP e head da URL final em produção.
2. Carregar a página em navegador sem clicar, extrair o texto do DOM e os links.
3. Abrir exemplos inativos e comparar se o conteúdo já existia ou foi criado sob demanda.
4. Inspecionar a URL publicada no Search Console e comparar o HTML renderizado.
5. Repetir após minificação, otimizações de performance e mudanças de consentimento.

Para a home, amostrar as sete frentes, não apenas a primeira. Em páginas institucionais adicionais, verificar título, definição, escopo e links. Mídia pode carregar depois; a explicação principal não deve ficar vazia esperando animação.

As respostas de FAQ foram recuperadas pela extração pública. Isso é um sinal favorável, mas não certifica todos os painéis nem o HTML inicial. A conclusão sobre a implementação definitiva permanece pendente desses testes.

**Trade-off:** renderizar todos os textos não significa baixar todos os vídeos, imagens e animações ao mesmo tempo. Conteúdo textual e carregamento pesado de mídia podem ser separados.

<!--PAGE-->
# 11. Migração do pivot e domínio canônico

A referência aprovada é **https://www.taliya.com.br/**. Recomendo conservá-la como endereço principal e alinhar redirecionamentos, links, canonical, sitemap e metadados sociais. O plano não pede troca de domínio. [I01]

| Origem | Tratamento recomendado | Condição |
|---|---|---|
| / | Servir a nova home com 200 | Conteúdo horizontal e pré-lançamento verdadeiro |
| HTTP e host alternativo | Redirecionamento permanente para HTTPS/www | Evitar cadeia e loop |
| /pilates | Mapear para sucessor realmente equivalente | Se não houver equivalência, página de transição/histórico ou encerramento explícito |
| /pilates/planos | Destino específico para a oferta substituta, quando existir | Não encaminhar a checkout que ainda não existe |
| Âncoras antigas | Alias temporário no front-end | Preservar links compartilhados sem ressuscitar o produto antigo |
| URLs retiradas sem sucessor | 404/410 legítimo ou arquivo histórico fora da jornada | Não redirecionar tudo indiscriminadamente para a home |

A decisão final das URLs antigas deve considerar o inventário de páginas, links e tráfego da propriedade. Não medimos esses dados. Uma migração segura usa equivalência de conteúdo, não apenas semelhança de URL. Manter redirecionamentos de migração por período longo; o Google recomenda pelo menos um ano nos cenários de mudança de URL. [G06]

**Canonical não é redirecionamento.** Cada página nova útil deve indicar sua própria URL final, não a home. URLs com parâmetros de campanha podem declarar a versão limpa como canônica sem perder o parâmetro na captura de atribuição.

Não usar canonical para declarar uma página de planos obsoleta como se fosse idêntica à nova home. Não bloquear a antiga URL no robots antes de o mecanismo conseguir ler o redirecionamento ou `noindex` que se decidiu aplicar.

**Publicação coordenada:** home nova, links, rotas legadas, política revisada, sitemap e mensagens de WhatsApp comercial devem mudar na mesma entrega. Reprocessamento do buscador leva tempo; o site não pode continuar emitindo sinais contraditórios enquanto esperamos a atualização.

<!--PAGE-->
# 12. Robots, sitemap e páginas privadas

**Diagnóstico observado:** 404 nos caminhos padrão de robots e sitemap consultados. Para o Google, o primeiro não significa proibição de rastreio; o segundo não prova que não exista algum mapa alternativo. Mesmo assim, recomendo publicar ambos deliberadamente no pivot. [L04, G04, G05]

### Robots

Usar um arquivo pequeno, consistente com os conteúdos que devem ser públicos. Não bloquear CSS, JavaScript ou imagens necessários para compreender a landing. A política de rastreamento precisa ser revisada também na CDN, no firewall e nas regras antibot.

O exemplo incluído no pacote permite páginas públicas aos buscadores. Ele não deve ser copiado sem revisar as rotas reais de app/API, arquivos privados e a política de treinamento por IA. Regras específicas por agente podem substituir regras gerais; não presumir que tudo se soma.

### Sitemap

Incluir apenas URLs públicas, canônicas, indexáveis e com resposta 200. Excluir âncoras, busca interna, páginas de obrigado, parâmetros de campanha, staging, páginas retiradas e fluxos autenticados. Usar `lastmod` quando houver alteração relevante real, não atualizar diariamente por efeito cosmético.

Cada página precisa também de links internos normais. O sitemap não substitui a arquitetura de navegação. Submeter o endereço no Search Console e no Bing Webmaster Tools depois de validar o deploy. IndexNow pode notificar mudanças aos participantes que o suportam; não substitui o sitemap nem equivale a submeter diretamente ao Google ou ao ChatGPT. [B02]

### Privacidade e staging

Robots não é controle de acesso. Fichas de clientes, recebimentos, anexos e dados de conta exigem autenticação e autorização no servidor; não devem virar páginas públicas “protegidas” apenas por `Disallow`.

Para páginas públicas que não devem entrar no índice, usar a política apropriada de `noindex`, deixando o robô ler a instrução. Para staging, preferir proteção de acesso. Um bloqueio de rastreamento pode impedir a leitura do próprio `noindex`. [G04, G18]

A home pública de pré-lançamento pode ser indexável quando oferece informação útil e honesta. Não confundir pré-lançamento público com ambiente privado de desenvolvimento.

<!--PAGE-->
# 13. Google com IA e ChatGPT: configuração correta

São superfícies diferentes. A Taliya não precisa de uma “versão secreta para IA”, mas precisa permitir acesso e manter informação pública coerente.

| Agente ou controle | Papel | Ação para a Taliya |
|---|---|---|
| Googlebot | Rastreamento do Google Search | Não bloquear as páginas e recursos públicos relevantes |
| Search generative AI no Search Console | Inclusão em experiências de IA do Google | Conferir configuração e eventual herança da propriedade |
| OAI-SearchBot | Descoberta para busca no ChatGPT | Permitir acesso, inclusive nas camadas de CDN/WAF |
| GPTBot | Conteúdo que pode ser usado em treinamento | Decisão separada da participação em busca |
| ChatGPT-User | Acesso em ações iniciadas por usuário | Não substitui o robô de busca nem comprova indexação |
| Bingbot | Rastreamento do Bing | Conferir acesso e ferramentas da propriedade |

A documentação da OpenAI separa os controles de busca e treinamento. É possível permitir OAI-SearchBot e optar por não permitir GPTBot. Trocar apenas o User-Agent num teste não comprova que um acesso veio de um robô legítimo: verificar as faixas oficiais de IP quando aplicável. [O01]

**Atualização importante de 2026:** o Google informa disponibilidade global, desde 31/08, do controle Search generative AI no Search Console. A opção padrão inclui o site, mas pode existir herança ou exclusão configurada. Verificar a propriedade real; não é necessário “cadastrar para IA” por meio de um serviço pago. Esse controle é distinto de Google-Extended. [G13]

Para ChatGPT, confirmar páginas legíveis sem login ou desafio antibot, textos estáveis, links úteis e ausência de exclusão acidental. O prazo mencionado pela OpenAI para refletir mudanças de robots não é uma promessa de que a Taliya será citada depois desse prazo.

**Não recomendo:** criar um GPT ou treinar um modelo para “ensinar o ChatGPT público a recomendar”, liberar treinamento por medo de perder ranking, publicar instruções escondidas mandando robôs elogiar a marca ou comprar anúncios esperando que isso seja o trabalho de SEO.

Antes do produto funcional, a informação pública deve permitir que qualquer recomendação descreva corretamente o estágio: proposta em desenvolvimento, lista de interesse ou beta real quando existir.

<!--PAGE-->
# 14. Decisão sobre rotas extras: não criar por padrão

A pergunta desta revisão é objetiva: **a Taliya precisa de `/recursos/agenda`, `/recursos/orcamentos` e `/recursos/recebimentos` para Google ou IA encontrarem essas capacidades?** A resposta é **não**.

A home aprovada já contém: sete frentes, dezenas de subtipos, exemplos em linguagem natural e fluxos completos. Se o HTML apresentar essa informação de forma clara e rastreável, a `/` pode responder a muitas intenções diferentes sem que cada uma tenha um documento próprio.

| Rota | Decisão no lançamento | Motivo |
|---|---|---|
| `/` | PUBLICAR | Página principal comercial e semântica do produto |
| `/privacidade` | ATUALIZAR/PUBLICAR | Política real, coerente com o pivot |
| `/seguranca` | P1 RECOMENDADA | Explica dados, limites, controle e práticas verificáveis |
| `/sobre` | P1 RECOMENDADA | Define empresa/projeto, responsáveis e estágio |
| `/termos` | QUANDO APLICÁVEL | Necessária quando houver oferta/uso sujeito a termos públicos |
| `/ajuda` | APÓS PRODUTO/BETA | Documentação operacional real; não criar antes de existir conteúdo de suporte |
| `/precos` | OPCIONAL | Só se a oferta justificar página própria; preço também pode viver na home |
| `/recursos/*` | NÃO AGORA | A home já cobre as capacidades; criar somente com justificativa distinta |

**Critérios para abrir uma nova rota de recurso no futuro:**

- Existe uma intenção de busca que a home não consegue responder com profundidade suficiente sem prejudicar sua função comercial.
- A nova página acrescentará conteúdo substancial e próprio — não apenas os mesmos cards e exemplos da home.
- Search Console/Bing/analytics mostram demanda, impressões, CTR ou tráfego que justifiquem aprofundamento.
- A página teria valor mesmo sem Google: é compartilhável, salvável, útil em campanhas, creators, parceiros ou suporte.
- Há uma necessidade de URL citável para backlink, campanha, documentação ou comparação específica.

**Não usar “mais páginas” como KPI.** O Google orienta foco em conteúdo útil e alerta contra produção em escala apenas para cobrir variações de busca. As experiências de IA também não exigem uma página separada para cada pergunta. [G01, G11]

A arquitetura inicial, portanto, é deliberadamente pequena: **uma home forte + páginas de confiança/políticas quando necessárias**. A expansão editorial passa a ser consequência de dados e conteúdo novo.

<!--PAGE-->
# 15. Matriz de cobertura: por que a home já atende as intenções principais

Esta matriz confronta exemplos de busca com o conteúdo que já está previsto na Especificação Definitiva. O objetivo é verificar suficiência semântica antes de criar URLs adicionais.

| Intenção/pergunta | Conteúdo já previsto na `/` | O que precisa estar explícito no HTML |
|---|---|---|
| “Tem algum app que me ajude a controlar entrada e saldo de serviços?” | Frente Recebimentos; mural; fluxo entrada→saldo→lembrete | “Valor combinado”, “recebido”, “restante”, pagamento parcial/sinal e consulta posterior |
| “Como organizar minha agenda pelo WhatsApp?” | Demo; frente Agenda; fluxo de agenda | O profissional pede para marcar/consultar/remarcar/cancelar; não é autoagendamento do cliente |
| “App para fazer orçamento de serviço” | Frente Orçamentos; fluxo orçamento→aprovação→agenda | Criar, revisar, versionar, gerar documento e registrar aprovação, sem prometer nota fiscal |
| “Como controlar pacote de sessões?” | Serviços + Agenda + fluxo Pacote | Quantidade contratada, reservas/agendadas, realizadas e disponíveis sem virar módulo separado |
| “Lembrar de cobrar cliente” | Frente Lembretes; Recebimentos; mural | Lembrete ao dono, inclusive condicional; não contato automático com cliente |
| “Organizar arquivos por cliente/serviço” | Frente Arquivos/Docs; fluxo de recuperação | Arquivo ligado ao serviço, versão/correção e recuperação posterior |
| “App para organizar clientes e serviços” | Hero, definição, Clientes, Serviços, fluxos | Público-alvo, Cliente/Serviço, histórico/contexto e continuidade WhatsApp + app |
| “Como remarcar sem perder o histórico?” | Agenda + fluxo remarcação/cancelamento | Mesma ocorrência é atualizada; histórico é preservado; não duplica serviço |

A home não precisa repetir a mesma frase em dez lugares. Ela precisa fornecer **uma resposta inequívoca em pelo menos um bloco textual forte e exemplos coerentes em outros pontos**.

### Regra de implementação

- Títulos de seção e descrições essenciais devem existir em HTML sem depender de um clique que faça novo carregamento.
- Os estados de tabs podem continuar visualmente ocultos quando não selecionados, desde que o conteúdo essencial seja parte da renderização acessível/semântica e a implementação seja validada no HTML final.
- Exemplos complementam a explicação; não são a única forma de definir a feature.
- Cada frente deve incluir **o que faz, um caso concreto e o limite relevante**.
- Âncoras como `/#recebimentos` podem ser compartilhadas para apontar diretamente à seção, sem virar páginas independentes.

### Quando a matriz deixaria de ser suficiente

Se dados reais mostrarem que uma intenção importante exige explicação muito maior, ou se a home ficar excessivamente densa para responder sem prejudicar conversão, aí uma rota dedicada passa a ser uma solução editorial razoável. Essa decisão acontece **depois**, não como requisito técnico prévio.

<!--PAGE-->
# 16. Conteúdo original que merece ser encontrado

A Taliya tem matéria-prima melhor que artigos genéricos de “produtividade”: as dúvidas e exceções já mapeadas no próprio produto. **No lançamento, parte desse conteúdo deve fortalecer a home; guias independentes entram quando tiverem valor editorial próprio.**

| Pauta proposta | O que precisa acrescentar | Primeiro destino |
|---|---|---|
| Sinal, pagamento parcial e saldo: como não se perder | Exemplo conciliado, correção e limites do registro | Home → Recebimentos |
| Como registrar uma remarcação | Antes/depois, mudança só daquela ocorrência e histórico | Home → Agenda |
| Cancelou o horário: o que acontece com o serviço? | Diferenciar agenda, contratação e acerto financeiro | Home → Agenda/Serviços |
| Orçamento revisado não é acordo aprovado | Duas versões, registro da decisão e continuidade | Home → Orçamentos |
| Pacote de oito sessões versus plano mensal | Quantidade total, ciclo e frequência independentes | Home → Serviços/Agenda |
| Como começar a organizar sem cadastrar o passado inteiro | Entrada por uma necessidade e enriquecimento progressivo | Home → Como funciona |
| Arquivo enviado não é pagamento confirmado | Exemplo de comprovante, contexto e confirmação do dono | Home → Arquivos/Recebimentos |
| Como usar só a agenda sem adotar tudo | Rotina mínima e o que a ferramenta não poderá concluir | Home → Agenda/Como funciona |

Uma pauta só deve virar uma nova URL quando trouxer uma resposta extensa e independente — por exemplo um guia realmente educativo sobre orçamento profissional, remarcações ou controle de sinal/saldo. **Não criar um artigo apenas para repetir a descrição da feature.**

Depois do beta, priorizar casos com autorização: situação inicial, método anterior, uso escolhido, período observado, resultado e o que continuou fora da Taliya. Não transformar dois depoimentos em estatística representativa de mercado.

**Controle de qualidade:** autoria/responsável identificável; exemplos com números corretos; revisão por quem conhece o produto; atualização quando a função mudar; link para a seção/capacidade correspondente. Não colocar data nova sem revisão real.

O Google orienta conteúdo original, útil e baseado em experiência, e alerta contra páginas feitas em massa apenas para cobrir variações de buscas. Não existe benefício automático em multiplicar páginas. [G01, G11]

Cadência inicial recomendada: publicar primeiro a home correta, medir o que aparece e só depois produzir poucas peças completas, revisadas e justificadas por intenção real.

<!--PAGE-->
# 17. Dados estruturados sem promessas falsas

Dados estruturados ajudam a descrever entidades e algumas experiências de busca. Não substituem conteúdo, não criam reputação e não são uma “senha” para respostas de IA.

| Tipo | Uso recomendado | Cuidados |
|---|---|---|
| Organization | Identificar Taliya, site, logo e contatos reais | `sameAs` apenas para perfis oficiais verificados |
| WebSite | Nome do site e URL principal | Nome da marca, não sequência de palavras-chave |
| WebPage | Descrever cada página pública real e sua relação com o site | URL canônica específica de cada documento existente |
| BreadcrumbList | Navegação de páginas profundas quando elas existirem | Não usar na home como se houvesse hierarquia artificial |
| SoftwareApplication | Descrição do produto, quando pertinente | Requisitos de resultado enriquecido são separados da validade semântica |
| Article | Guias editoriais próprios | Autor e datas correspondem ao conteúdo |
| VideoObject | Vídeo próprio elegível com dados reais | Não marcar mockup estático como vídeo publicado |

A marcação de aplicativo não autoriza inventar preço zero, disponibilidade, avaliações ou nota média. Para o resultado enriquecido de software, o Google exige propriedades específicas, incluindo informações de oferta e avaliação/review; só declarar dados reais que satisfaçam as regras. [G08–G10]

**FAQ em 2026:** a documentação do Google informa que os resultados enriquecidos de FAQ deixaram de ser exibidos a partir de 07/05/2026. Manter as perguntas porque ajudam o visitante e a compreensão, não para prometer um rich result que foi retirado. [G12]

No pré-lançamento, o exemplo do pacote usa Organization + WebSite + WebPage, sem ratings nem ofertas compráveis. A ausência desses campos é intencional. Incluir o produto como SoftwareApplication pode ser avaliado, mas não é requisito para a primeira publicação.

Validar sintaxe de JSON, URLs e aderência ao conteúdo. O Rich Results Test identifica funcionalidades suportadas; um schema válido pode não ser elegível para um resultado especial. Conferir também erros no Search Console depois da indexação.

Não atribuir à Taliya selos regulatórios, afiliação ao WhatsApp ou certificações apenas por usar APIs oficiais de terceiros.

<!--PAGE-->
# 18. Performance, mobile e acessibilidade

**Não temos nota de performance da Taliya nesta auditoria.** Nenhum número de Lighthouse, PageSpeed ou Core Web Vitals foi obtido. A recomendação abaixo é um plano de verificação, não diagnóstico de lentidão já comprovada.

Referências de boa experiência em dados de campo, no percentil 75: **LCP até 2,5 segundos, INP até 200 ms e CLS até 0,1**. Avaliar mobile e desktop. Laboratório ajuda a diagnosticar; não é a mesma coisa que experiência real acumulada. [G15]

| Risco possível na landing rica | Verificação proposta |
|---|---|
| Hero com mídia pesada | Identificar elemento de LCP; otimizar arquivo, dimensões e carregamento |
| Muitas conversas e animações | Medir JavaScript, uso de CPU e resposta ao toque |
| Carrosséis com dezenas de imagens | Carregar mídia sob demanda sem omitir o texto essencial |
| Chat flutuante e tags externas | Medir custo de terceiros e impacto na interação |
| Fontes e imagens sem espaço reservado | Verificar deslocamentos de layout |
| Mural com movimento contínuo | Respeitar redução de movimento e oferecer pausa |
| Tabs e modais | Testar teclado, foco, nomes acessíveis e retorno ao gatilho |

Executar mobile real em iPhone/Android e uma viewport de 390 × 844. Conferir zoom, leitura dos balões, controles acionáveis, CTA flutuante que não cobre conteúdo e texto dos resultados. Não esconder informação importante apenas na versão mobile.

Fazer medições reproduzíveis antes/depois das alterações, anotando data, URL, ambiente e condições. Se o CrUX ainda não tiver dados suficientes, registrar essa falta sem transformar a ausência em nota zero ou aprovação.

Acessibilidade beneficia usuários e agentes que navegam pela interface, mas não é um certificado automático de ranking. Labels, elementos HTML apropriados e estados expostos são melhores que botões compostos apenas por ícones sem nome. [O02]

**Prioridade:** a primeira demonstração deve carregar e responder bem; as outras podem ser progressivas. Não precisamos remover carrosséis, mas evitar que todos os recursos pesados concorram antes do visitante ler o hero.

<!--PAGE-->
# 19. Marca, confiança e presença fora do site

A pergunta estratégica é: **quem além da própria Taliya pode explicar, com conhecimento real, para que ela serve?** Nenhuma quantidade de markup substitui uma razão verdadeira para confiar no produto.

### Base controlada pela marca

Publicar responsáveis pelo projeto, contato de suporte verificável, descrição da empresa e estágio. Em segurança, explicar quais dados são recebidos, o que não é acessado automaticamente, como corrigir e como solicitar exclusão/exportação. Não apresentar a política comercial antiga como descrição completa do futuro produto.

Atualizar as bios e links dos perfis oficiais efetivamente controlados. A descrição precisa distinguir a Taliya nova do produto de studios. Não inserir perfis de nome parecido em `sameAs` nem inventar presença corporativa para preencher schema.

### Distribuição que cria evidência

Procurar comunidades e parceiros de profissionais para testar casos reais, publicar demonstrações autorizadas e participar de perguntas com transparência de vínculo. Uma associação que realmente oferece ou avalia o produto pode produzir uma página contextual; o exemplo do sindicato encontrado para Meu Assessor ilustra esse canal, não garante o mesmo resultado para a Taliya. [L11]

Creators podem demonstrar uma rotina real e levar diretamente à seção correspondente da home; uma rota própria só entra quando houver conteúdo realmente mais profundo. Produzir uma versão textual da demonstração no site e vídeo acessível é útil para quem precisa entender o caso sem depender de Instagram. Posts e seguidores não são comprovação de ranking.

**Não fazer:** comprar pacotes de backlinks, fabricar avaliações, inserir propaganda disfarçada em fóruns, contratar publicações “independentes” sem transparência ou criar páginas parasitas para emprestar reputação. As políticas do Google abrangem manipulação de links e conteúdo em escala. [G11]

### SEO local não é o objetivo principal

A Taliya é um software para profissionais de várias localidades, não uma clínica de Pilates ou prestador presencial em cada cidade. Negócios exclusivamente online não se enquadram por si só no Perfil da Empresa do Google. Não criar endereços fictícios, perfis locais ou dezenas de páginas “Taliya em [cidade]”. [G16]

<!--PAGE-->
# 20. Como aumentar a chance de uma citação correta

Recomendo tornar a Taliya uma fonte pública fácil de conferir, não escrever “para agradar um modelo”. A home — e qualquer página pública adicional que venha a existir — deve responder o que é, para quem serve, como funciona, o que fica registrado e o que não faz.

### Informações que precisam ser consistentes

**Categoria:** organização administrativa de serviços. **Usuário:** profissional operando a própria rotina. **Canal:** conversa com o número da Taliya e app sobre a mesma base. **Limites:** sem afirmar leitura de outros chats, cobrança bancária, emissão fiscal ou autoagendamento fora do escopo. **Estágio:** pré-lançamento agora; disponibilidade real depois.

Use exemplos em texto acompanhando imagens, uma matriz clara de capacidades e condições, ajuda pública e data de revisão pertinente. Esses são critérios editoriais propostos para reduzir interpretações erradas, não um número ideal de palavras ou um formato exigido por IA.

Para consultas comparativas, uma página deve reconhecer quando a Taliya não é a opção adequada. Alguém que precisa de equipe com agendas independentes, emissão fiscal ou atendimento automático pode necessitar de outra solução. Uma recomendação incorreta traz leads que o produto não consegue atender.

**Não recomendo uma página “Por que o ChatGPT deve recomendar Taliya”.** Recomendo páginas que permitam a uma pessoa verificar se ela serve para o caso concreto. Também não precisamos publicar instruções em texto escondido, alterar o conteúdo conforme o visitante seja robô ou inventar citações de especialistas.

A orientação oficial do Google dispensa arquivos especiais, escrita artificial para IA e fragmentação de conteúdo em pedacinhos. A OpenAI orienta acesso para busca e conteúdo público; não oferece uma regra para comprar ou garantir recomendações. [G01, O02, O03]

O melhor ativo futuro será uma demonstração do produto real acompanhada de um caso verificável: o que o usuário fazia antes, como passou a fazer, o que mudou e o que continuou fora. Até lá, não transformar exemplos fictícios em prova de resultado.

<!--PAGE-->
# 21. Pré-lançamento versus lançamento

| Tema | Agora: pré-lançamento | Depois: produto disponível |
|---|---|---|
| Home | Explica a proposta e identifica estágio | Explica o funcionamento efetivamente disponível |
| Demos | Experiência planejada rotulada | Capturas reais ou ilustrações fiéis identificadas |
| CTA | Cadastro de interesse ou convite real para beta | Onboarding/teste/assinatura que funcionam |
| Preço | Oculto se oferta ainda não aprovada | Valores, periodicidade, limites e cancelamento coerentes |
| Conteúdo educativo | Pode ensinar processos e exemplos | Acrescenta passos e telas do produto real |
| Dados estruturados | Sem avaliações e ofertas compráveis fictícias | Oferta e aplicação conforme dados públicos reais |
| Medição | Visita qualificada e lead verdadeiro | Ativação, recorrência e receita, além dos leads |

A especificação já prevê essa separação e deve ser preservada. Assistir a um exemplo não é `first_operation`; preencher uma waitlist não é cliente pagante; criar um cadastro de interesse não inicia um trial automaticamente. [I01]

**Indexação no pré-lançamento:** não há motivo para esconder uma página pública útil só porque o produto está em desenvolvimento. A condição é que ela seja verdadeira e não induza o visitante a acreditar numa disponibilidade inexistente. O staging privado é outro ambiente.

**Cuidado com reputação duradoura:** uma página publicada hoje pode ser encontrada e citada depois. Evitar números temporários, promessas de data sem compromisso real e descrição de recursos futuros como já disponíveis. Ao lançar, revisar conteúdo, metadados, schema, CTAs e referências externas controladas.

Os textos de preço existentes na galeria e na especificação são planejamento comercial. Não foram auditados checkout, contrato final nem limites operacionais nesta rodada; por isso o pacote não habilita uma oferta automaticamente.

**Decisão prática:** publicar o pivot bem descrito antes de produzir um catálogo enorme de páginas; depois expandir o conteúdo com o mesmo modelo de dados e um calendário de revisões. SEO não deve atrasar todo o produto, nem servir de desculpa para publicar uma promessa que ele ainda não cumpre.

<!--PAGE-->
# 22. Medição: Google, Bing, ChatGPT e negócio

| Superfície | O que observar | O que não concluir |
|---|---|---|
| Search Console tradicional | Indexação, canonical escolhido, consultas, impressões, cliques e páginas | Um relatório vazio não prova penalidade |
| Search Console — IA generativa | Impressões, páginas, país e dispositivo nas experiências suportadas | Não é relatório de ChatGPT nem de receita |
| Bing Webmaster — AI Performance | Citações e páginas usadas em superfícies contempladas | Não mede toda resposta de todos os assistentes |
| Analytics da Taliya | Entradas, origem, páginas e lead real | Visita não equivale a menção ou recomendação |
| Logs/CDN | Robôs verificados, erros, desafios e padrões de acesso | Rastreio não comprova indexação |
| Produto funcional | Primeira operação, continuidade e assinatura | Não disparar esses eventos em demos da landing |

**Google:** o anúncio oficial foi atualizado em 31/08/2026 informando expansão global dos relatórios de IA generativa. A documentação descreve impressões e dimensões próprias; dados insuficientes podem explicar a ausência de relatório. Não tratar essa visão como tráfego extra a somar novamente aos totais já abrangidos. [G14]

**Bing:** AI Performance foi anunciado em prévia pública em fevereiro de 2026 para citações em experiências contempladas. Verificar o que está disponível na conta e não interpretar a ferramenta como ranking universal do ChatGPT. [B01]

**ChatGPT:** a OpenAI informa o uso de `utm_source=chatgpt.com` em URLs de referência. Preservar esse parâmetro na atribuição e registrar também referrer quando disponível. Isso mede visitas identificáveis, não todas as citações sem clique nem recomendações. [O02]

**Dashboard recomendado:** marca versus não marca; por grupo de intenção e página; leads qualificados no pré-lançamento; ativação e receita somente depois. Não somar impressões de Google, citações do Bing e sessões do analytics como se fossem a mesma métrica.

Nenhuma propriedade privada foi acessada nesta auditoria. A instalação prévia dessas ferramentas não foi confirmada nem negada. A primeira implementação deve verificar acesso, medição e consentimentos necessários.

<!--PAGE-->
# 23. Protocolo para acompanhar respostas de IA

Uma conversa que já conhece todo o projeto, como esta, **não mede recomendação espontânea**. Acompanhamento deve usar consultas neutras e registrar as condições do teste.

| Grupo | Exemplo de consulta de teste |
|---|---|
| Marca | O que é a Taliya e para quem ela serve? |
| Disponibilidade | A Taliya já está disponível para usar? |
| Categoria | Que ferramentas ajudam autônomos a organizar clientes, agenda e recebimentos? |
| Agenda | Quero registrar e remarcar meus atendimentos pelo WhatsApp. Que opções existem? |
| Limite de canal | Preciso conectar meu WhatsApp comercial para usar a Taliya? |
| Orçamento | Como organizar versões de orçamento e o serviço aprovado? |
| Recebimentos | Como acompanhar sinal e saldo restante dos meus serviços? |
| Uso parcial | Existe uma ferramenta que eu possa começar usando só para minha agenda? |
| Pacotes | Como controlar aulas contratadas, agendadas e realizadas? |
| Busca de arquivos | Como manter fotos e PDFs ligados ao trabalho de cada cliente? |
| Exclusão de encaixe | Preciso de emissão fiscal e cobrança automática. A Taliya atende? |
| Confiança | Quais informações a Taliya recebe e como o usuário corrige um registro? |

Executar uma rodada de base e depois uma rotina compatível com o ritmo de publicação, por exemplo mensal no início. Registrar data, produto/modelo exibido, idioma, região informada, uso de busca, pergunta exata e resposta completa. Preferir sessões novas sem histórico do projeto; isso reduz contaminação, mas não transforma o teste em experimento universal.

Classificar: não mencionou; mencionou; citou domínio; recomendou; descreveu corretamente; confundiu produto/estágio; atribuiu função inexistente. Guardar URLs citadas e a passagem que fundamenta a conclusão.

Repetir variações relevantes sem transformar dezenas de respostas em porcentagem de mercado. O conjunto mede uma amostra definida, não “a visibilidade total da marca na IA”.

**Correção prioritária:** se uma resposta ainda descreve Pilates, cobrança automática ou disponibilidade inexistente, investigar as fontes que a sustentam e corrigir conteúdo controlado. Não responder com mais slogans ou pedir que o modelo “memorize” a versão desejada.

<!--PAGE-->
# 24. Plano 0–30 / 31–60 / 61–90 dias

O calendário é uma proposta de execução após a decisão de publicar o pivot; não prevê quando o Google dará uma posição. **Rotas de recurso foram removidas do cronograma inicial.**

| Período | Entregas | Critério de conclusão |
|---|---|---|
| 0–7 dias | Mapear código/rotas; capturar baseline; verificar ferramentas e permissões | Lista de URLs e evidências; nenhum dado privado exposto |
| 8–15 dias | Aplicar home horizontal, metadados, robots/sitemap, legado e conteúdo das abas/frentes | Testes P0 aprovados no ambiente publicado |
| 16–30 dias | Publicar/revisar Sobre, Segurança e políticas necessárias; validar Search Console/Bing/analytics | Presença pública coerente e mensurável, sem páginas de feature artificiais |
| 31–60 dias | Observar queries/impressões; corrigir indexação; produzir 1–3 conteúdos aprofundados somente se houver intenção real | Decisão editorial baseada em dados e conteúdo próprio |
| 61–90 dias | Acrescentar evidências de uso se existirem; parcerias reais; criar rota dedicada apenas para clusters justificados | Melhor qualidade de resposta e aquisição, não apenas volume de URLs |

**Responsabilidades:** desenvolvimento cuida de HTML, rotas e testes; produto valida as capacidades; conteúdo transforma casos em explicações; responsável comercial confirma oferta; privacidade revisa coleta e políticas; analytics verifica eventos e atribuição. Uma mesma pessoa pode assumir mais de um papel, mas o aceite precisa ter dono.

**Não esperar para o dia da publicação:** inventário do legado, escolha do domínio, revisão de exemplos, política de indexação de staging, estrutura semântica das sete frentes e medição de interesse.

**Não antecipar indevidamente:** rotas de recursos repetitivas, depoimentos inexistentes, preço no schema sem oferta real, tutorial com telas não implementadas como se fosse produto pronto ou estudo de economia de tempo feito apenas com simulação.

**Primeiro ciclo de revisão:** verificar se a busca de marca deixou de reproduzir informação antiga, se a home canônica é reconhecida e quais consultas começam a gerar impressões. Só depois decidir se Agenda, Orçamentos, Recebimentos ou outro cluster merecem página própria.

<!--PAGE-->
# 25. Backlog prioritário para a implementação

| ID | Prioridade | Entrega e evidência de conclusão |
|---|---|---|
| SEO-01 | P0 | Raiz serve a nova home; cadeia de redirects salva |
| SEO-02 | P0 | Title/description/H1/OG/Twitter representam o pivot |
| SEO-03 | P0 | Canonical consistente no HTML/DOM, próprio de cada página real |
| SEO-04 | P0 | robots e sitemap válidos nos hosts/URLs finais |
| SEO-05 | P0 | As sete frentes e intenções centrais têm texto explícito e legível sem clique obrigatório |
| SEO-06 | P0 | Tratamento aprovado de /pilates e /pilates/planos |
| SEO-07 | P0 | Acesso dos robôs de busca não bloqueado por regras indevidas |
| SEO-08 | P0 | Pré-lançamento preservado em copy, CTA, schema e eventos |
| SEO-09 | P0 | Formulário real testado; dados privados não indexáveis |
| SEO-10 | P1 | Matriz intenção→seção da home conferida no HTML final e nas âncoras |
| SEO-11 | P1 | Sobre/Segurança/Privacidade/Termos atuais conforme aplicabilidade |
| SEO-12 | P1 | Organization/WebSite/WebPage validados, sem avaliações inventadas |
| SEO-13 | P1 | Diagnóstico mobile, laboratório e campo documentado |
| SEO-14 | P1 | Search Console/Bing/analytics verificados; baseline salvo |
| SEO-15 | P1 | Primeiras análises de queries determinam se existe lacuna real de conteúdo |
| SEO-16 | P2 | Guias/rotas adicionais somente com intenção distinta e conteúdo próprio |
| SEO-17 | P2 | Casos e referências de terceiros após experiência real |
| SEO-18 | P2 | Testes de respostas de IA e expansão editorial orientados por dados |

P0 protege a correção da publicação. P1 torna a home observável e confiável. P2 acrescenta profundidade onde os dados justificarem. **Nenhuma rota `/recursos/*` é requisito de lançamento nesta versão.**

**Fora do backlog prioritário:** llms.txt, páginas de feature apenas para “ter URL”, centenas de páginas verticais, selo fictício de IA, compra de links e busca de estrelas sem avaliações autênticas.

Não foram alterados repositório, DNS, Search Console, robots, sitemap, perfis ou página pública. Este documento define o que deve ser implementado e comprovado.

# 26. Checklist de aceite e evidências

Cada aceite deve guardar URL, data, resultado e responsável. “Está no código” não equivale a “foi publicado corretamente”.

| Teste | Condição para aprovação |
|---|---|
| QA-01 | Home final responde 200 e não leva à antiga oferta de Pilates |
| QA-02 | HTTP/apex/www não criam loops ou múltiplos destinos concorrentes |
| QA-03 | Cada URL pública relevante tem canonical final consistente |
| QA-04 | Nenhuma página de aquisição recebe noindex acidental |
| QA-05 | robots não bloqueia recursos públicos necessários |
| QA-06 | Sitemap contém apenas páginas canônicas, públicas e existentes |
| QA-07 | Legado tem redirecionamento equivalente ou encerramento deliberado |
| QA-08 | Headline, metadados, formulário e oferta concordam sobre o estágio |
| QA-09 | H1 principal e hierarquia de headings são conferidos em tags reais |
| QA-10 | Sete frentes, subtipos essenciais e perguntas aparecem no HTML renderizado sem novo carregamento após clique |
| QA-11 | JSON em script não é a única representação textual do conteúdo |
| QA-12 | Âncoras internas e páginas institucionais usam href real; não existem rotas de recurso vazias |
| QA-13 | Imagens informativas têm texto alternativo útil; decorativas são tratadas como tais |
| QA-14 | Layout reserva espaço e não cobre texto/CTA no mobile |
| QA-15 | Tabs, mural e modais funcionam por teclado e respeitam redução de movimento |
| QA-16 | Schema corresponde ao conteúdo visível e não inventa oferta/rating |
| QA-17 | Search Console confirma acesso/inspeção; controle de IA é conferido |
| QA-18 | Bing Webmaster recebe sitemap e permite inspeção da propriedade |
| QA-19 | CDN/logs permitem verificar acessos legítimos de robôs |
| QA-20 | Analytics preserva origem de busca/ChatGPT sem enviar dados pessoais |
| QA-21 | Demos não disparam lead, compra ou operação real |
| QA-22 | Formulário registra sucesso apenas depois da gravação efetiva |
| QA-23 | Baseline de busca separa marca, intenção e páginas |
| QA-24 | Teste final de conteúdo não atribui funções fora da V1 |
| QA-25 | Revisão da matriz de intenções confirma que a `/` responde Agenda, Orçamentos e Recebimentos sem depender de URL extra |

**Aceites pendentes nesta auditoria:** inspeção privada, headers brutos, HTML entregue pelo servidor, mobile real, performance e tráfego. Eles foram incluídos como testes, não preenchidos com resultados inventados.

<!--PAGE-->
# 27. Handoff técnico e mudanças na especificação

O pacote técnico acompanha este relatório com exemplos editáveis. Ele é um adendo à landing v1, não uma implementação do site nem uma substituição da Product Bible.

| Artefato | Uso | Cuidado |
|---|---|---|
| seo_config.example.json | Title, descrições, domínio e estágio | Não sobrescrever oferta/contatos reais |
| robots.public.example.txt | Ponto de partida para conteúdo público | Revisar rotas privadas e política de agentes |
| structured_data.prelaunch.json | Exemplo mínimo de entidades públicas | Não contém avaliações, preço ou aplicativo disponível |
| route_plan.json | Arquitetura mínima + critérios para expansão futura | Não criar `/recursos/*` antes de cumprir os critérios |
| seo_acceptance.md | Testes e evidências da publicação | Marcar resultado real, não só intenção |
| evidence_summary.json | Fatos observados e incertezas | Não chamar inferências de medições |
| fontes.md | Referências consultadas | Revalidar documentos dinâmicos antes de futuras mudanças |

### Alterações na especificação aprovada

**B2 / metadados:** substituir o title centrado apenas no slogan por uma descrição de categoria; preservar o slogan no H1. Manter canonical www raiz, separação prelaunch/launch e imagem social original.

**QA38 / SEO:** desdobrar o aceite genérico em URL, status, canonical, robots, sitemap, HTML de conteúdo, schema e inspeção. O checklist desta auditoria fornece essa expansão.

**Componentes interativos:** manter a UI e acrescentar contrato de legibilidade para os textos essenciais, âncoras reais, foco e redução de movimento. Não transformar toda subtab em uma página rasa.

**Arquitetura pública revisada:** a home concentra as capacidades e intenções de produto. Sobre/Segurança/Privacidade/Termos cumprem papéis institucionais quando aplicáveis. Rotas de recurso e guias **não fazem parte do lançamento obrigatório**; entram somente por intenção distinta, conteúdo novo, dados de busca ou necessidade de distribuição.

**Medição:** preservar os eventos já definidos, acrescentando origem orgânica/IA e relatórios de plataforma, sem confundir métricas.

**Conclusão:** o melhor investimento não é fazer o site “parecer otimizado para IA” nem multiplicar URLs. É tornar a `/` da Taliya uma fonte acessível, específica, atual e confiável sobre um produto que resolve uma rotina real — e expandir somente quando a evidência mostrar que outra página acrescenta valor.

<!--PAGE-->
# Fontes e rastreabilidade — 1/4

Consulta pública e revisão documental em **19/09/2026**. As referências sustentam os fatos; o plano aplicado à Taliya é recomendação desta auditoria.

### [I01] Documento aprovado da Taliya
Arquivo fornecido nesta conversa; especialmente pp. 51–53 e 57. Não representa código publicado.

Taliya_Landing_Especificacao_Definitiva_v1_2026-09-18.pdf

### [L01] Taliya — página pública e redirecionamento da raiz
Leitura externa termina em /pilates; produto antigo e navegação pública.

https://www.taliya.com.br/

### [L02] Taliya — landing legada e metadados
Title, descrição, OG e Twitter recuperados. Canonical/contagem de headings requerem confirmação técnica.

https://www.taliya.com.br/pilates

### [L03] Taliya — planos legados
Oferta pública ainda referente a studios; não é a oferta do copiloto.

https://www.taliya.com.br/pilates/planos

### [L04] Arquivos técnicos e navegador de auditoria
Também testados /sitemap.xml e /llms.txt: 404 retornado pelo fetch externo. Run de navegador: 36fea777-bcc4-4eb8-875f-279fdbe8dfc1.

https://www.taliya.com.br/robots.txt

### [L05] Busca de marca — amostra pública
Consulta Taliya + WhatsApp, Brasil/português: resultado com título de Pilates. Provedor de pesquisa, não medição fixa do Google.

https://www.taliya.com.br/

### [L06] Meu Assessor — capacidades públicas
Benchmark de uma página explicativa além da home; alegações são do fornecedor.

https://www.meuassessor.com/funcionalidades

### [L07] Cotte — página pública
Exemplo de linguagem ligada a orçamentos via WhatsApp; produto não testado.

https://cotte.app/

### [L08] Interaup — página pública
Exemplo de página focada em orçamento/PDF; produto não testado.

https://interaup.com/


<!--PAGE-->
# Fontes e rastreabilidade — 2/4

Consulta pública e revisão documental em **19/09/2026**. As referências sustentam os fatos; o plano aplicado à Taliya é recomendação desta auditoria.

### [L09] Tramppo — página pública
Exemplo de categoria software para prestadores; produto não testado.

https://tramppo.app/

### [L10] AgendaBot — página pública
Exemplo de intenção de automação de atendimento/agendamento; produto não testado.

https://agendabot.app/

### [L11] Sindinutri-SP — benefício Meu Assessor
Exemplo de referência externa por entidade profissional; não valida performance do produto.

https://www.sindinutrisp.org.br/beneficios/varejo-e-servicos/aplicativo-meu-assessor

### [L12] Taliya — política pública
Texto recuperado com atualização de 27/05/2026 e escopo comercial/legado.

https://www.taliya.com.br/privacidade

### [G01] Google — guia de otimização para IA na busca
SEO e IA, conteúdo original, elegibilidade e limites de supostos atalhos.

https://developers.google.com/search/docs/fundamentals/ai-optimization-guide

### [G02] Google — lazy loading
Conteúdo essencial não deve depender de cliques; inspeção da renderização.

https://developers.google.com/search/docs/crawling-indexing/javascript/lazy-loading

### [G03] Google — JavaScript SEO
Renderização, links e conteúdo em JavaScript.

https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics

### [G04] Google — interpretação de robots.txt
Tratamento de 4xx, escopo de arquivo e regras de rastreamento.

https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec

### [G05] Google — sitemaps
Função de descoberta; sitemap não garante indexação.

https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview


<!--PAGE-->
# Fontes e rastreabilidade — 3/4

Consulta pública e revisão documental em **19/09/2026**. As referências sustentam os fatos; o plano aplicado à Taliya é recomendação desta auditoria.

### [G06] Google — migrações de URLs
Mapeamento de URLs e redirecionamentos de migração.

https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes

### [G07] Google — títulos dos resultados
Titles descritivos, fontes usadas e reprocessamento.

https://developers.google.com/search/docs/appearance/title-link

### [G08] Google — Organization
Identificação da organização e propriedades pertinentes.

https://developers.google.com/search/docs/appearance/structured-data/organization

### [G09] Google — SoftwareApplication
Propriedades exigidas para resultados enriquecidos de aplicativos.

https://developers.google.com/search/docs/appearance/structured-data/software-app

### [G10] Google — nomes de sites
Marca e WebSite na home.

https://developers.google.com/search/docs/appearance/site-names

### [G11] Google — políticas de spam
Conteúdo em escala, doorway pages, links e práticas manipulativas.

https://developers.google.com/search/docs/essentials/spam-policies

### [G12] Google — atualizações da documentação
Retirada de FAQ rich results em 07/05/2026; orientação atual sobre llms.txt e JavaScript.

https://developers.google.com/search/updates

### [G13] Google — Search generative AI control
Controle em Settings; disponibilidade global anunciada em 31/08/2026; verificar herança.

https://support.google.com/webmasters/answer/16908024

### [G14] Google — relatório de IA generativa
Impressões e dimensões do relatório de Search; disponibilidade e volume suficiente.

https://support.google.com/webmasters/answer/16984139


<!--PAGE-->
# Fontes e rastreabilidade — 4/4

Consulta pública e revisão documental em **19/09/2026**. As referências sustentam os fatos; o plano aplicado à Taliya é recomendação desta auditoria.

### [G15] web.dev — Web Vitals
Métricas de campo e limites de referência, percentil 75.

https://web.dev/articles/vitals

### [G16] Google — qualificação do Perfil da Empresa
Limites para empresas exclusivamente online.

https://support.google.com/business/answer/13763036?hl=pt-BR

### [G18] Google — impedir indexação
Noindex precisa ser acessível para leitura; não é autenticação.

https://developers.google.com/search/docs/crawling-indexing/block-indexing

### [O01] OpenAI — crawlers
OAI-SearchBot, GPTBot e ChatGPT-User; controles distintos e faixas oficiais de IP.

https://developers.openai.com/api/docs/bots

### [O02] OpenAI — Publishers and Developers FAQ
Visibilidade em busca, acesso e identificação de referências com utm_source.

https://help.openai.com/en/articles/12627856-publishers-and-developers-faq

### [O03] OpenAI — ChatGPT Search
Informações para editores e ausência de garantia de posicionamento.

https://help.openai.com/en/articles/9237897-chatgpt-search

### [B01] Bing — AI Performance
Prévia pública anunciada em fevereiro de 2026; citações, páginas e limites das métricas.

https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview

### [B02] Bing — diretrizes de webmaster
Rastreamento, sitemap e atualização de URLs; IndexNow não é garantia de ranking.

https://www.bing.com/webmasters/help/bing-webmaster-guidelines-30fba23a
