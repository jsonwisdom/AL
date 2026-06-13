import type { Address } from "viem";

export type OwnershipState = Map<Address, bigint>;

export interface TransferEvent {
  from: Address;
  to: Address;
  tokenId: bigint;
}

export interface RevenueEvent {
  payer: Address;
  recipient: Address;
  amountWei: bigint;
  txHash: `0x${string}`;
}

export function applyTransfer(state: OwnershipState, ev: TransferEvent): void {
  const zero = "0x0000000000000000000000000000000000000000" as Address;

  if (ev.from !== zero) {
    state.set(ev.from, (state.get(ev.from) ?? 0n) - 1n);
  }

  if (ev.to !== zero) {
    state.set(ev.to, (state.get(ev.to) ?? 0n) + 1n);
  }
}

export function snapshotOwnership(state: OwnershipState) {
  return [...state.entries()].map(([address, balance]) => ({
    address,
    balance: balance.toString()
  }));
}
