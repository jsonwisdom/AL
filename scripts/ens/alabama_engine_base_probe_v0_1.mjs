import fs from 'node:fs';
import crypto from 'node:crypto';
import { ethers } from 'ethers';

// Read-only Base 8453 observer. RPC quorum agreement is NOT a state proof.
const NAME = 'jaywisdom.base.eth';
const REGISTRY = '0xb94704422c2a1e396835a571837aa5ae53285a95';
const KEYS = ['alms.packet.cid', 'alms.packet.sha256', 'alms.matrix.hash'];
const SOURCES = [
  { id: 'base_official', url: process.env.BASE_RPC_A || 'https://mainnet.base.org' },
  { id: 'publicnode', url: process.env.BASE_RPC_B || 'https://base.publicnode.com' }
];
const registryAbi = new ethers.Interface(['function resolver(bytes32 node) view returns (address)']);
const textAbi = new ethers.Interface(['function text(bytes32 node, string key) view returns (string)']);
const OUTPUT = process.env.ALMS_PROBE_OUTPUT || 'artifacts/alabama_engine_base_probe_v0_1.json';

function canonicalSha(txt) {
  const sorted = Object.fromEntries(Object.keys(txt).sort().map(k => [k, txt[k]]));
  return crypto.createHash('sha256').update(JSON.stringify(sorted) + '\n', 'utf8').digest('hex');
}
function ensure(condition, label) {
  if (!condition) throw new Error(label);
}
async function rpc(source, method, params) {
  const response = await fetch(source.url, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ jsonrpc: '2.0', id: 1, method, params }),
    signal: AbortSignal.timeout(20000)
  });
  ensure(response.ok, 'RPC_HTTP_ERROR_' + source.id);
  const obj = await response.json();
  ensure(!obj.error && obj.result !== undefined && obj.result !== null, 'RPC_RESPONSE_ERROR_' + source.id + '_' + method);
  return obj.result;
}
function bytes32word(result) {
  ensure(/^0x[0-9a-fA-F]{64}$/.test(result), 'MALFORMED_RESOLVER_RETURN');
  return ethers.getAddress('0x' + result.slice(-40));
}
function same(a, b, key) {
  ensure(JSON.stringify(a).toLowerCase() === JSON.stringify(b).toLowerCase(), 'RPC_DIVERGENCE_' + key);
  return a;
}
function render(report) {
  fs.mkdirSync('artifacts', { recursive: true });
  fs.writeFileSync(OUTPUT, JSON.stringify(report, null, 2) + '\n');
  console.log('ALABAMA_BASE_PROBE status=' + report.status + ' block=' + (report.block_number_or_resolution_epoch ?? 'UNBOUND'));
  console.log('OUTPUT ' + OUTPUT);
}
async function main() {
  const [a, b] = SOURCES;
  ensure(a.url !== b.url, 'RPC_ENDPOINTS_NOT_DISTINCT');
  const chains = await Promise.all(SOURCES.map(src => rpc(src, 'eth_chainId', [])));
  ensure(chains.every(x => Number(BigInt(x)) === 8453), 'CHAIN_ID_MISMATCH');
  const heads = await Promise.all(SOURCES.map(src => rpc(src, 'eth_blockNumber', [])));
  const height = Math.min(...heads.map(x => Number(BigInt(x)))) - 12;
  ensure(Number.isSafeInteger(height) && height > 0, 'INVALID_COMMON_HEIGHT');
  const blockTag = '0x' + height.toString(16);
  const blocks = await Promise.all(SOURCES.map(src => rpc(src, 'eth_getBlockByNumber', [blockTag, false])));
  const blockHash = same(blocks[0].hash, blocks[1].hash, 'BLOCK_HASH');
  ensure(/^0x[0-9a-fA-F]{64}$/.test(blockHash), 'INVALID_BLOCK_HASH');
  const node = ethers.namehash(NAME);
  const call = async (source, to, data) => rpc(source, 'eth_call', [{ to, data }, blockTag]);
  const registryData = registryAbi.encodeFunctionData('resolver', [node]);
  const resolverRaw = await Promise.all(SOURCES.map(s => call(s, REGISTRY, registryData)));
  const resolver = bytes32word(same(resolverRaw[0], resolverRaw[1], 'REGISTRY_RESOLVER'));
  ensure(resolver !== ethers.ZeroAddress, 'RESOLVER_NOT_SET');
  const codes = await Promise.all(SOURCES.map(s => rpc(s, 'eth_getCode', [resolver, blockTag])));
  ensure(codes.every(code => /^0x[0-9a-fA-F]+$/.test(code) && code.length > 2), 'RESOLVER_CODE_ABSENT');
  same(codes[0], codes[1], 'RESOLVER_CODE');
  const txt = {};
  const raw = {};
  for (const key of KEYS) {
    const encoded = textAbi.encodeFunctionData('text', [node, key]);
    const values = await Promise.all(SOURCES.map(s => call(s, resolver, encoded)));
    raw[key] = same(values[0], values[1], 'TEXT_' + key);
    const decoded = textAbi.decodeFunctionResult('text', raw[key])[0];
    ensure(typeof decoded === 'string', 'INVALID_TEXT_DECODE_' + key);
    txt[key] = decoded;
  }
  const endBlocks = await Promise.all(SOURCES.map(src => rpc(src, 'eth_getBlockByNumber', [blockTag, false])));
  ensure(endBlocks.every(b => b.hash?.toLowerCase() === blockHash.toLowerCase()), 'BLOCK_REORG_DETECTED');
  const missing = KEYS.filter(k => !txt[k]);
  render({
    artifact_type: 'ALABAMA_ENGINE_RESOLVER_ARTIFACT_V0_1',
    status: missing.length ? 'RED_MISSING_TXT' : 'HOLD_RPC_AGREEMENT_NOT_CRYPTOGRAPHIC_PROOF',
    subject_name: NAME, chain_id: 8453, registry_address: REGISTRY,
    resolver_address_or_endpoint: resolver,
    observed_at_utc: new Date().toISOString(),
    block_number_or_resolution_epoch: height,
    block_hash: blockHash, node_hash: node, txt_records: txt,
    txt_records_sha256: canonicalSha(txt),
    raw_return_data: raw,
    rpc_agreement: { source_labels: SOURCES.map(s => s.id), chain_id_match: true, block_hash_match: true, registry_resolver_match: true, raw_text_match: true },
    missing_keys: missing,
    checker_output: 'RED_PROVENANCE_UNVERIFIED',
    workflow_run_id: Number(process.env.GITHUB_RUN_ID || 0),
    provenance_level: 'TWO_RPC_OBSERVATION_NOT_MERKLE_STATE_PROOF',
    no_fake_green: true
  });
  // Fail the GitHub job on any missing required TXT record; keep the artifact.
  if (missing.length) process.exitCode = 1;
}
if (process.argv.includes('--self-test')) {
  const node = ethers.namehash(NAME);
  ensure(/^0x[0-9a-f]{64}$/.test(node), 'BAD_NAMEHASH');
  const example = textAbi.encodeFunctionData('text', [node, KEYS[0]]);
  ensure(example.startsWith('0x59d1d43c'), 'BAD_TEXT_SELECTOR');
  ensure(canonicalSha({ b: '2', a: '1' }) === canonicalSha({ a: '1', b: '2' }), 'NONDETERMINISTIC_HASH');
  console.log('PASS namehash, EIP-634 text ABI, and canonical SHA-256');
} else {
  main().catch(e => {
    const status = String(e?.message || '').replace(/[^A-Za-z0-9_]/g, '_').slice(0, 120) || 'UNKNOWN_ERROR';
    render({ artifact_type: 'ALABAMA_ENGINE_RESOLVER_ARTIFACT_V0_1', status: 'RED_PROBE_FAILED', reason_code: status,
      subject_name: NAME, chain_id: 8453, no_fake_green: true, checker_output: 'RED_PROVENANCE_UNVERIFIED',
      observed_at_utc: new Date().toISOString(), workflow_run_id: Number(process.env.GITHUB_RUN_ID || 0) });
    process.exitCode = 1;
  });
}
