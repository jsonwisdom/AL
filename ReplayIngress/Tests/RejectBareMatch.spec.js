import { describe, expect, it } from "vitest";
import { basePacket, validateReplayIngress } from "./validator.js";

describe("ReplayIngressSpec_V1 bare verdict rejection", () => {
  const bareVerdicts = [
    "MATCH",
    "DELTA",
    "HOLD",
    "MISMATCH",
    "DRIFT",
    "UNREPLAYABLE"
  ];

  it.each(bareVerdicts)("rejects bare replay_result %s", (bareVerdict) => {
    expect(
      validateReplayIngress(basePacket({ replay_result: bareVerdict }))
    ).toBe(false);
  });

  it.each(bareVerdicts)("rejects bare verdict string elsewhere: %s", (bareVerdict) => {
    expect(
      validateReplayIngress(basePacket({ receipt_id: bareVerdict }))
    ).toBe(false);
  });

  it("rejects bare verdict strings nested inside diff_summary", () => {
    expect(
      validateReplayIngress(
        basePacket({
          replay_result: "REPLAY_MISMATCH",
          diff_summary: { observed_state: "DRIFT" }
        })
      )
    ).toBe(false);
  });
});
