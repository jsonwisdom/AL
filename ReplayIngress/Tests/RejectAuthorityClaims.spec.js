import { describe, expect, it } from "vitest";
import { basePacket, validateReplayIngress } from "./validator.js";

describe("ReplayIngressSpec_V1 authority and inference rejection", () => {
  const forbiddenProperties = [
    "al_match",
    "al_delta",
    "al_hold",
    "authorized",
    "accepted",
    "correct",
    "truth",
    "verified",
    "valid",
    "actor",
    "identity",
    "signer",
    "wallet",
    "settled",
    "final",
    "approved"
  ];

  it.each(forbiddenProperties)("rejects forbidden top-level property %s", (property) => {
    expect(
      validateReplayIngress(basePacket({ [property]: true }))
    ).toBe(false);
  });

  it.each(forbiddenProperties)("rejects forbidden nested diff property %s", (property) => {
    expect(
      validateReplayIngress(
        basePacket({
          replay_result: "REPLAY_MISMATCH",
          diff_summary: { [property]: true }
        })
      )
    ).toBe(false);
  });

  it.each([
    "authority_created",
    "acceptance_created",
    "correctness_proved"
  ])("requires %s to remain false", (property) => {
    expect(
      validateReplayIngress(basePacket({ [property]: true }))
    ).toBe(false);
  });
});
