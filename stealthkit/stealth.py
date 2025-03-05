import requests
import random
from fake_useragent import UserAgent
from typing import Dict, List, Any
class StealthSession:
    def __init__(self: "StealthSession", proxies: Dict[str, str] | None = None, retries: int = 3) -> None:
        self.session: requests.Session = requests.Session()
        self.retries: int = retries
        self.user_agent: UserAgent = UserAgent()
        self.default_headers: Dict[str, UserAgent | str] = {
            "User-Agent": UserAgent(browsers=['Chrome', 'Edge', 'Safari'], os=['Windows', 'MacOS', 'Linux']).random,
            "Referer": self._get_random_referer(),
        }
        self.session.headers.update(self.default_headers)
        self.proxies: Dict[str, str] = proxies
        self.cookies: requests.cookies.RequestsCookieJar | None = None
    
    def _get_random_referer(self: "StealthSession") -> str:
        referers: List[str] = [
            "https://www.google.com/",
            "https://www.bing.com/",
            "https://www.yahoo.com/",
            "https://duckduckgo.com/"
        ]
        return random.choice(referers)

    def set_headers(self: "StealthSession", additional_headers: Dict[str, str]) -> None:
        self.session.headers.update(additional_headers)
    
    def fetch_cookies(self: "StealthSession", base_url: str) -> None:
        response: requests.Response = self.session.get(base_url, proxies=self.proxies)
        if response.status_code == 200:
            self.cookies = response.cookies
            self.session.cookies.update(self.cookies)
    
    def clear_cookies(self: "StealthSession") -> None:
        self.session.cookies.clear()
        self.cookies = None

    def request(self: "StealthSession", method, url: str, **kwargs: Dict[str, Any]) -> requests.Response | None:
        if self.proxies:
            kwargs["proxies"] = self.proxies
        
        for _ in range(self.retries):
            try:
                response: requests.Response = self.session.request(method, url, **kwargs)
                return response
            except requests.RequestException:
                pass
        return None

    def get(self: "StealthSession", url: str, **kwargs: Dict[str, Any]) -> requests.Response:
        return self.request("GET", url, **kwargs)
    
    def post(self: "StealthSession", url: str, **kwargs: Dict[str, Any]) -> requests.Response:
        return self.request("POST", url, **kwargs)
    
    def put(self: "StealthSession", url: str, **kwargs: Dict[str, Any]) -> requests.Response:
        return self.request("PUT", url, **kwargs)
    
    def delete(self: "StealthSession", url: str, **kwargs: Dict[str, Any]) -> requests.Response:
        return self.request("DELETE", url, **kwargs)

if __name__ == "__main__":
    sr: StealthSession = StealthSession()
    nse_url: str = "https://www.nseindia.com/api/corporates-pit?index=equities"

    custom_headers: Dict[str, str] = {
        "Referer": "https://www.nseindia.com",
        "Accept": "application/json",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "method": "GET",
        "path": "/api/corporates-pit?",
        "scheme": "https",

     }
    
    sr.fetch_cookies("https://www.nseindia.com")
    sr.set_headers(custom_headers)
    response: requests.Response = sr.get(nse_url)

    if response:
        print(response.json())  # Print stock data as JSON
    else:
        print("Failed to fetch stock data")
