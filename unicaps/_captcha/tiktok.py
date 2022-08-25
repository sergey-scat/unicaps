# -*- coding: UTF-8 -*-
"""
TikTokCaptcha
"""

from dataclasses import dataclass
from typing import Optional

from .base import BaseCaptcha, BaseCaptchaSolution


@dataclass
class TikTokCaptcha(BaseCaptcha):
    """ TikTokCaptcha """

    page_url: str
    aid: Optional[int] = None
    host: Optional[str] = None

    def __post_init__(self):
        assert isinstance(self.page_url, str)
        assert self.aid is None or isinstance(self.aid, int)
        assert self.host is None or isinstance(self.host, str)


@dataclass
class TikTokCaptchaSolution(BaseCaptchaSolution):
    """ TikTokCaptcha solution """

    cookies: dict
