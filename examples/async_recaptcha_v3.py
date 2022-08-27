# -*- coding: UTF-8 -*-
"""
reCAPTCHA v3 solving example
"""

import asyncio
import os
import re
from pprint import pprint

import httpx
from unicaps import AsyncCaptchaSolver, CaptchaSolvingService, exceptions  # type: ignore

URL = 'https://recaptcha-demo.appspot.com/recaptcha-v3-request-scores.php'
VERIFY_URL = ('https://recaptcha-demo.appspot.com/recaptcha-v3-verify.php'
              '?action={action}&token={token}')
MIN_SCORE = 0.7
API_KEY = os.getenv('API_KEY_2CAPTCHA', default='<PLACE_YOUR_API_KEY_HERE>')


async def run(solver):
    """ Get and solve CAPTCHA """

    # make a session and go to URL
    session = httpx.AsyncClient(http2=True)
    response = await session.get(URL)

    # extract site-key and action from the page source using regular expression
    regexp = re.search(
        r"grecaptcha.execute\('([a-zA-Z0-9\-_]{40})', ?\{action: ?'(.*)'\}\)'",
        response.text
    )
    site_key = regexp.group(1)
    action = regexp.group(2)

    # solve reCAPTCHA
    try:
        solved = await solver.solve_recaptcha_v3(
            site_key=site_key,
            page_url=URL,
            action=action,
            min_score=MIN_SCORE
        )
    except exceptions.UnicapsException as exc:
        print(f'reCAPTCHA v3 solving exception: {str(exc)}')
        return False, None

    # verify token and print the result
    response = await session.get(
        VERIFY_URL.format(
            action=action,
            token=solved.solution.token
        )
    )
    result = response.json()
    pprint(result)

    # check the result
    if not result['score']:
        print('reCAPTCHA v3 wasn\'t solved! Error codes: ' + ', '.join(result['error-codes']))
        # report bad CAPTCHA
        await solved.report_bad()
        return False, solved

    if result['score'] < MIN_SCORE:
        print(
            f'Solved reCAPTCHA v3 score ({result["score"]}) is less than requested ({MIN_SCORE})!'
        )
        # report bad CAPTCHA
        await solved.report_bad()
        return False, solved

    print('reCAPTCHA v3 has been solved successfully!')
    # report good CAPTCHA
    await solved.report_good()
    return True, solved


if __name__ == '__main__':
    asyncio.run(
        run(
            AsyncCaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, API_KEY)
        )
    )
