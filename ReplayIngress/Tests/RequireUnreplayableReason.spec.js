import { describe, expect, it } from "vitest";
import { basePacket, validateReplayIngress } from "./validator.js";

describe("ReplayIngressSpec_V1 unreplayable reason requirements", () => {
  it("requires unreplayable_reason for REPLAY_UNREPLAYABLE", () => {
    expect(
      validateReplayIngress(
        basePacket({ replay_result: "REPLAY_UNREPLAYABLE" })
      )
    ).toBe(false);
  });

  it("accepts REPLAY_UNREPLAYABLE with a safe reason", () => {
    expect(
      validateReplayIngress(
        basePacket({
          replay_result: "REPLAY_UNREPLAYABLE",
          unreplayable_reason: "required primitive unavailable"
        })
      )
    ).toBe(true);
  });

  it("does not require unreplayable_reason for REPLAY_MATCH", () => {
    expect(validateReplayIngress(basePacket())).toBe(true);
  });
});
