import { describe, expect, it } from "vitest";
import { basePacket, validateReplayIngress } from "./validator.js";

describe("ReplayIngressSpec_V1 diff_summary requirements", () => {
  it.each(["REPLAY_MISMATCH", "REPLAY_DRIFT"])(
    "requires diff_summary for %s",
    (replayResult) => {
      expect(
        validateReplayIngress(basePacket({ replay_result: replayResult }))
      ).toBe(false);
    }
  );

  it.each(["REPLAY_MISMATCH", "REPLAY_DRIFT"])(
    "accepts safe diff_summary for %s",
    (replayResult) => {
      expect(
        validateReplayIngress(
          basePacket({
            replay_result: replayResult,
            diff_summary: { byte_delta: 1 }
          })
        )
      ).toBe(true);
    }
  );

  it("does not require diff_summary for REPLAY_MATCH", () => {
    expect(validateReplayIngress(basePacket())).toBe(true);
  });
});
