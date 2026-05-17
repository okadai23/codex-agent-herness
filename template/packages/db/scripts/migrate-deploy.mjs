import { mkdirSync, readdirSync, writeFileSync } from 'node:fs';
mkdirSync('.tmp/db', { recursive: true });
const migrations = readdirSync('packages/db/migrations').filter((f) => f.endsWith('.sql'));
writeFileSync('.tmp/db/deploy-migrations-applied.json', JSON.stringify({ migrations }, null, 2));
console.log(`Prepared ${migrations.length} migrations for deploy`);
