import test from 'node:test';
import assert from 'node:assert/strict';
import { classifyEnsTruthState } from '../scripts/ens_truth_state.mjs';

test('11 mismatches fail regardless of baseline', () => {
  assert.equal(classifyEnsTruthState({baselineStatus:'BASELINE_VERIFIED',failures:11,resolutionPathVerified:true}), 'FAIL_EVIDENCE_MISMATCH');
});
test('draft baseline cannot produce green', () => {
  assert.equal(classifyEnsTruthState({baselineStatus:'BASELINE_DRAFT',failures:0,resolutionPathVerified:true}), 'HOLD_BASELINE_UNVERIFIED');
});
test('unverified resolution path cannot produce green', () => {
  assert.equal(classifyEnsTruthState({baselineStatus:'BASELINE_VERIFIED',failures:0,resolutionPathVerified:false}), 'HOLD_RESOLUTION_PATH_UNVERIFIED');
});
test('verified baseline and resolution with zero failures is green', () => {
  assert.equal(classifyEnsTruthState({baselineStatus:'BASELINE_VERIFIED',failures:0,resolutionPathVerified:true}), 'GREEN_BYTE_MATCH');
});
test('invalid failure count cannot produce green', () => {
  assert.equal(classifyEnsTruthState({baselineStatus:'BASELINE_VERIFIED',failures:NaN,resolutionPathVerified:true}), 'HOLD_INVALID_FAILURE_COUNT');
});
