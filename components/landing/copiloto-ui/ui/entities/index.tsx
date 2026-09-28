import {
  Banknote,
  Bell,
  BriefcaseBusiness,
  CalendarDays,
  ChevronRight,
  FileText,
  User,
} from "lucide-react";
import type { ReactNode } from "react";
import {
  ActivityIndicator,
  Pressable,
  StyleSheet,
  Text,
  View,
} from "react-native";

import { Button } from "../actions";
import { fontFamily, uiTokens } from "../tokens";
import { cardElevationStyles } from "../card-elevation";

export type EntityType =
  "client" | "service" | "receipt" | "reminder" | "occurrence" | "document";

const iconByEntity = {
  client: User,
  service: BriefcaseBusiness,
  receipt: Banknote,
  reminder: Bell,
  occurrence: CalendarDays,
  document: FileText,
} as const;

export function EntityIcon({
  entityType,
  emphasis = false,
}: {
  entityType: EntityType;
  emphasis?: boolean;
}) {
  const Icon = iconByEntity[entityType];
  const teal = emphasis && entityType === "service";
  return (
    <View
      accessible={false}
      testID="entity-icon"
      style={[
        styles.iconSurface,
        teal && { backgroundColor: uiTokens.color.semantic.teal.background },
      ]}
    >
      <Icon
        size={uiTokens.icon.size}
        strokeWidth={uiTokens.icon.strokeWidth}
        color={
          teal
            ? uiTokens.color.semantic.teal.foreground
            : uiTokens.color.textSecondary
        }
      />
    </View>
  );
}

export type EntityRowProps = {
  entityType: EntityType;
  title: string;
  secondary?: string;
  status?: ReactNode;
  showIcon?: boolean;
  onOpen?: () => void;
  readOnly?: boolean;
  loading?: boolean;
  presentation?: "card" | "grouped";
};

export function EntityRow({
  entityType,
  title,
  secondary,
  status,
  showIcon = true,
  onOpen,
  readOnly = false,
  loading = false,
  presentation = "grouped",
}: EntityRowProps) {
  const content = (
    <>
      {showIcon ? <EntityIcon entityType={entityType} /> : null}
      <View style={styles.rowCopy}>
        <View style={styles.titleAndStatus}>
          <Text style={styles.rowTitle}>{title}</Text>
          {status}
        </View>
        {secondary ? <Text style={styles.secondary}>{secondary}</Text> : null}
      </View>
      {loading ? (
        <ActivityIndicator accessibilityLabel="Carregando" />
      ) : onOpen && !readOnly ? (
        <ChevronRight
          size={uiTokens.icon.size}
          strokeWidth={uiTokens.icon.strokeWidth}
          color={uiTokens.color.textSecondary}
        />
      ) : null}
    </>
  );
  const presentationStyles =
    presentation === "card"
      ? [styles.rowCard, cardElevationStyles.card]
      : [styles.rowGrouped];
  if (!onOpen || readOnly) {
    return <View style={[styles.row, ...presentationStyles]}>{content}</View>;
  }
  return (
    <Pressable
      accessibilityRole="button"
      accessibilityHint="Abre detalhes; não altera o registro"
      accessibilityState={{ disabled: loading, busy: loading }}
      disabled={loading}
      onPress={onOpen}
      style={({ pressed }) => [
        styles.row,
        ...presentationStyles,
        pressed && styles.rowPressed,
      ]}
    >
      {content}
    </Pressable>
  );
}

export type EntityHighlightProps = {
  entityType: EntityType;
  title: string;
  secondary?: string;
  status?: ReactNode;
  showIcon?: boolean;
  detail?: string;
  amount?: string;
  action?: { label: string; onPress: () => void; disabled?: boolean };
  loading?: boolean;
  surface?: "card" | "embedded";
};

export function EntityHighlight({
  entityType,
  title,
  secondary,
  status,
  showIcon = true,
  detail,
  amount,
  action,
  loading = false,
  surface = "card",
}: EntityHighlightProps) {
  return (
    <View
      style={[
        styles.highlight,
        surface === "card" ? styles.highlightCard : styles.highlightEmbedded,
        surface === "card" && cardElevationStyles.card,
      ]}
      testID="entity-highlight"
    >
      <View style={styles.highlightHeader} testID="entity-highlight-header">
        {showIcon ? <EntityIcon entityType={entityType} emphasis /> : null}
        <View style={styles.rowCopy}>
          <Text style={styles.highlightTitle}>{title}</Text>
          {secondary ? <Text style={styles.secondary}>{secondary}</Text> : null}
        </View>
      </View>
      {status ? (
        <View style={styles.statusRow} testID="entity-highlight-status">
          {status}
        </View>
      ) : null}
      {detail || amount ? (
        <View style={styles.detailsRow}>
          {detail ? <Text style={styles.detail}>{detail}</Text> : null}
          {amount ? <Text style={styles.amount}>{amount}</Text> : null}
        </View>
      ) : null}
      {action ? (
        <View style={styles.actionRow} testID="entity-highlight-action">
          <Button
            label={action.label}
            onPress={action.onPress}
            {...(action.disabled === undefined
              ? {}
              : { disabled: action.disabled })}
            loading={loading}
          />
        </View>
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  iconSurface: {
    width: uiTokens.size.entityIconContainer,
    minHeight: uiTokens.size.entityIconContainer,
    borderRadius: uiTokens.radius.entityIconContainer,
    backgroundColor: uiTokens.color.disabledBackground,
    alignItems: "center",
    justifyContent: "center",
  },
  row: {
    minHeight: uiTokens.size.compactRowMinHeight,
    paddingVertical: uiTokens.size.compactRowVerticalPadding,
    flexDirection: "row",
    alignItems: "center",
    gap: uiTokens.space.rowIconToText,
  },
  rowCard: {
    borderRadius: uiTokens.componentVariantOverrides["CMP-04"].compact.radius,
    borderWidth: uiTokens.border.normalWidth,
    borderColor: uiTokens.color.borderDecorative,
    paddingHorizontal:
      uiTokens.componentVariantOverrides["CMP-05"].contentInset,
    backgroundColor: uiTokens.color.surface,
  },
  rowGrouped: { paddingHorizontal: 0 },
  rowPressed: {
    backgroundColor: uiTokens.color.disabledBackground,
    borderRadius: uiTokens.radius.control,
  },
  rowCopy: { flex: 1, gap: uiTokens.space.feedbackTitleToBody },
  titleAndStatus: {
    flexDirection: "row",
    alignItems: "flex-start",
    justifyContent: "space-between",
    flexWrap: "wrap",
    gap: uiTokens.space.relatedRowGap,
  },
  rowTitle: {
    flexShrink: 1,
    color: uiTokens.color.textPrimary,
    fontFamily: fontFamily.semibold,
    fontWeight: "600",
    fontSize: uiTokens.typography.scale.rowTitle.fontSize,
    lineHeight: uiTokens.typography.scale.rowTitle.lineHeight,
  },
  secondary: {
    color: uiTokens.color.textSecondary,
    fontFamily: fontFamily.regular,
    fontSize: uiTokens.typography.scale.secondary.fontSize,
    lineHeight: uiTokens.typography.scale.secondary.lineHeight,
  },
  highlight: {
    gap: uiTokens.space.highlightIconToText,
  },
  highlightCard: {
    borderRadius: uiTokens.componentVariantOverrides["CMP-04"].highlight.radius,
    borderWidth: uiTokens.border.normalWidth,
    borderColor: uiTokens.color.borderDecorative,
    padding: uiTokens.componentVariantOverrides["CMP-04"].highlight.padding,
    backgroundColor: uiTokens.color.surface,
  },
  highlightEmbedded: {
    borderRadius: 0,
    padding: 0,
    backgroundColor: "transparent",
  },
  highlightHeader: {
    flexDirection: "row",
    alignItems: "center",
    gap: uiTokens.space.highlightIconToText,
  },
  highlightTitle: {
    flexShrink: 1,
    color: uiTokens.color.textPrimary,
    fontFamily: fontFamily.bold,
    fontWeight: "700",
    fontSize: uiTokens.typography.scale.highlightTitle.fontSize,
    lineHeight: uiTokens.typography.scale.highlightTitle.lineHeight,
  },
  statusRow: { alignItems: "flex-start" },
  detailsRow: {
    flexDirection: "row",
    alignItems: "flex-start",
    justifyContent: "space-between",
    flexWrap: "wrap",
    gap: uiTokens.space.relatedItemGap,
  },
  detail: {
    color: uiTokens.color.textPrimary,
    fontFamily: fontFamily.regular,
    fontSize: uiTokens.typography.scale.body.fontSize,
    lineHeight: uiTokens.typography.scale.body.lineHeight,
  },
  amount: {
    color: uiTokens.color.textPrimary,
    fontFamily: fontFamily.semibold,
    fontWeight: "600",
    fontSize: uiTokens.typography.scale.control.fontSize,
    lineHeight: uiTokens.typography.scale.control.lineHeight,
  },
  actionRow: { alignSelf: "stretch" },
});
