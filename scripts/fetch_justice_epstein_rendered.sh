#!/usr/bin/env bash
set -euo pipefail

# ALMS rendered web ingest for https://www.justice.gov/epstein
# Stage: INGEST_ONLY_QUARANTINED
# Requires: node, npm, Playwright Chromium installed locally.
# This script does not promote, does not write DOJ_RELEASE/HASH_INDEX,
# and does not create WRITE_RUN_0002_packet.json.

URL="https://www.justice.gov/epstein"
SOURCE_ID="justice_epstein"
OUT_DIR="_truth/ingest/justice_epstein_rendered"
PROFILE_DIR="_truth/browser_profiles/justice_epstein"
TS="$(date -u +%Y-%m-%dT%H-%M-%SZ)"
mkdir -p "$OUT_DIR" "$PROFILE_DIR"

HTML_FILE="$OUT_DIR/${TS}.rendered.html"
TEXT_FILE="$OUT_DIR/${TS}.rendered.txt"
SCREENSHOT_FILE="$OUT_DIR/${TS}.png"
COOKIES_FILE="$OUT_DIR/${TS}.cookies.json"
META_FILE="$OUT_DIR/${TS}.meta.json"
HASH_FILE="$OUT_DIR/${TS}.sha256"
PW_SCRIPT="$OUT_DIR/${TS}.playwright.cjs"

cat > "$PW_SCRIPT" <<'NODE'
const fs = require('fs');
const { chromium } = require('playwright');

(async () => {
  const url = process.env.ALMS_URL;
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
    ignoreHTTPSErrors: false
  });

  const page = await browser.newPage();
  const startedAt = new Date().toISOString();
  let responseStatus = null;
  let responseUrl = null;
  let title = null;
  let barrierLikely = false;

  try {
    const response = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 90000 });
    if (response) {
      responseStatus = response.status();
      responseUrl = response.url();
    }

    // Give JS challenge/client rendering a chance to settle, but stay bounded.
    await page.waitForLoadState('networkidle', { timeout: 30000 }).catch(() => {});
    await page.waitForTimeout(5000);

    title = await page.title().catch(() => null);
    const html = await page.content();
    const text = await page.locator('body').innerText({ timeout: 10000 }).catch(() => '');

    barrierLikely = /bm-verify|akamai|Bot Manager|Access Denied|verify you are human|_abck|sensor_data/i.test(html + '\n' + text);

    fs.writeFileSync(htmlFile, html, 'utf8');
    fs.writeFileSync(textFile, text, 'utf8');
    await page.screenshot({ path: screenshotFile, fullPage: true }).catch(() => {});
    fs.writeFileSync(cookiesFile, JSON.stringify(await browser.cookies(), null, 2) + '\n', 'utf8');

    console.log(JSON.stringify({
      ok: true,
      started_at_utc: startedAt,
      completed_at_utc: new Date().toISOString(),
      url,
      final_url: page.url(),
      response_status: responseStatus,
      response_url: responseUrl,
      title,
      barrier_likely: barrierLikely
    }));
  } catch (err) {
    console.log(JSON.stringify({
      ok: false,
      started_at_utc: startedAt,
      completed_at_utc: new Date().toISOString(),
      url,
      final_url: page.url ? page.url() : null,
      response_status: responseStatus,
      response_url: responseUrl,
      title,
      barrier_likely: true,
      error: String(err && err.message ? err.message : err)
    }));
    process.exitCode = 2;
  } finally {
    await browser.close();
  }
})();
NODE

if ! command -v node >/dev/null 2>&1; then
  echo "NODE_MISSING"
  echo "Install Node.js/npm first, then run: npm install playwright && npx playwright install chromium"
  exit 1
fi

if [ ! -d node_modules/playwright ]; then
  echo "PLAYWRIGHT_MISSING"
  echo "Run: npm install playwright && npx playwright install chromium"
  exit 1
fi

set +e
ALMS_URL="$URL" \
ALMS_HTML_FILE="$HTML_FILE" \
ALMS_TEXT_FILE="$TEXT_FILE" \
ALMS_SCREENSHOT_FILE="$SCREENSHOT_FILE" \
ALMS_COOKIES_FILE="$COOKIES_FILE" \
ALMS_PROFILE_DIR="$PROFILE_DIR" \
node "$PW_SCRIPT" > "$OUT_DIR/${TS}.playwright.result.json"
NODE_STATUS=$?
set -e

if [ ! -f "$HTML_FILE" ]; then
  echo "RENDERED_HTML_NOT_CREATED"
  cat "$OUT_DIR/${TS}.playwright.result.json" || true
  exit 1
fi

HTML_SHA256=$(sha256sum "$HTML_FILE" | awk '{print $1}')
TEXT_SHA256=$(sha256sum "$TEXT_FILE" | awk '{print $1}')
HTML_SIZE_BYTES=$(wc -c < "$HTML_FILE" | tr -d ' ')
TEXT_SIZE_BYTES=$(wc -c < "$TEXT_FILE" | tr -d ' ')
RESULT_JSON=$(cat "$OUT_DIR/${TS}.playwright.result.json")
FINAL_URL=$(printf '%s' "$RESULT_JSON" | jq -r '.final_url // empty')
HTTP_STATUS=$(printf '%s' "$RESULT_JSON" | jq -r '.response_status // empty')
TITLE=$(printf '%s' "$RESULT_JSON" | jq -r '.title // empty')
BARRIER_LIKELY=$(printf '%s' "$RESULT_JSON" | jq -r '.barrier_likely // true')

{
  echo "$HTML_SHA256  $(basename "$HTML_FILE")"
  echo "$TEXT_SHA256  $(basename "$TEXT_FILE")"
} > "$HASH_FILE"

cat > "$META_FILE" <<JSON
{
  "source": "$SOURCE_ID",
  "url": "$URL",
  "final_url": "$FINAL_URL",
  "http_status": "$HTTP_STATUS",
  "title": $(jq -Rn --arg v "$TITLE" '$v'),
  "fetched_at_utc": "${TS}",
  "render_method": "playwright_chromium_persistent_context",
  "profile_dir": "$PROFILE_DIR",
  "html_file": "$(basename "$HTML_FILE")",
  "text_file": "$(basename "$TEXT_FILE")",
  "screenshot_file": "$(basename "$SCREENSHOT_FILE")",
  "cookies_file": "$(basename "$COOKIES_FILE")",
  "html_size_bytes": ${HTML_SIZE_BYTES},
  "text_size_bytes": ${TEXT_SIZE_BYTES},
  "html_sha256": "$HTML_SHA256",
  "text_sha256": "$TEXT_SHA256",
  "barrier_likely": ${BARRIER_LIKELY},
  "node_exit_status": ${NODE_STATUS},
  "custody_stage": "INGEST_ONLY_QUARANTINED",
  "promotion_status": "NOT_PROMOTED",
  "write_run_0002": "UNCHANGED",
  "gate_status": "CLOSED",
  "note": "Rendered browser ingest only. Not canonical. Does not create WRITE_RUN_0002_packet.json."
}
JSON

echo "RENDERED_FETCH_OK"
echo "HTTP_STATUS=$HTTP_STATUS"
echo "FINAL_URL=$FINAL_URL"
echo "TITLE=$TITLE"
echo "BARRIER_LIKELY=$BARRIER_LIKELY"
echo "HTML_FILE=$HTML_FILE"
echo "HTML_SIZE_BYTES=$HTML_SIZE_BYTES"
echo "HTML_SHA256=$HTML_SHA256"
echo "TEXT_FILE=$TEXT_FILE"
echo "TEXT_SIZE_BYTES=$TEXT_SIZE_BYTES"
echo "TEXT_SHA256=$TEXT_SHA256"
echo "META=$META_FILE"
