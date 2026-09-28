export type CampaignStage = "validation" | "closed_access" | "launch" | "commercial";

export type PublicOfferMode = "diagnostic_and_early_access" | "direct_saas_subscription";

export type TrackingContext = {
  niche: string;
  sourcePage: string;
  campaignStage: CampaignStage;
  publicOfferMode: PublicOfferMode;
  internalGoal: string;
};

export type CTA = {
  label: string;
  href: string;
};

export type BillingPeriod = "monthly" | "annual";

export type TrustedDestination = {
  label: string;
  href: string;
  kind: "checkout" | "plan_selection" | "guided_demo" | "analysis" | "whatsapp" | "privacy";
};

export type PricingPlan = {
  id: "base" | "one_agent" | "three_agents" | "seven_agents" | string;
  name: string;
  monthlyPriceBRL: number;
  monthlyPriceLabel: string;
  billingPeriod: BillingPeriod;
  recommended?: boolean;
  bestFor: string;
  positioning: string;
  includedAgents: string[];
  whatsappAvailability: string;
  setupExpectation: string;
  usageBoundary: string;
  primaryCta: TrustedDestination;
  secondaryHumanCta: TrustedDestination;
  annual?: {
    priceBRL: number;
    priceLabel: string;
    discountLabel: string;
    checkout: TrustedDestination;
  };
};

export type SubscriptionConfig = {
  recommendedPlanId: string;
  defaultBillingPeriod: BillingPeriod;
  plans: PricingPlan[];
  fallbackPlanSelection: TrustedDestination;
};

export type AssistedConversionConfig = {
  title: string;
  subtitle: string;
  conversionPurpose: string;
  analysisDestination: TrustedDestination;
  humanWhatsAppDestination: TrustedDestination;
  privacyNotice: TrustedDestination;
  consentText: string;
  whatsappConsentText: string;
  fields: Array<
    | "name"
    | "whatsapp"
    | "email"
    | "studioName"
    | "cityState"
    | "activeStudents"
    | "biggestPain"
    | "currentSystem"
    | "customRoutine"
    | "preferredNextStep"
  >;
};

export type SalesSetupStep = {
  title: string;
  description: string;
  items: string[];
};

export type SalesSetupConfig = {
  eyebrow: string;
  title: string;
  subtitle: string;
  steps: SalesSetupStep[];
  reassurance: string;
};

export type SalesCtaConfig = {
  eyebrow: string;
  title: string;
  subtitle: string;
  primaryCta: string;
  secondaryCta: string;
  whatsappMessage: string;
  microcopy: string;
  proofPoints: string[];
};

export type LaunchOfferBillingOption = {
  label: string;
  price: string;
  priceBRL: number;
  period: string;
  renewal: string;
};

export type LaunchOfferBenefit = {
  title: string;
  description: string;
};

export type LaunchOfferConfig = {
  title: string;
  body: string;
  name: string;
  toggleLabel: string;
  monthly: LaunchOfferBillingOption;
  annual: LaunchOfferBillingOption;
  benefits: LaunchOfferBenefit[];
  trial: string;
  cta: string;
  smallPrint: string;
};

export type FloatingAgentQuickReply = {
  id:
    | "ask_product"
    | "describe_pain"
    | "ask_agents"
    | "ask_price"
    | "view_plans"
    | "guided_demo"
    | "checkout_intent"
    | "analysis_request"
    | "human_whatsapp_assist"
    | "custom_agent_interest"
    | string;
  label: string;
  intent:
    | "ask_product"
    | "describe_pain"
    | "ask_agent"
    | "ask_price"
    | "view_plans"
    | "guided_demo"
    | "checkout_intent"
    | "diagnostic_interest"
    | "human_whatsapp_assist"
    | "ask_unsupported_feature";
};

export type FloatingAgentPainOption = {
  id: string;
  label: string;
  keywords: string[];
};

export type FloatingAgentPainToAgents = {
  painId: string;
  agentIds: string[];
  explanation: string;
  exampleAction: string;
  nextQuestion?: string;
};

export type FloatingAgentQualificationQuestion = {
  field:
    | "name"
    | "whatsapp"
    | "email"
    | "studioName"
    | "cityState"
    | "activeStudentsRange"
    | "biggestPain"
    | "currentSystem"
    | "customRoutine"
    | "contactPreference"
    | "preferredNextStep";
  question: string;
  purpose: "analysis" | "human_whatsapp_assist" | "custom_agent_follow_up";
};

export type FloatingAgentConversionCtas = {
  viewPlans: {
    label: string;
    description: string;
    systemDestination: "configured_plan_comparison";
  };
  guidedDemo: {
    label: string;
    description: string;
    systemDestination: "configured_guided_demo";
  };
  checkoutIntent: {
    label: string;
    description: string;
    systemDestination: "recommended_plan_checkout" | "fallback_plan_selection";
  };
  analysis: {
    label: string;
    description: string;
    systemDestination: "assisted_analysis";
  };
  humanWhatsApp: {
    label: string;
    description: string;
    systemDestination: "assisted_human_whatsapp";
  };
  customAgent: {
    label: string;
    description: string;
    systemDestination: "assisted_analysis";
  };
};

export type FloatingAgentFallbackMessages = {
  providerFailure: string;
  promptInjection: string;
  unsupported: string;
  sensitiveData: string;
  offTopic: string;
  rateLimited: string;
};

export type FloatingAgentConfig = {
  enabled: boolean;
  label: string;
  availability: string;
  localeSignal: {
    label: string;
    emoji: string;
  };
  avatar: {
    src: string;
    alt: string;
  };
  greeting: string;
  quickReplies: FloatingAgentQuickReply[];
  painOptions: FloatingAgentPainOption[];
  painToAgents: FloatingAgentPainToAgents[];
  qualificationQuestions: FloatingAgentQualificationQuestion[];
  planComparisonDestination: TrustedDestination;
  guidedDemoDestination: TrustedDestination;
  guidedDemoReady: boolean;
  conversionCtas: FloatingAgentConversionCtas;
  commercialConfigRef: {
    subscriptionField: "subscription";
    assistedConversionField: "assistedConversion";
  };
  copyBoundaries: {
    prohibitedTerms: string[];
    preferredTerms: string[];
  };
  fallbackMessages: FloatingAgentFallbackMessages;
};

export type ConversationLine = {
  from: "student" | "agent" | "system" | "owner";
  label?: string;
  text: string;
};

export type ConversationMockup = {
  title: string;
  status: string;
  lines: ConversationLine[];
  quickReplies?: string[];
  result: string;
};

export type AutonomousFlowStep =
  | {
      type: "message";
      actor: "student" | "agent";
      speaker?: string;
      text: string;
    }
  | {
      type: "process";
      text: string;
    }
  | {
      type: "switch";
      text: string;
    }
  | {
      type: "notification";
      text: string;
    };

export type AutonomousFlowMockup = {
  title: string;
  status: string;
  agentId: string;
  contactName: string;
  contactAvatars?: Record<string, string>;
  steps: AutonomousFlowStep[];
  systemCards: string[];
  result: string;
};

export type PainOption = {
  id: string;
  chip: string;
  title: string;
  description: string;
  result: string;
  conversation: ConversationMockup;
  autonomousFlow?: AutonomousFlowMockup;
};

export type ProblemModeId = "without_agents" | "with_agents";

export type ProblemMode = {
  id: ProblemModeId;
  label: string;
  eyebrow: string;
  tone: "loss" | "gain";
  channels: string[];
  modeTitle: string;
  modeDescription: string;
  modeVisual: string;
  modeFlow: string;
  cards: { agent: string; title: string; description: string; preview: string }[];
};

export type CalculatorDefaults = {
  activeStudents: number;
  averageMonthlyFee: number;
  weeklyAbsences: number;
  weeklyOpenClasses: number;
  monthlyOverduePayments: number;
  plansExpiring30Days: number;
  inactiveStudents30Days: number;
  monthlyInterestedPeople: number;
  trialClassesWithoutClosing: number;
  manualHoursPerWeek: number;
};

export type AgentWorkspaceItem = {
  label: string;
  value: string;
  tone?: "neutral" | "warning" | "success" | "accent";
};

export type AgentOperationalFlow = {
  id: string;
  code: string;
  title: string;
  mode: "automatico" | "copiloto" | "humano" | "customizado";
  channel: "whatsapp" | "sistema" | "hibrido";
  trigger: string;
  checks: string[];
  action: string;
  message: string;
  result: string;
  handoff?: string;
};

export type Agent = {
  id: string;
  name: string;
  role: string;
  pain: string;
  action: string;
  result: string;
  accent: string;
  workspace: {
    title: string;
    subtitle: string;
    primaryMetric: string;
    primaryMetricLabel: string;
    queue: AgentWorkspaceItem[];
    conversation: ConversationMockup;
  };
  operationalFlows?: AgentOperationalFlow[];
};

export type HumanControlMode = {
  id: string;
  label: string;
  title: string;
  description: string;
  actions: string[];
  conversation: ConversationMockup;
};

export type GuidedStep = {
  title: string;
  description: string;
  screenTitle: string;
  screenItems: string[];
};

export type HowItWorksTopic = {
  id: string;
  label: string;
  navSubtitle?: string;
  eyebrow: string;
  title: string;
  description: string;
  accent: string;
  soft: string;
  icon: string;
  visual: "agents-explained" | "pilates-focus" | "agent-team" | "settings" | "channels" | "modes";
  points: string[];
  demoPainId?: string;
  systemUpdates?: AgentWorkspaceItem[];
  productCards?: {
    id: string;
    title: string;
    bullets: string[];
    agentId: string;
  }[];
  groups?: {
    title: string;
    description?: string;
    items: string[];
  }[];
  cta?: CTA;
};

export type NicheLandingConfig = {
  niche: string;
  route: string;
  brand: string;
  metadata: {
    title: string;
    description: string;
  };
  tracking: TrackingContext;
  header: {
    links: { label: string; href: string }[];
    cta: CTA;
  };
  hero: {
    eyebrow: string;
    headline: string;
    highlight: string;
    centralMessage: string;
    subheadline: string;
    primaryCta: CTA;
    secondaryCta: CTA;
    proofNotes: string[];
    proofConversation: ConversationMockup;
  };
  pains: PainOption[];
  diagnosis: {
    title: string;
    subtitle: string;
    modes: ProblemMode[];
  };
  calculator: {
    eyebrow: string;
    title: string;
    subtitle: string;
    defaults: CalculatorDefaults;
    disclaimer: string;
    cta: CTA;
  };
  agentsIntro: {
    eyebrow: string;
    title: string;
    subtitle: string;
  };
  agents: Agent[];
  howItWorks: {
    title: string;
    subtitle: string;
    topics: HowItWorksTopic[];
  };
  coverage: {
    title: string;
    subtitle: string;
    items: AgentWorkspaceItem[];
  };
  nicheSpecific: {
    title: string;
    description: string;
    items: string[];
  };
  customAgent: {
    title: string;
    description: string;
    examples: string[];
    cta: string;
  };
  humanControl: {
    title: string;
    subtitle: string;
    points: string[];
    conversation: ConversationMockup;
    modes: HumanControlMode[];
  };
  subscription: SubscriptionConfig;
  assistedConversion: AssistedConversionConfig;
  salesSetup: SalesSetupConfig;
  launchOffer: LaunchOfferConfig;
  salesCta: SalesCtaConfig;
  floatingAgent: FloatingAgentConfig;
  earlyAccess: {
    title: string;
    description: string;
    offerItems: string[];
    cta: string;
  };
  form: {
    title: string;
    subtitle: string;
    painOptions: string[];
    systemOptions: string[];
    accessOptions: string[];
  };
  faq: { question: string; answer: string }[];
  finalCta: {
    title: string;
    description: string;
    promptPlaceholder: string;
    cta: CTA;
  };
  footer: {
    text: string;
    contactEmail?: string;
    links: { label: string; href: string }[];
  };
};
