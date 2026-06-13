import fs from 'node:fs';
import crypto from 'node:crypto';
import { ethers } from 'ethers';

const BASELINE_PATH = process.env.ENS_TXT_BASELINE || 'projects/zora-jay-agent/config/ens_txt_byte_baseline_v0_1.json';
const REPORT_PATH = process.env.ENS_TXT_REPORT || 'artifacts/ens_txt_byte_check_report.json';
const ETH_RPC_URL = process.env.ETH_RPC_URL || 'https://ethereum.publicnode.com';
const BASE_RPC_URL = process.env.BASE_RPC_URL || 'https://base.publicnode.com';

function sha256Utf8(value) {
  return crypto.createHash('sha256').update(Buffer.from(value, 'utf8')).digest('hex');
}

function utf8Hex(value) {
  return `0x${Buffer.from(value, 'utf8').toString('hex')}`;
}

function byteLength(value) {
  return Buffer.byteLength(value, 'utf8');
}

function readBaseline() {
  if (!fs.existsSync(BASELINE_PATH)) {
    throw new Error(`Missing baseline file: ${BASELINE_PATH}`);
  }
  return JSON.parse(fs.readFileSync(BASELINE_PATH, 'utf8'));
}

async function getOptionalBlockNumber(rpcUrl) {
  try {
    const provider = new ethers.JsonRpcProvider(rpcUrl);
    return await provider.getBlockNumber();
  } catch (error) {
    return { error: String(error?.message || error) };
  }
}

async function readTextRecord(provider, name, keyCandidates) {
  const resolver = await provider.getResolver(name);
  if (!resolver) {
    return {
      found: false,
      status: 'RESOLVER_MISSING',
      error: `No resolver returned for ${name}`
    };
  }

  const attempts = [];
  for (const key of keyCandidates) {
    try {
      const value = await resolver.getText(key);
      attempts.push({ key, value_present: Boolean(value), value_length: value ? byteLength(value) : 0 });
      if (value && value.length > 0) {
        return {
          found: true,
          found_key: key,
          value,
          attempts
        };
      }
    } catch (error) {
      attempts.push({ key, error: String(error?.message || error) });
    }
  }

  return {
    found: false,
    status: 'MISSING_RECORD',
    attempts
  };
}

function evaluateBytes({ name, role, record, read }) {
  const expected = record.expected_utf8;
  const required = record.required !== false;

  if (!read.found) {
    return {
      name,
      role,
      canonical_key: record.canonical_key,
      key_candidates: record.key_candidates,
      required,
      status: read.status || 'READ_FAILED',
      no_fake_green: true,
      error: read.error || null,
      attempts: read.attempts || []
    };
  }

  const actual = read.value;
  const expectedBytes = utf8Hex(expected);
  const actualBytes = utf8Hex(actual);
  const exactMatch = expectedBytes === actualBytes;

  return {
    name,
    role,
    canonical_key: record.canonical_key,
    found_key: read.found_key,
    required,
    status: exactMatch ? 'OK_BYTE_MATCH' : 'BYTE_MISMATCH',
    no_fake_green: true,
    expected_utf8: expected,
    actual_utf8: actual,
    expected_sha256: sha256Utf8(expected),
    actual_sha256: sha256Utf8(actual),
    expected_byte_length: byteLength(expected),
    actual_byte_length: byteLength(actual),
    expected_bytes_hex: expectedBytes,
    actual_bytes_hex: actualBytes,
    attempts: read.attempts || []
  };
}

async function main() {
  const baseline = readBaseline();
  const provider = new ethers.JsonRpcProvider(ETH_RPC_URL);
  const ethBlock = await provider.getBlockNumber();
  const baseBlock = await getOptionalBlockNumber(BASE_RPC_URL);

  const results = [];

  for (const nameConfig of baseline.names || []) {
    for (const record of nameConfig.text_records || []) {
      const read = await readTextRecord(provider, nameConfig.name, record.key_candidates || [record.canonical_key]);
      results.push(evaluateBytes({
        name: nameConfig.name,
        role: nameConfig.role,
        record,
        read
      }));
    }
  }

  const failures = results.filter((result) => result.required && result.status !== 'OK_BYTE_MATCH');
  const report = {
    generated_at: new Date().toISOString(),
    checker: 'ENS_TXT_BYTE_CHECKER_V0_1',
    baseline_path: BASELINE_PATH,
    eth_block_number: ethBlock,
    base_block_number_observed: baseBlock,
    truth_state: failures.length === 0 ? 'GREEN_BYTE_MATCH' : 'RED_OR_YELLOW_CHECK_FAILED',
    no_fake_green: true,
    failure_count: failures.length,
    results
  };

  fs.mkdirSync(REPORT_PATH.split('/').slice(0, -1).join('/'), { recursive: true });
  fs.writeFileSync(REPORT_PATH, `${JSON.stringify(report, null, 2)}\n`);

  const lines = [
    '# ENS TXT Byte Check',
    '',
    `Generated: ${report.generated_at}`,
    `Truth state: ${report.truth_state}`,
    `NO_FAKE_GREEN: ${report.no_fake_green}`,
    `Failure count: ${report.failure_count}`,
    '',
    '| Name | Role | Key | Found Key | Status | Expected SHA256 | Actual SHA256 |',
    '| --- | --- | --- | --- | --- | --- | --- |'
  ];

  for (const result of results) {
    lines.push(`| ${result.name} | ${result.role} | ${result.canonical_key} | ${result.found_key || ''} | ${result.status} | ${result.expected_sha256 || ''} | ${result.actual_sha256 || ''} |`);
  }

  const summary = `${lines.join('\n')}\n`;
  console.log(summary);

  if (process.env.GITHUB_STEP_SUMMARY) {
    fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY, summary);
  }

  if (failures.length > 0) {
    console.error('ENS TXT byte checker failed. This is intentional NO_FAKE_GREEN behavior. See report artifact.');
    process.exit(1);
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
