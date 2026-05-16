import { jcsStringify } from "./jcs.ts";
import { verifyEnvelope } from "./signature.ts";
import { verifySelectiveDisclosure } from "./verify_proof.ts";
import { LogEntry, SignedCommitment } from "./types.ts";

async function sha256(data: string): Promise<string> {
  const encoder = new TextEncoder();
  const buf = await crypto.subtle.digest("SHA-256", encoder.encode(data));
  return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join('');
}

async function canonicalizeEntry(entry: LogEntry): Promise<string> {
  return jcsStringify({
    event_type: entry.event_type,
    payload_hash: entry.payload_hash,
    seq: entry.seq,
    timestamp: entry.timestamp,
    prev_hash: entry.prev_hash
  });
}

async function verifyHashChain(entries: LogEntry[]): Promise<boolean> {
  const genesisZero = "0".repeat(64);
  if (entries[0].prev_hash !== genesisZero) {
    console.log("❌ Genesis prev_hash is not all zeros");
    return false;
  }

  let prevHash = genesisZero;
  for (let i = 0; i < entries.length; i++) {
    const canonical = await canonicalizeEntry(entries[i]);
    const computedHash = await sha256(canonical);
    
    if (entries[i].prev_hash !== prevHash) {
      console.log(`❌ Entry ${i} prev_hash mismatch`);
      return false;
    }
    prevHash = computedHash;
  }
  console.log(`✅ Hash chain valid (${entries.length} entries)`);
  return true;
}

async function rebuildMerkleRoot(entries: LogEntry[]): Promise<string> {
  let currentLevel = await Promise.all(
    entries.map(e => sha256(jcsStringify({
      event_type: e.event_type,
      payload_hash: e.payload_hash,
      seq: e.seq,
      timestamp: e.timestamp,
      prev_hash: e.prev_hash
    })))
  );

  while (currentLevel.length > 1) {
    const nextLevel: string[] = [];
    for (let i = 0; i < currentLevel.length; i += 2) {
      const left = currentLevel[i];
      const right = i + 1 < currentLevel.length ? currentLevel[i + 1] : currentLevel[i];
      const sorted = [left, right].sort();
      nextLevel.push(await sha256(sorted[0] + sorted[1]));
    }
    currentLevel = nextLevel;
  }
  return currentLevel[0];
}

async function independentVerification() {
  console.log("🔍 INDEPENDENT VERIFIER — Constitutional Test\n");

  const chainContent = await Deno.readTextFile("./logs/execution_log_chain.jsonl");
  const entries: LogEntry[] = chainContent.trim().split("\n").map(line => JSON.parse(line));
  
  if (entries.length === 0) {
    console.log("🚨 Empty chain — constitutional failure");
    Deno.exit(1);
  }
  console.log(`📋 Loaded ${entries.length} chained log entries`);

  const runtimeConfig = JSON.parse(await Deno.readTextFile("./src/runtime_config.json"));
  const signedCommitment: SignedCommitment = runtimeConfig.signed_commitment;
  const { execution_root, agent_id, runtime_hash, timestamp, challenge_window_seconds, signature, public_key } = signedCommitment;

  console.log("\n🔗 Verifying hash chain...");
  const chainValid = await verifyHashChain(entries);
  if (!chainValid) Deno.exit(1);

  console.log("\n🌿 Rebuilding Merkle root from chain...");
  const rebuiltRoot = await rebuildMerkleRoot(entries);
  if (rebuiltRoot !== execution_root) {
    console.log("❌ Merkle root mismatch");
    Deno.exit(1);
  }
  console.log("✅ Merkle root matches");

  console.log("\n✍️ Verifying signature...");
  const signatureValid = await verifyEnvelope(
    { execution_root, agent_id, runtime_hash, timestamp, challenge_window_seconds },
    signature,
    public_key
  );
  if (!signatureValid) Deno.exit(1);
  console.log("✅ Signature valid");

  console.log("\n📎 Verifying selective disclosure proof...");
  const proofValid = await verifySelectiveDisclosure(
    execution_root,
    runtimeConfig.target_entry,
    runtimeConfig.proof
  );
  if (!proofValid) Deno.exit(1);
  console.log("✅ Selective disclosure proof valid");

  console.log("\n🧾 CONSTITUTIONAL REPLAY PASS");
  console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
  console.log("🌍 No operator trust required.");
  console.log("🔐 Membrane holds without privileged access.");
  console.log("📜 Witness Agent Pilot 001 — INDEPENDENT REPLAY CONFIRMED");
}

await independentVerification();
