# -*- coding: UTF-8 -*-
"""
GeeTest CAPTCHA
"""

from dataclasses import dataclass
from typing import Optional

from .base import BaseCaptcha, BaseCaptchaSolution


@dataclass
class GeeTest(BaseCaptcha):
    """ GeeTest """

    page_url: str
    gt_key: str
    challenge: str
    api_server: Optional[str] = None

    def __post_init__(self):
        assert isinstance(self.page_url, str)
        assert isinstance(self.gt_key, str)
        assert isinstance(self.challenge, str)
        assert self.api_server is None or isinstance(self.api_server, str)


@dataclass
class GeeTestSolution(BaseCaptchaSolution):
    """ GeeTest solution """

    challenge: str
    validate: str
    seccode: str
