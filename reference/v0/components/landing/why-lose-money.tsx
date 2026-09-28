"use client"

import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { cn } from "@/lib/utils"
import { SectionHeader } from "./section-header"
import {
  Brain,
  Unplug,
  TrendingDown,
  ArrowRight,
  Check,
  X,
  AlertTriangle,
} from "lucide-react"

const problems = [
  {
    id: "memoria",
    title: "Tudo depende da memória da equipe",
    shortTitle: "Depende da memória",
    icon: <Brain className="w-4 h-4 md:w-5 md:h-5" />,
    description: "Faltas, reposições e cobranças ficam espalhados entre WhatsApp, planilha e cabeça da recepção.",
    before: {
      title: "Sem agentes",
      items: ["Reposições esquecidas", "Cobranças atrasadas", "Alunos sem retorno", "Informações perdidas"],
    },
    after: {
      title: "Com agentes",
      items: ["Tudo registrado", "Lembretes automáticos", "Ninguém esquecido", "Histórico completo"],
    },
    result: "Menos dependência da memória",
    color: "text-amber",
    bgColor: "bg-amber/10",
  },
  {
    id: "separados",
    title: "WhatsApp, agenda e cobrança ficam separados",
    shortTitle: "Sistemas separados",
    icon: <Unplug className="w-4 h-4 md:w-5 md:h-5" />,
    description: "Aluno cancela no WhatsApp, mas agenda não reage. Plano vence, mas ninguém chama.",
    before: {
      title: "Sem agentes",
      items: ["Sistemas desconectados", "Ações manuais", "Atrasos na resposta", "Oportunidades perdidas"],
    },
    after: {
      title: "Com agentes",
      items: ["Tudo conectado", "Ações automáticas", "Resposta instantânea", "Evento vira ação"],
    },
    result: "Eventos viram ações",
    color: "text-blue",
    bgColor: "bg-blue/10",
  },
  {
    id: "percepcao",
    title: "Você só percebe a perda quando o mês fecha",
    shortTitle: "Perda invisível",
    icon: <TrendingDown className="w-4 h-4 md:w-5 md:h-5" />,
    description: "Vaga ficou vazia, mensalidade atrasou, aluno sumiu e interessado esfriou.",
    before: {
      title: "Sem agentes",
      items: ["Perdas invisíveis", "Decisões reativas", "Surpresas no fechamento", "Prejuízo recorrente"],
    },
    after: {
      title: "Com agentes",
      items: ["Alertas tempo real", "Decisões proativas", "Visibilidade constante", "Ação preventiva"],
    },
    result: "Saiba onde agir antes do prejuízo",
    color: "text-soft-red",
    bgColor: "bg-soft-red/10",
  },
]

export function WhyLoseMoney() {
  const [selectedProblem, setSelectedProblem] = useState(problems[0].id)

  const activeProblem = problems.find((p) => p.id === selectedProblem) || problems[0]

  return (
    <section className="py-16 md:py-24 lg:py-32 px-4 bg-secondary">
      <div className="max-w-6xl mx-auto">
        <SectionHeader
          eyebrow="Diagnóstico"
          title="Por que seu studio perde dinheiro"
          description="3 padrões que drenam receita silenciosamente."
        />

        <div className="mt-10 md:mt-16 grid lg:grid-cols-2 gap-6 lg:gap-12">
          {/* Problem Selector */}
          <div className="space-y-3 md:space-y-4 order-2 lg:order-1">
            {problems.map((problem, index) => (
              <motion.button
                key={problem.id}
                onClick={() => setSelectedProblem(problem.id)}
                className={cn(
                  "w-full text-left rounded-xl md:rounded-2xl border transition-all duration-200 overflow-hidden",
                  selectedProblem === problem.id
                    ? "bg-card border-foreground/20 shadow-md"
                    : "bg-card/50 border-border hover:bg-card"
                )}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
              >
                <div className="p-4 md:p-5">
                  <div className="flex items-start gap-3 md:gap-4">
                    <div
                      className={cn(
                        "w-9 h-9 md:w-10 md:h-10 rounded-lg md:rounded-xl flex items-center justify-center flex-shrink-0",
                        selectedProblem === problem.id
                          ? `${problem.bgColor} ${problem.color}`
                          : "bg-secondary text-foreground"
                      )}
                    >
                      {problem.icon}
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3
                        className={cn(
                          "font-medium transition-colors text-sm md:text-base",
                          selectedProblem === problem.id
                            ? "text-foreground"
                            : "text-muted-foreground"
                        )}
                      >
                        <span className="hidden sm:inline">{problem.title}</span>
                        <span className="sm:hidden">{problem.shortTitle}</span>
                      </h3>
                      <AnimatePresence>
                        {selectedProblem === problem.id && (
                          <motion.p
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: "auto" }}
                            exit={{ opacity: 0, height: 0 }}
                            className="mt-1.5 md:mt-2 text-xs md:text-sm text-muted-foreground leading-relaxed"
                          >
                            {problem.description}
                          </motion.p>
                        )}
                      </AnimatePresence>
                    </div>
                  </div>
                </div>
              </motion.button>
            ))}
          </div>

          {/* Before/After Visual */}
          <div className="lg:sticky lg:top-32 lg:self-start order-1 lg:order-2">
            <AnimatePresence mode="wait">
              <motion.div
                key={selectedProblem}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
                className="space-y-3 md:space-y-4"
              >
                {/* Before Card */}
                <div className="bg-card rounded-xl md:rounded-2xl border border-border p-4 md:p-6 shadow-sm">
                  <div className="flex items-center gap-2 mb-3 md:mb-4">
                    <div className="w-7 h-7 md:w-8 md:h-8 rounded-lg bg-soft-red/10 flex items-center justify-center">
                      <AlertTriangle className="w-3.5 h-3.5 md:w-4 md:h-4 text-soft-red" />
                    </div>
                    <span className="font-medium text-foreground text-sm md:text-base">
                      {activeProblem.before.title}
                    </span>
                  </div>
                  <div className="space-y-2 md:space-y-3">
                    {activeProblem.before.items.map((item, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.1 + index * 0.05 }}
                        className="flex items-center gap-2 md:gap-3 text-xs md:text-sm text-muted-foreground"
                      >
                        <X className="w-3.5 h-3.5 md:w-4 md:h-4 text-soft-red flex-shrink-0" />
                        {item}
                      </motion.div>
                    ))}
                  </div>
                </div>

                {/* Arrow */}
                <div className="flex justify-center">
                  <div className="w-8 h-8 md:w-10 md:h-10 rounded-full bg-secondary border border-border flex items-center justify-center">
                    <ArrowRight className="w-4 h-4 md:w-5 md:h-5 text-muted-foreground rotate-90" />
                  </div>
                </div>

                {/* After Card */}
                <div className="bg-card rounded-xl md:rounded-2xl border border-recovery/30 p-4 md:p-6 shadow-sm">
                  <div className="flex items-center gap-2 mb-3 md:mb-4">
                    <div className="w-7 h-7 md:w-8 md:h-8 rounded-lg bg-recovery/10 flex items-center justify-center">
                      <Check className="w-3.5 h-3.5 md:w-4 md:h-4 text-recovery" />
                    </div>
                    <span className="font-medium text-foreground text-sm md:text-base">
                      {activeProblem.after.title}
                    </span>
                  </div>
                  <div className="space-y-2 md:space-y-3">
                    {activeProblem.after.items.map((item, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.3 + index * 0.05 }}
                        className="flex items-center gap-2 md:gap-3 text-xs md:text-sm text-foreground"
                      >
                        <Check className="w-3.5 h-3.5 md:w-4 md:h-4 text-recovery flex-shrink-0" />
                        {item}
                      </motion.div>
                    ))}
                  </div>
                </div>

                {/* Result Badge */}
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.5 }}
                  className={cn(
                    "rounded-xl md:rounded-2xl p-3 md:p-4 text-center font-medium text-sm",
                    activeProblem.bgColor,
                    activeProblem.color
                  )}
                >
                  {activeProblem.result}
                </motion.div>
              </motion.div>
            </AnimatePresence>
          </div>
        </div>
      </div>
    </section>
  )
}
