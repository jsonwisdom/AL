import { Lineage, Receipt } from "./types.js";
import { sha256Hex } from "./hash.js";

export function applyEvent(payload: unknown, previousRoot: string): string {
  return sha256Hex({
    previousRoot,
    payload
  });
}

export function replayReceipt(receipt: Receipt, lineage: Lineage): string {
  let root = sha256Hex({ genesis: lineage.genesis });

  for (const eventId of receipt.replay_path) {
    const event = lineage.events[eventId];
    if (!event) throw new Error(`Missing event: ${eventId}`);
    root = applyEvent(event.payload, root);
  }

  return root;
}

export function pathExists(receipt: Receipt, lineage: Lineage): boolean {
  return receipt.replay_path.every((id) => Boolean(lineage.events[id]));
}
