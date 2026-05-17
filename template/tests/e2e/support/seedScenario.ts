import { execSync } from 'node:child_process';

export function seedScenario(name: string) {
  const dbUrl = process.env.DATABASE_URL ?? 'postgres://localhost/test_db';
  if (!/test|localhost|127\.0\.0\.1/i.test(dbUrl)) {
    throw new Error(`production DB URLではreset不可: ${dbUrl}`);
  }
  execSync(`node packages/db/scripts/reset-test-db.mjs`, { stdio: 'inherit' });
  execSync(`node packages/db/scripts/seed-scenario.mjs ${name}`, { stdio: 'inherit' });
}
