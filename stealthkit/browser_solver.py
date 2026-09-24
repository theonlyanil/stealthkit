"""
Browser solver module for StealthKit using Playwright.
Provides session cookie pre-warming by solving dynamic JS and Turnstile challenges in a headless browser.
"""
import logging
import time
from typing import Dict, Optional

logger = logging.getLogger("stealthkit.browser_solver")

STEALTH_INIT_SCRIPT = """
// 1. Overwrite navigator.webdriver
Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
});

// 2. Mock languages and plugins
Object.defineProperty(navigator, 'languages', {
    get: () => ['en-US', 'en']
});

Object.defineProperty(navigator, 'plugins', {
    get: () => [1, 2, 3, 4, 5]
});

// 3. WebGL vendor masking
const getParameter = WebGLRenderingContext.prototype.getParameter;
WebGLRenderingContext.prototype.getParameter = function(parameter) {
    // UNMASKED_VENDOR_WEBGL
    if (parameter === 37445) {
        return 'Intel Inc.';
    }
    // UNMASKED_RENDERER_WEBGL
    if (parameter === 37446) {
        return 'Intel(R) Iris(TM) Plus Graphics 640';
    }
    return getParameter.apply(this, arguments);
};
"""

class BrowserSolver:
    def __init__(self, headless: bool = True):
        self.headless = headless

    def solve_challenge(
        self,
        url: str,
        timeout: int = 15,
        proxy: Optional[Dict[str, str]] = None,
        wait_selector: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Launches a Playwright browser with stealth evasions, navigates to the URL,
        auto-clicks Turnstile challenges if detected, and returns captured cookies.
        """
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            raise ImportError(
                "Playwright is required for browser pre-warming. "
                "Install it with `pip install stealthkit[solver]` or `pip install playwright` "
                "and run `playwright install chromium`."
            )

        cookies_dict = {}
        playwright_proxy = None
        if proxy and ("http" in proxy or "https" in proxy):
            p_url = proxy.get("https") or proxy.get("http")
            if p_url:
                playwright_proxy = {"server": p_url}

        with sync_playwright() as p:
            # Stealth launch options
            browser_args = [
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-infobars",
                "--window-size=1920,1080",
                "--disable-dev-shm-usage",
                "--disable-accelerated-2d-canvas",
                "--no-first-run",
                "--no-zygote",
                "--disable-gpu",
            ]

            browser = p.chromium.launch(
                headless=self.headless,
                args=browser_args,
                proxy=playwright_proxy
            )

            context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                locale="en-US",
                timezone_id="America/New_York"
            )

            page = context.new_page()

            # Inject anti-detection evasions
            page.add_init_script(STEALTH_INIT_SCRIPT)

            try:
                page.goto(url, wait_until="domcontentloaded", timeout=timeout * 1000)
                time.sleep(2)

                # Auto-click Turnstile checkbox if present
                self._attempt_turnstile_click(page)

                time.sleep(3)

                if wait_selector:
                    try:
                        page.wait_for_selector(wait_selector, timeout=timeout * 1000)
                    except Exception:
                        pass

                raw_cookies = context.cookies()
                for c in raw_cookies:
                    cookies_dict[c["name"]] = c["value"]

            except Exception as e:
                logger.warning(f"BrowserSolver exception during page load: {e}")
            finally:
                browser.close()

        return cookies_dict

    def _attempt_turnstile_click(self, page):
        """Attempts to locate and click Cloudflare Turnstile checkbox frames."""
        try:
            # Check for Cloudflare Turnstile iframe
            turnstile_frames = [
                f for f in page.frames
                if "challenges.cloudflare.com" in f.url or "turnstile" in f.url
            ]
            for frame in turnstile_frames:
                checkbox = frame.locator('input[type="checkbox"], .cb-i, #challenge-stage')
                if checkbox.count() > 0:
                    logger.info("Found Cloudflare Turnstile checkbox frame. Attempting automated click...")
                    checkbox.first.click()
                    time.sleep(2)
        except Exception as e:
            logger.debug(f"Turnstile auto-click attempt exception: {e}")
