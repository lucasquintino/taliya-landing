
import { test, expect } from '@playwright/test';

const appUrl = "http://127.0.0.1:3999";
const demoUrl = "https://www.taliya.com.br/pilates/planos/demonstracao";
const desktopPath = "C:/Users/lucas/agentes-landing-system/specs/010-openai-cs-agents-adaptation-for-taliya-commercial/eval-reports/assets/autonomous-widget-sales-cost-tone-latest/widget-demo-desktop.png";
const mobilePath = "C:/Users/lucas/agentes-landing-system/specs/010-openai-cs-agents-adaptation-for-taliya-commercial/eval-reports/assets/autonomous-widget-sales-cost-tone-latest/widget-demo-mobile.png";

async function exerciseWidget(page, screenshotPath) {
  await page.goto(appUrl + '/pilates', { waitUntil: 'networkidle' });
  await expect(page.getByLabel('Abrir atendimento')).toBeVisible({ timeout: 20000 });
  await page.getByLabel('Abrir atendimento').click();
  await page.getByPlaceholder('Pergunte sobre planos ou rotina...').fill('quero ver uma demonstracao');
  await page.getByLabel('Enviar mensagem').click();
  const demoAction = page.locator('a[href="' + demoUrl + '"]').first();
  await expect(demoAction).toBeVisible({ timeout: 60000 });
  await page.screenshot({ path: screenshotPath, fullPage: true });
  await expect(demoAction).toContainText(/^Ver demonstra/i);
}

test('desktop widget demo CTA renders', async ({ page }) => {
  await page.setViewportSize({ width: 1365, height: 900 });
  await exerciseWidget(page, desktopPath);
});

test('mobile widget demo CTA renders', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await exerciseWidget(page, mobilePath);
});
