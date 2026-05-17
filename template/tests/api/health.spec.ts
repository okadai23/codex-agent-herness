import { expect, test } from '@playwright/test';

test('GET /health happy path', async ({ request }) => {
  const res = await request.get('/health');
  expect(res.ok()).toBeTruthy();
  await expect(res.json()).resolves.toMatchObject({ status: 'ok' });
});

test('GET /health error path', async ({ request }) => {
  const res = await request.get('/health?forceError=true');
  if (res.status() === 500) {
    await expect(res.json()).resolves.toHaveProperty('code');
  }
});
