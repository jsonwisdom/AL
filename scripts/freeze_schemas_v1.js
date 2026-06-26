import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const schemaDir = 'continuity-fabric/schemas';
const receiptDir = 'continuity-fabric/receipts';
const frozenPath = path.join(schemaDir, 'FROZEN_v1.0.0.sha256');

const schemas = [
  'Identity.json',
  'Directive.json',
  'Property.json',
  'Influence.json',
  'Integrity.json',
  'Continuity.json'
];

function sortKeys(value) {
  if (Array.isArray(value)) return value.map(sortKeys);
  if (value && typeof value === 'object') {
    return Object.fromEntries(
      Object.entries(value)
        .sort(([a], [b]) => a.localeCompare(b))
        .map(([k, v]) => [k, sortKeys(v)])
    );
  }
  return value;
}

function canonicalize(value) {
  return JSON.stringify(sortKeys(value));
}

function sha256Hex(input) {
  return crypto.createHash('sha256').update(input, 'utf8').digest('hex');
}

fs.mkdirSync(receiptDir, { recursive: true });

const frozenLines = [];

for (const schema of schemas) {
  const schemaPath = path.join(schemaDir, schema);
  const raw = fs.readFileSync(schemaPath, 'utf8');
  const parsed = JSON.parse(raw);
  const canonical = canonicalize(parsed);
  const digest = sha256Hex(canonical);

  frozenLines.push(`${digest}  ${schemaPath}`);

  const base = schema.replace(/\.json$/, '');
  const upper = base.toUpperCase();
  const receipt = {
    receipt_id: `${upper}_FREEZE_V1`,
    schema_path: schemaPath,
    schema_version: '1.0.0',
    canonicalization: 'JCS',
    hash_algorithm: 'sha256',
    schema_sha256: digest,
    status: 'FROZEN',
    authority: false
  };

  fs.writeFileSync(
    path.join(receiptDir, `${upper}_FREEZE_V1.json`),
    `${JSON.stringify(sortKeys(receipt), null, 2)}\n`
  );
}

fs.writeFileSync(frozenPath, `${frozenLines.join('\n')}\n`);

console.log(`wrote ${frozenPath}`);
console.log(`wrote ${schemas.length} freeze receipts`);
