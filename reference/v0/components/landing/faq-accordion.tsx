"use client"

import { motion } from "framer-motion"
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion"
import { SectionHeader } from "./section-header"
import { cn } from "@/lib/utils"

const faqItems = [
  {
    question: "Como os agentes funcionam na prática?",
    answer: "Os agentes são automações inteligentes que monitoram eventos do seu studio (cancelamentos, vencimentos, inatividade) e executam ações automáticas como enviar mensagens, reorganizar agenda ou alertar sobre oportunidades. Tudo integrado com WhatsApp e seu sistema de gestão."
  },
  {
    question: "Preciso trocar meu sistema de gestão atual?",
    answer: "Não. Os agentes se integram com os principais sistemas de gestão de studios de Pilates. Trabalhamos em paralelo, potencializando o que você já usa."
  },
  {
    question: "Quanto tempo leva para implementar?",
    answer: "A implementação básica leva de 3 a 7 dias, dependendo das integrações necessárias. Durante esse período, configuramos os agentes de acordo com a rotina específica do seu studio."
  },
  {
    question: "Os agentes substituem minha equipe?",
    answer: "Não. Os agentes automatizam tarefas repetitivas e administrativas, liberando sua equipe para focar no que realmente importa: cuidar dos alunos, dar aulas de qualidade e construir relacionamentos."
  },
  {
    question: "Como funciona o diagnóstico gratuito?",
    answer: "É uma conversa de 15 minutos onde analisamos sua operação atual e identificamos onde estão as maiores oportunidades de recuperação de receita. Sem compromisso."
  },
  {
    question: "Posso personalizar como os agentes se comunicam?",
    answer: "Sim! Você define o tom de voz, as mensagens padrão e as regras de quando cada agente deve atuar. Tudo configurável de acordo com a identidade do seu studio."
  },
]

export function FAQAccordion() {
  return (
    <section className="py-16 md:py-24 lg:py-32 px-4">
      <div className="max-w-3xl mx-auto">
        <SectionHeader
          eyebrow="Dúvidas"
          title="Perguntas frequentes"
          description="Tudo que você precisa saber sobre os agentes."
        />

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mt-10 md:mt-12"
        >
          <Accordion type="single" collapsible className="w-full space-y-2 md:space-y-3">
            {faqItems.map((item, index) => (
              <AccordionItem
                key={index}
                value={`item-${index}`}
                className="bg-card border border-border rounded-xl md:rounded-2xl px-4 md:px-6 data-[state=open]:shadow-sm"
              >
                <AccordionTrigger className="text-left font-medium text-foreground hover:no-underline py-4 md:py-5 text-sm md:text-base">
                  {item.question}
                </AccordionTrigger>
                <AccordionContent className="text-muted-foreground pb-4 md:pb-5 leading-relaxed text-xs md:text-sm">
                  {item.answer}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </motion.div>
      </div>
    </section>
  )
}
