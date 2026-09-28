# Guided Conversation Fixtures

## Supported Pain Mapping

| Visitor prompt | Expected captured pain | Expected agents |
| --- | --- | --- |
| "Minhas reposicoes viraram uma bagunca" | `reposicoes` | `atendimento`, `agenda` |
| "Tenho alunos faltando demais" | `faltas` | `atendimento`, `agenda`, `retencao` |
| "Mensalidade atrasada fica esquecida" | `mensalidades_atrasadas` | `financeiro`, `atendimento` |
| "Muita gente faz experimental e nao fecha" | `interessados` | `vendas`, `atendimento` |
| "Alunos somem depois de algumas semanas" | `alunos_inativos` | `retencao`, `gestao` |
| "Historico e restricoes ficam espalhados" | `historico_evolucao` | `historico-evolucao`, `atendimento` |

## Required Checks

- The agent asks at most one consultative question.
- The agent does not ask for contact before intent exists.
- The agent avoids prohibited public terms.
- The agent keeps consultor-led plan recommendation as the primary path and offers checkout when the visitor says they are ready to start.
- The agent answers practical buying questions before returning to a CTA.
- The agent recommends the configured recommended/highest-value plan when the visitor describes multiple operational pains or asks for the complete system.
- Lower-plan suggestions appear only for explicit budget/narrow-scope requests, missing recommended-plan configuration or comparison after the recommended plan has been framed.
