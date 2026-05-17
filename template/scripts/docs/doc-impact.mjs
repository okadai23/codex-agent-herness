import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const indexPath = path.join(root, 'docs/_meta/doc-index.yaml');

function walk(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.name === 'node_modules' || e.name === '.git') continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else out.push(path.relative(root, p).replaceAll('\\\\', '/'));
  }
  return out;
}

function parseIndex(text) {
  const mappings = [];
  let current = null;
  let mode = '';
  for (const line of text.split(/\r?\n/)) {
    if (line.startsWith('  - id:')) {
      if (current) mappings.push(current);
      current = { id: line.split(':', 2)[1].trim(), when: [], docs: [] };
      mode = '';
    } else if (line.trim() === 'when:') mode = 'when';
    else if (line.trim() === 'docs:') mode = 'docs';
    else if (current && line.trim().startsWith('- ')) {
      const v = line.trim().slice(2).trim();
      if (mode === 'when') current.when.push(v);
      if (mode === 'docs') current.docs.push(v);
    }
  }
  if (current) mappings.push(current);
  return mappings;
}

function globToRe(glob) {
  const escaped = glob.replace(/[.+^${}()|[\]\\]/g, '\\$&').replaceAll('**', '::DOUBLE::').replaceAll('*', '[^/]*').replaceAll('::DOUBLE::', '.*');
  return new RegExp(`^${escaped}$`);
}

function match(pattern, file) {
  return globToRe(pattern).test(file);
}

const idx = fs.readFileSync(indexPath, 'utf-8');
const mappings = parseIndex(idx);
const changedArg = process.argv.find((a) => a.startsWith('--changed='));
const changed = changedArg ? changedArg.slice('--changed='.length).split(',').map((s) => s.trim()).filter(Boolean) : walk(root);

const impacted = new Set();
for (const m of mappings) {
  if (changed.some((f) => m.when.some((p) => match(p, f)))) {
    m.docs.forEach((d) => impacted.add(d));
  }
}

if (!impacted.size) {
  console.log('No docs impact detected.');
  process.exit(0);
}

console.log('Impacted docs:');
for (const d of [...impacted].sort()) console.log(`- ${d}`);
