# -*- coding: UTF-8 -*-
"""
FunCaptcha
"""

from dataclasses import dataclass
from typing import Optional

from enforce_typing import enforce_types  # type: ignore

from .base import BaseCaptcha, BaseCaptchaSolution


@enforce_types
@dataclass
class FunCaptcha(BaseCaptcha):
    """ FunCaptcha """

    public_key: str
    page_url: str
    service_url: Optional[str] = None
    no_js: Optional[bool] = None
    blob: Optional[str] = None


@enforce_types
@dataclass
class FunCaptchaSolution(BaseCaptchaSolution):
    """ FunCaptcha solution """

    token: str
