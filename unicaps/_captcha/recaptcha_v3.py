# -*- coding: UTF-8 -*-
"""
Google reCAPTCHA v3
"""

from dataclasses import dataclass
from typing import Optional

from .base import BaseCaptcha, BaseCaptchaSolution


@dataclass
class RecaptchaV3(BaseCaptcha):
    """ Google reCAPTCHA v3 """

    site_key: str
    page_url: str
    action: Optional[str] = None
    min_score: Optional[float] = None

    def __post_init__(self):
        assert isinstance(self.site_key, str)
        assert isinstance(self.page_url, str)
        assert self.action is None or isinstance(self.action, str)
        assert self.min_score is None or isinstance(self.min_score, float)


@dataclass
class RecaptchaV3Solution(BaseCaptchaSolution):
    """ Google reCAPTCHA v3 solution """

    token: str
