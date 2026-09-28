"use client"

import { useState, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { cn } from "@/lib/utils"
import { SectionHeader } from "./section-header"
import {
  Calendar,
  MessageCircle,
  RefreshCcw,
  CreditCard,
  UserX,
  Sparkles,
  Users,
  Bot,
  Check,
  Send,
  ArrowRight,
} from "lucide-react"

const problems = [
  {
    id: "faltas",
    title: "Reduzir faltas e cancelamentos",
    icon: <Calendar className="w-5 h-5" />,
    color: "bg-amber/10 text-amber border-amber/30",
    mockup: {
      title: "Agente Agenda",
      messages: [
        { from: "user", text: "Oi, não vou conseguir ir hoje. Consigo repor essa semana?", delay: 0.2 },
        { from: "ai", label: "Verificando agenda...", text: "Claro! Você ainda tem 1 reposição disponível. Tenho vaga amanhã às 18h ou quinta às 7h. Qual prefere?", delay: 0.8 },
      ],
      quickReplies: ["Amanhã às 18h", "Quinta às 7h"],
      result: "Reposição organizada em segundos",
    },
  },
  {
    id: "reposicoes",
    title: "Organizar reposições",
    icon: <RefreshCcw className="w-5 h-5" />,
    color: "bg-blue/10 text-blue border-blue/30",
    mockup: {
      title: "Agente Reposição",
      messages: [
        { from: "user", text: "Preciso remarcar minha aula de quarta para outro dia.", delay: 0.2 },
        { from: "ai", label: "Buscando horários...", text: "Entendi! Posso colocar você na terça às 18h, quinta às 19h ou sexta às 8h. Qual funciona melhor?", delay: 0.8 },
      ],
      quickReplies: ["Terça 18h", "Quinta 19h", "Sexta 8h"],
      result: "Reagendamento feito sem esforço",
    },
  },
  {
    id: "mensalidades",
    title: "Renovar planos e mensalidades",
    icon: <CreditCard className="w-5 h-5" />,
    color: "bg-purple/10 text-purple border-purple/30",
    mockup: {
      title: "Agente Financeiro",
      messages: [
        { from: "system", text: "Plano de Marina Silva vence em 5 dias", delay: 0.2 },
        { from: "ai", label: "Mensagem automática", text: "Oi Marina! Seu plano vence dia 15. Quer renovar com as mesmas condições ou gostaria de ver outras opções?", delay: 0.8 },
      ],
      quickReplies: ["Renovar igual", "Ver opções"],
      result: "Renovação antecipada garantida",
    },
  },
  {
    id: "inativos",
    title: "Reativar alunos inativos",
    icon: <UserX className="w-5 h-5" />,
    color: "bg-soft-red/10 text-soft-red border-soft-red/30",
    mockup: {
      title: "Agente Retenção",
      messages: [
        { from: "system", text: "Paula Costa inativa há 15 dias", delay: 0.2 },
        { from: "ai", label: "Mensagem de reativação", text: "Oi Paula! Faz duas semanas que não te vemos por aqui. Tá tudo bem? Se quiser, tenho horários disponíveis essa semana.", delay: 0.8 },
      ],
      quickReplies: ["Ver horários", "Preciso pausar"],
      result: "Aluno recuperado antes de cancelar",
    },
  },
  {
    id: "experimentais",
    title: "Converter aulas experimentais",
    icon: <Sparkles className="w-5 h-5" />,
    color: "bg-recovery/10 text-recovery border-recovery/30",
    mockup: {
      title: "Agente Vendas",
      messages: [
        { from: "system", text: "Carla fez aula experimental há 2 dias", delay: 0.2 },
        { from: "ai", label: "Follow-up automático", text: "Oi Carla! Como foi sua experiência na aula de segunda? Gostaria de conhecer nossos planos?", delay: 0.8 },
      ],
      quickReplies: ["Ver planos", "Agendar outra"],
      result: "Lead quente convertido em aluno",
    },
  },
  {
    id: "historico",
    title: "Acompanhar histórico e evolução",
    icon: <Users className="w-5 h-5" />,
    color: "bg-teal/10 text-teal border-teal/30",
    mockup: {
      title: "Agente Histórico",
      messages: [
        { from: "system", text: "Consulta: Roberto Lima", delay: 0.2 },
        { from: "ai", label: "Perfil do aluno", text: "Roberto, aluno desde Mar/23. Restrição: Hérnia lombar L4-L5. Foco: Core. Frequência: 85%. Evolução consistente nas últimas 12 aulas.", delay: 0.8 },
      ],
      quickReplies: ["Ver evolução", "Histórico completo"],
      result: "Contexto completo em segundos",
    },
  },
]

export function ProblemSolver() {
  const [selectedProblem, setSelectedProblem] = useState(problems[0].id)
  const [animationKey, setAnimationKey] = useState(0)

  const activeProblem = problems.find((p) => p.id === selectedProblem) || problems[0]

  // Reset animation when problem changes
  useEffect(() => {
    setAnimationKey((prev) => prev + 1)
  }, [selectedProblem])

  return (
    <section id="como-funciona" className="py-16 md:py-24 lg:py-32 px-4">
      <div className="max-w-6xl mx-auto">
        <SectionHeader
          eyebrow="Interativo"
          title="O que você quer resolver primeiro?"
          description="Selecione um problema e veja como seus agentes trabalham."
        />

        <div className="mt-12 md:mt-16 grid lg:grid-cols-2 gap-6 lg:gap-12">
          {/* Problem Selector */}
          <div className="space-y-2 md:space-y-3 order-2 lg:order-1">
            {problems.map((problem) => (
              <motion.button
                key={problem.id}
                onClick={() => setSelectedProblem(problem.id)}
                className={cn(
                  "w-full text-left p-3 md:p-4 rounded-xl md:rounded-2xl border transition-all duration-200",
                  selectedProblem === problem.id
                    ? "bg-card border-foreground/20 shadow-sm"
                    : "bg-transparent border-border hover:bg-card/50"
                )}
                whileHover={{ scale: 1.01 }}
                whileTap={{ scale: 0.99 }}
              >
                <div className="flex items-center gap-3 md:gap-4">
                  <div
                    className={cn(
                      "w-9 h-9 md:w-10 md:h-10 rounded-lg md:rounded-xl flex items-center justify-center transition-colors shrink-0",
                      selectedProblem === problem.id
                        ? "bg-foreground text-background"
                        : "bg-secondary text-foreground"
                    )}
                  >
                    {problem.icon}
                  </div>
                  <span
                    className={cn(
                      "text-sm md:text-base font-medium transition-colors flex-1",
                      selectedProblem === problem.id
                        ? "text-foreground"
                        : "text-muted-foreground"
                    )}
                  >
                    {problem.title}
                  </span>
                  {selectedProblem === problem.id && (
                    <ArrowRight className="w-4 h-4 text-muted-foreground shrink-0 hidden md:block" />
                  )}
                </div>
              </motion.button>
            ))}
          </div>

          {/* Dynamic Mockup - Phone Style */}
          <div className="lg:sticky lg:top-32 lg:self-start order-1 lg:order-2">
            <AnimatePresence mode="wait">
              <motion.div
                key={`${selectedProblem}-${animationKey}`}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
                className="relative mx-auto max-w-[340px] lg:max-w-[380px]"
              >
                {/* Phone Frame */}
                <div className="relative bg-[#111315] rounded-[28px] md:rounded-[32px] p-1.5 md:p-2 shadow-2xl border border-white/10">
                  {/* Screen */}
                  <div className="bg-[#0b141a] rounded-[22px] md:rounded-[24px] overflow-hidden">
                    {/* WhatsApp Header */}
                    <div className="bg-[#1f2c33] px-3 md:px-4 py-2.5 md:py-3 flex items-center gap-2.5 md:gap-3">
                      <div className="w-8 h-8 md:w-10 md:h-10 rounded-full bg-recovery/20 flex items-center justify-center">
                        <Bot className="w-4 h-4 md:w-5 md:h-5 text-recovery" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="font-medium text-xs md:text-sm text-white truncate">
                          {activeProblem.mockup.title}
                        </p>
                        <p className="text-[10px] md:text-xs text-recovery">Online agora</p>
                      </div>
                    </div>

                    {/* Chat Messages */}
                    <div className="p-3 md:p-4 min-h-[280px] md:min-h-[320px] space-y-2.5 md:space-y-3">
                      {/* Time stamp */}
                      <div className="flex justify-center">
                        <span className="px-2.5 py-0.5 md:px-3 md:py-1 bg-[#1f2c33]/80 rounded-lg text-[10px] md:text-xs text-gray-400">
                          Hoje, 14:32
                        </span>
                      </div>

                      {/* Messages */}
                      {activeProblem.mockup.messages.map((msg, i) => (
                        <motion.div
                          key={i}
                          initial={{ opacity: 0, y: 10, scale: 0.95 }}
                          animate={{ opacity: 1, y: 0, scale: 1 }}
                          transition={{ delay: msg.delay, duration: 0.3 }}
                          className={cn(
                            "flex",
                            msg.from === "user" ? "justify-end" : "justify-start"
                          )}
                        >
                          <div
                            className={cn(
                              "max-w-[85%] rounded-2xl px-3 md:px-4 py-2 md:py-2.5 shadow-sm",
                              msg.from === "user"
                                ? "bg-[#005c4b] text-white rounded-tr-sm"
                                : msg.from === "system"
                                ? "bg-amber/20 text-amber border border-amber/30"
                                : "bg-[#1f2c33] text-gray-100 rounded-tl-sm"
                            )}
                          >
                            {msg.from === "system" && (
                              <div className="flex items-center gap-1.5 mb-1">
                                <Bot className="w-3 h-3" />
                                <span className="text-[10px] font-medium">IA detectou</span>
                              </div>
                            )}
                            {msg.from === "ai" && msg.label && (
                              <div className="flex items-center gap-1.5 mb-1">
                                <Bot className="w-3 h-3 text-recovery" />
                                <span className="text-[10px] font-medium text-recovery">{msg.label}</span>
                              </div>
                            )}
                            <p className="text-xs md:text-sm">{msg.text}</p>
                            {msg.from === "user" && (
                              <div className="flex items-center justify-end gap-1 mt-1">
                                <span className="text-[9px] md:text-[10px] text-white/60">14:32</span>
                                <Check className="w-3 h-3 md:w-3.5 md:h-3.5 text-blue-400" />
                              </div>
                            )}
                          </div>
                        </motion.div>
                      ))}

                      {/* Quick Replies */}
                      {activeProblem.mockup.quickReplies && (
                        <motion.div
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: 1.2 }}
                          className="flex flex-wrap gap-1.5 md:gap-2 pt-1 md:pt-2"
                        >
                          {activeProblem.mockup.quickReplies.map((reply, i) => (
                            <button
                              key={i}
                              className="px-2.5 md:px-3 py-1 md:py-1.5 bg-transparent border border-recovery/50 text-recovery text-[10px] md:text-xs rounded-full hover:bg-recovery/10 transition-colors"
                            >
                              {reply}
                            </button>
                          ))}
                        </motion.div>
                      )}

                      {/* Result Badge */}
                      <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 1.5 }}
                        className="flex items-center gap-2 bg-recovery/20 text-recovery rounded-xl px-3 md:px-4 py-2 md:py-2.5 text-xs md:text-sm font-medium mt-3 md:mt-4"
                      >
                        <Check className="w-3.5 h-3.5 md:w-4 md:h-4 shrink-0" />
                        {activeProblem.mockup.result}
                      </motion.div>
                    </div>

                    {/* Input bar */}
                    <div className="bg-[#1f2c33] px-2 md:px-3 py-2 flex items-center gap-2">
                      <div className="flex-1 bg-[#2a3942] rounded-full px-3 md:px-4 py-1.5 md:py-2 flex items-center">
                        <span className="text-xs md:text-sm text-gray-500">Mensagem</span>
                      </div>
                      <div className="w-8 h-8 md:w-10 md:h-10 bg-recovery rounded-full flex items-center justify-center shrink-0">
                        <Send className="w-4 h-4 md:w-5 md:h-5 text-white" />
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>
            </AnimatePresence>
          </div>
        </div>
      </div>
    </section>
  )
}
