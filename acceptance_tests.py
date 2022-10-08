"""
Acceptance tests
"""

import asyncio
import logging
import os
from importlib import import_module

from unicaps import CaptchaSolver, AsyncCaptchaSolver
from unicaps.__version__ import __version__

logging.basicConfig(level=logging.INFO)

SERVICES = {
    '2captcha.com': 'API_KEY_2CAPTCHA',
    'anti-captcha.com': 'API_KEY_ANTICAPTCHA',
    'azcaptcha.com': 'API_KEY_AZCAPTCHA',
    'captcha.guru': 'API_KEY_CAPTCHA_GURU',
    'cptch.net': 'API_KEY_CPTCH_NET'
}

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


def main():
    for service_name, env_var_name in SERVICES.items():
        api_key = os.getenv(env_var_name)
        if not api_key:
            logging.error(
                'Unable to read API key for the "%s" service. '
                'The environment variable "%s" doesn\'t exist!',
                service_name,
                env_var_name
            )
            continue

        logging.info('######### Service: %s #########', service_name)

        with CaptchaSolver(service_name, api_key) as solver:
            status = solver.get_status()
            balance = solver.get_balance()
            logging.info('Status: %s.  Balance: %.2f', 'OK' if status else 'ERROR', balance)

            for example_name in EXAMPLES:
                logging.info('Current module: %s', example_name)
                module = import_module(f'examples.{example_name}')
                try:
                    module.run(solver)
                except Exception:
                    logging.exception('%s run exception', module)


async def async_main():
    for service_name, env_var_name in SERVICES.items():
        api_key = os.getenv(env_var_name)
        if not api_key:
            logging.error(
                'Unable to read API key for the "%s" service. '
                'The environment variable "%s" doesn\'t exist!',
                service_name,
                env_var_name
            )
            continue

        logging.info('######### Service: %s #########', service_name)
        async with AsyncCaptchaSolver(service_name, api_key) as async_solver:
            status = await async_solver.get_status()
            balance = await async_solver.get_balance()
            logging.info(
                'Status: %s.  Balance: %.2f',
                'OK' if status else 'ERROR',
                balance
            )

            for example_name in EXAMPLES:
                logging.info('Current module: %s', example_name)
                module = import_module(f'examples.async_{example_name}')
                try:
                    await module.run(async_solver)
                except Exception:
                    logging.exception('%s run exception', module)


if __name__ == '__main__':
    main()
    asyncio.run(async_main(), debug=False)
