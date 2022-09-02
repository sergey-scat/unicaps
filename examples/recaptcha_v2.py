# -*- coding: UTF-8 -*-
"""
reCAPTCHA v2 solving example
"""

import os

import httpx
from lxml import html  # type: ignore
from unicaps import CaptchaSolver, CaptchaSolvingService, exceptions  # type: ignore

URL = 'https://recaptcha-demo.appspot.com/recaptcha-v2-checkbox.php'
API_KEY = os.getenv('API_KEY_2CAPTCHA', default='<PLACE_YOUR_API_KEY_HERE>')


def run(solver):
    """ Get and solve reCAPTCHA v2 """

    # make a session and go to URL
    with httpx.Client(http2=True) as session:
        response = session.get(URL)

        # parse page and get data-sitekey value
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
                page_url=URL
            )
        except exceptions.UnicapsException as exc:
            print(f'reCAPTCHA v2 solving exception: {str(exc)}')
            return False, None

        # add token to form data
        form_data['g-recaptcha-response'] = solved.solution.token

        # post form data
        response = session.post(URL, data=form_data)
        page = html.document_fromstring(response.text)

    # check the result
    if page.xpath('//h2[text()="Success!"]'):
        print('The reCAPTCHA v2 has been solved correctly!')
        # report good CAPTCHA
        solved.report_good()
        return True, solved

    print('The reCAPTCHA v2 has not been solved correctly!')
    # report bad CAPTCHA
    solved.report_bad()
    return False, solved


if __name__ == '__main__':
    with CaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, API_KEY) as captcha_solver:
        run(captcha_solver)
