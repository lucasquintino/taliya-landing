"use client"

import { useState, useMemo } from "react"
import { motion } from "framer-motion"
import { cn } from "@/lib/utils"
import { SectionHeader } from "./section-header"
import { Slider } from "@/components/ui/slider"
import { Label } from "@/components/ui/label"
import {
  MessageCircle,
  Calendar,
  CreditCard,
  TrendingUp,
  Users,
  BarChart3,
  History,
  AlertCircle,
} from "lucide-react"

interface CalculatorInput {
  id: string
  label: string
  shortLabel: string
  defaultValue: number
  min: number
  max: number
  step: number
  suffix?: string
  prefix?: string
}

const inputs: CalculatorInput[] = [
  { id: "alunos", label: "Alunos ativos", shortLabel: "Alunos", defaultValue: 80, min: 10, max: 500, step: 5 },
  { id: "mensalidade", label: "Mensalidade média", shortLabel: "Mensalidade", defaultValue: 350, min: 100, max: 1000, step: 10, prefix: "R$" },
  { id: "faltas", label: "Faltas por semana", shortLabel: "Faltas/sem", defaultValue: 12, min: 0, max: 50, step: 1 },
  { id: "vagasTurma", label: "Turmas com vaga", shortLabel: "Vagas", defaultValue: 8, min: 0, max: 30, step: 1 },
  { id: "mensalidadesAtrasadas", label: "Mensalidades atrasadas", shortLabel: "Atrasadas", defaultValue: 6, min: 0, max: 30, step: 1 },
  { id: "planosVencendo", label: "Planos vencendo (30d)", shortLabel: "Vencendo", defaultValue: 10, min: 0, max: 50, step: 1 },
  { id: "inativos", label: "Inativos (30d)", shortLabel: "Inativos", defaultValue: 8, min: 0, max: 50, step: 1 },
  { id: "interessados", label: "Interessados/mês", shortLabel: "Leads", defaultValue: 20, min: 0, max: 100, step: 1 },
]

const agents = [
  { id: "atendimento", name: "Atendimento", icon: <MessageCircle className="w-3.5 h-3.5 md:w-4 md:h-4" />, color: "bg-blue/10 text-blue" },
  { id: "agenda", name: "Agenda", icon: <Calendar className="w-3.5 h-3.5 md:w-4 md:h-4" />, color: "bg-amber/10 text-amber" },
  { id: "vendas", name: "Vendas", icon: <TrendingUp className="w-3.5 h-3.5 md:w-4 md:h-4" />, color: "bg-recovery/10 text-recovery" },
  { id: "financeiro", name: "Financeiro", icon: <CreditCard className="w-3.5 h-3.5 md:w-4 md:h-4" />, color: "bg-purple/10 text-purple" },
  { id: "retencao", name: "Retenção", icon: <Users className="w-3.5 h-3.5 md:w-4 md:h-4" />, color: "bg-teal/10 text-teal" },
  { id: "gestao", name: "Gestão", icon: <BarChart3 className="w-3.5 h-3.5 md:w-4 md:h-4" />, color: "bg-soft-red/10 text-soft-red" },
  { id: "historico", name: "Histórico", icon: <History className="w-3.5 h-3.5 md:w-4 md:h-4" />, color: "bg-foreground/10 text-foreground" },
]

export function Calculator() {
  const [values, setValues] = useState<Record<string, number>>(
    inputs.reduce((acc, input) => ({ ...acc, [input.id]: input.defaultValue }), {})
  )

  const updateValue = (id: string, value: number) => {
    setValues((prev) => ({ ...prev, [id]: value }))
  }

  const calculations = useMemo(() => {
    const mensalidade = values.mensalidade
    const valorAula = mensalidade / 8
    
    const perdaFaltas = values.faltas * 4 * valorAula * 0.3
    const perdaVagas = values.vagasTurma * 4 * valorAula * 0.4
    const perdaMensalidades = values.mensalidadesAtrasadas * mensalidade * 0.2
    const perdaPlanos = values.planosVencendo * mensalidade * 0.15
    const perdaInativos = values.inativos * mensalidade * 0.5
    const perdaExperimentais = values.interessados * 0.2 * mensalidade * 3 * 0.3
    const custoHoras = 10 * 4 * 30

    const byAgent = {
      atendimento: Math.round(perdaFaltas * 0.3 + custoHoras * 0.2),
      agenda: Math.round(perdaFaltas * 0.4 + perdaVagas * 0.5),
      vendas: Math.round(perdaExperimentais + custoHoras * 0.1),
      financeiro: Math.round(perdaMensalidades + perdaPlanos * 0.3),
      retencao: Math.round(perdaInativos + perdaPlanos * 0.7),
      gestao: Math.round(custoHoras * 0.4 + perdaVagas * 0.3),
      historico: Math.round(custoHoras * 0.3 + perdaVagas * 0.2),
    }

    const total = Object.values(byAgent).reduce((a, b) => a + b, 0)

    return { total, byAgent }
  }, [values])

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value)
  }

  return (
    <section id="calculadora" className="py-16 md:py-24 lg:py-32 px-4">
      <div className="max-w-6xl mx-auto">
        <SectionHeader
          eyebrow="Calculadora"
          title="Quanto dinheiro está escapando?"
          description="Ajuste os números do seu studio e veja a estimativa de perdas."
        />

        <div className="mt-10 md:mt-16 grid lg:grid-cols-5 gap-6 lg:gap-12">
          {/* Inputs */}
          <div className="lg:col-span-3 space-y-4 md:space-y-6">
            <div className="grid grid-cols-2 gap-3 md:gap-6">
              {inputs.map((input, index) => (
                <motion.div
                  key={input.id}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.03 }}
                  className="space-y-2 md:space-y-3"
                >
                  <div className="flex items-center justify-between gap-2">
                    <Label
                      htmlFor={input.id}
                      className="text-xs md:text-sm font-medium text-muted-foreground truncate"
                    >
                      <span className="hidden sm:inline">{input.label}</span>
                      <span className="sm:hidden">{input.shortLabel}</span>
                    </Label>
                    <span className="text-xs md:text-sm font-semibold text-foreground tabular-nums shrink-0">
                      {input.prefix}
                      {values[input.id]}
                      {input.suffix}
                    </span>
                  </div>
                  <Slider
                    id={input.id}
                    value={[values[input.id]]}
                    onValueChange={([value]) => updateValue(input.id, value)}
                    min={input.min}
                    max={input.max}
                    step={input.step}
                    className="w-full"
                  />
                </motion.div>
              ))}
            </div>
          </div>

          {/* Results */}
          <div className="lg:col-span-2 lg:sticky lg:top-32 lg:self-start space-y-4 md:space-y-6">
            {/* Total */}
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              className="bg-dark-panel rounded-2xl md:rounded-3xl p-5 md:p-8 text-center"
            >
              <p className="text-xs md:text-sm font-medium text-gray-400 mb-1 md:mb-2">
                Estimativa de perdas mensais
              </p>
              <motion.p
                key={calculations.total}
                initial={{ scale: 1.1 }}
                animate={{ scale: 1 }}
                className="text-3xl sm:text-4xl md:text-5xl font-bold text-white"
              >
                {formatCurrency(calculations.total)}
              </motion.p>
              <p className="text-xs md:text-sm text-gray-400 mt-1 md:mt-2">
                em dinheiro na mesa
              </p>
            </motion.div>

            {/* By Agent */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2 }}
              className="bg-card rounded-xl md:rounded-2xl border border-border p-4 md:p-5 space-y-2 md:space-y-3"
            >
              <p className="text-xs md:text-sm font-medium text-muted-foreground mb-2 md:mb-4">
                Recuperação por agente
              </p>
              {agents.map((agent) => (
                <div
                  key={agent.id}
                  className="flex items-center gap-2 md:gap-3"
                >
                  <div
                    className={cn(
                      "w-7 h-7 md:w-8 md:h-8 rounded-lg flex items-center justify-center flex-shrink-0",
                      agent.color
                    )}
                  >
                    {agent.icon}
                  </div>
                  <span className="flex-1 text-xs md:text-sm text-foreground truncate">
                    {agent.name}
                  </span>
                  <span className="text-xs md:text-sm font-semibold text-foreground tabular-nums">
                    {formatCurrency(calculations.byAgent[agent.id as keyof typeof calculations.byAgent])}
                  </span>
                </div>
              ))}
            </motion.div>

            {/* Disclaimer */}
            <motion.div
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true }}
              transition={{ delay: 0.3 }}
              className="flex items-start gap-2 md:gap-3 p-3 md:p-4 bg-secondary rounded-lg md:rounded-xl"
            >
              <AlertCircle className="w-3.5 h-3.5 md:w-4 md:h-4 text-muted-foreground flex-shrink-0 mt-0.5" />
              <p className="text-[10px] md:text-xs text-muted-foreground leading-relaxed">
                Estimativa simples. O valor real depende da rotina do studio.
              </p>
            </motion.div>
          </div>
        </div>
      </div>
    </section>
  )
}
