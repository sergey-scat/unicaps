"""
KeyCaptcha solving example
"""

import os
import re
from urllib.parse import urljoin

import httpx
from lxml import html  # type: ignore
from unicaps import CaptchaSolver, CaptchaSolvingService, exceptions  # type: ignore

URL = 'https://2captcha.com/demo/keycaptcha'
URL_VERIFY = 'https://2captcha.com/api/v1/captcha-demo/key-captcha/verify'
API_KEY = os.getenv('API_KEY_2CAPTCHA', default='YOUR_API_KEY')


def run(solver):
    """ Get and solve KeyCaptcha """

    # create an HTTP2 session
    with httpx.Client(http2=True) as session:
        # open page and extract CAPTCHA URL
        response = session.get(URL)
        page = html.document_fromstring(response.text)

        # extract captcha URL, parse page and get captcha params
        captcha_url = page.xpath('//iframe[@name="key-captcha-widget"]')[0].attrib['src']
        captcha_url = urljoin(URL, captcha_url)
        response = session.get(captcha_url)
        captcha_page = html.document_fromstring(response.text)
        script = captcha_page.xpath('//script[contains(text(), "var s_s_c_user_id")]')[0].text

        def extract_var_value(var_name):
            return re.search(fr"var {var_name} = '(.+)';", script).group(1)

        s_s_c_user_id = extract_var_value('s_s_c_user_id')
        s_s_c_session_id = extract_var_value('s_s_c_session_id')
        s_s_c_web_server_sign = extract_var_value('s_s_c_web_server_sign')
        s_s_c_web_server_sign2 = extract_var_value('s_s_c_web_server_sign2')

        # solve KeyCaptcha
        try:
            solved = solver.solve_keycaptcha(
                page_url=URL,
                user_id=s_s_c_user_id,
                session_id=s_s_c_session_id,
                ws_sign=s_s_c_web_server_sign,
                ws_sign2=s_s_c_web_server_sign2
            )
        except exceptions.UnicapsException as exc:
            print(f'KeyCaptcha solving exception: {str(exc)}')
            return False, None

        # post solved captcha token
        response = session.post(
            URL_VERIFY,
            json={'capcode': solved.solution.token}
        )

    # check the result
    if response.json().get('success'):
        print('The KeyCaptcha has been solved correctly!')
        # report good CAPTCHA
        solved.report_good()
        return True, solved

    print('The KeyCaptcha has not been solved correctly!')
    # report bad CAPTCHA
    solved.report_bad()
    return False, solved


if __name__ == '__main__':
    with CaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, API_KEY) as captcha_solver:
        run(captcha_solver)
