import {
  Banknote,
  BriefcaseBusiness,
  CalendarDays,
  ChevronLeft,
  House,
  User,
} from "lucide-react";
import { useEffect, useRef, useState } from "react";
import type { ReactNode, RefObject } from "react";
import {
  Keyboard,
  KeyboardAvoidingView,
  Platform,
  Pressable,
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  View,
  useWindowDimensions,
  type LayoutChangeEvent,
  type StyleProp,
  type ViewStyle,
} from "react-native";
import { IconAction } from "../actions";
import { TaliyaBrand } from "../brand/TaliyaBrand";
import { fontFamily, uiTokens } from "../tokens";

const useSafeAreaInsets = () => ({ top: 0, right: 0, bottom: 0, left: 0 });

export type LayoutVariant =
  "principal" | "detail" | "form" | "guided" | "panel";
export type MainDestination =
  "Hoje" | "Serviços" | "Agenda" | "Clientes" | "Recebimentos";

const destinations = [
  { label: "Hoje", Icon: House },
  { label: "Serviços", Icon: BriefcaseBusiness },
  { label: "Agenda", Icon: CalendarDays },
  { label: "Clientes", Icon: User },
  { label: "Recebimentos", Icon: Banknote },
] as const;

function screenHorizontalInset(width: number) {
  return width <= uiTokens.layout.compactWidth
    ? uiTokens.space.screenHorizontalCompact360
    : uiTokens.space.screenHorizontal;
}

function colorFromToken(reference: string) {
  if (reference.startsWith("color.")) {
    const value =
      uiTokens.color[
        reference.slice("color.".length) as keyof typeof uiTokens.color
      ];
    if (typeof value === "string") return value;
  }
  return uiTokens.color.surface;
}

export type BottomNavigationProps = {
  active: MainDestination;
  onNavigate: (destination: MainDestination) => void;
  blurTarget?: RefObject<View | null>;
  onLayout?: (event: LayoutChangeEvent) => void;
};

export function BottomNavigation({
  active,
  onNavigate,
  onLayout,
}: BottomNavigationProps) {
  return (
    <View
      accessibilityRole="tablist"
      testID="bottom-navigation"
      onLayout={onLayout}
      style={styles.navigation}
    >
      <View style={[StyleSheet.absoluteFill, styles.navigationBlur, { pointerEvents: "none" }]} />
      <View style={styles.navigationRow}>
        {destinations.map(({ label, Icon }) => {
          const selected = active === label;
          const color = colorFromToken(
            selected
              ? uiTokens.navigation.selection.iconColorToken
              : uiTokens.navigation.unselected.iconColorToken,
          );
          return (
            <Pressable
              key={label}
              accessibilityRole="tab"
              accessibilityLabel={label}
              accessibilityState={{ selected }}
              onPress={() => onNavigate(label)}
              style={[
                styles.destination,
                selected && styles.destinationSelected,
              ]}
            >
              <Icon
                aria-hidden="true"
                size={uiTokens.navigation.item.iconSize}
                strokeWidth={uiTokens.icon.strokeWidth}
                color={color}
              />
            </Pressable>
          );
        })}
      </View>
    </View>
  );
}

export type HeaderActionProps = {
  title: string;
  titleContent?: ReactNode;
  onBack?: () => void;
  action?: ReactNode;
};

export function HeaderAction({
  title,
  titleContent,
  onBack,
  action,
}: HeaderActionProps) {
  const { width, fontScale } = useWindowDimensions();
  const hasTitle = titleContent != null || title.trim().length > 0;
  const hasBack = onBack != null;
  const hasAction = action != null;
  const brandOnLeft = !hasBack && hasAction;
  const standaloneBrandOnLeft = !hasBack && !hasAction && !hasTitle;
  const brandOnRight = !hasAction && (hasBack || hasTitle);
  const useWordmarkOnRight =
    !hasBack && width >= 390 && fontScale < 1.2;

  return (
    <View
      style={[
        styles.header,
        {
          paddingHorizontal: screenHorizontalInset(width),
        },
      ]}
    >
      {onBack ? (
        <View style={styles.headerSide}>
          <IconAction
            label="Voltar"
            appearance="plain"
            edgeAlignment="leading"
            icon={
              <ChevronLeft
                size={uiTokens.icon.size}
                strokeWidth={uiTokens.icon.strokeWidth}
                color={uiTokens.color.textPrimary}
              />
            }
            onPress={onBack}
          />
        </View>
      ) : brandOnLeft || standaloneBrandOnLeft ? (
        <View
          style={[
            styles.headerSide,
            brandOnLeft && styles.headerMarkSide,
          ]}
        >
          <TaliyaBrand
            variant={brandOnLeft ? "mark" : "wordmark"}
            width={brandOnLeft ? 32 : 128}
          />
        </View>
      ) : null}
      {hasTitle ? (
        <View
          style={[
            styles.headerTitleSlot,
            !hasBack && !hasAction && styles.headerTitleSlotLeading,
          ]}
        >
          {titleContent != null ? (
            <View
              style={[
                styles.headerTitleContent,
                !hasBack && !hasAction &&
                  styles.headerTitleContentLeading,
              ]}
            >
              {titleContent}
            </View>
          ) : (
            <Text
              accessibilityRole="header"
              style={[
                styles.headerTitle,
                !hasBack && !hasAction && styles.headerTitleTextLeading,
              ]}
            >
              {title}
            </Text>
          )}
        </View>
      ) : null}
      {action ? (
        <View style={styles.headerSide}>{action}</View>
      ) : brandOnRight ? (
        <View
          style={[
            styles.headerSide,
            !useWordmarkOnRight && styles.headerMarkSide,
          ]}
        >
          <TaliyaBrand
            variant={useWordmarkOnRight ? "wordmark" : "mark"}
            width={useWordmarkOnRight ? 128 : 32}
          />
        </View>
      ) : null}
    </View>
  );
}

export function ActionFooter({
  children,
  safeAreaBottom = true,
}: {
  children: ReactNode;
  safeAreaBottom?: boolean;
}) {
  const insets = useSafeAreaInsets();
  const { width } = useWindowDimensions();
  return (
    <View
      style={[
        styles.footer,
        {
          paddingBottom: safeAreaBottom
            ? Math.max(uiTokens.space.componentGap, insets.bottom)
            : uiTokens.space.componentGap,
          paddingHorizontal: screenHorizontalInset(width),
        },
      ]}
    >
      {children}
    </View>
  );
}

type ScreenLayoutCommonProps = {
  title: string;
  children?: ReactNode;
  renderScrollableContent?: ScreenScrollableContentRenderer;
  scrollResetKey?: string | number;
  headerTitleContent?: ReactNode;
  headerAction?: ReactNode;
  overlay?: ReactNode;
};

export type ScreenLayoutProps = ScreenLayoutCommonProps &
  (
    | {
        variant: "principal";
        navigation: BottomNavigationProps;
        floatingAction: ReactNode;
        onBack?: never;
        footer?: never;
      }
    | {
        variant: "detail";
        onBack: () => void;
        navigation?: never;
        floatingAction?: ReactNode;
        footer?: never;
      }
    | {
        variant: "form" | "guided" | "panel";
        onBack?: () => void;
        navigation?: never;
        floatingAction?: never;
        footer?: ReactNode;
      }
  );

export type ScreenScrollableContentRendererProps = {
  style: StyleProp<ViewStyle>;
  contentContainerStyle: StyleProp<ViewStyle>;
};
export type ScreenScrollableContentRenderer = (
  props: ScreenScrollableContentRendererProps,
) => ReactNode;

export function ScreenLayout({
  variant,
  title,
  children,
  renderScrollableContent,
  scrollResetKey,
  headerTitleContent,
  onBack,
  headerAction,
  footer,
  navigation,
  floatingAction,
  overlay,
}: ScreenLayoutProps) {
  const { width } = useWindowDimensions();
  const insets = useSafeAreaInsets();
  const navigationBlurTargetRef = useRef<View>(null);
  const [keyboardVisible, setKeyboardVisible] = useState(false);
  const [navigationHeight, setNavigationHeight] = useState(
    uiTokens.navigation.floating.minHeight,
  );
  const horizontal = screenHorizontalInset(width);
  const showNavigation =
    variant === "principal" && navigation !== undefined && !keyboardVisible;
  const showFab = floatingAction != null && !keyboardVisible;
  const navigationBottom =
    insets.bottom + uiTokens.navigation.floating.bottomGap;
  const copilotBottom = showNavigation
    ? navigationBottom + navigationHeight + uiTokens.copilot.fab.gap
    : insets.bottom + uiTokens.copilot.fab.detailBottomGap;
  const bottomContentClearance = showNavigation
    ? navigationBottom +
      navigationHeight +
      uiTokens.copilot.fab.gap +
      (showFab ? uiTokens.copilot.fab.size : 0) +
      uiTokens.layout.contentClearance
    : showFab
      ? insets.bottom +
        uiTokens.copilot.fab.detailBottomGap +
        uiTokens.copilot.fab.size +
        uiTokens.layout.contentClearance
      : uiTokens.space.sectionGap;
  const contentContainerStyle = [
    styles.body,
    {
      paddingHorizontal: horizontal,
      paddingBottom: bottomContentClearance,
    },
  ];

  useEffect(() => {
    const showSubscription = Keyboard.addListener("keyboardDidShow", () =>
      setKeyboardVisible(true),
    );
    const hideSubscription = Keyboard.addListener("keyboardDidHide", () =>
      setKeyboardVisible(false),
    );
    return () => {
      showSubscription.remove();
      hideSubscription.remove();
    };
  }, []);

  function handleNavigationLayout(event: LayoutChangeEvent) {
    const measuredHeight = event.nativeEvent.layout.height;
    setNavigationHeight((current) =>
      current === measuredHeight ? current : measuredHeight,
    );
  }

  return (
    <SafeAreaView style={styles.safeArea}>
      <KeyboardAvoidingView
        behavior={Platform.OS === "ios" ? "padding" : "height"}
        style={styles.flex}
      >
        <View ref={navigationBlurTargetRef} style={styles.flex}>
          <HeaderAction
            title={title}
            {...(headerTitleContent ? { titleContent: headerTitleContent } : {})}
            {...(onBack ? { onBack } : {})}
            action={headerAction}
          />
          {renderScrollableContent ? (
            <View style={styles.flex}>
              {renderScrollableContent({
                style: styles.flex,
                contentContainerStyle,
              })}
            </View>
          ) : (
            <ScrollView
              key={scrollResetKey}
              keyboardShouldPersistTaps="handled"
              style={styles.flex}
              contentContainerStyle={contentContainerStyle}
              testID="screen-layout-scroll"
            >
              {children}
            </ScrollView>
          )}
          {footer ? (
            <ActionFooter safeAreaBottom={variant !== "principal"}>
              {footer}
            </ActionFooter>
          ) : null}
        </View>
        {showNavigation && navigation ? (
          <View
            style={[
              styles.floatingNavigation,
              { pointerEvents: "box-none" },
              {
                left: uiTokens.navigation.floating.sideInset,
                right: uiTokens.navigation.floating.sideInset,
                bottom: navigationBottom,
              },
            ]}
          >
            <BottomNavigation
              {...navigation}
              blurTarget={navigationBlurTargetRef}
              onLayout={handleNavigationLayout}
            />
          </View>
        ) : null}
        {showFab ? (
          <View
            style={[
              styles.floatingFab,
              { pointerEvents: "box-none" },
              { right: uiTokens.copilot.fab.edge, bottom: copilotBottom },
            ]}
          >
            {floatingAction}
          </View>
        ) : null}
        {overlay}
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  safeArea: { flex: 1, backgroundColor: uiTokens.color.background },
  header: {
    minHeight: uiTokens.header.minHeight,
    flexDirection: "row",
    alignItems: "center",
    gap: uiTokens.space.headerIconActionToTitle,
    paddingTop: 0,
  },
  headerTitle: {
    flexShrink: 1,
    minWidth: 0,
    textAlign: "center",
    color: uiTokens.color.textPrimary,
    fontFamily: fontFamily.bold,
    fontSize: uiTokens.typography.scale.appBarTitle.fontSize,
    lineHeight: uiTokens.typography.scale.appBarTitle.lineHeight,
  },
  headerTitleContent: {
    flex: 1,
    flexShrink: 1,
    minWidth: 0,
    justifyContent: "center",
    alignItems: "center",
  },
  headerTitleContentLeading: { alignItems: "flex-start" },
  headerTitleSlot: {
    flex: 1,
    minWidth: 0,
    alignItems: "center",
    justifyContent: "center",
  },
  headerTitleSlotLeading: { alignItems: "flex-start" },
  headerTitleTextLeading: { textAlign: "left" },
  headerSide: { flexShrink: 0, alignItems: "center", justifyContent: "center" },
  headerMarkSide: { width: uiTokens.size.iconAction, minHeight: uiTokens.size.iconAction },
  body: {
    flexGrow: 1,
    paddingTop: uiTokens.space.componentGap,
    paddingBottom: uiTokens.space.sectionGap,
    gap: uiTokens.space.componentGap,
  },
  footer: {
    backgroundColor: uiTokens.color.surface,
    paddingTop: uiTokens.footer.topPadding,
    gap: uiTokens.footer.copilotoGap,
  },
  floatingNavigation: {
    position: "absolute",
    zIndex: 10,
  },
  floatingFab: {
    position: "absolute",
    zIndex: 11,
  },
  navigation: {
    height: uiTokens.navigation.floating.minHeight,
    backgroundColor: "transparent",
    borderRadius: uiTokens.navigation.floating.radius,
    padding: uiTokens.navigation.floating.padding,
    borderWidth: uiTokens.navigation.floating.glass.borderWidth,
    borderColor: colorFromToken(uiTokens.navigation.floating.glass.borderToken),
    justifyContent: "center",
    elevation: uiTokens.elevation.android,
    boxShadow: `0px ${uiTokens.elevation.shadowOffsetY}px ${uiTokens.elevation.shadowRadius * 2}px rgba(0, 0, 0, ${uiTokens.elevation.shadowOpacity})`,
  },
  navigationBlur: {
    top: uiTokens.navigation.floating.glass.borderWidth,
    right: uiTokens.navigation.floating.glass.borderWidth,
    bottom: uiTokens.navigation.floating.glass.borderWidth,
    left: uiTokens.navigation.floating.glass.borderWidth,
    borderRadius: uiTokens.navigation.floating.radius,
    overflow: "hidden",
    backgroundColor: "rgba(255, 255, 255, 0.88)",
  },
  navigationRow: {
    flex: 1,
    flexDirection: "row",
    alignItems: "stretch",
  },
  destination: {
    flex: 1,
    minHeight: uiTokens.navigation.item.minTarget,
    minWidth: uiTokens.navigation.item.minTarget,
    alignItems: "center",
    justifyContent: "center",
  },
  destinationSelected: {
    margin: uiTokens.navigation.selection.inset,
    borderRadius: uiTokens.navigation.floating.radius,
    backgroundColor: colorFromToken(
      uiTokens.navigation.selection.backgroundToken,
    ),
  },
});
