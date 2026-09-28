# Baseline da cópia independente

## Proveniência observada

- Repositório de origem: `https://github.com/lucasquintino/agentes-landing-system`
- Commit copiado: `c473a440d562acf6d5314cce0701d48ec284fc07`
- Data/mensagem do commit: `2026-08-05T13:20:29-03:00` — `Expose commercial contract in runtime health`
- Branch local de retomada: `013-taliya-foundation`
- Diretório independente: `outputs/taliya-copiloto-landing-restart/`
- Remote Git: removido da cópia depois do clone; nenhum remote foi configurado no projeto independente.
- Estado inicial da cópia: arquivos de aplicação iguais ao commit acima, antes dos documentos desta migração.
- O repositório original não foi editado por este trabalho.

## Estrutura observada

- Next.js App Router, React, TypeScript, Tailwind e `npm` com `package-lock.json`.
- `/` redireciona para `/pilates` em `app/page.tsx`.
- `/pilates` monta `NicheLandingPage` usando `pilatesLanding` e sua metadata.
- A página atual compõe Header, Hero, seletor de intenção, comparação/diagnóstico, Como funciona, calculadora, demonstração de agentes, etapas de venda, FAQ, CTA final, Footer e assistente flutuante.
- `/pilates/planos` e `/privacidade` também existem. Existem rotas de API e serviços do produto; elas não fazem parte desta migração.
- O pacote SEO propõe `/` como landing Copiloto e deixa a decisão pública de `/pilates` e `/pilates/planos` pendente. Esta cópia manterá essas rotas sem alteração até decisão baseada na política do pacote.
- Os 35 arquivos de `TALIYA_INICIAR` foram copiados e os hashes de `07_INTEGRIDADE/SHA256SUMS.txt` passaram.

## Spec Kit observado

- CLI local: `specify 1.0.7`.
- Integração e templates existentes: Codex / Spec Kit `0.8.3.dev0` em `.specify/` e `.agents/skills/`.
- A configuração original apontava o contexto ativo para a feature comercial 010 do repositório. Esta cópia passa a usar o contexto da migração Taliya.
- O hook obrigatório `speckit.git.feature` foi executado uma vez por `bash`; criou a branch `013-taliya-foundation`.
- Hooks de commit automático estão desativados em `.specify/extensions/git/git-config.yml`.
- Não foi reinstalado nem atualizado o Spec Kit.

## Baseline ainda pendente

- A captura desktop foi observada via navegador local em `http://127.0.0.1:3001/pilates`; o screenshot não foi salvo como arquivo.
- Captura mobile permanece pendente porque a ferramenta CUA atual não expõe controle de viewport e BrowserAct não tem navegador configurado.
- Lint, testes e build permanecem não verificados.
- Esses itens devem ser concluídos antes da primeira alteração visual/textual de aplicação, conforme a spec 001. Nenhuma evidência visual é declarada nesta etapa.
