# -*- coding: UTF-8 -*-
"""
hCaptcha solving example
"""

import os

import requests
from lxml import html
from unicaps import CaptchaSolver, exceptions

URL = 'http://democaptcha.com/demo-form-eng/hcaptcha.html'
API_KEY = os.getenv('2CAPTCHA_API_KEY', default='YOUR_API_KEY')


def solve(service_name, api_key):
    # init captcha solver
    solver = CaptchaSolver(service_name, api_key)

    # make a session and go to URL
    session = requests.Session()
    response = session.get(URL)

    # parse page and get site-key
    page = html.document_fromstring(response.text)
    site_key = page.cssselect('.h-captcha')[0].attrib['data-sitekey']

    # parse form data
    page_form_data = page.xpath('//form//input')
    form_data = {}
    for input_data in page_form_data:
        if input_data.xpath('@name'):
            form_data[input_data.xpath('@name')[0]] = next(iter(input_data.xpath('@value')), None)

    # solve hCaptcha
    try:
        solved = solver.solve_hcaptcha(
            site_key=site_key,
            page_url=URL
        )
    except exceptions.UnicapsException as exc:
        print('hCaptcha solving exception: %s' % exc)
        return

    # add token to form data
    form_data['h-captcha-response'] = solved.solution.token
    form_data['g-recaptcha-response'] = solved.solution.token

    # post form data
    response = session.post(URL, data=form_data)
    page = html.document_fromstring(response.text)

    # check the result
    if page.xpath('//h2[starts-with(text(), "Thank you")]'):
        print('hCaptcha solved successfully!')
        # report good CAPTCHA
        solved.report_good()
    else:
        print('hCaptcha wasn\'t solved!')
        # report bad CAPTCHA
        solved.report_bad()


if __name__ == '__main__':
    solve('2captcha.com', API_KEY)
