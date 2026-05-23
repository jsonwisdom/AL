import { describe, it, expect, beforeEach } from "vitest";
import {
  appendRaidResolution,
  readRaidChallenge,
  readRaidResolutionStream,
  writeRaidChallenge,
} from "./filesystemAnchor";
import { existsSync, readFileSync, rmSync } from "node:fs";
import { join } from "node:path";

function resetRuntime() {
  if (existsSync("runtime-data")) rmSync("runtime-data", { recursive: true, force: true });
}

describe("E06_RAID_SURFACE_V1 — edge invariants", () => {
  beforeEach(() => resetRuntime());

  it("raidId first write wins and duplicate write does not change bytes", async () => {
    const raidId = "raid-collision-test";

    const raid1 = {
      raidId,
      targetReceiptIds: ["r1"],
      challenger: "userA",
      reason: "first",
      timestamp: "2024-01-01T00:00:00.000Z",
    };

    const raid2 = {
      raidId,
      targetReceiptIds: ["r1"],
      challenger: "userB",
      reason: "second",
      timestamp: "2024-01-01T00:00:01.000Z",
    };

    const first = await writeRaidChallenge(raid1);
    expect(first.ok).toBe(true);
    expect(first.status).toBe("WRITTEN");

    const path = join("runtime-data", "raids", `${raidId}.json`);
    const beforeBytes = readFileSync(path, "utf8");

    const second = await writeRaidChallenge(raid2);
    expect(second.ok).toBe(false);
    expect(second.status).toBe("ALREADY_EXISTS");

    const afterBytes = readFileSync(path, "utf8");
    expect(afterBytes).toBe(beforeBytes);

    const loaded = await readRaidChallenge(raidId);
    expect(loaded?.challenger).toBe("userA");
    expect(loaded?.reason).toBe("first");
  });

  it("resolution stream preserves append order and replay is deterministic", async () => {
    const raidId = "raid-resolution-order";

    await writeRaidChallenge({
      raidId,
      targetReceiptIds: ["rX"],
      challenger: "user",
      reason: "order-test",
      timestamp: "2024-01-01T00:00:00.000Z",
    });

    const r1 = { raidId, status: "PENDING", resolver: "mod", decision: "Under review", timestamp: "2024-01-01T00:00:01.000Z" };
    const r2 = { raidId, status: "RESOLVED", resolver: "mod", decision: "Valid claim", timestamp: "2024-01-01T00:00:02.000Z" };
    const r3 = { raidId, status: "DISMISSED", resolver: "mod", decision: "Out of scope", timestamp: "2024-01-01T00:00:03.000Z" };

    expect((await appendRaidResolution(raidId, r1)).status).toBe("APPENDED");
    expect((await appendRaidResolution(raidId, r2)).status).toBe("APPENDED");
    expect((await appendRaidResolution(raidId, r3)).status).toBe("APPENDED");

    const stream1 = await readRaidResolutionStream(raidId);
    const stream2 = await readRaidResolutionStream(raidId);

    expect(stream1).toEqual(stream2);
    expect(stream1).toHaveLength(3);
    expect((stream1[0] as any).status).toBe("PENDING");
    expect((stream1[1] as any).status).toBe("RESOLVED");
    expect((stream1[2] as any).status).toBe("DISMISSED");
  });
});
