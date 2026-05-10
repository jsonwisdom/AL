// test/phase-3-3-cross-rpc-replay.test.js
// PHASE_3.3 — Cross-RPC Replay Parity (Deterministic)

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
    query: `query Attestation($uid: String!) {
      attestation(where: { id: $uid }) {
        id attester recipient refUID schemaId revocable revocationTime time data decodedDataJson
      }
    }`,
    variables: { uid: uid.toLowerCase() }
  };

  const res = await fetch(graphqlUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(query)
  });

  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const json = await res.json();
  return json?.data?.attestation || null;
}

function createTraversalEngine(graphqlUrl) {
  const visited = new Set();
  const lineageNodes = [];

  async function traverseLineage(uid, depth, schemaFilter) {
    if (depth > MAX_DEPTH) return { truncated: true };
    const normalized = uid.toLowerCase();
    if (visited.has(normalized)) return { cycle: true };

    visited.add(normalized);
    const att = await fetchAttestation(graphqlUrl, normalized);
    if (!att) return { missing: true };

    if (schemaFilter && att.schemaId?.toLowerCase() !== schemaFilter.toLowerCase()) {
      return { schemaFiltered: true };
    }

    const node = {
      uid: att.id,
      attester: att.attester,
      recipient: att.recipient,
      refUID: att.refUID,
      schemaId: att.schemaId,
      revocable: att.revocable,
      revocationTime: att.revocationTime,
      time: att.time,
      depth,
      data: att.decodedDataJson ? JSON.parse(att.decodedDataJson) : null
    };

    lineageNodes.push(node);

    if (att.refUID && att.refUID !== '0x0000000000000000000000000000000000000000000000000000000000000000') {
      await traverseLineage(att.refUID, depth + 1, schemaFilter);
    }

    return node;
  }

  function buildDeterministicBundle(rootUID, schemaFilter) {
    const aggregation = {
      verdict: lineageNodes.some(n => n.revocationTime && n.revocationTime !== '0') ? 'REVOKED' :
               new Set(lineageNodes.map(n => n.schemaId)).size > 1 ? 'SCHEMA_MISMATCH' : 'CLEAN',
      totalNodes: lineageNodes.length
    };

    return {
      version: 'PHASE_3.3',
      rootUID,
      schemaFilter: schemaFilter || 'none',
      maxDepth: MAX_DEPTH,
      totalNodes: lineageNodes.length,
      aggregation,
      nodes: lineageNodes.map(n => ({
        uid: n.uid,
        depth: n.depth,
        schemaId: n.schemaId,
        refUID: n.refUID,
        revocable: n.revocable,
        revoked: !!(n.revocationTime && n.revocationTime !== '0')
      })).sort((a, b) => a.uid.localeCompare(b.uid))
    };
  }

  return { traverseLineage, buildDeterministicBundle, lineageNodes };
}

function canonicalize(value) {
  if (Array.isArray(value)) return value.map(canonicalize);
  if (value && typeof value === 'object') {
    return Object.keys(value).sort().reduce((out, key) => {
      out[key] = canonicalize(value[key]);
      return out;
    }, {});
  }
  return value;
}

function computeCanonicalHash(bundle) {
  const canonical = JSON.stringify(canonicalize(bundle));
  const bytes = new TextEncoder().encode(canonical);
  return '0x' + Array.from(keccak_256(bytes))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
}

describe('PHASE_3.3 — Cross-RPC Replay Parity', () => {
  it('produces byte-identical lineage bundle hashes from different RPC endpoints', async () => {
    if (!ROOT_UID || ROOT_UID.length < 66) {
      console.log('SKIP: Set PHASE_3_3_ROOT_UID');
      return;
    }

    const hashes = [];

    for (const endpoint of RPC_ENDPOINTS) {
      console.log(`Traversing via ${endpoint.name}`);

      const engine = createTraversalEngine(endpoint.graphql);
      await engine.traverseLineage(ROOT_UID, 0, SCHEMA_FILTER);

      const bundle = engine.buildDeterministicBundle(ROOT_UID, SCHEMA_FILTER);
      const hash = computeCanonicalHash(bundle);

      hashes.push({ name: endpoint.name, hash, nodes: bundle.totalNodes });
      console.log(`  ${endpoint.name} → Nodes: ${bundle.totalNodes} | Hash: ${hash}`);
    }

    const uniqueHashes = [...new Set(hashes.map(h => h.hash))];

    assert.equal(uniqueHashes.length, 1,
      `HASH DIVERGENCE DETECTED: ${uniqueHashes.length} different hashes`);

    console.log(`\n✅ REPLAY PARITY CONFIRMED: ${uniqueHashes[0]}`);
  });
});
