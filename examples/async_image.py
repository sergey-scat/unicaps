# -*- coding: UTF-8 -*-
"""
Image CAPTCHA solving example
"""

import asyncio
import os

import httpx
from lxml import html  # type: ignore
from unicaps import AsyncCaptchaSolver, CaptchaSolvingService, exceptions  # type: ignore
from unicaps.common import CaptchaCharType, CaptchaAlphabet  # type: ignore

URL = 'https://democaptcha.com/demo-form-eng/image.html'
API_KEY = os.getenv('API_KEY_2CAPTCHA', default='<PLACE_YOUR_API_KEY_HERE>')


async def main():
    """ Init AsyncCaptchaSolver and run the example """

    async with AsyncCaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, API_KEY) as solver:
        await run(solver)


async def run(solver):
    """ Solve image CAPTCHA """

    # make a session and go to URL
    async with httpx.AsyncClient(http2=True) as session:
        response = await session.get(URL)

        # parse page and get captcha URL
        page = html.document_fromstring(response.text)

        # fetch captcha image
        captcha_url = page.cssselect('#htest_image')[0].attrib['src']
        captcha_response = await session.get(captcha_url)

        # solve the captcha
        try:
            solved = await solver.solve_image_captcha(
                image=captcha_response.content,  # binary image data
                char_type=CaptchaCharType.ALPHANUMERIC,  # consists of alphanumeric characters
                is_phrase=False,  # not a phrase (no whitespaces)
                is_case_sensitive=True,  # case-sensitive text
                is_math=False,  # no calculation needed
                alphabet=CaptchaAlphabet.LATIN  # latin alphabet being used
            )
        except exceptions.UnicapsException as exc:
            print(f'Image CAPTCHA solving exception: {str(exc)}')
            return False, None

        form_data = {}
        # parse form data
        page_form_data = page.xpath('//form//input')
        for input_data in page_form_data:
            if input_data.xpath('@name'):
                form_data[str(input_data.xpath('@name')[0])] = str(
                    next(iter(input_data.xpath('@value')), None)
                )

        form_data['message'] = 'test'
        # add token to form data
        form_data['vericode'] = solved.solution.text

        # post form data and parse result page
        response = await session.post(URL, data=form_data)
        page = html.document_fromstring(response.text)

    # check the result
    if page.xpath('//h2[text()="Your message has been sent (actually not), thank you!"]'):
        print('The Image CAPTCHA has been solved correctly!')
        # report good CAPTCHA
        await solved.report_good()
        return True, solved

    print('The Image CAPTCHA has not been solved correctly!')
    # report bad CAPTCHA
    await solved.report_bad()
    return False, solved


if __name__ == '__main__':
    asyncio.run(main())
