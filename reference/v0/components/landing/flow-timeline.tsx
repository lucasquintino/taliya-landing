"use client"

import { motion } from "framer-motion"
import { cn } from "@/lib/utils"

interface TimelineStep {
  icon: React.ReactNode
  title: string
  description: string
  color?: string
}

interface FlowTimelineProps {
  steps: TimelineStep[]
  className?: string
}

export function FlowTimeline({ steps, className }: FlowTimelineProps) {
  return (
    <div className={cn("relative", className)}>
      {/* Connecting line */}
      <div className="absolute left-6 top-0 bottom-0 w-px bg-border hidden md:block" />

      <div className="space-y-6">
        {steps.map((step, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ delay: index * 0.1, duration: 0.4 }}
            className="flex gap-4 md:gap-6"
          >
            <div
              className={cn(
                "relative z-10 flex-shrink-0 w-12 h-12 rounded-xl flex items-center justify-center",
                step.color || "bg-blue/10 text-blue"
              )}
            >
              {step.icon}
            </div>
            <div className="flex-1 pt-1">
              <h4 className="font-medium text-foreground">{step.title}</h4>
              <p className="mt-1 text-sm text-muted-foreground leading-relaxed">
                {step.description}
              </p>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
