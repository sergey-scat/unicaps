# -*- coding: UTF-8 -*-
"""
Google reCAPTCHA v2
"""

from dataclasses import dataclass
from typing import Optional

from .base import BaseCaptcha, BaseCaptchaSolution


@dataclass
class RecaptchaV2(BaseCaptcha):
    """ Google reCAPTCHA v2 """

    site_key: str
    page_url: str
    is_invisible: bool = False
    data_s: Optional[str] = None

    def __post_init__(self):
        assert isinstance(self.site_key, str)
        assert isinstance(self.page_url, str)
        assert isinstance(self.is_invisible, bool)
        assert self.data_s is None or isinstance(self.data_s, str)


@dataclass
class RecaptchaV2Solution(BaseCaptchaSolution):
    """ Google reCAPTCHA v2 solution """

    token: str
