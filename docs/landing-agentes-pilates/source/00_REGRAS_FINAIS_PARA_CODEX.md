# Regras finais para Codex + Speckit

## Atualizacao comercial posterior

Este documento e legado para decisoes comerciais que conflitarem com as specs atuais. Para implementacao, seguir `specs/001-niche-landing-system/spec.md`, `specs/002-floating-ai-sales-agent/spec.md` e `specs/spec-1-2-final-readiness-map.md`.

Referencias a acesso antecipado, beta, validacao de nicho ou formulario antigo foram substituidas pela venda do SaaS vertical por nicho, com consultor/agente de IA, planos, assinatura, WhatsApp e diagnostico de agente sob medida.

Este arquivo sobrescreve qualquer decisão anterior em caso de conflito.

## Decisão final

Não estamos construindo uma landing única para validar qual nicho escolher.

Estamos construindo um **sistema reutilizável de landing pages por nicho**, onde cada landing é específica e capta clientes qualificados daquele nicho.

A primeira landing é **Pilates**, mas a arquitetura deve suportar futuras páginas como:

- `/pilates`
- `/fisioterapia`
- `/estetica`
- `/personal`

## Regra principal

Pilates é a primeira implementação, não o produto inteiro.

Não hardcode o conteúdo de Pilates diretamente nos componentes. Use componentes reutilizáveis e conteúdo vindo de arquivos de configuração por nicho.

## Arquitetura esperada

Criar estrutura data-driven:

```txt
data/landing/niches/
  pilates.ts
  types.ts
```

Preparar para adicionar futuramente:

```txt
data/landing/niches/
  fisioterapia.ts
  estetica.ts
  personal.ts
```

Componentes devem ser reutilizáveis:

- HeroSection
- IntentSelectorSection
- ProblemDiagnosisSection
- MoneyCalculatorSection
- AgentsDemoSection
- AgentWorkflowSection
- HowItWorksSection
- CoverageSection
- NicheSpecificSection
- CustomAgentSection
- HumanControlSection
- EarlyAccessSection
- DiagnosisFormSection
- FAQSection
- FinalCTASection
- Footer

## Landing de Pilates

A rota inicial deve ser `/pilates`.

A landing de Pilates deve parecer 100% feita para Pilates, usando termos como:

- studio
- alunos
- turmas
- presença
- reposição
- mensalidades
- planos vencendo
- alunos inativos
- histórico/evolução
- restrições
- observações

Não mostrar ao visitante a separação entre core, comum e específico. Tudo deve parecer parte natural da solução para Pilates.

## Formulário

O formulário deve capturar automaticamente:

```ts
niche: "pilates"
sourcePage: "/pilates"
```

Campos mínimos:

- Nome
- WhatsApp
- Nome do studio
- Cidade/Estado
- Quantos alunos ativos você tem?
- Qual sua maior dor hoje?
- Você usa algum sistema hoje?
- Existe alguma rotina específica que você gostaria que um agente cuidasse?
- Tem interesse em acesso antecipado?

## Eventos

Criar estrutura de tracking mesmo que inicialmente seja `console.log`.

Todos os eventos devem incluir o nicho.

Eventos:

- page_view_niche
- cta_click
- pain_selected
- agent_selected
- calculator_started
- calculator_result_updated
- form_started
- form_submitted
- early_access_clicked
- custom_agent_interest_clicked

Payload mínimo:

```ts
{
  niche: "pilates",
  sourcePage: "/pilates",
  eventName: "...",
  metadata: {}
}
```

## Agentes

Os 7 agentes principais são:

1. Atendimento
2. Agenda
3. Vendas
4. Financeiro
5. Retenção
6. Gestão
7. Histórico/Evolução

Agente sob medida não é o oitavo agente principal. Ele é a camada de expansão do sistema.

## Referências

- Rebookly: estrutura, ritmo visual, narrativa de dinheiro recuperável e scroll.
- Landbot: hero textual e componentes interativos.
- Lufisio: lógica da calculadora e contexto Pilates/Fisio.

Não copiar marcas, textos, assets, screenshots ou identidade visual literal.

## Regra final

A implementação deve entregar a landing `/pilates` agora, mas nascer como um motor reutilizável para múltiplas landings por nicho.
