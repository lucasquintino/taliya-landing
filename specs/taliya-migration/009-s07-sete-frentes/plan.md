# Plano — Produção em Frentes do negócio

## Recorte autorizado

Implementar localmente a proposta de Produção nos seis fluxos existentes, para revisão humana ao final. A autorização atual é exclusiva desta seção; preservar as mudanças anteriores de outras seções.

## Implementação

1. Usar `featuredFlowEditorial`, `reviewedFlowSummaries` e `reviewedFlowNarrative` em `data/landing/agentFlowCatalog.ts`; essas fontes montam os fluxos ativos G1/G2/G3/G4/G5/G12.
2. Atualizar apenas os rótulos G1 e G3 em `flowNavLabels` do componente `AgentsDemoSection.tsx`. Manter Produção e Versões do documento já aprovados.
3. Preservar o modelo de dados, IDs, canais, seis abas, seleção desktop, navegação mobile, swipe, indicação de overflow e callbacks. Os possíveis caminhos usam a lista rolável existente.
4. Não editar o app, outras frentes, outras seções, condições comerciais ou o subtítulo removido.

## Verificação e revisão

Conferir diff e conteúdo calculado dos seis fluxos; lint dos arquivos alterados; resposta HTTP local e ausência do subtítulo removido. Inspeção visual desktop/mobile permanece pendente pelo bloqueio do navegador integrado nesta conversa; não usar outro navegador ou automação para contornar o bloqueio. Entregar o preview da porta 3001 para revisão humana.

A autorização de copy não valida a disponibilidade das capacidades ampliadas. Registrar a confirmação de produto como pendência antes de publicação; nenhum deploy é autorizado.
