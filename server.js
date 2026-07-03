import http from "node:http";
import { spawn } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const port = Number(process.env.PORT || 3000);
const witnessDir = ".runtime/witnesses";
const authorityStatePath = "runtime/state/authority_state.json";
const serviceUrl = process.env.AL_PUBLIC_URL || process.env.RENDER_EXTERNAL_URL || "https://al-dnlo.onrender.com";
const identity = process.env.AL_IDENTITY || "jaywisdom44";
const commitHash =
  process.env.RENDER_GIT_COMMIT ||
  process.env.SOURCE_VERSION ||
  process.env.GIT_COMMIT ||
  "unknown";

function runCommand(command, args, res) {
  const child = spawn(command, args, {
    cwd: process.cwd(),
    env: process.env,
    shell: false,
  });

  child.stdout.on("data", (data) => res.write(data));
  child.stderr.on("data", (data) => res.write(data));
  child.on("error", (error) => {
    res.write(`ERROR: ${error.message}\n`);
    res.end();
  });
  child.on("close", (code) => {
    res.write(`\nEXIT_CODE=${code}\n`);
    res.end();
  });
}

function newestWitnessPath() {
  const latest = path.join(witnessDir, "latest.json");
  if (fs.existsSync(latest)) return latest;

  if (!fs.existsSync(witnessDir)) return latest;

  const files = fs
    .readdirSync(witnessDir)
    .filter((file) => file.endsWith(".json"))
    .filter((file) => file !== "latest.json")
    .map((file) => path.join(witnessDir, file))
    .sort((a, b) => fs.statSync(b).mtimeMs - fs.statSync(a).mtimeMs);

  return files[0] || latest;
}

function newestWitnessUid() {
  const target = newestWitnessPath();
  const base = path.basename(target, ".json");
  return base === "latest" ? "NO_WITNESS_EMITTED" : base;
}

function readAuthorityState() {
  const fallback = { authority: false, nonce: 0 };

  try {
    if (!fs.existsSync(authorityStatePath)) return fallback;
    const parsed = JSON.parse(fs.readFileSync(authorityStatePath, "utf8"));
    return {
      authority: parsed.authority === true,
      nonce: Number.isInteger(parsed.nonce) ? parsed.nonce : 0,
    };
  } catch {
    return fallback;
  }
}

function writeText(res, body) {
  res.statusCode = 200;
  res.end(`${body}\n`);
}

function writeJson(res, body) {
  res.statusCode = 200;
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.end(`${JSON.stringify(body, null, 2)}\n`);
}

const server = http.createServer((req, res) => {
  const url = new URL(req.url || "/", serviceUrl);

  res.setHeader("Content-Type", "text/plain; charset=utf-8");
  res.setHeader("Cache-Control", "no-store");

  if (url.pathname === "/health" || url.pathname === "/") {
    res.statusCode = 200;
    res.end("AL online\nauthority=false\n");
    return;
  }

  if (url.pathname === "/emit") {
    runCommand("npm", ["run", "witness:emit:gauntlet"], res);
    return;
  }

  if (url.pathname === "/verify") {
    const target = newestWitnessPath();
    res.write(`VERIFY_TARGET=${target}\n`);
    runCommand("npm", ["run", "witness:verify", "--", target], res);
    return;
  }

  if (url.pathname === "/uid") {
    writeText(res, newestWitnessUid());
    return;
  }

  if (url.pathname === "/replay_url") {
    writeText(res, `${serviceUrl}/verify`);
    return;
  }

  if (url.pathname === "/hash") {
    writeText(res, commitHash);
    return;
  }

  if (url.pathname === "/identity") {
    writeText(res, identity);
    return;
  }

  if (url.pathname === "/governance/status" && req.method === "GET") {
    writeJson(res, {
      ...readAuthorityState(),
      authority_eligible: true,
      membrane: "AMS_v1.0_VALIDATE_ONLY",
      mutation_enabled: false,
    });
    return;
  }

  if (url.pathname === "/governance/authorize" && req.method === "POST") {
    writeJson(res, {
      stub: true,
      action: "GRANT_AUTHORITY",
      validated: false,
      mutated: false,
      authority: readAuthorityState().authority,
      reason: "EIP-712 governance proof verification deferred to later patch.",
    });
    return;
  }

  if (url.pathname === "/governance/revoke" && req.method === "POST") {
    writeJson(res, {
      stub: true,
      action: "REVOKE_AUTHORITY",
      validated: false,
      mutated: false,
      authority: readAuthorityState().authority,
      reason: "EIP-712 governance proof verification deferred to later patch.",
    });
    return;
  }

  res.statusCode = 404;
  res.end("NOT_FOUND\n");
});

server.listen(port, "0.0.0.0", () => {
  console.log(`AL listening on ${port}`);
});
