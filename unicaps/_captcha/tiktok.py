# -*- coding: UTF-8 -*-
"""
TikTokCaptcha
"""

from dataclasses import dataclass

from .base import BaseCaptcha, BaseCaptchaSolution


@dataclass
class TikTokCaptcha(BaseCaptcha):
    """ TikTokCaptcha """

    page_url: str

    def __post_init__(self):
        assert isinstance(self.page_url, str)


@dataclass
class TikTokCaptchaSolution(BaseCaptchaSolution):
    """ TikTokCaptcha solution """

    cookies: dict
