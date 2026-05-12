import canonicalize from 'canonicalize';
import { sha256 } from '@noble/hashes/sha256';
import { utf8ToBytes, bytesToHex } from '@noble/hashes/utils';
import { base58btc } from 'multiformats/bases/base58';
import * as ed from '@noble/ed25519';
import Ajv from 'ajv';
import fs from 'node:fs';

const uidSchema = JSON.parse(fs.readFileSync('schemas/UID_V1.schema.json', 'utf8'));
const witnessSchema = JSON.parse(fs.readFileSync('schemas/WITNESS_V1.schema.json', 'utf8'));

const ajv = new Ajv({ allErrors: true, strict: true });
const validateUID = ajv.compile(uidSchema);
const validateWitness = ajv.compile(witnessSchema);

function hash(data: string): string {
  return 'sha256:' + bytesToHex(sha256(utf8ToBytes(data)));
}

const eventPayload = {
  workflow: 'gauntlet',
  run_id: 27,
  commit: 'a2d2b013dfe1a7bb63c997747c87958794d5d660',
  status: 'GREEN'
};

const eventPayloadCanonical = canonicalize(eventPayload)!;
const eventPayloadHash = hash(eventPayloadCanonical);

const envelope = {
  schema: 'alms/uid@v1',
  schema_hash: hash(
    fs.readFileSync('schemas/UID_V1.schema.json', 'utf8') +
    fs.readFileSync('schemas/WITNESS_V1.schema.json', 'utf8')
  ),
  kind: 'GAUNTLET_RUN',
  repo: 'jsonwisdom/AL',
  timestamp_logical: 1,
  state_hash: hash('WHOLE_REPO_RUNTIME_GREEN'),
  engine_fingerprint: hash('node-ts-runtime'),
  event_payload_hash: eventPayloadHash
};

if (!validateUID(envelope)) {
  console.error(validateUID.errors);
  process.exit(1);
}

const envelopeCanonical = canonicalize(envelope)!;
const uidDigest = sha256(utf8ToBytes(envelopeCanonical));
const uid = 'uid:' + base58btc.encode(uidDigest).replace('z', '');

const privateKey = ed.utils.randomPrivateKey();
const publicKey = await ed.getPublicKeyAsync(privateKey);

const witness = {
  schema: 'alms/witness@v1',
  uid,
  envelope,
  event_payload: eventPayload,
  artifacts: [
    {
      path: '.github/workflows/gauntlet.yml',
      sha256: hash(fs.readFileSync('.github/workflows/gauntlet.yml', 'utf8'))
    }
  ],
  signatures: []
};

const signable = canonicalize(witness)!;
const signableHash = sha256(utf8ToBytes(signable));
const signature = await ed.signAsync(signableHash, privateKey);

witness.signatures.push({
  algorithm: 'Ed25519',
  public_key: bytesToHex(publicKey),
  signature: bytesToHex(signature)
});

if (!validateWitness(witness)) {
  console.error(validateWitness.errors);
  process.exit(1);
}

fs.mkdirSync('.runtime/witnesses', { recursive: true });
fs.writeFileSync(
  `.runtime/witnesses/${uid}.json`,
  canonicalize(witness)!
);

console.log('EMITTED', uid);
