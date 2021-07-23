# -*- coding: UTF-8 -*-
"""
Capy Puzzle
"""

from dataclasses import dataclass
from typing import Optional

from .base import BaseCaptcha, BaseCaptchaSolution


@dataclass
class Capy(BaseCaptcha):
    """ Capy Puzzle CAPTCHA """

    site_key: str
    page_url: str
    api_server: Optional[str] = None

    def __post_init__(self):
        assert isinstance(self.site_key, str)
        assert isinstance(self.page_url, str)
        assert self.api_server is None or isinstance(self.api_server, str)


@dataclass
class CapySolution(BaseCaptchaSolution):
    """ Capy CAPTCHA solution """

    captchakey: str
    challengekey: str
    answer: str
