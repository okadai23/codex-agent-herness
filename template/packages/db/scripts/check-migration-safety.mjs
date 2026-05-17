import { readFileSync, readdirSync } from 'node:fs';
const files = readdirSync('packages/db/migrations').filter((f) => f.endsWith('.sql'));
const risky = [];
for (const file of files) {
  const sql = readFileSync(`packages/db/migrations/${file}`, 'utf8').toUpperCase();
  if (sql.includes('DROP TABLE') || sql.includes('DROP COLUMN') || sql.includes('TRUNCATE')) risky.push(file);
}
if (risky.length) {
  console.error(`Destructive migration detected: ${risky.join(', ')}`);
  process.exit(1);
}
console.log('Migration safety check passed');
