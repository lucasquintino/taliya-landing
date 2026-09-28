import type { ReactNode } from "react";

import { CopilotFab } from "../../ui/context/CopilotFab";
import {
  ScreenLayout,
  type MainDestination,
} from "../../ui/layout";

/**
 * Cópia da composição MainShell do app Copiloto, com navegação local sem rotas
 * Expo para que a tela Agenda funcione dentro da prévia web da landing.
 */
export function MainShell({
  destination,
  children,
}: {
  destination: MainDestination;
  children?: ReactNode;
}) {
  return (
    <ScreenLayout
      variant="principal"
      title={destination}
      floatingAction={<CopilotFab onPress={() => undefined} />}
      navigation={{ active: destination, onNavigate: () => undefined }}
    >
      {children}
    </ScreenLayout>
  );
}
