import canonicalize from 'canonicalize';
import { sha256 } from '@noble/hashes/sha256';
import { utf8ToBytes, bytesToHex } from '@noble/hashes/utils';
import { base58btc } from 'multiformats/bases/base58';
import * as ed from '@noble/ed25519';
import Ajv from 'ajv';
import fs from 'node:fs';

const witnessSchema = JSON.parse(fs.readFileSync('schemas/WITNESS_V1.schema.json', 'utf8'));
const ajv = new Ajv({ allErrors: true, strict: false });
const validateWitness = ajv.compile(witnessSchema);

function jcs(value: unknown): string {
  const out = canonicalize(value);
  if (out === undefined) throw new Error('CANONICALIZE_FAILED');
  return out;
}

function hash(data: string): string {
  return 'sha256:' + bytesToHex(sha256(utf8ToBytes(data)));
}

const file = process.argv[2];
if (!file) {
  console.error('usage: verifier <witness.json>');
  process.exit(1);
}

const witness = JSON.parse(fs.readFileSync(file, 'utf8'));

if (!validateWitness(witness)) {
  console.error(validateWitness.errors);
  process.exit(1);
}

const recomputedPayloadHash = hash(jcs(witness.event_payload));
if (recomputedPayloadHash !== witness.envelope.event_payload_hash) {
  console.error('NONCONFORMANT_EVENT_PAYLOAD_HASH');
  process.exit(1);
}

const uidDigest = sha256(utf8ToBytes(jcs(witness.envelope)));
const recomputedUID = 'uid:' + base58btc.encode(uidDigest).slice(1);

if (recomputedUID !== witness.uid) {
  console.error('NONCONFORMANT_UID');
  process.exit(1);
}

const sig = witness.signatures[0];
const signable = {
  ...witness,
  signatures: []
};

const signableHash = sha256(utf8ToBytes(jcs(signable)));

const verified = await ed.verifyAsync(
  sig.signature,
  signableHash,
  sig.public_key
);

if (!verified) {
  console.error('NONCONFORMANT_SIGNATURE');
  process.exit(1);
}

console.log('REPLAY_OK', witness.uid);
