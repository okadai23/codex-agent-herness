import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const docsDir = path.join(root, 'docs');

function walk(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else out.push(p);
  }
  return out;
}

const files = walk(docsDir).filter((f) => /\.(md|ya?ml)$/i.test(f));
const secrets = [/(?:sk|api|ghp)_[A-Za-z0-9]{16,}/, /AKIA[0-9A-Z]{16}/];
const today = new Date().toISOString().slice(0, 10);
let failed = false;

for (const file of files) {
  const rel = path.relative(root, file).replaceAll('\\\\', '/');
  const txt = fs.readFileSync(file, 'utf-8');
  for (const pat of secrets) {
    if (pat.test(txt)) {
      console.error(`[secret] ${rel}`);
      failed = true;
    }
  }

  const staleMatch = txt.match(/stale_after:\s*(\d{4}-\d{2}-\d{2})/);
  if (staleMatch && staleMatch[1] < today) {
    console.error(`[stale] ${rel} stale_after=${staleMatch[1]}`);
    failed = true;
  }

  const lines = txt.split(/\r?\n/);
  lines.forEach((line, idx) => {
    if (line.length > 140) {
      console.error(`[lint] ${rel}:${idx + 1} line too long`);
      failed = true;
    }
    const m = line.match(/\[[^\]]+\]\(([^)]+)\)/);
    if (m && !/^https?:\/\//.test(m[1])) {
      const target = path.resolve(path.dirname(file), m[1]);
      if (!fs.existsSync(target)) {
        console.error(`[link] ${rel}:${idx + 1} missing ${m[1]}`);
        failed = true;
      }
    }
  });
}

if (failed) process.exit(1);
console.log('docs verification passed');
