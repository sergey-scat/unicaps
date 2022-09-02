# -*- coding: UTF-8 -*-
"""
TikTokCaptcha
"""

from dataclasses import dataclass
from typing import Optional

from enforce_typing import enforce_types  # type: ignore

from .base import BaseCaptcha, BaseCaptchaSolution


@enforce_types
@dataclass
class TikTokCaptcha(BaseCaptcha):
    """ TikTokCaptcha """

    page_url: str
    aid: Optional[int] = None
    host: Optional[str] = None


@enforce_types
@dataclass
class TikTokCaptchaSolution(BaseCaptchaSolution):
    """ TikTokCaptcha solution """

    cookies: dict
