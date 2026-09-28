import resolved from "../../../../Pacote_Implementacao_Copiloto_v1_0/tokens/tokens_resolvidos.json";

/** Fonte única dos valores visuais aprovados; diferenças finais já estão no JSON resolvido. */
export const uiTokens = resolved;

export const fontFamily = {
  regular: "Arial, sans-serif",
  semibold: "Arial, sans-serif",
  bold: "Arial, sans-serif",
} as const;
