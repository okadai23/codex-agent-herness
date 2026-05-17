import { readFileSync, readdirSync } from 'node:fs';
const files = readdirSync('packages/db/migrations').filter((f) => f.endsWith('.sql'));
const risky = [];
for (const file of files) {
  const sql = readFileSync(`packages/db/migrations/${file}`, 'utf8').toUpperCase();
  const normalizedSql = sql.replace(/\s+/g, ' ');
  if (
    /DROP\s+TABLE/.test(normalizedSql)
    || /DROP\s+COLUMN/.test(normalizedSql)
    || /TRUNCATE/.test(normalizedSql)
  ) {
    risky.push(file);
  }
}
if (risky.length) {
  console.error(`Destructive migration detected: ${risky.join(', ')}`);
  process.exit(1);
}
console.log('Migration safety check passed');
