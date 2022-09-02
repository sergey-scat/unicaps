"""
GeeTest v4 solving example
"""

import asyncio
import os
import re
from urllib.parse import urljoin

import httpx
from lxml import html  # type: ignore
from unicaps import AsyncCaptchaSolver, CaptchaSolvingService, exceptions  # type: ignore

URL = 'https://2captcha.com/demo/geetest-v4'
URL_VERIFY = 'https://2captcha.com/api/v1/captcha-demo/gee-test-v4/verify'
API_KEY = os.getenv('API_KEY_2CAPTCHA', default='<PLACE_YOUR_API_KEY_HERE>')


async def main():
    """ Init AsyncCaptchaSolver and run the example """
    async with AsyncCaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, API_KEY) as solver:
        await run(solver)


async def run(solver):
    """ Solve GeeTest v4 """

    # create an HTTP2 session
    async with httpx.AsyncClient(http2=True) as session:
        # open page and extract CAPTCHA URL
        response = await session.get(URL)
        page = html.document_fromstring(response.text)
        captcha_js_url = page.xpath(
            '//script[@data-chunk="pages-CaptchaDemo" and '
            'starts-with(@src, "/dist/web/pages-CaptchaDemo.")]'
        )[0].attrib['src']
        captcha_js_url = urljoin(URL, captcha_js_url)

        # load pages-CaptchaDemo js-file and extract captcha ID
        response = await session.get(captcha_js_url)
        regexp = re.search(
            r'window\.initGeetest4\(\{\s*captchaId:\s?"([0-9a-z]+)"',
            response.text
        )

        # solve GeeTest v4
        try:
            solved = await solver.solve_geetest_v4(
                page_url=URL,
                captcha_id=regexp.group(1)
            )
        except exceptions.UnicapsException as exc:
            print(f'GeeTestV4 solving exception: {str(exc)}')
            return False, None

        # post solved captcha token
        response = await session.post(
            URL_VERIFY,
            json={
                'captcha_id': solved.solution.captcha_id,
                'lot_number': solved.solution.lot_number,
                'pass_token': solved.solution.pass_token,
                'gen_time': solved.solution.gen_time,
                'captcha_output': solved.solution.captcha_output
            }
        )

    # check the result
    if response.json().get('result') == 'success':
        print('The GeeTest v4 has been solved correctly!')
        # report good CAPTCHA
        await solved.report_good()
        return True, solved

    print('The GeeTest v4 has not been solved correctly!')
    # report bad CAPTCHA
    await solved.report_bad()
    return False, solved


if __name__ == '__main__':
    asyncio.run(main())
