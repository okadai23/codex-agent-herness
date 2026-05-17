import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.',
  projects: [
    {
      name: 'mock',
      testMatch: /tests\/(api|e2e|monkey)\/.*\.spec\.ts/,
      use: {
        baseURL: process.env.PW_BASE_URL ?? 'http://127.0.0.1:3001'
      }
    }
  ]
});
