const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

function candidatePlaywrightModulePaths() {
  const candidates = [];
  if (process.env.MMR_PLAYWRIGHT_MODULE_PATH) {
    candidates.push(process.env.MMR_PLAYWRIGHT_MODULE_PATH);
  }

  const nvmVersionsDir = path.join(os.homedir(), '.nvm', 'versions', 'node');
  if (fs.existsSync(nvmVersionsDir)) {
    for (const version of fs.readdirSync(nvmVersionsDir)) {
      candidates.push(path.join(nvmVersionsDir, version, 'lib', 'node_modules', 'playwright'));
    }
  }
  return candidates;
}

function loadPlaywright() {
  try {
    return require('playwright');
  } catch (localError) {
    const attempted = ['playwright'];
    for (const modulePath of candidatePlaywrightModulePaths()) {
      attempted.push(modulePath);
      try {
        return require(modulePath);
      } catch (_) {
        // Keep trying known local/global install locations before failing.
      }
    }

    throw new Error(
      [
        'Playwright is required for safe local demo verification, but it was not found.',
        `Attempted: ${attempted.join(', ')}`,
        'Install it in this repo with `npm install playwright`, or set MMR_PLAYWRIGHT_MODULE_PATH to an existing Playwright module path.',
        `Original error: ${localError.message}`,
      ].join('\n')
    );
  }
}

const { chromium } = loadPlaywright();

const APP_URL = process.env.MMR_VERIFY_URL || 'http://127.0.0.1:8768';
const TARGET_TITLE = process.env.MMR_DEFAULT_DRILLDOWN || 'Putin out as President of Russia by December 31, 2026?';
const TARGET_HEADLINE = process.env.MMR_DEFAULT_HEADLINE || 'Recent movement or instability is doing meaningful work in the score.';

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
    const openedDetail = await page.evaluate((targetTitle) => {
      const blocks = [...document.querySelectorAll('div[data-testid="stVerticalBlock"]')]
        .filter((el) => {
          const text = el.innerText || '';
          return text.includes(targetTitle) && text.includes('Focus in detail');
        })
        .sort((a, b) => (a.innerText || '').length - (b.innerText || '').length);
      const targetBlock = blocks[0];
      if (!targetBlock) {
        return false;
      }
      const button = [...targetBlock.querySelectorAll('button')].find((el) => (el.innerText || '').includes('Focus in detail'));
      if (!button) {
        return false;
      }
      button.click();
      return true;
    }, TARGET_TITLE);
    await page.waitForTimeout(2500);
    const detailText = await page.locator('body').innerText();
    result.detail = {
      openedDetail,
      hasDetailIntro: detailText.includes('Drill into one market to see why the radar flagged it'),
      hasTargetTitle: detailText.includes(TARGET_TITLE),
      hasHeadlineReason: detailText.includes(TARGET_HEADLINE),
      hasPrimarySignal: detailText.includes('Primary signal:'),
      hasWhyFlagged: detailText.includes('Why this market is flagged'),
      hasObservedSignals: detailText.includes('Observed market signals'),
    };

    assertCheck('radar title', result.radar.hasTitle);
    assertCheck('ranked radar', result.radar.hasRankedRadar);
    assertCheck('methodology nav', result.radar.hasMethodologyNav);
    assertCheck('target radar card', result.radar.hasTargetCard);
    assertCheck('methodology page', result.methodology.hasMethodologyPage);
    assertCheck('methodology honest scope', result.methodology.hasHonestScope);
    assertCheck('detail open action', result.detail.openedDetail);
    assertCheck('market detail intro', result.detail.hasDetailIntro);
    assertCheck('detail target title', result.detail.hasTargetTitle);
    assertCheck('detail headline reason', result.detail.hasHeadlineReason);
    assertCheck('detail primary signal', result.detail.hasPrimarySignal);
    assertCheck('detail why flagged', result.detail.hasWhyFlagged);
    assertCheck('detail observed signals', result.detail.hasObservedSignals);

    console.log(JSON.stringify(result, null, 2));
  } finally {
    await browser.close();
  }
})().catch((error) => {
  console.error(error.stack || String(error));
  process.exit(1);
});
