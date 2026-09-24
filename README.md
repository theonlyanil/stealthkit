# StealthKit (v1.1.1)

## Overview

`StealthKit` is a Python module that provides a stealthy session handler for web scraping and automated requests. It mimics real browser behavior by synchronizing TLS fingerprints (`curl_cffi`) with matching User-Agent headers, rotating Client Hints, solving JS challenges via Playwright, integrating CAPTCHA solvers, and handling proxies with automatic rotation.

## Features

- **Synchronized Browser Profiles**: Dynamically matches TLS/JA3 fingerprints (`impersonate`) with matching `User-Agent` and `sec-ch-ua` Client Hint headers across Chrome, Safari, and Edge.
- **Session Cookie Pre-Warming**: Solve Cloudflare, DataDome, and PerimeterX JavaScript challenges using a headless browser to pre-warm session cookies.
- **Auto-Rotation & Auto-Solve on Block**: Automatically rotates browser profiles and triggers headless browser pre-warming when encountering HTTP `403`/`429` blocks or JS challenge pages.
- **Residential & Mobile Proxy Management**: Effortless sticky session rotation for residential proxy gateways.
- **3rd-Party CAPTCHA Solvers**: Integrated support for Cloudflare Turnstile solvers (2Captcha, CapSolver).
- **Cookie Handling**: Fetch, store, update, and clear session cookies seamlessly (`clear_cookies()`).
- **RESTful Requests**: Supports GET, POST, PUT, and DELETE methods with full proxy and header integration.

## Anti-Bot Protection Benchmark

The following benchmark demonstrates `StealthKit`'s performance against high-security anti-bot systems:

| Target & Protection System | Status Code | Anti-Bot Result | Verdict |
| :--- | :---: | :---: | :---: |
| **Cloudflare** (`nowsecure.nl`) | `200 OK` | Bypassed | ✅ **PASSED** |
| **Akamai Bot Manager** (`nike.com`) | `200 OK` | Bypassed | ✅ **PASSED** |
| **Akamai Bot Manager** (`airbnb.com`) | `200 OK` | Bypassed | ✅ **PASSED** |
| **DataDome Security** (`hermes.com`) | `200 OK` | Bypassed | ✅ **PASSED** |
| **PerimeterX / HUMAN** (`stockx.com`) | `200 OK` | Bypassed | ✅ **PASSED** |
| **NSE India WAF** (`nseindia.com`) | `200 OK` | Bypassed | ✅ **PASSED** |

---

## Installation

### Basic Installation
```sh
pip install stealthkit
```

### Installation with Headless Browser Solver Support
```sh
pip install stealthkit[solver]
playwright install chromium
```

---

## Basic Usage

```python
from stealthkit import StealthSession

# Create a stealth session
sr = StealthSession()

# Fetch cookies from a base URL
sr.fetch_cookies("https://www.example.com")

# Make a GET request
response = sr.get("https://www.example.com/api")

if response:
    print("Status:", response.status_code)
    print(response.json())

# Clear cookies when needed
sr.clear_cookies()
```

---

## Advanced Usage

### 1. Synchronized TLS & User-Agent Profiles
`StealthKit` matches TLS fingerprints (`impersonate`) with exact User-Agent and `sec-ch-ua` Client Hints:
```python
from stealthkit import StealthSession, BROWSER_PROFILES

# Initialize with explicit profile target
sr = StealthSession(impersonate="chrome124")

# Rotate profile dynamically on the fly
sr.rotate_profile()
print("New Profile:", sr.current_profile["name"])
```

### 2. Session Cookie Pre-Warming (Headless Browser)
Pre-warm session cookies (`cf_clearance`, `datadome`, `_px3`) by solving dynamic JS challenges via Playwright:
```python
sr = StealthSession()

# Solves JS challenges in headless browser & populates sr.cookies automatically
sr.solve_challenge("https://www.target-site.com")
response = sr.get("https://www.target-site.com/api/data")
```

### 3. Residential & Mobile Proxy Session Rotation
Rotate sticky session IDs across proxy requests seamlessly:
```python
sr = StealthSession()
proxy_template = "http://user-session-{session_id}:password@gate.smartproxy.com:7000"

# Rotates proxy session ID
sr.rotate_proxy_session(proxy_template)
response = sr.get("https://www.target-site.com")
```

### 4. 3rd-Party CAPTCHA & Turnstile Solvers
Integrate 2Captcha or CapSolver for Turnstile resolution:
```python
from stealthkit import CaptchaSolver

solver = CaptchaSolver(api_key="YOUR_2CAPTCHA_API_KEY", provider="2captcha")
token = solver.solve_turnstile(page_url="https://site.com", sitekey="0x4AAAAAA...")
```

### 5. Custom Headers & HTTP Methods
```python
sr = StealthSession()

# Set custom headers
sr.set_headers({"Accept": "application/json", "Referer": "https://www.google.com"})

# HTTP POST, PUT, DELETE
sr.post("https://www.example.com/api", json={"key": "value"})
sr.put("https://www.example.com/api", json={"key": "updated"})
sr.delete("https://www.example.com/api")
```

### 6. Retries, Auto-Rotation & Auto-Solve on Block
```python
# Automatically rotates browser profile & triggers headless browser pre-warming on JS challenge / block responses
sr = StealthSession(
    retries=3,
    auto_rotate_on_blocked=True,
    auto_solve_on_blocked=True
)
```

---

## License
This project is licensed under the MIT License.
