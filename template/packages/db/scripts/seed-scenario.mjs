import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
const scenario = process.argv[2] ?? 'base';
const json = JSON.parse(readFileSync(`packages/db/seeds/scenarios/${scenario}.json`, 'utf8'));
mkdirSync('.tmp/db', { recursive: true });
writeFileSync('.tmp/db/seed-state.json', JSON.stringify({ scenario, data: json }, null, 2));
console.log(`Seeded scenario: ${scenario}`);
