import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import zlib from "node:zlib";

import { chromium } from "playwright";

const root = process.cwd();
const task = "T011-095";
const feature = "011-taliya-commercial-agent-core-reset";
const baselineDir = path.join(root, "test-results", "spec011-t011-090-pilates-baseline");
const outputDir = path.join(root, "test-results", "spec011-t011-095-pilates-no-drift");
const reportDir = path.join(root, "specs", feature, "eval-reports");
const baselineJsonPath = path.join(baselineDir, "pilates-baseline-before-t011-090.json");
const url = process.env.SPEC011_PILATES_URL ?? "http://127.0.0.1:3021/pilates";
const maxChangedRatio = Number(process.env.SPEC011_PILATES_MAX_CHANGED_RATIO ?? "0.001");
const maxMeanDelta = Number(process.env.SPEC011_PILATES_MAX_MEAN_DELTA ?? "0.25");
const manualReviewStatus = process.env.SPEC011_PILATES_MANUAL_REVIEW ?? "not_provided";
const manualReviewReviewer = process.env.SPEC011_PILATES_MANUAL_REVIEWER ?? "";
const manualReviewNote = process.env.SPEC011_PILATES_MANUAL_REVIEW_NOTE ?? "";
const protectedPaths = [
  "app/pilates",
  "components/landing",
  "data/landing",
  "lib/landing/floating-agent.ts",
  "components/internal/SalesInboxClient.tsx",
];

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function crc32(buffer) {
  let crc = 0xffffffff;
  for (let index = 0; index < buffer.length; index += 1) {
    crc ^= buffer[index];
    for (let bit = 0; bit < 8; bit += 1) {
      crc = (crc >>> 1) ^ (0xedb88320 & -(crc & 1));
    }
  }
  return (crc ^ 0xffffffff) >>> 0;
}

function chunk(type, data) {
  const typeBuffer = Buffer.from(type, "ascii");
  const length = Buffer.alloc(4);
  length.writeUInt32BE(data.length, 0);
  const crcInput = Buffer.concat([typeBuffer, data]);
  const crc = Buffer.alloc(4);
  crc.writeUInt32BE(crc32(crcInput), 0);
  return Buffer.concat([length, typeBuffer, data, crc]);
}

function writePng({ width, height, data }, filePath) {
  const header = Buffer.alloc(13);
  header.writeUInt32BE(width, 0);
  header.writeUInt32BE(height, 4);
  header[8] = 8;
  header[9] = 6;
  header[10] = 0;
  header[11] = 0;
  header[12] = 0;

  const stride = width * 4;
  const raw = Buffer.alloc((stride + 1) * height);
  for (let y = 0; y < height; y += 1) {
    raw[y * (stride + 1)] = 0;
    data.copy(raw, y * (stride + 1) + 1, y * stride, (y + 1) * stride);
  }

  fs.writeFileSync(
    filePath,
    Buffer.concat([
      Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
      chunk("IHDR", header),
      chunk("IDAT", zlib.deflateSync(raw)),
      chunk("IEND", Buffer.alloc(0)),
    ]),
  );
}

function paeth(left, up, upLeft) {
  const estimate = left + up - upLeft;
  const leftDistance = Math.abs(estimate - left);
  const upDistance = Math.abs(estimate - up);
  const upLeftDistance = Math.abs(estimate - upLeft);
  if (leftDistance <= upDistance && leftDistance <= upLeftDistance) return left;
  if (upDistance <= upLeftDistance) return up;
  return upLeft;
}

function decodePng(filePath) {
  const png = fs.readFileSync(filePath);
  const signature = "89504e470d0a1a0a";
  if (png.subarray(0, 8).toString("hex") !== signature) {
    throw new Error(`Invalid PNG signature: ${filePath}`);
  }

  let offset = 8;
  let width = 0;
  let height = 0;
  let colorType = 0;
  const idat = [];
  while (offset < png.length) {
    const length = png.readUInt32BE(offset);
    const type = png.subarray(offset + 4, offset + 8).toString("ascii");
    const data = png.subarray(offset + 8, offset + 8 + length);
    offset += 12 + length;
    if (type === "IHDR") {
      width = data.readUInt32BE(0);
      height = data.readUInt32BE(4);
      colorType = data[9];
      if (data[8] !== 8 || ![2, 6].includes(colorType)) {
        throw new Error(`Unsupported PNG format for ${filePath}: bitDepth=${data[8]} colorType=${colorType}`);
      }
    } else if (type === "IDAT") {
      idat.push(data);
    } else if (type === "IEND") {
      break;
    }
  }

  const channels = colorType === 6 ? 4 : 3;
  const bytesPerPixel = channels;
  const scanlineLength = width * channels;
  const inflated = zlib.inflateSync(Buffer.concat(idat));
  const unfiltered = Buffer.alloc(scanlineLength * height);
  let sourceOffset = 0;

  for (let y = 0; y < height; y += 1) {
    const filter = inflated[sourceOffset];
    sourceOffset += 1;
    const rowOffset = y * scanlineLength;
    const priorRowOffset = (y - 1) * scanlineLength;
    for (let x = 0; x < scanlineLength; x += 1) {
      const raw = inflated[sourceOffset + x];
      const left = x >= bytesPerPixel ? unfiltered[rowOffset + x - bytesPerPixel] : 0;
      const up = y > 0 ? unfiltered[priorRowOffset + x] : 0;
      const upLeft = y > 0 && x >= bytesPerPixel ? unfiltered[priorRowOffset + x - bytesPerPixel] : 0;
      let value = raw;
      if (filter === 1) value = raw + left;
      else if (filter === 2) value = raw + up;
      else if (filter === 3) value = raw + Math.floor((left + up) / 2);
      else if (filter === 4) value = raw + paeth(left, up, upLeft);
      else if (filter !== 0) throw new Error(`Unsupported PNG filter ${filter} in ${filePath}`);
      unfiltered[rowOffset + x] = value & 0xff;
    }
    sourceOffset += scanlineLength;
  }

  const rgba = Buffer.alloc(width * height * 4);
  for (let pixel = 0; pixel < width * height; pixel += 1) {
    rgba[pixel * 4] = unfiltered[pixel * channels];
    rgba[pixel * 4 + 1] = unfiltered[pixel * channels + 1];
    rgba[pixel * 4 + 2] = unfiltered[pixel * channels + 2];
    rgba[pixel * 4 + 3] = colorType === 6 ? unfiltered[pixel * channels + 3] : 255;
  }
  return { width, height, data: rgba };
}

function comparePngs(baselinePath, currentPath, diffPath) {
  const baseline = decodePng(baselinePath);
  const current = decodePng(currentPath);
  if (baseline.width !== current.width || baseline.height !== current.height) {
    return {
      ok: false,
      dimensionMismatch: true,
      baseline: { width: baseline.width, height: baseline.height },
      current: { width: current.width, height: current.height },
      changedPixels: null,
      changedRatio: 1,
      meanDelta: null,
      maxDelta: null,
    };
  }

  let changedPixels = 0;
  let totalDelta = 0;
  let maxDelta = 0;
  const diff = Buffer.alloc(current.data.length);
  for (let index = 0; index < current.data.length; index += 4) {
    const dr = Math.abs(baseline.data[index] - current.data[index]);
    const dg = Math.abs(baseline.data[index + 1] - current.data[index + 1]);
    const db = Math.abs(baseline.data[index + 2] - current.data[index + 2]);
    const da = Math.abs(baseline.data[index + 3] - current.data[index + 3]);
    const delta = Math.max(dr, dg, db, da);
    totalDelta += dr + dg + db + da;
    maxDelta = Math.max(maxDelta, delta);
    if (delta > 8) {
      changedPixels += 1;
      diff[index] = 255;
      diff[index + 1] = 0;
      diff[index + 2] = 80;
      diff[index + 3] = 255;
    } else {
      diff[index] = Math.floor(current.data[index] * 0.25);
      diff[index + 1] = Math.floor(current.data[index + 1] * 0.25);
      diff[index + 2] = Math.floor(current.data[index + 2] * 0.25);
      diff[index + 3] = 255;
    }
  }
  writePng({ width: current.width, height: current.height, data: diff }, diffPath);

  const totalPixels = current.width * current.height;
  const changedRatio = changedPixels / totalPixels;
  const meanDelta = totalDelta / (totalPixels * 4);
  return {
    ok: changedRatio <= maxChangedRatio && meanDelta <= maxMeanDelta,
    dimensionMismatch: false,
    baseline: { width: baseline.width, height: baseline.height },
    current: { width: current.width, height: current.height },
    totalPixels,
    changedPixels,
    changedRatio,
    meanDelta,
    maxDelta,
    diffPath,
  };
}

function protectedSourceDiff() {
  try {
    const output = execFileSync(
      "git",
      ["-c", `safe.directory=${root.replaceAll("\\", "/")}`, "diff", "--name-only", "--", ...protectedPaths],
      { cwd: root, encoding: "utf8" },
    );
    return output.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
  } catch (error) {
    return [`source-diff-check-failed:${error instanceof Error ? error.message : String(error)}`];
  }
}

function manualReviewAccepted() {
  return manualReviewStatus === "approved" && manualReviewReviewer.trim().length > 0 && manualReviewNote.trim().length >= 40;
}

async function capture() {
  const baseline = readJson(baselineJsonPath);
  fs.mkdirSync(outputDir, { recursive: true });
  fs.mkdirSync(reportDir, { recursive: true });

  const browser = await chromium.launch();
  const results = [];
  try {
    for (const baselineResult of baseline.results) {
      const page = await browser.newPage({ viewport: baselineResult.viewport });
      await page.goto(url, { waitUntil: "networkidle", timeout: 60000 });
      await page.screenshot({
        path: path.join(outputDir, `pilates-${baselineResult.id}-after-t011-095.png`),
        fullPage: true,
        animations: "disabled",
      });
      const metrics = await page.evaluate(() => ({
        title: document.title,
        bodyTextLength: document.body.innerText.length,
        scrollWidth: document.documentElement.scrollWidth,
        scrollHeight: document.documentElement.scrollHeight,
        clientWidth: document.documentElement.clientWidth,
        clientHeight: document.documentElement.clientHeight,
        floatingAgent: Boolean(document.querySelector("[data-floating-agent-root], [data-ai-attendant-widget]")),
      }));
      await page.close();

      const currentPath = path.join(outputDir, `pilates-${baselineResult.id}-after-t011-095.png`);
      const diffPath = path.join(outputDir, `pilates-${baselineResult.id}-diff-t011-095.png`);
      const imageComparison = comparePngs(baselineResult.path, currentPath, diffPath);
      const metricDiff = {
        title: { baseline: baselineResult.metrics.title, current: metrics.title },
        bodyTextLength: {
          baseline: baselineResult.metrics.bodyTextLength,
          current: metrics.bodyTextLength,
          delta: metrics.bodyTextLength - baselineResult.metrics.bodyTextLength,
        },
        scrollWidth: {
          baseline: baselineResult.metrics.scrollWidth,
          current: metrics.scrollWidth,
          delta: metrics.scrollWidth - baselineResult.metrics.scrollWidth,
        },
        scrollHeight: {
          baseline: baselineResult.metrics.scrollHeight,
          current: metrics.scrollHeight,
          delta: metrics.scrollHeight - baselineResult.metrics.scrollHeight,
        },
        floatingAgent: {
          baseline: baselineResult.metrics.floatingAgent,
          current: metrics.floatingAgent,
        },
      };
      const metricsOk =
        metricDiff.title.baseline === metricDiff.title.current &&
        metricDiff.scrollWidth.delta === 0 &&
        Math.abs(metricDiff.scrollHeight.delta) <= 2 &&
        metricDiff.floatingAgent.baseline === metricDiff.floatingAgent.current;
      const visualReviewEligible = metricsOk && !imageComparison.ok && !imageComparison.dimensionMismatch;
      const visualReviewAccepted = visualReviewEligible && manualReviewAccepted();
      const visualGate = imageComparison.ok
        ? "strict_pixel_pass"
        : visualReviewAccepted
          ? "pass_with_manual_visual_review"
          : visualReviewEligible
            ? "manual_visual_review_required"
            : "fail";

      results.push({
        id: baselineResult.id,
        viewport: baselineResult.viewport,
        baselinePath: baselineResult.path,
        currentPath,
        diffPath,
        metrics,
        metricDiff,
        metricsOk,
        imageComparison,
        visualGate,
        manualVisualReviewAccepted: visualReviewAccepted,
        ok: metricsOk && (imageComparison.ok || visualReviewAccepted),
      });
    }
  } finally {
    await browser.close();
  }

  const sourceDiff = protectedSourceDiff();
  const summary = {
    total: results.length + 1,
    passed: results.filter((item) => item.ok).length + (sourceDiff.length === 0 ? 1 : 0),
    failed: results.filter((item) => !item.ok).length + (sourceDiff.length === 0 ? 0 : 1),
  };
  const report = {
    runId: `agent-runtime-spec011-pilates-no-drift-${Date.now()}`,
    feature,
    task,
    createdAt: new Date().toISOString(),
    url,
    thresholds: { maxChangedRatio, maxMeanDelta },
    manualReview: {
      status: manualReviewStatus,
      reviewer: manualReviewReviewer,
      note: manualReviewNote,
      accepted: manualReviewAccepted(),
    },
    summary,
    releaseGate:
      summary.failed === 0 && results.every((item) => item.imageComparison.ok)
        ? "pass"
        : summary.failed === 0
          ? "pass_with_manual_visual_review"
          : "fail",
    protectedPaths,
    protectedSourceDiff: sourceDiff,
    results,
  };

  const jsonPath = path.join(reportDir, "agent-runtime-spec011-pilates-no-drift.json");
  const mdPath = path.join(reportDir, "agent-runtime-spec011-pilates-no-drift.md");
  fs.writeFileSync(jsonPath, `${JSON.stringify(report, null, 2)}\n`);
  fs.writeFileSync(
    mdPath,
    [
      "# agent-runtime-spec011-pilates-no-drift",
      "",
      `Generated at: ${report.createdAt}`,
      `URL: ${url}`,
      `Release gate: ${report.releaseGate}`,
      `Passed: ${summary.passed}/${summary.total}`,
      "",
      `Manual review: ${manualReviewAccepted() ? "accepted" : "not accepted"}`,
      `Manual reviewer: ${manualReviewReviewer || "(none)"}`,
      `Manual note: ${manualReviewNote || "(none)"}`,
      "",
      `Protected source diff: ${sourceDiff.length === 0 ? "none" : sourceDiff.join(", ")}`,
      "",
      ...results.flatMap((item) => [
        `## ${item.ok ? "PASS" : "FAIL"} ${item.id}`,
        "",
        `Current screenshot: ${item.currentPath}`,
        `Diff image: ${item.diffPath}`,
        "",
        "```json",
        JSON.stringify(
          {
            metricsOk: item.metricsOk,
            visualGate: item.visualGate,
            manualVisualReviewAccepted: item.manualVisualReviewAccepted,
            metricDiff: item.metricDiff,
            imageComparison: item.imageComparison,
          },
          null,
          2,
        ),
        "```",
        "",
      ]),
    ].join("\n").trim() + "\n",
  );

  if (summary.failed > 0) {
    console.error(`agent-runtime-spec011-pilates-no-drift: ${summary.failed} failure(s). Report: ${jsonPath}`);
    process.exitCode = 1;
  } else {
    console.log(`agent-runtime-spec011-pilates-no-drift: ${summary.passed}/${summary.total} passed. Report: ${jsonPath}`);
  }
}

await capture();
