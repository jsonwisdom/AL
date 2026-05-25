#!/usr/bin/env node
'use strict';

// REPLAY_SEQUENCE_VALIDATOR_V1
// Purpose: enforce sequence invariants that JSON Schema cannot fully express.
// Boundary: this validator does not verify chain transactions, wallet signatures, or EAS attestations.

function isUtcTimestamp(value) {
  return typeof value === 'string' && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$/.test(value);
}

function isBatchId(value) {
  return typeof value === 'string' && /^BATCH_\d{3}$/.test(value);
}

function expectedBatchId(sequence) {
  return `BATCH_${String(sequence).padStart(3, '0')}`;
}

const PROMO_PATTERNS = [
  /\b(lfg|moon|pump|alpha|gem|ape|buy|send it|legendary|insane|guaranteed|massive|100x)\b/i,
  /\b(i|we|our|my)\b/i,
  /[!]{2,}/
];

function hasPromotionalLanguage(text) {
  if (typeof text !== 'string') return true;
  return PROMO_PATTERNS.some((rx) => rx.test(text));
}

function validateReplaySequence(record, priorSealedByBatch = {}) {
  const errors = [];

  if (!record || typeof record !== 'object') {
    return { valid: false, errors: ['record must be an object'] };
  }

  if (!Array.isArray(record.batches)) {
    return { valid: false, errors: ['batches must be an array'] };
  }

  record.batches.forEach((batch, index) => {
    const expectedSequence = index + 1;
    const label = batch && batch.batch ? batch.batch : `index_${index}`;

    if (!batch || typeof batch !== 'object') {
      errors.push(`batch ${index} must be an object`);
      return;
    }

    if (batch.sequence !== expectedSequence) {
      errors.push(`${label}: sequence must increment by one; expected ${expectedSequence}`);
    }

    if (batch.batch !== expectedBatchId(batch.sequence)) {
      errors.push(`${label}: batch id must match sequence; expected ${expectedBatchId(batch.sequence)}`);
    }

    if (batch.next_phase !== null) {
      const expectedNext = index === record.batches.length - 1 ? null : expectedBatchId(batch.sequence + 1);
      if (batch.next_phase !== expectedNext) {
        errors.push(`${label}: next_phase mismatch; expected ${expectedNext}`);
      }
    }

    if ((batch.status === 'SEALED' || batch.status === 'FROZEN_EMPTY') && !isUtcTimestamp(batch.timestamp)) {
      errors.push(`${label}: SEALED/FROZEN_EMPTY requires RFC3339 UTC timestamp ending in Z`);
    }

    if (batch.status === 'OPEN' && batch.timestamp && !isUtcTimestamp(batch.timestamp)) {
      errors.push(`${label}: OPEN timestamp, when present, must be RFC3339 UTC ending in Z`);
    }

    if (batch.status === 'PLANNED' && batch.timestamp) {
      errors.push(`${label}: PLANNED must not have timestamp`);
    }

    if (batch.status === 'FROZEN_EMPTY' && Array.isArray(batch.items) && batch.items.length !== 0) {
      errors.push(`${label}: FROZEN_EMPTY must have zero items`);
    }

    if (batch.status === 'PLANNED' && Array.isArray(batch.items) && batch.items.length !== 0) {
      errors.push(`${label}: PLANNED must have zero items`);
    }

    if (priorSealedByBatch[batch.batch]) {
      const prior = JSON.stringify(priorSealedByBatch[batch.batch]);
      const current = JSON.stringify(batch);
      if (prior !== current) {
        errors.push(`${label}: sealed/frozen batch mutation detected`);
      }
    }

    if (Array.isArray(batch.items)) {
      batch.items.forEach((item, itemIndex) => {
        const itemLabel = `${label}.items[${itemIndex}]`;
        if (!item || typeof item !== 'object') {
          errors.push(`${itemLabel}: item must be object`);
          return;
        }
        if (!isUtcTimestamp(item.timestamp) && !/^block:\d+$/.test(item.timestamp || '') && !/^github_commit:[a-fA-F0-9]{7,40}$/.test(item.timestamp || '')) {
          errors.push(`${itemLabel}: timestamp must be UTC, block:number, or github_commit:sha`);
        }
        if (hasPromotionalLanguage(item.neutral_summary)) {
          errors.push(`${itemLabel}: neutral_summary contains first-person or promotional language`);
        }
      });
    }
  });

  return { valid: errors.length === 0, errors };
}

module.exports = { validateReplaySequence };

if (require.main === module) {
  const fs = require('fs');
  const inputPath = process.argv[2];
  if (!inputPath) {
    console.error('Usage: node validate_replay_sequence_v1.js <record.json>');
    process.exit(2);
  }
  const record = JSON.parse(fs.readFileSync(inputPath, 'utf8'));
  const result = validateReplaySequence(record);
  console.log(JSON.stringify(result, null, 2));
  process.exit(result.valid ? 0 : 1);
}
