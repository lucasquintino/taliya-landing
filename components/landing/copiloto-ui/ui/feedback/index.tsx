import {
  CircleCheck,
  Clock,
  CloudAlert,
  Info,
  LoaderCircle,
  Pencil,
  TriangleAlert,
} from "lucide-react";
import { StyleSheet, Text, View } from "react-native";

import { Button } from "../actions";
import { fontFamily, uiTokens } from "../tokens";

export type FeedbackKind =
  | "information"
  | "caution"
  | "processing"
  | "unknown"
  | "success"
  | "partial"
  | "error"
  | "unsaved";

export type InlineFeedbackProps = {
  kind: FeedbackKind;
  title: string;
  message?: string;
};

const pairByKind = {
  information: uiTokens.color.semantic.blue,
  caution: uiTokens.color.semantic.amber,
  processing: uiTokens.color.semantic.blue,
  unknown: uiTokens.color.semantic.neutral,
  success: uiTokens.color.semantic.green,
  partial: uiTokens.color.semantic.amber,
  error: uiTokens.color.semantic.rose,
  unsaved: uiTokens.color.semantic.amber,
} as const;

const iconByKind = {
  information: Info,
  caution: TriangleAlert,
  processing: LoaderCircle,
  unknown: Clock,
  success: CircleCheck,
  partial: CloudAlert,
  error: TriangleAlert,
  unsaved: Pencil,
} as const;

export function InlineFeedback({ kind, title, message }: InlineFeedbackProps) {
  const pair = pairByKind[kind];
  const Icon = iconByKind[kind];
  return (
    <View
      accessible
      accessibilityRole={kind === "error" ? "alert" : "summary"}
      style={styles.container}
    >
      <View style={[styles.iconSurface, { backgroundColor: pair.background }]}>
        <Icon
          size={uiTokens.icon.size}
          strokeWidth={uiTokens.icon.strokeWidth}
          color={pair.foreground}
        />
      </View>
      <View style={styles.copy}>
        <Text style={styles.title}>{title}</Text>
        {message ? <Text style={styles.message}>{message}</Text> : null}
      </View>
    </View>
  );
}

export type OperationResultProps = {
  state: "processing" | "confirmed" | "partial" | "unknown" | "failed";
  title: string;
  context: string;
  confirmedEffects?: readonly string[];
  pendingEffects?: readonly string[];
  operationId?: string;
  onCheckOperation?: () => void;
  onRetryConfirmedFailure?: () => void;
};

/** Recebe fatos do chamador; nunca infere que a operação concluiu pelo estado visual. */
export function OperationResult({
  state,
  title,
  context,
  confirmedEffects = [],
  pendingEffects = [],
  operationId,
  onCheckOperation,
  onRetryConfirmedFailure,
}: OperationResultProps) {
  const kind: FeedbackKind =
    state === "confirmed" ? "success" : state === "failed" ? "error" : state;
  return (
    <View style={styles.result}>
      <InlineFeedback kind={kind} title={title} message={context} />
      {confirmedEffects.length > 0 ? (
        <View style={styles.effectGroup}>
          <Text style={styles.effectHeading}>Confirmado</Text>
          {confirmedEffects.map((effect) => (
            <Text key={effect} style={styles.message}>
              {effect}
            </Text>
          ))}
        </View>
      ) : null}
      {pendingEffects.length > 0 ? (
        <View style={styles.effectGroup}>
          <Text style={styles.effectHeading}>Ainda pendente</Text>
          {pendingEffects.map((effect) => (
            <Text key={effect} style={styles.message}>
              {effect}
            </Text>
          ))}
        </View>
      ) : null}
      {operationId ? (
        <Text style={styles.operationId}>Operação: {operationId}</Text>
      ) : null}
      {state === "unknown" && onCheckOperation ? (
        <Button
          label="Consultar operação"
          onPress={onCheckOperation}
          variant="secondary"
        />
      ) : null}
      {state === "failed" && onRetryConfirmedFailure ? (
        <Button
          label="Tentar novamente"
          onPress={onRetryConfirmedFailure}
          variant="secondary"
        />
      ) : null}
    </View>
  );
}

export type ConfirmDialogProps = {
  title: string;
  object: string;
  scope: string;
  consequence: string;
  confirmLabel: string;
  cancelLabel?: string;
  onConfirm?: () => void;
  onCancel: () => void;
  showTitle?: boolean;
  destructive?: boolean;
  confirming?: boolean;
};

export function ConfirmDialog({
  title,
  object,
  scope,
  consequence,
  confirmLabel,
  cancelLabel = "Cancelar",
  onConfirm,
  onCancel,
  showTitle = true,
  destructive = false,
  confirming = false,
}: ConfirmDialogProps) {
  return (
    <View accessibilityRole="alert" style={styles.dialogContent}>
      {showTitle ? <Text style={styles.dialogTitle}>{title}</Text> : null}
      <Text style={styles.message}>Objeto: {object}</Text>
      <Text style={styles.message}>Alcance: {scope}</Text>
      <Text style={styles.message}>{consequence}</Text>
      <View style={styles.dialogActions}>
        <Button
          label={cancelLabel}
          onPress={onCancel}
          variant={destructive ? "primary" : "secondary"}
          disabled={confirming}
        />
        <Button
          label={confirmLabel}
          {...(onConfirm ? { onPress: onConfirm } : {})}
          variant={destructive ? "dangerText" : "primary"}
          loading={confirming}
        />
      </View>
    </View>
  );
}

export type UnsavedChangesDialogProps = {
  dirty: boolean;
  object: string;
  onKeepEditing: () => void;
  onDiscard: () => void;
  showTitle?: boolean;
};

export function UnsavedChangesDialog({
  dirty,
  object,
  onKeepEditing,
  onDiscard,
  showTitle = true,
}: UnsavedChangesDialogProps) {
  if (!dirty) return null;
  return (
    <ConfirmDialog
      title="Descartar alterações?"
      object={object}
      scope="Somente as alterações não salvas desta tela"
      consequence="O que já foi salvo permanece disponível."
      confirmLabel="Descartar alterações"
      cancelLabel="Continuar editando"
      onConfirm={onDiscard}
      onCancel={onKeepEditing}
      showTitle={showTitle}
      destructive
    />
  );
}

const styles = StyleSheet.create({
  container: {
    minHeight: uiTokens.size.entityIconContainer,
    flexDirection: "row",
    alignItems: "flex-start",
    gap: uiTokens.space.rowIconToText,
  },
  iconSurface: {
    width: uiTokens.size.entityIconContainer,
    minHeight: uiTokens.size.entityIconContainer,
    borderRadius: uiTokens.radius.entityIconContainer,
    justifyContent: "center",
    alignItems: "center",
  },
  copy: {
    flex: 1,
    gap: uiTokens.space.feedbackTitleToBody,
  },
  title: {
    color: uiTokens.color.textPrimary,
    fontFamily: fontFamily.semibold,
    fontWeight: "600",
    fontSize: uiTokens.typography.scale.control.fontSize,
    lineHeight: uiTokens.typography.scale.control.lineHeight,
  },
  message: {
    color: uiTokens.color.textSecondary,
    fontFamily: fontFamily.regular,
    fontSize: uiTokens.typography.scale.secondary.fontSize,
    lineHeight: uiTokens.typography.scale.secondary.lineHeight,
  },
  result: { gap: uiTokens.space.componentGap },
  effectGroup: { gap: uiTokens.space.feedbackTitleToBody },
  effectHeading: {
    color: uiTokens.color.textPrimary,
    fontFamily: fontFamily.semibold,
    fontWeight: "600",
    fontSize: uiTokens.typography.scale.secondary.fontSize,
    lineHeight: uiTokens.typography.scale.secondary.lineHeight,
  },
  operationId: {
    color: uiTokens.color.textSecondary,
    fontFamily: fontFamily.regular,
    fontSize: uiTokens.typography.scale.caption.fontSize,
    lineHeight: uiTokens.typography.scale.caption.lineHeight,
  },
  dialogContent: {
    gap: uiTokens.space.componentGap,
  },
  dialogTitle: {
    color: uiTokens.color.textPrimary,
    fontFamily: fontFamily.bold,
    fontWeight: "700",
    fontSize: uiTokens.typography.scale.title.fontSize,
    lineHeight: uiTokens.typography.scale.title.lineHeight,
  },
  dialogActions: { gap: uiTokens.space.relatedItemGap },
});
