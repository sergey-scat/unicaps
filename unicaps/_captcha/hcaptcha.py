# -*- coding: UTF-8 -*-
"""
hCaptcha
"""

from dataclasses import dataclass

from .base import BaseCaptcha, BaseCaptchaSolution


@dataclass
class HCaptcha(BaseCaptcha):
    """ hCaptcha """

    site_key: str
    page_url: str

    def __post_init__(self):
        assert isinstance(self.site_key, str)
        assert isinstance(self.page_url, str)


@dataclass
class HCaptchaSolution(BaseCaptchaSolution):
    """ hCaptcha solution """

    token: str
