# PROMPT MESTRE v2 — TALIYA / COPILOTO — LANDING COM SDD POR SEÇÃO

Versão: 2.0 • 24/09/2026

Este é o prompt completo de implementação. Substitui a versão anterior, incorpora os requisitos dos dois ZIPs e acrescenta o processo obrigatório de SDD com Spec Kit, com uma spec por seção. Não é necessário executar também o prompt anterior.

## 0. Diretriz de execução

Crie um projeto independente usando o código da landing Taliya Pilates como base. Aplique o conteúdo Taliya/Copiloto e o adendo SEO sem redesenhar a landing ou reconstruir a aplicação.

Use SDD de verdade: requisitos verificáveis antes da implementação, plano apoiado no código real, tarefas rastreáveis e verificação após cada recorte. Apenas criar arquivos chamados `spec.md` depois de programar não atende à solicitação.

A organização obrigatória é: uma fundação compartilhada, uma spec transversal de SEO, uma spec para cada seção S01–S14 e uma spec final de integração. São 17 recortes de trabalho, NÃO 17 seções públicas e NÃO 17 aplicações.

Leia primeiro as regras de produto, preservação e fontes nas seções 1–9. Execute pelo processo das seções 10–15. O escopo funcional continua o dos pacotes; SDD muda o método de execução, não o produto nem a direção visual.

## 1. Objetivo e escopo

Quero criar um NOVO PROJETO a partir do código-fonte da landing atual da Taliya Pilates e aplicar os dois ZIPs fornecidos. A Taliya foi pivotada para o Copiloto operacional de quem trabalha por conta e presta serviços.

A marca pública continua sendo TALIYA. “Copiloto” identifica a proposta do produto, não uma autorização para renomear a marca.

Esta tarefa é uma migração de conteúdo sobre a base existente, NÃO um redesign, NÃO uma landing reconstruída do zero e NÃO a implementação do aplicativo Copiloto.

Preserve a stack, arquitetura, dependências, design system, identidade, cores, tipografia, containers, espaçamentos, proporções, responsividade e padrões de interação existentes. Reaproveite header, hero, mockups, balões, cards, seletores, tabs, subtabs, carrosséis, accordions, formulários, footer e botão flutuante.

Altere textos, exemplos, dados, rótulos, destinos, metadados e estados necessários ao pivot. Faça somente as adaptações mínimas de código e composição exigidas pelos pacotes. Não aproveite a tarefa para modernizar o projeto, trocar bibliotecas, reorganizar pastas, criar um novo design system ou acrescentar funcionalidades.

## 2. Fontes que você deve ler

Os arquivos de entrada são:

A. `Taliya_Landing_Pacote_Implementacao_v1_2026-09-18.zip`
B. `Taliya_SEO_Google_ChatGPT_Adendo_Implementacao_v1_1_2026-09-19.zip`
C. Código-fonte original da landing Taliya Pilates, disponível no ambiente de trabalho.

Extraia os ZIPs em diretórios separados: ambos têm README e arquivos que não devem sobrescrever uns aos outros. Não extraia os pacotes cegamente sobre o código.

No pacote A, leia `Taliya_Landing_v1/README.md`, `PROMPT_IMPLEMENTACAO.md`, `Taliya_Landing_Especificacao_v1.md`, `landing.content.pt-BR.json`, `schema.description.md`, `qa-checklist.json`, `sources.json` e `validate_content.py`. PDF e DOCX são versões de consulta; não extraia copy deles quando o JSON já fornece o campo exato.

No pacote B, leia `README.md`, `Taliya_Auditoria_SEO_Google_ChatGPT_v1_1_2026-09-19.md`, `seo_config.example.json`, `route_plan.json`, `structured_data.prelaunch.json`, `robots.public.example.txt`, `robots_policy_notes.md`, `seo_acceptance.md`, `evidence_summary.json` e `fontes.md`.

Use esta divisão de autoridade:

- Este prompt define escopo, proteção do projeto original e ausência de autorização para publicação.
- O código existente é a referência de estrutura técnica, visual e reaproveitamento; a copy antiga não é referência do produto novo.
- O JSON da landing é a fonte canônica de copy, IDs, cenários e estados, complementado pela especificação.
- O adendo SEO v1.1 prevalece nos pontos que revisa explicitamente: metadados, arquitetura pública, política de legado, legibilidade do conteúdo e critérios de SEO. Ele não substitui toda a especificação da landing.

As specs derivam dessas fontes e registram a mudança autorizada; não passam a autorizar uma copy diferente, novos recursos ou redesign apenas por terem sido escritas. Conflitos devem ser resolvidos na fonte responsável, com rastreabilidade.

Não transforme exemplos de configuração em fatos verificados. Não afirme ter lido Product Bibles ou documentos apenas citados nos pacotes se eles não estiverem disponíveis. Não amplie o produto para preencher essas ausências.

## 3. Crie uma cópia independente e preserve a origem

Antes de editar, identifique a raiz real do projeto, instruções do repositório, framework, gerenciador de pacotes, lockfile, scripts, rotas, integração de formulários e configurações de deploy. Não presuma Next.js, nomes de componentes ou caminhos de arquivos.

Se o ambiente já contiver uma cópia independente destinada ao novo projeto, trabalhe nela. Caso contrário, crie uma cópia de trabalho separada, com identificação técnica como `taliya-copiloto-landing`, sem sobrescrever o diretório original. Uma branch no projeto de produção não deve ser tratada, sozinha, como a criação do projeto independente solicitado.

Preserve versões, lockfile, assets reutilizáveis e funcionamento da base. Não copie nem reutilize automaticamente segredos, arquivos `.env` reais, bancos, endpoints de produção ou vínculos com o deploy antigo. Não carregue bindings como `.vercel` ou equivalentes para publicar sobre o projeto original. Use configuração de exemplo sem valores sensíveis.

Não altere o repositório original, seus remotes, DNS, serviços externos ou site publicado. Não faça push, deploy, envio de mensagens ou compra de serviços sem autorização específica.

Execute a base localmente e registre o estado inicial. Capture a landing original antes da migração, quando o ambiente permitir. Separe erros preexistentes de regressões introduzidas. Se o código-fonte não estiver disponível, informe essa ausência: não recrie uma página parecida a partir dos documentos.

## 4. Mapeie os componentes antes de modificar

Produza uma matriz curta com: slot do pacote → componente/arquivo real → alteração → comportamento preservado → teste correspondente. Os IDs S01–S14 identificam recortes funcionais, cada um com sua própria spec de migração. Não são instruções para criar 14 novos componentes, módulos, páginas ou projetos: a divisão documental não deve forçar mudanças na componentização existente.

Aplique o seguinte mapa, respeitando o dataset:

| Slot | Aplicação sobre a base existente |
|---|---|
| S01 | Header e hero: manter composição e trocar narrativa, navegação e demo. |
| S02 | Confiança e controle: inserir a faixa compacta prevista, com os mesmos tokens e primitivas. |
| S03 | Na prática: reutilizar seletor e mockup para os 5 casos. |
| S04 | Sem/Com Taliya: reutilizar toggle e carrossel para os 7 comparativos. |
| S05 | Como funciona: preservar a estrutura de 6 abas e seus padrões internos. |
| S06 | Mural: compor com balões existentes; biblioteca de 84 mensagens e seleção inicial de 24, com adaptação mobile prevista. |
| S07 | Sete frentes: reaproveitar o antigo Time Taliya e subtabs para as 7 categorias e 39 subtipos. |
| S08 | Fluxos: reaproveitar área e cards da calculadora para 5 cenários de 4 passos. |
| S09 | Como começar: reutilizar a estrutura de 4 etapas. |
| S10 | Entrada/oferta: formulário de interesse no pré-lançamento; oferta de lançamento bloqueada. |
| S11 | Prova real: slot reservado, sem renderizar na ausência de evidência autorizada. |
| S12 | FAQ: reutilizar accordion para as 14 perguntas e respostas do modo ativo. |
| S13 | Sua rotina: reutilizar textarea e formulário de pesquisa de encaixe. |
| S14 | CTA final, footer e flutuante: manter componentes e corrigir conteúdo e destinos. |

As adaptações de composição expressamente previstas são a faixa de confiança, o mural e a transformação da calculadora em fluxos. O mural fica entre Como funciona e Sete frentes; os fluxos ficam depois das Sete frentes. Isso não autoriza outros blocos ou uma nova direção visual.

Remova da versão nova a lógica da calculadora de ROI, seus sliders e promessas de dinheiro/tempo recuperado. Não mantenha a calculadora escondida nem apenas renomeie seus campos. Não preserve avatares de agentes como se o novo produto fosse uma equipe de personagens; use a linguagem visual de categoria/marca prevista.

Se faltar uma peça, componha com componentes e tokens existentes, com o menor código adicional possível. Justifique qualquer alteração que ultrapasse conteúdo, estado ou as adaptações explicitamente previstas.

## 5. Aplique o conteúdo completo, sem inventar o produto

Não faça somente uma substituição global de “Pilates” por “serviços”. Atualize contexto, mensagens, exemplos, resultados, CTAs, placeholders, validações, textos acessíveis, navegação, imagens informativas, títulos e metadados.

As sete frentes comerciais são: Clientes, Serviços, Agenda, Orçamentos, Recebimentos, Lembretes e Arquivos e documentos. Elas não são sete agentes nem sete módulos novos do aplicativo. Histórico/contexto são transversais; o orçamento pertence ao mesmo Serviço.

Preserve os limites da V1: o profissional conversa com o número da Taliya usando seu WhatsApp comum; a Taliya não lê os outros chats. WhatsApp e app representam os mesmos registros, mas conta, permissões e assinatura podem exigir o app. Não prometa “nunca precisa do app”, “sem cadastro” ou acesso automático às conversas do negócio.

Não acrescente equipe/múltiplos funcionários, autoagendamento público, tarefas, emissão fiscal, detecção automática de Pix, movimentação bancária, links de pagamento ou cobrança/mensagens automáticas aos clientes. Não invente preços, depoimentos, integrações, métricas, disponibilidade ou datas de lançamento.

Não transforme as demos em regras de negócio erradas: cancelar horário não apaga serviço/pagamento; agendado não significa realizado; recebimento informado não significa integração bancária; lembrete ao dono não significa mensagem enviada ao cliente. A adoção pode ser parcial, sem exigir o fluxo inteiro em todo uso.

Mantenha a copy canônica centralizada, respeitando o padrão do projeto. Um adaptador leve é aceitável; duplicar manualmente o conteúdo em vários componentes não é. Preserve IDs e referências cruzadas. Não exponha guardrails, fontes, instruções internas, gates, dados privados ou `null` como texto público; projete somente os campos necessários para a UI.

## 6. Pré-lançamento e demonstrações

Mantenha `meta.activeMode = prelaunch` como modo inicial e efetivamente renderizado, inclusive em CTAs, FAQ, metadados e eventos.

Use o H1 “Seu negócio organizado. É só falar.”, o CTA principal “Quero testar primeiro”, o secundário “Ver como vai funcionar” e os avisos de desenvolvimento definidos no pacote. Identifique as demos como “Demonstração ilustrativa da experiência planejada.” de forma visível.

A existência de copy de lançamento não autoriza ativá-la. Preços, trial, checkout, fundador e prova social continuam bloqueados pelos gates. Não misture FAQ de lançamento com hero de pré-lançamento.

Implemente cenários locais e determinísticos. Não conecte as demos ao LLM, WhatsApp, backend do produto ou registros reais. Não crie o aplicativo para que a landing funcione.

Preserve os 5 casos, 7 comparativos, 6 abas, 39 subtipos, biblioteca de 84 mensagens, 5 fluxos/20 passos e 14 FAQs. Respeite as quantidades e visibilidades por dispositivo; não exiba todas as mensagens simultaneamente por conveniência.

Cliques no mural, seletor e comparativos abrem a frente/subtipo correto. Links para FAQ abrem a pergunta e tratam foco adequadamente. Fragmentos como `#o-que-resolve?frente=AG&caso=AG04` são navegação local, não endpoints. Trocas de aba não reiniciam a página nem provocam saltos desnecessários.

Cada passo de fluxo mostra o estado acumulado correspondente, mesmo ao acessar diretamente o passo 3. Trocar cenário não mistura dados; voltar passos restaura o snapshot correto. Não apresente como concluída uma ação cuja confirmação ainda não aconteceu no roteiro.

Os cenários usam o relógio fictício de 18/09/2026, America/Sao_Paulo. Não atualize datas isoladas com `Date.now()`. Preserve a coerência de dias, horários, valores, parcelas, reservas e saldos.

Reutilize os mockups existentes com os dados novos. Não invente screenshots “reais” do aplicativo ou chame novas telas de galeria aprovada. Na ausência de asset, mantenha uma apresentação textual acessível e identificada, sem imagem quebrada.

## 7. SEO sem redesenhar nem fragmentar a home

A rota `/` deve servir a landing nova completa no novo projeto. Remova nela o comportamento herdado de levar a raiz para `/pilates`.

Aplique o title do adendo: “Taliya | Organize serviços, agenda e recebimentos pelo WhatsApp”. Preserve o slogan no H1. Use a descrição de pré-lançamento de `seo_config.example.json` e alinhe OG/Twitter ao mesmo estágio. Não publique `ogImageUrl: null`; referencie somente asset existente e coerente.

Use `https://www.taliya.com.br` como origem canônica prevista nos documentos, com configuração adequada ao ambiente. Isso não autoriza alterar o domínio publicado nem redirecionar localhost/preview para o site antigo. Cada página real deve ter sua própria canonical, sem apontar indiscriminadamente para a home.

Não crie `/recursos/*`, páginas por profissão, 39 URLs para subtipos, blog ou rotas vazias apenas por SEO. A home concentra as capacidades. Sobre, Segurança, Privacidade e Termos só entram conforme aplicabilidade e existência de conteúdo verdadeiro/revisado; Ajuda não deve fingir documentação de produto já disponível.

Use âncoras reais para as frentes, compatíveis com os deep links e aliases do pacote. Não inclua fragmentos no sitemap.

Mantenha o texto essencial de todas as frentes, casos e FAQs disponível na renderização inicial, sem exigir clique/fetch para nascer. Preserve as tabs: painéis podem continuar visualmente alternados. Não confunda JSON em script com conteúdo semântico da página, não crie texto escondido exclusivo para robôs e não carregue todas as mídias pesadas de uma vez. Use os recursos de renderização da stack existente, sem migrar de framework.

Prepare robots, sitemap e dados estruturados com base nas rotas reais. O sitemap deve conter apenas páginas públicas, existentes, indexáveis e canônicas. Schema deve refletir conteúdo visível: Organization/WebSite/WebPage, sem ratings, avaliações, preço ou disponibilidade inventados.

Revise os exemplos de robots antes de aplicá-los. Separe política de descoberta e política de treinamento; não invente a preferência do responsável. Revalide documentação oficial dinâmica antes de configurar regras externas. Proteja preview/staging separadamente da futura home pública. Robots não substitui autenticação.

IMPORTANTE: não copie cegamente os redirects do pacote A. O adendo v1.1 revisa o tratamento de `/pilates` e `/pilates/planos`: é preciso sucessor equivalente, transição ou encerramento deliberado. Os destinos `null` não autorizam mandar tudo para `/` ou checkout inexistente. Não deixe a oferta antiga na jornada nova; registre a decisão de migração pendente quando faltar evidência, sem alterar produção.

Não prometa indexação, posição no Google ou recomendação no ChatGPT como resultado garantido da implementação.

## 8. Formulários, integrações e dados

Implemente os dois formulários especificados: `waitlist` e `fit`. Preserve sua distinção: responder sobre a rotina não inscreve automaticamente a pessoa na lista de avisos.

Reutilize somente integrações existentes, compatíveis e autorizadas para o novo projeto. Não suponha que um endpoint antigo de Pilates serve para o pivot ou que uma variável existente pode ser reutilizada em produção.

`runtime.onboardingUrl`, `runtime.leadEndpoint` e `runtime.supportWhatsAppUrl` estão sem valor no pacote. Não invente destinos, números ou serviços. Não simule sucesso com timer, mock, localStorage ou retorno fictício. Sucesso exige confirmação efetiva do backend; timeout/resultado desconhecido não equivale a sucesso.

Implemente validação, loading, prevenção de envio duplicado, erro, estado desconhecido e recuperação conforme o contrato. Dados válidos devem ser preservados para nova tentativa. Testes devem usar dados sintéticos e ambiente autorizado, sem cadastrar leads em produção indevidamente.

Se faltar integração real, prepare a conexão/configuração e mantenha o envio indisponível de maneira honesta na cópia de desenvolvimento. Registre que isso bloqueia a publicação da captura. Não transforme essa dependência em autorização para criar banco, backend ou infraestrutura novos.

Não publique a política antiga de Pilates como se estivesse revisada. Não invente contratos jurídicos ou práticas de segurança. Conteúdo institucional/jurídico ausente deve permanecer como dependência, não como página pública falsa ou link quebrado.

Reutilize a instrumentação aprovada. Não envie nome, e-mail, telefone, conversa, anexos ou relato de rotina ao analytics. `lead_submit_success` só ocorre após confirmação real; assistir a demos nunca dispara compra, trial ou operação real. Preserve atribuição permitida sem coletar conteúdo pessoal.

## 9. Validação obrigatória

Execute `validate_content.py` na pasta correta e os comandos reais de lint, tipos, testes e build do repositório, conforme disponíveis. Não troque o gerenciador de pacotes para contornar problemas.

O arquivo `VALIDACAO_CONTEUDO.json` e a validação do dataset NÃO comprovam funcionamento da landing. Mantenha separadas as evidências de integridade do conteúdo, implementação local e publicação.

Cubra os 42 itens do QA da landing e os 25 do adendo SEO, identificando a origem de cada checklist. Verifique todos os 39 subtipos, 20 passos, 14 FAQs, os dois formulários, referências cruzadas, CTAs, hashes, aliases, navegação mobile e teclado.

Compare antes/depois em 320, 390, 768, 1280 e 1440 px. Essas medidas são larguras de teste, não novos breakpoints. Examine overflow, truncamento, alturas, legibilidade, foco, header, flutuante cobrindo conteúdo e deslocamentos na troca de abas. Corrija encaixes localizados com os tokens existentes; não esconda copy aprovada para fazê-la caber.

Verifique hierarquia real de headings, HTML/DOM antes dos cliques, conteúdo das sete frentes, canonical, links, schema, robots e sitemap. Separe testes locais de verificações que exigem domínio final, CDN, Search Console, Bing ou dados de tráfego.

Faça uma busca final por resíduos de Pilates, studios, alunos, sete agentes, diagnóstico consultivo, ROI, planos antigos, trial e URLs antigas. Analise cada ocorrência: aliases/documentação histórica não são o mesmo que copy pública incorreta. Não faça remoção cega de termos legítimos, como “pacote de sessões”.

Registre resultado como aprovado, falhou, bloqueado ou não testado, com evidência. Não invente screenshots, testes, integrações, desempenho ou validações externas. Corrija o que estiver no escopo e preserve as dependências reais no relatório.

## 10. Adote Spec Kit na cópia, sem recomeçar o projeto

Faça a leitura inicial do código e dos pacotes, identifique a origem/destino e estabeleça uma cópia segura e uma referência do estado inicial. Leitura, cópia, inventário, captura de evidências e preparação documental são o bootstrap; ainda não autorizam alterações funcionais sem spec/plan/tasks.

Identifique se Spec Kit já está instalado, sua versão, a integração com o agente, os templates, as regras e os gates existentes. Preserve customizações úteis. Não reinstale nem atualize ferramentas automaticamente apenas para seguir um exemplo deste prompt.

Se for necessário inicializar Spec Kit, faça-o somente no projeto novo e depois de preservar uma referência revisável. Confira a documentação oficial e os comandos disponíveis na versão escolhida antes de executar instalação/inicialização. Não aplique `--force` cegamente sobre arquivos existentes. Inspecione o diff da configuração e confirme que a aplicação não foi reconstruída.

Registre versão e forma de invocação. As grafias `/speckit.specify`, `/speckit-specify` ou `$speckit-specify` dependem da integração/modo. Use a forma realmente exposta pelo agente. Etapas SDD são invocadas no agente; não são comandos de terminal. Se a ferramenta não puder ser executada, registre a limitação: documentação manual equivalente pode ser preparada, mas não afirme que executou Spec Kit.

Crie ou atualize a Constitution em `.specify/memory/constitution.md` e as instruções aplicáveis em `AGENTS.md`, respeitando arquivos e convenções existentes. A Constitution é única para a landing; não crie uma por seção. Ela deve fixar, sem repetir toda a copy:

- Projeto original intocado; execução restrita à cópia e sem publicação automática.
- Reaproveitamento da stack, dos componentes e do design system existentes; nenhum redesign ou upgrade oportunista.
- Fontes canônicas, modo de pré-lançamento, limites da V1 e ausência de promessas inventadas.
- Uma spec de mudança por seção; comportamento comum com um único contrato responsável.
- Plano técnico baseado no repositório, análise antes de implementar e verificação com evidências.
- Mudanças de contrato exigem análise das specs consumidoras; testes e critérios não podem ser enfraquecidos para esconder falhas.

A adoção de SDD não exige documentar retroativamente toda a aplicação antiga. Inventarie somente o necessário para executar e verificar esta migração. Não acrescente arquitetura ou infraestrutura apenas porque um template oferece campos para isso.

### 10.1. Organização documental

Adote a seguinte organização lógica. Reutilize diretórios documentais equivalentes que já existam; não mova o código da aplicação para imitar esta árvore.

```text
AGENTS.md
.specify/
  memory/
    constitution.md
specs/
  README.md
  001-fundacao-migracao/
  002-seo-arquitetura-publica/
  003-s01-header-hero/
  004-s02-confianca-controle/
  005-s03-na-pratica/
  006-s04-sem-com-taliya/
  007-s05-como-funciona/
  008-s06-mural/
  009-s07-sete-frentes/
  010-s08-fluxos/
  011-s09-como-comecar/
  012-s10-entrada-oferta/
  013-s11-prova-real/
  014-s12-faq/
  015-s13-sua-rotina/
  016-s14-cta-footer-flutuante/
  017-integracao-validacao-final/
docs/
  landing/
    baseline.md
    source-map.md
    shared-contracts.md
    seo-contract.md
    traceability.md
    decisions.md
```

`specs/README.md` é o índice único de specs, dependências e andamento. Identifique o que está especificado, revisado, implementado, verificado, bloqueado externamente e não publicado; não reduza esses estados a um único “concluído”. Registre também a próxima tarefa e os arquivos relevantes para retomada por outra conversa/agente.

Os nomes numéricos identificam recortes, não impõem a ordem técnica de implementação, a ordem de branches ou novas rotas. A ordem visual da landing continua sendo a do pacote.

Não trate uma convenção manual de “spec ativa” como suficiente para a ferramenta. Antes de cada etapa, confirme o diretório que Spec Kit realmente resolverá. Nas versões que usam `.specify/feature.json` ou `SPECIFY_FEATURE_DIRECTORY`, confira esse contexto; não suponha que trocar a branch troca a feature ativa. Evite executar etapas de specs distintas sobre o mesmo contexto ativo compartilhado.

## 11. Catálogo obrigatório de specs

| Spec | Responsabilidade e limite |
|---|---|
| 001 — Fundação da migração | Diagnóstico delimitado, preservação da origem, baseline visual/técnico, inventário de componentes, fonte canônica, modo de pré-lançamento e contratos compartilhados. Implementar apenas adaptações comuns realmente necessárias. Não reconstruir a base. |
| 002 — SEO e arquitetura pública | Home em `/`, metadados, canonical, renderização semântica, âncoras, sitemap, robots, schema e tratamento documentado do legado. É responsável pelas regras transversais do adendo SEO; não cria uma coleção de páginas novas. |
| 003 — S01 Header e hero | Migrar conteúdo, navegação, CTAs e demonstração do topo preservando a composição. Consumir os contratos globais de destino, modo e conteúdo; não recriar o header. |
| 004 — S02 Confiança e controle | Faixa compacta prevista, com copy e limites verdadeiros e composição pelas primitivas existentes. Sem selos, certificações ou garantias inventadas. |
| 005 — S03 Na prática | Cinco casos, seletor, mockup, estados e ligações para os subtipos correspondentes. Reutilizar a interação existente. |
| 006 — S04 Sem/Com Taliya | Sete comparativos, toggle, carrossel e destinos consistentes, sem prometer resultados financeiros fictícios. |
| 007 — S05 Como funciona | Seis abas e seus conteúdos/estados. Preservar os padrões visuais e garantir conteúdo semântico acessível sem depender de clique para ser criado. |
| 008 — S06 Mural | Biblioteca de 84 mensagens, seleção prevista e adaptação por dispositivo; cliques abrem o destino correto. Não criar um chat real ou uma spec para cada mensagem. |
| 009 — S07 Sete frentes | Sete categorias, 39 subtipos, tabs/subtabs, mockups, deep links e conteúdo inicial. Uma única spec desta seção; os 39 subtipos são dados/cenários parametrizados. |
| 010 — S08 Fluxos | Substituir a calculadora pelos cinco fluxos de quatro passos, com snapshots coerentes. Remover a lógica antiga de ROI na cópia. |
| 011 — S09 Como começar | Quatro etapas com narrativa e destinos de pré-lançamento; não pressupor onboarding já disponível. |
| 012 — S10 Entrada/oferta | Formulário `waitlist`, validações, consentimentos e estados previstos. Preços/trial/checkout continuam bloqueados. Consome o contrato comum de envio, sem criar uma API diferente. |
| 013 — S11 Prova real | Regras de evidência, autorização e visibilidade. Sem prova válida, não renderizar bloco, espaço vazio ou depoimento de exemplo. Verificar a ausência correta é uma entrega válida desta spec. |
| 014 — S12 FAQ | Quatorze perguntas/respostas do modo ativo, accordion, links, abertura e foco. Copy de lançamento não pode vazar para o pré-lançamento. |
| 015 — S13 Sua rotina | Formulário `fit`, relato, validações e estados. Mantém a finalidade separada da lista de interesse e reutiliza o contrato técnico comum quando aplicável. |
| 016 — S14 CTA final, footer e flutuante | Conteúdo, destinos, controles e comportamento responsivo, sem sobreposição indevida. Links institucionais somente para destinos reais e revisados. |
| 017 — Integração e validação final | Coerência da página inteira, jornadas entre seções, regressões compartilhadas, cobertura dos dois pacotes e classificação de bloqueios de publicação. Não introduz novos requisitos de produto. |

S01–S14 continuam com os IDs canônicos dos pacotes. Os números 003–016 são apenas os identificadores dos diretórios SDD. Não renumere os IDs do conteúdo para coincidirem com as pastas.

Nenhuma spec de seção deve virar uma spec por botão, card, aba, mensagem, categoria ou subtipo. Componentes reutilizados não recebem specs de reconstrução separadas. Quando um ajuste comum for necessário, ele tem um único responsável e consumidores documentados.

S11 deve ter uma spec mesmo sem bloco visível: ela formaliza e testa a regra de não publicar prova fictícia. Não adicionar prova real nesta etapa não autoriza inventá-la nem implica que a landing precise de um placeholder público.

## 12. Contratos compartilhados e fronteiras de alteração

A spec 001 é responsável por `shared-contracts.md`; a spec 002 é responsável por `seo-contract.md`. Escreva cada regra comum uma vez e referencie-a nas specs de seção. Não replique a mesma configuração em 14 documentos divergentes.

`shared-contracts.md` deve registrar os contratos realmente necessários:

**Conteúdo e modo:** localização da fonte canônica, IDs, projeção dos campos públicos, resolução de `prelaunch`, gates e política de conteúdo ausente. Referencie o JSON, sem copiá-lo inteiro para as specs ou criar uma segunda fonte editável de copy.

**Navegação e destinos:** seções/âncoras, frente/subtipo/FAQ, aliases, comportamento de abertura, histórico, scroll e foco. Para cada vínculo, identifique emissor e receptor, sem misturar fragmentos locais com rotas de servidor.

**Demonstrações:** relógio fictício, seleção ativa, snapshots de fluxo, reset por cenário, avisos e ausência de efeitos reais. Prefira os mecanismos já existentes e adapte apenas o necessário; não crie um motor genérico de workflow.

**Formulários:** finalidades separadas de `waitlist` e `fit`, campos e consentimentos do pacote, estados, formato de envio/resposta comprovado, prevenção de duplicidade e comportamento sem integração. Dados pessoais não entram em analytics. Não inferir um contrato de servidor apenas a partir da UI.

**Instrumentação e apresentação compartilhada:** eventos autorizados, ausência de dados pessoais, responsabilidades sobre componentes/tokens e regras comuns de acessibilidade. Não redesenhar componentes globais para resolver um texto isolado.

`seo-contract.md` centraliza rotas públicas, metadados, canonical, HTML inicial, hierarquia de títulos, dados estruturados, políticas de ambiente e indexação. Cada seção verifica sua contribuição sem editar configurações globais por conta própria. O title descritivo de SEO e o H1 comercial têm papéis distintos; não os torne iguais por automatismo.

Mantenha em `source-map.md` a relação entre pacote/arquivo, heading ou caminho JSON real e spec responsável. Em `traceability.md`, ligue requisito de origem → requisito da spec → tarefa → arquivo alterado → evidência. Use IDs canônicos dos checklists e um prefixo de origem para evitar colisões entre QA da landing e QA de SEO.

Uma seção pode depender de várias fontes e contratos, mas cada alteração compartilhada precisa de um responsável único. Exemplo: S01 e S14 consomem o mesmo destino de CTA; S10 é o destino da inscrição; não crie três interpretações independentes de “Quero testar primeiro”.

Se uma seção exigir alteração em componente, utilitário, estilo ou contrato compartilhado, registre a necessidade no plano, a spec responsável e os consumidores impactados. Valide os consumidores depois da mudança. Não misture alterações de várias specs sem vínculo explícito nem deixe a decisão acontecer silenciosamente no código.

Não é necessário criar branch/PR ou pacote de código para cada spec. Caso o repositório use essa organização, preserve suas regras, mas mantenha uma linha integrada que contenha as dependências. A separação documental não autoriza forks incompatíveis dos componentes.

## 13. Conteúdo mínimo de cada spec e seus artefatos

Cada pasta de feature deve conter, respeitando os templates efetivamente instalados:

```text
spec.md
plan.md
tasks.md
checklists/
  requirements.md
verification.md
```

`verification.md` é um registro adicional exigido por este projeto, não a afirmação de que Spec Kit o gera automaticamente. Use também os relatórios nativos produzidos pela versão instalada. Artefatos como `research.md`, `data-model.md`, `contracts/` e `quickstart.md` só precisam de conteúdo quando tiverem função real ou forem exigidos pelo workflow; nunca invente banco, API ou pesquisa para preencher um template.

### 13.1. `spec.md` — o que muda e como reconhecer o resultado

A spec de uma seção deve registrar:

1. Identificador Sxx, objetivo da seção e resultado esperado para o visitante.
2. Fontes exatas: arquivos, headings, caminhos JSON e IDs efetivamente encontrados. Um caminho ainda não inspecionado não pode ser apresentado como confirmado.
3. Estado atual relevante observado no repositório e diferença desejada. Não fazer uma especificação retroativa de toda a aplicação.
4. O que permanece invariável: composição, padrões visuais/interativos e limites de escopo.
5. Conteúdo que entra, conteúdo antigo que sai, quantidade de cenários e regras de pré-lançamento/visibilidade, sem duplicar o dataset integral.
6. Comportamentos: estado inicial, interações, transições, resultados e estados de erro/ausência quando aplicáveis.
7. Relação com outras seções e referências aos contratos comuns, incluindo emissão/recepção de deep links e CTAs.
8. Requisitos responsivos, de acessibilidade e de contribuição ao SEO relevantes à seção.
9. Critérios de aceitação observáveis e exemplos Given/When/Then quando houver comportamento. Frases vagas como “bonito”, “moderno” ou “SEO bom” não são critérios suficientes.
10. Fora de escopo, dependências, dúvidas materiais e bloqueios externos com impacto delimitado.

Use IDs únicos, por exemplo `S07-FR-001` para requisito e `S07-AC-001` para aceitação, sem alterar IDs do pacote. Não atribua precisão fictícia a medidas que ainda não foram verificadas no código.

### 13.2. `plan.md` — como fazer na base real

O plano deve informar arquivos/componentes efetivamente encontrados, entradas de dados, reaproveitamento, adaptações mínimas, impacto em compartilhados, testes existentes e estratégias de verificação. Separe claramente preservar, alterar e remover. Código, arquitetura e decisões técnicas detalhadas pertencem aqui, não a uma reescrita especulativa do produto.

Inclua uma matriz de mudança por arquivo: motivo, requisito atendido, alteração esperada e consumidores afetados. Não trate a matriz como autorização para mudanças extras. Escolha o menor ajuste viável; não reestruture pastas, dependências ou estilos para tornar as specs simétricas.

### 13.3. `tasks.md` — trabalho executável e rastreável

Gere tarefas pequenas, ordenadas por dependência, vinculadas aos requisitos/aceitação e aos arquivos reais. Use a sintaxe de tarefas exigida pelo template instalado; o identificador da spec junto do ID da tarefa elimina ambiguidade entre pastas.

Inclua implementação, atualização documental pertinente, verificações locais, integrações entre seções e registro de evidência. Não marque tarefas de execução como concluídas apenas porque há texto explicando como executá-las.

### 13.4. Checklists versus verificação

Os checklists de requisitos avaliam a qualidade/completude da especificação. Eles não comprovam que o código funciona. Respeite a responsabilidade de revisão prevista pelo workflow; o implementador não deve marcar checklists arbitrariamente para liberar seu próprio avanço.

Em `verification.md`, registre ambiente, cenário, comando ou procedimento realizado, resultado, evidência e limitações. Para cada verificação, use aprovado, falhou, bloqueado ou não testado. Distinga observação visual, teste automatizado, análise documental e validação externa.

O conjunto de evidências deve incluir comparação antes/depois da região quando possível. Textos diferentes podem mudar quebras de linha; a comparação verifica preservação visual e encaixe, não exige identidade literal de pixels entre copys diferentes. Desvios intencionais precisam de justificativa vinculada ao pacote.

### 13.5. Exemplo de requisito, sem inventar a implementação

Para S07, um critério possível baseado no contrato do pacote é:

“Dado o deep link válido da frente AG e do caso AG04, quando a landing é carregada ou o vínculo é acionado em outra seção, a seção Sete frentes seleciona a frente e o subtipo correspondentes, apresenta sua demonstração e aplica scroll/foco conforme o contrato compartilhado, sem navegação para uma rota inexistente.”

Verifique os IDs e a copy no JSON antes de usar o exemplo. O critério descreve um comportamento; o `plan.md` identifica qual componente real o implementará. Não invente nomes como `SevenFronts.tsx` antes de ler o projeto.

## 14. Ciclo e ordem de execução

### 14.1. Primeira passagem: preparar a migração

Apresente um plano curto, inventarie a base relevante e os dois pacotes, estabeleça as regras comuns e crie o catálogo de specs com dependências e responsáveis. Prepare primeiro a fundação e os contratos transversais. Não substitua esta passagem por uma auditoria genérica da web ou por uma proposta de redesign.

Antes de começar as seções, deixe o `spec.md` de S01–S14 com escopo, fontes, invariantes, vínculos e aceitação definidos o suficiente para detectar conflitos entre as partes. Isso não obriga a detalhar antecipadamente todas as tarefas de todas as seções: produza/revise `plan.md` e `tasks.md` da spec ativa perto da execução, com base no estado real do código.

A preparação documental não é entrega final desta tarefa. Continue pela implementação dos recortes autorizados depois das verificações de prontidão.

### 14.2. Ciclo obrigatório por recorte

Use a Constitution uma vez no nível do projeto. Para cada spec, siga o ciclo lógico abaixo, com as invocações suportadas pela integração instalada:

```text
Specify → Clarify → Plan → Checklist → Tasks → Analyze
        → Implement → Converge → registrar evidências
```

Clarify deve consultar primeiro os pacotes, os contratos e o código. Não reabra decisões já aprovadas, não invente respostas do usuário e não transforme lacunas externas em decisões próprias. Onde nada estiver ambíguo, registre isso sem criar perguntas artificiais.

Analyze ocorre antes da implementação e verifica consistência entre spec, plano, tarefas, fontes e contratos comuns. Resolva achados bloqueadores nos artefatos responsáveis e repita a análise. Uma análise somente da spec ativa não substitui a revisão das dependências documentadas.

Implemente somente o trabalho coberto pelo plano/tarefas. Depois execute a verificação de convergência e os testes reais. Se surgirem lacunas dentro do escopo, acrescente as tarefas necessárias, corrija e verifique novamente. Não reduza os critérios de aceitação, suprima testes ou declare N/A para obter um relatório positivo.

O relatório da ferramenta deve ser preservado com seu resultado real. Ele não substitui testes executados, revisão visual, confirmação de endpoint ou validação externa. Não declare Converged quando a ferramenta não foi executada ou retornou outro estado.

Em versões sem uma etapa nativa disponível, registre a diferença e realize uma revisão equivalente explicitamente identificada, sem inventar um comando executado. Isso não elimina a obrigação de verificar a implementação.

### 14.3. Dependências entre seções

Comece pela spec 001. Estabeleça cedo o contrato e as tarefas estruturais executáveis da spec 002; as verificações de SEO que dependem da home completa serão fechadas após as seções. Não marque 002 como totalmente verificada só porque os metadados foram alterados.

Defina a sequência das seções pelo grafo real de dependências, sem modificar a ordem visual da página. Alvos de navegação como Sete frentes, FAQ e o formulário de interesse precisam de contratos estáveis antes de seus emissores. Sempre que viável, implemente/verifique o receptor antes do vínculo que o utiliza.

As seções simples podem avançar independentemente quando não alteram os mesmos arquivos/contratos. Não paralelize automaticamente vários agentes sobre componentes compartilhados, estilos globais ou o mesmo contexto ativo do Spec Kit.

Não é obrigatório esperar a integração externa do formulário para ajustar o texto de outra seção. Porém, o fluxo de captura não pode ser declarado funcional até ter a integração e a verificação correspondentes.

Finalize as tarefas globais de 002 e execute 017 sobre a landing integrada. Essa spec final deve testar, especialmente, transições entre seções, ausência de IDs duplicados, CTAs coerentes, modo único, HTML inicial, formulários, links reais, responsividade e ausência de resíduos do pivot antigo.

### 14.4. Prontidão, autonomia e mudanças

Não inicie alterações funcionais de uma spec sem fontes consultadas, requisitos verificáveis, plano apoiado no código, tarefas e análise sem conflitos bloqueadores. Não considere “arquivo existe” suficiente para atender a esse gate.

Dentro do escopo aprovado, continue sem pedir confirmação a cada seção ou microetapa. Respeite gates humanos que tenham sido explicitamente exigidos pelo usuário ou pelo repositório: nunca registre aprovação humana inexistente. Apresente o material necessário nesse gate, sem burlar a regra por automação.

Decisões materiais não resolvidas sobre redesign, expansão de produto, infraestrutura, credenciais, jurídico ou publicação não devem ser tomadas silenciosamente. Isole o bloqueio e execute os recortes independentes. Não interrompa tudo por uma limitação que afeta apenas um destino externo, nem declare o conjunto pronto para publicar com esse bloqueio.

Trate as specs como contratos vivos desta migração: novas descobertas relevantes exigem alteração rastreável no artefato responsável e revisão de plano/tarefas/consumidores. Isso não autoriza modificar retroativamente os requisitos para justificar uma implementação divergente. Mudança de produto ou direção visual continua exigindo autorização.

## 15. Entrega, cobertura e condição de conclusão

Entregue o projeto independente, a organização SDD preenchida e o relatório de migração. O relatório deve indicar origem/destino, preservações, adaptações justificadas, arquivos alterados, matriz S01–S14, cobertura dos checklists dos dois pacotes, testes realmente executados e evidências visuais disponíveis.

Mostre no índice o estado de cada uma das 17 specs. Uma spec pode ter implementação local pronta e ainda ter validação externa bloqueada; isso deve ficar visível. S11 pode estar corretamente implementada e verificada com o bloco ausente, sem significar que prova comercial tenha sido coletada.

Não declare os 42 itens da landing ou os 25 itens SEO aprovados automaticamente por terem sido mapeados. Documentar um requisito, implementar código, executar teste e publicar são quatro fatos distintos.

Mantenha os limites de implementação/publicação das seções anteriores: não fazer push, merge, deploy, alteração do domínio ou uso de serviços reais sem a autorização pertinente. Preparação para produção não equivale a publicação autorizada.

A retomada deve ser possível a partir de `specs/README.md`, Constitution, contratos, spec ativa, tarefas e evidências, sem depender da memória desta conversa. Documente o mecanismo real de seleção da spec ativa e preserve trabalho já concluído ao retomar.

**Critério final:** mesma base visual e técnica da Taliya, em projeto independente, com o conteúdo Copiloto e SEO aplicados pelos recortes SDD, cada seção rastreável e verificável, sem semântica antiga indevida, expansão de escopo, alteração do site original ou promessas fictícias.

## Referências do processo

Estas referências orientam a adoção do Spec Kit, não alteram os requisitos dos ZIPs. Consulte a documentação compatível com a versão efetivamente instalada. URLs de referência técnica:

```text
https://github.com/github/spec-kit
https://github.github.io/spec-kit/guides/existing-projects.html
https://github.github.io/spec-kit/quickstart.html
https://github.github.io/spec-kit/reference/integrations.html
https://github.github.io/spec-kit/reference/agentic-sdd.html
```
