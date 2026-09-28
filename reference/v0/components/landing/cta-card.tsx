"use client"

import { motion } from "framer-motion"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { ArrowRight } from "lucide-react"

interface CTACardProps {
  title: string
  description?: string
  primaryAction: {
    label: string
    href?: string
    onClick?: () => void
  }
  secondaryAction?: {
    label: string
    href?: string
    onClick?: () => void
  }
  variant?: "default" | "dark" | "gradient"
  className?: string
}

export function CTACard({
  title,
  description,
  primaryAction,
  secondaryAction,
  variant = "default",
  className,
}: CTACardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      className={cn(
        "rounded-2xl md:rounded-3xl p-6 md:p-8 lg:p-12",
        variant === "default" && "bg-card border border-border",
        variant === "dark" && "bg-dark-panel text-white",
        variant === "gradient" && "bg-gradient-to-br from-blue to-purple text-white",
        className
      )}
    >
      <div className="max-w-2xl mx-auto text-center">
        <h3
          className={cn(
            "text-xl md:text-2xl lg:text-3xl font-semibold text-balance",
            variant === "default" ? "text-foreground" : "text-white"
          )}
        >
          {title}
        </h3>
        {description && (
          <p
            className={cn(
              "mt-3 md:mt-4 text-sm md:text-base lg:text-lg",
              variant === "default" ? "text-muted-foreground" : "text-white/80"
            )}
          >
            {description}
          </p>
        )}
        <div className="mt-6 md:mt-8 flex flex-col sm:flex-row items-center justify-center gap-3 md:gap-4">
          <Button
            size="lg"
            className={cn(
              "w-full sm:w-auto rounded-full px-6 md:px-8 h-11 md:h-12 text-sm md:text-base font-medium",
              variant === "dark" && "bg-white text-dark-panel hover:bg-white/90",
              variant === "gradient" && "bg-white text-blue hover:bg-white/90"
            )}
            onClick={primaryAction.onClick}
          >
            {primaryAction.label}
            <ArrowRight className="ml-2 w-4 h-4" />
          </Button>
          {secondaryAction && (
            <Button
              size="lg"
              variant="ghost"
              className={cn(
                "w-full sm:w-auto rounded-full px-6 md:px-8 h-11 md:h-12 text-sm md:text-base font-medium",
                variant !== "default" && "text-white hover:text-white hover:bg-white/10"
              )}
              onClick={secondaryAction.onClick}
            >
              {secondaryAction.label}
            </Button>
          )}
        </div>
      </div>
    </motion.div>
  )
}
