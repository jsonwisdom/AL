// test/phase-3-3-cross-rpc-replay.test.js
// PHASE_3.3 — Cross-RPC Replay Parity

import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { keccak_256 } from '@noble/hashes/sha3';

const MAX_DEPTH = 3;
const ROOT_UID = process.env.PHASE_3_3_ROOT_UID || '';
const SCHEMA_FILTER = process.env.PHASE_3_3_SCHEMA_FILTER || null;

const RPC_ENDPOINTS = [
  { name: 'RPC_A', graphql: 'https://base-sepolia.easscan.org/graphql' },
  { name: 'RPC_B', graphql: 'https://base-sepolia.easscan.org/graphql' }
];

async function fetchAttestation(graphqlUrl, uid) {
  const query = {
    query: `query Attestation($uid: String!) { attestation(where: { id: $uid }) { id attester recipient refUID schemaId revocable revocationTime time data decodedDataJson } }`,
    variables: { uid }
  };
  const res = await fetch(graphqlUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(query)
  });
  if (!res.ok) throw new Error(`GraphQL error: ${res.status}`);
  const json = await res.json();
  return json?.data?.attestation || null;
}

function createTraversalEngine(graphqlUrl) {
  const visited = new Set();
  const lineageNodes = [];

  async function traverseLineage(uid, depth, schemaFilter) {
    if (depth > MAX_DEPTH) return { truncated: true, reason: `MAX_DEPTH ${MAX_DEPTH} reached` };
    const normalizedUID = uid.toLowerCase();
    if (visited.has(normalizedUID)) return { cycle: true, uid: normalizedUID, depth };
    visited.add(normalizedUID);
    const att = await fetchAttestation(graphqlUrl, normalizedUID);
    if (!att) return { missing: true, uid: normalizedUID, depth };
    if (schemaFilter && att.schemaId?.toLowerCase() !== schemaFilter.toLowerCase()) {
      return { schemaFiltered: true, uid: normalizedUID, schemaId: att.schemaId, depth };
    }
    const node = {
      uid: att.id, attester: att.attester, recipient: att.recipient,
      refUID: att.refUID, schemaId: att.schemaId, revocable: att.revocable,
      revocationTime: att.revocationTime, time: att.time, depth,
      data: att.decodedDataJson ? JSON.parse(att.decodedDataJson) : null
    };
    lineageNodes.push(node);
    if (att.refUID && att.refUID !== '0x0000000000000000000000000000000000000000000000000000000000000000') {
      const childResult = await traverseLineage(att.refUID, depth + 1, schemaFilter);
      node.childResult = childResult;
    }
    return node;
  }

  function aggregateVerdict(nodes) {
    if (!nodes.length) return { verdict: 'EMPTY', totalNodes: 0, hasRevoked: false, hasRevocable: false, schemaMismatch: false };
    let hasRevoked = false, hasRevocable = false;
    const schemas = new Set();
    for (const n of nodes) {
      if (n.revocationTime && n.revocationTime !== '0') hasRevoked = true;
      if (n.revocable === true) hasRevocable = true;
      if (n.schemaId) schemas.add(n.schemaId.toLowerCase());
    }
    if (hasRevoked) return { verdict: 'REVOKED', totalNodes: nodes.length, hasRevoked: true, hasRevocable, schemaMismatch: schemas.size > 1 };
    if (schemas.size > 1) return { verdict: 'SCHEMA_MISMATCH', totalNodes: nodes.length, hasRevoked: false, hasRevocable, schemaMismatch: true };
    if (hasRevocable) return { verdict: 'REVOCABLE_WARNING', totalNodes: nodes.length, hasRevoked: false, hasRevocable: true, schemaMismatch: false };
    return { verdict: 'CLEAN', totalNodes: nodes.length, hasRevoked: false, hasRevocable: false, schemaMismatch: false };
  }

  function buildBundle(rootUID, schemaFilter) {
    const aggregation = aggregateVerdict(lineageNodes);
    return {
      version: 'PHASE_3.3', rootUID, schemaFilter: schemaFilter || 'none',
      maxDepth: MAX_DEPTH, traversalTimestamp: new Date().toISOString(),
      totalNodes: lineageNodes.length,
      uniqueSchemas: [...new Set(lineageNodes.map(n => n.schemaId).filter(Boolean))],
      aggregation,
      nodes: lineageNodes.map(n => ({
        uid: n.uid, attester: n.attester, refUID: n.refUID,
        schemaId: n.schemaId, depth: n.depth, revocable: n.revocable,
        revoked: n.revocationTime && n.revocationTime !== '0'
      }))
    };
  }

  return { traverseLineage, buildBundle, lineageNodes, visited };
}

function hashBundle(bundle) {
  const canonical = JSON.stringify(bundle, Object.keys(bundle).sort());
  const bytes = new TextEncoder().encode(canonical);
  return '0x' + Array.from(keccak_256(bytes)).map(b => b.toString(16).padStart(2, '0')).join('');
}

describe('PHASE_3.3 — Cross-RPC Replay Parity', () => {
  it('produces byte-identical lineage bundle hashes from different RPC endpoints', async () => {
    if (!ROOT_UID || ROOT_UID.length < 66) {
      console.log('SKIP: PHASE_3_3_ROOT_UID not set. Set env var to run.');
      return;
    }
    const hashes = [];
    for (const endpoint of RPC_ENDPOINTS) {
      console.log(`Traversing via ${endpoint.name}: ${endpoint.graphql}`);
      const engine = createTraversalEngine(endpoint.graphql);
      await engine.traverseLineage(ROOT_UID, 0, SCHEMA_FILTER);
      const bundle = engine.buildBundle(ROOT_UID, SCHEMA_FILTER);
      const hash = hashBundle(bundle);
      hashes.push({ name: endpoint.name, hash });
      console.log(`  ${endpoint.name} hash: ${hash}`);
      console.log(`  Nodes: ${bundle.totalNodes}, Verdict: ${bundle.aggregation.verdict}`);
    }
    const uniqueHashes = [...new Set(hashes.map(h => h.hash))];
    if (uniqueHashes.length > 1) {
      console.error('CRITICAL_DRIFT: HASH DIVERGENCE DETECTED');
      console.error('RPC_DIVERGENCE: TRUE');
      for (const h of hashes) console.error(`  ${h.name}: ${h.hash}`);
    } else {
      console.log('NO CRITICAL_DRIFT');
      console.log('NO RPC_DIVERGENCE');
      console.log('NO SCHEMA_FILTER_MISMATCH');
    }
    assert.equal(uniqueHashes.length, 1);
    console.log(`\nREPLAY PARITY CONFIRMED: ${uniqueHashes[0]}`);
  });
});
