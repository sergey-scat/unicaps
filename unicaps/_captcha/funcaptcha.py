# -*- coding: UTF-8 -*-
"""
FunCaptcha
"""

from dataclasses import dataclass
from typing import Optional

from .base import BaseCaptcha, BaseCaptchaSolution


@dataclass
class FunCaptcha(BaseCaptcha):
    """ FunCaptcha """

    public_key: str
    page_url: str
    service_url: Optional[str] = None
    no_js: Optional[bool] = None

    def __post_init__(self):
        assert isinstance(self.public_key, str)
        assert isinstance(self.page_url, str)
        assert self.service_url is None or isinstance(self.service_url, str)
        assert self.no_js is None or isinstance(self.no_js, bool)


@dataclass
class FunCaptchaSolution(BaseCaptchaSolution):
    """ FunCaptcha solution """

    token: str
