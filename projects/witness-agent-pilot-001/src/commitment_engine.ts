import { crypto } from "https://deno.land/std@0.177.0/crypto/mod.ts";
import { jcsStringify } from "./jcs.ts";
import { LogEntry, RawLogEntry } from "./types.ts";

export class MembraneCommitmentEngine {
  public async sha256(data: string): Promise<string> {
    const encoder = new TextEncoder();
    const buf = await crypto.subtle.digest("SHA-256", encoder.encode(data));
    return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join('');
  }

  public canonicalize(entry: LogEntry): string {
    return jcsStringify({
      event_type: entry.event_type,
      payload_hash: entry.payload_hash,
      seq: entry.seq,
      timestamp: entry.timestamp,
      prev_hash: entry.prev_hash
    });
  }

  private async hashPair(left: string, right: string): Promise<string> {
    const sorted = [left, right].sort();
    return await this.sha256(sorted[0] + sorted[1]);
  }

  public async buildMerkleRoot(entries: LogEntry[]): Promise<{ root: string; leaves: string[] }> {
    if (entries.length === 0) throw new Error("Empty log");
    let currentLevel = await Promise.all(entries.map(e => this.sha256(this.canonicalize(e))));
    const leaves = [...currentLevel];

    while (currentLevel.length > 1) {
      const nextLevel: string[] = [];
      for (let i = 0; i < currentLevel.length; i += 2) {
        if (i + 1 < currentLevel.length) {
          nextLevel.push(await this.hashPair(currentLevel[i], currentLevel[i + 1]));
        } else {
          nextLevel.push(await this.hashPair(currentLevel[i], currentLevel[i]));
        }
      }
      currentLevel = nextLevel;
    }
    return { root: currentLevel[0], leaves };
  }

  public async generateProof(leaves: string[], index: number): Promise<{ sibling: string; position: 'left' | 'right' }[]> {
    const proof: { sibling: string; position: 'left' | 'right' }[] = [];
    let currentLevel = [...leaves];
    let targetIndex = index;

    while (currentLevel.length > 1) {
      const nextLevel: string[] = [];
      for (let i = 0; i < currentLevel.length; i += 2) {
        const hasRight = i + 1 < currentLevel.length;
        const left = currentLevel[i];
        const right = hasRight ? currentLevel[i + 1] : currentLevel[i];
        
        if (i === targetIndex || i + 1 === targetIndex) {
          if (targetIndex % 2 === 0) {
            proof.push({ sibling: right, position: 'right' });
          } else {
            proof.push({ sibling: left, position: 'left' });
          }
        }
        
        const sorted = [left, right].sort();
        nextLevel.push(await this.sha256(sorted[0] + sorted[1]));
      }
      currentLevel = nextLevel;
      targetIndex = Math.floor(targetIndex / 2);
    }
    return proof;
  }

  public async computeHashChain(rawEntries: RawLogEntry[]): Promise<LogEntry[]> {
    const chain: LogEntry[] = [];
    let prevHash = "0".repeat(64);
    
    for (let i = 0; i < rawEntries.length; i++) {
      const entry: LogEntry = { ...rawEntries[i], prev_hash: prevHash };
      chain.push(entry);
      prevHash = await this.sha256(this.canonicalize(entry));
    }
    return chain;
  }
}
