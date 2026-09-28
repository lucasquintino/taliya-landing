# Implementation Plan: Fundação da migração Taliya/Copiloto

**Branch**: `013-taliya-foundation` | **Date**: 2026-09-25 | **Spec**: `spec.md`

## Summary

Preparar uma cópia local independente do commit escolhido, preservar a experiência `/pilates`, trazer os pacotes para uma área documental fora de `public/`, ativar o fluxo Spec Kit para a migração e registrar o plano textual com seus limites.

## Technical Context

**Language/Version**: TypeScript / React do repositório existente  
**Primary Dependencies**: Next.js App Router e dependências já fixadas no lockfile  
**Storage**: N/A nesta etapa  
**Testing**: Nenhum teste de aplicação solicitado para a fundação documental  
**Target Platform**: Aplicação web existente  
**Project Type**: Landing web com rotas adicionais preservadas  
**Performance Goals**: Sem alteração de runtime nesta etapa  
**Constraints**: Cópia sem remote, sem alteração da origem, sem publicação  
**Scale/Scope**: Um projeto local e 18 specs sequenciais

## Constitution Check

- Cópia independente e proveniência: atende.
- Preservação da base, layout e interações: atende; não há mudança de aplicação nesta etapa.
- Fonte canônica e SEO: identificadas com responsabilidades separadas.
- Escopo de UI: somente S06 está autorizado como nova seção; SEO e S018 têm gates próprios.
- Evidência honesta: baseline visual ainda pendente e marcado como tal.
- Publicação: fora do escopo e sem autorização.

## Project Structure

```text
AGENTS.md
.specify/
  feature.json
  memory/constitution.md
docs/landing-migration/
  baseline.md
  decisions.md
  plan.md
  shared-contracts.md
  source-map.md
  reference/TALIYA_INICIAR/
specs/taliya-migration/
  README.md
  001-fundacao-migracao/
    spec.md
    plan.md
    tasks.md
    checklists/requirements.md
    verification.md
```

**Structure Decision**: Os artefatos da migração ficam em `specs/taliya-migration/`, separados dos specs de produção já existentes no repositório-base. Os IDs lógicos pedidos (001–018) são mantidos sem substituir os specs que vieram na origem.

## Design Impact

Nenhuma alteração de aplicação, componente, asset, estilo, interação, API ou rota nesta etapa. Os próximos planos precisam conter matriz arquivo→motivo→requisito→efeito e demonstrar preservação.

## Complexity Tracking

Sem violação da Constituição nesta etapa.
