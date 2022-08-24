"""
TextCaptcha solving example
"""

import os

from unicaps import CaptchaSolver, CaptchaSolvingService, exceptions
from unicaps.common import WorkerLanguage

API_KEY = os.getenv('API_KEY_2CAPTCHA', default='YOUR_API_KEY')
TEXT_CAPTCHA = 'If tomorrow is Sunday, what day is today?'
TEXT_CAPTCHA_ANSWER = 'saturday'


def run(solver):
    # solve TextCaptcha
    try:
        solved = solver.solve_text_captcha(
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
        solved.report_good()
        return True, solved

    print('TextCaptcha wasn\'t solved!')
    # report bad CAPTCHA
    solved.report_bad()
    return False, solved


if __name__ == '__main__':
    solver = CaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, API_KEY)
    run(solver)
