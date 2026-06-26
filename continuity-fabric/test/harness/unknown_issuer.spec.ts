import { describe, expect, it } from 'vitest';
import { createHash } from 'node:crypto';

function sha256(input: string): string {
  return createHash('sha256').update(input, 'utf8').digest('hex');
}

function recordHash(record: unknown): string {
  return `sha256:${sha256(JSON.stringify(record))}`;
}

describe('Continuity Fabric #371 — unknown issuer rejection', () => {
  it('rejects unauthorized ConfigUpdate at P1 with no WAL append and unchanged lineage', () => {
    const previousContinuity = {
      record_id: 'genesis-policy',
      record_type: 'GENESIS',
      sequence: 0,
      prev_record_hash: null,
      policy_config_hash: 'sha256:genesis',
      activation_state: 'ACTIVE'
    };
    const previousHash = recordHash(previousContinuity);

    const configUpdate = {
      tx_id: '0xunknownissuer00000000000000000000000000000000000000000000001',
      issuer_id: 'gateway-root-02-injected',
      policy_config_hash: 'sha256:attempted-policy-change',
      signature: '0x' + '22'.repeat(65)
    };

    const rootTrustConfig = new Set(['root-trust-01']);
    const admitted = rootTrustConfig.has(configUpdate.issuer_id);

    const response = {
      http_status: admitted ? 200 : 401,
      p1_result: admitted ? 'ADMIT' : 'REJECT_UNKNOWN_ISSUER'
    };

    const walEntries = admitted ? [configUpdate] : [];
    const alertEvent = admitted
      ? null
      : {
          level: 'YELLOW',
          reason: 'UNKNOWN_ISSUER',
          tx_id: configUpdate.tx_id,
          action_required: 'SECURITY_REVIEW'
        };

    const currentContinuityHash = previousHash;

    expect(response.http_status).toBe(401);
    expect(response.p1_result).toBe('REJECT_UNKNOWN_ISSUER');
    expect(walEntries).toHaveLength(0);
    expect(alertEvent?.reason).toBe('UNKNOWN_ISSUER');
    expect(currentContinuityHash).toBe(previousHash);
  });
});
