# -*- coding: UTF-8 -*-
"""
Google reCAPTCHA v2
"""

from dataclasses import dataclass
from typing import Optional

from enforce_typing import enforce_types  # type: ignore

from .base import BaseCaptcha, BaseCaptchaSolution


@enforce_types
@dataclass
class RecaptchaV2(BaseCaptcha):
    """ Google reCAPTCHA v2 """

    site_key: str
    page_url: str
    is_invisible: bool = False
    is_enterprise: bool = False
    data_s: Optional[str] = None
    api_domain: Optional[str] = None


@enforce_types
@dataclass
class RecaptchaV2Solution(BaseCaptchaSolution):
    """ Google reCAPTCHA v2 solution """

    token: str
