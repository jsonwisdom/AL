import { readFileSync } from "node:fs";
import { glob } from "glob";

type Violation = {
  file: string;
  line: number;
  text: string;
  pattern: string;
};

const PATTERNS = [
  "private" + "Key",
  "PRIVATE" + "_" + "KEY",
  "mnemonic",
  "MNEMONIC",
  "Wallet(",
  "new Wallet",
  "Signer",
  "JsonRpcSigner",
  "sendTransaction",
  "writeContract",
  "signMessage",
  "signTypedData"
];

const ALLOWLIST = [
  "scripts/check-no-keys.ts"
];

function isAllowlisted(file: string) {
  return ALLOWLIST.some((entry) => file.endsWith(entry));
}

async function main() {
  const files = await glob(["src/**/*.ts", "scripts/**/*.ts"], {
    absolute: true,
    cwd: process.cwd()
  });

  const violations: Violation[] = [];

  for (const file of files) {
    if (isAllowlisted(file)) continue;
    const lines = readFileSync(file, "utf8").split("\n");

    lines.forEach((line, idx) => {
      for (const pattern of PATTERNS) {
        if (line.includes(pattern)) {
          violations.push({
            file,
            line: idx + 1,
            text: line.trim(),
            pattern
          });
        }
      }
    });
  }

  if (violations.length > 0) {
    console.error("Zero-key check failed: signing-related patterns detected.");
    for (const v of violations) {
      console.error(`- ${v.file}:${v.line} [${v.pattern}] :: ${v.text}`);
    }
    process.exit(1);
  }

  console.log("Zero-key check passed: no signing patterns found in checked source files.");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
