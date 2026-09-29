import { readFile } from "node:fs/promises";
import { join } from "node:path";
import { ImageResponse } from "next/og";
import { pilatesLanding } from "@/data/landing/niches/pilates";

export const alt = pilatesLanding.metadata.title;
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default async function Image() {
  const logo = await readFile(join(process.cwd(), "public/taliya-logo.svg"));

  return new ImageResponse(
    <div
      style={{
        alignItems: "flex-start",
        backgroundColor: "#FFFDF8",
        color: "#101B3A",
        display: "flex",
        flexDirection: "column",
        height: "100%",
        justifyContent: "space-between",
        padding: "68px 78px",
        width: "100%",
      }}
    >
      <img
        alt="Taliya"
        height={74}
        src={`data:image/svg+xml;base64,${logo.toString("base64")}`}
        width={331}
      />
      <div style={{ display: "flex", flexDirection: "column", width: "100%" }}>
        <div
          style={{
            fontSize: 67,
            fontWeight: 800,
            letterSpacing: -3,
            lineHeight: 1.06,
            maxWidth: 1020,
          }}
        >
          {pilatesLanding.hero.headline}
        </div>
        <div
          style={{
            color: "#667085",
            fontSize: 27,
            fontWeight: 600,
            lineHeight: 1.35,
            marginTop: 24,
            maxWidth: 1000,
          }}
        >
          {pilatesLanding.hero.centralMessage}
        </div>
      </div>
      <div style={{ backgroundColor: "#0E8F7E", borderRadius: 999, height: 7, width: 135 }} />
    </div>,
    size,
  );
}
