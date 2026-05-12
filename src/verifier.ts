import canonicalize from 'canonicalize';
import { sha256 } from '@noble/hashes/sha256';
import { utf8ToBytes, bytesToHex } from '@noble/hashes/utils';
import { base58btc } from 'multiformats/bases/base58';
import * as ed from '@noble/ed25519';
import Ajv from 'ajv';
import fs from 'node:fs';

const witnessSchema = JSON.parse(fs.readFileSync('schemas/WITNESS_V1.schema.json', 'utf8'));
const ajv = new Ajv({ allErrors: true, strict: true });
const validateWitness = ajv.compile(witnessSchema);

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

const eventPayloadCanonical = canonicalize(witness.event_payload)!;
const recomputedPayloadHash = hash(eventPayloadCanonical);

if (recomputedPayloadHash !== witness.envelope.event_payload_hash) {
  console.error('NONCONFORMANT_EVENT_PAYLOAD_HASH');
  process.exit(1);
}

const envelopeCanonical = canonicalize(witness.envelope)!;
const uidDigest = sha256(utf8ToBytes(envelopeCanonical));
const recomputedUID = 'uid:' + base58btc.encode(uidDigest).replace('z', '');

if (recomputedUID !== witness.uid) {
  console.error('NONCONFORMANT_UID');
  process.exit(1);
}

const sig = witness.signatures[0];
const signable = canonicalize({ ...witness, signatures: [] })!;
const signableHash = sha256(utf8ToBytes(signable));

const verified = await ed.verifyAsync(
  sig.signature,
  signableHash,
  sig.public_key
);

if (!verified) {
  console.error('NONCONFORMANT_SIGNATURE');
  process.exit(1);
}

console.log('VALID', witness.uid);
