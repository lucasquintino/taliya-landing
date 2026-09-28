import type { CalculatorDefaults } from "@/data/landing/niches/types";

export const ESTIMATED_OPERATIONAL_HOUR_VALUE = 75;

export type MoneyCalculatorResult = {
  total: number;
  breakdown: {
    atendimento: number;
    agenda: number;
    vendas: number;
    financeiro: number;
    retencao: number;
    gestao: number;
    historicoEvolucao: number;
  };
  metrics: {
    absencesAvoided: number;
    studentsReactivated: number;
    financeFollowUps: number;
    trialOpportunitiesRecovered: number;
    monthlyManualHours: number;
    absencesRevenue: number;
    reactivationRevenue: number;
    financeRevenue: number;
    salesRevenue: number;
  };
};

export function calculateMoneyOnTable(
  input: CalculatorDefaults,
): MoneyCalculatorResult {
  const activeStudents = Math.max(input.activeStudents, 0);
  const monthlyFee = Math.max(input.averageMonthlyFee, 0);
  const valuePerClassSpot = Math.max(input.averageMonthlyFee / 8, 0);

  const absencesAvoided = Math.max(1, Math.round(activeStudents * 0.28));
  const studentsReactivated = Math.max(1, Math.round(activeStudents * 0.12));
  const financeFollowUps = Math.max(1, Math.round(activeStudents * 0.15));
  const trialOpportunitiesRecovered = Math.max(1, Math.round(activeStudents * 0.1));
  const monthlyManualHours = Math.max(2, Math.round(activeStudents * 0.55));

  const absencesRevenue = absencesAvoided * valuePerClassSpot * 0.85;
  const reactivationRevenue = studentsReactivated * monthlyFee * 0.45;
  const financeRevenue = financeFollowUps * monthlyFee * 0.35;
  const salesRevenue = trialOpportunitiesRecovered * monthlyFee * 0.3;
  const manualTimeValue = monthlyManualHours * ESTIMATED_OPERATIONAL_HOUR_VALUE;

  const atendimento = salesRevenue * 0.22;
  const agenda = absencesRevenue;
  const vendas = salesRevenue * 0.78;
  const financeiro = financeRevenue;
  const retencao = reactivationRevenue;
  const gestao = manualTimeValue * 0.56;
  const historicoEvolucao = manualTimeValue * 0.44;

  const subtotal =
    atendimento +
    agenda +
    vendas +
    financeiro +
    retencao +
    gestao +
    historicoEvolucao;

  return {
    total: Math.round(subtotal),
    breakdown: {
      atendimento: Math.round(atendimento),
      agenda: Math.round(agenda),
      vendas: Math.round(vendas),
      financeiro: Math.round(financeiro),
      retencao: Math.round(retencao),
      gestao: Math.round(gestao),
      historicoEvolucao: Math.round(historicoEvolucao),
    },
    metrics: {
      absencesAvoided,
      studentsReactivated,
      financeFollowUps,
      trialOpportunitiesRecovered,
      monthlyManualHours,
      absencesRevenue: Math.round(absencesRevenue),
      reactivationRevenue: Math.round(reactivationRevenue),
      financeRevenue: Math.round(financeRevenue),
      salesRevenue: Math.round(salesRevenue),
    },
  };
}

export function formatCurrency(value: number) {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
    maximumFractionDigits: 0,
  }).format(value);
}
