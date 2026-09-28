# Handoff Codex + Speckit


## Atualizacao comercial posterior

Este documento e legado quando falar de acesso antecipado, beta ou validacao. A direcao atual esta em `specs/001-niche-landing-system/spec.md`, `specs/002-floating-ai-sales-agent/spec.md` e `specs/spec-1-2-final-readiness-map.md`: vender o SaaS vertical por nicho com consultor/agente de IA, planos, assinatura, WhatsApp e diagnostico de agente sob medida.

## Primeiro prompt para conversa avulsa do Codex + Speckit

Anexe o ZIP completo e cole:

```text
Você vai iniciar um projeto novo usando Codex + Spec Kit para construir um sistema de landing pages por nicho.

IMPORTANTE:
Não implemente nada ainda.
Primeiro leia os documentos anexados, entenda o escopo, proponha arquitetura e prepare o fluxo Spec Kit.

Leia primeiro o arquivo 00_REGRAS_FINAIS_PARA_CODEX.md. Ele sobrescreve qualquer decisão anterior.
A fonte principal consolidada é 10_Final_Handoff_Consolidado_MultiNicho_vFinal.md.

Se houver conflito entre documentos antigos e estes arquivos finais, siga estes arquivos finais.

Decisão principal:
Pilates é a primeira landing, mas o produto deve nascer como um sistema multi-nicho de landing pages.
Não implemente uma página hardcoded apenas para Pilates.

Precisamos de uma arquitetura reutilizável para futuras landings:
- /pilates
- /fisioterapia
- /estetica
- /personal

A primeira entrega será /pilates, mas a estrutura deve permitir criar novas landings por configuração/dados.

Antes de implementar qualquer código, faça apenas isto:
1. Liste quais documentos encontrou e leu.
2. Resuma o entendimento do produto e da landing.
3. Confirme que Pilates é a primeira landing de um sistema multi-nicho.
4. Proponha a arquitetura técnica do projeto.
5. Diga quais dependências precisam ser instaladas.
6. Diga se o Spec Kit está disponível ou precisa ser inicializado.
7. Proponha a sequência de comandos/etapas para inicializar projeto, Spec Kit, specification, plan, tasks, analyze e implementação.
8. Não implemente ainda.
```

## Prompt para speckit.specify

```text
/speckit.specify Criar um sistema reutilizável de landing pages por nicho, começando pela landing /pilates.

A landing de Pilates deve vender acesso antecipado a uma plataforma de agentes de IA operacionais para studios de Pilates.

O sistema deve usar componentes reutilizáveis e conteúdo data-driven por nicho.

A primeira landing é /pilates, mas a arquitetura deve permitir futuras páginas /fisioterapia, /estetica e /personal por configuração.

Seguir 00_REGRAS_FINAIS_PARA_CODEX.md e 10_Final_Handoff_Consolidado_MultiNicho_vFinal.md como fonte da verdade.
```

## Prompt para speckit.plan

```text
/speckit.plan Implementar usando Next.js, TypeScript, Tailwind CSS, shadcn/ui, lucide-react e Framer Motion.

Criar estrutura data-driven:
- data/landing/niches/pilates.ts
- data/landing/niches/types.ts
- components/landing/shared
- components/landing/sections
- components/landing/mockups
- lib/landing/money-calculator.ts
- lib/landing/tracking.ts

A primeira rota deve ser /pilates.
```

## Prompt para speckit.tasks

```text
/speckit.tasks Quebrar em tarefas por fases:
1. Setup do projeto e dependências
2. Tipos e dados por nicho
3. Componentes compartilhados
4. Hero e seções estáticas
5. Blocos interativos
6. Calculadora Dinheiro na Mesa
7. Mockups por agente
8. Formulário e tracking com niche
9. Responsivo/mobile
10. Animações
11. Build/lint/typecheck
```
