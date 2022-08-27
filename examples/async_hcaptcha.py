# -*- coding: UTF-8 -*-
"""
hCaptcha solving example
"""

import asyncio
import os

import httpx
from lxml import html  # type: ignore
from unicaps import AsyncCaptchaSolver, CaptchaSolvingService, exceptions  # type: ignore

URL = 'https://democaptcha.com/demo-form-eng/hcaptcha.html'
API_KEY = os.getenv('API_KEY_2CAPTCHA', default='YOUR_API_KEY')


async def run(solver):
    """ Solve hCaptcha """

    # make a session and go to URL
    session = httpx.AsyncClient(http2=True)
    response = await session.get(URL)

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
        solved = await solver.solve_hcaptcha(
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
    response = await session.post(URL, data=form_data)
    page = html.document_fromstring(response.text)

    # check the result
    if page.xpath('//h2[starts-with(text(), "Thank you")]'):
        print('hCaptcha has been solved successfully!')
        # report good CAPTCHA
        await solved.report_good()
        return True, solved

    print('hCaptcha wasn\'t solved!')
    # report bad CAPTCHA
    await solved.report_bad()
    return False, solved


if __name__ == '__main__':
    asyncio.run(
        run(
            AsyncCaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, API_KEY)
        )
    )
