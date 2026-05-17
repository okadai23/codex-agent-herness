import { defineConfig } from 'orval';

export default defineConfig({
  api: {
    input: 'packages/api-contract/openapi.yaml',
    output: {
      target: 'packages/api-client/src/generated/client.ts',
      mock: {
        type: 'msw',
        path: 'packages/api-mocks/src/generated/handlers.ts'
      },
      mode: 'split',
      schemas: 'packages/api-client/src/generated/schemas'
    }
  }
});
