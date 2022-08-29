# -*- coding: UTF-8 -*-
"""
GeeTest v4 CAPTCHA
"""

from dataclasses import dataclass
from typing import Optional

from enforce_typing import enforce_types  # type: ignore

from .base import BaseCaptcha, BaseCaptchaSolution


@enforce_types
@dataclass
class GeeTestV4(BaseCaptcha):
    """ GeeTest v4 """

    page_url: str
    captcha_id: str


@enforce_types
@dataclass
class GeeTestV4Solution(BaseCaptchaSolution):
    """ GeeTest v4 solution """

    captcha_id: str
    lot_number: str
    pass_token: str
    gen_time: str
    captcha_output: str
