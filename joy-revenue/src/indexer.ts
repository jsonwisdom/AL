import { decodeEventLog, parseAbiItem, type Address } from "viem";

import {
  JOY_CONTRACT_ADDRESS,
  START_BLOCK,
  ZERO_KEY_RULING,
  assertVerifiedTarget,
  targetReceipt
} from "./config.js";
import { client } from "./rpc.js";
import { applyTransfer, snapshotOwnership, type OwnershipState } from "./state.js";

const ownership: OwnershipState = new Map();

const transferEvent = parseAbiItem(
  "event Transfer(address indexed from, address indexed to, uint256 tokenId)"
);

async function main() {
  console.log(JSON.stringify({
    subsystem: "joy-revenue-indexer",
    mode: "read_only_event_indexer",
    target: targetReceipt(),
    start_block: START_BLOCK.toString(),
    ...ZERO_KEY_RULING
  }));

  assertVerifiedTarget();

  await client.watchEvent({
    address: JOY_CONTRACT_ADDRESS,
    event: transferEvent,
    fromBlock: START_BLOCK,
    onLogs: (logs) => {
      for (const log of logs) {
        const decoded = decodeEventLog({
          abi: [transferEvent],
          data: log.data,
          topics: log.topics
        });

        if (decoded.eventName !== "Transfer") continue;

        const { from, to, tokenId } = decoded.args as {
          from: Address;
          to: Address;
          tokenId: bigint;
        };

        applyTransfer(ownership, { from, to, tokenId });

        console.log(JSON.stringify({
          type: "transfer_observed",
          block_number: log.blockNumber?.toString(),
          tx_hash: log.transactionHash,
          log_index: log.logIndex,
          from,
          to,
          token_id: tokenId.toString(),
          ownership_snapshot: snapshotOwnership(ownership),
          target: targetReceipt(),
          ...ZERO_KEY_RULING
        }));
      }
    },
    onError: (error) => {
      console.error(JSON.stringify({
        type: "indexer_error",
        error: error.message,
        target: targetReceipt(),
        ...ZERO_KEY_RULING
      }));
    }
  });
}

main().catch((err) => {
  console.error(JSON.stringify({
    type: "indexer_halted",
    error: err instanceof Error ? err.message : String(err),
    target: targetReceipt(),
    ...ZERO_KEY_RULING
  }));
  process.exit(1);
});
