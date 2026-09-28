"use client"

import { Header } from "@/components/landing/header"
import { Hero } from "@/components/landing/hero"
import { ProblemSolver } from "@/components/landing/problem-solver"
import { WhyLoseMoney } from "@/components/landing/why-lose-money"
import { Calculator } from "@/components/landing/calculator"
import { AgentsShowcase } from "@/components/landing/agents-showcase"
import { FAQAccordion } from "@/components/landing/faq-accordion"
import { CTACard } from "@/components/landing/cta-card"

export default function HomePage() {
  return (
    <main className="min-h-screen bg-background">
      <Header />
      
      {/* Hero Section */}
      <Hero />
      
      {/* Interactive Problem Solver */}
      <ProblemSolver />
      
      {/* Why Studios Lose Money */}
      <WhyLoseMoney />
      
      {/* Calculator */}
      <Calculator />
      
      {/* Agents Showcase */}
      <AgentsShowcase />
      
      {/* FAQ */}
      <FAQAccordion />
      
      {/* Final CTA */}
      <section className="py-16 md:py-20 px-4">
        <div className="max-w-4xl mx-auto">
          <CTACard
            title="Pronto para parar de perder dinheiro?"
            description="Faça seu diagnóstico gratuito e descubra quanto você pode recuperar."
            primaryAction={{ label: "Quero meu diagnóstico gratuito" }}
            secondaryAction={{ label: "Falar com especialista" }}
            variant="dark"
          />
        </div>
      </section>
      
      {/* Footer */}
      <footer className="py-8 md:py-12 px-4 border-t border-border">
        <div className="max-w-6xl mx-auto">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4 md:gap-6">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 md:w-8 md:h-8 rounded-lg bg-foreground flex items-center justify-center">
                <span className="text-background font-bold text-xs md:text-sm">AP</span>
              </div>
              <span className="font-semibold text-foreground text-sm md:text-base">Agentes Pilates</span>
            </div>
            <p className="text-xs md:text-sm text-muted-foreground text-center">
              2024 Agentes Pilates. Todos os direitos reservados.
            </p>
            <div className="flex items-center gap-4 md:gap-6">
              <a href="#" className="text-xs md:text-sm text-muted-foreground hover:text-foreground transition-colors">
                Termos
              </a>
              <a href="#" className="text-xs md:text-sm text-muted-foreground hover:text-foreground transition-colors">
                Privacidade
              </a>
              <a href="#" className="text-xs md:text-sm text-muted-foreground hover:text-foreground transition-colors">
                Contato
              </a>
            </div>
          </div>
        </div>
      </footer>
    </main>
  )
}
