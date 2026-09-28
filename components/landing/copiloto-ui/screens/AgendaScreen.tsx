"use client";

import { useState } from "react";

import { MainShell } from "../features/shell/MainShell";
import {
  AgendaGrid,
  type AgendaEntry,
  type DayOption,
} from "../ui/agenda";

/**
 * Tela Agenda copiada de apps/mobile/src/app/(tabs)/agenda.tsx.
 * Dados chegam do fluxo demonstrado na landing; os componentes de tela são do app.
 */
export function AgendaScreen({
  days,
  entries,
  selectedDateId,
}: {
  days: readonly DayOption[];
  entries: readonly AgendaEntry[];
  selectedDateId: string;
}) {
  const [view, setView] = useState<"day" | "week" | "list">("list");

  return (
    <MainShell destination="Agenda">
      <AgendaGrid
        view={view}
        onChangeView={setView}
        selectedDateId={selectedDateId}
        days={days}
        entries={entries}
        emptyState="no-events"
      />
    </MainShell>
  );
}
