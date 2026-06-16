export type Hash = string;

export type DivergenceClass = "D0" | "D1" | "D2" | "D3" | "D4";

export type Verdict =
  | "MATCH"
  | "DIVERGENCE"
  | "INVALID"
  | "INSUFFICIENT_EVIDENCE"
  | "CONSTITUTIONAL_UNKNOWN"
  | "CONSTITUTIONAL_CONTRADICTION";

export interface Signature {
  observer_id: string;
  signature: string;
}

export interface Event {
  id: Hash;
  parent: Hash | null;
  payload: unknown;
  signatures: Signature[];
  timestamp: number;
}

export interface Lineage {
  genesis: Hash;
  tip: Hash;
  events: Record<Hash, Event>;
}

export interface Receipt {
  event_id: Hash | null;
  replay_path: Hash[];
  state_snapshot: Hash;
  constitution_hash: Hash;
  evidence_root: Hash;
  policy_hash: Hash;
  verdict?: Verdict;
  signatures: Signature[];
}
