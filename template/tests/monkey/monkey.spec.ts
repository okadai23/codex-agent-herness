import { expect, test } from '@playwright/test';

const seed = process.env.MONKEY_SEED ?? 'example';
const steps = Number(process.env.MONKEY_STEPS ?? '20');

test('monkey smoke invariants', async ({ page }) => {
  test.info().annotations.push({ type: 'seed', description: seed });
  await page.goto('/');

  for (let i = 0; i < steps; i += 1) {
    await page.keyboard.press('Tab');
  }

  await expect(page.locator('body')).toBeVisible();
});
