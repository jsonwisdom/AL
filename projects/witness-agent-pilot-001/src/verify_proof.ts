import { MembraneCommitmentEngine, LogEntry } from "./commitment_engine.ts";

export async function verifySelectiveDisclosure(
  publicRoot: string,
  exposedEntry: LogEntry,
  proof: { sibling: string; position: 'left' | 'right' }[]
): Promise<boolean> {
  const engine = new MembraneCommitmentEngine();
  let currentHash = await engine.sha256(engine.canonicalize(exposedEntry));

  for (const p of proof) {
    const sorted = [currentHash, p.sibling].sort();
    currentHash = await engine.sha256(sorted[0] + sorted[1]);
  }
  return currentHash === publicRoot;
}
