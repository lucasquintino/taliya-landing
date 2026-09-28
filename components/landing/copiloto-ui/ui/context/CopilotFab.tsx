import { MessageSquare } from "lucide-react";
import { useState } from "react";
import { Pressable, StyleSheet } from "react-native";

import { uiTokens } from "../tokens";

export function CopilotFab({ onPress }: { onPress: () => void }) {
  const [focused, setFocused] = useState(false);
  return (
    <Pressable
      accessibilityRole="button"
      accessibilityLabel={uiTokens.copilot.fab.accessibilityLabel}
      onPress={onPress}
      onFocus={() => setFocused(true)}
      onBlur={() => setFocused(false)}
      style={({ pressed }) => [
        styles.fab,
        pressed && styles.fabPressed,
        focused && styles.fabFocused,
      ]}
    >
      <MessageSquare
        aria-hidden="true"
        size={uiTokens.copilot.fab.iconSize}
        strokeWidth={uiTokens.icon.strokeWidth}
        color={uiTokens.color.onAction}
      />
    </Pressable>
  );
}

const styles = StyleSheet.create({
  fab: {
    width: uiTokens.copilot.fab.size,
    height: uiTokens.copilot.fab.size,
    borderRadius: uiTokens.copilot.fab.radius,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: uiTokens.color.action,
    boxShadow: `0px ${uiTokens.elevation.shadowOffsetY}px ${uiTokens.elevation.shadowRadius * 2}px rgba(0, 0, 0, ${uiTokens.elevation.shadowOpacity})`,
  },
  fabPressed: { backgroundColor: uiTokens.color.pressedAction },
  fabFocused: {
    borderWidth: uiTokens.border.focusSelectedWidth,
    borderColor: uiTokens.color.surface,
  },
});
