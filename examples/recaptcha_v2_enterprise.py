# -*- coding: UTF-8 -*-
"""
reCAPTCHA v2 Enterprise solving example
"""

import os
import random
import string

import httpx
from unicaps import CaptchaSolver, CaptchaSolvingService, exceptions
from unicaps.proxy import ProxyServer

URL = 'https://store.steampowered.com/join'
URL_REFRESH_CAPTCHA = 'https://store.steampowered.com/join/refreshcaptcha/'
URL_VERIFY_EMAIL = 'https://store.steampowered.com/join/ajaxverifyemail'
API_KEY_2CAPTCHA = os.getenv('API_KEY_2CAPTCHA', default='<PLACE_YOUR_API_KEY_HERE>')
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
PROXY = os.getenv(
    'HTTP_PROXY_SERVER',
    default='http://<LOGIN>:<PASSWORD>@<PROXY_ADDRESS>:<PORT>'
)


def get_random_word(length):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))


def run(solver):
    """ Get and solve CAPTCHA """

    # make a session, update headers and proxies
    session = httpx.Client(proxies=PROXY)
    session.headers.update({
        'User-Agent': USER_AGENT,
    })
    #session.proxies.update({
        #'http': PROXY,
        #'https': PROXY
    #})

    # open the "Join" page just to get session cookies
    response = session.get(URL)

    # get reCAPTCHA params
    captcha_params = session.post(
        URL_REFRESH_CAPTCHA,
        data=dict(count=1)
    ).json()

    # solve reCAPTCHA
    try:
        solved = solver.solve_recaptcha_v2(
            site_key=captcha_params['sitekey'],
            page_url=URL,
            data_s=captcha_params['s'],
            is_enterprise=True,
            proxy=ProxyServer(PROXY),
            user_agent=USER_AGENT,
            cookies=dict(session.cookies)
        )
    except exceptions.UnicapsException as exc:
        print('reCAPTCHA v2 Enterprise solving exception: %s' % exc)
        return False, None

    # generate email address
    email = f'random_{get_random_word(10)}@gmail.com'

    # verify email
    response = session.post(
        URL_VERIFY_EMAIL,
        data=dict(
            email=email,
            captchagid=captcha_params['gid'],
            captcha_text=solved.solution.token,
            elang=0
        )
    )
    response_data = response.json()

    print(f"Email: {email}\nResult: {response_data['details']}")

    # check the result
    if 'the CAPTCHA appears to be invalid' not in response_data['details']:
        print('reCAPTCHA v2 Enterprise has been solved successfully!')
        # report good CAPTCHA
        solved.report_good()
        return True, solved
    else:
        print('reCAPTCHA v2 Enterprise wasn\'t solved!')
        # report bad CAPTCHA
        solved.report_bad()
        return False, solved


if __name__ == '__main__':
    solver = CaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, API_KEY)
    run(solver)
