const rawUrl = process.env.DATABASE_URL ?? 'postgres://localhost/test_db';

let parsedUrl;
try {
  parsedUrl = new URL(rawUrl);
} catch {
  console.error(`Refusing reset for unparseable DATABASE_URL: ${rawUrl}`);
  process.exit(1);
}

const hostname = parsedUrl.hostname.toLowerCase();
const databaseName = parsedUrl.pathname.replace(/^\//, '').toLowerCase();
const isLocalHost = hostname === 'localhost' || hostname === '127.0.0.1';
const isTestDatabase = /(^|[_-])test([_-]|$)/i.test(databaseName);

if (!isLocalHost && !isTestDatabase) {
  console.error(`Refusing reset for non-test database host/name: ${rawUrl}`);
  process.exit(1);
}

console.log(`Test DB reset allowed for ${rawUrl}`);
