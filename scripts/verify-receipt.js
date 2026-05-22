#!/usr/bin/env node

import { existsSync, readFileSync } from 'fs';
import { dirname, resolve } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(__dirname, '..');
const rootContractRelativePath = 'specs/guardrails/source-requirements.v1.json';
const rootContractPath = resolve(repoRoot, rootContractRelativePath);

function parseJsonFile(filePath) {
  return JSON.parse(readFileSync(filePath, 'utf8'));
}

function auditRuntimeContracts() {
  const checkedContractPaths = [rootContractRelativePath];
  const validationErrors = [];
  const missingSources = [];

  if (!existsSync(rootContractPath)) {
    return {
      verdict: 'NEEDS_SOURCE',
      script: 'verify-receipt.js',
      checked_contract_paths: checkedContractPaths,
      missing_sources: ['root_source_contract_missing'],
      validation_errors: ['root_source_contract_missing'],
      promotion_status: 'STUB_LOCKED',
      ghost_anchor_risk: false
    };
  }

  let rootContract;
  try {
    rootContract = parseJsonFile(rootContractPath);
  } catch (error) {
    return {
      verdict: 'UNSUPPORTED',
      script: 'verify-receipt.js',
      checked_contract_paths: checkedContractPaths,
      missing_sources: [],
      validation_errors: [`root_source_contract_json_parse_failed: ${error.message}`],
      promotion_status: 'STUB_LOCKED',
      ghost_anchor_risk: false
    };
  }

  const requiredSources = rootContract.required_sources || {};

  for (const [sourceName, spec] of Object.entries(requiredSources)) {
    if (!spec || spec.required !== true) {
      continue;
    }

    if (spec.status !== 'PRESENT') {
      missingSources.push(sourceName);
      validationErrors.push(`${sourceName}_status_not_present`);
      continue;
    }

    if (!spec.source_path) {
      missingSources.push(sourceName);
      validationErrors.push(`${sourceName}_source_path_undefined`);
      continue;
    }

    checkedContractPaths.push(spec.source_path);
    const absolutePath = resolve(repoRoot, spec.source_path);

    if (!existsSync(absolutePath)) {
      missingSources.push(sourceName);
      validationErrors.push(`${sourceName}_file_missing_on_disk`);
      continue;
    }

    try {
      parseJsonFile(absolutePath);
    } catch (error) {
      validationErrors.push(`${sourceName}_json_parse_failed: ${error.message}`);
    }
  }

  return {
    verdict: validationErrors.length === 0 ? 'SUPPORTED' : 'NEEDS_SOURCE',
    script: 'verify-receipt.js',
    checked_contract_paths: checkedContractPaths,
    missing_sources: [...new Set(missingSources)],
    validation_errors: validationErrors,
    promotion_status: 'STUB_LOCKED',
    ghost_anchor_risk: false
  };
}

console.log(JSON.stringify(auditRuntimeContracts(), null, 2));
