function loadPlaywright() {
  try {
    return require('playwright');
  } catch (_) {
    return require('/home/catalysm/.openclaw/workspace/state/browser/node_modules/playwright');
  }
}

const { chromium } = loadPlaywright();

const APP_URL = process.env.MMR_VERIFY_URL || 'http://127.0.0.1:8768';
const TARGET_TITLE = process.env.MMR_DEFAULT_DRILLDOWN || 'GTA VI released before June 2026?';
const TARGET_HEADLINE = process.env.MMR_DEFAULT_HEADLINE || 'Extreme pricing is being carried with relatively weak support.';

function assertCheck(name, value) {
  if (!value) {
    throw new Error(`verification failed: ${name}`);
  }
}

(async() => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1200 } });

  try {
    await page.goto(APP_URL, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(4000);

    const radarText = await page.locator('body').innerText();
    const refreshMatch = radarText.match(/Refresh ID:\s*(\S+)/);
    const result = {
      appUrl: APP_URL,
      targetTitle: TARGET_TITLE,
      refreshId: refreshMatch ? refreshMatch[1] : null,
      radar: {
        hasTitle: radarText.includes('Market Mispricing Radar'),
        hasRankedRadar: radarText.includes('Ranked Radar'),
        hasMethodologyNav: radarText.includes('Methodology'),
        hasTargetCard: radarText.includes(TARGET_TITLE),
      },
      methodology: null,
      detail: null,
    };

    await page.getByText('Methodology').first().click();
    await page.waitForTimeout(1500);
    const methodologyText = await page.locator('body').innerText();
    result.methodology = {
      hasMethodologyPage: methodologyText.includes('Methodology'),
      hasHonestScope:
        methodologyText.includes('triage signal') ||
        methodologyText.includes('profit promise') ||
        methodologyText.includes('fair value'),
    };

    await page.goto(APP_URL, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(3000);
    await page.getByText(TARGET_TITLE).first().click();
    await page.waitForTimeout(2500);
    const detailText = await page.locator('body').innerText();
    result.detail = {
      hasMarketDetail: detailText.includes('Market Detail'),
      hasTargetTitle: detailText.includes(TARGET_TITLE),
      hasHeadlineReason: detailText.includes(TARGET_HEADLINE),
      hasPrimarySignal: detailText.includes('Primary signal:'),
    };

    assertCheck('radar title', result.radar.hasTitle);
    assertCheck('ranked radar', result.radar.hasRankedRadar);
    assertCheck('methodology nav', result.radar.hasMethodologyNav);
    assertCheck('target radar card', result.radar.hasTargetCard);
    assertCheck('methodology page', result.methodology.hasMethodologyPage);
    assertCheck('methodology honest scope', result.methodology.hasHonestScope);
    assertCheck('market detail', result.detail.hasMarketDetail);
    assertCheck('detail target title', result.detail.hasTargetTitle);
    assertCheck('detail headline reason', result.detail.hasHeadlineReason);

    console.log(JSON.stringify(result, null, 2));
  } finally {
    await browser.close();
  }
})().catch((error) => {
  console.error(error.stack || String(error));
  process.exit(1);
});
