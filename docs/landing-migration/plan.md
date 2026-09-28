# Plano concreto — migração Taliya/Copiloto

## Objetivo

Preparar uma cópia independente do repositório original e migrar a landing para Taliya/Copiloto mantendo a mesma base React/Next.js, os componentes visuais e as interações existentes. A mudança de conteúdo será textual. O adendo de SEO/descoberta no ChatGPT e a inclusão do Mural são os únicos incrementos de produto autorizados. A análise de arquitetura e reuso acontece por último, depois da integração.

## Fontes e autoridade

1. O pedido mais recente do usuário fixa o escopo: textos, SEO/ChatGPT, Mural, integração e arquitetura/reuso.
2. O repositório `lucasquintino/agentes-landing-system`, no commit `c473a440d562acf6d5314cce0701d48ec284fc07`, é a base técnica e visual.
3. `landing.content.pt-BR.json` é a fonte dos textos e dos nomes/conteúdos do produto Copiloto.
4. O pacote SEO v1.1 governa metadados, indexação, conteúdo legível por busca, estrutura pública e descoberta pelo ChatGPT. Exemplos marcados como propostos não são fatos de produção.
5. As instruções de implementação do ZIP só se aplicam onde não conflitam com o limite textual explicitado pelo usuário. Uma spec não amplia esse limite.

## Limites invariáveis

- Não alterar o repositório original; todo trabalho fica nesta cópia local.
- Não redesenhar, reconstruir, reorganizar a página por simetria, trocar stack/dependências ou reescrever componentes durante as specs de seção.
- Em S01–S14, mudar apenas conteúdo textual visível e nomes/textos acessíveis já existentes. Preservar árvore de componentes, ordem, CSS, tokens, espaçamentos, estados, handlers, comportamento de CTA e navegação.
- Exceções autorizadas: ajustes técnicos de SEO; inserir o Mural S06 usando primeiro os mockups/balões existentes; e refatorações pontuais na spec 018 depois de S017, sem mudar aparência ou comportamento.
- Não criar faixa S02, fluxos substitutos da calculadora, novos formulários, rotas de recurso ou novos controles durante as specs de conteúdo. Se a copy canônica não couber em um slot sem essas mudanças, registrar o conflito para a spec da seção; não improvisar uma UI.
- Manter `/pilates` e `/pilates/planos` como estão na cópia enquanto a decisão de legado permanecer pendente. A nova home `/` é tratada na spec SEO, sem redirecionar o legado por suposição.
- Não implementar o aplicativo, back-end, endpoints, checkout, integrações, preço, prova social, ofertas ou captura simulada. Não publicar, fazer push/deploy ou alterar DNS/serviços.

## Sequência de trabalho

Cada etapa é concluída antes da seguinte: especificação → análise da fonte e do código → plano/tarefas → implementação estritamente delimitada → verificação e evidências. Checks não executados ficam como pendentes.

| Etapa | Recorte | Trabalho autorizado |
|---|---|---|
| 001 | Fundação | Cópia limpa, proveniência, baseline, Constitution, contratos, mapa de código e índice SDD. Nenhuma mudança na aplicação. |
| 002 | SEO transversal | Home pública, metadados, semântica, canonical configurável, Open Graph, schema verídico, sitemap/robots e critérios de descoberta pelo ChatGPT. Sem páginas de feature. |
| 003 | S01 — Header/hero | Atualizar os textos existentes e rótulos acessíveis; conservar composição, interações e destinos. |
| 004 | S02 — Confiança/controle | Atualizar somente texto que já tenha slot existente. Não inserir a faixa de confiança prevista no pacote enquanto a regra textual prevalecer. |
| 005 | S03 — Na prática | Atualizar textos e exemplos dos itens existentes; conservar seletor e transições. |
| 006 | S04 — Sem/Com Taliya | Atualizar textos dos comparativos existentes; conservar toggle/carrossel e estado. |
| 007 | S05 — Como funciona | Atualizar textos das seis abas existentes; conservar componente, estrutura e estado. |
| 008 | S06 — Mural | Inserir o Mural como exceção autorizada, reaproveitando os balões/mockups existentes. O desenho e a interação serão especificados antes de implementar; não criar chat real. |
| 009 | S07 — Sete frentes | Atualizar nomes e textos nos slots existentes. Não acrescentar navegação de subtipos que não exista hoje. |
| 010 | S08 — Fluxos | Revisar encaixe de texto nos componentes atuais sem trocar a lógica da calculadora. Se a copy exigir comportamento novo ou deixar resultados antigos falsos, registrar bloqueio para decisão antes de alterar. |
| 011 | S09 — Como começar | Atualizar textos nos slots existentes, preservando estados e disposição. |
| 012 | S10 — Entrada/oferta | Atualizar textos já existentes sem mudar formulário, oferta, envio ou endpoint. |
| 013 | S11 — Prova real | Manter ausente se não existir evidência autorizada; não criar depoimentos nem bloco novo. |
| 014 | S12 — FAQ | Atualizar textos das respostas existentes; conservar accordion e navegação. Mudanças de quantidade só se couberem no contrato atual sem alterar interação. |
| 015 | S13 — Sua rotina | Atualizar texto de slot existente; não adicionar formulário ou fluxo novo nesta migração textual. |
| 016 | S14 — CTA/footer/flutuante | Atualizar rótulos e textos existentes; conservar alvos, destinos, instrumentação e comportamento. |
| 017 | Integração final | Conferir consistência da home integrada, copy, links existentes, semântica e regressões de `/pilates`; fechar verificações locais e documentar dependências externas. |
| 018 | Arquitetura e reuso | Depois da integração, propor e executar somente refatorações justificadas de estrutura/composição/reuso/clean code/SOLID, com equivalência visual e comportamental. |

Os nomes S01–S14 são recortes documentais do pacote. Não autorizam criar uma seção/componente para cada recorte. A seção S06 Mural é a única inserção de UI autorizada pelo pedido atual.

## Critérios de passagem por etapa

- A spec aponta campos exatos do JSON, componentes e arquivos existentes, texto antes/depois e invariantes preservados.
- O plano não contém mudança de layout, componente, fluxo ou integração que não esteja expressamente listada acima.
- A revisão de requisitos não deixa conflito de escopo silencioso.
- A implementação não muda handlers, estado, callbacks, URLs de CTA nem tokens CSS nas etapas de copy.
- Cada verificação descreve procedimento e resultado reais; a revisão de aparência compara a cópia com o baseline da origem.
- A etapa 017 verifica a home completa; a etapa 018 ocorre somente depois e repete as verificações afetadas.

## Situação inicial

- Base limpa preparada na branch local `013-taliya-foundation`, sem remote configurado.
- Commit de origem registrado em `baseline.md`.
- ZIP e pacotes extraídos preservados em `reference/TALIYA_INICIAR/`.
- Spec Kit presente; etapa 001 em preparação.
- Nenhuma alteração de aplicação, teste, build, publicação ou mudança no projeto original foi executada nesta nova cópia.
