# -*- coding: UTF-8 -*-
"""
Capy Puzzle
"""

from dataclasses import dataclass

from .base import BaseCaptcha, BaseCaptchaSolution


@dataclass
class Capy(BaseCaptcha):
    """ Capy Puzzle CAPTCHA """

    site_key: str
    page_url: str

    def __post_init__(self):
        assert isinstance(self.site_key, str)
        assert isinstance(self.page_url, str)


@dataclass
class CapySolution(BaseCaptchaSolution):
    """ Capy CAPTCHA solution """

    captchakey: str
    challengekey: str
    answer: str
