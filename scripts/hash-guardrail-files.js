#!/usr/bin/env node

import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'fs';
import { createHash } from 'crypto';
import { dirname, resolve } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(__dirname, '..');
const rootContractRelativePath = 'specs/guardrails/source-requirements.v1.json';
const rootContractPath = resolve(repoRoot, rootContractRelativePath);
const outputRelativePath = 'checkpoints/guardrails/hash-observation.v1.json';
const outputPath = resolve(repoRoot, outputRelativePath);

function sha256File(filePath) {
  return createHash('sha256').update(readFileSync(filePath)).digest('hex');
}

function parseJsonFile(filePath) {
  return JSON.parse(readFileSync(filePath, 'utf8'));
}

function observeFile(relativePath) {
  const absolutePath = resolve(repoRoot, relativePath);

  if (!existsSync(absolutePath)) {
    return {
      path: relativePath,
      exists: false,
      parse_ok: false,
      sha256: null
    };
  }

  let parseOk = false;
  try {
    parseJsonFile(absolutePath);
    parseOk = true;
  } catch {
    parseOk = false;
  }

  return {
    path: relativePath,
    exists: true,
    parse_ok: parseOk,
    sha256: sha256File(absolutePath)
  };
}

function runHashObservation() {
  const files = [];

  if (!existsSync(rootContractPath)) {
    const checkpoint = {
      schema_id: 'AL_GUARDRAIL_HASH_OBSERVATION_V1',
      status: 'STRUCTURAL_HASH_OBSERVATION_ONLY',
      verdict: 'NEEDS_SOURCE',
      evaluation: null,
      promotion_status: 'STUB_LOCKED',
      files: [observeFile(rootContractRelativePath)],
      validation_errors: ['root_source_contract_missing'],
      ghost_anchor_risk: true
    };
    return checkpoint;
  }

  files.push(observeFile(rootContractRelativePath));

  let rootContract;
  try {
    rootContract = parseJsonFile(rootContractPath);
  } catch (error) {
    return {
      schema_id: 'AL_GUARDRAIL_HASH_OBSERVATION_V1',
      status: 'STRUCTURAL_HASH_OBSERVATION_ONLY',
      verdict: 'UNSUPPORTED',
      evaluation: null,
      promotion_status: 'STUB_LOCKED',
      files,
      validation_errors: [`root_source_contract_json_parse_failed: ${error.message}`],
      ghost_anchor_risk: false
    };
  }

  const requiredSources = rootContract.required_sources || {};

  for (const spec of Object.values(requiredSources)) {
    if (spec && spec.required === true && spec.source_path) {
      files.push(observeFile(spec.source_path));
    }
  }

  const validationErrors = files
    .filter((file) => !file.exists || !file.parse_ok)
    .map((file) => `${file.path}:${!file.exists ? 'missing' : 'json_parse_failed'}`);

  const checkpoint = {
    schema_id: 'AL_GUARDRAIL_HASH_OBSERVATION_V1',
    status: 'STRUCTURAL_HASH_OBSERVATION_ONLY',
    verdict: validationErrors.length === 0 ? 'SUPPORTED' : 'NEEDS_SOURCE',
    evaluation: null,
    promotion_status: 'STUB_LOCKED',
    files,
    validation_errors: validationErrors,
    ghost_anchor_risk: false
  };

  mkdirSync(dirname(outputPath), { recursive: true });
  writeFileSync(outputPath, `${JSON.stringify(checkpoint, null, 2)}\n`, 'utf8');

  return checkpoint;
}

console.log(JSON.stringify(runHashObservation(), null, 2));
