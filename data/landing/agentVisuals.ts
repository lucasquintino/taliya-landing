export type AgentVisualToken = {
  label: string;
  accent: string;
  soft: string;
  activeBg: string;
};

export const agentVisualTokens: Record<string, AgentVisualToken> = {
  atendimento: {
    label: "Atendimento",
    accent: "#6E7F2C",
    soft: "#F0F3DF",
    activeBg: "#FBFDF2",
  },
  agenda: {
    label: "Agenda",
    accent: "#008C8C",
    soft: "#E5F6F4",
    activeBg: "#F3FFFC",
  },
  reposicoes: {
    label: "Reposições",
    accent: "#C18A16",
    soft: "#FFF4D9",
    activeBg: "#FFF9EC",
  },
  financeiro: {
    label: "Financeiro",
    accent: "#A95722",
    soft: "#FBEBDD",
    activeBg: "#FFF6EE",
  },
  gestao: {
    label: "Gestão",
    accent: "#263238",
    soft: "#E9EEF0",
    activeBg: "#F5F8F8",
  },
  vendas: {
    label: "Vendas",
    accent: "#C8492E",
    soft: "#FBE7E0",
    activeBg: "#FFF4F0",
  },
  retencao: {
    label: "Retenção",
    accent: "#D59A00",
    soft: "#FFF2C9",
    activeBg: "#FFF9E8",
  },
  historico: {
    label: "Histórico",
    accent: "#6F4E7C",
    soft: "#F0E8F4",
    activeBg: "#FBF7FD",
  },
};
