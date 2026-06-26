#!/usr/bin/env node
'use strict';

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const RPC_URL = process.env.BASE_RPC_URL;
const TX_HASH = process.env.DEEZER_TX_HASH || '0x4092721e7db7a389727e0f05a1fb2ad97caf9b6fa4a07bdcbab3a3d72ea6774b';
const EXPECTED_CHAIN_ID = Number(process.env.EXPECTED_CHAIN_ID || '8453');
const EXPECTED_RECIPIENT = (process.env.EXPECTED_RECIPIENT || '0xA380552a27b0a5a2874Ea7AA52CAC09f542002E8').toLowerCase();
const EXPECTED_AMOUNT_HUMAN = process.env.EXPECTED_AMOUNT_HUMAN || '0.00000000001';
const TOKEN_SYMBOL = process.env.TOKEN_SYMBOL || 'DEEZER';
const OUT_PATH = process.env.OUT_PATH || 'artifacts/deezer/DEEZER_MICRO_TRANSFER_VALIDATION_RESULT_V0_1.json';

function sha256(value) {
  return crypto.createHash('sha256').update(value).digest('hex');
}

function canonical(value) {
  if (Array.isArray(value)) return `[${value.map(canonical).join(',')}]`;
  if (value && typeof value === 'object') {
    return `{${Object.keys(value).sort().map(k => `${JSON.stringify(k)}:${canonical(value[k])}`).join(',')}}`;
  }
  return JSON.stringify(value);
}

async function rpc(method, params = []) {
  if (!RPC_URL) throw new Error('BASE_RPC_URL is required');
  const res = await fetch(RPC_URL, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ jsonrpc: '2.0', id: 1, method, params })
  });
  const body = await res.json();
  if (body.error) throw new Error(`${method}: ${JSON.stringify(body.error)}`);
  return body.result;
}

function hexToInt(hex) {
  if (!hex) return null;
  return Number.parseInt(hex, 16);
}

function topicAddress(topic) {
  if (!topic || topic.length !== 66) return null;
  return `0x${topic.slice(26)}`.toLowerCase();
}

function containsAddressInTopicsOrData(log, address) {
  const target = address.toLowerCase().replace(/^0x/, '');
  const topics = (log.topics || []).join('').toLowerCase();
  const data = (log.data || '').toLowerCase();
  return topics.includes(target) || data.includes(target);
}

function dataToBigInt(data) {
  try {
    if (!data || data === '0x') return null;
    return BigInt(data);
  } catch {
    return null;
  }
}

function expectedRawAmountCandidates() {
  // Candidate raw unit values for common token decimals. The validator records match/no-match
  // without assuming decimals unless an event amount equals one candidate.
  const [whole, frac = ''] = EXPECTED_AMOUNT_HUMAN.split('.');
  const candidates = [];
  for (const decimals of [18, 9, 6]) {
    const padded = (frac + '0'.repeat(decimals)).slice(0, decimals);
    const raw = BigInt(whole || '0') * (10n ** BigInt(decimals)) + BigInt(padded || '0');
    candidates.push({ decimals, raw: raw.toString() });
  }
  return candidates;
}

(async () => {
  const checkedAt = new Date().toISOString();
  let result;

  try {
    const chainHex = await rpc('eth_chainId');
    const chainId = hexToInt(chainHex);
    const receipt = await rpc('eth_getTransactionReceipt', [TX_HASH]);
    const tx = await rpc('eth_getTransactionByHash', [TX_HASH]);
    const block = receipt?.blockNumber ? await rpc('eth_getBlockByNumber', [receipt.blockNumber, false]) : null;

    const rawReceiptCanonical = canonical(receipt || null);
    const rawReceiptHash = sha256(rawReceiptCanonical);

    const logs = receipt?.logs || [];
    const recipientLogs = logs.filter(log => containsAddressInTopicsOrData(log, EXPECTED_RECIPIENT));
    const amountCandidates = expectedRawAmountCandidates();
    const candidateRawSet = new Set(amountCandidates.map(c => c.raw));
    const logsWithCandidateAmount = logs.filter(log => {
      const raw = dataToBigInt(log.data);
      return raw !== null && candidateRawSet.has(raw.toString());
    });

    const normalizedEvent = {
      tx_hash: TX_HASH,
      chain_id: chainId,
      status_hex: receipt?.status || null,
      block_number: hexToInt(receipt?.blockNumber),
      from_address: tx?.from || receipt?.from || null,
      to_address: tx?.to || receipt?.to || null,
      expected_recipient: EXPECTED_RECIPIENT,
      recipient_log_count: recipientLogs.length,
      amount_candidate_log_count: logsWithCandidateAmount.length,
      log_count: logs.length,
      token_symbol_expected: TOKEN_SYMBOL
    };

    const txStatus = receipt?.status === '0x1' ? 'success' : receipt?.status === '0x0' ? 'fail' : 'unknown';
    const chainMatch = chainId === EXPECTED_CHAIN_ID;
    const recipientMatch = recipientLogs.length > 0;
    const amountMatch = logsWithCandidateAmount.length > 0;
    const logsPresent = logs.length > 0;
    const fieldState = txStatus === 'success' && chainMatch && recipientMatch && amountMatch && logsPresent
      ? 'TOUCHDOWN_CONFIRMED_INDEPENDENT'
      : 'FLAG_ON_THE_PLAY';

    result = {
      schema_version: 'DEEZER_MICRO_TRANSFER_CI_VALIDATION_RECEIPT_V0_1',
      validator_version: 'validate_deezer_micro_transfer_v0_1.js',
      checked_at_utc: checkedAt,
      tx_hash: TX_HASH,
      chain_id: chainId,
      network: 'Base',
      tx_status: txStatus,
      block_number: hexToInt(receipt?.blockNumber),
      block_hash: receipt?.blockHash || null,
      timestamp_unix: block?.timestamp ? hexToInt(block.timestamp) : null,
      logs_present: logsPresent,
      log_count: logs.length,
      deezer_event_match: recipientMatch && amountMatch,
      token_symbol_expected: TOKEN_SYMBOL,
      token_contract_candidates: [...new Set(logs.map(l => l.address).filter(Boolean))],
      from_address: tx?.from || receipt?.from || null,
      to_address: tx?.to || receipt?.to || null,
      recipient_expected: EXPECTED_RECIPIENT,
      recipient_match: recipientMatch,
      amount_expected: `${EXPECTED_AMOUNT_HUMAN} ${TOKEN_SYMBOL}`,
      amount_observed: logsWithCandidateAmount.map(log => ({ address: log.address, data: log.data, raw: dataToBigInt(log.data)?.toString() || null })),
      amount_match: amountMatch,
      raw_receipt_hash: rawReceiptHash,
      normalized_event_hash: sha256(canonical(normalizedEvent)),
      normalized_event: normalizedEvent,
      field_state: fieldState,
      authority: false,
      no_fake_green: true
    };
  } catch (err) {
    result = {
      schema_version: 'DEEZER_MICRO_TRANSFER_CI_VALIDATION_RECEIPT_V0_1',
      validator_version: 'validate_deezer_micro_transfer_v0_1.js',
      checked_at_utc: checkedAt,
      tx_hash: TX_HASH,
      chain_id: EXPECTED_CHAIN_ID,
      tx_status: 'unknown',
      error: String(err && err.message ? err.message : err),
      field_state: 'FLAG_ON_THE_PLAY',
      authority: false,
      no_fake_green: true
    };
  }

  fs.mkdirSync(path.dirname(OUT_PATH), { recursive: true });
  fs.writeFileSync(OUT_PATH, `${JSON.stringify(result, null, 2)}\n`);
  console.log(JSON.stringify(result, null, 2));

  if (result.field_state !== 'TOUCHDOWN_CONFIRMED_INDEPENDENT') {
    process.exitCode = 1;
  }
})();
