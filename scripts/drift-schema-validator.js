#!/usr/bin/env node
'use strict';

const fs = require('fs');

const SUPPORTED_VERSIONS = ['1.0.0', '1.1.0'];

const SCHEMAS = {
  supported_versions: SUPPORTED_VERSIONS,
  version: '1.1.0',
  '1.0.0': {
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
  },
  '1.1.0': {
    ST_CLOUD: {
      schema_version: '1.1.0',
      scopes: {
        zoning_land_use: {
          fields: [
            'setback_standards',
            'zoning_overlay',
            'high_density',
            'height setback',
            'rear setback',
            'industrial adjacency setback',
            'R-5',
            'R-6',
            'Board of Adjustment variance',
            'multi-family setback'
          ],
          parameters: ['setback', 'variance', 'overlay', 'high-density', 'multifamily', 'height', 'rear', 'adjacency', 'R-5', 'R-6'],
          criticality_weight: 1.0
        },
        fiscal_appropriation: {
          fields: ['levy', 'bond', 'allocation', 'funds'],
          parameters: ['levy', 'bond', 'allocation', 'funds'],
          criticality_weight: 0.8
        }
      },
      ignore_patterns: ['\\bPage\\s+\\d+\\b', 'Minutes\\s+Approved', 'Approved\\s+Minutes', '\\bAgenda\\s+Packet\\b']
    },
    DULUTH: {
      schema_version: '1.1.0',
      scopes: {
        waterfront_port_infra: {
          fields: [
            'port_infra',
            'shipping',
            'environmental',
            'MU-W',
            'IW',
            'waterfront',
            'natural resources overlay',
            'shoreland',
            'commercial containers'
          ],
          parameters: ['port', 'lake', 'ore', 'waterfront', 'MU-W', 'IW', 'NR-O', 'shoreland', 'dock'],
          criticality_weight: 1.0
        },
        housing_density: {
          fields: ['fourplex', 'housing density', 'setback reduction'],
          parameters: ['fourplex', 'density', 'setback', 'housing'],
          criticality_weight: 0.85
        }
      },
      ignore_patterns: ['\\bPage\\s+\\d+\\b', 'Minutes\\s+Approved', 'Approved\\s+Minutes', '\\bAgenda\\s+Packet\\b']
    }
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

function applyIgnorePatterns(text, patterns = []) {
  return patterns.reduce((output, pattern) => {
    const regex = new RegExp(pattern, 'gi');
    return output.replace(regex, '');
  }, text);
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

function findKeywordHits(keywords, original, mutated) {
  const lowerOriginal = original.toLowerCase();
  const lowerMutated = mutated.toLowerCase();
  return keywords.filter((keyword) => {
    const key = String(keyword).toLowerCase();
    return lowerOriginal.includes(key) || lowerMutated.includes(key);
  });
}

function runLegacyValidator(city, schema, original, mutated) {
  const diffSegments = buildDiffSegments(original, mutated);
  const keywordHits = findKeywordHits(schema.keywords || [], original, mutated);

  return {
    schema_version: '1.0.0',
    validator_version: SCHEMAS.version,
    city,
    has_drift: diffSegments.length > 0,
    impact_threshold: schema.impact_threshold,
    fields: schema.fields || [],
    keyword_hits: keywordHits,
    diff_segments: diffSegments
  };
}

function runEvolvedValidator(city, schema, original, mutated) {
  const cleanOriginal = applyIgnorePatterns(original, schema.ignore_patterns || []);
  const cleanMutated = applyIgnorePatterns(mutated, schema.ignore_patterns || []);
  const diffSegments = buildDiffSegments(cleanOriginal, cleanMutated);
  const triggeredScopes = [];

  Object.entries(schema.scopes || {}).forEach(([scopeName, scope]) => {
    const keywordHits = findKeywordHits(scope.parameters || [], cleanOriginal, cleanMutated);
    if (keywordHits.length > 0) {
      triggeredScopes.push({
        scope: scopeName,
        criticality_weight: scope.criticality_weight,
        fields: scope.fields || [],
        keyword_hits: keywordHits
      });
    }
  });

  const maxWeight = triggeredScopes.reduce((max, scope) => Math.max(max, Number(scope.criticality_weight || 0)), 0);

  return {
    schema_version: '1.1.0',
    validator_version: SCHEMAS.version,
    city,
    has_drift: diffSegments.length > 0,
    impact_score: maxWeight,
    triggered_scopes: triggeredScopes,
    ignored_patterns: schema.ignore_patterns || [],
    drift_metadata: {
      triggered_scope_count: triggeredScopes.length,
      max_criticality_weight: maxWeight
    },
    diff_segments: diffSegments
  };
}

function validateDrift(city, targetVersion, originalText, mutatedText) {
  if (!SUPPORTED_VERSIONS.includes(targetVersion)) {
    throw new Error(`Unsupported schema version validation requested: ${targetVersion}`);
  }

  const schema = SCHEMAS[targetVersion] && SCHEMAS[targetVersion][city];
  if (!schema) {
    throw new Error(`No schema for city ${city} under version ${targetVersion}`);
  }

  const original = normalizeText(originalText);
  const mutated = normalizeText(mutatedText);

  if (targetVersion === '1.0.0') {
    return runLegacyValidator(city, schema, original, mutated);
  }

  return runEvolvedValidator(city, schema, original, mutated);
}

function readManifestVersion(city, manifestPath) {
  if (!manifestPath || !fs.existsSync(manifestPath)) return '1.0.0';
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  return manifest.schema_version || '1.0.0';
}

function analyze(city, originalPath, mutatedPath, manifestPath) {
  const targetVersion = readManifestVersion(city, manifestPath);
  return validateDrift(city, targetVersion, readText(originalPath), readText(mutatedPath));
}

if (require.main === module) {
  const [city, originalPath, mutatedPath, manifestPath] = process.argv.slice(2);

  if (!city || !originalPath || !mutatedPath) {
    console.error('Usage: node scripts/drift-schema-validator.js CITY ORIGINAL_FILE MUTATED_FILE [MANIFEST_FILE]');
    process.exit(1);
  }

  try {
    const result = analyze(city, originalPath, mutatedPath, manifestPath);
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
    process.exit(result.has_drift ? 2 : 0);
  } catch (error) {
    process.stderr.write(`FATAL: ${error.message}\n`);
    process.exit(1);
  }
}

module.exports = { SCHEMAS, validateDrift, analyze };
