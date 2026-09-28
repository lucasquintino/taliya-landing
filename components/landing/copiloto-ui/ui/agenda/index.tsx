import { Bell, CalendarDays, CalendarRange, List } from "lucide-react";
import { useState } from "react";
import {
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
  useWindowDimensions,
} from "react-native";

import { Button } from "../actions";
import { EntityRow } from "../entities";
import {
  ChoiceGroup,
  Field,
  SelectField,
  SegmentedControl,
  SwitchField,
} from "../fields";
import { InlineFeedback } from "../feedback";
import { fontFamily, uiTokens } from "../tokens";

export type ScheduleMode = "once" | "dates" | "recurrence" | "period";
export type ScheduleScope = "this" | "following" | "all";
export type DurationUnit = "minutes" | "hours";
export type ScheduleDateDraft = {
  id: string;
  dateText: string;
  startText: string;
  durationValueText: string;
  endLabel?: string;
};
export type PeriodDayDraft = {
  id: string;
  dateText: string;
  ranges: AvailabilityRangeDraft[];
};
export type AvailabilityRangeDraft = {
  id: string;
  startText: string;
  endText: string;
};
export type ScheduleDraft = {
  mode: ScheduleMode;
  dateText: string;
  startText: string;
  durationValueText: string;
  durationUnit: DurationUnit;
  endLabel?: string;
  endDateText: string;
  dateEntries: ScheduleDateDraft[];
  recurrenceWeekdays: string[];
  scope: ScheduleScope;
  periodHasTimes: boolean;
  periodDays: PeriodDayDraft[];
};

export function createEmptyScheduleDraft(mode: ScheduleMode): ScheduleDraft {
  return {
    mode,
    dateText: "",
    startText: "",
    durationValueText: "",
    durationUnit: "minutes",
    endDateText: "",
    dateEntries: mode === "dates" ? [createEmptyDateEntry()] : [],
    recurrenceWeekdays: [],
    scope: "this",
    periodHasTimes: false,
    periodDays: [],
  };
}

const modes = [
  { id: "once", label: "Uma vez" },
  { id: "dates", label: "Várias datas" },
  { id: "recurrence", label: "Recorrência" },
  { id: "period", label: "Período sem horários" },
] as const;

const weekdays = [
  { id: "monday", label: "Segunda-feira" },
  { id: "tuesday", label: "Terça-feira" },
  { id: "wednesday", label: "Quarta-feira" },
  { id: "thursday", label: "Quinta-feira" },
  { id: "friday", label: "Sexta-feira" },
  { id: "saturday", label: "Sábado" },
  { id: "sunday", label: "Domingo" },
] as const;

const durationUnits = [
  { id: "minutes", label: "Minutos" },
  { id: "hours", label: "Horas" },
] as const;

const scopes = [
  { id: "this", label: "Esta ocorrência" },
  { id: "following", label: "Esta e as seguintes" },
  { id: "all", label: "Todas as ocorrências" },
] as const;

let draftRowCounter = 0;

function createDraftRowId(prefix: string) {
  draftRowCounter += 1;
  return `${prefix}-${draftRowCounter}`;
}

function createEmptyDateEntry(): ScheduleDateDraft {
  return {
    id: createDraftRowId("date"),
    dateText: "",
    startText: "",
    durationValueText: "",
  };
}

export type AgendaEditorProps = {
  draft: ScheduleDraft;
  timezoneLabel: string;
  onChange: (draft: ScheduleDraft) => void;
  onRefreshAvailability?: () => void;
  alternatives?: readonly { id: string; label: string }[];
  onChooseAlternative?: (id: string) => void;
  availabilityState:
    "unknown" | "clear" | "conflict" | "stale" | "outside-cycle";
};

/** Edição local; consulta, aplicação e disponibilidade pertencem à tela chamadora. */
export function AgendaEditor({
  draft,
  timezoneLabel,
  onChange,
  onRefreshAvailability,
  alternatives = [],
  onChooseAlternative,
  availabilityState,
}: AgendaEditorProps) {
  const [mode, setMode] = useState<ScheduleMode>(draft.mode);
  const [modeOpen, setModeOpen] = useState(false);
  const [selectedAlternativeId, setSelectedAlternativeId] = useState("");
  const [draftsByMode, setDraftsByMode] = useState<
    Record<ScheduleMode, ScheduleDraft>
  >(() => ({
    once: createEmptyScheduleDraft("once"),
    dates: createEmptyScheduleDraft("dates"),
    recurrence: createEmptyScheduleDraft("recurrence"),
    period: createEmptyScheduleDraft("period"),
    [draft.mode]: draft,
  }));
  const activeDraft = mode === draft.mode ? draft : draftsByMode[mode];
  const updateDraft = (updates: Partial<ScheduleDraft>) => {
    const nextDraft = { ...activeDraft, ...updates, mode };
    setDraftsByMode((current) => ({ ...current, [mode]: nextDraft }));
    onChange(nextDraft);
  };
  const updateDateEntry = (id: string, updates: Partial<ScheduleDateDraft>) => {
    updateDraft({
      dateEntries: activeDraft.dateEntries.map((entry) =>
        entry.id === id ? { ...entry, ...updates } : entry,
      ),
    });
  };
  const updatePeriodDay = (id: string, updates: Partial<PeriodDayDraft>) => {
    updateDraft({
      periodDays: activeDraft.periodDays.map((day) =>
        day.id === id ? { ...day, ...updates } : day,
      ),
    });
  };
  const changeMode = (nextMode: string) => {
    const selectedMode = nextMode as ScheduleMode;
    setDraftsByMode((current) => ({ ...current, [draft.mode]: draft }));
    const nextDraft = draftsByMode[selectedMode];
    setMode(selectedMode);
    setSelectedAlternativeId("");
    onChange(nextDraft);
  };

  return (
    <View style={styles.section}>
      <SelectField
        label="Quando"
        value={modes.find((option) => option.id === mode)?.label ?? null}
        onPress={() => setModeOpen((open) => !open)}
      />
      {modeOpen ? (
        <ChoiceGroup
          label="Forma de agendamento"
          options={modes}
          selectedIds={[mode]}
          selectionMode="single"
          onChange={([selectedMode]) => {
            if (selectedMode) {
              changeMode(selectedMode);
              setModeOpen(false);
            }
          }}
        />
      ) : null}
      {mode === "once" || mode === "recurrence" ? (
        <>
          <Field
            label={mode === "recurrence" ? "A partir de" : "Data"}
            value={activeDraft.dateText}
            placeholder="DD/MM/AAAA"
            helper="Digite a data. Um seletor de calendário será usado quando estiver disponível."
            onChangeText={(dateText) => updateDraft({ dateText })}
          />
          <Field
            label="Horário de início"
            value={activeDraft.startText}
            placeholder="HH:MM"
            helper="Digite o horário no formato 24 horas."
            onChangeText={(startText) => updateDraft({ startText })}
          />
          <ScheduleDurationFields
            value={activeDraft.durationValueText}
            unit={activeDraft.durationUnit}
            endLabel={activeDraft.endLabel}
            onChangeValue={(durationValueText) =>
              updateDraft({ durationValueText })
            }
            onChangeUnit={(durationUnit) => updateDraft({ durationUnit })}
          />
          {mode === "recurrence" ? (
            <>
              <ChoiceGroup
                label="Repetir nos dias"
                options={weekdays}
                selectedIds={activeDraft.recurrenceWeekdays}
                selectionMode="multiple"
                onChange={(recurrenceWeekdays) =>
                  updateDraft({ recurrenceWeekdays })
                }
              />
              <ChoiceGroup
                label="Aplicar alteração a"
                options={scopes}
                selectedIds={[activeDraft.scope]}
                selectionMode="single"
                onChange={([scope]) => {
                  if (scope) updateDraft({ scope: scope as ScheduleScope });
                }}
              />
            </>
          ) : null}
        </>
      ) : null}
      {mode === "dates" ? (
        <View style={styles.section}>
          <Text style={styles.title}>Datas e horários</Text>
          {activeDraft.dateEntries.map((entry, index) => (
            <View key={entry.id} style={styles.draftGroup}>
              <Text style={styles.caption}>Data {index + 1}</Text>
              <Field
                label="Data"
                value={entry.dateText}
                placeholder="DD/MM/AAAA"
                helper="Digite a data. Um seletor de calendário será usado quando estiver disponível."
                onChangeText={(dateText) =>
                  updateDateEntry(entry.id, { dateText })
                }
              />
              <Field
                label="Horário de início"
                value={entry.startText}
                placeholder="HH:MM"
                helper="Digite o horário no formato 24 horas."
                onChangeText={(startText) =>
                  updateDateEntry(entry.id, { startText })
                }
              />
              <ScheduleDurationFields
                value={entry.durationValueText}
                unit={activeDraft.durationUnit}
                endLabel={entry.endLabel}
                onChangeValue={(durationValueText) =>
                  updateDateEntry(entry.id, { durationValueText })
                }
                onChangeUnit={(durationUnit) => updateDraft({ durationUnit })}
              />
              {activeDraft.dateEntries.length > 1 ? (
                <Button
                  label={`Remover data ${index + 1}`}
                  variant="secondary"
                  onPress={() =>
                    updateDraft({
                      dateEntries: activeDraft.dateEntries.filter(
                        (item) => item.id !== entry.id,
                      ),
                    })
                  }
                />
              ) : null}
            </View>
          ))}
          <Button
            label="Adicionar data"
            variant="secondary"
            onPress={() =>
              updateDraft({
                dateEntries: [
                  ...activeDraft.dateEntries,
                  createEmptyDateEntry(),
                ],
              })
            }
          />
        </View>
      ) : null}
      {mode === "period" ? (
        <>
          <Field
            label="Início do período"
            value={activeDraft.dateText}
            placeholder="DD/MM/AAAA"
            helper="Digite a data. Um seletor de calendário será usado quando estiver disponível."
            onChangeText={(dateText) => updateDraft({ dateText })}
          />
          <Field
            label="Fim do período"
            value={activeDraft.endDateText}
            placeholder="DD/MM/AAAA"
            helper="Digite a data. Um seletor de calendário será usado quando estiver disponível."
            onChangeText={(endDateText) => updateDraft({ endDateText })}
          />
          <SwitchField
            label="Informar horários por dia"
            value={activeDraft.periodHasTimes}
            commitMode="draft"
            description="Sem horários, o período não ocupa blocos na agenda."
            onChange={(periodHasTimes) =>
              updateDraft({
                periodHasTimes,
                periodDays:
                  periodHasTimes && activeDraft.periodDays.length === 0
                    ? [createEmptyPeriodDay()]
                    : activeDraft.periodDays,
              })
            }
          />
          {activeDraft.periodHasTimes ? (
            <View style={styles.section}>
              <Text style={styles.title}>Faixas por dia</Text>
              {activeDraft.periodDays.map((day, index) => (
                <View key={day.id} style={styles.draftGroup}>
                  <Text style={styles.caption}>Dia {index + 1}</Text>
                  <Field
                    label="Data"
                    value={day.dateText}
                    placeholder="DD/MM/AAAA"
                    onChangeText={(dateText) =>
                      updatePeriodDay(day.id, { dateText })
                    }
                  />
                  {day.ranges.map((range, rangeIndex) => (
                    <TimeRangeFields
                      key={range.id}
                      label={`Faixa ${rangeIndex + 1}`}
                      range={range}
                      onChange={(updates) =>
                        updatePeriodDay(day.id, {
                          ranges: day.ranges.map((item) =>
                            item.id === range.id
                              ? { ...item, ...updates }
                              : item,
                          ),
                        })
                      }
                      onRemove={() =>
                        updatePeriodDay(day.id, {
                          ranges: day.ranges.filter(
                            (item) => item.id !== range.id,
                          ),
                        })
                      }
                      canRemove={day.ranges.length > 1}
                    />
                  ))}
                  <Button
                    label="Adicionar faixa neste dia"
                    variant="secondary"
                    onPress={() =>
                      updatePeriodDay(day.id, {
                        ranges: [
                          ...day.ranges,
                          createEmptyRange("period-range"),
                        ],
                      })
                    }
                  />
                  {activeDraft.periodDays.length > 1 ? (
                    <Button
                      label={`Remover dia ${index + 1}`}
                      variant="secondary"
                      onPress={() =>
                        updateDraft({
                          periodDays: activeDraft.periodDays.filter(
                            (item) => item.id !== day.id,
                          ),
                        })
                      }
                    />
                  ) : null}
                </View>
              ))}
              <Button
                label="Adicionar dia ao período"
                variant="secondary"
                onPress={() =>
                  updateDraft({
                    periodDays: [
                      ...activeDraft.periodDays,
                      createEmptyPeriodDay(),
                    ],
                  })
                }
              />
            </View>
          ) : null}
        </>
      ) : null}
      <Text style={styles.caption}>Fuso horário: {timezoneLabel}</Text>
      {availabilityState === "conflict" ? (
        <InlineFeedback
          kind="caution"
          title="Este horário conflita com a agenda"
          message="Seu pedido continua preservado. Consulte a disponibilidade ou escolha uma alternativa antes de aplicar."
        />
      ) : availabilityState === "stale" ? (
        <InlineFeedback
          kind="caution"
          title="A disponibilidade pode ter mudado"
          message="Seu pedido continua preservado. Consulte novamente antes de aplicar."
        />
      ) : availabilityState === "outside-cycle" ? (
        <InlineFeedback
          kind="caution"
          title="Data fora do ciclo atual"
          message="Confira as condições do Serviço antes de aplicar este rascunho."
        />
      ) : availabilityState === "unknown" ? (
        <InlineFeedback
          kind="information"
          title="Disponibilidade não consultada"
          message="O rascunho está preservado; ainda não há confirmação de horário livre."
        />
      ) : availabilityState === "clear" ? (
        <InlineFeedback
          kind="success"
          title="Disponibilidade consultada"
          message="Não foi encontrado conflito nesta consulta."
        />
      ) : null}
      {availabilityState === "conflict" && alternatives.length > 0 ? (
        <>
          <ChoiceGroup
            label="Horários alternativos disponíveis"
            options={alternatives}
            selectedIds={selectedAlternativeId ? [selectedAlternativeId] : []}
            selectionMode="single"
            onChange={([id]) => setSelectedAlternativeId(id ?? "")}
          />
          {onChooseAlternative ? (
            <Button
              label="Reconsultar alternativa"
              variant="secondary"
              disabled={!selectedAlternativeId}
              onPress={() => onChooseAlternative(selectedAlternativeId)}
            />
          ) : null}
        </>
      ) : null}
      {availabilityState === "stale" && onRefreshAvailability ? (
        <Button
          label="Consultar disponibilidade novamente"
          variant="secondary"
          onPress={onRefreshAvailability}
        />
      ) : null}
      {mode === "once" && !activeDraft.durationValueText ? (
        <InlineFeedback
          kind="information"
          title="Duração ainda não informada"
          message="O horário permanece provisório até que a duração seja definida."
        />
      ) : null}
    </View>
  );
}

function createEmptyRange(prefix: string): AvailabilityRangeDraft {
  return {
    id: createDraftRowId(prefix),
    startText: "",
    endText: "",
  };
}

function createEmptyPeriodDay(): PeriodDayDraft {
  return {
    id: createDraftRowId("period-day"),
    dateText: "",
    ranges: [createEmptyRange("period-range")],
  };
}

function ScheduleDurationFields({
  value,
  unit,
  endLabel,
  onChangeValue,
  onChangeUnit,
}: {
  value: string;
  unit: DurationUnit;
  endLabel?: string;
  onChangeValue: (value: string) => void;
  onChangeUnit: (unit: DurationUnit) => void;
}) {
  return (
    <View style={styles.section}>
      <Field
        label="Duração"
        value={value}
        placeholder="Ex.: 50"
        keyboardType="numeric"
        onChangeText={onChangeValue}
      />
      <ChoiceGroup
        label="Unidade da duração"
        options={durationUnits}
        selectedIds={[unit]}
        selectionMode="single"
        onChange={([id]) => {
          if (id) onChangeUnit(id as DurationUnit);
        }}
      />
      {endLabel ? (
        <Text style={styles.caption}>Término previsto: {endLabel}</Text>
      ) : null}
    </View>
  );
}

function TimeRangeFields({
  label,
  range,
  onChange,
  onRemove,
  canRemove,
}: {
  label: string;
  range: AvailabilityRangeDraft;
  onChange: (updates: Partial<AvailabilityRangeDraft>) => void;
  onRemove: () => void;
  canRemove: boolean;
}) {
  return (
    <View style={styles.draftGroup}>
      <Text style={styles.caption}>{label}</Text>
      <Field
        label="De"
        value={range.startText}
        placeholder="HH:MM"
        helper="Digite no formato 24 horas."
        onChangeText={(startText) => onChange({ startText })}
      />
      <Field
        label="Até"
        value={range.endText}
        placeholder="HH:MM"
        helper="Digite no formato 24 horas."
        onChangeText={(endText) => onChange({ endText })}
      />
      {canRemove ? (
        <Button
          label={`Remover ${label.toLowerCase()}`}
          variant="secondary"
          onPress={onRemove}
        />
      ) : null}
    </View>
  );
}

export type DayOption = {
  id: string;
  weekday: string;
  dayNumber: string;
  fullDate: string;
};

export function DaySelector({
  days,
  selectedId,
  onSelect,
}: {
  days: readonly DayOption[];
  selectedId: string;
  onSelect: (id: string) => void;
}) {
  return (
    <ScrollView
      horizontal
      showsHorizontalScrollIndicator={false}
      contentContainerStyle={styles.days}
    >
      {days.map((day) => {
        const selected = day.id === selectedId;
        return (
          <Pressable
            key={day.id}
            accessibilityRole="radio"
            accessibilityLabel={day.fullDate}
            accessibilityState={{ checked: selected }}
            onPress={() => onSelect(day.id)}
            style={[styles.day, selected && styles.daySelected]}
          >
            <Text style={[styles.caption, selected && styles.daySelectedText]}>
              {day.weekday}
            </Text>
            <Text
              style={[styles.dayNumber, selected && styles.daySelectedText]}
            >
              {day.dayNumber}
            </Text>
          </Pressable>
        );
      })}
    </ScrollView>
  );
}

type AgendaEntryBase = {
  id: string;
  dateId: string;
  title: string;
  detail: string;
  onOpen?: () => void;
};

export type AgendaEntry =
  | (AgendaEntryBase & {
      kind: "timed";
      startMinute: number;
      endMinute: number;
    })
  | (AgendaEntryBase & { kind: "period" })
  | (AgendaEntryBase & { kind: "due"; dueMinute?: number });

const hourHeight = uiTokens.size.touchTargetMin + uiTokens.space.componentGap;

function clockLabel(minute: number) {
  return `${Math.floor(minute / 60)}h${String(minute % 60).padStart(2, "0")}`;
}

function weekHourRange(entries: readonly AgendaEntry[]) {
  const timed = entries.filter((entry) => entry.kind === "timed");
  if (timed.length === 0) return { first: 9, last: 18 };
  return {
    first: Math.max(
      0,
      Math.floor(Math.min(...timed.map((entry) => entry.startMinute)) / 60) - 2,
    ),
    last: Math.min(
      24,
      Math.max(
        Math.ceil(Math.max(...timed.map((entry) => entry.endMinute)) / 60),
        Math.floor(Math.min(...timed.map((entry) => entry.startMinute)) / 60) +
          2,
      ),
    ),
  };
}

function WeekTimeline({
  days,
  entries,
}: {
  days: readonly DayOption[];
  entries: readonly AgendaEntry[];
}) {
  const datedEntries = entries.filter((entry) =>
    days.some((day) => day.id === entry.dateId),
  );
  const { first, last } = weekHourRange(datedEntries);
  const hours = Array.from(
    { length: last - first + 1 },
    (_, index) => first + index,
  );
  return (
    <ScrollView
      horizontal
      showsHorizontalScrollIndicator={false}
      accessibilityLabel="Grade semanal com horários"
      contentContainerStyle={styles.weekColumns}
    >
      <View style={styles.weekTimeColumn}>
        <View style={styles.weekHeader} />
        {hours.map((hour) => (
          <Text key={hour} style={[styles.caption, styles.weekHour]}>
            {hour}h
          </Text>
        ))}
      </View>
      {days.map((day) => (
        <View key={day.id} style={styles.weekColumn}>
          <Text style={[styles.caption, styles.weekHeader]}>
            {day.weekday} {day.dayNumber}
          </Text>
          <View style={{ height: (last - first) * hourHeight }}>
            {hours.slice(0, -1).map((hour) => (
              <View
                key={hour}
                style={[styles.weekRule, { top: (hour - first) * hourHeight }]}
              />
            ))}
            {datedEntries
              .filter(
                (entry): entry is Extract<AgendaEntry, { kind: "timed" }> =>
                  entry.dateId === day.id && entry.kind === "timed",
              )
              .map((entry) => (
                <View
                  key={entry.id}
                  style={[
                    styles.weekEvent,
                    {
                      top: ((entry.startMinute - first * 60) / 60) * hourHeight,
                      height: Math.max(
                        uiTokens.size.touchTargetMin,
                        ((entry.endMinute - entry.startMinute) / 60) *
                          hourHeight,
                      ),
                    },
                  ]}
                >
                  <AgendaEntryRow entry={entry} compact />
                </View>
              ))}
          </View>
        </View>
      ))}
    </ScrollView>
  );
}

function DayTimeline({ entries }: { entries: readonly AgendaEntry[] }) {
  const timed = entries.filter(
    (entry): entry is Extract<AgendaEntry, { kind: "timed" }> =>
      entry.kind === "timed",
  );
  const due = entries.filter(
    (
      entry,
    ): entry is Extract<AgendaEntry, { kind: "due" }> & {
      dueMinute: number;
    } => entry.kind === "due" && entry.dueMinute != null,
  );
  const timedRange = weekHourRange(timed);
  const firstDueHour = due.length
    ? Math.floor(Math.min(...due.map((entry) => entry.dueMinute)) / 60)
    : null;
  const lastDueHour = due.length
    ? Math.ceil(Math.max(...due.map((entry) => entry.dueMinute)) / 60)
    : null;
  const first =
    firstDueHour === null
      ? timedRange.first
      : timed.length
        ? Math.max(0, Math.min(timedRange.first, firstDueHour - 1))
        : Math.max(0, firstDueHour - 2);
  const last =
    lastDueHour === null
      ? timedRange.last
      : timed.length
        ? Math.min(24, Math.max(timedRange.last, lastDueHour + 1))
        : Math.min(24, Math.max(lastDueHour + 2, first + 4));
  const hours = Array.from({ length: last - first + 1 }, (_, i) => first + i);
  return (
    <View
      style={[
        styles.dayTimeline,
        {
          height:
            (last - first) * hourHeight +
            uiTokens.typography.scale.caption.lineHeight,
        },
      ]}
    >
      {hours.map((hour) => (
        <View
          key={hour}
          style={[styles.dayHourRow, { top: (hour - first) * hourHeight }]}
        >
          <Text style={styles.caption}>{hour}h</Text>
          <View style={styles.dayHourRule} />
        </View>
      ))}
      {due.map((entry) => (
        <View
          key={entry.id}
          style={[
            styles.dayReminder,
            {
              top: ((entry.dueMinute - first * 60) / 60) * hourHeight,
            },
          ]}
        >
          <Bell
            size={uiTokens.icon.compactSize}
            strokeWidth={uiTokens.icon.strokeWidth}
            color={uiTokens.color.textSecondary}
          />
          <Text style={styles.dayReminderText}>
            {clockLabel(entry.dueMinute)} · {entry.title}
          </Text>
        </View>
      ))}
      {timed.map((entry) => (
        <View
          key={entry.id}
          style={[
            styles.dayEvent,
            {
              top: ((entry.startMinute - first * 60) / 60) * hourHeight,
              height: Math.max(
                uiTokens.size.touchTargetMin,
                ((entry.endMinute - entry.startMinute) / 60) * hourHeight,
              ),
            },
          ]}
        >
          <AgendaEntryRow entry={entry} compact />
        </View>
      ))}
    </View>
  );
}

function DayAgendaView({
  selectedDateId,
  days,
  entries,
  emptyState,
}: {
  selectedDateId: string;
  days: readonly DayOption[];
  entries: readonly AgendaEntry[];
  emptyState: AgendaEmptyState;
}) {
  const { fontScale } = useWindowDimensions();
  const expandedText = fontScale >= 1.5;
  const selectedDate = days.find((day) => day.id === selectedDateId);
  const dated = entries.filter((entry) => entry.dateId === selectedDateId);
  const timelineEntries = dated.filter(
    (entry) =>
      entry.kind === "timed" ||
      (entry.kind === "due" && entry.dueMinute != null && !expandedText),
  );
  return (
    <View style={styles.section}>
      {selectedDate ? (
        <Text style={styles.caption}>{selectedDate.fullDate}</Text>
      ) : null}
      {dated
        .filter(
          (entry) =>
            entry.kind === "period" ||
            (entry.kind === "due" && (entry.dueMinute == null || expandedText)),
        )
        .map((entry) => (
          <EntityRow
            key={entry.id}
            entityType={entry.kind === "period" ? "occurrence" : "reminder"}
            presentation="card"
            title={
              entry.kind === "due" && entry.dueMinute != null
                ? `${clockLabel(entry.dueMinute)} · ${entry.title}`
                : entry.title
            }
            secondary={entry.detail}
            {...(entry.onOpen ? { onOpen: entry.onOpen } : {})}
          />
        ))}
      {dated.length === 0 ? <AgendaEmptyMessage state={emptyState} /> : null}
      {timelineEntries.length > 0 ? (
        <DayTimeline entries={timelineEntries} />
      ) : null}
    </View>
  );
}

export type AgendaEmptyState =
  "no-events" | "availability-not-configured" | "not-consulted";

function AgendaEmptyMessage({ state }: { state: AgendaEmptyState }) {
  const copy =
    state === "availability-not-configured"
      ? {
          title: "Horário de atendimento não configurado",
          message: "Cadastre os dias e as faixas em que o negócio atende.",
        }
      : state === "not-consulted"
        ? {
            title: "Disponibilidade ainda não consultada",
            message: "Ainda não há uma consulta para este período.",
          }
        : {
            title: "Nenhum evento neste período",
            message: "Não há compromissos ou lembretes para mostrar.",
          };
  return (
    <InlineFeedback
      kind="information"
      title={copy.title}
      message={copy.message}
    />
  );
}

export function AgendaGrid({
  view,
  onChangeView,
  selectedDateId,
  days,
  entries,
  emptyState = "no-events",
}: {
  view: "day" | "week" | "list";
  onChangeView: (view: "day" | "week" | "list") => void;
  selectedDateId: string;
  days: readonly DayOption[];
  entries: readonly AgendaEntry[];
  emptyState?: AgendaEmptyState;
}) {
  return (
    <View style={styles.section}>
      <SegmentedControl
        label="Visualização da agenda"
        fitToContainer
        options={[
          { id: "day", label: "Dia", icon: CalendarDays },
          { id: "week", label: "Semana", icon: CalendarRange },
          { id: "list", label: "Lista", icon: List },
        ]}
        selectedId={view}
        onChange={(id) => onChangeView(id as "day" | "week" | "list")}
      />
      {view === "week" ? (
        entries.length === 0 ? (
          <AgendaEmptyMessage state={emptyState} />
        ) : (
          <WeekTimeline days={days} entries={entries} />
        )
      ) : view === "list" ? (
        entries.length === 0 ? (
          <AgendaEmptyMessage state={emptyState} />
        ) : (
          days.map((day) => {
            const dated = entries.filter((entry) => entry.dateId === day.id);
            return dated.length === 0 ? null : (
              <View key={day.id} style={styles.section}>
                <Text style={styles.title}>{day.fullDate}</Text>
                {dated.map((entry) => (
                  <AgendaEntryRow key={entry.id} entry={entry} />
                ))}
              </View>
            );
          })
        )
      ) : (
        <DayAgendaView
          selectedDateId={selectedDateId}
          days={days}
          entries={entries}
          emptyState={emptyState}
        />
      )}
      {view === "week"
        ? entries
            .filter((entry) => entry.kind !== "timed")
            .map((entry) => <AgendaEntryRow key={entry.id} entry={entry} />)
        : null}
    </View>
  );
}

function AgendaEntryRow({
  entry,
  compact = false,
}: {
  entry: AgendaEntry;
  compact?: boolean;
}) {
  const content = (
    <>
      <Text style={styles.entryTitle}>{entry.title}</Text>
      <Text style={styles.caption}>{entry.detail}</Text>
    </>
  );
  const rowStyle = compact ? styles.weekEntry : styles.entry;
  if (!entry.onOpen) return <View style={rowStyle}>{content}</View>;
  return (
    <Pressable
      accessibilityRole="button"
      accessibilityLabel={entry.title}
      onPress={entry.onOpen}
      style={rowStyle}
    >
      {content}
    </Pressable>
  );
}

export type AvailabilityDayDraft = {
  id: string;
  weekday: string;
  enabled: boolean;
  ranges: AvailabilityRangeDraft[];
};

export type AvailabilityDraft = {
  days: AvailabilityDayDraft[];
};

export function createAvailabilityDraft(): AvailabilityDraft {
  return {
    days: weekdays.map((day, index) => ({
      id: day.id,
      weekday: day.label,
      enabled: index < 5,
      ranges:
        index === 0
          ? [
              {
                id: "availability-monday-morning",
                startText: "09:00",
                endText: "12:00",
              },
              {
                id: "availability-monday-afternoon",
                startText: "13:00",
                endText: "18:00",
              },
            ]
          : index < 5
            ? [
                {
                  id: `availability-${day.id}-range-1`,
                  startText: "09:00",
                  endText: "18:00",
                },
              ]
            : [],
    })),
  };
}

export function AvailabilityEditor({
  draft,
  onChange,
}: {
  draft: AvailabilityDraft;
  onChange: (draft: AvailabilityDraft) => void;
}) {
  const updateDay = (id: string, updates: Partial<AvailabilityDayDraft>) => {
    onChange({
      ...draft,
      days: draft.days.map((day) =>
        day.id === id ? { ...day, ...updates } : day,
      ),
    });
  };
  const copyMondayToWeekdays = () => {
    const monday = draft.days.find((day) => day.id === "monday");
    if (!monday?.enabled || monday.ranges.length === 0) return;
    onChange({
      days: draft.days.map((day) =>
        ["tuesday", "wednesday", "thursday", "friday"].includes(day.id)
          ? {
              ...day,
              enabled: true,
              ranges: monday.ranges.map((range) => ({
                ...range,
                id: createDraftRowId(`availability-${day.id}`),
              })),
            }
          : day,
      ),
    });
  };
  return (
    <View style={styles.section}>
      <Text style={styles.title}>Horário de atendimento</Text>
      <Text style={styles.caption}>
        Ative os dias de atendimento e informe uma ou mais faixas por dia.
      </Text>
      {draft.days.map((day) => (
        <View key={day.id} style={styles.draftGroup}>
          <SwitchField
            label={day.weekday}
            value={day.enabled}
            commitMode="draft"
            description={day.enabled ? "Atendimento ativo" : "Sem atendimento"}
            onChange={(enabled) =>
              updateDay(day.id, {
                enabled,
                ranges:
                  enabled && day.ranges.length === 0
                    ? [createEmptyRange("availability-range")]
                    : day.ranges,
              })
            }
          />
          {day.enabled ? (
            <>
              {day.ranges.map((range, index) => (
                <TimeRangeFields
                  key={range.id}
                  label={`Faixa ${index + 1}`}
                  range={range}
                  onChange={(updates) =>
                    updateDay(day.id, {
                      ranges: day.ranges.map((item) =>
                        item.id === range.id ? { ...item, ...updates } : item,
                      ),
                    })
                  }
                  onRemove={() =>
                    updateDay(day.id, {
                      ranges: day.ranges.filter((item) => item.id !== range.id),
                    })
                  }
                  canRemove={day.ranges.length > 1}
                />
              ))}
              <Button
                label={`Adicionar faixa em ${day.weekday.toLowerCase()}`}
                variant="secondary"
                onPress={() =>
                  updateDay(day.id, {
                    ranges: [
                      ...day.ranges,
                      createEmptyRange("availability-range"),
                    ],
                  })
                }
              />
            </>
          ) : null}
        </View>
      ))}
      <Button
        label="Copiar horários de segunda a sexta"
        variant="secondary"
        disabled={
          !draft.days.find((day) => day.id === "monday")?.enabled ||
          (draft.days.find((day) => day.id === "monday")?.ranges.length ??
            0) === 0
        }
        onPress={copyMondayToWeekdays}
      />
    </View>
  );
}

const selector = uiTokens.componentVariantOverrides["CMP-10"].daySelector;
const styles = StyleSheet.create({
  section: { gap: uiTokens.space.componentGap },
  draftGroup: {
    gap: uiTokens.space.relatedItemGap,
    paddingTop: uiTokens.space.relatedItemGap,
    borderTopWidth: uiTokens.border.controlHairlineWidth,
    borderColor: uiTokens.color.borderDecorative,
  },
  title: {
    color: uiTokens.color.textPrimary,
    fontFamily: fontFamily.semibold,
    fontWeight: "600",
    fontSize: uiTokens.typography.scale.control.fontSize,
    lineHeight: uiTokens.typography.scale.control.lineHeight,
  },
  caption: {
    color: uiTokens.color.textSecondary,
    fontFamily: fontFamily.regular,
    fontSize: uiTokens.typography.scale.caption.fontSize,
    lineHeight: uiTokens.typography.scale.caption.lineHeight,
  },
  days: { gap: uiTokens.space.relatedItemGap },
  day: {
    minWidth: selector.hitTargetMin,
    minHeight: selector.height,
    borderRadius: uiTokens.radius.control,
    backgroundColor: uiTokens.color.surface,
    alignItems: "center",
    justifyContent: "center",
  },
  daySelected: { backgroundColor: uiTokens.color.action },
  daySelectedText: { color: uiTokens.color.onAction },
  dayNumber: {
    color: uiTokens.color.textPrimary,
    fontFamily: fontFamily.semibold,
    fontWeight: "600",
    fontSize: uiTokens.typography.scale.control.fontSize,
    lineHeight: uiTokens.typography.scale.control.lineHeight,
  },
  weekColumns: { gap: uiTokens.space.relatedItemGap },
  weekTimeColumn: { width: uiTokens.size.iconAction },
  weekHeader: {
    height: uiTokens.size.touchTargetMin,
    textAlign: "center",
    textAlignVertical: "center",
  },
  weekHour: { height: hourHeight },
  weekColumn: {
    width: Math.round(selector.baseContentWidth / 3),
  },
  weekRule: {
    position: "absolute",
    left: 0,
    right: 0,
    borderTopWidth: uiTokens.border.normalWidth,
    borderColor: uiTokens.color.borderDecorative,
  },
  weekEvent: {
    position: "absolute",
    left: uiTokens.space.feedbackTitleToBody,
    right: uiTokens.space.feedbackTitleToBody,
  },
  weekEntry: {
    flex: 1,
    padding: uiTokens.space.relatedRowGap,
    borderRadius: uiTokens.radius.control,
    backgroundColor: uiTokens.color.semantic.blue.background,
    gap: uiTokens.space.feedbackTitleToBody,
  },
  dayTimeline: { position: "relative" },
  dayHourRow: {
    position: "absolute",
    left: 0,
    right: 0,
    flexDirection: "row",
    alignItems: "center",
    gap: uiTokens.space.relatedItemGap,
  },
  dayHourRule: {
    flex: 1,
    borderTopWidth: uiTokens.border.normalWidth,
    borderColor: uiTokens.color.borderDecorative,
  },
  dayReminder: {
    position: "absolute",
    left: uiTokens.size.iconAction,
    right: 0,
    flexDirection: "row",
    alignItems: "center",
    gap: uiTokens.space.relatedItemGap,
  },
  dayReminderText: {
    flexShrink: 1,
    color: uiTokens.color.textPrimary,
    fontFamily: fontFamily.regular,
    fontSize: uiTokens.typography.scale.caption.fontSize,
    lineHeight: uiTokens.typography.scale.caption.lineHeight,
  },
  dayEvent: {
    position: "absolute",
    left: uiTokens.size.iconAction,
    right: 0,
  },
  entry: {
    minHeight: uiTokens.size.touchTargetMin,
    padding: uiTokens.space.relatedItemGap,
    borderRadius: uiTokens.radius.control,
    backgroundColor: uiTokens.color.semantic.blue.background,
    gap: uiTokens.space.feedbackTitleToBody,
  },
  entryTitle: {
    color: uiTokens.color.textPrimary,
    fontFamily: fontFamily.semibold,
    fontWeight: "600",
    fontSize: uiTokens.typography.scale.secondary.fontSize,
    lineHeight: uiTokens.typography.scale.secondary.lineHeight,
  },
});
