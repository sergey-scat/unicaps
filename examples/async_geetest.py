"""
GeeTest solving example
"""

import asyncio
import os
import time

import httpx
from unicaps import AsyncCaptchaSolver, CaptchaSolvingService, exceptions  # type: ignore

URL = 'https://2captcha.com/demo/geetest'
INIT_PARAMS_URL = 'https://2captcha.com/api/v1/captcha-demo/gee-test/init-params?t={ms}'
URL_VERIFY = 'https://2captcha.com/api/v1/captcha-demo/gee-test/verify'
API_KEY = os.getenv('API_KEY_2CAPTCHA', default='YOUR_API_KEY')


async def run(solver):
    """ Solve GeeTest """

    # create an HTTP2 session
    session = httpx.AsyncClient(http2=True)

    # open page and extract CAPTCHA URL
    response = await session.get(INIT_PARAMS_URL.format(ms=int(time.time() * 1000)))
    init_params = response.json()

    # solve GeeTest
    try:
        solved = await solver.solve_geetest(
            page_url=URL,
            gt_key=init_params['gt'],
            challenge=init_params['challenge']
        )
    except exceptions.UnicapsException as exc:
        print(f'GeeTest solving exception: {str(exc)}')
        return False, None

    # post solved captcha token
    response = await session.post(
        URL_VERIFY,
        json={
            'geetest_challenge': solved.solution.challenge,
            'geetest_seccode': solved.solution.seccode,
            'geetest_validate': solved.solution.validate
        }
    )

    # check the result
    if response.json().get('success'):
        print('GeeTest has been solved successfully!')
        # report good CAPTCHA
        await solved.report_good()
        return True, solved

    print('GeeTest wasn\'t solved!')
    # report bad CAPTCHA
    await solved.report_bad()
    return False, solved


if __name__ == '__main__':
    asyncio.run(
        run(
            AsyncCaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, API_KEY)
        )
    )
