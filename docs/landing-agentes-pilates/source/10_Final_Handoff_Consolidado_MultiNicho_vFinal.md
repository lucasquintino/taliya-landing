# Final Handoff Consolidado Multi-Nicho vFinal

## Atualizacao comercial posterior

Este documento e legado para decisoes comerciais que conflitarem com as specs atuais. Para implementacao, seguir `specs/001-niche-landing-system/spec.md`, `specs/002-floating-ai-sales-agent/spec.md` e `specs/spec-1-2-final-readiness-map.md`.

Referencias a acesso antecipado, beta, validacao de nicho ou formulario antigo foram substituidas pela venda do SaaS vertical por nicho, com consultor/agente de IA, planos, assinatura, WhatsApp e diagnostico de agente sob medida.

## Finalidade deste documento

Este é o handoff final para Codex + Speckit. Ele substitui documentos anteriores em caso de conflito.

## Decisão central

Construir um **sistema reutilizável de landing pages por nicho**, começando por `/pilates`.

Não construir uma página hardcoded apenas para Pilates.

A landing de Pilates deve captar clientes qualificados para o nicho Pilates, mas a arquitetura deve permitir adicionar `/fisioterapia`, `/estetica`, `/personal` e outros nichos por configuração.

## Produto

Agentes Pilates é a primeira landing para uma plataforma de agentes de IA operacionais.

Não é CRM, agenda, chatbot, automação genérica ou consultoria.

É um sistema de agentes que acompanha a rotina, identifica pendências e ajuda a equipe a agir.

Mensagem central:

> Você cuida dos alunos. Seus agentes cuidam do resto.

Headline:

> Reduza faltas, organize reposições e renove planos com agentes de IA para Pilates.

## Arquitetura

Estrutura recomendada:

```txt
app/
  pilates/
    page.tsx

components/
  landing/
    shared/
    sections/
    mockups/

data/
  landing/
    niches/
      pilates.ts
      types.ts

lib/
  landing/
    money-calculator.ts
    tracking.ts
```

## Blocos da landing

1. Header
2. Hero estilo Landbot
3. O que você quer resolver primeiro no seu studio?
4. Por que seu studio perde dinheiro sem perceber
5. Dinheiro na Mesa
6. Veja o que cada agente cuida no seu studio
7. Como os agentes trabalham juntos
8. Como funciona
9. Tudo que hoje fica espalhado passa a ser acompanhado pelos agentes
10. Feito para a rotina real de um studio de Pilates
11. Agente sob medida
12. Humano no controle
13. Acesso antecipado
14. Formulário de diagnóstico
15. FAQ
16. CTA final
17. Footer

## Interativos obrigatórios

Blocos 3, 4, 5 e 6 são interativos.

- Bloco 3: interação por dor.
- Bloco 4: interação por problema/diagnóstico.
- Bloco 5: calculadora Dinheiro na Mesa.
- Bloco 6: interação por agente.

## Agentes principais

1. Atendimento
2. Agenda
3. Vendas
4. Financeiro
5. Retenção
6. Gestão
7. Histórico/Evolução

Agente sob medida é camada de expansão, não oitavo agente principal.

## Multi-nicho

O conteúdo visível deve vir de `data/landing/niches/pilates.ts`.

Para criar outro nicho no futuro, deve ser possível adicionar outro arquivo de config e uma nova rota sem reescrever os componentes principais.

## Tracking

Todos os eventos precisam incluir `niche` e `sourcePage`.

## Qualidade esperada

- Visual próximo ao ritmo e estrutura da Rebookly.
- Hero e componentes interativos com padrão de interação da Landbot.
- Calculadora com lógica inspirada na Lufisio.
- Copy simples, sem jargão SaaS.
- Mobile excelente, sem overflow.
- Interações por toque.
- Vendas e Histórico/Evolução bem aproveitados.
