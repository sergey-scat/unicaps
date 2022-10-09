<p align="center">
  <img src="https://i.imgur.com/8aQf6On.png" />
</p>

# Unicaps
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/unicaps.png)](https://pypi.python.org/pypi/unicaps/)
[![PyPI version](https://img.shields.io/pypi/v/unicaps)](https://pypi.python.org/pypi/unicaps/)
[![PyPI status](https://img.shields.io/pypi/status/unicaps.png)](https://pypi.python.org/pypi/unicaps/)
[![CodeFactor](https://www.codefactor.io/repository/github/sergey-scat/unicaps/badge)](https://www.codefactor.io/repository/github/sergey-scat/unicaps)

Unicaps is a unified Python API for CAPTCHA solving services.


⚠ **PLEASE NOTE**</br>
⚠ A solving service API key is required to use this package!</br>
⚠ The list of the supported services you can find in the table below.


## Key Features
 - A unified Python interface that is independent of the service used
 - Uses native service protocol/endpoints (eg, no needs in patching _hosts_ file)
 - Has both synchronous and asynchronous client
 - Supports 11 types of CAPTCHAs
 - Supports 7 CAPTCHA solving services
 - Written Pythonic way and is intended for humans

## Installation
```pip install -U unicaps```

## Simple Usage Example
```python
>>> from unicaps import CaptchaSolver, CaptchaSolvingService
>>> solver = CaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, api_key="<PLACE_YOUR_API_KEY_HERE>")
>>> solver.get_balance()
2.84161
>>> solved = solver.solve_image_captcha(open("captcha.jpg", "rb"), is_phrase=False, is_case_sensitive=True)
>>> solved.solution.text
'w93Bx'
>>> solved.cost
0.00078
>>> solved.report_good()
True
```

## Asynchronous Example
```python
import asyncio
from pathlib import Path
from unicaps import AsyncCaptchaSolver, CaptchaSolvingService

API_KEY = '<PLACE_YOUR_API_KEY_HERE>'

async def main():
    async with AsyncCaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, API_KEY) as solver:
        solved = await solver.solve_image_captcha(
            Path("captcha.jpg"),
            is_phrase=False,
            is_case_sensitive=True
        )
        print(f'CAPTCHA text: {solved.solution.text}')
        await solved.report_good()

if __name__ == '__main__':
    asyncio.run(main())
```

## Supported CAPTCHAs / Services
| CAPTCHA➡ \ Service⬇| Image | Text | [reCAPTCHA v2](https://developers.google.com/recaptcha/docs/display) | [reCAPTCHA v3](https://developers.google.com/recaptcha/docs/v3) | [FunCaptcha](https://funcaptcha.com/fc/api/nojs/?pkey=69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC) | [KeyCAPTCHA](https://www.keycaptcha.com/) | [Geetest](https://www.geetest.com/en/demo) | [Geetest v4](https://www.geetest.com/en/demo) | [hCaptcha](https://www.hcaptcha.com/) | [Capy](https://www.capy.me/) | TikTok
| ------------- | :---: | :---:	| :---:	| :---:	| :---:	| :---:	| :---:	| :---:	| :---:	| :---:	| :---:	|
| [2captcha.com](http://2captcha.com/?from=8754088)	| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| [anti-captcha.com](http://getcaptchasolution.com/vus77mnl48) | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ |
| [azcaptcha.com](https://azcaptcha.com) | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| [captcha.guru](https://captcha.guru/ru/reg/?ref=127872) | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ |
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| [deathbycaptcha.com](http://deathbycaptcha.com) | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| [rucaptcha.com](https://rucaptcha.com?from=9863637) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

### Image CAPTCHA
| Service | Regular | Case Sensitive | Phrase | Numbers only | Letters only | Math | Length | Language | Comment for worker
| ------------- | :---: | :---:	| :---:	| :---:	| :---:	| :---:	| :---:	| :---:	| :---:	|
| [2captcha.com](http://2captcha.com/?from=8754088)	| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Cyrillic/Latin | ✅ |
| [anti-captcha.com](http://getcaptchasolution.com/vus77mnl48) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Latin | ✅ |
| [azcaptcha.com](https://azcaptcha.com/) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | Latin | ✅ |
| [captcha.guru](https://captcha.guru/ru/reg/?ref=127872) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | Latin | ✅ |
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | Cyrillic/Latin | ❌ |
| [deathbycaptcha.com](http://deathbycaptcha.com) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | Latin | ❌ |
| [rucaptcha.com](https://rucaptcha.com?from=9863637) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Cyrillic/Latin | ✅ |

### Text CAPTCHA
<details closed>
<summary>What is this?</summary>

<i>Text Captcha is a type of captcha that is represented as text and doesn't contain images. Usually you have to answer a question to pass the verification.
  For example: "If tomorrow is Saturday, what day is today?".</i>
</details>

| Service | Language |
| ------------- | :---: |
| [2captcha.com](http://2captcha.com/?from=8754088)	| English, Russian |
| [anti-captcha.com](http://getcaptchasolution.com/vus77mnl48) | ❌ |
| [azcaptcha.com](https://azcaptcha.com/) | ❌ |
| [captcha.guru](https://captcha.guru/ru/reg/?ref=127872) | ❌ |
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ❌ |
| [deathbycaptcha.com](http://deathbycaptcha.com) | ❌ |
| [rucaptcha.com](https://rucaptcha.com?from=9863637) | English, Russian |

### reCAPTCHA v2
| Service | Regular | Invisible | Enterprise | Google service<sup>1</sup> | Proxy<sup>2</sup> | Cookies<sup>3</sup> | User-Agent<sup>4</sup> |
| ------------- | :---: | :---:	| :---:	| :---:	| :---:	| :---:	| :---:	|
| [2captcha.com](http://2captcha.com/?from=8754088)	| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| [anti-captcha.com](http://getcaptchasolution.com/vus77mnl48) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| [azcaptcha.com](https://azcaptcha.com/) | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| [captcha.guru](https://captcha.guru/ru/reg/?ref=127872) | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| [deathbycaptcha.com](http://deathbycaptcha.com) | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| [rucaptcha.com](https://rucaptcha.com?from=9863637) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

<sup>1</sup> Support of solving reCAPTCHA on Google services (e.g. Google Search) </br>
<sup>2</sup> Support of solving via proxy server </br>
<sup>3</sup> Support of passing custom cookies </br>
<sup>4</sup> Support of passing custom User-Agent header </br>

### reCAPTCHA v3
| Service | Regular | Enterprise | Proxy | Cookies | User-Agent |
| ------------- | :---: | :---:	| :---:	| :---:	| :---:	|
| [2captcha.com](http://2captcha.com/?from=8754088)	| ✅ | ✅ | ❌ | ❌ | ❌ |
| [anti-captcha.com](http://getcaptchasolution.com/vus77mnl48) | ✅ | ✅ | ❌ | ❌ | ❌ |
| [azcaptcha.com](https://azcaptcha.com/) | ✅ | ❌ | ✅ | ❌ | ❌ |
| [captcha.guru](https://captcha.guru/ru/reg/?ref=127872) | ✅ | ❌ | ✅ | ✅ | ✅ |
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ✅ | ❌ | ❌ | ❌ | ❌ |
| [deathbycaptcha.com](http://deathbycaptcha.com) | ✅ | ❌ | ✅ | ❌ | ❌ |
| [rucaptcha.com](https://rucaptcha.com?from=9863637) | ✅ | ✅ | ❌ | ❌ | ❌ |

### FunCaptcha (Arkose Labs)
| Service | Regular | Data (BLOB) | Proxy | Cookies | User-Agent |
| ------------- | :---: | :---:	| :---:	| :---:	| :---:	|
| [2captcha.com](http://2captcha.com/?from=8754088)	| ✅ | ✅ | ✅ | ❌ | ✅ |
| [anti-captcha.com](http://getcaptchasolution.com/vus77mnl48) | ✅ | ✅ | ✅ | ❌ | ✅ |
| [azcaptcha.com](https://azcaptcha.com/) | ✅ | ✅ | ✅ | ❌ | ✅ |
| [captcha.guru](https://captcha.guru/ru/reg/?ref=127872) | ❌ | ❌ | ❌ | ❌ | ❌ |
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ❌ | ❌ | ❌ | ❌ | ❌ |
| [deathbycaptcha.com](http://deathbycaptcha.com) | ✅ | ❌ | ✅ | ❌ | ❌ |
| [rucaptcha.com](https://rucaptcha.com?from=9863637) | ✅ | ✅ | ✅ | ❌ | ✅ |

### KeyCAPTCHA
| Service | Regular | Proxy | Cookies | User-Agent |
| ------------- | :---: | :---:	| :---:	| :---:	|
| [2captcha.com](http://2captcha.com/?from=8754088)	| ✅ | ❌ | ❌ | ❌ |
| [anti-captcha.com](http://getcaptchasolution.com/vus77mnl48) | ❌ | ❌ | ❌ | ❌ |
| [azcaptcha.com](https://azcaptcha.com/) | ❌ | ❌ | ❌ | ❌ |
| [captcha.guru](https://captcha.guru/ru/reg/?ref=127872) | ❌ | ❌ | ❌ | ❌ |
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ❌ | ❌ | ❌ | ❌ |
| [deathbycaptcha.com](http://deathbycaptcha.com) | ❌ | ❌ | ❌ | ❌ |
| [rucaptcha.com](https://rucaptcha.com?from=9863637) | ✅ | ❌ | ❌ | ❌ |

### Geetest
| Service | Regular | API server | GetLib | Proxy | Cookies | User-Agent |
| ------------- | :---: | :---:	| :---:	| :---:	| :---:	| :---:	|
| [2captcha.com](http://2captcha.com/?from=8754088)	| ✅ | ✅ | ❌ | ✅ | ❌ | ✅ |
| [anti-captcha.com](http://getcaptchasolution.com/vus77mnl48) | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| [azcaptcha.com](https://azcaptcha.com/) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| [captcha.guru](https://captcha.guru/ru/reg/?ref=127872) | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| [deathbycaptcha.com](http://deathbycaptcha.com) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| [rucaptcha.com](https://rucaptcha.com?from=9863637) | ✅ | ✅ | ❌ | ✅ | ❌ | ✅ |

### Geetest v4
| Service | Regular | Proxy | Cookies | User-Agent |
| ------------- | :---: | :---:	| :---:	| :---:	|
| [2captcha.com](http://2captcha.com/?from=8754088)	| ✅ | ✅ | ❌ | ✅ |
| [anti-captcha.com](http://getcaptchasolution.com/vus77mnl48) | ✅ | ✅ | ❌ | ✅ |
| [azcaptcha.com](https://azcaptcha.com/) | ❌ | ❌ | ❌ | ❌ |
| [captcha.guru](https://captcha.guru/ru/reg/?ref=127872) | ❌ | ❌ | ❌ | ❌ |
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ❌ | ❌ | ❌ | ❌ |
| [deathbycaptcha.com](http://deathbycaptcha.com) | ❌ | ❌ | ❌ | ❌ |
| [rucaptcha.com](https://rucaptcha.com?from=9863637) | ✅ | ✅ | ❌ | ✅ |

### hCaptcha
| Service | Regular | Invisible | Custom Data | Proxy | Cookies | User-Agent |
| ------------- | :---: | :---:	| :---:	| :---:	| :---:	| :---:	|
| [2captcha.com](http://2captcha.com/?from=8754088)	| ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| [anti-captcha.com](http://getcaptchasolution.com/vus77mnl48) | ✅ | ✅ | ❌ | ✅ | ❌ | ✅ |
| [azcaptcha.com](https://azcaptcha.com/) | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| [captcha.guru](https://captcha.guru/ru/reg/?ref=127872) | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| [deathbycaptcha.com](http://deathbycaptcha.com) | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| [rucaptcha.com](https://rucaptcha.com?from=9863637) | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |

### Capy Puzzle
| Service | Regular | API server | Proxy | Cookies | User-Agent |
| ------------- | :---: | :---:	| :---:	| :---:	| :---:	|
| [2captcha.com](http://2captcha.com/?from=8754088)	| ✅ | ✅ | ✅ | ❌ | ❌ |
| [anti-captcha.com](http://getcaptchasolution.com/vus77mnl48) | ❌ | ❌ | ❌ | ❌ | ❌ |
| [azcaptcha.com](https://azcaptcha.com/) | ❌ | ❌ | ❌ | ❌ | ❌ |
| [captcha.guru](https://captcha.guru/ru/reg/?ref=127872) | ❌ | ❌ | ❌ | ❌ | ❌ |
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ❌ | ❌ | ❌ | ❌ | ❌ |
| [deathbycaptcha.com](http://deathbycaptcha.com) | ❌ | ❌ | ❌ | ❌ | ❌ |
| [rucaptcha.com](https://rucaptcha.com?from=9863637) | ✅ | ✅ | ✅ | ❌ | ❌ |

### TikTok CAPTCHA
| Service | Regular | Proxy | Cookies | User-Agent |
| ------------- | :---: | :---:	| :---:	| :---:	|
| [2captcha.com](http://2captcha.com/?from=8754088)	| ✅ | ✅ | ✅ | ❌ |
| [anti-captcha.com](http://getcaptchasolution.com/vus77mnl48) | ❌ | ❌ | ❌ | ❌ |
| [azcaptcha.com](https://azcaptcha.com/) | ❌ | ❌ | ❌ | ❌ |
| [captcha.guru](https://captcha.guru/ru/reg/?ref=127872) | ❌ | ❌ | ❌ | ❌ |
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ❌ | ❌ | ❌ | ❌ |
| [deathbycaptcha.com](http://deathbycaptcha.com) | ❌ | ❌ | ❌ | ❌ |
| [rucaptcha.com](https://rucaptcha.com?from=9863637) | ✅ | ✅ | ✅ | ❌ |

## Supported Proxy types
| Service | HTTP | HTTPS | SOCKS 4 | SOCKS 5 |
| ------------- | :---: | :---:	| :---:	| :---:	|
| [2captcha.com](http://2captcha.com/?from=8754088)	| ✅ | ✅ | ✅ | ✅ |
| [anti-captcha.com](http://getcaptchasolution.com/vus77mnl48) | ✅ | ✅ | ✅ | ✅ |
| [azcaptcha.com](https://azcaptcha.com/) | ✅ | ✅ | ✅ | ✅ |
| [captcha.guru](https://captcha.guru/ru/reg/?ref=127872) | ✅ | ✅ | ✅ | ✅ |
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ❌ | ❌ | ❌ | ❌ |
| [deathbycaptcha.com](http://deathbycaptcha.com) | ✅ | ❌ | ❌ | ❌ |
| [rucaptcha.com](https://rucaptcha.com?from=9863637) | ✅ | ✅ | ✅ | ✅ |

## How to...
### Common
<details>
<summary>Get balance</summary>

```python
from unicaps import CaptchaSolver, CaptchaSolvingService

# init captcha solver
with CaptchaSolver(CaptchaSolvingService.ANTI_CAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
    balance = solver.get_balance()
```
</details>

<details>
<summary>Get service status (is the service is up?)</summary>

```python
from unicaps import CaptchaSolver, CaptchaSolvingService

# init captcha solver
with CaptchaSolver(CaptchaSolvingService.ANTI_CAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
    # get status of the service (True - everything is Okay, False - probably the service is down)
    status = solver.get_status()
```
</details>

<details>
<summary>Get technical details after solving</summary>

```python
from unicaps import CaptchaSolver, CaptchaSolvingService

# init captcha solver and solve the captcha
with CaptchaSolver(CaptchaSolvingService.ANTI_CAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
    solved = solver.solve_...(...)

    # get cost of the solving
    cost = solved.cost

    # get cookies (if any)
    cookies = solved.cookies

    # report good captcha
    solved.report_good()

    # report bad captcha
    solved.report_bad()

    # get solving start time
    start_time = solved.start_time

    # get solving end time
    end_time = solved.end_time
```
</details>

### CAPTCHAs
<details>
<summary>Solve Image CAPTCHA</summary>

```python
import pathlib

from unicaps import CaptchaSolver, CaptchaSolvingService
from unicaps.common import CaptchaCharType, CaptchaAlphabet

# image file: it can be a Path, file-object or bytes.
image_file = pathlib.Path(r'/tmp/captcha.png')

# init captcha solver
with CaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
    # solve CAPTCHA
    solved = solver.solve_image_captcha(
        image=image_file,
        char_type=CaptchaCharType.ALPHA,
        is_phrase=False,
        is_case_sensitive=True,
        is_math=False,
        min_len=4,
        max_len=6,
        alphabet=CaptchaAlphabet.LATIN,
        comment='Type RED letters only'
    )
    # get CAPTCHA text
    token = solved.solution.text
```
</details>

<details>
<summary>Solve reCAPTCHA v2</summary>

```python
from unicaps import CaptchaSolver, CaptchaSolvingService

# get page URL and site_key from your page
page_url = ...
site_key = ...

# init captcha solver
with CaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
    # solve CAPTCHA
    solved = solver.solve_recaptcha_v2(
        site_key=site_key,
        page_url=page_url
    )
    # get response token
    token = solved.solution.token
```
</details>

<details>
<summary>Solve reCAPTCHA v2 Invisible</summary>

```python
from unicaps import CaptchaSolver, CaptchaSolvingService

# get page url and site_key from your page
page_url = ...
site_key = ...

# init captcha solver
with CaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
    # solve CAPTCHA
    solved = solver.solve_recaptcha_v2(
        site_key=site_key,
        page_url=page_url,
        is_invisible=True
    )
    # get response token
    token = solved.solution.token
```
</details>

<details>
<summary>Solve reCAPTCHA v2 Enterprise</summary>

```python
from unicaps import CaptchaSolver, CaptchaSolvingService

# get page URL, site_key and data_s from your page
page_url = ...
site_key = ...
data_s = ...

# init captcha solver
with CaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
    # solve CAPTCHA
    solved = solver.solve_recaptcha_v2(
        site_key=site_key,
        page_url=page_url,
        data_s=data_s,
        is_enterprise=True
    )
    # get response token
    token = solved.solution.token
```
</details>

<details>
<summary>Solve reCAPTCHA v3</summary>

```python
from unicaps import CaptchaSolver, CaptchaSolvingService

# get CAPTCHA params from the target page/site
page_url = ...
site_key = ...
action = ...
min_score = 0.7

# init captcha solver
with CaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
    # solve CAPTCHA
    solved = solver.solve_recaptcha_v3(
        site_key=site_key,
        page_url=page_url,
        action=action,
        min_score=min_score
    )
    # get response token
    token = solved.solution.token
```
</details>

<details>
<summary>Solve hCaptcha</summary>

```python
from unicaps import CaptchaSolver, CaptchaSolvingService

# get CAPTCHA params from the target page/site
page_url = ...
site_key = ...

# init captcha solver
with CaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
    # solve CAPTCHA
    solved = solver.solve_hcaptcha(
        site_key=site_key,
        page_url=page_url
    )
    # get response token
    token = solved.solution.token
```
</details>

<details>
<summary>Solve FunCaptcha</summary>

```python
from unicaps import CaptchaSolver, CaptchaSolvingService

# get CAPTCHA params from the target page/site
public_key = ...
page_url = ...

# init captcha solver
with CaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
    # solve CAPTCHA
    solved = solver.solve_funcaptcha(
        public_key=public_key,
        page_url=page_url
    )
    # get response token
    token = solved.solution.token
```
</details>

<details>
<summary>Solve KeyCaptcha</summary>

```python
from unicaps import CaptchaSolver, CaptchaSolvingService

# get CAPTCHA params from the target page/site
page_url = ...
user_id = ...
session_id = ...
ws_sign = ...
ws_sign2 = ...

# init captcha solver
with CaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
    # solve CAPTCHA
    solved = solver.solve_keycaptcha(
        page_url=page_url,
        user_id=user_id,
        session_id=session_id,
        ws_sign=ws_sign,
        ws_sign2=ws_sign2
    )
    # get response token
    token = solved.solution.token
```
</details>

<details>
<summary>Solve Geetest</summary>

```python
from unicaps import CaptchaSolver, CaptchaSolvingService

# get CAPTCHA params from the target page/site
page_url = ...
gt_key = ...
challenge = ...

# init captcha solver
with CaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
    # solve CAPTCHA
    solved = solver.solve_geetest(
        page_url=page_url,
        gt_key=gt_key,
        challenge=challenge
    )
    # get response token
    token = solved.solution.token
```
</details>

<details>
<summary>Solve Geetest v4</summary>

```python
from unicaps import CaptchaSolver, CaptchaSolvingService

# get CAPTCHA params from the target page/site
page_url = ...
captcha_id = ...

# init captcha solver
with CaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
    # solve CAPTCHA
    solved = solver.solve_geetest_v4(
        page_url=page_url,
        captcha_id=captcha_id
    )

    # get solution data
    lot_number = solved.solution.lot_number
    pass_token = solved.solution.pass_token
    gen_time = solved.solution.gen_time
    captcha_output = solved.solution.captcha_output
```
</details>

<details>
<summary>Solve Capy Puzzle</summary>

```python
from unicaps import CaptchaSolver, CaptchaSolvingService

# get CAPTCHA params from the target page/site
site_key = ...
page_url = ...

# init captcha solver
with CaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
    # solve CAPTCHA
    solved = solver.solve_capy_puzzle(
        site_key=site_key,
        page_url=page_url
    )

    # get solution data
    captchakey = solved.solution.captchakey
    challengekey = solved.solution.challengekey
    answer = solved.solution.answer
```
</details>

<details>
<summary>Solve TikTok CAPTCHA</summary>

```python
from unicaps import CaptchaSolver, CaptchaSolvingService

# get CAPTCHA params from the target page/site
page_url = ...
cookies = {'name': 'value', ...}

# init captcha solver
with CaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
    # solve CAPTCHA
    solved = solver.solve_tiktok(
        page_url=page_url,
        cookies=cookies
    )

    # get solution data
    cookies = solved.solution.cookies
```
</details>

<details>
<summary>Solve a text CAPTCHA</summary>

```python
from unicaps import CaptchaSolver, CaptchaSolvingService
from unicaps.common import WorkerLanguage

# init captcha solver
with CaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
    # solve CAPTCHA
    solved = solver.solve_text_captcha(
        text='Si mañana es domingo, ¿qué día es hoy?',
        language=WorkerLanguage.SPANISH
    )

    # get answer
    answer = solved.solution.text  # Sábado
```
</details>

### Error handling
<details>
<summary>Catch exceptions</summary>

```python
from unicaps import CaptchaSolver, CaptchaSolvingService, exceptions

# init captcha solver
with CaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
    # solve CAPTCHA
    try:
        solved = solver.solve_recaptcha_v2(
            site_key=site_key,
            page_url=page_url
        )
    except exceptions.AccessDeniedError:  # wrong API key or the current IP is banned
        pass
    except exceptions.LowBalanceError:  # low balance
        pass
    except exceptions.ServiceTooBusy:  # no available slots to solve CAPTCHA
        pass
    except exceptions.SolutionWaitTimeout:  # haven't received a solution within N minutes
        pass
    except exceptions.TooManyRequestsError:  # request limit exceeded
        pass
    except exceptions.BadInputDataError:  # bad CAPTCHA data (bad image, wrong URL, etc.)
        pass
    except exceptions.UnableToSolveError:  # CAPTCHA unsolvable
        pass
    except exceptions.ProxyError:  # bad proxy
        pass
    except exceptions.NetworkError:  # network connection error
        pass
    else:
        # get response token
        token = solved.solution.token
```
</details>

### Misc
<details>
<summary>Create a task and wait for the result</summary>

```python
from unicaps import CaptchaSolver, CaptchaSolvingService
from unicaps.captcha import RecaptchaV2

# get page URL and site_key from your page
page_url = ...
site_key = ...

# init captcha solver
with CaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
    # create a task
    task = solver.create_task(
        RecaptchaV2(site_key, page_url)
    )

    # print task ID
    print(task.task_id)

    # wait for task to be completed
    solved = task.wait()

    # get response token
    token = solved.solution.token
```
</details>

<details>
<summary>Add proxy, cookies and User-Agent</summary>

```python
from unicaps import CaptchaSolver, CaptchaSolvingService
from unicaps.proxy import ProxyServer

# get page URL and site_key from your page
page_url = ...
site_key = ...
proxy = 'http://user:password@domain.com:8080'
user_agent = '<USER AGENT STRING>'
cookies = {'name': 'value', ...}

# init captcha solver
with CaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
    # solve CAPTCHA
    solved = solver.solve_recaptcha_v2(
        site_key=site_key,
        page_url=page_url,
        proxy=ProxyServer(proxy),
        user_agent=user_agent,
        cookies=cookies
    )
    # get response token
    token = solved.solution.token
```
</details>

## Real-life code examples
[Examples](https://github.com/sergey-scat/unicaps/tree/master/examples)
