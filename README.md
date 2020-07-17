<p align="center">
  <img src="https://i.imgur.com/8aQf6On.png" />
</p>

# Unicaps
[![](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20-blue.svg)](https://www.python.org/downloads/release/python-3611/)

Unicaps is a unified Python API for CAPTCHA solving services.


⚠ **PLEASE NOTE**</br>
⚠ A solving service API key is required to use this package!</br>
⚠ The list of the supported services you can find in the table below.


## Key Features
 - A unified Python interface that is independent of the service used
 - Uses native service protocol/endpoints (eg, no needs in patching _hosts_ file)
 - Supports 9 types of CAPTCHAs
 - Supports 3 CAPTCHA solving services (5 more would be added soon)
 - Written Pythonic way and is intended for humans
 
## Simple Usage Example
```python
>>> from unicaps import CaptchaSolver
>>> solver = CaptchaSolver("2captcha.com", api_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
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
| CAPTCHA➡ \ Service⬇| Image | Text | [reCAPTCHA v2](https://developers.google.com/recaptcha/docs/display) | [reCAPTCHA v3](https://developers.google.com/recaptcha/docs/v3) | [FunCaptcha](https://funcaptcha.com/fc/api/nojs/?pkey=69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC) | [KeyCAPTCHA](https://www.keycaptcha.com/) | [Geetest](https://www.geetest.com/en/demo) | [hCaptcha](https://www.hcaptcha.com/) | [Capy](https://www.capy.me/) |
| ------------- | :---: | :---:	| :---:	| :---:	| :---:	| :---:	| :---:	| :---:	| :---:	|
| [2captcha.com](http://2captcha.com/?from=8754088)	| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| [anti-captcha.com](http://getcaptchasolution.com/vus77mnl48) | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ |
| [rucaptcha.com](https://rucaptcha.com?from=9863637) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

## Code examples
[Examples](https://github.com/sergey-scat/unicaps/examples)
