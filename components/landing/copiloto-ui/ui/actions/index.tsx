import { useState } from "react";
import type { ReactNode } from "react";
import {
  ActivityIndicator,
  Pressable,
  StyleSheet,
  Text,
  View,
} from "react-native";

import { fontFamily, uiTokens } from "../tokens";
import { controlElevationStyles } from "../control-elevation";

export type ButtonVariant =
  "primary" | "secondary" | "text" | "danger" | "dangerText";

export type ButtonProps = {
  label: string;
  onPress?: () => void;
  variant?: ButtonVariant;
  disabled?: boolean;
  loading?: boolean;
  icon?: ReactNode;
  iconPosition?: "leading" | "trailing";
  /** Centraliza ícone e rótulo como um único grupo dentro do botão. */
  centeredIconGroup?: boolean;
  contextual?: boolean;
  accessibilityLabel?: string;
  accessibilityHint?: string;
  /** Permite capturar o mesmo estilo de pressão no catálogo de desenvolvimento. */
  previewPressed?: boolean;
  testID?: string;
};

export type IconActionProps = {
  label: string;
  icon: ReactNode;
  onPress: () => void;
  appearance?: "surface" | "plain";
  edgeAlignment?: "leading" | "trailing" | "center";
  disabled?: boolean;
  /** Permite mostrar pressão/foco na prévia de desenvolvimento do catálogo. */
  previewPressed?: boolean;
  previewFocused?: boolean;
  testID?: string;
};

/** A ação visual não interpreta o resultado de uma operação nem anuncia sucesso. */
export function Button({
  label,
  onPress,
  variant = "primary",
  disabled = false,
  loading = false,
  icon,
  iconPosition = "leading",
  centeredIconGroup = false,
  contextual = false,
  accessibilityLabel,
  accessibilityHint,
  previewPressed = false,
  testID,
}: ButtonProps) {
  const [focused, setFocused] = useState(false);
  const disabledLook = disabled || !onPress;
  const blocked = disabledLook || loading;
  const primary = variant === "primary";
  const danger = variant === "danger";
  const dangerText = variant === "dangerText";
  const textVariant = variant === "text" || dangerText;
  const foreground = disabledLook
    ? uiTokens.color.disabledForeground
    : primary
      ? uiTokens.color.onAction
      : danger || dangerText
        ? uiTokens.color.semantic.rose.foreground
        : uiTokens.color.textPrimary;

  return (
    <Pressable
      accessibilityRole="button"
      accessibilityLabel={accessibilityLabel ?? label}
      accessibilityHint={accessibilityHint}
      accessibilityState={{ disabled: blocked, busy: loading }}
      disabled={blocked}
      onPress={onPress}
      onFocus={() => setFocused(true)}
      onBlur={() => setFocused(false)}
      testID={testID}
      style={({ pressed }) => [
        styles.button,
        textVariant ? styles.text : styles.outlined,
        !textVariant && !disabledLook && controlElevationStyles.resting,
        primary && styles.primary,
        danger && styles.danger,
        contextual && !primary && styles.contextual,
        disabledLook && styles.disabled,
        focused &&
          !blocked &&
          (primary ? styles.focusedPrimary : styles.focused),
        (pressed || (__DEV__ && previewPressed)) &&
          !blocked && [
            !textVariant && controlElevationStyles.pressed,
            primary ? styles.pressedPrimary : styles.pressedOutlined,
          ],
      ]}
    >
      <View
        style={[
          styles.content,
          centeredIconGroup && iconPosition === "leading" &&
            styles.centeredIconGroupContent,
          (loading || (icon != null && iconPosition === "trailing")) &&
            styles.balancedContent,
        ]}
      >
        {loading ? (
          <View style={styles.leadingProgress} testID="button-loading-progress">
            <ActivityIndicator
              color={primary ? uiTokens.color.onAction : foreground}
            />
          </View>
        ) : iconPosition === "leading" ? (
          centeredIconGroup ? (
            <View style={styles.centeredIconGroupIcon}>{icon}</View>
          ) : icon
        ) : null}
        <Text
          style={[
            styles.label,
            { color: foreground },
            centeredIconGroup && iconPosition === "leading" &&
              styles.centeredIconGroupLabel,
          ]}
        >
          {label}
        </Text>
        {!loading && iconPosition === "trailing" ? (
          <View style={styles.trailingIcon}>{icon}</View>
        ) : null}
      </View>
    </Pressable>
  );
}

export function IconAction({
  label,
  icon,
  onPress,
  appearance = "surface",
  edgeAlignment = "center",
  disabled = false,
  previewPressed = false,
  previewFocused = false,
  testID,
}: IconActionProps) {
  const [focused, setFocused] = useState(false);
  return (
    <Pressable
      accessibilityRole="button"
      accessibilityLabel={label}
      accessibilityState={{ disabled }}
      disabled={disabled}
      onPress={onPress}
      onFocus={() => setFocused(true)}
      onBlur={() => setFocused(false)}
      testID={testID}
      style={({ pressed }) => [
        styles.iconAction,
        appearance === "plain" && styles.plainIconAction,
        appearance === "surface" &&
          !disabled &&
          controlElevationStyles.resting,
        appearance === "surface" &&
          (pressed || (__DEV__ && previewPressed)) &&
          !disabled &&
          controlElevationStyles.pressed,
        appearance === "surface" &&
          (pressed || (__DEV__ && previewPressed)) &&
          !disabled &&
          styles.pressedIconAction,
        appearance === "plain" &&
          (pressed || (__DEV__ && previewPressed)) &&
          !disabled &&
          styles.pressedPlainIconAction,
        disabled && appearance === "surface" && styles.disabled,
        disabled && appearance === "plain" && styles.disabledPlain,
        (focused || (__DEV__ && previewFocused)) &&
          !disabled &&
          styles.focusedIconAction,
      ]}
    >
      <View
        style={[
          styles.iconGlyph,
          appearance === "plain" &&
            edgeAlignment === "leading" &&
            styles.iconGlyphLeading,
          appearance === "plain" &&
            edgeAlignment === "trailing" &&
            styles.iconGlyphTrailing,
        ]}
      >
        {icon}
      </View>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  button: {
    minHeight: uiTokens.size.controlMinHeight,
    borderRadius: uiTokens.radius.button,
    justifyContent: "center",
    paddingHorizontal: uiTokens.space.controlHorizontal,
    paddingVertical: 10,
  },
  content: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: uiTokens.space.iconToText,
  },
  centeredIconGroupContent: {
    alignSelf: "stretch",
    justifyContent: "center",
  },
  centeredIconGroupIcon: {
    width: uiTokens.icon.size,
    alignItems: "center",
    justifyContent: "center",
  },
  centeredIconGroupLabel: { textAlign: "left" },
  balancedContent: {
    paddingHorizontal: uiTokens.icon.size + uiTokens.space.iconToText,
  },
  leadingProgress: {
    position: "absolute",
    left: 0,
    top: 0,
    bottom: 0,
    justifyContent: "center",
  },
  trailingIcon: {
    position: "absolute",
    right: 0,
    top: 0,
    bottom: 0,
    justifyContent: "center",
  },
  label: {
    fontFamily: fontFamily.semibold,
    fontWeight: "600",
    fontSize: uiTokens.typography.scale.control.fontSize,
    lineHeight: uiTokens.typography.scale.control.lineHeight,
    textAlign: "center",
    flexShrink: 1,
  },
  outlined: {
    backgroundColor: uiTokens.color.surface,
    borderWidth: uiTokens.border.controlHairlineWidth,
    borderColor: uiTokens.color.borderControl,
  },
  text: { backgroundColor: "transparent" },
  primary: {
    backgroundColor: uiTokens.color.action,
    borderWidth: 0,
  },
  danger: { borderColor: uiTokens.color.semantic.rose.foreground },
  focused: {
    borderWidth: uiTokens.border.focusSelectedWidth,
    borderColor: uiTokens.color.focus,
  },
  focusedPrimary: {
    borderWidth: uiTokens.border.focusSelectedWidth,
    borderColor: uiTokens.color.surface,
  },
  contextual: {
    backgroundColor:
      uiTokens.componentVariantOverrides["CMP-02"].contextualButton.surface,
    borderWidth:
      uiTokens.componentVariantOverrides["CMP-02"].contextualButton.borderWidth,
  },
  disabled: {
    backgroundColor: uiTokens.color.disabledBackground,
    borderColor: uiTokens.color.borderDecorative,
  },
  pressedPrimary: { backgroundColor: uiTokens.color.pressedAction },
  pressedOutlined: { backgroundColor: uiTokens.color.disabledBackground },
  iconAction: {
    width: uiTokens.size.iconAction,
    minHeight: uiTokens.size.iconAction,
    borderRadius: uiTokens.radius.iconAction,
    backgroundColor: uiTokens.color.surface,
    borderWidth: uiTokens.border.controlHairlineWidth,
    borderColor: uiTokens.color.borderControl,
    alignItems: "center",
    justifyContent: "center",
  },
  iconGlyph: { alignItems: "center", justifyContent: "center" },
  iconGlyphLeading: {
    transform: [
      { translateX: -(uiTokens.size.iconAction - uiTokens.icon.size) / 2 },
    ],
  },
  iconGlyphTrailing: {
    transform: [
      { translateX: (uiTokens.size.iconAction - uiTokens.icon.size) / 2 },
    ],
  },
  plainIconAction: {
    backgroundColor: "transparent",
    borderWidth: 0,
    borderColor: "transparent",
    borderRadius: uiTokens.size.iconAction / 2,
    boxShadow: "none",
    elevation: 0,
  },
  disabledPlain: { opacity: 0.5 },
  pressedIconAction: { backgroundColor: uiTokens.color.disabledBackground },
  pressedPlainIconAction: {
    backgroundColor: uiTokens.color.disabledBackground,
  },
  focusedIconAction: {
    borderWidth: uiTokens.border.focusSelectedWidth,
    borderColor: uiTokens.color.focus,
  },
});
