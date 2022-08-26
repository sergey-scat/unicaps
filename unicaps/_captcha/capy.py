# -*- coding: UTF-8 -*-
"""
Capy Puzzle
"""

from dataclasses import dataclass
from typing import Optional

from enforce_typing import enforce_types  # type: ignore

from .base import BaseCaptcha, BaseCaptchaSolution


@enforce_types
@dataclass
class CapyPuzzle(BaseCaptcha):
    """ Capy Puzzle CAPTCHA """

    site_key: str
    page_url: str
    api_server: Optional[str] = None


@enforce_types
@dataclass
class CapyPuzzleSolution(BaseCaptchaSolution):
    """ Capy Puzzle CAPTCHA solution """

    captchakey: str
    challengekey: str
    answer: str
