"use client"

import { motion } from "framer-motion"
import { SectionHeader } from "./section-header"
import { MetricCard } from "./metric-card"
import { CTACard } from "./cta-card"
import { FAQAccordion } from "./faq-accordion"
import { FlowTimeline } from "./flow-timeline"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import {
  Users,
  TrendingUp,
  Clock,
  ArrowRight,
  MessageCircle,
  Calendar,
  Check,
  Sparkles,
} from "lucide-react"

const faqItems = [
  {
    question: "Preciso trocar meu sistema atual?",
    answer:
      "Não. Os agentes trabalham em paralelo ao que você já usa. Eles leem e reagem a eventos do WhatsApp, agenda e pagamentos, sem substituir suas ferramentas.",
  },
  {
    question: "Os agentes respondem sozinhos ou eu aprovo antes?",
    answer:
      "Você escolhe. Pode configurar para responder automaticamente, sugerir respostas para aprovação ou apenas notificar. O controle é seu.",
  },
  {
    question: "Funciona para studios pequenos?",
    answer:
      "Sim. Os agentes são especialmente úteis para studios pequenos onde o dono faz múltiplas funções. Quanto menos pessoas, mais valioso é o tempo automatizado.",
  },
  {
    question: "Quanto tempo leva para configurar?",
    answer:
      "O diagnóstico inicial leva 15 minutos. A configuração completa dos agentes é feita pela nossa equipe em até 48 horas.",
  },
]

const timelineSteps = [
  {
    icon: <MessageCircle className="w-5 h-5" />,
    title: "Aluno manda mensagem",
    description: "WhatsApp, SMS ou qualquer canal conectado",
    color: "bg-blue/10 text-blue",
  },
  {
    icon: <Sparkles className="w-5 h-5" />,
    title: "IA identifica a intenção",
    description: "Cancelamento, reposição, dúvida, renovação...",
    color: "bg-amber/10 text-amber",
  },
  {
    icon: <Calendar className="w-5 h-5" />,
    title: "Agente consulta contexto",
    description: "Agenda, histórico, plano, restrições...",
    color: "bg-purple/10 text-purple",
  },
  {
    icon: <Check className="w-5 h-5" />,
    title: "Ação executada ou sugerida",
    description: "Resposta automática ou aprovação manual",
    color: "bg-recovery/10 text-recovery",
  },
]

export function ComponentPatterns() {
  return (
    <section className="py-20 md:py-32 px-4">
      <div className="max-w-6xl mx-auto">
        <SectionHeader
          eyebrow="Padrões de Componentes"
          title="Biblioteca de UI para o restante da landing"
          description="Componentes reutilizáveis prontos para uso nas próximas seções."
        />

        <div className="mt-16 space-y-16">
          {/* Metric Cards */}
          <div>
            <h3 className="text-lg font-semibold text-foreground mb-6">
              Metric Cards
            </h3>
            <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <MetricCard
                label="Alunos ativos"
                value="127"
                trend="+12% este mês"
                trendUp
                icon={<Users className="w-5 h-5" />}
              />
              <MetricCard
                label="Taxa de retenção"
                value="94%"
                trend="+5% vs. média"
                trendUp
                icon={<TrendingUp className="w-5 h-5" />}
              />
              <MetricCard
                label="Tempo de resposta"
                value="< 2min"
                trend="-85% vs. manual"
                trendUp
                icon={<Clock className="w-5 h-5" />}
              />
              <MetricCard
                label="Recuperação"
                value="R$ 8.4k"
                trend="Este mês"
                trendUp
                icon={<TrendingUp className="w-5 h-5" />}
              />
            </div>
          </div>

          {/* Flow Timeline */}
          <div>
            <h3 className="text-lg font-semibold text-foreground mb-6">
              Flow/Timeline
            </h3>
            <div className="max-w-xl">
              <FlowTimeline steps={timelineSteps} />
            </div>
          </div>

          {/* CTA Cards */}
          <div>
            <h3 className="text-lg font-semibold text-foreground mb-6">
              CTA Cards
            </h3>
            <div className="grid md:grid-cols-2 gap-6">
              <CTACard
                title="Pronto para recuperar tempo e dinheiro?"
                description="Faça seu diagnóstico gratuito em 15 minutos."
                primaryAction={{ label: "Quero meu diagnóstico" }}
                secondaryAction={{ label: "Ver demonstração" }}
                variant="default"
              />
              <CTACard
                title="Seus agentes estão esperando"
                description="Comece hoje e veja resultados na primeira semana."
                primaryAction={{ label: "Começar agora" }}
                variant="dark"
              />
            </div>
          </div>

          {/* FAQ Accordion */}
          <div>
            <h3 className="text-lg font-semibold text-foreground mb-6">
              FAQ Accordion
            </h3>
            <div className="max-w-2xl">
              <FAQAccordion items={faqItems} />
            </div>
          </div>

          {/* Form Fields */}
          <div>
            <h3 className="text-lg font-semibold text-foreground mb-6">
              Form Fields
            </h3>
            <div className="max-w-md space-y-4">
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                className="bg-card rounded-2xl border border-border p-6"
              >
                <h4 className="font-medium text-foreground mb-4">
                  Agende seu diagnóstico
                </h4>
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="name" className="text-sm text-muted-foreground">
                      Nome completo
                    </Label>
                    <Input
                      id="name"
                      placeholder="Seu nome"
                      className="h-11 rounded-xl border-border bg-background"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="email" className="text-sm text-muted-foreground">
                      E-mail
                    </Label>
                    <Input
                      id="email"
                      type="email"
                      placeholder="seu@email.com"
                      className="h-11 rounded-xl border-border bg-background"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="studio" className="text-sm text-muted-foreground">
                      Nome do studio
                    </Label>
                    <Input
                      id="studio"
                      placeholder="Studio Pilates"
                      className="h-11 rounded-xl border-border bg-background"
                    />
                  </div>
                  <Button className="w-full h-11 rounded-xl bg-foreground text-background hover:bg-foreground/90">
                    Agendar diagnóstico
                    <ArrowRight className="ml-2 w-4 h-4" />
                  </Button>
                </div>
              </motion.div>
            </div>
          </div>

          {/* Agent Selector Pills */}
          <div>
            <h3 className="text-lg font-semibold text-foreground mb-6">
              Agent Selector Pills
            </h3>
            <div className="flex flex-wrap gap-2">
              {["Atendimento", "Agenda", "Vendas", "Financeiro", "Retenção", "Gestão", "Histórico"].map(
                (agent, i) => (
                  <motion.button
                    key={agent}
                    initial={{ opacity: 0, scale: 0.9 }}
                    whileInView={{ opacity: 1, scale: 1 }}
                    viewport={{ once: true }}
                    transition={{ delay: i * 0.05 }}
                    className={`px-4 py-2.5 rounded-full text-sm font-medium transition-all ${
                      i === 0
                        ? "bg-foreground text-background"
                        : "bg-secondary text-foreground hover:bg-secondary/80 border border-border"
                    }`}
                  >
                    {agent}
                  </motion.button>
                )
              )}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
