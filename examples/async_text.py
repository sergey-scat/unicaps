"""
TextCaptcha solving example
"""

import asyncio
import os

from unicaps import AsyncCaptchaSolver, CaptchaSolvingService, exceptions  # type: ignore
from unicaps.common import WorkerLanguage  # type: ignore

API_KEY = os.getenv('API_KEY_2CAPTCHA', default='YOUR_API_KEY')
TEXT_CAPTCHA = 'If tomorrow is Sunday, what day is today?'
TEXT_CAPTCHA_ANSWER = 'saturday'


async def run(solver):
    """ TextCaptcha solving func """

    # solve TextCaptcha
    try:
        solved = await solver.solve_text_captcha(
            text=TEXT_CAPTCHA,
            language=WorkerLanguage.ENGLISH
        )
    except exceptions.UnicapsException as exc:
        print(f'TextCaptcha solving exception: {str(exc)}')
        return False, None

    # check the result
    if solved.solution.text.lower() == TEXT_CAPTCHA_ANSWER:
        print('TextCaptcha has been solved successfully!')
        # report good CAPTCHA
        await solved.report_good()
        return True, solved

    print('TextCaptcha wasn\'t solved!')
    # report bad CAPTCHA
    await solved.report_bad()
    return False, solved


if __name__ == '__main__':
    asyncio.run(
        run(
            AsyncCaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, API_KEY)
        )
    )
