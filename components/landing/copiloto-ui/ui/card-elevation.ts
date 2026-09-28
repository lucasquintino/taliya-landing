import { StyleSheet } from "react-native";

import { uiTokens } from "./tokens";

/** Sombra compartilhada de cartões, abaixo da elevação de overlays. */
export const cardElevationStyles = StyleSheet.create({
  card: {
    boxShadow: `0px ${uiTokens.elevation.card.shadowOffsetY}px ${uiTokens.elevation.card.shadowRadius * 2}px rgba(0, 0, 0, ${uiTokens.elevation.card.shadowOpacity})`,
    elevation: uiTokens.elevation.card.android,
  },
});
