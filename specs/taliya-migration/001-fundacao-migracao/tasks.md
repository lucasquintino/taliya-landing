# Tasks: Fundação da migração Taliya/Copiloto

**Input**: `spec.md`, `plan.md`  
**Prerequisites**: Repositório e pacotes identificados  
**Tests**: Nenhum teste de aplicação nesta etapa documental.

## Phase 1: Cópia e proveniência

- [x] T001 Clonar o repositório indicado no diretório independente.
- [x] T002 Conferir que `HEAD` corresponde ao commit de origem `c473a440d562acf6d5314cce0701d48ec284fc07`.
- [x] T003 Criar branch local para a retomada Spec Kit.
- [x] T004 Remover `origin` da cópia independente e confirmar ausência de remotes.
- [x] T005 Registrar revisão, branch, rotas e limites em `docs/landing-migration/baseline.md`.

## Phase 2: Fontes e contexto SDD

- [x] T006 Copiar os materiais extraídos do ZIP para `docs/landing-migration/reference/TALIYA_INICIAR/`, fora de `public/`.
- [x] T007 Registrar autoridade dos pacotes, escopo e sequência em `docs/landing-migration/plan.md`.
- [x] T008 Mapear as rotas e componentes reais em `docs/landing-migration/source-map.md`.
- [x] T009 Definir contratos transversais e pendências em `shared-contracts.md` e `decisions.md`.
- [x] T010 Preparar a spec 001, plano e índice da migração em `specs/taliya-migration/`.
- [x] T011 Configurar o contexto ativo Spec Kit para a feature 001 sem remover os templates da origem.
- [x] T012 Capturar o baseline desktop de `/pilates` e registrar que a viewport mobile não está disponível na ferramenta atual.
- [x] T013 Revisar a qualidade da spec e registrar os checks de aplicação como pendentes, já que não houve mudança de aplicação.

## Dependencies & Execution Order

- T001–T005 habilitam a base independente.
- T006–T011 definem o escopo e a rastreabilidade.
- T012 está documentada; desktop foi observado e a captura mobile permanece limitação explícita antes de mudanças que afetem layout responsivo.
- O usuário pediu etapas sequenciais; o próximo recorte é a spec 002 de SEO transversal.
