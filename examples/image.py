# -*- coding: UTF-8 -*-
"""
Image CAPTCHA solving example
"""

import os

import requests
from lxml import html
from unicaps import CaptchaSolver, CaptchaSolvingService, exceptions
from unicaps.common import CaptchaCharType, CaptchaAlphabet

URL = 'http://democaptcha.com/demo-form-eng/image.html'
API_KEY = os.getenv('API_KEY_2CAPTCHA', default='<PLACE_YOUR_API_KEY_HERE>')


def solve(service_name, api_key):
    """ Get and solve CAPTCHA """

    # init captcha solver
    solver = CaptchaSolver(service_name, api_key)

    # make a session and go to URL
    session = requests.Session()
    response = session.get(URL)

    # parse page and get captcha URL
    page = html.document_fromstring(response.text)
    captcha_url = page.cssselect('#htest_image')[0].attrib['src']

    captcha_response = session.get(captcha_url)

    # parse form data
    page_form_data = page.xpath('//form//input')
    form_data = {}
    for input_data in page_form_data:
        if input_data.xpath('@name'):
            form_data[input_data.xpath('@name')[0]] = next(iter(input_data.xpath('@value')), None)

    # solve reCAPTCHA
    try:
        solved = solver.solve_image_captcha(
            image=captcha_response.content,
            char_type=CaptchaCharType.ALPHANUMERIC,
            is_phrase=False,
            is_case_sensitive=True,
            is_math=False,
            alphabet=CaptchaAlphabet.LATIN
        )
    except exceptions.UnicapsException as exc:
        print('Image CAPTCHA solving exception: %s' % exc)
        return

    # add token to form data
    form_data['vericode'] = solved.solution.text
    form_data['message'] = 'test'

    # post form data
    response = session.post(URL, data=form_data)
    page = html.document_fromstring(response.text)

    # check the result
    if page.xpath('//h2[text()="Your message has been sent (actually not), thank you!"]'):
        print('Image CAPTCHA solved successfully!')
        # report good CAPTCHA
        solved.report_good()
    else:
        print('Image CAPTCHA wasn\'t solved!')
        # report bad CAPTCHA
        solved.report_bad()


if __name__ == '__main__':
    solve(CaptchaSolvingService.TWOCAPTCHA, API_KEY)
