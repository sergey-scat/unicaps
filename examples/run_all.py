# -*- coding: UTF-8 -*-
"""
All examples runner
"""

from importlib import import_module
import logging
import os
import sys

# services dict: key is a name of CAPTCHA solving service, value is an env variable containing
# the API key
SERVICES = {
    '2captcha.com': '2CAPTCHA_API_KEY',
    'anti-captcha.com': 'ANTICAPTCHA_API_KEY',
    'azcaptcha.com': 'AZCAPTCHA_API_KEY',
    'cptch.net': 'CPTCH_NET_API_KEY'
}

# list of modules containing CAPTCHA solving examples
EXAMPLES = [
    'image',
    'recaptcha_v2',
    'recaptcha_v2_invisible',
    'recaptcha_v2_proxy',
    'recaptcha_v3',
    'hcaptcha'
]

logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    for service_name in SERVICES:
        api_key = os.getenv(SERVICES[service_name])
        print(f'######### Service: {service_name} #########')

        for example in EXAMPLES:
            module = import_module(example)
            module.solve(service_name, api_key)
