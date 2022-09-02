"""
Capy Puzzle CAPTCHA solving example
"""

import asyncio
import os
from urllib.parse import urlparse, parse_qs

import httpx
from lxml import html  # type: ignore
from unicaps import AsyncCaptchaSolver, CaptchaSolvingService, exceptions  # type: ignore

URL = 'https://www.capy.me/products/puzzle_captcha/'
API_KEY = os.getenv('API_KEY_2CAPTCHA', default='<PLACE_YOUR_API_KEY_HERE>')
USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36')


async def main():
    """ Init AsyncCaptchaSolver and run the example """
    async with AsyncCaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, API_KEY) as solver:
        await run(solver)


async def run(solver):
    """ Solve Capy Puzzle CAPTCHA """

    # create an HTTP2 session
    async with httpx.AsyncClient(http2=True,
                                 headers={'User-Agent': USER_AGENT}) as session:
        # open page and extract CAPTCHA URL
        response = await session.get(URL)
        page = html.document_fromstring(response.text)

        capy_url = page.xpath('//script[contains(@src, "/puzzle/get_js/")]')[0].attrib['src']
        capy_url_parsed = urlparse(capy_url)
        api_server = f'{capy_url_parsed.scheme}://{capy_url_parsed.hostname}'
        site_key = parse_qs(capy_url_parsed.query)['k'][0]

        # solve Capy Puzzle CAPTCHA
        try:
            solved = await solver.solve_capy_puzzle(
                site_key=site_key,
                page_url=URL,
                api_server=api_server,
                user_agent=USER_AGENT
            )
        except exceptions.UnicapsException as exc:
            print(f'Capy Puzzle CAPTCHA solving exception: {str(exc)}')
            return False, None

        # post solved captcha token
        response = await session.post(
            URL,
            data={
                'capy_captchakey': solved.solution.captchakey,
                'capy_challengekey': solved.solution.challengekey,
                'capy_answer': solved.solution.answer
            }
        )
        page = html.document_fromstring(response.text)

    # check the result
    if page.xpath('//div[@class="result success"]'):
        print('The Capy Puzzle CAPTCHA has been solved correctly!')
        # report good CAPTCHA
        await solved.report_good()
        return True, solved

    print('The Capy Puzzle CAPTCHA has not been solved correctly!')
    # report bad CAPTCHA
    await solved.report_bad()
    return False, solved


if __name__ == '__main__':
    asyncio.run(main())
