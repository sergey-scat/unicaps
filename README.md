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
 - Supports 10 types of CAPTCHAs
 - Supports 5 CAPTCHA solving services (3 more would be added soon)
 - Written Pythonic way and is intended for humans

## Installation
```pip install unicaps```

## Simple Usage Example
```python
>>> from unicaps import CaptchaSolver, CaptchaSolvingService
>>> solver = CaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, api_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
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

## Supported CAPTCHAs / Services
| CAPTCHA➡ \ Service⬇| Image | Text | [reCAPTCHA v2](https://developers.google.com/recaptcha/docs/display) | [reCAPTCHA v3](https://developers.google.com/recaptcha/docs/v3) | [FunCaptcha](https://funcaptcha.com/fc/api/nojs/?pkey=69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC) | [KeyCAPTCHA](https://www.keycaptcha.com/) | [Geetest](https://www.geetest.com/en/demo) | [hCaptcha](https://www.hcaptcha.com/) | [Capy](https://www.capy.me/) | TikTok
| ------------- | :---: | :---:	| :---:	| :---:	| :---:	| :---:	| :---:	| :---:	| :---:	| :---:	|
| [2captcha.com](http://2captcha.com/?from=8754088)	| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| [anti-captcha.com](http://getcaptchasolution.com/vus77mnl48) | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ |
| [azcaptcha.com](https://azcaptcha.com) | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| [rucaptcha.com](https://rucaptcha.com?from=9863637) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

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
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
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
| [azcaptcha.com](https://azcaptcha.com/) | ✅ | ✅ | ✅ | ❌ | ❌ |
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ✅ | ❌ | ❌ | ❌ | ❌ |
| [rucaptcha.com](https://rucaptcha.com?from=9863637) | ✅ | ✅ | ❌ | ❌ | ❌ |

### FunCaptcha (Arkose Labs)
| Service | Regular | Data (BLOB) | Proxy | Cookies | User-Agent |
| ------------- | :---: | :---:	| :---:	| :---:	| :---:	|
| [2captcha.com](http://2captcha.com/?from=8754088)	| ✅ | ✅ | ✅ | ❌ | ✅ |
| [anti-captcha.com](http://getcaptchasolution.com/vus77mnl48) | ✅ | ✅ | ✅ | ❌ | ✅ |
| [azcaptcha.com](https://azcaptcha.com/) | ❌ | ❌ | ❌ | ❌ | ❌ |
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

### hCaptcha
| Service | Regular | Invisible | Custom Data | Proxy | Cookies | User-Agent |
| ------------- | :---: | :---:	| :---:	| :---:	| :---:	| :---:	|
| [2captcha.com](http://2captcha.com/?from=8754088)	| ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| [anti-captcha.com](http://getcaptchasolution.com/vus77mnl48) | ✅ | ❌ | ❌ | ✅ | ❌ | ✅ |
| [azcaptcha.com](https://azcaptcha.com/) | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| [cptch.net](https://cptch.net/auth/signup?frm=0ebc1ab34eb04f67ac320f020a8f709f) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| [rucaptcha.com](https://rucaptcha.com?from=9863637) | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |

### Capy
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

## How to...
### Common
<details>
<summary><b>Get balance</b></summary>

```python
from unicaps import CaptchaSolver, CaptchaSolvingService

# init captcha solver
solver = CaptchaSolver(CaptchaSolvingService.ANTI_CAPTCHA, "PLACE YOUR API KEY HERE")
balance = solver.get_balance()
```
</details>

<details>
<summary><b>Get service status (is the service is up?)</b></summary>

```python
from unicaps import CaptchaSolver, CaptchaSolvingService

# init captcha solver
solver = CaptchaSolver(CaptchaSolvingService.ANTI_CAPTCHA, "PLACE YOUR API KEY HERE")
# get status of the service (True - everything is Okay, False - the service is down)
status = solver.get_status()
```
</details>

### Solving
<details>
<summary><b>reCAPTCHA v2</b></summary>

```python
from unicaps import CaptchaSolver, CaptchaSolvingService

# get page url and site_key from your page
page_url = ...
site_key = ...

# init captcha solver
solver = CaptchaSolver(CaptchaSolvingService.ANTI_CAPTCHA, "PLACE YOUR API KEY HERE")
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
<summary><b>Invisible reCAPTCHA v2</b></summary>

```python
from unicaps import CaptchaSolver, CaptchaSolvingService

# get page url and site_key from your page
page_url = ...
site_key = ...

# init captcha solver
solver = CaptchaSolver(CaptchaSolvingService.ANTI_CAPTCHA, "PLACE YOUR API KEY HERE")
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
<summary><b>reCAPTCHA v3</b></summary>

```python
from unicaps import CaptchaSolver, CaptchaSolvingService

# get page url, site_key and action from your page
page_url = ...
site_key = ...
action = ...
min_score = 0.7

# init captcha solver
solver = CaptchaSolver(CaptchaSolvingService.ANTI_CAPTCHA, "PLACE YOUR API KEY HERE")
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

## Code examples
[Examples](https://github.com/sergey-scat/unicaps/tree/master/examples)
