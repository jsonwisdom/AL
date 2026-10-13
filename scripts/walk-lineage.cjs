const { ethers } = require('ethers');

const EAS_ADDR = '0x4200000000000000000000000000000000000021';
const LINK_SCHEMA_UID = '0x93c5ccbb6334ce3f9b56e77580c45cbeb616ad27a9f1955a65ab51b8f7e2d35e';
const RPC = process.env.LINEAGE_RPC || 'https://sepolia.base.org';
const EXPECTED_CHAIN_ID = Number(process.env.LINEAGE_CHAIN_ID || '84532');
const MAX_DEPTH = Number(process.env.LINEAGE_MAX_DEPTH || '3');

const ABI = [
  'function getAttestation(bytes32 uid) view returns (tuple(bytes32 uid,bytes32 schema,uint64 time,uint64 expirationTime,uint64 revocationTime,bytes32 refUID,address recipient,address attester,bool revocable,bytes data))'
];

const TYPES = ['bytes32','bytes32','bytes32','bytes32','address','address','string','uint64','string'];
const RELATIONS = new Set(['spawned','verified','delegated','superseded']);

async function verifyEdge(eas, uid) {
  const att = await eas.getAttestation(uid);
  if (!att.uid || att.uid === ethers.ZeroHash) {
    return { ok: false, step: { status: 'BROKEN_EDGE', reason: 'link_attestation_not_found', uid } };
  }
  if (att.schema.toLowerCase() !== LINK_SCHEMA_UID.toLowerCase()) {
    return { ok: false, step: { status: 'BROKEN_EDGE', reason: 'wrong_schema', uid, expected: LINK_SCHEMA_UID, actual: att.schema } };
  }

  const decoded = ethers.AbiCoder.defaultAbiCoder().decode(TYPES, att.data);
  const edge = {
    parentUID: decoded[0],
    encodedChildUID: decoded[1],
    childUID: uid,
    parentActionHash: decoded[2],
    childActionHash: decoded[3],
    parentSigner: decoded[4],
    childSigner: decoded[5],
    relation: decoded[6],
    timestamp: Number(decoded[7]),
    payloadRef: decoded[8]
  };

  if (!RELATIONS.has(edge.relation)) {
    return { ok: false, step: { status: 'BROKEN_EDGE', reason: 'invalid_relation', uid, edge } };
  }

  return { ok: true, parentUID: edge.parentUID, step: { status: 'EDGE_VALID', uid, edge } };
}

async function walkLineage(startUID) {
  const provider = new ethers.JsonRpcProvider(RPC);
  const network = await provider.getNetwork();
  if (Number(network.chainId) !== EXPECTED_CHAIN_ID) {
    return { status: 'CHAIN_MISMATCH', expectedChainId: EXPECTED_CHAIN_ID, actualChainId: Number(network.chainId), rpc: RPC };
  }

  const eas = new ethers.Contract(EAS_ADDR, ABI, provider);
  const seen = new Set();
  const path = [];
  let uid = startUID;

  for (let depth = 0; depth <= MAX_DEPTH; depth++) {
    const normalized = uid.toLowerCase();
    if (seen.has(normalized)) {
      path.push({ status: 'CYCLE_DETECTED', uid, break_at_depth: depth });
      return { status: 'CYCLE_DETECTED', break_at_depth: depth, path };
    }
    seen.add(normalized);

    const edge = await verifyEdge(eas, uid);
    path.push({ depth, ...edge.step });
    if (!edge.ok) return { status: 'BROKEN_EDGE', break_at_depth: depth, path };
    if (!edge.parentUID || edge.parentUID === ethers.ZeroHash) return { status: 'ROOT', depth, path };
    uid = edge.parentUID;
  }

  path.push({ status: 'MAX_DEPTH', uid, break_at_depth: MAX_DEPTH + 1 });
  return { status: 'MAX_DEPTH', break_at_depth: MAX_DEPTH + 1, path };
}

async function main() {
  const uid = process.argv[2];
  if (!uid || !/^0x[0-9a-fA-F]{64}$/.test(uid)) throw new Error('Usage: node scripts/walk-lineage.cjs <0x64-link-uid>');
  console.log(JSON.stringify(await walkLineage(uid), null, 2));
}

main().catch((err) => {
  console.error(JSON.stringify({ status: 'WALK_FAILED', error: err && err.message ? err.message : String(err) }, null, 2));
  process.exit(1);
});
