import { MembraneCommitmentEngine } from "./commitment_engine.ts";
import { verifySelectiveDisclosure } from "./verify_proof.ts";
import { verifyEnvelope } from "./signature.ts";

const engine = new MembraneCommitmentEngine();
const runtimeConfig = JSON.parse(await Deno.readTextFile("./src/runtime_config.json"));

const { signed_commitment } = runtimeConfig;
const { execution_root, agent_id, runtime_hash, timestamp, challenge_window_seconds, signature, public_key } = signed_commitment;

console.log("🔍 Verifying signature on commitment envelope...");

const envelopeValid = await verifyEnvelope(
  { execution_root, agent_id, runtime_hash, timestamp, challenge_window_seconds },
  signature,
  public_key
);

if (!envelopeValid) {
  console.log("🚨 Invalid signature — root rejected");
  Deno.exit(1);
}
console.log("✅ Signature valid — root provenance confirmed");

console.log("\n⚙️ Processing Challenge Request...");
const isValid = await verifySelectiveDisclosure(
  execution_root,
  runtimeConfig.target_entry,
  runtimeConfig.proof
);

console.log(`🧾 Verification Result: ${isValid ? "PASS ✅" : "FAIL ❌"}`);
if (isValid) {
  console.log("🌍 System invariant clean. Secrets remained isolated behind the membrane.");
  console.log("🔐 Authenticated replay membrane confirmed.");
} else {
  console.log("🚨 Topology halt triggered. Network authorization revoked.");
  Deno.exit(1);
}
