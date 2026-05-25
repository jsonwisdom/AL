import { ZERO_STATE } from "./zero-state.ts";
import { canonicalize, utf8Bytes, bytesHex } from "./jcs.ts";
import { sha256Hex } from "./digest.ts";
import { engineSignature, exitRuntime } from "./runtime.ts";
import { runMutation001Audit } from "./mutation-001.ts";

function assertEqual(label: string, a: string, b: string): void {
  if (a !== b) {
    console.error(`FAIL:${label}`);
    console.error(JSON.stringify({ a, b }, null, 2));
    exitRuntime(1);
  }
}

function assertBytesEqual(label: string, a: Uint8Array, b: Uint8Array): void {
  if (a.length !== b.length) {
    console.error(`FAIL:${label}:LENGTH`);
    exitRuntime(1);
  }

  for (let i = 0; i < a.length; i++) {
    if (a[i] !== b[i]) {
      console.error(`FAIL:${label}:BYTE_${i}`);
      exitRuntime(1);
    }
  }
}

async function runZeroStateAudit() {
  const stringA = canonicalize(ZERO_STATE);
  const stringB = canonicalize(JSON.parse(JSON.stringify(ZERO_STATE)));

  const bytesA = utf8Bytes(stringA);
  const bytesB = utf8Bytes(stringB);

  const hashA = await sha256Hex(bytesA);
  const hashB = await sha256Hex(bytesB);

  assertEqual("ZERO_CANONICAL_STRING", stringA, stringB);
  assertBytesEqual("ZERO_CANONICAL_BYTES", bytesA, bytesB);
  assertEqual("ZERO_SHA256_HASH", hashA, hashB);

  return {
    gate: "ZERO_STATE_PARITY",
    canonical_string: stringA,
    canonical_bytes_hex: bytesHex(bytesA),
    sha256: hashA
  };
}

const zero = await runZeroStateAudit();
const mutation = await runMutation001Audit();

assertEqual("MUTATION_PRE_HASH_EQUALS_ZERO_HASH", zero.sha256, mutation.pre_state_hash);

console.log(JSON.stringify({
  audit_status: "PASS",
  engine: engineSignature(),
  zero,
  mutation
}, null, 2));
