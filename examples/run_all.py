# -*- coding: UTF-8 -*-
"""
All examples runner
"""

from importlib import import_module
import logging
import os

from unicaps import CaptchaSolver  # type: ignore

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
    'recaptcha_v2_enterprise',
    'recaptcha_v3',
    'hcaptcha',
    'keycaptcha',
    'geetest',
    'geetest_v4',
    'capy_puzzle',
    'text',
    'funcaptcha'
]

logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    for service_name, env_var_name in SERVICES.items():
        api_key = os.getenv(env_var_name)
        print(f'######### Service: {service_name} #########')

        # init captcha solver
        with CaptchaSolver(service_name, api_key) as solver:
            for example_name in EXAMPLES:
                print(example_name)
                module = import_module(example_name)
                module.run(solver)
                print()
