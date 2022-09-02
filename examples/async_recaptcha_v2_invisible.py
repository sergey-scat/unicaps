# -*- coding: UTF-8 -*-
"""
reCAPTCHA v2 invisible solving example
"""

import asyncio
import os

import httpx
from lxml import html  # type: ignore
from unicaps import AsyncCaptchaSolver, CaptchaSolvingService, exceptions  # type: ignore

URL = 'https://recaptcha-demo.appspot.com/recaptcha-v2-invisible.php'
API_KEY = os.getenv('API_KEY_2CAPTCHA', default='<PLACE_YOUR_API_KEY_HERE>')


async def main():
    """ Init AsyncCaptchaSolver and run the example """
    async with AsyncCaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, API_KEY) as solver:
        await run(solver)


async def run(solver):
    """ Get and solve reCAPTCHA v2 invisible """

    # make a session and go to URL
    async with httpx.AsyncClient(http2=True) as session:
        response = await session.get(URL)

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
            solved = await solver.solve_recaptcha_v2(
                site_key=site_key,
                page_url=URL,
                is_invisible=True
            )
        except exceptions.UnicapsException as exc:
            print(f'reCAPTCHA v2 (invisible) solving exception: {str(exc)}')
            return False, None

        # add token to form data
        form_data['g-recaptcha-response'] = solved.solution.token

        # post form data
        response = await session.post(URL, data=form_data)
        page = html.document_fromstring(response.text)

    # check the result
    if page.xpath('//h2[text()="Success!"]'):
        print('The Invisible reCAPTCHA v2 has been solved correctly!')
        # report good CAPTCHA
        await solved.report_good()
        return True, solved

    print('The Invisible reCAPTCHA v2 has not been solved correctly!')
    # report bad CAPTCHA
    await solved.report_bad()
    return False, solved


if __name__ == '__main__':
    asyncio.run(main())
