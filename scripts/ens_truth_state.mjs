// Fail closed until both baseline and resolution path are independently verified.
export function classifyEnsTruthState({ baselineStatus, failures, resolutionPathVerified }) {
  if (!Number.isInteger(failures) || failures < 0) return 'HOLD_INVALID_FAILURE_COUNT';
  if (failures > 0) return 'FAIL_EVIDENCE_MISMATCH';
  if (baselineStatus !== 'BASELINE_VERIFIED') return 'HOLD_BASELINE_UNVERIFIED';
  if (resolutionPathVerified !== true) return 'HOLD_RESOLUTION_PATH_UNVERIFIED';
  return 'GREEN_BYTE_MATCH';
}
