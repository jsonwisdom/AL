import { sha256HexCanonical } from "./hash.js";
import {
  DECIMAL_SCALE,
  absBigInt,
  parseFixed6DecimalToScaledBigInt,
  scaledBigIntToReceiptString,
  type DecimalString
} from "./decimal.js";

export type P0NeutralityReceiptV0 = Readonly<{
  receipt_type: "P0_NEUTRALITY_RECEIPT_V0";
  test_vector_id: string;
  policy_hash: string;
  input_hash: string;
  gate_id: "NEUTRALITY_GATE_V0";
  transform_id: "LOG_COORDINATE_T_V0";
  math_mode: "SCALED_BIGINT_DECIMAL_V0";
  decimal_scale: 6;
  values_count: number;
  sum_scaled: string;
  residual_scaled: string;
  epsilon_static_scaled: string;
  epsilon_local_scaled: "UNRESOLVED";
  epsilon_effective_scaled: string;
  epsilon_mode: "STATIC_ENFORCED_LOCAL_SHADOW";
  verdict: "ADMISSIBLE" | "REFUSE";
  reason: "NEUTRAL_MANIFOLD_PASS" | "RESIDUAL_EXCEEDS_BOUND";
}>;

export function runP0NeutralityGate(args: Readonly<{
  test_vector_id: string;
  policy_hash: string;
  input_hash: string;
  values_log_space: readonly DecimalString[];
  epsilon_static: DecimalString;
}>): P0NeutralityReceiptV0 {
  const scaledValues = args.values_log_space.map(parseFixed6DecimalToScaledBigInt);
  const sum = scaledValues.reduce((acc, value) => acc + value, 0n);
  const residual = absBigInt(sum);
  const epsilonStatic = parseFixed6DecimalToScaledBigInt(args.epsilon_static);
  const admissible = residual < epsilonStatic;

  return {
    receipt_type: "P0_NEUTRALITY_RECEIPT_V0",
    test_vector_id: args.test_vector_id,
    policy_hash: args.policy_hash,
    input_hash: args.input_hash,
    gate_id: "NEUTRALITY_GATE_V0",
    transform_id: "LOG_COORDINATE_T_V0",
    math_mode: "SCALED_BIGINT_DECIMAL_V0",
    decimal_scale: DECIMAL_SCALE,
    values_count: args.values_log_space.length,
    sum_scaled: scaledBigIntToReceiptString(sum),
    residual_scaled: scaledBigIntToReceiptString(residual),
    epsilon_static_scaled: scaledBigIntToReceiptString(epsilonStatic),
    epsilon_local_scaled: "UNRESOLVED",
    epsilon_effective_scaled: scaledBigIntToReceiptString(epsilonStatic),
    epsilon_mode: "STATIC_ENFORCED_LOCAL_SHADOW",
    verdict: admissible ? "ADMISSIBLE" : "REFUSE",
    reason: admissible ? "NEUTRAL_MANIFOLD_PASS" : "RESIDUAL_EXCEEDS_BOUND"
  };
}

export function hashP0NeutralityReceipt(receipt: P0NeutralityReceiptV0): string {
  return sha256HexCanonical(receipt);
}
