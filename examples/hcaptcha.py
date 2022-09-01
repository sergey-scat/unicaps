# -*- coding: UTF-8 -*-
"""
hCaptcha solving example
"""

import os

import httpx
from lxml import html  # type: ignore
from unicaps import CaptchaSolver, CaptchaSolvingService, exceptions  # type: ignore

URL = 'https://democaptcha.com/demo-form-eng/hcaptcha.html'
API_KEY = os.getenv('API_KEY_2CAPTCHA', default='YOUR_API_KEY')


def run(solver):
    """ Solve hCaptcha """

    # make a session and go to URL
    with httpx.Client(http2=True) as session:
        response = session.get(URL)

        # parse page and get site-key
        page = html.document_fromstring(response.text)
        site_key = page.cssselect('.h-captcha')[0].attrib['data-sitekey']

        # parse form data
        page_form_data = page.xpath('//form//input')
        form_data = {}
        for input_data in page_form_data:
            if input_data.xpath('@name'):
                form_data[input_data.xpath('@name')[0]] = next(
                    iter(input_data.xpath('@value')),
                    None
                )

        # solve hCaptcha
        try:
            solved = solver.solve_hcaptcha(
                site_key=site_key,
                page_url=URL
            )
        except exceptions.UnicapsException as exc:
            print(f'hCaptcha solving exception: {str(exc)}')
            return False, None

        # add token to form data
        form_data['h-captcha-response'] = solved.solution.token
        form_data['g-recaptcha-response'] = solved.solution.token

        # post form data
        response = session.post(URL, data=form_data)
        page = html.document_fromstring(response.text)

    # check the result
    if page.xpath('//h2[starts-with(text(), "Thank you")]'):
        print('The hCaptcha has been solved correctly!')
        # report good CAPTCHA
        solved.report_good()
        return True, solved

    print('The hCaptcha has not been solved correctly!')
    # report bad CAPTCHA
    solved.report_bad()
    return False, solved


if __name__ == '__main__':
    with CaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, API_KEY) as captcha_solver:
        run(captcha_solver)
