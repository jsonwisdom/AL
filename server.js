import http from "node:http";
import { spawn } from "node:child_process";

const port = Number(process.env.PORT || 3000);

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
    runCommand("npm", ["run", "witness:verify", "--", ".runtime/witnesses/latest.json"], res);
    return;
  }

  res.statusCode = 404;
  res.end("NOT_FOUND\n");
});

server.listen(port, "0.0.0.0", () => {
  console.log(`AL listening on ${port}`);
});
