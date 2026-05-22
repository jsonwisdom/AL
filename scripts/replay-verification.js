#!/usr/bin/env node

import { existsSync, readFileSync } from 'fs';
import { dirname, resolve } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const contractPath = resolve(__dirname, '../specs/guardrails/source-requirements.v1.json');

function loadContract() {
  if (!existsSync(contractPath)) {
    return {
      required_sources: {},
      missing_sources: ['source_contract_file_missing']
    };
  }

  const raw = readFileSync(contractPath, 'utf8');
  return JSON.parse(raw);
}

function checkMissingSources(contract) {
  const missing = [];
  const requiredSources = contract.required_sources || {};

  for (const [name, spec] of Object.entries(requiredSources)) {
    if (spec && spec.required === true && spec.status === 'MISSING') {
      missing.push(name);
    }
  }

  if (Array.isArray(contract.missing_sources)) {
    missing.push(...contract.missing_sources);
  }

  return [...new Set(missing)];
}

const contract = loadContract();
const missing = checkMissingSources(contract);

const verdict = {
  verdict: missing.length === 0 ? 'SUPPORTED' : 'NEEDS_SOURCE',
  script: 'replay-verification.js',
  checked: [
    'source_contract_file',
    'required_source_statuses'
  ],
  contract_path: contractPath,
  missing_sources: missing,
  promotion_status: 'STUB_LOCKED',
  ghost_anchor_risk: false
};

console.log(JSON.stringify(verdict, null, 2));
