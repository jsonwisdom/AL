#!/usr/bin/env bash
set -euo pipefail

# ALMS age-verification-aware PDF ingest.
# Usage: scripts/fetch_age_verified_pdf.sh <URL> <source_id>
# Stage: INGEST_ONLY_QUARANTINED
# This script only clicks a visible age-confirmation/continue control.
# It does not bypass access controls, rotate identity, promote artifacts,
# or create WRITE_RUN_0002_packet.json.

URL="${1:-}"
SOURCE_ID="${2:-age_verified_pdf}"

if [ -z "$URL" ]; then
  echo "Usage: $0 <URL> <source_id>"
  exit 1
fi

OUT_DIR="_truth/ingest/${SOURCE_ID}"
PROFILE_DIR="_truth/browser_profiles/${SOURCE_ID}"
TS="$(date -u +%Y-%m-%dT%H-%M-%SZ)"
mkdir -p "$OUT_DIR" "$PROFILE_DIR"

PDF_FILE="$OUT_DIR/${TS}.pdf"
HTML_FILE="$OUT_DIR/${TS}.landing.html"
TEXT_FILE="$OUT_DIR/${TS}.landing.txt"
SCREENSHOT_FILE="$OUT_DIR/${TS}.png"
COOKIES_FILE="$OUT_DIR/${TS}.cookies.json"
META_FILE="$OUT_DIR/${TS}.meta.json"
HASH_FILE="$OUT_DIR/${TS}.sha256"
PW_SCRIPT="$OUT_DIR/${TS}.age_pdf_fetch.cjs"
RESULT_FILE="$OUT_DIR/${TS}.playwright.result.json"

cat > "$PW_SCRIPT" <<'NODE'
const fs = require('fs');
const { chromium } = require('playwright');

(async () => {
  const url = process.env.ALMS_URL;
  const pdfFile = process.env.ALMS_PDF_FILE;
  const htmlFile = process.env.ALMS_HTML_FILE;
  const textFile = process.env.ALMS_TEXT_FILE;
  const screenshotFile = process.env.ALMS_SCREENSHOT_FILE;
  const cookiesFile = process.env.ALMS_COOKIES_FILE;
  const profileDir = process.env.ALMS_PROFILE_DIR;

  const browser = await chromium.launchPersistentContext(profileDir, {
    headless: true,
    viewport: { width: 1365, height: 900 },
    userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36',
    javaScriptEnabled: true,
    acceptDownloads: true
  });

  const page = await browser.newPage();
  let pdfResponse = null;
  let downloadPath = null;
  let ageGateDetected = false;
  let ageGateClicked = false;
  let responseStatus = null;
  let responseUrl = null;

  try {
    page.on('response', async (response) => {
      const ct = (response.headers()['content-type'] || '').toLowerCase();
      if (!pdfResponse && ct.includes('application/pdf')) {
        pdfResponse = response;
        try {
          const body = await response.body();
          fs.writeFileSync(pdfFile, body);
        } catch (_) {}
      }
    });

    const response = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 90000 });
    if (response) {
      responseStatus = response.status();
      responseUrl = response.url();
    }
    await page.waitForLoadState('networkidle', { timeout: 30000 }).catch(() => {});

    const html1 = await page.content();
    const text1 = await page.locator('body').innerText({ timeout: 10000 }).catch(() => '');
    ageGateDetected = /18 years|18\+|age verification|confirm age|older to access|I am 18|Yes, I am|Continue/i.test(html1 + '\n' + text1);

    if (ageGateDetected) {
      const candidates = [
        page.getByRole('button', { name: /18|agree|confirm|continue|enter|yes/i }),
        page.getByRole('link', { name: /18|agree|confirm|continue|enter|yes/i }),
        page.locator('button:has-text("Continue"), button:has-text("Yes"), button:has-text("I am"), a:has-text("Continue"), a:has-text("Yes"), input[type="submit"]')
      ];
      for (const locator of candidates) {
        try {
          if (await locator.first().isVisible({ timeout: 3000 })) {
            const downloadPromise = page.waitForEvent('download', { timeout: 15000 }).catch(() => null);
            await locator.first().click({ timeout: 10000 });
            ageGateClicked = true;
            const download = await downloadPromise;
            if (download) {
              downloadPath = await download.path();
              if (downloadPath) fs.copyFileSync(downloadPath, pdfFile);
            }
            break;
          }
        } catch (_) {}
      }
      await page.waitForLoadState('networkidle', { timeout: 30000 }).catch(() => {});
      await page.waitForTimeout(3000);
    }

    const html2 = await page.content();
    const text2 = await page.locator('body').innerText({ timeout: 10000 }).catch(() => '');
    fs.writeFileSync(htmlFile, html2, 'utf8');
    fs.writeFileSync(textFile, text2, 'utf8');
    fs.writeFileSync(cookiesFile, JSON.stringify(await browser.cookies(), null, 2) + '\n', 'utf8');
    await page.screenshot({ path: screenshotFile, fullPage: true }).catch(() => {});

    const pdfExists = fs.existsSync(pdfFile);
    console.log(JSON.stringify({
      ok: true,
      url,
      final_url: page.url(),
      response_status: responseStatus,
      response_url: responseUrl,
      title: await page.title().catch(() => null),
      age_gate_detected: ageGateDetected,
      age_gate_clicked: ageGateClicked,
      pdf_captured: pdfExists,
      pdf_response_url: pdfResponse ? pdfResponse.url() : null,
      pdf_response_status: pdfResponse ? pdfResponse.status() : null,
      completed_at_utc: new Date().toISOString()
    }));
  } catch (err) {
    console.log(JSON.stringify({
      ok: false,
      url,
      final_url: page.url ? page.url() : null,
      response_status: responseStatus,
      response_url: responseUrl,
      age_gate_detected: ageGateDetected,
      age_gate_clicked: ageGateClicked,
      pdf_captured: fs.existsSync(pdfFile),
      error: String(err && err.message ? err.message : err),
      completed_at_utc: new Date().toISOString()
    }));
    process.exitCode = 2;
  } finally {
    await browser.close();
  }
})();
NODE

if ! command -v node >/dev/null 2>&1; then
  echo "NODE_MISSING"
  exit 1
fi

if [ ! -d node_modules/playwright ]; then
  echo "PLAYWRIGHT_MISSING"
  echo "Run: npm install playwright && npx playwright install chromium"
  exit 1
fi

set +e
ALMS_URL="$URL" \
ALMS_PDF_FILE="$PDF_FILE" \
ALMS_HTML_FILE="$HTML_FILE" \
ALMS_TEXT_FILE="$TEXT_FILE" \
ALMS_SCREENSHOT_FILE="$SCREENSHOT_FILE" \
ALMS_COOKIES_FILE="$COOKIES_FILE" \
ALMS_PROFILE_DIR="$PROFILE_DIR" \
node "$PW_SCRIPT" > "$RESULT_FILE"
NODE_STATUS=$?
set -e

RESULT_JSON=$(cat "$RESULT_FILE")
FINAL_URL=$(printf '%s' "$RESULT_JSON" | jq -r '.final_url // empty')
HTTP_STATUS=$(printf '%s' "$RESULT_JSON" | jq -r '.response_status // empty')
AGE_GATE_DETECTED=$(printf '%s' "$RESULT_JSON" | jq -r '.age_gate_detected // false')
AGE_GATE_CLICKED=$(printf '%s' "$RESULT_JSON" | jq -r '.age_gate_clicked // false')
PDF_CAPTURED=$(printf '%s' "$RESULT_JSON" | jq -r '.pdf_captured // false')

HTML_SHA256=$(sha256sum "$HTML_FILE" | awk '{print $1}')
HTML_SIZE_BYTES=$(wc -c < "$HTML_FILE" | tr -d ' ')
TEXT_SHA256=$(sha256sum "$TEXT_FILE" | awk '{print $1}')
TEXT_SIZE_BYTES=$(wc -c < "$TEXT_FILE" | tr -d ' ')

PDF_SHA256=""
PDF_SIZE_BYTES=0
if [ -f "$PDF_FILE" ]; then
  PDF_SHA256=$(sha256sum "$PDF_FILE" | awk '{print $1}')
  PDF_SIZE_BYTES=$(wc -c < "$PDF_FILE" | tr -d ' ')
fi

{
  echo "$HTML_SHA256  $(basename "$HTML_FILE")"
  echo "$TEXT_SHA256  $(basename "$TEXT_FILE")"
  if [ -f "$PDF_FILE" ]; then echo "$PDF_SHA256  $(basename "$PDF_FILE")"; fi
} > "$HASH_FILE"

cat > "$META_FILE" <<JSON
{
  "source": "$SOURCE_ID",
  "url": "$URL",
  "final_url": "$FINAL_URL",
  "http_status": "$HTTP_STATUS",
  "fetched_at_utc": "${TS}",
  "render_method": "playwright_chromium_persistent_context_age_gate_click",
  "profile_dir": "$PROFILE_DIR",
  "age_gate_detected": ${AGE_GATE_DETECTED},
  "age_gate_clicked": ${AGE_GATE_CLICKED},
  "pdf_captured": ${PDF_CAPTURED},
  "pdf_file": "$(basename "$PDF_FILE")",
  "pdf_size_bytes": ${PDF_SIZE_BYTES},
  "pdf_sha256": "$PDF_SHA256",
  "landing_html_file": "$(basename "$HTML_FILE")",
  "landing_html_size_bytes": ${HTML_SIZE_BYTES},
  "landing_html_sha256": "$HTML_SHA256",
  "landing_text_file": "$(basename "$TEXT_FILE")",
  "landing_text_size_bytes": ${TEXT_SIZE_BYTES},
  "landing_text_sha256": "$TEXT_SHA256",
  "screenshot_file": "$(basename "$SCREENSHOT_FILE")",
  "cookies_file": "$(basename "$COOKIES_FILE")",
  "node_exit_status": ${NODE_STATUS},
  "custody_stage": "INGEST_ONLY_QUARANTINED",
  "promotion_status": "NOT_PROMOTED",
  "write_run_0002": "UNCHANGED",
  "gate_status": "CLOSED",
  "note": "Age verification interaction only. Not canonical. Does not create WRITE_RUN_0002_packet.json."
}
JSON

echo "AGE_PDF_FETCH_DONE"
echo "HTTP_STATUS=$HTTP_STATUS"
echo "FINAL_URL=$FINAL_URL"
echo "AGE_GATE_DETECTED=$AGE_GATE_DETECTED"
echo "AGE_GATE_CLICKED=$AGE_GATE_CLICKED"
echo "PDF_CAPTURED=$PDF_CAPTURED"
echo "PDF_FILE=$PDF_FILE"
echo "PDF_SIZE_BYTES=$PDF_SIZE_BYTES"
echo "PDF_SHA256=$PDF_SHA256"
echo "META=$META_FILE"
