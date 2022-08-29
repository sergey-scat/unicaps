# -*- coding: UTF-8 -*-
"""
hCaptcha
"""

from dataclasses import dataclass
from typing import Optional

from enforce_typing import enforce_types  # type: ignore

from .base import BaseCaptcha, BaseCaptchaSolution


@enforce_types
@dataclass
class HCaptcha(BaseCaptcha):
    """ hCaptcha """

    site_key: str
    page_url: str
    is_invisible: bool = False
    api_domain: Optional[str] = None


@enforce_types
@dataclass
class HCaptchaSolution(BaseCaptchaSolution):
    """ hCaptcha solution """

    token: str
