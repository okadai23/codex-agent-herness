import { mkdirSync, readdirSync, writeFileSync } from 'node:fs';
mkdirSync('.tmp/db', { recursive: true });
const migrations = readdirSync('packages/db/migrations').filter((f) => f.endsWith('.sql'));
writeFileSync('.tmp/db/dev-migrations-applied.json', JSON.stringify({ migrations }, null, 2));
console.log(`Applied ${migrations.length} migrations to test DB`);
