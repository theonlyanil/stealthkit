# StealthKit

A Python package for making stealthy HTTP requests with rotating user agents, proxies, and customizable headers.

## Installation

```bash
pip install stealthkit
```

## Features

✨ **Automated Request Obfuscation**
- 🔄 Rotating user agents
- 🌐 Proxy support with auto-rotation
- 🎭 Browser fingerprint randomization
- 🍪 Smart cookie management
- 📍 Dynamic referrer headers

## Quick Start

```python
from stealthkit import StealthRequests

# Initialize with default settings
stealth = StealthRequests()

# Make a GET request
response = stealth.get('https://api.example.com')
print(response.json())

# POST request with automatic headers
data = {'key': 'value'}
response = stealth.post('https://api.example.com/post', json=data)
```

## Advanced Configuration

```python
# Initialize with custom settings
stealth = StealthRequests(
    proxies=['http://proxy1:8080', 'http://proxy2:8080'],
    browsers=['chrome', 'firefox'],
    operating_systems=['windows', 'macos'],
    use_cookies=True
)

# Custom headers with request
response = stealth.get(
    'https://api.example.com',
    headers={'Custom-Header': 'Value'}
)
```

## API Reference

### StealthRequests Class

| Parameter | Type | Description |
|-----------|------|-------------|
| `proxies` | `List[str]` | List of proxy URLs |
| `browsers` | `List[str]` | Browser types to emulate |
| `operating_systems` | `List[str]` | OS types to emulate |
| `use_cookies` | `bool` | Enable cookie persistence |

### Methods

- `.get(url, **kwargs)` - Make GET request
- `.post(url, **kwargs)` - Make POST request
- `.put(url, **kwargs)` - Make PUT request
- `.delete(url, **kwargs)` - Make DELETE request
- `.close()` - Close session

## Requirements

- Python 3.7+
- requests >= 2.32.3
- fake-useragent >= 2.0.3

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/name`)
3. Commit changes (`git commit -am 'Add feature'`)
4. Push branch (`git push origin feature/name`)
5. Open Pull Request

## Support

- 📦 [PyPI Package](https://pypi.org/project/stealthkit/)
- 📝 [Documentation](https://github.com/theonlyanil/stealthkit)
- 🐛 [Issue Tracker](https://github.com/theonlyanil/stealthkit/issues)

---
Created by [Anil Sardiwal](https://github.com/theonlyanil)