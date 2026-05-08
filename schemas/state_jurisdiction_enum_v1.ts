export const STATE_JURISDICTION_ENUM_V1 = [
  "NOT_ESTABLISHED",
  "SUSPENDED",
  "ACTIVE_SCAFFOLD_ONLY",
  "ACTIVE_ECONOMIC_ONLY",
  "ACTIVE_SPARSE_OVERLAY_ONLY",
  "ACTIVE_FULL_STATE_WORKFLOW"
] as const;

export type StateJurisdictionEnumV1 =
  typeof STATE_JURISDICTION_ENUM_V1[number];

/**
 * Forbidden ambiguous values:
 * - ACTIVE
 * - OPERATIONAL
 * - VERIFIED
 * - COMPLETE
 * - FULLY_VERIFIED
 * - READY
 * - GREEN
 *
 * Unknown values must be rejected.
 * ACTIVE must always be tier-scoped.
 * Fail closed, never open.
 */
