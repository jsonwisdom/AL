import { test, expect } from '@playwright/test';

const HARNESS = 'file://' + process.cwd() + '/transport-constitution/indexeddb-smoke.test.html';

function baseReceipt() {
  return {
    sourceHash: '0x' + 'ab'.repeat(32),
    sourceContext: '0x1',
    targetContext: '0x8453',
    sourceConfidenceLevel: 1,
    targetConfidenceLevel: 2,
    translationMetadataHash: '0x' + 'cd'.repeat(32),
    attester: '0x' + '12'.repeat(20),
    attesterProof: '0xproof',
    timestamp: 1700000000000,
    translation_loss: [
      {
        classification: 'PRECISION_DOWNGRADED',
        field: 'timestamp_ms',
        source_precision: '1ms',
        target_precision: '1s',
        result: 'DEGRADED_DURING_TRANSPORT'
      }
    ]
  };
}

test.beforeEach(async ({ page }) => {
  await page.goto(HARNESS);
  await page.evaluate(async () => {
    await indexedDB.deleteDatabase('TransportConstitution');
  });
  await page.reload();
});

test('valid receipt writes', async ({ page }) => {
  const result = await page.evaluate(async (receipt) => window.__modules.writeReceipt(receipt), baseReceipt());
  expect(result.success).toBe(true);
  expect(result.rejectionCode).toBe(0);
  expect(result.receiptHash).toMatch(/^0x[0-9a-f]{64}$/);
});

test('duplicate valid receipt is idempotent', async ({ page }) => {
  const receipt = baseReceipt();
  const first = await page.evaluate(async (r) => window.__modules.writeReceipt(r), receipt);
  const second = await page.evaluate(async (r) => window.__modules.writeReceipt(r), receipt);
  const stats = await page.evaluate(async () => window.__modules.getReceiptStats());
  expect(first.success).toBe(true);
  expect(second.success).toBe(true);
  expect(first.receiptHash).toBe(second.receiptHash);
  expect(stats.total).toBe(1);
});

test('inflated confidence rejected', async ({ page }) => {
  const receipt = { ...baseReceipt(), sourceConfidenceLevel: 2, targetConfidenceLevel: 1 };
  const result = await page.evaluate(async (r) => window.__modules.writeReceipt(r), receipt);
  expect(result.success).toBe(false);
  expect(result.rejectionCode).toBe(1);
});

test('missing translation_loss rejected', async ({ page }) => {
  const receipt = baseReceipt();
  delete receipt.translation_loss;
  const result = await page.evaluate(async (r) => window.__modules.writeReceipt(r), receipt);
  expect(result.success).toBe(false);
  expect(result.rejectionCode).toBe(7);
});

test('empty translation_loss requires zero sentinel', async ({ page }) => {
  const receipt = { ...baseReceipt(), translation_loss: [] };
  const result = await page.evaluate(async (r) => window.__modules.writeReceipt(r), receipt);
  const stored = await page.evaluate(async (hash) => window.__modules.getReceipt(hash), result.receiptHash);
  expect(result.success).toBe(true);
  expect(stored.degradationLogHash).toBe(await page.evaluate(() => window.__modules.ZERO_HASH_FOR_EMPTY_DEGRADATION_LOG));
});

test('non-empty translation_loss cannot use zero sentinel', async ({ page }) => {
  const outcome = await page.evaluate(async (receipt) => {
    const { prepareReceiptForStorage, ZERO_HASH_FOR_EMPTY_DEGRADATION_LOG } = await import('./canonicalizeReceipt.js');
    const { constitutionalValidate } = await import('./indexeddb-transaction-wrapper.js');
    const prepared = await prepareReceiptForStorage(receipt);
    prepared.degradationLogHash = ZERO_HASH_FOR_EMPTY_DEGRADATION_LOG;
    return constitutionalValidate(prepared, receipt);
  }, baseReceipt());

  expect(outcome.valid).toBe(false);
  expect(outcome.rejectionCode).toBe(6);
});

test('sourceContext == targetContext rejected', async ({ page }) => {
  const receipt = { ...baseReceipt(), targetContext: '0x1' };
  const result = await page.evaluate(async (r) => window.__modules.writeReceipt(r), receipt);
  expect(result.success).toBe(false);
  expect(result.rejectionCode).toBe(5);
});

test('rejected receipt not stored when failClosed=true', async ({ page }) => {
  const receipt = { ...baseReceipt(), sourceConfidenceLevel: 2, targetConfidenceLevel: 1 };
  await page.evaluate(async (r) => window.__modules.writeReceipt(r, { failClosed: true }), receipt);
  const stats = await page.evaluate(async () => window.__modules.getReceiptStats());
  expect(stats.total).toBe(0);
});

test('rejected receipt stored only when failClosed=false', async ({ page }) => {
  const receipt = { ...baseReceipt(), sourceConfidenceLevel: 2, targetConfidenceLevel: 1 };
  await page.evaluate(async (r) => window.__modules.writeReceipt(r, { failClosed: false }), receipt);
  const stats = await page.evaluate(async () => window.__modules.getReceiptStats());
  expect(stats.total).toBe(1);
  expect(stats.rejected).toBe(1);
});

test('canonicalJSON survives readback byte-identical', async ({ page }) => {
  const result = await page.evaluate(async (receipt) => window.__modules.writeReceipt(receipt), baseReceipt());
  const stored = await page.evaluate(async (hash) => window.__modules.getReceipt(hash), result.receiptHash);
  expect(stored.canonicalJSON).toBe(result.canonicalJSON);
});
