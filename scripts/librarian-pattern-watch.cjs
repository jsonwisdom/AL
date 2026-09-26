#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const cp = require('child_process');

const ROOT = process.cwd();
const CONFIG = JSON.parse(fs.readFileSync(path.join(ROOT, 'config/librarian-pattern-watch.json'), 'utf8'));
const MODE = process.argv.includes('--mode') ? process.argv[process.argv.indexOf('--mode') + 1] : 'gate';
const OUT_DIR = path.join(ROOT, 'pattern-watch-out');
fs.mkdirSync(OUT_DIR, { recursive: true });

function readJson(p) {
  return JSON.parse(fs.readFileSync(path.join(ROOT, p), 'utf8'));
}
function sha256Text(s) {
  return crypto.createHash('sha256').update(s).digest('hex');
}
function fileText(p) {
  return fs.readFileSync(path.join(ROOT, p), 'utf8');
}
function write(name, obj) {
  fs.writeFileSync(path.join(OUT_DIR, name), JSON.stringify(obj, null, 2) + '\n');
}
function receiptFiles() {
  const dir = path.join(ROOT, 'registry/_receipts');
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir)
    .map(name => ({ name, m: name.match(/^LIBRARIAN-REPLAY-(\d+)\.json$/) }))
    .filter(x => x.m)
    .sort((a, b) => Number(a.m[1]) - Number(b.m[1]));
}
function latestReceipts() {
  const files = receiptFiles();
  if (!files.length) return { files, latest: null, previous: null };
  const latest = readJson('registry/_receipts/' + files[files.length - 1].name);
  const previous = files.length > 1
    ? readJson('registry/_receipts/' + files[files.length - 2].name)
    : null;
  return { files, latest, previous };
}
function nodeMap(receipt) {
  return new Map((receipt?.nodes || []).map(n => [n.target_id, n]));
}
function gitShow(ref, p) {
  try {
    return cp.execFileSync('git', ['show', ref + ':' + p], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] });
  } catch {
    return null;
  }
}
function currentControlHashes() {
  const out = {};
  for (const p of CONFIG.control_paths) {
    const cur = fs.existsSync(path.join(ROOT, p)) ? fileText(p) : null;
    const prev = gitShow('HEAD^', p);
    out[p] = {
      current_sha256: cur === null ? null : sha256Text(cur),
      parent_sha256: prev === null ? null : sha256Text(prev),
      changed_from_parent: cur !== prev
    };
  }
  return out;
}
function baseResult(mode) {
  return {
    pattern_watch_version: CONFIG.version,
    mode,
    timestamp: new Date().toISOString(),
    status: 'PASS',
    material: false,
    reasons: [],
    observations: {}
  };
}

function structure() {
  const r = baseResult('structure');
  const { latest } = latestReceipts();
  if (!latest) {
    r.status = 'HOLD';
    r.reasons.push('NO_LIBRARIAN_RECEIPT');
    write('structure.json', r); return r;
  }
  const requiredTop = ['receipt_id','version','timestamp','master_runtime','audit_summary','nodes','signature'];
  for (const k of requiredTop) if (!(k in latest)) r.reasons.push('MISSING_RECEIPT_FIELD:' + k);
  if (!CONFIG.known_receipt_versions.includes(latest.version)) r.reasons.push('UNKNOWN_RECEIPT_VERSION:' + latest.version);

  const nodes = Array.isArray(latest.nodes) ? latest.nodes : [];
  if (nodes.length !== CONFIG.expected_node_count) r.reasons.push('NODE_COUNT:' + nodes.length);
  if (latest.audit_summary?.node_count !== nodes.length) r.reasons.push('ROLLUP_NODE_COUNT_MISMATCH');

  const seen = new Set(nodes.map(n => n.target_id));
  for (const t of CONFIG.expected_targets) if (!seen.has(t)) r.reasons.push('MISSING_TARGET:' + t);

  for (const n of nodes) {
    const d = n?.payload?.drift_analysis;
    if (!d) { r.reasons.push('MISSING_DRIFT_ANALYSIS:' + n.target_id); continue; }
    for (const k of ['schema_version','validator_version','has_drift','diff_segments']) {
      if (!(k in d)) r.reasons.push('MISSING_NODE_FIELD:' + n.target_id + ':' + k);
    }
    if (!Array.isArray(d.diff_segments)) r.reasons.push('DIFF_SEGMENTS_NOT_ARRAY:' + n.target_id);
  }
  if (r.reasons.length) r.status = 'HOLD';
  r.observations = {
    receipt_id: latest.receipt_id,
    receipt_version: latest.version,
    node_count: nodes.length,
    audit_summary_drift_detected: latest.audit_summary?.drift_detected ?? null
  };
  write('structure.json', r); return r;
}

function semantics() {
  const r = baseResult('semantics');
  const validator = fileText('scripts/drift-schema-validator.cjs');
  const workflow = fileText('.github/workflows/librarian-replay.yml');
  const guard = fileText('scripts/production-settlement-guard.cjs');

  const validatorModule = require(path.join(ROOT, 'scripts/drift-schema-validator.cjs'));
  const behavior = {};
  try {
    const legacySame = validatorModule.validateDrift(
      'ST_CLOUD', '1.0.0',
      'Council Minutes Page 1 setback variance',
      'Council Minutes Page 1 setback variance'
    );
    behavior.legacy_same_no_drift = legacySame.has_drift === false;

    const legacyChanged = validatorModule.validateDrift(
      'ST_CLOUD', '1.0.0',
      'Council Minutes Page 1 setback variance',
      'Council Minutes Page 2 setback variance'
    );
    behavior.legacy_page_change_is_drift = legacyChanged.has_drift === true;

    const evolvedIgnored = validatorModule.validateDrift(
      'ST_CLOUD', '1.1.0',
      'Council Minutes Page 1 Minutes Approved setback variance',
      'Council Minutes Page 99 setback variance'
    );
    behavior.evolved_ignored_change_no_drift = evolvedIgnored.has_drift === false;

    const evolvedChanged = validatorModule.validateDrift(
      'ST_CLOUD', '1.1.0',
      'Council Minutes setback variance',
      'Council Minutes setback variance amended'
    );
    behavior.evolved_substantive_change_is_drift = evolvedChanged.has_drift === true;

    let unknownThrows = false;
    try {
      validatorModule.validateDrift('ST_CLOUD', '9.9.9', 'a', 'a');
    } catch (error) {
      unknownThrows = /Unsupported schema version validation requested/.test(String(error.message || error));
    }
    behavior.unknown_version_throws = unknownThrows;
  } catch (error) {
    r.status = 'HOLD';
    r.reasons.push('BEHAVIORAL_TEST_HARNESS_ERROR:' + String(error.message || error));
  }

  const checks = {
    schema_fallback_1_0_0: /manifest\.schema_version\s*\|\|\s*['"]1\.0\.0['"]/.test(validator),
    explicit_supported_version_guard: /SUPPORTED_VERSIONS\.includes\(targetVersion\)/.test(validator),
    legacy_explicit_branch: /targetVersion\s*===\s*['"]1\.0\.0['"]/.test(validator),
    explicit_1_1_0_branch: /targetVersion\s*===\s*['"]1\.1\.0['"]/.test(validator),
    unimplemented_supported_version_is_fatal: /Supported schema version .* has no implemented predicate/.test(validator),
    raw_sha_is_synthetic: /TARGET_ID:\$GITHUB_SHA:raw/.test(workflow),
    receipt_drift_is_literal_false: /drift_detected:false/.test(workflow),
    receipt_green_is_literal: /status:"GREEN"/.test(workflow),
    receipt_step_success_gated: /Generate Atomic Runtime Receipt[\s\S]*?if:\s*success\(\)/.test(workflow),
    settlement_guard_invoked_before_receipt:
      workflow.indexOf('Run Production Settlement Guard') >= 0 &&
      workflow.indexOf('Run Production Settlement Guard') < workflow.indexOf('Generate Atomic Runtime Receipt'),
    blocking_states_present: /DRIFT_DETECTED/.test(guard) && /REVIEW_PENDING/.test(guard) &&
      /INVALIDATED/.test(guard) && /FETCH_BLOCKED/.test(guard)
  };

  for (const [k, ok] of Object.entries(checks)) if (!ok) r.reasons.push('SEMANTIC_CONTRACT_CHANGED:' + k);
  for (const [k, ok] of Object.entries(behavior)) if (!ok) r.reasons.push('BEHAVIORAL_CONTRACT_CHANGED:' + k);

  const contractReasons = r.reasons.filter(x =>
    x.startsWith('SEMANTIC_CONTRACT_CHANGED:') || x.startsWith('BEHAVIORAL_CONTRACT_CHANGED:')
  );
  if (contractReasons.length && r.status !== 'HOLD') {
    r.status = 'PASS';
    r.material = true;
  }
  r.observations = { source_checks: checks, behavioral_checks: behavior };
  write('semantics.json', r); return r;
}

function history() {
  const r = baseResult('history');
  const { latest, previous, files } = latestReceipts();
  if (!latest) {
    r.status = 'HOLD'; r.reasons.push('NO_LIBRARIAN_RECEIPT');
    write('history.json', r); return r;
  }

  const changes = [];
  if (previous) {
    const a = nodeMap(previous), b = nodeMap(latest);
    const ids = [...new Set([...a.keys(), ...b.keys()])].sort();
    for (const id of ids) {
      const oldNode = a.get(id), newNode = b.get(id);
      if (!oldNode || !newNode) { changes.push({target_id:id, field:'node_presence'}); continue; }
      const oldD = oldNode.payload?.drift_analysis || {};
      const newD = newNode.payload?.drift_analysis || {};
      const compare = [
        ['schema_version', oldD.schema_version, newD.schema_version],
        ['validator_version', oldD.validator_version, newD.validator_version],
        ['has_drift', oldD.has_drift, newD.has_drift],
        ['diff_segments_count', Array.isArray(oldD.diff_segments) ? oldD.diff_segments.length : null,
                                Array.isArray(newD.diff_segments) ? newD.diff_segments.length : null],
        ['diff_segments_sha256',
          sha256Text(JSON.stringify(Array.isArray(oldD.diff_segments) ? oldD.diff_segments : null)),
          sha256Text(JSON.stringify(Array.isArray(newD.diff_segments) ? newD.diff_segments : null))]
      ];
      for (const [field, oldValue, newValue] of compare) {
        if (JSON.stringify(oldValue) !== JSON.stringify(newValue)) changes.push({target_id:id, field, oldValue, newValue});
      }
    }
  }

  for (const n of latest.nodes || []) {
    const d = n.payload?.drift_analysis || {};
    if (!CONFIG.known_schema_versions.includes(d.schema_version)) {
      changes.push({target_id:n.target_id, field:'unknown_schema_version', newValue:d.schema_version});
      r.status = 'HOLD';
    }
    if (d.has_drift === true || (Array.isArray(d.diff_segments) && d.diff_segments.length > 0)) {
      changes.push({target_id:n.target_id, field:'drift_signal', has_drift:d.has_drift, diff_segments_count:d.diff_segments?.length});
    }
  }

  const controls = currentControlHashes();
  for (const [p, h] of Object.entries(controls)) {
    if (h.changed_from_parent) changes.push({field:'control_path_changed', path:p});
  }

  r.material = changes.length > 0;
  r.reasons = changes.map(c => c.field + (c.target_id ? ':' + c.target_id : c.path ? ':' + c.path : ''));
  r.observations = {
    receipt_count: files.length,
    latest_receipt_id: latest.receipt_id,
    previous_receipt_id: previous?.receipt_id || null,
    changes,
    control_hashes: controls
  };
  write('history.json', r); return r;
}

function gate() {
  const r = baseResult('gate');
  const parts = {};
  for (const name of ['structure','semantics','history']) {
    const p = path.join(OUT_DIR, name + '.json');
    if (!fs.existsSync(p)) {
      r.status = 'HOLD'; r.reasons.push('MISSING_RUNNER_OUTPUT:' + name);
      continue;
    }
    parts[name] = JSON.parse(fs.readFileSync(p, 'utf8'));
  }
  if (Object.values(parts).some(p => p.status === 'HOLD')) r.status = 'HOLD';
  r.material = Object.values(parts).some(p => p.material === true);
  if (r.status === 'HOLD') r.classification = 'HOLD';
  else if (r.material) r.classification = 'MATERIAL_PATTERN_DELTA';
  else r.classification = 'ROUTINE_LIBRARIAN_REPLAY';

  r.reasons.push(...Object.values(parts).flatMap(p => p.reasons || []));
  r.observations = {
    runners: parts,
    boundaries: {
      audit_summary_is_runtime_metadata: true,
      audit_summary_drift_is_not_independent_proof: true,
      raw_sha256_is_synthetic_tuple: 'SHA256(target_id : github_sha : "raw")',
      raw_sha_move_is_not_document_byte_drift: true,
      historical_has_drift_is_not_rewritten: true,
      new_rules_code_input_or_execution_requires_new_result: true
    }
  };
  write('pattern_watch.json', r);

  if (r.classification === 'MATERIAL_PATTERN_DELTA') {
    const handoff = {
      schema_version: '1.0.0',
      object: 'AL_LIBRARIAN_PATTERN_WATCH',
      authority: 'JASON',
      classification: r.classification,
      reasons: [...new Set(r.reasons)],
      instructions: [
        'MASTER ROOM routes the smallest useful worker set.',
        'Ask: what would kill this claim?',
        'Producer must not self-verify.',
        'Inspect node validator outputs before audit_summary.',
        'Preserve conflicts and historical receipts.',
        'No merge, publish, payment, deletion, canon, seal, or external write without Jason authorization.'
      ],
      suggested_capabilities: [
        'GitHubBot: repository facts',
        'ProofPocket Auditor or ReceiptCheck: independent receipt verification',
        'LeahPrime: sequence and historical replay',
        'MaryDeeBot: purpose check only if purpose changed',
        'HeiDeeBot: human flow only; not machine routing'
      ],
      source_receipt: 'pattern-watch-out/pattern_watch.json'
    };
    write('grok_handoff.json', handoff);
  }

  console.log(JSON.stringify({classification:r.classification, reasons:r.reasons}, null, 2));
  if (r.status === 'HOLD') process.exitCode = 1;
  return r;
}

if (MODE === 'structure') structure();
else if (MODE === 'semantics') semantics();
else if (MODE === 'history') history();
else if (MODE === 'gate') gate();
else { console.error('Unknown mode:', MODE); process.exit(2); }
