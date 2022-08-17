# -*- coding: UTF-8 -*-
"""
reCAPTCHA v2 invisible solving example
"""

import os

import httpx
from lxml import html
from unicaps import CaptchaSolver, CaptchaSolvingService, exceptions

URL = 'https://recaptcha-demo.appspot.com/recaptcha-v2-invisible.php'
API_KEY = os.getenv('API_KEY_2CAPTCHA', default='<PLACE_YOUR_API_KEY_HERE>')


def run(solver):
    """ Get and solve reCAPTCHA v2 invisible """

    # make a session and go to URL
    session = httpx.Client(http2=True)
    response = session.get(URL)

    # parse page and get site-key
    page = html.document_fromstring(response.text)
    site_key = page.cssselect('.g-recaptcha')[0].attrib['data-sitekey']

    # parse form data
    page_form_data = page.xpath('//form//input')
    form_data = {}
    for input_data in page_form_data:
        form_data[input_data.xpath('@name')[0]] = input_data.xpath('@value')[0]

    # solve reCAPTCHA
    try:
        solved = solver.solve_recaptcha_v2(
            site_key=site_key,
            page_url=URL,
            is_invisible=True
        )
    except exceptions.UnicapsException as exc:
        print('reCAPTCHA v2 (invisible) solving exception: %s' % exc)
        return False, None

    # add token to form data
    form_data['g-recaptcha-response'] = solved.solution.token

    # post form data
    response = session.post(URL, data=form_data)
    page = html.document_fromstring(response.text)

    # check the result
    if page.xpath('//h2[text()="Success!"]'):
        print('Invisible reCAPTCHA v2 has been solved successfully!')
        # report good CAPTCHA
        solved.report_good()
        return True, solved
    else:
        print('Invisible reCAPTCHA v2 wasn\'t solved!')
        # report bad CAPTCHA
        solved.report_bad()
        return False, solved


if __name__ == '__main__':
    solver = CaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, API_KEY)
    run(solver)
