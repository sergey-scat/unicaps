# -*- coding: UTF-8 -*-
"""
Text CAPTCHA
"""

from dataclasses import dataclass
from typing import Optional

from .base import BaseCaptcha, BaseCaptchaSolution
from ..common import CaptchaAlphabet, WorkerLanguage


@dataclass
class TextCaptcha(BaseCaptcha):
    """ Text CAPTCHA """

    text: str
    alphabet: Optional[CaptchaAlphabet] = None
    language: Optional[WorkerLanguage] = None

    def __post_init__(self):
        assert isinstance(self.text, str)
        assert self.alphabet is None or isinstance(self.alphabet, CaptchaAlphabet)
        assert self.language is None or isinstance(self.language, WorkerLanguage)


@dataclass
class TextCaptchaSolution(BaseCaptchaSolution):
    """ Text CAPTCHA solution """

    text: str
