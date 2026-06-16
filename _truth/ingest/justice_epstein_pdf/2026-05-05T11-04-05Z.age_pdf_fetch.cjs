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
