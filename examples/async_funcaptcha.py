"""
FunCaptcha solving example
"""

import asyncio
import os
import re

import httpx
from lxml import html  # type: ignore
from unicaps import AsyncCaptchaSolver, CaptchaSolvingService, exceptions  # type: ignore

URL = 'https://client-demo.arkoselabs.com/solo-animals'
URL_VERIFY = 'https://client-demo.arkoselabs.com/solo-animals/verify'
API_KEY = os.getenv('API_KEY_2CAPTCHA', default='<PLACE_YOUR_API_KEY_HERE>')


async def main():
    """ Init AsyncCaptchaSolver and run the example """
    async with AsyncCaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, API_KEY) as solver:
        await run(solver)


async def run(solver):
    """ Load and solve FunCaptcha """

    # create an HTTP2 session
    async with httpx.AsyncClient(http2=True) as session:
        # open page and extract CAPTCHA URL
        response = await session.get(URL)
        page = html.document_fromstring(response.text)

        # extract Public Key and Service URL values
        script = page.xpath('//script[contains(text(), "public_key")]')[0].text
        regexp = re.search(
            r'public_key: ?"([0-9A-Z-]+)",\s*surl: ?"(.*)",',
            script
        )
        public_key = regexp.group(1)
        service_url = regexp.group(2)

        # solve FunCaptcha
        try:
            solved = await solver.solve_funcaptcha(
                public_key=public_key,
                page_url=URL,
                service_url=service_url
            )
        except exceptions.UnicapsException as exc:
            print(f'FunCaptcha solving exception: {str(exc)}')
            return False, None

        # post solved captcha token
        response = await session.post(
            URL_VERIFY,
            data={
                'name': 'test',
                'verification-token': solved.solution.token,
                'fc-token': solved.solution.token
            }
        )

    # check the result
    if '<h3>Solved!</h3>' in response.text:
        print('The FunCaptcha has been solved correctly!')
        # report good CAPTCHA
        await solved.report_good()
        return True, solved

    print('The FunCaptcha has not been solved correctly!')
    # report bad CAPTCHA
    await solved.report_bad()
    return False, solved


if __name__ == '__main__':
    asyncio.run(main())
