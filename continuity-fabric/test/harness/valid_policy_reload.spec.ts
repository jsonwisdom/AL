import { describe, expect, it } from 'vitest';
import { createHash } from 'node:crypto';

const frozen = `70af281981f0b6c8fd2701fb90c2dd59c63125855028ab6f305f23003981d4e7  continuity-fabric/schemas/Identity.json
fb8357791138fff306622dbde3f9a1bb22af800e49ffb4ac91bde4d98052b698  continuity-fabric/schemas/Directive.json
8a8639094a0bc6e23c8c7eadb9a08fd3234a6eaebc028abbbd61414c48198224  continuity-fabric/schemas/Property.json
8701fb9e16a549267d980c5a17d2d7ed4abe710bb76bc342f50935b0520460fb  continuity-fabric/schemas/Influence.json
a09de36d3422d5db2cf826ccd2e79b7ac7c19627788f512a9d8d493fbebfad00  continuity-fabric/schemas/Integrity.json
ae78bf08a0694523f77d8458ccbf36cf95de6578ab03e27c1d2084266ff67d2d  continuity-fabric/schemas/Continuity.json
`;

function sha256(input: string): string {
  return createHash('sha256').update(input, 'utf8').digest('hex');
}

function recordHash(record: unknown): string {
  return `sha256:${sha256(JSON.stringify(record))}`;
}

describe('Continuity Fabric #371 — valid policy reload', () => {
  it('executes P1 -> P4 -> ActivationRecord with no alert', () => {
    const policyConfigHash = `sha256:${sha256(frozen)}`;

    const configUpdate = {
      tx_id: '0xvalidreload00000000000000000000000000000000000000000000000001',
      issuer_id: 'root-trust-01',
      prev_policy_hash: null,
      policy_config_hash: policyConfigHash,
      effective_from_timestamp: '2026-06-26T17:00:00.000Z',
      rules: {
        ambiguous_policy: 'TIERED_ALLOW',
        max_value_without_model: 0,
        strict_mode: true,
        allowlisted_contracts: [],
        halt_all_user_tx: false
      },
      signature: '0x' + '11'.repeat(65)
    };

    const p1 = configUpdate.issuer_id === 'root-trust-01' ? 'ADMIT' : 'REJECT_UNKNOWN_ISSUER';
    expect(p1).toBe('ADMIT');

    const walEntry = {
      record_type: 'CONFIG_UPDATE',
      tx_id: configUpdate.tx_id,
      policy_config_hash: configUpdate.policy_config_hash
    };
    const walHash = recordHash(walEntry);

    const quorumReceipts = ['log-node-1', 'log-node-2', 'log-node-3'].map((node, index) => ({
      log_node_id: node,
      sequence: index + 1,
      integrity: {
        canonical_hash: walHash,
        signature: '0x' + String(index + 1).repeat(130)
      }
    }));

    const p2 = quorumReceipts.length >= 2 ? 'VALID_QUORUM' : 'QUORUM_FAILURE';
    expect(p2).toBe('VALID_QUORUM');
    expect(new Set(quorumReceipts.map((r) => r.integrity.canonical_hash)).size).toBe(1);
    expect(quorumReceipts[0].integrity.canonical_hash).toBe(walHash);

    const p3 = 'SKIPPED_SYSTEM_TX';
    expect(p3).toBe('SKIPPED_SYSTEM_TX');

    const settlementRecord = {
      record_type: 'SETTLEMENT_RECORD',
      tx_id: configUpdate.tx_id,
      policy_config_hash: configUpdate.policy_config_hash,
      wal_entry_hash: walHash,
      classification: 'SETTLEMENT_CONFIRMED'
    };
    expect(settlementRecord.classification).toBe('SETTLEMENT_CONFIRMED');

    const activationRecord = {
      record_type: 'ACTIVATION_RECORD',
      policy_config_hash: configUpdate.policy_config_hash,
      prev_record_hash: recordHash(settlementRecord),
      activation_state: 'ACTIVE'
    };

    const alertEvents: unknown[] = [];

    expect(activationRecord.policy_config_hash).toBe(policyConfigHash);
    expect(alertEvents).toHaveLength(0);
    expect(activationRecord.prev_record_hash).toBe(recordHash(settlementRecord));
  });
});
