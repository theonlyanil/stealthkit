"""
Browser profiles registry for StealthKit.
Synchronizes curl_cffi TLS impersonation targets with matching User-Agent and sec-ch-ua headers.
"""

BROWSER_PROFILES = [
    {
        "name": "chrome124_win",
        "impersonate": "chrome124",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "sec_ch_ua": '"Not-A.Brand";v="99", "Chromium";v="124", "Google Chrome";v="124"',
        "sec_ch_ua_platform": '"Windows"',
        "sec_ch_ua_mobile": "?0",
    },
    {
        "name": "chrome120_mac",
        "impersonate": "chrome120",
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "sec_ch_ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "sec_ch_ua_platform": '"macOS"',
        "sec_ch_ua_mobile": "?0",
    },
    {
        "name": "chrome119_linux",
        "impersonate": "chrome119",
        "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "sec_ch_ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        "sec_ch_ua_platform": '"Linux"',
        "sec_ch_ua_mobile": "?0",
    },
    {
        "name": "safari17_0_mac",
        "impersonate": "safari17_0",
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        "sec_ch_ua": None,
        "sec_ch_ua_platform": None,
        "sec_ch_ua_mobile": None,
    },
    {
        "name": "safari15_5_mac",
        "impersonate": "safari15_5",
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15",
        "sec_ch_ua": None,
        "sec_ch_ua_platform": None,
        "sec_ch_ua_mobile": None,
    },
    {
        "name": "edge101_win",
        "impersonate": "edge101",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47",
        "sec_ch_ua": '"Not A;Brand";v="99", "Chromium";v="101", "Microsoft Edge";v="101"',
        "sec_ch_ua_platform": '"Windows"',
        "sec_ch_ua_mobile": "?0",
    },
]
