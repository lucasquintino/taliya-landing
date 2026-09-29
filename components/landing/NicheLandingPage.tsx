"use client";

import { useEffect, useState } from "react";
import type { BillingPeriod, NicheLandingConfig, ProblemModeId } from "@/data/landing/niches/types";
import { trackLandingEvent } from "@/lib/landing/tracking";
import { AgentsDemoSection } from "./sections/AgentsDemoSection";
import { FAQSection } from "./sections/FAQSection";
import { FinalCTASection } from "./sections/FinalCTASection";
import { FooterSection } from "./sections/FooterSection";
import { HeroSection } from "./sections/HeroSection";
import { HowItWorksSection } from "./sections/HowItWorksSection";
import { IntentSelectorSection } from "./sections/IntentSelectorSection";
import { MessageWallSection } from "./sections/MessageWallSection";
import { PlanOfferSection } from "./sections/PlanOfferSection";
import { ProblemDiagnosisSection } from "./sections/ProblemDiagnosisSection";
import { SalesStartSection } from "./sections/SalesStartSection";
import { FloatingAiAttendant } from "./shared/FloatingAiAttendant";
import { Header } from "./shared/Header";

type Props = {
  config: NicheLandingConfig;
};

const observedSections = [
  "top",
  "intencoes",
  "diagnostico-operacional",
  "como-funciona",
  "fale-do-seu-jeito",
  "agentes",
  "comecar",
  "planos",
  "vendas",
  "faq",
  "cta-final",
];

const SALES_START_FIRST_CARD_DELAY_MS = 40;
const SALES_START_CARD_INTERVAL_MS = 170;

export function NicheLandingPage({ config }: Props) {
  const [selectedPain, setSelectedPain] = useState(config.pains[0]);
  const [selectedMode, setSelectedMode] = useState<ProblemModeId>(config.diagnosis.modes[0].id);
  const [selectedAgent, setSelectedAgent] = useState(config.agents[0]);
  const [activeSection, setActiveSection] = useState("top");
  const [isLoaderExiting, setIsLoaderExiting] = useState(false);
  const [isLoaderVisible, setIsLoaderVisible] = useState(true);
  const [isPageReady, setIsPageReady] = useState(false);
  const [isLoaderMotionReady, setIsLoaderMotionReady] = useState(false);
  const [scrollProgress, setScrollProgress] = useState(0);

  useEffect(() => {
    trackLandingEvent(config.tracking, "page_view_niche");
  }, [config.tracking]);

  useEffect(() => {
    let isMounted = true;
    const timers: number[] = [];
    const motionFrame = window.requestAnimationFrame(() => {
      if (isMounted) setIsLoaderMotionReady(true);
    });
    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const minimumDuration = new Promise<void>((resolve) => {
      timers.push(window.setTimeout(resolve, prefersReducedMotion ? 520 : 2600));
    });

    document.body.classList.add("landing-page-loading");

    waitForLandingEntryReadiness(minimumDuration).then(() => {
      if (!isMounted) return;
      lockHeroEntryMetrics();
      setIsLoaderExiting(true);
      timers.push(window.setTimeout(() => {
        if (!isMounted) return;
        setIsPageReady(true);
        setIsLoaderVisible(false);
        document.body.classList.remove("landing-page-loading");
      }, 280));
    });

    return () => {
      isMounted = false;
      window.cancelAnimationFrame(motionFrame);
      timers.forEach((timer) => window.clearTimeout(timer));
      document.body.classList.remove("landing-page-loading");
      unlockHeroEntryMetrics();
    };
  }, []);

  useEffect(() => {
    if (!isPageReady) return;

    document.body.classList.add("landing-motion-ready");
    const revealItems = Array.from(document.querySelectorAll<HTMLElement>(".reveal-on-scroll"));
    const revealSteps = Array.from(document.querySelectorAll<HTMLElement>(".reveal-on-scroll .reveal-step"));
    const revealSubstepSelectors = [
      ".reveal-step > h1",
      ".reveal-step > h2",
      ".reveal-step > h3",
      ".reveal-step > p",
      ".reveal-step > article",
      ".reveal-step > label",
      ".reveal-step > a",
      ".reveal-step > button",
      ".topic-carousel-slide h2",
      ".topic-carousel-slide h2 + p",
      ".how-topic-bullet",
      ".how-topic-visual-part",
      ".how-topic-interactive",
      ".how-topic-mini-card",
      ".agent-team-card",
      ".agent-team-bullet",
      ".settings-visual-card",
      ".settings-visual-footer",
      ".taliya-app-class-card",
      ".taliya-app-student-row",
      ".taliya-app-bottom-nav",
      ".concept-step-button",
      ".live-flow-step",
      ".chat-line",
      ".intent-pain-option",
      ".sales-start-step > span:first-child",
      ".sales-start-step h3",
      ".sales-start-step p",
      ".agent-nav-item",
      ".agent-flow-tab",
      ".agent-flow-heading",
      ".agent-channel-chips span",
      ".agent-flow-card",
      ".agent-detail-row",
      ".agent-detail-item",
      ".agent-path-card",
      ".agent-path-card-aligned",
      ".panel-row",
      ".mobile-topic-nav button",
      ".mobile-agent-nav button",
    ].join(",");
    const revealObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
          }
        });
      },
      { rootMargin: "0px 0px 8% 0px", threshold: 0.08 },
    );
    const stepObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-step-visible");
            stepObserver.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px 14% 0px", threshold: 0.04 },
    );
    const useLateMobileReveal = window.matchMedia("(max-width: 767px)").matches;
    const salesStartSequenceTimers: number[] = [];
    let hasStartedSalesStartSequence = false;
    const startSalesStartDesktopSequence = () => {
      if (useLateMobileReveal || hasStartedSalesStartSequence) return;

      hasStartedSalesStartSequence = true;
      document.getElementById("comecar")?.classList.add("is-visible");

      const steps = Array.from(document.querySelectorAll<HTMLElement>("#comecar .sales-start-step"));

      steps.forEach((step, index) => {
        const timer = window.setTimeout(() => {
          step.classList.add("is-step-visible");
        }, SALES_START_FIRST_CARD_DELAY_MS + index * SALES_START_CARD_INTERVAL_MS);
        salesStartSequenceTimers.push(timer);
      });
    };
    const salesStartSequenceObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (useLateMobileReveal || !entry.isIntersecting || hasStartedSalesStartSequence) return;

          startSalesStartDesktopSequence();
          salesStartSequenceObserver.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -35% 0px", threshold: 0.08 },
    );
    const salesStartMobileStepObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;

          document.getElementById("comecar")?.classList.add("is-visible");
          entry.target.classList.add("is-step-visible");
          salesStartMobileStepObserver.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -22% 0px", threshold: 0.16 },
    );
    const lateStepObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-step-visible");
            lateStepObserver.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.12 },
    );
    const substepObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-substep-visible");
            substepObserver.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px 18% 0px", threshold: 0.04 },
    );

    const observedSubsteps = new WeakSet<HTMLElement>();
    const observeSubsteps = (root: ParentNode = document) => {
      const groupedIndexes = new Map<Element, number>();
      const candidates = [
        ...(root instanceof HTMLElement && root.matches(revealSubstepSelectors) ? [root] : []),
        ...Array.from(root.querySelectorAll<HTMLElement>(revealSubstepSelectors)),
      ];

      candidates.forEach((item) => {
        if (!item.closest(".reveal-on-scroll")) return;
        if (item.classList.contains("reveal-step")) return;
        if (item.closest("[data-no-scroll-reveal]")) return;

        item.classList.add("reveal-substep");

        const group = item.closest(".reveal-step") ?? item.closest(".reveal-on-scroll") ?? item.parentElement ?? item;
        const index = groupedIndexes.get(group) ?? 0;
        groupedIndexes.set(group, index + 1);
        item.style.setProperty("--substep-delay", `${Math.min(index * 58, 348)}ms`);

        if (!observedSubsteps.has(item)) {
          observedSubsteps.add(item);
          substepObserver.observe(item);
        }
      });
    };

    revealItems.forEach((item) => revealObserver.observe(item));
    revealSteps.forEach((item) => {
      if (item.closest("#comecar")) return;

      if (useLateMobileReveal && item.hasAttribute("data-mobile-late-reveal")) {
        lateStepObserver.observe(item);
        return;
      }

      stepObserver.observe(item);
    });
    if (useLateMobileReveal) {
      document.querySelectorAll<HTMLElement>("#comecar .sales-start-step").forEach((item) => {
        salesStartMobileStepObserver.observe(item);
      });
    } else {
      document.querySelectorAll<HTMLElement>("#comecar").forEach((item) => {
        salesStartSequenceObserver.observe(item);
      });
    }
    observeSubsteps();

    const substepMutationObserver = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node instanceof HTMLElement) {
            observeSubsteps(node);
          }
        });
      });
    });
    substepMutationObserver.observe(document.body, { childList: true, subtree: true });

    const revealHashTarget = () => {
      const targetId = window.location.hash.replace("#", "");
      if (!targetId) return;
      const target = document.getElementById(targetId);
      target?.classList.add("is-visible");
      if (targetId === "comecar") {
        startSalesStartDesktopSequence();
        return;
      }
      target?.querySelectorAll(".reveal-step").forEach((item) => item.classList.add("is-step-visible"));
      target?.querySelectorAll(".reveal-substep").forEach((item) => item.classList.add("is-substep-visible"));
    };

    revealHashTarget();

    const updateScrollState = () => {
      const scrollable = document.documentElement.scrollHeight - window.innerHeight;
      const progress = scrollable > 0 ? (window.scrollY / scrollable) * 100 : 0;
      setScrollProgress(Math.max(0, Math.min(100, progress)));

      const anchorLine = window.scrollY + 140;
      const currentSection = observedSections.reduce((current, id) => {
        const element = document.getElementById(id);
        if (!element) return current;
        return element.offsetTop <= anchorLine ? id : current;
      }, "top");
      setActiveSection(currentSection);
    };

    updateScrollState();
    window.addEventListener("scroll", updateScrollState, { passive: true });
    window.addEventListener("resize", updateScrollState);
    window.addEventListener("hashchange", revealHashTarget);

    return () => {
      revealObserver.disconnect();
      stepObserver.disconnect();
      lateStepObserver.disconnect();
      salesStartSequenceObserver.disconnect();
      salesStartMobileStepObserver.disconnect();
      salesStartSequenceTimers.forEach((timer) => window.clearTimeout(timer));
      substepObserver.disconnect();
      substepMutationObserver.disconnect();
      window.removeEventListener("scroll", updateScrollState);
      window.removeEventListener("resize", updateScrollState);
      window.removeEventListener("hashchange", revealHashTarget);
      document.body.classList.remove("landing-motion-ready");
    };
  }, [isPageReady]);

  function trackCta(label: string, href: string) {
    trackLandingEvent(config.tracking, "cta_click", { label, href });
  }

  function choosePain(painId: string) {
    const pain = config.pains.find((item) => item.id === painId);
    if (!pain) return;
    setSelectedPain(pain);
    trackLandingEvent(config.tracking, "pain_selected", {
      painId: pain.id,
      title: pain.title,
    });
  }

  function chooseAgent(agentId: string) {
    const agent = config.agents.find((item) => item.id === agentId);
    if (!agent) return;
    setSelectedAgent(agent);
    trackLandingEvent(config.tracking, "agent_selected", {
      agentId: agent.id,
      name: agent.name,
    });
  }

  function trackHumanWhatsApp(sourceSection: string) {
    const destination = config.assistedConversion.humanWhatsAppDestination;
    trackLandingEvent(config.tracking, "human_whatsapp_clicked", {
      sourceSection,
      destinationLabel: destination.label,
      destinationKind: destination.kind,
      destinationHref: destination.href,
      conversionPurpose: config.assistedConversion.conversionPurpose,
    });
  }

  function openSalesAgent() {
    trackLandingEvent(config.tracking, "cta_click", {
      label: config.salesCta.primaryCta,
      href: "#floating-agent",
      sourceSection: "studio_diagnostic",
      entryPath: "diagnostic_cta",
      selectedPainId: selectedPain.id,
      selectedAgentId: selectedAgent.id,
    });
    window.dispatchEvent(
      new CustomEvent("landing:open-sales-agent", {
        detail: {
          sourceSection: "studio_diagnostic",
          message: "Quero começar meu teste grátis de 14 dias.",
        },
      }),
    );
  }

  function openPlanOfferAgent(billingPeriod: BillingPeriod) {
    const billingOption = billingPeriod === "annual" ? config.launchOffer.annual : config.launchOffer.monthly;
    trackLandingEvent(config.tracking, "plan_cta_clicked", {
      planId: "taliya_single",
      planName: config.launchOffer.name,
      billingPeriod,
      priceBRL: billingOption.priceBRL,
      sourceSection: "plan_offer",
    });
    window.dispatchEvent(
      new CustomEvent("landing:open-sales-agent", {
        detail: {
          sourceSection: "plan_offer",
          message: `Quero começar os 14 dias grátis e seguir com o plano ${billingOption.label.toLowerCase()} da Taliya (${billingOption.price} ${billingOption.period}).`,
        },
      }),
    );
  }

  function trackFaqSupportEmailClick() {
    trackLandingEvent(config.tracking, "faq_doubt_cta_clicked", {
      sourceSection: "faq_doubt_cta",
      destination: "support_email",
      contactEmail: config.footer.contactEmail,
    });
  }

  if (!isPageReady && !isLoaderVisible) {
    return (
      <main className={`landing-page-loader ${isLoaderExiting ? "is-exiting" : ""}`} aria-busy="true" aria-label="Carregando página">
        <div className={`landing-loader-shell landing-loader-taliya ${isLoaderMotionReady ? "is-motion-ready" : ""}`} aria-hidden="true">
          <svg className="landing-loader-logo-mark" viewBox="0 0 272 224" focusable="false">
            <path
              className="landing-loader-logo-body"
              d="M193.49 96.44 L191.65 90.29 L188.57 85.38 L183.05 80.47 L135.14 48.53 L100.74 17.81 L90.91 12.29 L85.38 11.06 L27.03 11.06 L18.43 14.74 L13.51 20.27 L11.06 27.64 L11.67 33.78 L14.13 39.31 L53.44 79.24 L58.35 81.7 L64.5 82.92 L123.46 82.92 L124.69 84.15 L124.69 195.33 L127.76 203.32 L132.68 208.23 L139.43 211.3 L179.36 211.3 L186.73 207.62 L191.03 202.7 L193.49 196.56 Z"
            />
          </svg>
          <span className="landing-loader-logo-dot-flight">
            <span className="landing-loader-logo-dot" />
          </span>
        </div>
      </main>
    );
  }

  return (
    <>
      <main aria-busy={!isPageReady} className="min-h-screen overflow-x-clip bg-[#FAF7F1] text-[#101B3A]">
      <Header config={config} onCta={trackCta} activeSection={activeSection} scrollProgress={scrollProgress} />
      <HeroSection config={config} isReady={isPageReady} onCta={trackCta} />
      <IntentSelectorSection pains={config.pains} selectedPain={selectedPain} onSelectPain={choosePain} />
      <ProblemDiagnosisSection config={config} selectedMode={selectedMode} onSelectMode={setSelectedMode} />
      <HowItWorksSection config={config} onSelectAgent={chooseAgent} />
      <MessageWallSection onSelectAgent={chooseAgent} />
      <AgentsDemoSection agents={config.agents} intro={config.agentsIntro} selectedAgent={selectedAgent} onSelectAgent={chooseAgent} />
      <SalesStartSection config={config} onOpenAgent={openSalesAgent} onCta={trackCta} />
      <PlanOfferSection config={config} onStartSubscription={openPlanOfferAgent} />
      <FAQSection config={config} onContactSupport={trackFaqSupportEmailClick} />
      <FinalCTASection config={config} onCta={trackCta} />
      <FooterSection config={config} />
      <FloatingAiAttendant
        config={config}
        pageSignals={{
          selectedPainId: selectedPain.id,
          selectedAgentId: selectedAgent.id,
        }}
      />
      </main>
      {isLoaderVisible ? (
        <div className={`landing-page-loader ${isLoaderExiting ? "is-exiting" : ""}`} aria-busy="true" aria-label="Carregando pÃ¡gina" role="status">
          <div className={`landing-loader-shell landing-loader-taliya ${isLoaderMotionReady ? "is-motion-ready" : ""}`} aria-hidden="true">
            <svg className="landing-loader-logo-mark" viewBox="0 0 272 224" focusable="false">
              <path
                className="landing-loader-logo-body"
                d="M193.49 96.44 L191.65 90.29 L188.57 85.38 L183.05 80.47 L135.14 48.53 L100.74 17.81 L90.91 12.29 L85.38 11.06 L27.03 11.06 L18.43 14.74 L13.51 20.27 L11.06 27.64 L11.67 33.78 L14.13 39.31 L53.44 79.24 L58.35 81.7 L64.5 82.92 L123.46 82.92 L124.69 84.15 L124.69 195.33 L127.76 203.32 L132.68 208.23 L139.43 211.3 L179.36 211.3 L186.73 207.62 L191.03 202.7 L193.49 196.56 Z"
              />
            </svg>
            <span className="landing-loader-logo-dot-flight">
              <span className="landing-loader-logo-dot" />
            </span>
          </div>
        </div>
      ) : null}
    </>
  );
}

async function waitForLandingEntryReadiness(minimumDuration: Promise<void>) {
  await nextPaint();
  await Promise.all([waitForFonts(), waitForWindowLoad(), waitForCriticalImages(), minimumDuration]);
  await waitForHeroLayoutStability();
  await nextPaint();
}

function nextPaint() {
  return new Promise<void>((resolve) => {
    window.requestAnimationFrame(() => {
      window.requestAnimationFrame(() => resolve());
    });
  });
}

function waitForFonts() {
  if (!("fonts" in document)) return Promise.resolve();
  return document.fonts.ready.then(() => undefined).catch(() => undefined);
}

function waitForWindowLoad() {
  if (document.readyState === "complete") return Promise.resolve();
  return new Promise<void>((resolve) => window.addEventListener("load", () => resolve(), { once: true }));
}

function waitForCriticalImages() {
  const criticalImages = Array.from(document.querySelectorAll<HTMLImageElement>("header img, #top img, .hero-stage img"));
  if (criticalImages.length === 0) return Promise.resolve();

  return Promise.all(criticalImages.map(waitForImage)).then(() => undefined);
}

function waitForHeroLayoutStability() {
  const startedAt = performance.now();
  const maxWaitMs = 5200;
  const requiredStableFrames = 12;
  let stableFrames = 0;
  let previousSignature = "";

  return new Promise<void>((resolve) => {
    const sample = () => {
      const title = document.querySelector<HTMLElement>("#top .hero-title");
      if (!title) {
        window.requestAnimationFrame(sample);
        return;
      }

      const rect = title.getBoundingClientRect();
      const style = window.getComputedStyle(title);
      const signature = [
        roundLayoutValue(rect.width),
        roundLayoutValue(rect.height),
        roundLayoutValue(rect.top),
        roundLayoutValue(rect.left),
        style.fontSize,
        style.lineHeight,
        style.fontFamily,
        "fonts" in document ? document.fonts.status : "unsupported",
      ].join("|");

      stableFrames = signature === previousSignature ? stableFrames + 1 : 0;
      previousSignature = signature;

      if (stableFrames >= requiredStableFrames || performance.now() - startedAt > maxWaitMs) {
        resolve();
        return;
      }

      window.requestAnimationFrame(sample);
    };

    window.requestAnimationFrame(sample);
  });
}

function roundLayoutValue(value: number) {
  return Math.round(value * 100) / 100;
}

function waitForImage(image: HTMLImageElement) {
  if (image.complete && image.naturalWidth > 0) return Promise.resolve();
  if (typeof image.decode === "function") return image.decode().then(() => undefined).catch(() => undefined);

  return new Promise<void>((resolve) => {
    image.addEventListener("load", () => resolve(), { once: true });
    image.addEventListener("error", () => resolve(), { once: true });
  });
}

function lockHeroEntryMetrics() {
  const title = document.querySelector<HTMLElement>("#top .hero-title");
  if (!title) return;

  const style = window.getComputedStyle(title);
  document.documentElement.style.setProperty("--hero-entry-title-font-size", style.fontSize);
  document.documentElement.style.setProperty("--hero-entry-title-font-family", style.fontFamily);
  document.documentElement.style.setProperty("--hero-entry-title-line-height", style.lineHeight);
  document.documentElement.style.setProperty("--hero-entry-title-letter-spacing", style.letterSpacing);
  document.documentElement.classList.add("landing-hero-entry-locked");
  window.addEventListener("resize", unlockHeroEntryMetrics, { once: true });
  window.addEventListener("orientationchange", unlockHeroEntryMetrics, { once: true });
}

function unlockHeroEntryMetrics() {
  document.documentElement.classList.remove("landing-hero-entry-locked");
  document.documentElement.style.removeProperty("--hero-entry-title-font-size");
  document.documentElement.style.removeProperty("--hero-entry-title-font-family");
  document.documentElement.style.removeProperty("--hero-entry-title-line-height");
  document.documentElement.style.removeProperty("--hero-entry-title-letter-spacing");
}
