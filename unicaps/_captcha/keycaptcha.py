# -*- coding: UTF-8 -*-
"""
KeyCaptcha
"""

from dataclasses import dataclass

from .base import BaseCaptcha, BaseCaptchaSolution


@dataclass
class KeyCaptcha(BaseCaptcha):
    """ KeyCaptcha """

    page_url: str
    user_id: str
    session_id: str
    ws_sign: str
    ws_sign2: str

    def __post_init__(self):
        assert isinstance(self.page_url, str)
        assert isinstance(self.user_id, str)
        assert isinstance(self.session_id, str)
        assert isinstance(self.ws_sign, str)
        assert isinstance(self.ws_sign2, str)


@dataclass
class KeyCaptchaSolution(BaseCaptchaSolution):
    """ KeyCaptcha solution """

    token: str
