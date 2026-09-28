"use client"

import { motion } from "framer-motion"
import { cn } from "@/lib/utils"

interface SectionHeaderProps {
  eyebrow?: string
  title: string
  description?: string
  align?: "left" | "center"
  className?: string
}

export function SectionHeader({
  eyebrow,
  title,
  description,
  align = "center",
  className,
}: SectionHeaderProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-100px" }}
      transition={{ duration: 0.5 }}
      className={cn(
        "max-w-3xl",
        align === "center" && "mx-auto text-center",
        className
      )}
    >
      {eyebrow && (
        <span className="inline-block text-xs md:text-sm font-medium text-muted-foreground mb-2 md:mb-3 tracking-wide uppercase">
          {eyebrow}
        </span>
      )}
      <h2 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-semibold tracking-tight text-foreground text-balance">
        {title}
      </h2>
      {description && (
        <p className="mt-3 md:mt-4 text-sm md:text-base lg:text-lg text-muted-foreground text-pretty leading-relaxed">
          {description}
        </p>
      )}
    </motion.div>
  )
}
