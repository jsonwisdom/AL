/**
 * MinimalVerifiableKernel v1.0.0
 * License: CC0-1.0
 */

type Hash = `0x${string}`;
type RejectionClass = "FAIL_NUMBER_FORBIDDEN" | "FAIL_MANIFEST_HASH_MISMATCH" | "FAIL_INDEX_GAP" | "FAIL_UNKNOWN";

interface RawEvent { index: number; payload: unknown; manifestRef?: Hash; timestamp?: string; }
interface CanonicalEvent { id: Hash; index: number; canonicalPayload: Uint8Array; manifestUsed: Hash; parentHash: Hash; }
interface CanonicalizationManifest {
  version: string;
  hash: Hash;
  rules: {
    json: "RFC8785";
    text_encoding: "UTF-8";
    text_normalization: "NFC";
    line_endings: "LF";
    float_policy: "forbidden" | "decimal-string";
    timestamp_format: "TAI64";
    ordering: "index-ascending";
  };
  checkpoint_policy?: { mode: "every_event"; record: "post_event_state_root" };
  state_accumulator?: { key_format: "event:{index}:{field}"; ordering: "lexicographic_key_ascending"; serialization: "key:value_lf_no_trailing_newline"; root: "sha256_utf8_0x_hex" };
  rejection_classes?: RejectionClass[];
  pin: { hashFunction: "SHA-256"; hashFunctionSpec: string; };
}
interface EventLog { genesisHash: Hash; manifestRef: Hash; events: CanonicalEvent[]; }
interface ReplayResult { root: Hash; eventCount: number; checkpoints: { index: number; root: Hash }[]; manifestUsed: Hash; degraded: boolean; degradationNotes: string[]; }

const ZERO_HASH = (`0x${"00".repeat(32)}`) as Hash;
const REJECTION_CLASSES: RejectionClass[] = ["FAIL_NUMBER_FORBIDDEN", "FAIL_MANIFEST_HASH_MISMATCH", "FAIL_INDEX_GAP", "FAIL_UNKNOWN"];

function rotr(x: number, n: number): number { return (x >>> n) | (x << (32 - n)); }

function sha256Sync(data: Uint8Array): Hash {
  const k = [0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2];
  const h = [0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19];
  const bitLen = data.length * 8;
  const paddedLen = (((data.length + 9 + 63) >> 6) << 6);
  const padded = new Uint8Array(paddedLen);
  padded.set(data);
  padded[data.length] = 0x80;
  const view = new DataView(padded.buffer);
  view.setUint32(paddedLen - 8, Math.floor(bitLen / 0x100000000), false);
  view.setUint32(paddedLen - 4, bitLen >>> 0, false);
  const w = new Array<number>(64);
  for (let offset = 0; offset < paddedLen; offset += 64) {
    for (let i = 0; i < 16; i++) w[i] = view.getUint32(offset + i * 4, false);
    for (let i = 16; i < 64; i++) {
      const s0 = rotr(w[i - 15], 7) ^ rotr(w[i - 15], 18) ^ (w[i - 15] >>> 3);
      const s1 = rotr(w[i - 2], 17) ^ rotr(w[i - 2], 19) ^ (w[i - 2] >>> 10);
      w[i] = (w[i - 16] + s0 + w[i - 7] + s1) >>> 0;
    }
    let [a,b,c,d,e,f,g,hh] = h;
    for (let i = 0; i < 64; i++) {
      const s1 = rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25);
      const ch = (e & f) ^ (~e & g);
      const temp1 = (hh + s1 + ch + k[i] + w[i]) >>> 0;
      const s0 = rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22);
      const maj = (a & b) ^ (a & c) ^ (b & c);
      const temp2 = (s0 + maj) >>> 0;
      hh = g; g = f; f = e; e = (d + temp1) >>> 0; d = c; c = b; b = a; a = (temp1 + temp2) >>> 0;
    }
    h[0]=(h[0]+a)>>>0; h[1]=(h[1]+b)>>>0; h[2]=(h[2]+c)>>>0; h[3]=(h[3]+d)>>>0;
    h[4]=(h[4]+e)>>>0; h[5]=(h[5]+f)>>>0; h[6]=(h[6]+g)>>>0; h[7]=(h[7]+hh)>>>0;
  }
  return (`0x${h.map(x => x.toString(16).padStart(8,"0")).join("")}`) as Hash;
}

function cloneJson<T>(value: T): T { return JSON.parse(JSON.stringify(value)) as T; }
function jcsCanonicalize(obj: unknown): string {
  if (obj === null || typeof obj !== "object") return JSON.stringify(obj);
  if (Array.isArray(obj)) return `[${obj.map(jcsCanonicalize).join(",")}]`;
  const record = obj as Record<string, unknown>;
  return `{${Object.keys(record).sort().map(k => `${JSON.stringify(k)}:${jcsCanonicalize(record[k])}`).join(",")}}`;
}
function normalizeNFC(obj: unknown): unknown {
  if (typeof obj === "string") return obj.normalize("NFC");
  if (Array.isArray(obj)) return obj.map(normalizeNFC);
  if (obj !== null && typeof obj === "object") {
    const result: Record<string, unknown> = {};
    for (const [k, v] of Object.entries(obj as Record<string, unknown>)) result[k.normalize("NFC")] = normalizeNFC(v);
    return result;
  }
  return obj;
}
function enforceLF(obj: unknown): unknown {
  if (typeof obj === "string") return obj.replace(/\r\n/g, "\n").replace(/\r/g, "\n");
  if (Array.isArray(obj)) return obj.map(enforceLF);
  if (obj !== null && typeof obj === "object") {
    const result: Record<string, unknown> = {};
    for (const [k, v] of Object.entries(obj as Record<string, unknown>)) result[k] = enforceLF(v);
    return result;
  }
  return obj;
}
function enforceNumberPolicy(obj: unknown, policy: "forbidden" | "decimal-string"): unknown {
  if (typeof obj === "number") {
    if (policy === "forbidden") throw new Error(`Number forbidden by manifest: ${obj}`);
    if (!Number.isSafeInteger(obj)) throw new Error(`Number forbidden by manifest: ${obj}`);
    return obj.toString(10);
  }
  if (Array.isArray(obj)) return obj.map(v => enforceNumberPolicy(v, policy));
  if (obj !== null && typeof obj === "object") {
    const result: Record<string, unknown> = {};
    for (const [k, v] of Object.entries(obj as Record<string, unknown>)) result[k] = enforceNumberPolicy(v, policy);
    return result;
  }
  return obj;
}
function toCanonicalBytes(obj: unknown, manifest: CanonicalizationManifest): Uint8Array {
  let working = cloneJson(obj);
  working = normalizeNFC(working);
  working = enforceLF(working);
  working = enforceNumberPolicy(working, manifest.rules.float_policy);
  const canonicalJSON = jcsCanonicalize(working);
  if (canonicalJSON.includes("\n")) throw new Error("Canonical JSON must be single-line");
  return new TextEncoder().encode(canonicalJSON);
}
function stateRoot(state: Map<string, string>): Hash {
  const entries = [...state.entries()].sort(([a], [b]) => a < b ? -1 : a > b ? 1 : 0);
  const serialized = entries.map(([k, v]) => `${k}:${v}`).join("\n");
  return sha256Sync(new TextEncoder().encode(serialized));
}

class CanonicalizationEngine {
  constructor(public readonly manifest: CanonicalizationManifest) { this.validate(); }
  private validate(): void {
    const r = this.manifest.rules;
    if (r.json !== "RFC8785") throw new Error("Only RFC8785 supported");
    if (r.text_encoding !== "UTF-8") throw new Error("Only UTF-8 supported");
    if (r.text_normalization !== "NFC") throw new Error("Only NFC supported");
    if (r.line_endings !== "LF") throw new Error("Only LF supported");
    if (r.timestamp_format !== "TAI64") throw new Error("Only TAI64 supported");
    if (r.ordering !== "index-ascending") throw new Error("Only index-ascending supported");
  }
  canonicalize(raw: RawEvent, parentHash: Hash): CanonicalEvent {
    const canonicalPayload = toCanonicalBytes(raw.payload, this.manifest);
    return { id: sha256Sync(canonicalPayload), index: raw.index, canonicalPayload, manifestUsed: this.manifest.hash, parentHash };
  }
}

class MinimalVerifiableKernel {
  private log: EventLog;
  private manifestCache = new Map<Hash, CanonicalizationManifest>();
  constructor(genesisManifest: CanonicalizationManifest) {
    const computedHash = hashManifest(genesisManifest);
    if (computedHash !== genesisManifest.hash) throw new Error(`Manifest hash mismatch: ${computedHash} !== ${genesisManifest.hash}`);
    this.manifestCache.set(genesisManifest.hash, genesisManifest);
    this.log = { genesisHash: ZERO_HASH, manifestRef: genesisManifest.hash, events: [] };
  }
  registerManifest(manifest: CanonicalizationManifest): void {
    const computedHash = hashManifest(manifest);
    if (computedHash !== manifest.hash) throw new Error(`Manifest hash mismatch: ${computedHash} !== ${manifest.hash}`);
    this.manifestCache.set(manifest.hash, manifest);
  }
  appendEvent(raw: RawEvent): Hash {
    if (raw.index !== this.log.events.length) throw new Error(`Index must be gap-free: expected ${this.log.events.length}, got ${raw.index}`);
    const manifestHash = raw.manifestRef ?? this.log.manifestRef;
    const manifest = this.manifestCache.get(manifestHash);
    if (!manifest) throw new Error(`Manifest not found: ${manifestHash}`);
    const parentHash = this.log.events.length ? this.log.events[this.log.events.length - 1].id : ZERO_HASH;
    const canon = new CanonicalizationEngine(manifest).canonicalize(raw, parentHash);
    this.log.events.push(canon);
    if (this.log.events.length === 1) this.log.genesisHash = canon.id;
    return canon.id;
  }
  replay(manifestHash?: Hash): ReplayResult {
    const targetManifestHash = manifestHash ?? this.log.manifestRef;
    if (!this.manifestCache.has(targetManifestHash)) throw new Error(`Manifest not found: ${targetManifestHash}`);
    const state = new Map<string, string>();
    const checkpoints: { index: number; root: Hash }[] = [];
    const degradationNotes: string[] = [];
    for (const event of this.log.events) {
      if (event.manifestUsed !== targetManifestHash) degradationNotes.push(`Event ${event.index} used manifest ${event.manifestUsed}; target replay manifest is ${targetManifestHash}`);
      state.set(`event:${event.index}:id`, event.id);
      state.set(`event:${event.index}:manifest`, event.manifestUsed);
      state.set(`event:${event.index}:parent`, event.parentHash);
      checkpoints.push({ index: event.index, root: stateRoot(state) });
    }
    return { root: stateRoot(state), eventCount: this.log.events.length, checkpoints, manifestUsed: targetManifestHash, degraded: degradationNotes.length > 0, degradationNotes };
  }
  compareRoots(a: Hash, b: Hash): "MATCH" | "DIVERGENCE" { return a === b ? "MATCH" : "DIVERGENCE"; }
  exportLog(): EventLog { return { genesisHash: this.log.genesisHash, manifestRef: this.log.manifestRef, events: this.log.events.map(e => ({ ...e, canonicalPayload: new Uint8Array(e.canonicalPayload) })) }; }
  get eventCount(): number { return this.log.events.length; }
  get genesisHash(): Hash { return this.log.genesisHash; }
}

function hashManifest(manifest: CanonicalizationManifest): Hash {
  const copy = cloneJson(manifest);
  copy.hash = ZERO_HASH;
  return sha256Sync(new TextEncoder().encode(jcsCanonicalize(copy)));
}

const GENESIS_MANIFEST: CanonicalizationManifest = {
  version: "1.0.0",
  hash: ZERO_HASH,
  rules: { json: "RFC8785", text_encoding: "UTF-8", text_normalization: "NFC", line_endings: "LF", float_policy: "forbidden", timestamp_format: "TAI64", ordering: "index-ascending" },
  checkpoint_policy: { mode: "every_event", record: "post_event_state_root" },
  state_accumulator: { key_format: "event:{index}:{field}", ordering: "lexicographic_key_ascending", serialization: "key:value_lf_no_trailing_newline", root: "sha256_utf8_0x_hex" },
  rejection_classes: REJECTION_CLASSES,
  pin: { hashFunction: "SHA-256", hashFunctionSpec: "FIPS 180-4" }
};
GENESIS_MANIFEST.hash = hashManifest(GENESIS_MANIFEST);

function testReplayParity(): boolean {
  const kernelA = new MinimalVerifiableKernel(GENESIS_MANIFEST);
  const kernelB = new MinimalVerifiableKernel(GENESIS_MANIFEST);
  const events: RawEvent[] = [
    { index: 0, payload: { type: "system_init", manifest_hash: GENESIS_MANIFEST.hash, version: "1.0.0" }, timestamp: "TAI64N:PLACEHOLDER" },
    { index: 1, payload: { type: "genesis_attestation", root: "0xc79d3d89" }, timestamp: "TAI64N:PLACEHOLDER" },
    { index: 2, payload: { type: "schema_registration", schema: "CONSTITUTIONAL_ROOT" }, timestamp: "TAI64N:PLACEHOLDER" }
  ];
  for (const event of events) if (kernelA.appendEvent(event) !== kernelB.appendEvent(event)) return false;
  return kernelA.compareRoots(kernelA.replay().root, kernelB.replay().root) === "MATCH";
}

export { MinimalVerifiableKernel, CanonicalizationEngine, GENESIS_MANIFEST, REJECTION_CLASSES, jcsCanonicalize, stateRoot as merkleRoot, sha256Sync, testReplayParity, toCanonicalBytes };
export type { CanonicalEvent, CanonicalizationManifest, EventLog, Hash, RawEvent, RejectionClass, ReplayResult };
