"use client";

import { usePathname } from "next/navigation";
import { useEffect } from "react";
import { recordObservedAcquisition } from "@/lib/landing/acquisition";

/**
 * Records one page view for every public page (sign-up, terms and privacy included), not only the
 * home. The home's own view event shares the same occurrence, so it is never counted twice.
 */
export function PageViewRecorder() {
  const pathname = usePathname();
  useEffect(() => {
    if (!pathname || pathname.startsWith("/internal") || pathname.startsWith("/api")) return;
    void recordObservedAcquisition("page_opened", {});
  }, [pathname]);
  return null;
}
