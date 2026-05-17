import { defineConfig } from '@playwright/test';

const appBaseURL = process.env.PW_BASE_URL ?? 'http://127.0.0.1:3001';
const apiBaseURL = process.env.PW_API_BASE_URL ?? process.env.PW_BASE_URL ?? 'http://localhost:3000';

export default defineConfig({
  testDir: '.',
  projects: [
    {
      name: 'api',
      testMatch: /tests\/api\/.*\.spec\.ts/,
      use: {
        baseURL: apiBaseURL
      }
    },
    {
      name: 'app',
      testMatch: /tests\/(e2e|monkey)\/.*\.spec\.ts/,
      use: {
        baseURL: appBaseURL
      }
    }
  ]
});
