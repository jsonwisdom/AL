import { MembraneCommitmentEngine } from "./commitment_engine.ts";
import { RawLogEntry, LogEntry, CommitmentEnvelope, SignedCommitment } from "./types.ts";
import { signEnvelope } from "./signature.ts";

const engine = new MembraneCommitmentEngine();

const logContent = await Deno.readTextFile("./logs/execution_log.jsonl");
const rawEntries: RawLogEntry[] = logContent
  .trim()
  .split("\n")
  .map(line => JSON.parse(line));

const entries: LogEntry[] = await engine.computeHashChain(rawEntries);

await Deno.writeTextFile("./logs/execution_log_chain.jsonl", 
  entries.map(e => JSON.stringify(e)).join("\n")
);

const { root, leaves } = await engine.buildMerkleRoot(entries);

const agent_id = "jaywisdom.base.eth/agent-pilot-001";
const runtime_hash = await engine.sha256(await Deno.readTextFile("./src/commitment_engine.ts"));

const envelope: CommitmentEnvelope = {
  execution_root: root,
  agent_id: agent_id,
  runtime_hash: runtime_hash,
  timestamp: Math.floor(Date.now() / 1000),
  challenge_window_seconds: 259200
};

const privateKeyHex = (await Deno.readTextFile("./keys/private_key.pkcs8.hex")).trim();
const signature = await signEnvelope(envelope, privateKeyHex);
const publicKeyHex = (await Deno.readTextFile("./keys/public_key.hex")).trim();

const signedCommitment: SignedCommitment = {
  ...envelope,
  signature,
  public_key: publicKeyHex
};

const runtimeConfig = {
  execution_root: root,
  leaves: leaves,
  target_index: 1,
  target_entry: entries[1],
  proof: await engine.generateProof(leaves, 1),
  signed_commitment: signedCommitment
};

await Deno.writeTextFile("./src/runtime_config.json", JSON.stringify(runtimeConfig, null, 2));
console.log("✅ Runtime config with signed commitment written");
console.log("🔐 Execution root:", root);
console.log("✍️ Signature:", signature.slice(0, 32) + "...");
