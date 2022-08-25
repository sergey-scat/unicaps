# -*- coding: UTF-8 -*-
"""
hCaptcha
"""

from dataclasses import dataclass

from enforce_typing import enforce_types

from .base import BaseCaptcha, BaseCaptchaSolution


@enforce_types
@dataclass
class HCaptcha(BaseCaptcha):
    """ hCaptcha """

    site_key: str
    page_url: str


@enforce_types
@dataclass
class HCaptchaSolution(BaseCaptchaSolution):
    """ hCaptcha solution """

    token: str
