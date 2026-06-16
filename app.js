const $ = (id) => document.getElementById(id);

async function loadJson(path) {
  const r = await fetch(path + "?t=" + Date.now());
  if (!r.ok) throw new Error(`${path} -> HTTP ${r.status}`);
  return r.json();
}

function isGreen(v) {
  return ["GREEN","CLEAN","VERIFIED","SATISFIED","success"].includes(String(v));
}

function badge(v) {
  return `${isGreen(v) ? "🟢" : "🔴"} ${v}`;
}

function render(status, replay) {
  const states = status.states || {};
  const head = status.head || "unknown";

  $("status").innerHTML = `
ALMS FACTORY MISSION CONTROL
============================

FACTORY STATE: ${badge(states.CI_STATE || "UNKNOWN")}
CONTROLLER: jaywisdom.base.eth
BRANCH: ${status.branch || "unknown"}
HEAD: ${head.slice(0, 12)}
EVENT: ${status.last_event || "unknown"}
UPDATED: ${status.updated_at || "unknown"}

PRODUCTION GREEN BOARD
----------------------
${Object.entries(states).map(([k,v]) => `${k.padEnd(18)} ${badge(v)}`).join("\n")}

GOBLIN PRESS
------------
GENERATOR STATE: ${badge(states.GENERATOR_STATE || "UNKNOWN")}
NO FAKE GREEN:   ${badge(states.NO_FAKE_GREEN || "UNKNOWN")}
PUBLIC STATUS:   LIVE
`;

  if ($("replay600")) {
    $("replay600").textContent =
      `REPLAY WINDOW: ${replay.window_days} DAYS\n` +
      `GENERATED: ${replay.generated_at}\n\n` +
      (replay.events || []).map(e =>
        `${e.state === "GREEN" ? "🟢" : "🔴"} ${e.date} | ${e.type}\n${e.title}\n${e.commits ? `COMMITS: ${e.commits}\n` : ""}`
      ).join("\n");
  }
}

async function main() {
  try {
    const status = await loadJson("./status.json");
    const replay = await loadJson("./factory-console/logs/last-600-days.json");
    render(status, replay);
  } catch (e) {
    $("status").textContent = "RED: " + e.message;
  }
}

main();
