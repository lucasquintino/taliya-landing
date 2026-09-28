import assert from "node:assert/strict";
import fs from "node:fs";
import vm from "node:vm";
import ts from "typescript";

const sourcePath = "lib/landing/ai-attendant/delivery-timing.ts";
const source = fs.readFileSync(sourcePath, "utf8");
const compiled = ts.transpileModule(source, {
  compilerOptions: {
    module: ts.ModuleKind.CommonJS,
    target: ts.ScriptTarget.ES2020,
  },
});

const cjsModule = { exports: {} };
vm.runInNewContext(compiled.outputText, { exports: cjsModule.exports, module: cjsModule });

const { widgetFirstResponseDelay, widgetNextResponseDelay, whatsappReplyDelayMs } = cjsModule.exports;

assert.equal(widgetFirstResponseDelay(1500, false), 700);
assert.equal(widgetFirstResponseDelay(3500, false), 350);
assert.equal(widgetFirstResponseDelay(6500, false), 80);
assert.equal(widgetFirstResponseDelay(1500, true), 900);
assert.equal(widgetFirstResponseDelay(3500, true), 500);
assert.equal(widgetFirstResponseDelay(6500, true), 200);

assert.ok(inRange(widgetNextResponseDelay(1500, 120, 1, false), 900, 1200));
assert.ok(inRange(widgetNextResponseDelay(3500, 120, 1, false), 600, 900));
assert.ok(inRange(widgetNextResponseDelay(6500, 120, 1, false), 400, 700));
assert.ok(inRange(widgetNextResponseDelay(6500, 420, 1, true), 400, 850));

assert.ok(inRange(whatsappReplyDelayMs("Claro, faço sim.", 0), 500, 1000));
assert.ok(inRange(whatsappReplyDelayMs("Claro, faço sim.", 1), 600, 1200));
const longProductAnswer = "Hoje os planos sao Base, Essencial, Avance e Completo. Posso te explicar com calma qual faz sentido para o seu studio a partir do tamanho, da rotina e do gargalo principal que voce quer resolver primeiro.";
assert.ok(inRange(whatsappReplyDelayMs(longProductAnswer, 0), 3500, 3600));
assert.ok(inRange(whatsappReplyDelayMs(longProductAnswer, 1), 4400, 4500));
assert.ok(whatsappReplyDelayMs(longProductAnswer, 1) > whatsappReplyDelayMs("Ok.", 1));

const widgetSource = fs.readFileSync("components/landing/shared/FloatingAiAttendantPanel.tsx", "utf8");
assert.equal(widgetSource.includes("Preparando a resposta"), false);
assert.equal(widgetSource.includes("Digitando"), true);

console.log("agent delivery timing contracts passed");

function inRange(value, min, max) {
  return value >= min && value <= max;
}
