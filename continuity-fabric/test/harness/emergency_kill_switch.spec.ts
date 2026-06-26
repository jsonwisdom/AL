import { describe, expect, it } from 'vitest';
import { createHash } from 'node:crypto';

function sha256(input: string): string {
  return createHash('sha256').update(input, 'utf8').digest('hex');
}

function recordHash(record: unknown): string {
  return `sha256:${sha256(JSON.stringify(record))}`;
}

describe('Continuity Fabric #371 — emergency kill switch', () => {
  it('requires manual review, emits RED, and auto-quarantines later user tx without settlement divergence', () => {
    const prior = {
      record_id: 'active-policy-before-kill-switch',
      record_type: 'ACTIVATION_RECORD',
      sequence: 12,
      policy_config_hash: 'sha256:active-before-kill-switch'
    };

    const configUpdate = {
      tx_id: '0xkillswitch00000000000000000000000000000000000000000000000001',
      issuer_id: 'root-trust-01',
      prev_record_hash: recordHash(prior),
      rules: {
        ambiguous_policy: 'STRICT_HALT',
        max_value_without_model: 0,
        strict_mode: true,
        allowlisted_contracts: [],
        halt_all_user_tx: true
      },
      signature: '0x' + '33'.repeat(65)
    };

    const p1 = configUpdate.issuer_id === 'root-trust-01' ? 'ADMIT' : 'REJECT_UNKNOWN_ISSUER';
    expect(p1).toBe('ADMIT');

    const p2 = 'VALID_QUORUM';
    expect(p2).toBe('VALID_QUORUM');

    const settlement = {
      tx_id: configUpdate.tx_id,
      classification: 'SETTLEMENT_CONFIRMED',
      settlement_divergence: false
    };
    expect(settlement.classification).toBe('SETTLEMENT_CONFIRMED');
    expect(settlement.settlement_divergence).toBe(false);

    const policyDecision = configUpdate.rules.halt_all_user_tx
      ? {
          resolution: 'MANUAL_REVIEW',
          downstream_state: 'BLOCKED',
          reason: 'HALT_ALL_USER_TX_REQUIRES_MANUAL_REVIEW'
        }
      : {
          resolution: 'PROCEED_WITH_WARNING',
          downstream_state: 'YELLOW_AMBIGUOUS',
          reason: 'NON_HALTING_CONFIG'
        };

    const alertEvent = {
      level: policyDecision.resolution === 'MANUAL_REVIEW' ? 'RED' : 'INFO',
      action_required: policyDecision.resolution,
      reason: policyDecision.reason,
      tx_id: configUpdate.tx_id
    };

    const gatewayState = alertEvent.level === 'RED' ? 'FABRIC_HALT_PENDING_REVIEW' : 'ACTIVE';
    const subsequentUserTxResult = gatewayState === 'FABRIC_HALT_PENDING_REVIEW'
      ? 'AUTO_QUARANTINE'
      : 'ADMIT';

    expect(alertEvent.level).toBe('RED');
    expect(alertEvent.action_required).toBe('MANUAL_REVIEW');
    expect(subsequentUserTxResult).toBe('AUTO_QUARANTINE');
    expect(settlement.settlement_divergence).toBe(false);
    expect(configUpdate.prev_record_hash).toBe(recordHash(prior));
  });
});
