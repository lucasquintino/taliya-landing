"use client"

import { motion } from "framer-motion"
import { cn } from "@/lib/utils"

interface MetricCardProps {
  label: string
  value: string
  trend?: string
  trendUp?: boolean
  icon?: React.ReactNode
  className?: string
}

export function MetricCard({
  label,
  value,
  trend,
  trendUp,
  icon,
  className,
}: MetricCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      className={cn(
        "bg-card rounded-2xl border border-border p-6 shadow-sm",
        className
      )}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-muted-foreground">{label}</p>
          <p className="mt-2 text-3xl font-semibold text-foreground">{value}</p>
          {trend && (
            <p
              className={cn(
                "mt-1 text-sm font-medium",
                trendUp ? "text-recovery" : "text-soft-red"
              )}
            >
              {trend}
            </p>
          )}
        </div>
        {icon && (
          <div className="rounded-xl bg-secondary p-3 text-foreground">
            {icon}
          </div>
        )}
      </div>
    </motion.div>
  )
}
