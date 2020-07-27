# -*- coding: UTF-8 -*-
"""
reCAPTCHA v2 invisible solving example
"""

import os

import requests
from lxml import html
from unicaps import CaptchaSolver, exceptions

URL = 'https://recaptcha-demo.appspot.com/recaptcha-v2-invisible.php'
API_KEY = os.getenv('2CAPTCHA_API_KEY', default='YOUR_API_KEY')


def solve(service_name, api_key):
    """ Get and solve CAPTCHA """

    # init captcha solver
    solver = CaptchaSolver(service_name, api_key)

    # make a session and go to URL
    session = requests.Session()
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
        return

    # add token to form data
    form_data['g-recaptcha-response'] = solved.solution.token

    # post form data
    response = session.post(URL, data=form_data)
    page = html.document_fromstring(response.text)

    # check the result
    if page.xpath('//h2[text()="Success!"]'):
        print('Invisible reCAPTCHA v2 solved successfully!')
        # report good CAPTCHA
        solved.report_good()
    else:
        print('Invisible reCAPTCHA v2 wasn\'t solved!')
        # report bad CAPTCHA
        solved.report_bad()


if __name__ == '__main__':
    solve('2captcha.com', API_KEY)
