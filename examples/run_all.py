# -*- coding: UTF-8 -*-
"""
All examples runner
"""

from importlib import import_module
import logging
import os

# services dict: key is a name of CAPTCHA solving service, value is an env variable containing
# the API key
SERVICES = {
    '2captcha.com': 'API_KEY_2CAPTCHA',
    'anti-captcha.com': 'API_KEY_ANTICAPTCHA',
    'azcaptcha.com': 'API_KEY_AZCAPTCHA',
    'cptch.net': 'API_KEY_CPTCH_NET'
}

# list of modules containing CAPTCHA solving examples
EXAMPLES = [
    'image',
    'recaptcha_v2',
    'recaptcha_v2_invisible',
    'recaptcha_v2_proxy',
    'recaptcha_v2_enterprise',
    'recaptcha_v3',
    'hcaptcha'
]

logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    for service_name in SERVICES:
        api_key = os.getenv(SERVICES[service_name])
        print(f'######### Service: {service_name} #########')

        for example_name in EXAMPLES:
            print(example_name)
            module = import_module(example_name)
            module.solve(service_name, api_key)
            print()
