const url = process.env.DATABASE_URL ?? 'postgres://localhost/test_db';
if (!/test|localhost|127\.0\.0\.1/i.test(url)) {
  console.error(`Refusing reset for non-test database: ${url}`);
  process.exit(1);
}
console.log(`Test DB reset allowed for ${url}`);
