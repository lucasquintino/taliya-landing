"use client"

import { useState, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Button } from "@/components/ui/button"
import { Menu, X } from "lucide-react"
import { cn } from "@/lib/utils"

const navLinks = [
  { label: "Como funciona", href: "#como-funciona" },
  { label: "Agentes", href: "#agentes" },
  { label: "Calculadora", href: "#calculadora" },
]

export function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20)
    }
    window.addEventListener("scroll", handleScroll)
    return () => window.removeEventListener("scroll", handleScroll)
  }, [])

  // Close mobile menu on resize
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= 768) {
        setMobileMenuOpen(false)
      }
    }
    window.addEventListener("resize", handleResize)
    return () => window.removeEventListener("resize", handleResize)
  }, [])

  // Prevent body scroll when menu is open
  useEffect(() => {
    if (mobileMenuOpen) {
      document.body.style.overflow = "hidden"
    } else {
      document.body.style.overflow = ""
    }
    return () => {
      document.body.style.overflow = ""
    }
  }, [mobileMenuOpen])

  return (
    <>
      <header className="fixed top-0 left-0 right-0 z-50">
        <motion.div
          initial={{ y: -100 }}
          animate={{ y: 0 }}
          transition={{ duration: 0.5 }}
          className="mx-3 md:mx-4 mt-3 md:mt-4"
        >
          <div
            className={cn(
              "max-w-6xl mx-auto backdrop-blur-xl border rounded-xl md:rounded-2xl px-3 md:px-6 py-2.5 md:py-3 transition-all duration-300",
              scrolled
                ? "bg-card/90 border-border shadow-lg"
                : "bg-card/70 border-border/50"
            )}
          >
            <div className="flex items-center justify-between">
              {/* Logo */}
              <a href="/" className="flex items-center gap-2">
                <div className="w-7 h-7 md:w-8 md:h-8 rounded-lg bg-foreground flex items-center justify-center">
                  <span className="text-background font-bold text-xs md:text-sm">AP</span>
                </div>
                <span className="font-semibold text-foreground text-sm md:text-base hidden sm:block">
                  Agentes Pilates
                </span>
              </a>

              {/* Desktop Navigation */}
              <nav className="hidden md:flex items-center gap-6 lg:gap-8">
                {navLinks.map((link) => (
                  <a
                    key={link.href}
                    href={link.href}
                    className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
                  >
                    {link.label}
                  </a>
                ))}
              </nav>

              {/* CTA + Mobile Menu Button */}
              <div className="flex items-center gap-2 md:gap-3">
                <Button
                  className="hidden sm:flex rounded-full px-4 md:px-5 h-9 md:h-10 text-xs md:text-sm font-medium bg-foreground text-background hover:bg-foreground/90"
                >
                  Quero meu diagnóstico
                </Button>
                <button
                  className="md:hidden p-2 text-foreground rounded-lg hover:bg-secondary transition-colors"
                  onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                  aria-label={mobileMenuOpen ? "Fechar menu" : "Abrir menu"}
                >
                  {mobileMenuOpen ? (
                    <X className="w-5 h-5" />
                  ) : (
                    <Menu className="w-5 h-5" />
                  )}
                </button>
              </div>
            </div>
          </div>
        </motion.div>
      </header>

      {/* Mobile Menu Overlay */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <>
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="fixed inset-0 bg-background/80 backdrop-blur-sm z-40 md:hidden"
              onClick={() => setMobileMenuOpen(false)}
            />

            {/* Menu Panel */}
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.2 }}
              className="fixed top-16 left-3 right-3 bg-card border border-border rounded-2xl shadow-xl z-50 md:hidden overflow-hidden"
            >
              <nav className="p-4 flex flex-col">
                {navLinks.map((link, index) => (
                  <motion.a
                    key={link.href}
                    href={link.href}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.05 }}
                    className="px-4 py-3 text-base font-medium text-foreground hover:bg-secondary rounded-xl transition-colors"
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    {link.label}
                  </motion.a>
                ))}
                <motion.div
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: navLinks.length * 0.05 }}
                  className="mt-3 pt-3 border-t border-border"
                >
                  <Button 
                    className="w-full rounded-full h-12 text-sm font-medium bg-foreground text-background hover:bg-foreground/90"
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    Quero meu diagnóstico
                  </Button>
                </motion.div>
              </nav>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  )
}
