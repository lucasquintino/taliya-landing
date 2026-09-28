import { Check, ChevronDown, Search } from "lucide-react";
import type { LucideIcon } from "lucide-react";
import type { Ref, ReactNode } from "react";
import { useEffect, useRef, useState } from "react";
import {
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
  type KeyboardTypeOptions,
  useWindowDimensions,
} from "react-native";

import { fontFamily, uiTokens } from "../tokens";
import { controlElevationStyles } from "../control-elevation";

export type FieldProps = {
  label: string;
  hideLabel?: boolean;
  accessibilityLabel?: string;
  value: string;
  onChangeText: (value: string) => void;
  placeholder?: string;
  helper?: string;
  error?: string | undefined;
  required?: boolean;
  disabled?: boolean;
  readOnly?: boolean;
  multiline?: boolean;
  keyboardType?: KeyboardTypeOptions;
  autoFocus?: boolean;
  autoCapitalize?: "none" | "sentences" | "words" | "characters";
  inputRef?: Ref<TextInput>;
  onBlur?: () => void;
  testID?: string;
  trailingAdornment?: ReactNode;
};

/** Edição controlada: o valor permanece no rascunho do chamador até salvar. */
export function Field({
  label,
  hideLabel = false,
  accessibilityLabel,
  value,
  onChangeText,
  placeholder,
  helper,
  error,
  required = false,
  disabled = false,
  readOnly = false,
  multiline = false,
  keyboardType,
  autoFocus,
  autoCapitalize,
  inputRef,
  onBlur,
  testID,
  trailingAdornment,
}: FieldProps) {
  const locked = disabled || readOnly;
  const guidance = error ?? helper;
  const accessibilityHint = readOnly
    ? guidance
      ? `Somente leitura. ${guidance}`
      : "Somente leitura"
    : guidance;
  const [focused, setFocused] = useState(Boolean(autoFocus && !locked));
  const mounted = useRef(false);
  useEffect(() => {
    mounted.current = true;
    return () => {
      mounted.current = false;
    };
  }, []);
  return (
    <View style={styles.group}>
      {!hideLabel ? <FieldLabel label={label} required={required} /> : null}
      <View>
        <TextInput
          ref={inputRef}
          accessibilityLabel={accessibilityLabel ?? label}
          accessibilityHint={accessibilityHint}
          accessibilityState={{ disabled }}
          autoFocus={autoFocus && !locked}
          autoCapitalize={autoCapitalize}
          editable={!locked}
          keyboardType={keyboardType}
          multiline={multiline}
          onBlur={() => {
            if (mounted.current) setFocused(false);
            onBlur?.();
          }}
          onChangeText={onChangeText}
          onFocus={() => {
            if (mounted.current) setFocused(true);
          }}
          placeholder={placeholder}
          placeholderTextColor={uiTokens.color.textSecondary}
          style={[
            styles.input,
            !locked && controlElevationStyles.resting,
            multiline && styles.multiline,
            trailingAdornment != null && styles.inputWithAdornment,
            focused && !locked && styles.focused,
            error && styles.invalid,
            locked && styles.locked,
          ]}
          testID={testID}
          value={value}
        />
        {trailingAdornment ? (
          <View style={[styles.adornment, { pointerEvents: "none" }]}>
            {trailingAdornment}
          </View>
        ) : null}
      </View>
      {error ? (
        <Text
          accessibilityRole="alert"
          accessibilityLiveRegion="assertive"
          style={styles.error}
        >
          {error}
        </Text>
      ) : helper ? (
        <Text style={styles.helper}>{helper}</Text>
      ) : null}
    </View>
  );
}

/** Rótulo visual compartilhado para campos compostos por mais de um controle. */
export function FieldLabel({
  label,
  required = false,
}: {
  label: string;
  required?: boolean;
}) {
  return (
    <Text style={styles.label}>
      {label}
      {required ? " *" : ""}
    </Text>
  );
}

export function SearchField(props: Omit<FieldProps, "keyboardType">) {
  return (
    <Field
      {...props}
      autoCapitalize="none"
      trailingAdornment={
        <Search
          size={uiTokens.icon.size}
          strokeWidth={uiTokens.icon.strokeWidth}
          color={uiTokens.color.textSecondary}
        />
      }
    />
  );
}

export type SelectFieldProps = {
  label: string;
  value: string | null;
  onPress: () => void;
  placeholder?: string;
  helper?: string;
  error?: string;
  disabled?: boolean;
  readOnly?: boolean;
};

export function SelectField({
  label,
  value,
  onPress,
  placeholder = "Selecione uma opção",
  helper,
  error,
  disabled = false,
  readOnly = false,
}: SelectFieldProps) {
  const [focused, setFocused] = useState(false);
  const locked = disabled || readOnly;
  const staticReadOnly = readOnly && !disabled;
  const guidance = error ?? helper;
  const controlStyle = [
    styles.select,
    !locked && controlElevationStyles.resting,
    focused && !locked && styles.focused,
    error && styles.invalid,
    locked && styles.locked,
  ];
  const controlContent = (
    <>
      <Text
        style={[
          styles.inputText,
          !value && styles.placeholder,
          locked && styles.disabledLabel,
        ]}
      >
        {value ?? placeholder}
      </Text>
      {!staticReadOnly ? (
        <ChevronDown
          size={uiTokens.icon.size}
          strokeWidth={uiTokens.icon.strokeWidth}
          color={uiTokens.color.textSecondary}
        />
      ) : null}
    </>
  );
  return (
    <View style={styles.group}>
      <Text style={styles.label}>{label}</Text>
      {staticReadOnly ? (
        <View
          accessible
          accessibilityRole="text"
          accessibilityLabel={label}
          accessibilityValue={{ text: value ?? "Não selecionado" }}
          accessibilityHint={
            guidance ? `Somente leitura. ${guidance}` : "Somente leitura"
          }
          style={controlStyle}
        >
          {controlContent}
        </View>
      ) : (
        <Pressable
          accessibilityRole="button"
          accessibilityLabel={label}
          accessibilityValue={{ text: value ?? "Não selecionado" }}
          accessibilityHint={guidance ?? "Abre as opções"}
          accessibilityState={{ disabled }}
          disabled={disabled}
          onFocus={() => setFocused(true)}
          onBlur={() => setFocused(false)}
          onPress={onPress}
          style={({ pressed }) => [
            ...controlStyle,
            pressed && !locked && controlElevationStyles.pressed,
            pressed && !locked && styles.selectPressed,
          ]}
        >
          {controlContent}
        </Pressable>
      )}
      {error ? <Text style={styles.error}>{error}</Text> : null}
      {!error && helper ? <Text style={styles.helper}>{helper}</Text> : null}
    </View>
  );
}

export type ChoiceOption = {
  id: string;
  label: string;
  description?: string;
  disabled?: boolean;
};

export type ChoiceGroupProps = {
  label: string;
  options: readonly ChoiceOption[];
  selectedIds: readonly string[];
  selectionMode: "single" | "multiple";
  onChange: (selectedIds: string[]) => void;
  disabled?: boolean;
  readOnly?: boolean;
  error?: string;
};

export function ChoiceGroup({
  label,
  options,
  selectedIds,
  selectionMode,
  onChange,
  disabled = false,
  readOnly = false,
  error,
}: ChoiceGroupProps) {
  const [focusedOptionId, setFocusedOptionId] = useState<string | null>(null);
  return (
    <View
      accessibilityRole={selectionMode === "single" ? "radiogroup" : undefined}
      style={styles.group}
    >
      <Text style={styles.label}>{label}</Text>
      {options.map((option) => {
        const selected = selectedIds.includes(option.id);
        const locked = disabled || readOnly || option.disabled === true;
        return (
          <Pressable
            key={option.id}
            accessibilityRole={
              selectionMode === "single" ? "radio" : "checkbox"
            }
            accessibilityLabel={option.label}
            accessibilityState={{ checked: selected, disabled: locked }}
            disabled={locked}
            onFocus={() => setFocusedOptionId(option.id)}
            onBlur={() => setFocusedOptionId(null)}
            onPress={() => {
              if (selectionMode === "single") {
                onChange([option.id]);
                return;
              }
              onChange(
                selected
                  ? selectedIds.filter((id) => id !== option.id)
                  : [...selectedIds, option.id],
              );
            }}
            style={({ pressed }) => [
              styles.option,
              !locked && controlElevationStyles.resting,
              pressed && !locked && controlElevationStyles.pressed,
              pressed && !locked && styles.optionPressed,
              selected && styles.optionSelected,
              focusedOptionId === option.id && !locked && styles.focused,
              locked && styles.locked,
            ]}
          >
            <View
              style={[
                styles.mark,
                selectionMode === "single" && styles.radioMark,
                selected && styles.markSelected,
              ]}
            >
              {selected && selectionMode === "single" ? (
                <View style={styles.radioCenter} />
              ) : null}
              {selected && selectionMode === "multiple" ? (
                <Check
                  size={14}
                  strokeWidth={3}
                  color={uiTokens.color.onAction}
                />
              ) : null}
            </View>
            <View style={styles.optionCopy}>
              <Text
                style={[styles.optionLabel, locked && styles.disabledLabel]}
              >
                {option.label}
              </Text>
              {option.description ? (
                <Text style={styles.helper}>{option.description}</Text>
              ) : null}
            </View>
          </Pressable>
        );
      })}
      {error ? <Text style={styles.error}>{error}</Text> : null}
    </View>
  );
}

export type SwitchFieldProps = {
  label: string;
  value: boolean;
  onChange: (value: boolean) => void;
  commitMode: "draft" | "explicit-setting";
  description?: string;
  disabled?: boolean;
  saving?: boolean;
  error?: string;
};

export function SwitchField({
  label,
  value,
  onChange,
  commitMode,
  description,
  disabled = false,
  saving = false,
  error,
}: SwitchFieldProps) {
  const locked = disabled || saving;
  const [pressed, setPressed] = useState(false);
  return (
    <View style={styles.group}>
      <Pressable
        accessibilityRole="switch"
        accessibilityLabel={label}
        accessibilityHint={
          commitMode === "draft"
            ? "Altera o rascunho; salve para confirmar"
            : "Solicita alteração desta preferência"
        }
        accessibilityState={{ checked: value, disabled: locked, busy: saving }}
        disabled={locked}
        onPress={() => onChange(!value)}
        onPressIn={() => setPressed(true)}
        onPressOut={() => setPressed(false)}
        style={styles.switchRow}
      >
        <View style={styles.optionCopy}>
          <Text style={styles.optionLabel}>{label}</Text>
          {description ? (
            <Text style={styles.helper}>{description}</Text>
          ) : null}
        </View>
        <View style={[styles.switchTrack, value && styles.switchTrackOn]}>
          <View
            style={[
              styles.switchThumb,
              !locked &&
                (pressed
                  ? controlElevationStyles.pressed
                  : controlElevationStyles.resting),
              value && styles.switchThumbOn,
            ]}
          />
        </View>
      </Pressable>
      {error ? <Text style={styles.error}>{error}</Text> : null}
    </View>
  );
}

export type SegmentOption = {
  id: string;
  label: string;
  icon: LucideIcon;
};

export type SegmentedControlProps = {
  label: string;
  options: readonly SegmentOption[];
  selectedId: string;
  onChange: (id: string) => void;
  disabled?: boolean;
  fitToContainer?: boolean;
};

export function SegmentedControl({
  label,
  options,
  selectedId,
  onChange,
  disabled = false,
  fitToContainer = false,
}: SegmentedControlProps) {
  const [focusedOptionId, setFocusedOptionId] = useState<string | null>(null);
  const { fontScale } = useWindowDimensions();
  const expandForText = fitToContainer && fontScale >= 1.2;
  const segments = (
    <View
      accessibilityRole="radiogroup"
      accessibilityLabel={label}
      style={[
        styles.segments,
        fitToContainer && styles.fitSegments,
        expandForText && styles.expandedSegments,
      ]}
    >
      {options.map((option) => {
        const selected = selectedId === option.id;
        const Icon = option.icon;
        return (
          <Pressable
            key={option.id}
            accessibilityRole="radio"
            accessibilityLabel={option.label}
            accessibilityState={{ checked: selected, disabled }}
            disabled={disabled}
            onFocus={() => setFocusedOptionId(option.id)}
            onBlur={() => setFocusedOptionId(null)}
            onPress={() => onChange(option.id)}
            style={({ pressed }) => [
              styles.segment,
              fitToContainer && styles.fitSegment,
              expandForText && styles.expandedSegment,
              selected &&
                !disabled &&
                !pressed &&
                controlElevationStyles.resting,
              pressed && !disabled && controlElevationStyles.pressed,
              pressed && !disabled && styles.segmentPressed,
              selected &&
                (disabled
                  ? styles.segmentSelectedDisabled
                  : styles.segmentSelected),
              focusedOptionId === option.id &&
                !disabled &&
                styles.segmentFocused,
            ]}
          >
            <View style={styles.segmentContent}>
              <Icon
                aria-hidden="true"
                size={uiTokens.icon.compactSize}
                strokeWidth={uiTokens.icon.strokeWidth}
                color={
                  disabled
                    ? uiTokens.color.disabledForeground
                    : selected
                      ? uiTokens.color.textPrimary
                      : uiTokens.color.textSecondary
                }
              />
              <Text
                style={[
                  styles.segmentLabel,
                  selected && styles.segmentLabelSelected,
                  disabled && styles.disabledLabel,
                ]}
              >
                {option.label}
              </Text>
            </View>
          </Pressable>
        );
      })}
    </View>
  );
  return (
    <View style={styles.group}>
      <Text style={styles.label}>{label}</Text>
      {fitToContainer ? (
        segments
      ) : (
        <ScrollView horizontal showsHorizontalScrollIndicator={false}>
          {segments}
        </ScrollView>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  group: { gap: uiTokens.space.labelToControl },
  label: {
    color: uiTokens.color.textPrimary,
    fontFamily: fontFamily.semibold,
    fontWeight: "600",
    fontSize: uiTokens.typography.scale.label.fontSize,
    lineHeight: uiTokens.typography.scale.label.lineHeight,
  },
  input: {
    minHeight: uiTokens.size.controlMinHeight,
    borderWidth: uiTokens.border.controlHairlineWidth,
    borderColor: uiTokens.color.borderControl,
    borderRadius: uiTokens.radius.control,
    paddingHorizontal: uiTokens.space.controlHorizontal,
    paddingVertical: 10,
    color: uiTokens.color.textPrimary,
    backgroundColor: uiTokens.color.surface,
    fontFamily: fontFamily.regular,
    fontSize: uiTokens.typography.scale.body.fontSize,
    lineHeight: uiTokens.typography.scale.body.lineHeight,
  },
  inputWithAdornment: { paddingRight: uiTokens.size.iconAction },
  adornment: {
    position: "absolute",
    right: uiTokens.space.controlHorizontal,
    top: 0,
    bottom: 0,
    justifyContent: "center",
  },
  inputText: {
    flex: 1,
    color: uiTokens.color.textPrimary,
    fontFamily: fontFamily.regular,
    fontSize: uiTokens.typography.scale.body.fontSize,
    lineHeight: uiTokens.typography.scale.body.lineHeight,
  },
  placeholder: { color: uiTokens.color.textSecondary },
  select: {
    minHeight: uiTokens.size.controlMinHeight,
    borderWidth: uiTokens.border.controlHairlineWidth,
    borderColor: uiTokens.color.borderControl,
    borderRadius: uiTokens.radius.control,
    backgroundColor: uiTokens.color.surface,
    paddingHorizontal: uiTokens.space.controlHorizontal,
    flexDirection: "row",
    alignItems: "center",
    gap: uiTokens.space.iconToText,
  },
  selectPressed: { backgroundColor: uiTokens.color.disabledBackground },
  option: {
    minHeight: uiTokens.size.optionMinHeight,
    borderWidth: uiTokens.border.controlHairlineWidth,
    borderColor: uiTokens.color.borderControl,
    borderRadius: uiTokens.radius.control,
    backgroundColor: uiTokens.color.surface,
    paddingHorizontal: uiTokens.space.relatedItemGap,
    paddingVertical: uiTokens.space.relatedItemGap,
    flexDirection: "row",
    alignItems: "center",
    gap: uiTokens.space.relatedItemGap,
  },
  optionSelected: {
    borderColor: uiTokens.color.action,
  },
  optionPressed: { backgroundColor: uiTokens.color.disabledBackground },
  disabledLabel: { color: uiTokens.color.disabledForeground },
  mark: {
    width: 20,
    height: 20,
    borderWidth: uiTokens.border.normalWidth,
    borderColor: uiTokens.color.borderControl,
    borderRadius: 4,
    alignItems: "center",
    justifyContent: "center",
  },
  radioMark: { borderRadius: 10 },
  markSelected: {
    borderColor: uiTokens.color.action,
    backgroundColor: uiTokens.color.action,
  },
  radioCenter: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: uiTokens.color.onAction,
  },
  optionCopy: { flex: 1, gap: uiTokens.space.feedbackTitleToBody },
  optionLabel: {
    color: uiTokens.color.textPrimary,
    fontFamily: fontFamily.semibold,
    fontWeight: "600",
    fontSize: uiTokens.typography.scale.control.fontSize,
    lineHeight: uiTokens.typography.scale.control.lineHeight,
  },
  switchRow: {
    minHeight: uiTokens.size.optionMinHeight,
    flexDirection: "row",
    alignItems: "center",
    gap: uiTokens.space.relatedItemGap,
  },
  switchTrack: {
    width: 52,
    height: 32,
    borderRadius: 16,
    borderWidth: uiTokens.border.normalWidth,
    borderColor: uiTokens.color.borderControl,
    backgroundColor: uiTokens.color.disabledBackground,
    padding: 3,
  },
  switchTrackOn: {
    backgroundColor: uiTokens.color.action,
    borderColor: uiTokens.color.action,
  },
  switchThumb: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: uiTokens.color.surface,
  },
  switchThumbOn: { alignSelf: "flex-end" },
  segments: {
    flexDirection: "row",
    alignItems: "stretch",
    borderWidth: uiTokens.border.controlHairlineWidth,
    borderColor: uiTokens.color.borderDecorative,
    borderRadius: uiTokens.componentVariantOverrides["CMP-03"].segments.radius,
    backgroundColor: uiTokens.color.disabledBackground,
    padding: uiTokens.componentVariantOverrides["CMP-03"].segments.inset,
  },
  fitSegments: { width: "100%" },
  expandedSegments: { flexDirection: "column" },
  segment: {
    minHeight: uiTokens.componentVariantOverrides["CMP-03"].segments.minHeight,
    minWidth:
      uiTokens.componentVariantOverrides["CMP-03"].segments.minSegmentWidth,
    borderRadius:
      uiTokens.componentVariantOverrides["CMP-03"].segments.activeRadius,
    paddingHorizontal: 8,
    justifyContent: "center",
    alignItems: "center",
    flexDirection: "row",
  },
  fitSegment: { flex: 1, minWidth: 0 },
  expandedSegment: { flex: 0, width: "100%" },
  segmentContent: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: uiTokens.componentVariantOverrides["CMP-03"].segments.iconGap,
    flexShrink: 1,
  },
  segmentSelected: {
    backgroundColor: uiTokens.color.surface,
  },
  segmentSelectedDisabled: { backgroundColor: uiTokens.color.surface },
  segmentPressed: { backgroundColor: uiTokens.color.surface },
  segmentFocused: {
    borderWidth: uiTokens.border.focusSelectedWidth,
    borderColor: uiTokens.color.focus,
  },
  segmentLabel: {
    color: uiTokens.color.textSecondary,
    fontFamily: fontFamily.semibold,
    fontWeight: "600",
    fontSize: uiTokens.componentVariantOverrides["CMP-03"].segments.fontSize,
    lineHeight:
      uiTokens.componentVariantOverrides["CMP-03"].segments.lineHeight,
    textAlign: "center",
    flexShrink: 1,
  },
  segmentLabelSelected: { color: uiTokens.color.textPrimary },
  multiline: {
    minHeight: uiTokens.size.multilineMinHeight,
    textAlignVertical: "top",
  },
  focused: {
    borderWidth: uiTokens.border.focusSelectedWidth,
    borderColor: uiTokens.color.focus,
  },
  locked: {
    backgroundColor: uiTokens.color.disabledBackground,
    borderColor: uiTokens.color.borderDecorative,
    color: uiTokens.color.disabledForeground,
  },
  invalid: { borderColor: uiTokens.color.semantic.rose.foreground },
  helper: {
    color: uiTokens.color.textSecondary,
    fontFamily: fontFamily.regular,
    fontSize: uiTokens.typography.scale.secondary.fontSize,
    lineHeight: uiTokens.typography.scale.secondary.lineHeight,
  },
  error: {
    color: uiTokens.color.semantic.rose.foreground,
    fontFamily: fontFamily.regular,
    fontSize: uiTokens.typography.scale.secondary.fontSize,
    lineHeight: uiTokens.typography.scale.secondary.lineHeight,
  },
});
