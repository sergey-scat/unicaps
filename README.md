<p align="center">
  <img src="https://i.imgur.com/8aQf6On.png" />
</p>

# Unicaps
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/unicaps.svg)](https://pypi.python.org/pypi/unicaps/)
[![PyPI version fury.io](https://badge.fury.io/py/unicaps.svg)](https://pypi.python.org/pypi/unicaps/)
[![PyPI status](https://img.shields.io/pypi/status/unicaps.svg)](https://pypi.python.org/pypi/unicaps/)

Unicaps is a unified Python API for CAPTCHA solving services.


⚠ **PLEASE NOTE**</br>
⚠ A solving service API key is required to use this package!</br>
⚠ The list of the supported services you can find in the table below.


## Key Features
 - A unified Python interface that is independent of the service used
 - Uses native service protocol/endpoints (eg, no needs in patching _hosts_ file)
 - Has both synchronous and asynchronous client
 - Supports 11 types of CAPTCHAs
 - Supports 5 CAPTCHA solving services
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
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| [rucaptcha.com](https://rucaptcha.com?from=9863637) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

### Image CAPTCHA
| Service | Regular | Case Sensitive | Phrase | Numbers only | Letters only | Math | Length | Language | Comment for worker
| ------------- | :---: | :---:	| :---:	| :---:	| :---:	| :---:	| :---:	| :---:	| :---:	|
| [2captcha.com](http://2captcha.com/?from=8754088)	| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Cyrillic/Latin | ✅ |
| [anti-captcha.com](http://getcaptchasolution.com/vus77mnl48) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Latin | ✅ |
| [azcaptcha.com](https://azcaptcha.com/) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | Latin | ✅ |
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | Cyrillic/Latin | ❌ |
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
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ❌ |
| [rucaptcha.com](https://rucaptcha.com?from=9863637) | English, Russian |

### reCAPTCHA v2
| Service | Regular | Invisible | Enterprise | Google service<sup>1</sup> | Proxy<sup>2</sup> | Cookies<sup>3</sup> | User-Agent<sup>4</sup> |
| ------------- | :---: | :---:	| :---:	| :---:	| :---:	| :---:	| :---:	|
| [2captcha.com](http://2captcha.com/?from=8754088)	| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| [anti-captcha.com](http://getcaptchasolution.com/vus77mnl48) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| [azcaptcha.com](https://azcaptcha.com/) | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
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
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ✅ | ❌ | ❌ | ❌ | ❌ |
| [rucaptcha.com](https://rucaptcha.com?from=9863637) | ✅ | ✅ | ❌ | ❌ | ❌ |

### FunCaptcha (Arkose Labs)
| Service | Regular | Data (BLOB) | Proxy | Cookies | User-Agent |
| ------------- | :---: | :---:	| :---:	| :---:	| :---:	|
| [2captcha.com](http://2captcha.com/?from=8754088)	| ✅ | ✅ | ✅ | ❌ | ✅ |
| [anti-captcha.com](http://getcaptchasolution.com/vus77mnl48) | ✅ | ✅ | ✅ | ❌ | ✅ |
| [azcaptcha.com](https://azcaptcha.com/) | ✅ | ✅ | ✅ | ❌ | ✅ |
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ❌ | ❌ | ❌ | ❌ | ❌ |
| [rucaptcha.com](https://rucaptcha.com?from=9863637) | ✅ | ✅ | ✅ | ❌ | ✅ |

### KeyCAPTCHA
| Service | Regular | Proxy | Cookies | User-Agent |
| ------------- | :---: | :---:	| :---:	| :---:	|
| [2captcha.com](http://2captcha.com/?from=8754088)	| ✅ | ❌ | ❌ | ❌ |
| [anti-captcha.com](http://getcaptchasolution.com/vus77mnl48) | ❌ | ❌ | ❌ | ❌ |
| [azcaptcha.com](https://azcaptcha.com/) | ❌ | ❌ | ❌ | ❌ |
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ❌ | ❌ | ❌ | ❌ |
| [rucaptcha.com](https://rucaptcha.com?from=9863637) | ✅ | ❌ | ❌ | ❌ |

### Geetest
| Service | Regular | API server | GetLib | Proxy | Cookies | User-Agent |
| ------------- | :---: | :---:	| :---:	| :---:	| :---:	| :---:	|
| [2captcha.com](http://2captcha.com/?from=8754088)	| ✅ | ✅ | ❌ | ✅ | ❌ | ✅ |
| [anti-captcha.com](http://getcaptchasolution.com/vus77mnl48) | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| [azcaptcha.com](https://azcaptcha.com/) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| [rucaptcha.com](https://rucaptcha.com?from=9863637) | ✅ | ✅ | ❌ | ✅ | ❌ | ✅ |

### Geetest v4
| Service | Regular | Proxy | Cookies | User-Agent |
| ------------- | :---: | :---:	| :---:	| :---:	|
| [2captcha.com](http://2captcha.com/?from=8754088)	| ✅ | ✅ | ❌ | ✅ |
| [anti-captcha.com](http://getcaptchasolution.com/vus77mnl48) | ✅ | ✅ | ❌ | ✅ |
| [azcaptcha.com](https://azcaptcha.com/) | ❌ | ❌ | ❌ | ❌ |
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ❌ | ❌ | ❌ | ❌ |
| [rucaptcha.com](https://rucaptcha.com?from=9863637) | ✅ | ✅ | ❌ | ✅ |

### hCaptcha
| Service | Regular | Invisible | Custom Data | Proxy | Cookies | User-Agent |
| ------------- | :---: | :---:	| :---:	| :---:	| :---:	| :---:	|
| [2captcha.com](http://2captcha.com/?from=8754088)	| ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| [anti-captcha.com](http://getcaptchasolution.com/vus77mnl48) | ✅ | ✅ | ❌ | ✅ | ❌ | ✅ |
| [azcaptcha.com](https://azcaptcha.com/) | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| [rucaptcha.com](https://rucaptcha.com?from=9863637) | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |

### Capy Puzzle
| Service | Regular | API server | Proxy | Cookies | User-Agent |
| ------------- | :---: | :---:	| :---:	| :---:	| :---:	|
| [2captcha.com](http://2captcha.com/?from=8754088)	| ✅ | ✅ | ✅ | ❌ | ❌ |
| [anti-captcha.com](http://getcaptchasolution.com/vus77mnl48) | ❌ | ❌ | ❌ | ❌ | ❌ |
| [azcaptcha.com](https://azcaptcha.com/) | ❌ | ❌ | ❌ | ❌ | ❌ |
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ❌ | ❌ | ❌ | ❌ | ❌ |
| [rucaptcha.com](https://rucaptcha.com?from=9863637) | ✅ | ✅ | ✅ | ❌ | ❌ |

### TikTok CAPTCHA
| Service | Regular | Proxy | Cookies | User-Agent |
| ------------- | :---: | :---:	| :---:	| :---:	|
| [2captcha.com](http://2captcha.com/?from=8754088)	| ✅ | ✅ | ✅ | ❌ |
| [anti-captcha.com](http://getcaptchasolution.com/vus77mnl48) | ❌ | ❌ | ❌ | ❌ |
| [azcaptcha.com](https://azcaptcha.com/) | ❌ | ❌ | ❌ | ❌ |
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ❌ | ❌ | ❌ | ❌ |
| [rucaptcha.com](https://rucaptcha.com?from=9863637) | ✅ | ✅ | ✅ | ❌ |

## Supported Proxy types
| Service | HTTP | HTTPS | SOCKS 4 | SOCKS 5 |
| ------------- | :---: | :---:	| :---:	| :---:	|
| [2captcha.com](http://2captcha.com/?from=8754088)	| ✅ | ✅ | ✅ | ✅ |
| [anti-captcha.com](http://getcaptchasolution.com/vus77mnl48) | ✅ | ✅ | ✅ | ✅ |
| [azcaptcha.com](https://azcaptcha.com/) | ✅ | ✅ | ✅ | ✅ |
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ❌ | ❌ | ❌ | ❌ |
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

### Solving
<details>
<summary>Image CAPTCHA</summary>

```python
import pathlib

from unicaps import CaptchaSolver, CaptchaSolvingService
from unicaps.common import CaptchaCharType, CaptchaAlphabet

# get image file
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
<summary>reCAPTCHA v2</summary>

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
<summary>reCAPTCHA v2 Invisible</summary>

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
<summary>reCAPTCHA v2 Enterprise</summary>

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
<summary>reCAPTCHA v3</summary>

```python
from unicaps import CaptchaSolver, CaptchaSolvingService

# get page URL, site_key and action from your page
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
<summary>hCaptcha</summary>

```python
from unicaps import CaptchaSolver, CaptchaSolvingService

# get page URL and site_key from your page
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

### Error handling
<details>
<summary>Exceptions</summary>

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

### Proxy
<details>
<summary>Add proxy, cookies and User-Agent</summary>

```python
from unicaps import CaptchaSolver, CaptchaSolvingService
from unicaps.proxy import ProxyServer

# get page URL and site_key from your page
PAGE_URL = ...
SITE_KEY = ...
PROXY = 'http://user:password@domain.com:8080'
USER_AGENT = '<USER AGENT STRING>'
COOKIES = {'name': 'value', ...}

# init captcha solver
with CaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
    # solve CAPTCHA
    solved = solver.solve_recaptcha_v2(
        site_key=site_key,
        page_url=page_url,
        proxy=ProxyServer(PROXY),
        user_agent=USER_AGENT,
        cookies=COOKIES
    )
    # get response token
    token = solved.solution.token
```
</details>

## Real-life code examples
[Examples](https://github.com/sergey-scat/unicaps/tree/master/examples)
