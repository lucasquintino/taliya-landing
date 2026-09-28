"use client"

import { useState, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { cn } from "@/lib/utils"
import { SectionHeader } from "./section-header"
import {
  MessageCircle,
  Calendar,
  TrendingUp,
  CreditCard,
  Users,
  BarChart3,
  History,
  Sparkles,
  Bot,
  Check,
  Send,
  Bell,
} from "lucide-react"

const coreAgents = [
  {
    id: "atendimento",
    name: "Atendimento",
    icon: <MessageCircle className="w-4 h-4 md:w-5 md:h-5" />,
    color: "bg-blue/10 text-blue",
    borderColor: "border-blue/30",
    pain: "Mensagens não respondidas, respostas demoradas",
    does: "Responde WhatsApp automaticamente e identifica intenções",
    mockup: {
      messages: [
        { from: "user", text: "Oi, quanto custa a aula de Pilates?" },
        { from: "ai", label: "Consulta de preço", text: "Nosso plano mensal 2x/semana é R$350. Quer agendar uma aula experimental gratuita?" },
      ],
      quickReplies: ["Agendar aula", "Ver planos"],
    },
    result: "Resposta em segundos",
  },
  {
    id: "agenda",
    name: "Agenda",
    icon: <Calendar className="w-4 h-4 md:w-5 md:h-5" />,
    color: "bg-amber/10 text-amber",
    borderColor: "border-amber/30",
    pain: "Faltas não comunicadas, horários vazios",
    does: "Monitora cancelamentos e preenche vagas automaticamente",
    mockup: {
      messages: [
        { from: "system", text: "Cancelamento: Turma 18h - Maria" },
        { from: "ai", label: "Ação automática", text: "Marina da lista de espera foi convidada. Vaga preenchida!" },
      ],
      quickReplies: ["Ver turma", "Lista espera"],
    },
    result: "Vaga preenchida automaticamente",
  },
  {
    id: "vendas",
    name: "Vendas",
    icon: <TrendingUp className="w-4 h-4 md:w-5 md:h-5" />,
    color: "bg-recovery/10 text-recovery",
    borderColor: "border-recovery/30",
    pain: "Leads esfriam, experimentais não fecham",
    does: "Acompanha interessados e faz follow-up automático",
    mockup: {
      messages: [
        { from: "system", text: "Carla fez experimental há 2 dias" },
        { from: "ai", label: "Follow-up", text: "Oi Carla! Como foi sua experiência? Posso te apresentar nossos planos?" },
      ],
      quickReplies: ["Ver planos", "Outra aula"],
    },
    result: "Taxa de conversão 2x maior",
  },
  {
    id: "financeiro",
    name: "Financeiro",
    icon: <CreditCard className="w-4 h-4 md:w-5 md:h-5" />,
    color: "bg-purple/10 text-purple",
    borderColor: "border-purple/30",
    pain: "Mensalidades atrasadas, renovações esquecidas",
    does: "Monitora vencimentos e envia lembretes automáticos",
    mockup: {
      messages: [
        { from: "system", text: "8 mensalidades vencem em 5 dias" },
        { from: "ai", label: "Lembretes enviados", text: "Lembretes automáticos enviados. 6 de 8 já renovaram!" },
      ],
      quickReplies: ["Ver pendentes", "Histórico"],
    },
    result: "Inadimplência -40%",
  },
  {
    id: "retencao",
    name: "Retenção",
    icon: <Users className="w-4 h-4 md:w-5 md:h-5" />,
    color: "bg-teal/10 text-teal",
    borderColor: "border-teal/30",
    pain: "Alunos sumindo, cancelamentos inesperados",
    does: "Detecta alunos em risco e envia mensagens personalizadas",
    mockup: {
      messages: [
        { from: "system", text: "Paula inativa há 12 dias" },
        { from: "ai", label: "Reativação", text: "Oi Paula! Faz um tempo que não te vemos. Reservei um horário especial pra você!" },
      ],
      quickReplies: ["Aceitar", "Ver horários"],
    },
    result: "Aluno recuperado",
  },
  {
    id: "gestao",
    name: "Gestão",
    icon: <BarChart3 className="w-4 h-4 md:w-5 md:h-5" />,
    color: "bg-soft-red/10 text-soft-red",
    borderColor: "border-soft-red/30",
    pain: "Falta de visibilidade, decisões no escuro",
    does: "Consolida métricas e alerta anomalias",
    mockup: {
      type: "metrics",
      items: [
        { label: "Faltas", value: "↓ 23%", trend: "down" },
        { label: "Ocupação", value: "↑ 87%", trend: "up" },
        { label: "Renovações", value: "↑ 12%", trend: "up" },
      ],
    },
    result: "Decisões baseadas em dados",
  },
  {
    id: "historico",
    name: "Histórico",
    icon: <History className="w-4 h-4 md:w-5 md:h-5" />,
    color: "bg-foreground/10 text-foreground",
    borderColor: "border-foreground/30",
    pain: "Perfil do aluno espalhado, restrições esquecidas",
    does: "Centraliza histórico e acompanha objetivos",
    mockup: {
      type: "profile",
      student: {
        name: "Roberto Lima",
        initials: "RL",
        since: "Mar 2023",
        restriction: "Hérnia L4-L5",
        goal: "Fortalecimento",
        frequency: "85%",
      },
    },
    result: "Contexto em segundos",
  },
]

const expansionAgent = {
  id: "sobmedida",
  name: "Sob Medida",
  icon: <Sparkles className="w-4 h-4 md:w-5 md:h-5" />,
  color: "bg-gradient-to-br from-blue/10 to-purple/10 text-blue",
  borderColor: "border-blue/30",
  pain: "Necessidades específicas do seu studio",
  does: "Agentes personalizados para qualquer processo",
  mockup: {
    type: "custom",
    examples: [
      "Pós-cirúrgico",
      "Integração sistemas",
      "Relatórios custom",
      "Fluxos específicos",
    ],
  },
  result: "Automação sob medida",
}

export function AgentsShowcase() {
  const [selectedAgent, setSelectedAgent] = useState(coreAgents[0].id)
  const [animationKey, setAnimationKey] = useState(0)

  const activeAgent = [...coreAgents, expansionAgent].find((a) => a.id === selectedAgent) || coreAgents[0]

  useEffect(() => {
    setAnimationKey((prev) => prev + 1)
  }, [selectedAgent])

  return (
    <section id="agentes" className="py-16 md:py-24 lg:py-32 px-4 bg-secondary">
      <div className="max-w-6xl mx-auto">
        <SectionHeader
          eyebrow="7 Agentes + Expansão"
          title="Veja seus agentes em ação"
          description="Cada agente resolve um problema específico do seu studio."
        />

        <div className="mt-12 md:mt-16 grid lg:grid-cols-2 gap-6 lg:gap-12">
          {/* Agent Selector */}
          <div className="space-y-4 order-2 lg:order-1">
            <p className="text-xs md:text-sm font-medium text-muted-foreground">
              Agentes principais
            </p>
            
            {/* Mobile: Horizontal scroll */}
            <div className="flex lg:hidden gap-2 overflow-x-auto pb-2 -mx-4 px-4 scrollbar-hide">
              {coreAgents.map((agent) => (
                <button
                  key={agent.id}
                  onClick={() => setSelectedAgent(agent.id)}
                  className={cn(
                    "flex items-center gap-2 px-3 py-2 rounded-xl border whitespace-nowrap transition-all shrink-0",
                    selectedAgent === agent.id
                      ? `bg-card ${agent.borderColor} shadow-sm`
                      : "bg-card/50 border-border"
                  )}
                >
                  <div className={cn("w-7 h-7 rounded-lg flex items-center justify-center", agent.color)}>
                    {agent.icon}
                  </div>
                  <span className={cn("text-sm font-medium", selectedAgent === agent.id ? "text-foreground" : "text-muted-foreground")}>
                    {agent.name}
                  </span>
                </button>
              ))}
            </div>

            {/* Desktop: Grid */}
            <div className="hidden lg:grid grid-cols-2 gap-2">
              {coreAgents.map((agent) => (
                <motion.button
                  key={agent.id}
                  onClick={() => setSelectedAgent(agent.id)}
                  className={cn(
                    "text-left p-3 rounded-xl border transition-all duration-200",
                    selectedAgent === agent.id
                      ? `bg-card ${agent.borderColor} shadow-sm`
                      : "bg-card/50 border-border hover:bg-card"
                  )}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <div className="flex items-center gap-3">
                    <div className={cn("w-9 h-9 rounded-lg flex items-center justify-center", agent.color)}>
                      {agent.icon}
                    </div>
                    <span className={cn("text-sm font-medium", selectedAgent === agent.id ? "text-foreground" : "text-muted-foreground")}>
                      {agent.name}
                    </span>
                  </div>
                </motion.button>
              ))}
            </div>

            {/* Expansion Agent */}
            <div className="pt-2 md:pt-4">
              <p className="text-xs md:text-sm font-medium text-muted-foreground mb-2 md:mb-3">
                Camada de expansão
              </p>
              <motion.button
                onClick={() => setSelectedAgent(expansionAgent.id)}
                className={cn(
                  "w-full text-left p-3 md:p-4 rounded-xl border transition-all duration-200",
                  selectedAgent === expansionAgent.id
                    ? `bg-card ${expansionAgent.borderColor} shadow-sm`
                    : "bg-card/50 border-border hover:bg-card"
                )}
                whileHover={{ scale: 1.01 }}
                whileTap={{ scale: 0.99 }}
              >
                <div className="flex items-center gap-3">
                  <div className={cn("w-9 h-9 md:w-10 md:h-10 rounded-xl flex items-center justify-center", expansionAgent.color)}>
                    {expansionAgent.icon}
                  </div>
                  <div className="min-w-0">
                    <span className={cn("font-medium text-sm md:text-base block", selectedAgent === expansionAgent.id ? "text-foreground" : "text-muted-foreground")}>
                      {expansionAgent.name}
                    </span>
                    <p className="text-xs text-muted-foreground truncate">
                      Agentes personalizados
                    </p>
                  </div>
                </div>
              </motion.button>
            </div>
          </div>

          {/* Dynamic Mockup */}
          <div className="lg:sticky lg:top-32 lg:self-start order-1 lg:order-2">
            <AnimatePresence mode="wait">
              <motion.div
                key={`${selectedAgent}-${animationKey}`}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
                className="bg-card rounded-2xl border border-border overflow-hidden shadow-sm"
              >
                {/* Header */}
                <div className="p-4 md:p-5 border-b border-border">
                  <div className="flex items-center gap-3 mb-2 md:mb-3">
                    <div className={cn("w-9 h-9 md:w-10 md:h-10 rounded-xl flex items-center justify-center", activeAgent.color)}>
                      {activeAgent.icon}
                    </div>
                    <div>
                      <h3 className="font-semibold text-foreground text-sm md:text-base">
                        Agente {activeAgent.name}
                      </h3>
                    </div>
                  </div>
                  <p className="text-xs md:text-sm text-muted-foreground">
                    <span className="font-medium text-soft-red">Problema:</span> {activeAgent.pain}
                  </p>
                  <p className="text-xs md:text-sm text-muted-foreground mt-1">
                    <span className="font-medium text-recovery">Solução:</span> {activeAgent.does}
                  </p>
                </div>

                {/* Mockup Content */}
                <div className="p-4 md:p-5 min-h-[220px] md:min-h-[260px]">
                  {/* WhatsApp style mockup */}
                  {activeAgent.mockup.messages && (
                    <div className="bg-dark-panel rounded-xl p-3 md:p-4 space-y-2 md:space-y-3">
                      {activeAgent.mockup.messages.map((msg: any, i: number) => (
                        <motion.div
                          key={i}
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: i * 0.2 }}
                          className={cn("flex", msg.from === "user" ? "justify-end" : "justify-start")}
                        >
                          <div
                            className={cn(
                              "max-w-[85%] rounded-2xl px-3 md:px-4 py-2 md:py-2.5 text-xs md:text-sm",
                              msg.from === "user"
                                ? "bg-[#005c4b] text-white rounded-tr-sm"
                                : msg.from === "system"
                                ? "bg-amber/20 text-amber border border-amber/30"
                                : "bg-[#1f2c33] text-gray-100 rounded-tl-sm"
                            )}
                          >
                            {msg.from === "system" && (
                              <div className="flex items-center gap-1.5 mb-1">
                                <Bell className="w-3 h-3" />
                                <span className="text-[10px] font-medium">Alerta</span>
                              </div>
                            )}
                            {msg.label && msg.from === "ai" && (
                              <div className="flex items-center gap-1.5 mb-1">
                                <Bot className="w-3 h-3 text-recovery" />
                                <span className="text-[10px] font-medium text-recovery">{msg.label}</span>
                              </div>
                            )}
                            {msg.text}
                          </div>
                        </motion.div>
                      ))}
                      
                      {activeAgent.mockup.quickReplies && (
                        <motion.div
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          transition={{ delay: 0.5 }}
                          className="flex flex-wrap gap-1.5 md:gap-2 pt-1 md:pt-2"
                        >
                          {activeAgent.mockup.quickReplies.map((reply: string, i: number) => (
                            <span key={i} className="px-2.5 md:px-3 py-1 bg-transparent border border-recovery/50 text-recovery text-[10px] md:text-xs rounded-full">
                              {reply}
                            </span>
                          ))}
                        </motion.div>
                      )}
                    </div>
                  )}

                  {/* Metrics mockup */}
                  {activeAgent.mockup.type === "metrics" && (
                    <div className="grid grid-cols-3 gap-2 md:gap-3">
                      {activeAgent.mockup.items.map((item: any, i: number) => (
                        <motion.div
                          key={i}
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: i * 0.1 }}
                          className="bg-secondary rounded-xl p-3 md:p-4 text-center"
                        >
                          <p className="text-[10px] md:text-xs text-muted-foreground mb-1">{item.label}</p>
                          <p className={cn("text-base md:text-lg font-semibold", item.trend === "up" ? "text-recovery" : "text-soft-red")}>
                            {item.value}
                          </p>
                        </motion.div>
                      ))}
                    </div>
                  )}

                  {/* Profile mockup */}
                  {activeAgent.mockup.type === "profile" && (
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="bg-secondary rounded-xl p-3 md:p-4"
                    >
                      <div className="flex items-center gap-3 mb-3 md:mb-4">
                        <div className="w-10 h-10 md:w-12 md:h-12 rounded-full bg-foreground/10 flex items-center justify-center text-foreground font-semibold text-sm md:text-base">
                          {activeAgent.mockup.student.initials}
                        </div>
                        <div>
                          <p className="font-medium text-foreground text-sm md:text-base">{activeAgent.mockup.student.name}</p>
                          <p className="text-xs text-muted-foreground">Aluno desde {activeAgent.mockup.student.since}</p>
                        </div>
                      </div>
                      <div className="space-y-2 text-xs md:text-sm">
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">Restrição</span>
                          <span className="text-soft-red font-medium">{activeAgent.mockup.student.restriction}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">Objetivo</span>
                          <span className="text-foreground">{activeAgent.mockup.student.goal}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">Frequência</span>
                          <span className="text-recovery font-medium">{activeAgent.mockup.student.frequency}</span>
                        </div>
                      </div>
                    </motion.div>
                  )}

                  {/* Custom mockup */}
                  {activeAgent.mockup.type === "custom" && (
                    <div className="space-y-2 md:space-y-3">
                      <p className="text-xs md:text-sm text-muted-foreground mb-3 md:mb-4">
                        Exemplos de agentes personalizados:
                      </p>
                      {activeAgent.mockup.examples.map((example: string, i: number) => (
                        <motion.div
                          key={i}
                          initial={{ opacity: 0, x: -10 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: i * 0.1 }}
                          className="flex items-center gap-2 md:gap-3 bg-secondary rounded-xl p-2.5 md:p-3"
                        >
                          <div className="w-7 h-7 md:w-8 md:h-8 rounded-lg bg-blue/10 flex items-center justify-center text-blue">
                            <Sparkles className="w-3.5 h-3.5 md:w-4 md:h-4" />
                          </div>
                          <span className="text-xs md:text-sm text-muted-foreground">{example}</span>
                        </motion.div>
                      ))}
                    </div>
                  )}
                </div>

                {/* Result */}
                <div className="px-4 md:px-5 pb-4 md:pb-5">
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.6 }}
                    className="flex items-center gap-2 bg-recovery/10 text-recovery rounded-xl px-3 md:px-4 py-2 md:py-2.5 text-xs md:text-sm font-medium"
                  >
                    <Check className="w-3.5 h-3.5 md:w-4 md:h-4 shrink-0" />
                    {activeAgent.result}
                  </motion.div>
                </div>
              </motion.div>
            </AnimatePresence>
          </div>
        </div>
      </div>
    </section>
  )
}
