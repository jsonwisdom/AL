import {
  createPublicClient,
  decodeEventLog,
  erc20Abi,
  getAddress,
  http,
  parseAbiItem,
  type Address,
  type Hash
} from "viem";

import {
  JOY_CONTRACT_ADDRESS,
  RPC_URL,
  START_BLOCK,
  ZERO_KEY_RULING,
  assertVerifiedTarget,
  targetReceipt
} from "./config.js";

const transferEvent = parseAbiItem(
  "event Transfer(address indexed from, address indexed to, uint256 value)"
);

const creatorAddress = process.env.CREATOR_ADDRESS
  ? getAddress(process.env.CREATOR_ADDRESS)
  : undefined;

const rewardsContractAddress = process.env.REWARDS_CONTRACT_ADDRESS
  ? getAddress(process.env.REWARDS_CONTRACT_ADDRESS)
  : undefined;

const rewardsEventAbi = process.env.REWARDS_EVENT_ABI;

const client = createPublicClient({
  transport: http(RPC_URL.replace(/^wss:/, "https:").replace(/^ws:/, "http:"))
});

function asString(value: unknown): string {
  return typeof value === "bigint" ? value.toString() : String(value);
}

function uniq(values: Iterable<string>) {
  return [...new Set(values.map((v) => v.toLowerCase()))];
}

async function readTokenMetadata() {
  const [name, symbol, decimals, totalSupply] = await Promise.all([
    client.readContract({ address: JOY_CONTRACT_ADDRESS, abi: erc20Abi, functionName: "name" }),
    client.readContract({ address: JOY_CONTRACT_ADDRESS, abi: erc20Abi, functionName: "symbol" }),
    client.readContract({ address: JOY_CONTRACT_ADDRESS, abi: erc20Abi, functionName: "decimals" }),
    client.readContract({ address: JOY_CONTRACT_ADDRESS, abi: erc20Abi, functionName: "totalSupply" })
  ]);

  return {
    name,
    symbol,
    decimals,
    total_supply_raw: totalSupply.toString()
  };
}

async function readTransferSurface(toBlock: bigint) {
  const logs = await client.getLogs({
    address: JOY_CONTRACT_ADDRESS,
    event: transferEvent,
    fromBlock: START_BLOCK,
    toBlock
  });

  const transfers = logs.map((log) => {
    const decoded = decodeEventLog({
      abi: [transferEvent],
      data: log.data,
      topics: log.topics
    });

    const args = decoded.args as {
      from: Address;
      to: Address;
      value: bigint;
    };

    return {
      block_number: log.blockNumber?.toString(),
      tx_hash: log.transactionHash as Hash,
      log_index: log.logIndex,
      from: args.from,
      to: args.to,
      value_raw: args.value.toString()
    };
  });

  const totalTransferRaw = transfers.reduce((sum, transfer) => sum + BigInt(transfer.value_raw), 0n);
  const senders = uniq(transfers.map((t) => t.from));
  const recipients = uniq(transfers.map((t) => t.to));
  const touched = uniq([...senders, ...recipients]);

  return {
    from_block: START_BLOCK.toString(),
    to_block: toBlock.toString(),
    transfer_log_count: transfers.length,
    unique_senders_observed: senders.length,
    unique_recipients_observed: recipients.length,
    unique_addresses_touched_observed: touched.length,
    transfer_volume_raw_observed: totalTransferRaw.toString(),
    sample_transfers: transfers.slice(-25)
  };
}

async function readRewardsSurface(toBlock: bigint) {
  if (!creatorAddress || !rewardsContractAddress || !rewardsEventAbi) {
    return {
      configured: false,
      creator_earnings_confirmed: false,
      reason: "CREATOR_ADDRESS, REWARDS_CONTRACT_ADDRESS, and REWARDS_EVENT_ABI are required before rewards logs can be classified."
    };
  }

  const event = parseAbiItem(rewardsEventAbi as `event ${string}`);
  const logs = await client.getLogs({
    address: rewardsContractAddress,
    event,
    fromBlock: START_BLOCK,
    toBlock
  });

  const decodedLogs = logs.map((log) => {
    const decoded = decodeEventLog({
      abi: [event],
      data: log.data,
      topics: log.topics
    });

    return {
      block_number: log.blockNumber?.toString(),
      tx_hash: log.transactionHash as Hash,
      log_index: log.logIndex,
      event_name: decoded.eventName,
      args: Object.fromEntries(
        Object.entries(decoded.args ?? {}).map(([key, value]) => [key, asString(value)])
      )
    };
  });

  const creatorMatches = decodedLogs.filter((entry) =>
    Object.values(entry.args).some((value) => value.toLowerCase() === creatorAddress.toLowerCase())
  );

  return {
    configured: true,
    rewards_contract: rewardsContractAddress,
    creator_address: creatorAddress,
    rewards_log_count: decodedLogs.length,
    creator_rewards_log_matches: creatorMatches.length,
    creator_earnings_confirmed: creatorMatches.length > 0,
    sample_creator_rewards_logs: creatorMatches.slice(-25)
  };
}

async function main() {
  assertVerifiedTarget();

  const latestBlock = await client.getBlockNumber();
  const [token, transfers, rewards] = await Promise.all([
    readTokenMetadata(),
    readTransferSurface(latestBlock),
    readRewardsSurface(latestBlock)
  ]);

  console.log(JSON.stringify({
    receipt_id: "JOY_REVENUE_READBACK_RUNTIME_V0_1",
    generated_at: new Date().toISOString(),
    target: targetReceipt(),
    latest_block: latestBlock.toString(),
    token,
    transfers,
    rewards,
    revenue_ruling: {
      market_surface_observed: true,
      token_transfer_surface_observed: transfers.transfer_log_count > 0,
      creator_earnings_confirmed: rewards.creator_earnings_confirmed === true,
      net_profit_confirmed: false,
      withdrawable_balance_confirmed: false,
      ...ZERO_KEY_RULING
    }
  }, null, 2));
}

main().catch((err) => {
  console.error(JSON.stringify({
    receipt_id: "JOY_REVENUE_READBACK_RUNTIME_V0_1",
    status: "HALTED",
    error: err instanceof Error ? err.message : String(err),
    target: targetReceipt(),
    ...ZERO_KEY_RULING
  }, null, 2));
  process.exit(1);
});
