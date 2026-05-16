export interface LogEntry {
  seq: number;
  timestamp: number;
  event_type: string;
  payload_hash: string;
  prev_hash: string;  // SHA256 of previous entry's canonicalized form
}

export type RawLogEntry = Omit<LogEntry, "prev_hash">;

export interface CommitmentEnvelope {
  execution_root: string;
  agent_id: string;
  runtime_hash: string;
  timestamp: number;
  challenge_window_seconds: number;
}

export interface SignedCommitment extends CommitmentEnvelope {
  signature: string;
  public_key: string;
}
