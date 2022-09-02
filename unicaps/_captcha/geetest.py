# -*- coding: UTF-8 -*-
"""
GeeTest CAPTCHA
"""

from dataclasses import dataclass
from typing import Optional

from enforce_typing import enforce_types  # type: ignore

from .base import BaseCaptcha, BaseCaptchaSolution


@enforce_types
@dataclass
class GeeTest(BaseCaptcha):
    """ GeeTest """

    page_url: str
    gt_key: str
    challenge: str
    api_server: Optional[str] = None


@enforce_types
@dataclass
class GeeTestSolution(BaseCaptchaSolution):
    """ GeeTest solution """

    challenge: str
    validate: str
    seccode: str
