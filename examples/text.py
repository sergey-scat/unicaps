"""
TextCaptcha solving example
"""

import os

from unicaps import CaptchaSolver, CaptchaSolvingService, exceptions  # type: ignore
from unicaps.common import WorkerLanguage  # type: ignore

API_KEY = os.getenv('API_KEY_2CAPTCHA', default='<PLACE_YOUR_API_KEY_HERE>')
TEXT_CAPTCHA = 'If tomorrow is Sunday, what day is today?'
TEXT_CAPTCHA_ANSWER = 'saturday'


def run(solver):
    """ Solve TextCaptcha """

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
        print('The TextCaptcha has been solved correctly!')
        # report good CAPTCHA
        solved.report_good()
        return True, solved

    print('The TextCaptcha has not been solved correctly!')
    # report bad CAPTCHA
    solved.report_bad()
    return False, solved


if __name__ == '__main__':
    with CaptchaSolver(CaptchaSolvingService.TWOCAPTCHA, API_KEY) as captcha_solver:
        run(captcha_solver)
