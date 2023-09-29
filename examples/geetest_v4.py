"""
GeeTest solving example
"""

import os
import re
from urllib.parse import urljoin

import httpx
from lxml import html  # type: ignore
from unicaps import CaptchaSolver, CaptchaSolvingService, exceptions  # type: ignore

URL = 'https://2captcha.com/demo/geetest-v4'
URL_VERIFY = 'https://2captcha.com/api/v1/captcha-demo/gee-test-v4/verify'
API_KEY = os.getenv('API_KEY_2CAPTCHA', default='<PLACE_YOUR_API_KEY_HERE>')


def run(solver):
    """ Solve GeeTest v4 """

    # create an HTTP2 session
    with httpx.Client(http2=True) as session:
        # open page and extract pages-CaptchaDemo URL
        response = session.get(URL)
        page = html.document_fromstring(response.text)
        captcha_js_url = page.xpath(
            '//script[@data-chunk="pages-CaptchaDemo-pages-GeeTestV4" and '
            'starts-with(@src, "/dist/web/pages-CaptchaDemo-pages-GeeTestV4.")]'
        )[0].attrib['src']
        captcha_js_url = urljoin(URL, captcha_js_url)

        # load pages-CaptchaDemo js-file and extract captcha ID
        response = session.get(captcha_js_url)
        regexp = re.search(
            r'window\.initGeetest4\(\{\s*captchaId:\s?"([0-9a-z]+)"',
            response.text
        )

        # solve GeeTest v4
        try:
            solved = solver.solve_geetest_v4(
                page_url=URL,
                captcha_id=regexp.group(1)
            )
        except exceptions.UnicapsException as exc:
            print(f'GeeTestV4 solving exception: {str(exc)}')
            return False, None

        # post solved captcha token
        response = session.post(
            URL_VERIFY,
            json={
                'captcha_id': solved.solution.captcha_id,
                'lot_number': solved.solution.lot_number,
                'pass_token': solved.solution.pass_token,
                'gen_time': solved.solution.gen_time,
                'captcha_output': solved.solution.captcha_output
            }
        )

    # check the result
    if response.json().get('result') == 'success':
        print('The GeeTest v4 has been solved correctly!')
        # report good CAPTCHA
        solved.report_good()
        return True, solved

    print('The GeeTest v4 has not been solved correctly!')
    # report bad CAPTCHA
    solved.report_bad()
    return False, solved


if __name__ == '__main__':
    with CaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, API_KEY) as captcha_solver:
        run(captcha_solver)
