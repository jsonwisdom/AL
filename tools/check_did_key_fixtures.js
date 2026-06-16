const fs = require('fs');
const path = require('path');
const { decodeDidKey, DidKeyError } = require('../replayloop/did.js');

const VALID_FIXTURE = 'testdata/v1/did-key-valid.json';
const INVALID_DIR = 'testdata/v1/invalid/did-key';

const valid = JSON.parse(fs.readFileSync(VALID_FIXTURE, 'utf8'));
const expectedRaw = valid.raw_public_key_hex;
const actualRaw = Buffer.from(decodeDidKey(valid.did)).toString('hex');

if (actualRaw !== expectedRaw) {
  console.error(`VALID FIXTURE FAILED: got ${actualRaw}, expected ${expectedRaw}`);
  process.exit(1);
}

const files = fs.readdirSync(INVALID_DIR).filter(name => name.endsWith('.json')).sort();

for (const file of files) {
  const fixturePath = path.join(INVALID_DIR, file);
  const fixture = JSON.parse(fs.readFileSync(fixturePath, 'utf8'));
  const expected = fixture.expected_error;

  try {
    decodeDidKey(fixture.did);
    console.error(`INVALID FIXTURE DID NOT FAIL: ${fixturePath}`);
    process.exit(1);
  } catch (error) {
    if (!(error instanceof DidKeyError)) {
      console.error(`INVALID ERROR TYPE in ${fixturePath}: ${error}`);
      process.exit(1);
    }
    if (error.message !== expected) {
      console.error(
        `INVALID FIXTURE WRONG ERROR in ${fixturePath}:\n` +
        `  got:      ${error.message}\n` +
        `  expected: ${expected}`
      );
      process.exit(1);
    }
  }
}

console.log('JS decoder: OK');
