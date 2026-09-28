"use client"

import { motion, AnimatePresence } from "framer-motion"
import { cn } from "@/lib/utils"
import { MessageCircle, Bot, Check, Clock, User, ArrowRight } from "lucide-react"

interface MockupMessage {
  type: "user" | "system" | "ai"
  content: string
  delay?: number
}

interface MockupStep {
  icon: React.ReactNode
  label: string
  value?: string
  color?: string
}

interface ProductMockupProps {
  title?: string
  messages?: MockupMessage[]
  steps?: MockupStep[]
  result?: {
    icon?: React.ReactNode
    text: string
    color?: string
  }
  className?: string
  variant?: "whatsapp" | "dashboard" | "minimal"
}

export function ProductMockup({
  title,
  messages = [],
  steps = [],
  result,
  className,
  variant = "whatsapp",
}: ProductMockupProps) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      transition={{ duration: 0.4 }}
      className={cn(
        "rounded-2xl overflow-hidden shadow-lg",
        variant === "whatsapp" && "bg-dark-panel",
        variant === "dashboard" && "bg-card border border-border",
        variant === "minimal" && "bg-secondary",
        className
      )}
    >
      {/* Header */}
      {title && (
        <div
          className={cn(
            "px-4 py-3 border-b flex items-center gap-3",
            variant === "whatsapp"
              ? "bg-[#1f2c33] border-[#2a3942]"
              : "border-border"
          )}
        >
          <div
            className={cn(
              "w-10 h-10 rounded-full flex items-center justify-center",
              variant === "whatsapp" ? "bg-recovery/20" : "bg-secondary"
            )}
          >
            <Bot
              className={cn(
                "w-5 h-5",
                variant === "whatsapp" ? "text-recovery" : "text-foreground"
              )}
            />
          </div>
          <div>
            <p
              className={cn(
                "font-medium text-sm",
                variant === "whatsapp" ? "text-white" : "text-foreground"
              )}
            >
              {title}
            </p>
            <p
              className={cn(
                "text-xs",
                variant === "whatsapp" ? "text-gray-400" : "text-muted-foreground"
              )}
            >
              Agente ativo
            </p>
          </div>
        </div>
      )}

      {/* Messages */}
      <div className="p-4 space-y-3 min-h-[200px]">
        <AnimatePresence mode="wait">
          {messages.map((message, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: (message.delay || index * 0.15), duration: 0.3 }}
              className={cn(
                "flex",
                message.type === "user" ? "justify-end" : "justify-start"
              )}
            >
              <div
                className={cn(
                  "max-w-[85%] rounded-2xl px-4 py-2.5 text-sm",
                  message.type === "user" &&
                    "bg-recovery text-white rounded-tr-sm",
                  message.type === "system" &&
                    "bg-amber/20 text-amber border border-amber/30",
                  message.type === "ai" &&
                    "bg-[#1f2c33] text-gray-100 rounded-tl-sm"
                )}
              >
                {message.type === "system" && (
                  <div className="flex items-center gap-2 mb-1">
                    <Bot className="w-3.5 h-3.5" />
                    <span className="text-xs font-medium">IA detectou</span>
                  </div>
                )}
                {message.content}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {/* Steps */}
        {steps.length > 0 && (
          <div className="mt-4 space-y-2">
            {steps.map((step, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 + index * 0.1, duration: 0.3 }}
                className={cn(
                  "flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm",
                  variant === "whatsapp"
                    ? "bg-[#1f2c33]"
                    : "bg-secondary"
                )}
              >
                <div
                  className={cn(
                    "w-8 h-8 rounded-lg flex items-center justify-center",
                    step.color || "bg-blue/20 text-blue"
                  )}
                >
                  {step.icon}
                </div>
                <span
                  className={cn(
                    "flex-1",
                    variant === "whatsapp" ? "text-gray-300" : "text-muted-foreground"
                  )}
                >
                  {step.label}
                </span>
                {step.value && (
                  <span
                    className={cn(
                      "font-medium",
                      variant === "whatsapp" ? "text-white" : "text-foreground"
                    )}
                  >
                    {step.value}
                  </span>
                )}
              </motion.div>
            ))}
          </div>
        )}

        {/* Result */}
        {result && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8, duration: 0.3 }}
            className={cn(
              "mt-4 flex items-center gap-2 rounded-xl px-4 py-3 text-sm font-medium",
              result.color || "bg-recovery/20 text-recovery"
            )}
          >
            {result.icon || <Check className="w-4 h-4" />}
            {result.text}
          </motion.div>
        )}
      </div>
    </motion.div>
  )
}
