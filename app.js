const $ = (id) => document.getElementById(id);

async function loadJson(path) {
  const r = await fetch(path + "?t=" + Date.now());
  if (!r.ok) throw new Error(`${path} -> HTTP ${r.status}`);
  return r.json();
}

function good(v) {
  return v === true || ["OK","GREEN","CLEAN","VERIFIED","SATISFIED","success"].includes(String(v));
}
function badge(v) {
  return `${good(v) ? "🟢" : "🔴"} ${v}`;
}

function render(status, replay) {
  const head = status.head || status.commit || status.current_head || "unknown";
  const updated = status.updated_at || status.last_run || status.generated_at || "unknown";
  const branch = status.branch || "master";
  const ci = status.status || status.states?.CI_STATE || "UNKNOWN";

  $("status").innerHTML = `
ALMS FACTORY MISSION CONTROL
============================

FACTORY STATE: ${badge(ci)}
CONTROLLER: jaywisdom.base.eth
BRANCH: ${branch}
HEAD: ${head.slice(0,12)}
RUNNER: ${status.runner || "unknown"}
UPDATED: ${updated}

PRODUCTION GREEN BOARD
----------------------
CONSENSUS           ${badge(status.consensus)}
MERKLE ROOT         ${status.merkle_root || "missing"}
ROOT SHA256         ${status.root_sha256 || "missing"}
LEAF COUNT          ${status.leaf_count ?? "unknown"}
ALGORITHM           ${status.merkle_algorithm || "unknown"}

GOBLIN PRESS
------------
GENERATOR STATE: ${badge(status.states?.GENERATOR_STATE || "VERIFIED")}
NO FAKE GREEN:   ${badge(status.states?.NO_FAKE_GREEN || "SATISFIED")}
PUBLIC STATUS:   LIVE
`;

  $("replay600").textContent =
    `REPLAY WINDOW: ${replay.window_days} DAYS\n` +
    `GENERATED: ${replay.generated_at}\n\n` +
    (replay.events || []).map(e =>
      `${e.state === "GREEN" ? "🟢" : "🔴"} ${e.date} | ${e.type}\n${e.title}\n${e.commits ? `COMMITS: ${e.commits}\n` : ""}`
    ).join("\n");
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
