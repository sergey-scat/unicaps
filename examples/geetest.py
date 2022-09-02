"""
GeeTest solving example
"""

import os
import time

import httpx
from unicaps import CaptchaSolver, CaptchaSolvingService, exceptions  # type: ignore

URL = 'https://2captcha.com/demo/geetest'
INIT_PARAMS_URL = 'https://2captcha.com/api/v1/captcha-demo/gee-test/init-params?t={ms}'
URL_VERIFY = 'https://2captcha.com/api/v1/captcha-demo/gee-test/verify'
API_KEY = os.getenv('API_KEY_2CAPTCHA', default='<PLACE_YOUR_API_KEY_HERE>')


def run(solver):
    """ Solve GeeTest """

    # create an HTTP2 session
    with httpx.Client(http2=True) as session:
        # open page and extract CAPTCHA URL
        response = session.get(INIT_PARAMS_URL.format(ms=int(time.time() * 1000)))
        init_params = response.json()

        # solve GeeTest
        try:
            solved = solver.solve_geetest(
                page_url=URL,
                gt_key=init_params['gt'],
                challenge=init_params['challenge']
            )
        except exceptions.UnicapsException as exc:
            print(f'GeeTest solving exception: {str(exc)}')
            return False, None

        # post solved captcha token
        response = session.post(
            URL_VERIFY,
            json={
                'geetest_challenge': solved.solution.challenge,
                'geetest_seccode': solved.solution.seccode,
                'geetest_validate': solved.solution.validate
            }
        )

    # check the result
    if response.json().get('success'):
        print('The GeeTest has been solved correctly!')
        # report good CAPTCHA
        solved.report_good()
        return True, solved

    print('The GeeTest has not been solved correctly!')
    # report bad CAPTCHA
    solved.report_bad()
    return False, solved


if __name__ == '__main__':
    with CaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, API_KEY) as captcha_solver:
        run(captcha_solver)
