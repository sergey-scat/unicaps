# -*- coding: UTF-8 -*-
"""
Text CAPTCHA
"""

from dataclasses import dataclass
from typing import Optional

from enforce_typing import enforce_types  # type: ignore

from .base import BaseCaptcha, BaseCaptchaSolution
from ..common import CaptchaAlphabet, WorkerLanguage


@enforce_types
@dataclass
class TextCaptcha(BaseCaptcha):
    """ Text CAPTCHA """

    text: str
    alphabet: Optional[CaptchaAlphabet] = None
    language: Optional[WorkerLanguage] = None


@enforce_types
@dataclass
class TextCaptchaSolution(BaseCaptchaSolution):
    """ Text CAPTCHA solution """

    text: str
