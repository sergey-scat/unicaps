# -*- coding: UTF-8 -*-
"""
Google reCAPTCHA v3
"""

from dataclasses import dataclass
from typing import Optional

from enforce_typing import enforce_types

from .base import BaseCaptcha, BaseCaptchaSolution


@enforce_types
@dataclass
class RecaptchaV3(BaseCaptcha):
    """ Google reCAPTCHA v3 """

    site_key: str
    page_url: str
    is_enterprise: bool = False
    action: Optional[str] = None
    min_score: Optional[float] = None


@enforce_types
@dataclass
class RecaptchaV3Solution(BaseCaptchaSolution):
    """ Google reCAPTCHA v3 solution """

    token: str
