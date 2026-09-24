import curl_cffi.requests as requests
from curl_cffi.requests.errors import RequestsError
import random
import logging
import uuid
from typing import Dict, Optional

from .profiles import BROWSER_PROFILES

logger = logging.getLogger("stealthkit")

class StealthSession:
    def __init__(
        self,
        impersonate: str = "chrome124",
        proxies: Optional[Dict[str, str]] = None,
        retries: int = 3,
        auto_rotate_on_blocked: bool = True,
        auto_solve_on_blocked: bool = False,
        captcha_solver: Optional[object] = None,
    ):
        self.session = requests.Session()
        self.retries = retries
        self.proxies = proxies
        self.cookies = None
        self.auto_rotate = auto_rotate_on_blocked
        self.auto_solve = auto_solve_on_blocked
        self.captcha_solver = captcha_solver
        self.current_profile = None

        # Apply initial synchronized profile
        self.set_profile(impersonate)

    def _get_random_referer(self) -> str:
        referers = [
            "https://www.google.com/",
            "https://www.bing.com/",
            "https://www.yahoo.com/",
            "https://duckduckgo.com/",
        ]
        return random.choice(referers)

    def set_profile(self, target_impersonate: Optional[str] = None):
        """
        Synchronizes TLS fingerprint (impersonate) with matching headers (User-Agent, sec-ch-ua).
        """
        if target_impersonate:
            matched = [p for p in BROWSER_PROFILES if p["impersonate"] == target_impersonate]
            profile = matched[0] if matched else BROWSER_PROFILES[0]
        else:
            profile = random.choice(BROWSER_PROFILES)

        self.current_profile = profile
        self.session.impersonate = profile["impersonate"]

        headers = {
            "User-Agent": profile["user_agent"],
            "Referer": self._get_random_referer(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }

        if profile["sec_ch_ua"]:
            headers["sec-ch-ua"] = profile["sec_ch_ua"]
            headers["sec-ch-ua-mobile"] = profile["sec_ch_ua_mobile"]
            headers["sec-ch-ua-platform"] = profile["sec_ch_ua_platform"]

        self.session.headers.update(headers)

    def rotate_profile(self):
        """Rotates to a different synchronized browser profile."""
        current_name = self.current_profile["name"] if self.current_profile else ""
        available = [p for p in BROWSER_PROFILES if p["name"] != current_name]
        chosen = random.choice(available if available else BROWSER_PROFILES)
        self.set_profile(chosen["impersonate"])

    def set_headers(self, additional_headers: Dict[str, str]):
        self.session.headers.update(additional_headers)

    def fetch_cookies(self, base_url: str):
        response = self.session.get(base_url, proxies=self.proxies)
        if response and response.status_code == 200:
            self.cookies = response.cookies.get_dict()
            self.session.cookies.update(self.cookies)

    def clear_cookies(self):
        self.session.cookies.clear()
        self.cookies = None

    def solve_challenge(self, url: str, timeout: int = 15, headless: bool = True) -> Dict[str, str]:
        """
        Uses Playwright to solve dynamic JS / Turnstile challenges and pre-warm session cookies.
        """
        from .browser_solver import BrowserSolver
        solver = BrowserSolver(headless=headless)
        solved_cookies = solver.solve_challenge(url, timeout=timeout, proxy=self.proxies)
        if solved_cookies:
            self.session.cookies.update(solved_cookies)
            self.cookies = self.session.cookies.get_dict()
        return solved_cookies

    def rotate_proxy_session(self, proxy_template: str) -> Dict[str, str]:
        """
        Helper for residential proxy rotation. Appends a unique session ID tag.
        Example template: 'http://user-session-{session_id}:pass@proxy.example.com:7000'
        """
        session_id = uuid.uuid4().hex[:8]
        new_proxy_str = proxy_template.format(session_id=session_id)
        self.proxies = {"http": new_proxy_str, "https": new_proxy_str}
        return self.proxies

    def request(self, method: str, url: str, **kwargs):
        if self.proxies:
            kwargs["proxies"] = self.proxies

        for attempt in range(1, self.retries + 1):
            try:
                response = self.session.request(method, url, **kwargs)
                if response is not None:
                    is_js_challenge = any(
                        b in response.text.lower()
                        for b in ['captcha', 'robot or human', 'just a moment', 'pardon our interruption', 'enable javascript']
                    )
                    is_blocked = response.status_code in [403, 429] or is_js_challenge

                    if is_blocked and attempt < self.retries:
                        if self.auto_solve:
                            logger.info(f"Block/Challenge detected on {url}. Triggering headless BrowserSolver pre-warming on retry {attempt}/{self.retries}...")
                            try:
                                self.solve_challenge(url, timeout=12)
                            except Exception as solve_err:
                                logger.warning(f"Auto solve_challenge failed: {solve_err}")

                        if self.auto_rotate:
                            logger.info(f"Rotating profile on retry {attempt}/{self.retries}...")
                            self.rotate_profile()

                        continue
                    return response
            except (RequestsError, Exception) as e:
                logger.warning(f"Request exception attempt {attempt}/{self.retries}: {e}")
                if attempt < self.retries:
                    if self.auto_rotate:
                        self.rotate_profile()
                continue
        return None

    def get(self, url: str, **kwargs):
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs):
        return self.request("POST", url, **kwargs)

    def put(self, url: str, **kwargs):
        return self.request("PUT", url, **kwargs)

    def delete(self, url: str, **kwargs):
        return self.request("DELETE", url, **kwargs)


if __name__ == "__main__":
    sr = StealthSession()
    res = sr.get("https://tls.browserleaks.com/json")
    if res:
        print("Status:", res.status_code)
        print("TLS Profile Test Response:", res.text[:200])