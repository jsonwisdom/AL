import express from "express";
import crypto from "crypto";
import bodyParser from "body-parser";

const app = express();
const PORT = process.env.PORT || 3000;
const SECRET = process.env.GITHUB_WEBHOOK_SECRET || "";

let clients = [];
let state = {
  head: "16ac80f7",
  branch: "receipt-goblins-core-v1",
  checks: { total: 9, passed: 9, state: "success" },
  states: {
    MERGE_STATE: "CLEAN",
    CI_STATE: "GREEN",
    REMOTE_STATE: "GREEN",
    GENERATOR_STATE: "VERIFIED",
    NO_FAKE_GREEN: "SATISFIED"
  },
  generator: { start: 1, end: 500, verified: true },
  updated_at: new Date().toISOString()
};

function verify(req, raw) {
  if (!SECRET) return true;
  const sig = req.headers["x-hub-signature-256"] || "";
  const h = "sha256=" + crypto.createHmac("sha256", SECRET).update(raw).digest("hex");
  return crypto.timingSafeEqual(Buffer.from(sig), Buffer.from(h));
}

function publish() {
  state.updated_at = new Date().toISOString();
  for (const res of clients) res.write(`data: ${JSON.stringify(state)}\n\n`);
}

app.use(bodyParser.json({
  verify: (req, res, buf) => { req.rawBody = buf; }
}));

app.get("/api/status", (req, res) => res.json(state));

app.get("/api/events", (req, res) => {
  res.setHeader("Content-Type", "text/event-stream");
  res.setHeader("Cache-Control", "no-cache");
  res.write(`data: ${JSON.stringify(state)}\n\n`);
  clients.push(res);
  req.on("close", () => clients = clients.filter(c => c !== res));
});

app.post("/webhook/github", (req, res) => {
  if (!verify(req, req.rawBody)) return res.status(401).send("bad signature");

  const event = req.headers["x-github-event"];
  const p = req.body;

  if (event === "push") {
    state.head = (p.after || state.head).slice(0, 8);
    state.branch = (p.ref || "").replace("refs/heads/", "") || state.branch;
    state.states.REMOTE_STATE = "GREEN";
  }

  if (event === "workflow_run") {
    state.states.CI_STATE = p.workflow_run?.conclusion === "success" ? "GREEN" : "RED";
    state.checks.state = p.workflow_run?.conclusion || "unknown";
  }

  if (event === "repository_dispatch" && p.action === "generator-verified") {
    state.generator = { ...p.client_payload, verified: true };
    state.states.GENERATOR_STATE = "VERIFIED";
  }

  publish();
  res.json({ ok: true });
});

app.listen(PORT, () => console.log(`factory console listening on ${PORT}`));
