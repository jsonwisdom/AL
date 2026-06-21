#!/usr/bin/env node
'use strict';

const fs = require('fs');

const BLOCKING_STATES = new Set(['DRIFT_DETECTED', 'REVIEW_PENDING', 'INVALIDATED', 'FETCH_BLOCKED']);

function loadIndex(indexPath) {
  if (!fs.existsSync(indexPath)) {
    throw new Error(`Missing librarian index: ${indexPath}`);
  }
  return JSON.parse(fs.readFileSync(indexPath, 'utf8'));
}

function getNodes(index) {
  if (Array.isArray(index.cards)) return index.cards;
  if (Array.isArray(index.registry)) return index.registry;
  return [];
}

function verifySettlementClearance(indexPath) {
  const index = loadIndex(indexPath);
  const nodes = getNodes(index);

  console.log(`[SETTLEMENT_GUARD] Executing structural audit across ${nodes.length} nodes...`);

  for (const node of nodes) {
    const state = node.state || 'UNKNOWN';
    const isGated = BLOCKING_STATES.has(state);

    if (isGated && !node.review_receipt_hash) {
      console.error('\nFATAL: Economic settlement blocked.');
      console.error(`Target: ${node.target_id || 'UNKNOWN'} is in state [${state}] with NULL review receipt.`);
      console.error('Action: payout and royalty distribution channels remain locked.');
      process.exit(1);
    }
  }

  console.log('\nPASS: All nodes verified or explicitly cleared via receipt hash. Settlement channels remain eligible.');
  process.exit(0);
}

if (require.main === module) {
  const indexPath = process.argv[2] || 'public/LIBRARIAN_INDEX.json';
  try {
    verifySettlementClearance(indexPath);
  } catch (error) {
    console.error(`FATAL: ${error.message}`);
    process.exit(1);
  }
}

module.exports = { verifySettlementClearance };
