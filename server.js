import http from "node:http";
import { spawn } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const port = Number(process.env.PORT || 3000);
const witnessDir = ".runtime/witnesses";

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

const server = http.createServer((req, res) => {
  res.setHeader("Content-Type", "text/plain; charset=utf-8");
  res.setHeader("Cache-Control", "no-store");

  if (req.url === "/health" || req.url === "/") {
    res.statusCode = 200;
    res.end("AL online\nauthority=false\n");
    return;
  }

  if (req.url === "/emit") {
    runCommand("npm", ["run", "witness:emit:gauntlet"], res);
    return;
  }

  if (req.url === "/verify") {
    const target = newestWitnessPath();
    res.write(`VERIFY_TARGET=${target}\n`);
    runCommand("npm", ["run", "witness:verify", "--", target], res);
    return;
  }

  res.statusCode = 404;
  res.end("NOT_FOUND\n");
});

server.listen(port, "0.0.0.0", () => {
  console.log(`AL listening on ${port}`);
});
