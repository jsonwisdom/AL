import { decodeEventLog, parseAbiItem, type Address } from "viem";

import { JOY_CONTRACT_ADDRESS, START_BLOCK, ZERO_KEY_RULING } from "./config.js";
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
    contract: JOY_CONTRACT_ADDRESS,
    start_block: START_BLOCK.toString(),
    ...ZERO_KEY_RULING
  }));

  if (JOY_CONTRACT_ADDRESS === "0x0000000000000000000000000000000000000000") {
    console.error("JOY_CONTRACT_ADDRESS is not set. Refusing fake revenue indexing.");
    process.exit(1);
  }

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
          ...ZERO_KEY_RULING
        }));
      }
    },
    onError: (error) => {
      console.error(JSON.stringify({
        type: "indexer_error",
        error: error.message,
        ...ZERO_KEY_RULING
      }));
    }
  });
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
