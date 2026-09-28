import { StyleSheet } from "react-native";

import { uiTokens } from "./tokens";

/** Elevação baixa de superfícies de controle, separada da elevação de overlays. */
export const controlElevationStyles = StyleSheet.create({
  resting: {
    boxShadow: `0px ${uiTokens.elevation.control.shadowOffsetY}px ${uiTokens.elevation.control.shadowRadius * 2}px rgba(0, 0, 0, ${uiTokens.elevation.control.shadowOpacity})`,
    elevation: uiTokens.elevation.control.android,
  },
  pressed: {
    boxShadow: `0px ${uiTokens.elevation.controlPressed.shadowOffsetY}px ${uiTokens.elevation.controlPressed.shadowRadius * 2}px rgba(0, 0, 0, ${uiTokens.elevation.controlPressed.shadowOpacity})`,
    elevation: uiTokens.elevation.controlPressed.android,
  },
});
