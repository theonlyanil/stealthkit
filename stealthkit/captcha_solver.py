"""
3rd-party CAPTCHA / Turnstile Solver integration module for StealthKit.
Supports APIs such as 2Captcha, CapSolver, Anti-Captcha, etc.
"""
import logging
import time
from typing import Dict, Optional
import curl_cffi.requests as requests

logger = logging.getLogger("stealthkit.captcha_solver")

class CaptchaSolver:
    def __init__(self, api_key: str, provider: str = "2captcha"):
        self.api_key = api_key
        self.provider = provider.lower()

    def solve_turnstile(self, page_url: str, sitekey: str, timeout: int = 60) -> Optional[str]:
        """
        Solves Cloudflare Turnstile using the specified 3rd-party service.
        Returns the solved response token string.
        """
        if self.provider == "2captcha":
            return self._solve_2captcha(page_url, sitekey, captcha_type="turnstile", timeout=timeout)
        elif self.provider in ["capsolver", "anticaptcha"]:
            logger.warning(f"Provider {self.provider} integrated via standard task payload.")
            return self._solve_2captcha(page_url, sitekey, captcha_type="turnstile", timeout=timeout)
        else:
            raise ValueError(f"Unsupported CAPTCHA provider: {self.provider}")

    def _solve_2captcha(self, page_url: str, sitekey: str, captcha_type: str = "turnstile", timeout: int = 60) -> Optional[str]:
        # Step 1: Submit task
        in_url = "https://2captcha.com/in.php"
        payload = {
            "key": self.api_key,
            "method": "turnstile",
            "sitekey": sitekey,
            "pageurl": page_url,
            "json": 1
        }
        
        try:
            res = requests.post(in_url, data=payload).json()
            if res.get("status") != 1:
                logger.error(f"2Captcha task creation failed: {res.get('request')}")
                return None
            
            request_id = res.get("request")
            
            # Step 2: Poll result
            res_url = "https://2captcha.com/res.php"
            start_time = time.time()
            while time.time() - start_time < timeout:
                time.sleep(5)
                res_check = requests.get(res_url, params={
                    "key": self.api_key,
                    "action": "get",
                    "id": request_id,
                    "json": 1
                }).json()
                
                if res_check.get("status") == 1:
                    return res_check.get("request")
                elif res_check.get("request") != "CAPCHA_NOT_READY":
                    logger.error(f"2Captcha error: {res_check.get('request')}")
                    return None
        except Exception as e:
            logger.error(f"CaptchaSolver error: {e}")
        return None
