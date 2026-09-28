# Research — Fundação da migração

## Fontes consultadas

- `TALIYA_INICIAR/00_COMECE_AQUI.txt`: objetivo original, hierarquia das fontes, leitura e limites.
- `TALIYA_INICIAR/03_CONTEXTO_E_ESTADO.md`: decisões anteriores, preservação e estado de implementação.
- `TALIYA_INICIAR/02_PROMPT_MESTRE_SDD.md`: sequência SDD e salvaguardas.
- `TALIYA_INICIAR/04_MAPA_DE_SPECS.md`: catálogo documental de 001–017.
- Pacote landing v1.0: JSON, especificação Markdown, README, schema, QA, fontes e validador.
- Pacote SEO v1.1: auditoria Markdown, política de rotas, critérios, configuração e notas robots.
- Repositório GitHub, commit confirmado pelo Git: `c473a440d562acf6d5314cce0701d48ec284fc07`.
- Arquivos reais: `app/page.tsx`, `app/pilates/page.tsx`, `components/landing/NicheLandingPage.tsx`, seções e `data/landing/niches/pilates.ts`.

## Fatos observados

- A raiz atual redireciona para `/pilates`; a rota Pilates monta o `NicheLandingPage` com `pilatesLanding`.
- O componente principal mantém estados locais de seletor, diagnóstico, agente e calculadora e compõe dez blocos principais mais Header, Footer e assistente flutuante.
- O layout protegido de `/pilates` possui regra local explícita de preservação no `AGENTS.md` do repositório.
- O repo já contém uma instalação Spec Kit/Codex e documentação de outras features, então os artefatos desta migração estão isolados sob `specs/taliya-migration/`.
- O pacote landing define 14 recortes e o SEO define `/` como home pretendida; os destinos públicos de `/pilates` e `/pilates/planos` estão nulos/pendentes no plano de rotas.

## Decisões derivadas

- A nova home pode reutilizar o mesmo compositor e os mesmos blocos sob uma config separada, sem reescrever os componentes.
- Specs S01–S14 não são licença para mexer no JSX/layout/handlers. O conteúdo que não couber nos slots atuais precisa ser escalado na spec responsável.
- S06 é exceção expressa para compor uma seção Mural; deve priorizar as primitivas de conversa já existentes.
- O Mapa SEO, os controles de robots e a intenção de URL canônica dependem de decisão/configuração de publicação e não podem simular produção.
- Refatoração estrutural é post-integration, só com motivação verificável, e preserva a experiência.

## Limites e não executado nesta etapa

- Dependências instaladas do lockfile e preview local iniciado apenas para observar a origem.
- Captura desktop feita no navegador do Codex; a imagem apareceu na conversa, mas não pode ser salva como arquivo do projeto pela interface disponível.
- Captura mobile, lint, testes e build não executados.
- Nenhuma edição de componentes, dados de landing ou rotas.
- Nenhuma verificação de DNS, domínio, crawler em produção, Search Console/Bing ou integração externa.
