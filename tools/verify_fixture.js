#!/usr/bin/env node
const { spawnSync } = require('child_process');
const path = require('path');

function verify(receiptPath, bindingPath, policyPath) {
  const verifierPath = path.join(__dirname, 'verify_fixture.py');

  const result = spawnSync('python3', [
    verifierPath,
    receiptPath,
    bindingPath,
    policyPath
  ], {
    encoding: 'utf8'
  });

  const stdout = (result.stdout || '').trim();
  const stderr = (result.stderr || '').trim();

  if (stderr) {
    return stderr;
  }

  if (stdout) {
    return stdout;
  }

  return `FAIL: error - Python verifier exited with status ${result.status ?? 'unknown'} and no output`;
}

if (require.main === module) {
  if (process.argv.length !== 5) {
    console.error('Usage: node verify_fixture.js <receipt.json> <binding.json> <policy.json>');
    process.exit(1);
  }

  const result = verify(process.argv[2], process.argv[3], process.argv[4]);
  console.log(result);
  process.exit(result === 'PASS' ? 0 : 1);
}

module.exports = { verify };
