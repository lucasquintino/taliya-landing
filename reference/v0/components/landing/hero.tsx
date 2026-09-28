"use client"

import { useState, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Button } from "@/components/ui/button"
import { ArrowRight, Sparkles, Bot, Check, Send } from "lucide-react"
import { cn } from "@/lib/utils"

const agentChips = [
  { id: "faltas", label: "Faltas" },
  { id: "reposicoes", label: "Reposições" },
  { id: "mensalidades", label: "Mensalidades" },
  { id: "inativos", label: "Alunos inativos" },
  { id: "experimentais", label: "Aulas experimentais" },
  { id: "historico", label: "Histórico do aluno" },
]

// Chat demo messages
const chatDemo = [
  { type: "user" as const, text: "Oi, não vou conseguir ir hoje. Posso repor?" },
  { type: "typing" as const },
  { type: "ai" as const, label: "Verificando agenda...", text: "Claro! Tenho vaga amanhã às 18h ou quinta às 7h. Qual prefere?" },
]

export function Hero() {
  const [selectedChips, setSelectedChips] = useState<string[]>([])
  const [chatStep, setChatStep] = useState(0)
  const [isTyping, setIsTyping] = useState(false)

  const toggleChip = (id: string) => {
    setSelectedChips((prev) =>
      prev.includes(id)
        ? prev.filter((c) => c !== id)
        : [...prev, id]
    )
  }

  // Auto-play chat demo
  useEffect(() => {
    const timers: NodeJS.Timeout[] = []
    
    // First message appears
    timers.push(setTimeout(() => setChatStep(1), 1500))
    
    // Typing indicator
    timers.push(setTimeout(() => {
      setIsTyping(true)
    }, 2500))
    
    // AI response
    timers.push(setTimeout(() => {
      setIsTyping(false)
      setChatStep(2)
    }, 4000))

    // Reset and loop
    timers.push(setTimeout(() => {
      setChatStep(0)
      setIsTyping(false)
    }, 9000))

    const loopInterval = setInterval(() => {
      setChatStep(0)
      setIsTyping(false)
      
      setTimeout(() => setChatStep(1), 1500)
      setTimeout(() => setIsTyping(true), 2500)
      setTimeout(() => {
        setIsTyping(false)
        setChatStep(2)
      }, 4000)
    }, 9000)

    return () => {
      timers.forEach(clearTimeout)
      clearInterval(loopInterval)
    }
  }, [])

  return (
    <section className="relative min-h-screen pt-28 md:pt-32 pb-16 md:pb-20 px-4 overflow-hidden">
      {/* Subtle background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 -left-32 w-64 h-64 bg-recovery/5 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 -right-32 w-64 h-64 bg-blue/5 rounded-full blur-3xl" />
      </div>

      <div className="relative max-w-6xl mx-auto">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
          {/* Left Content */}
          <div className="text-center lg:text-left">
            {/* Eyebrow */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="flex justify-center lg:justify-start mb-6"
            >
              <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-secondary border border-border text-sm font-medium text-muted-foreground">
                <Sparkles className="w-4 h-4 text-amber" />
                Para studios de Pilates
              </span>
            </motion.div>

            {/* Headline */}
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
              className="text-3xl sm:text-4xl md:text-5xl lg:text-[3.25rem] font-semibold text-foreground tracking-tight text-balance leading-[1.15]"
            >
              Reduza faltas, organize reposições e renove planos com{" "}
              <span className="text-recovery">agentes de IA</span>
            </motion.h1>

            {/* Subheadline */}
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="mt-5 md:mt-6 text-base md:text-lg text-muted-foreground max-w-xl mx-auto lg:mx-0 text-pretty leading-relaxed"
            >
              Enquanto você cuida dos alunos, seus agentes cuidam do WhatsApp, da agenda, das reposições e das cobranças.
            </motion.p>

            {/* CTA Buttons */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.3 }}
              className="mt-8 flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-3"
            >
              <Button
                size="lg"
                className="w-full sm:w-auto rounded-full px-6 md:px-8 h-12 md:h-14 text-sm md:text-base font-medium bg-foreground text-background hover:bg-foreground/90 shadow-lg shadow-foreground/10"
              >
                Quero meu diagnóstico gratuito
                <ArrowRight className="ml-2 w-4 h-4" />
              </Button>
              <Button
                size="lg"
                variant="ghost"
                className="w-full sm:w-auto rounded-full px-6 md:px-8 h-12 md:h-14 text-sm md:text-base font-medium text-foreground hover:bg-secondary"
              >
                Ver como funciona
              </Button>
            </motion.div>

            {/* Trust indicators */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5, delay: 0.5 }}
              className="mt-8 flex items-center justify-center lg:justify-start gap-4"
            >
              <div className="flex -space-x-2">
                {[1, 2, 3, 4].map((i) => (
                  <div
                    key={i}
                    className="w-8 h-8 rounded-full bg-secondary border-2 border-background flex items-center justify-center text-xs font-medium text-muted-foreground"
                  >
                    {String.fromCharCode(64 + i)}
                  </div>
                ))}
              </div>
              <p className="text-sm text-muted-foreground">
                <span className="font-medium text-foreground">+50 studios</span> já usam
              </p>
            </motion.div>
          </div>

          {/* Right - Interactive Chat Demo */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="relative"
          >
            {/* Phone Frame */}
            <div className="relative mx-auto max-w-[340px] lg:max-w-none">
              {/* Glow effect */}
              <div className="absolute -inset-4 bg-gradient-to-b from-recovery/20 via-transparent to-transparent rounded-[40px] blur-2xl opacity-50" />
              
              <div className="relative bg-[#111315] rounded-[32px] p-2 shadow-2xl border border-white/10">
                {/* Phone notch */}
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-24 h-6 bg-[#111315] rounded-b-2xl z-10" />
                
                {/* Screen */}
                <div className="bg-[#0b141a] rounded-[24px] overflow-hidden">
                  {/* WhatsApp Header */}
                  <div className="bg-[#1f2c33] px-4 py-3 flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-recovery/20 flex items-center justify-center">
                      <Bot className="w-5 h-5 text-recovery" />
                    </div>
                    <div className="flex-1">
                      <p className="font-medium text-sm text-white">Agente Pilates</p>
                      <p className="text-xs text-recovery">Online agora</p>
                    </div>
                    <div className="flex gap-4 text-gray-400">
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M15.9 14.3H15l-.3-.3c1-1.1 1.6-2.7 1.6-4.3 0-3.7-3-6.7-6.7-6.7S3 6 3 9.7s3 6.7 6.7 6.7c1.6 0 3.2-.6 4.3-1.6l.3.3v.8l5.1 5.1 1.5-1.5-5-5.2zm-6.2 0c-2.6 0-4.6-2.1-4.6-4.6s2.1-4.6 4.6-4.6 4.6 2.1 4.6 4.6-2 4.6-4.6 4.6z"/>
                      </svg>
                    </div>
                  </div>

                  {/* Chat Messages */}
                  <div className="p-4 min-h-[320px] space-y-3 bg-[url('/chat-bg.png')] bg-repeat">
                    {/* Time stamp */}
                    <div className="flex justify-center">
                      <span className="px-3 py-1 bg-[#1f2c33]/80 rounded-lg text-xs text-gray-400">
                        Hoje, 14:32
                      </span>
                    </div>

                    {/* User message */}
                    <AnimatePresence>
                      {chatStep >= 1 && (
                        <motion.div
                          initial={{ opacity: 0, y: 10, scale: 0.95 }}
                          animate={{ opacity: 1, y: 0, scale: 1 }}
                          exit={{ opacity: 0, scale: 0.95 }}
                          className="flex justify-end"
                        >
                          <div className="bg-[#005c4b] text-white rounded-2xl rounded-tr-sm px-4 py-2.5 max-w-[85%] shadow-sm">
                            <p className="text-sm">{chatDemo[0].text}</p>
                            <div className="flex items-center justify-end gap-1 mt-1">
                              <span className="text-[10px] text-white/60">14:32</span>
                              <Check className="w-3.5 h-3.5 text-blue-400" />
                            </div>
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>

                    {/* Typing indicator */}
                    <AnimatePresence>
                      {isTyping && (
                        <motion.div
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          exit={{ opacity: 0, y: -10 }}
                          className="flex justify-start"
                        >
                          <div className="bg-[#1f2c33] rounded-2xl rounded-tl-sm px-4 py-3 shadow-sm">
                            <div className="flex gap-1">
                              <motion.div
                                animate={{ opacity: [0.4, 1, 0.4] }}
                                transition={{ duration: 1, repeat: Infinity, delay: 0 }}
                                className="w-2 h-2 bg-gray-400 rounded-full"
                              />
                              <motion.div
                                animate={{ opacity: [0.4, 1, 0.4] }}
                                transition={{ duration: 1, repeat: Infinity, delay: 0.2 }}
                                className="w-2 h-2 bg-gray-400 rounded-full"
                              />
                              <motion.div
                                animate={{ opacity: [0.4, 1, 0.4] }}
                                transition={{ duration: 1, repeat: Infinity, delay: 0.4 }}
                                className="w-2 h-2 bg-gray-400 rounded-full"
                              />
                            </div>
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>

                    {/* AI response */}
                    <AnimatePresence>
                      {chatStep >= 2 && (
                        <motion.div
                          initial={{ opacity: 0, y: 10, scale: 0.95 }}
                          animate={{ opacity: 1, y: 0, scale: 1 }}
                          exit={{ opacity: 0, scale: 0.95 }}
                          className="flex justify-start"
                        >
                          <div className="bg-[#1f2c33] rounded-2xl rounded-tl-sm px-4 py-2.5 max-w-[85%] shadow-sm">
                            <div className="flex items-center gap-1.5 mb-1">
                              <Bot className="w-3 h-3 text-recovery" />
                              <span className="text-[10px] font-medium text-recovery">Agente IA</span>
                            </div>
                            <p className="text-sm text-gray-100">{chatDemo[2].text}</p>
                            <span className="text-[10px] text-white/40 mt-1 block">14:32</span>
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>

                    {/* Quick replies */}
                    <AnimatePresence>
                      {chatStep >= 2 && (
                        <motion.div
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: 0.3 }}
                          className="flex flex-wrap gap-2 pt-2"
                        >
                          <button className="px-3 py-1.5 bg-transparent border border-recovery/50 text-recovery text-xs rounded-full hover:bg-recovery/10 transition-colors">
                            Amanhã às 18h
                          </button>
                          <button className="px-3 py-1.5 bg-transparent border border-recovery/50 text-recovery text-xs rounded-full hover:bg-recovery/10 transition-colors">
                            Quinta às 7h
                          </button>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>

                  {/* Input bar */}
                  <div className="bg-[#1f2c33] px-3 py-2 flex items-center gap-2">
                    <div className="flex-1 bg-[#2a3942] rounded-full px-4 py-2 flex items-center">
                      <span className="text-sm text-gray-500">Mensagem</span>
                    </div>
                    <div className="w-10 h-10 bg-recovery rounded-full flex items-center justify-center">
                      <Send className="w-5 h-5 text-white" />
                    </div>
                  </div>
                </div>
              </div>

              {/* Floating badge */}
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.8 }}
                className="absolute -right-4 top-20 bg-card rounded-xl border border-border shadow-lg px-3 py-2 hidden lg:flex items-center gap-2"
              >
                <div className="w-8 h-8 rounded-full bg-recovery/20 flex items-center justify-center">
                  <Check className="w-4 h-4 text-recovery" />
                </div>
                <div>
                  <p className="text-xs font-medium text-foreground">Reposição agendada</p>
                  <p className="text-[10px] text-muted-foreground">Sem intervenção manual</p>
                </div>
              </motion.div>
            </div>
          </motion.div>
        </div>

        {/* Agent Selector - Below */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.6 }}
          className="mt-16 md:mt-20 max-w-2xl mx-auto"
        >
          <div className="bg-card rounded-2xl md:rounded-3xl border border-border p-5 md:p-8 shadow-sm">
            <p className="text-center text-sm font-medium text-muted-foreground mb-4 md:mb-5">
              Quero que meus agentes cuidem de...
            </p>
            
            <div className="flex flex-wrap justify-center gap-2">
              {agentChips.map((chip) => (
                <button
                  key={chip.id}
                  onClick={() => toggleChip(chip.id)}
                  className={cn(
                    "px-3 md:px-4 py-2 md:py-2.5 rounded-full text-xs md:text-sm font-medium transition-all duration-200",
                    selectedChips.includes(chip.id)
                      ? "bg-foreground text-background"
                      : "bg-secondary text-foreground hover:bg-secondary/80 border border-border"
                  )}
                >
                  {chip.label}
                </button>
              ))}
            </div>

            <div className="mt-5 md:mt-6 flex justify-center">
              <Button
                className={cn(
                  "rounded-full px-5 md:px-6 h-10 md:h-11 text-xs md:text-sm font-medium transition-all duration-200",
                  selectedChips.length > 0
                    ? "bg-recovery text-white hover:bg-recovery/90"
                    : "bg-secondary text-muted-foreground cursor-not-allowed"
                )}
                disabled={selectedChips.length === 0}
              >
                Começar diagnóstico
                <ArrowRight className="ml-2 w-4 h-4" />
              </Button>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
