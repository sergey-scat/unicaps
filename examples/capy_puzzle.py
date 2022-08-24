"""
Capy Puzzle CAPTCHA solving example
"""

import os
import time
from urllib.parse import urlparse, parse_qs

import httpx
from lxml import html
from unicaps import CaptchaSolver, CaptchaSolvingService, exceptions

URL = 'https://www.capy.me/products/puzzle_captcha/'
API_KEY = os.getenv('API_KEY_2CAPTCHA', default='YOUR_API_KEY')
USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36')


def run(solver):
    # create an HTTP2 session
    session = httpx.Client(
        http2=True,
        headers={'User-Agent': USER_AGENT}
    )

    # open page and extract CAPTCHA URL
    response = session.get(URL)
    page = html.document_fromstring(response.text)

    capy_url = page.xpath('//script[contains(@src, "/puzzle/get_js/")]')[0].attrib['src']
    capy_url_parsed = urlparse(capy_url)
    api_server = f'{capy_url_parsed.scheme}://{capy_url_parsed.hostname}'
    site_key = parse_qs(capy_url_parsed.query)['k'][0]

    # solve Capy Puzzle CAPTCHA
    try:
        solved = solver.solve_capy_puzzle(
            site_key=site_key,
            page_url=URL,
            api_server=api_server,
            user_agent=USER_AGENT
        )
    except exceptions.UnicapsException as exc:
        print(f'Capy Puzzle CAPTCHA solving exception: {str(exc)}')
        return False, None

    # post solved captcha token
    response = session.post(
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
        print('Capy Puzzle CAPTCHA has been solved successfully!')
        # report good CAPTCHA
        solved.report_good()
        return True, solved

    print('Capy Puzzle CAPTCHA wasn\'t solved!')
    # report bad CAPTCHA
    solved.report_bad()
    return False, solved


if __name__ == '__main__':
    solver = CaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, API_KEY)
    run(solver)
