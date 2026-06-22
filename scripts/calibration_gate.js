#!/usr/bin/env node
import { mkdirSync, writeFileSync, readFileSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';

const mode = process.argv[2];
const reportsDir = 'reports';
const receiptPath = `${reportsDir}/calibration_receipt.json`;
const matrixPath = `${reportsDir}/tier_matrix.json`;
const markdownPath = `${reportsDir}/tier_matrix.md`;

function sha256(value) {
  return createHash('sha256').update(value).digest('hex');
}

function ensureReportsDir() {
  mkdirSync(reportsDir, { recursive: true });
}

function writeJson(path, value) {
  writeFileSync(path, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

function readJson(path) {
  return JSON.parse(readFileSync(path, 'utf8'));
}

function calibrate() {
  ensureReportsDir();

  const controlSurface = {
    surface: 'control.local',
    calibration: true,
    semantic_inference: false,
    authority: false,
    expected_max_tier: 0,
    observed_findings: []
  };

  const receipt = {
    schema: 'CALIBRATION_GATE_RECEIPT_V0_1',
    status: 'CALIBRATION_CONTROL_READY',
    control_surface_hash: sha256(JSON.stringify(controlSurface)),
    max_tier: 0,
    high_tier_findings: 0,
    semantic_inference: false,
    authority: false
  };

  writeJson(receiptPath, receipt);
  console.log(`CALIBRATION_READY ${receipt.control_surface_hash}`);
}

function capture() {
  ensureReportsDir();

  if (!existsSync(receiptPath)) {
    calibrate();
  }

  const receipt = readJson(receiptPath);
  receipt.status = 'CALIBRATION_CONTROL_CAPTURED';
  receipt.capture_surface = 'control.local';
  receipt.capture_hash = sha256(JSON.stringify(receipt));
  writeJson(receiptPath, receipt);
  console.log(`CALIBRATION_CAPTURED ${receipt.capture_hash}`);
}

function aggregate() {
  ensureReportsDir();

  if (!existsSync(receiptPath)) {
    calibrate();
  }

  const receipt = readJson(receiptPath);
  const matrix = [
    {
      surface: receipt.capture_surface || 'control.local',
      max_tier: 0,
      high_tier_findings: 0,
      receipt_hash: sha256(JSON.stringify(receipt)),
      status: 'PASS'
    }
  ];

  writeJson(matrixPath, matrix);
  writeFileSync(
    markdownPath,
    `# Calibration Tier Matrix\n\n- surface: ${matrix[0].surface}\n- max_tier: ${matrix[0].max_tier}\n- high_tier_findings: ${matrix[0].high_tier_findings}\n- status: ${matrix[0].status}\n`,
    'utf8'
  );

  console.log(`CALIBRATION_AGGREGATED max_tier=${matrix[0].max_tier}`);
}

if (mode === 'calibrate') {
  calibrate();
} else if (mode === 'capture') {
  capture();
} else if (mode === 'aggregate') {
  aggregate();
} else {
  console.error('Usage: node scripts/calibration_gate.js <calibrate|capture|aggregate>');
  process.exit(2);
}
