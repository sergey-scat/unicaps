# -*- coding: UTF-8 -*-
"""
KeyCaptcha
"""

from dataclasses import dataclass

from enforce_typing import enforce_types  # type: ignore

from .base import BaseCaptcha, BaseCaptchaSolution


@enforce_types
@dataclass
class KeyCaptcha(BaseCaptcha):
    """ KeyCaptcha """

    page_url: str
    user_id: str
    session_id: str
    ws_sign: str
    ws_sign2: str


@enforce_types
@dataclass
class KeyCaptchaSolution(BaseCaptchaSolution):
    """ KeyCaptcha solution """

    token: str
