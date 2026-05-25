export const DECIMAL_SCALE = 6 as const;
export const SCALE_FACTOR = 1_000_000n;

export type DecimalString = string;

const DECIMAL_RE = /^-?\d+\.\d{6}$/;

export function parseFixed6DecimalToScaledBigInt(value: DecimalString): bigint {
  if (!DECIMAL_RE.test(value)) {
    throw new Error("INVALID_FIXED6_DECIMAL_STRING");
  }

  const negative = value.startsWith("-");
  const unsigned = negative ? value.slice(1) : value;
  const [intPart, fracPart] = unsigned.split(".") as [string, string];

  const scaled = BigInt(intPart) * SCALE_FACTOR + BigInt(fracPart);
  return negative ? -scaled : scaled;
}

export function scaledBigIntToReceiptString(value: bigint): string {
  return value.toString();
}

export function absBigInt(value: bigint): bigint {
  return value < 0n ? -value : value;
}
