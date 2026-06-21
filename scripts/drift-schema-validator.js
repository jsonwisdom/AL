#!/usr/bin/env node
'use strict';

const fs = require('fs');

const SCHEMAS = {
  version: '1.0.0',
  ST_CLOUD: {
    schema_version: '1.0.0',
    fields: ['setback_standards', 'zoning_overlay'],
    impact_threshold: 'HIGH',
    keywords: ['setback', 'variance', 'zoning', 'buffer']
  },
  MANKATO: {
    schema_version: '1.0.0',
    fields: ['solar_project', 'energy_ordinance'],
    impact_threshold: 'MEDIUM',
    keywords: ['solar', 'array', 'kw', 'interconnect']
  },
  MINNEAPOLIS: {
    schema_version: '1.0.0',
    fields: ['housing_density', 'transit'],
    impact_threshold: 'CRITICAL',
    keywords: ['density', 'transit', 'corridor', 'multi-family']
  },
  DULUTH: {
    schema_version: '1.0.0',
    fields: ['port_infra', 'shipping', 'environmental'],
    impact_threshold: 'HIGH',
    keywords: ['port', 'lake', 'ore', 'maritime', 'dock']
  },
  ROCHESTER: {
    schema_version: '1.0.0',
    fields: ['medical', 'mayo_clinic', 'healthcare_zoning'],
    impact_threshold: 'MEDIUM',
    keywords: ['clinic', 'hospital', 'biotech', 'medical', 'campus']
  }
};

function readText(path) {
  return fs.readFileSync(path, 'utf8');
}

function normalizeText(value) {
  return String(value || '')
    .replace(/\r\n/g, '\n')
    .replace(/[ \t]+/g, ' ')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

function findKeywordHits(schema, original, mutated) {
  const lowerOriginal = original.toLowerCase();
  const lowerMutated = mutated.toLowerCase();
  return schema.keywords.filter((keyword) => {
    const key = keyword.toLowerCase();
    return lowerOriginal.includes(key) || lowerMutated.includes(key);
  });
}

function buildDiffSegments(original, mutated) {
  if (original === mutated) return [];

  return [
    {
      segment_type: 'normalized_text_change',
      original_excerpt: original.slice(0, 500),
      mutated_excerpt: mutated.slice(0, 500)
    }
  ];
}

function analyze(city, originalPath, mutatedPath) {
  const schema = SCHEMAS[city];
  if (!schema) {
    throw new Error(`Unknown city schema: ${city}`);
  }

  const original = normalizeText(readText(originalPath));
  const mutated = normalizeText(readText(mutatedPath));
  const diffSegments = buildDiffSegments(original, mutated);
  const keywordHits = findKeywordHits(schema, original, mutated);
  const hasDrift = diffSegments.length > 0;

  return {
    schema_version: schema.schema_version,
    validator_version: SCHEMAS.version,
    city,
    has_drift: hasDrift,
    impact_threshold: schema.impact_threshold,
    fields: schema.fields,
    keyword_hits: keywordHits,
    diff_segments: diffSegments
  };
}

if (require.main === module) {
  const [city, originalPath, mutatedPath] = process.argv.slice(2);

  if (!city || !originalPath || !mutatedPath) {
    console.error('Usage: node scripts/drift-schema-validator.js CITY ORIGINAL_FILE MUTATED_FILE');
    process.exit(1);
  }

  try {
    const result = analyze(city, originalPath, mutatedPath);
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
    process.exit(result.has_drift ? 2 : 0);
  } catch (error) {
    process.stderr.write(`FATAL: ${error.message}\n`);
    process.exit(1);
  }
}

module.exports = { SCHEMAS, analyze };
