# Mapa da base e dos slots

| Slot/rota | Código existente | Decisão da migração |
|---|---|---|
| Home `/` | `app/page.tsx` | Hoje redireciona para `/pilates`; a spec 002 define a home pública Copiloto reutilizando a landing atual. |
| Landing antiga | `app/pilates/page.tsx`, `data/landing/niches/pilates.ts` | Preservar rota, metadata, config e experiência antiga durante esta migração. |
| Página de planos | `app/pilates/planos/page.tsx` | Não alterar nesta migração textual; destino legado continua uma decisão SEO pendente. |
| Composição e estados | `components/landing/NicheLandingPage.tsx` | Reutilizar. Manter layout e handlers nas etapas de copy. |
| Cabeçalho | `components/landing/shared/Header.tsx` | Atualizar apenas labels/copy já existentes. |
| Hero | `components/landing/sections/HeroSection.tsx` | Atualizar campos de texto e copy do mockup, mantendo composição. |
| Seletor | `components/landing/sections/IntentSelectorSection.tsx` | Usar slots existentes, sem mudar controles ou lógica. |
| Comparação | `components/landing/sections/ProblemDiagnosisSection.tsx` | Atualizar texto nos slots atuais; preservar controle e estado. |
| Como funciona | `components/landing/sections/HowItWorksSection.tsx` | Mapear os seis tópicos do JSON para os seis painéis atuais; preservar componente e interação. |
| Calculadora | `components/landing/sections/MoneyCalculatorSection.tsx`, `lib/landing/money-calculator.ts` | Não trocar por fluxos nem alterar cálculos nesta migração. S08 exige revisão semântica antes de qualquer alteração. |
| Demonstração | `components/landing/sections/AgentsDemoSection.tsx` | Atualizar textos dos slots existentes; não criar subtabs nem alterar a navegação existente. |
| Começar/vendas | `components/landing/sections/SalesStartSection.tsx` | Somente textos existentes; manter handlers e destinos. |
| FAQ | `components/landing/sections/FAQSection.tsx` | Substituir conteúdo textual usando o accordion existente; sem mudança de comportamento. |
| CTA/footer/flutuante | `FinalCTASection.tsx`, `FooterSection.tsx`, `shared/FloatingAiAttendant*` | Copy somente. Não alterar envio, destino ou conversa operacional nesta migração. |
| Mural S06 | Ainda não existe wrapper de seção confirmado | Única inserção autorizada. Na spec 008 selecionar primitivas de conversa já existentes, incluindo `WhatsAppConversationMockup` ou `AutonomousWhatsAppFlowMockup`, antes de decidir código adicional. |
| SEO transversal | `app/layout.tsx`, metadata de rotas, `app/robots.ts`, `app/sitemap.ts` ou equivalentes | Inspecionar os arquivos reais na spec 002 antes de modificar; não criar rotas de feature. |

## Composição atual verificada

`NicheLandingPage` renderiza Header → Hero → Intent Selector → Problem Diagnosis → How It Works → Money Calculator → Agents Demo → Sales Start → FAQ → Final CTA → Footer → Floating AI Attendant. A lista foi lida em `components/landing/NicheLandingPage.tsx`; não foi inferida do pacote.

## Conflitos para tratar na spec própria

- O pacote prevê uma faixa S02 e substituir a calculadora S08 por fluxos. As duas mudanças alteram composição ou comportamento e entram em conflito com o limite atual do usuário. Não implementar essas duas mudanças sem nova autorização.
- Os 39 subtipos S07 e comportamentos de formulários no pacote exigiriam interações que não estão garantidas pelo pedido atual. Specs podem mapear textos aos controles existentes, mas não criar controles novos.
- S11 não tem evidência para prova social; o padrão continua ausente.
- A cópia do mural é autorizada, mas seus estados e controles precisam ser limitados ao que for necessário para o próprio mural e aprovados na spec S06 antes da implementação.
