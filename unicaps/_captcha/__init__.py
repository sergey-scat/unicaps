# -*- coding: UTF-8 -*-

""" CAPTCHAs """

# pylint: disable=unused-import,import-error
from .image import ImageCaptcha
from .text import TextCaptcha
from .recaptcha_v2 import RecaptchaV2
from .recaptcha_v3 import RecaptchaV3
from .hcaptcha import HCaptcha
from .funcaptcha import FunCaptcha
from .keycaptcha import KeyCaptcha
from .geetest import GeeTest
from .geetest_v4 import GeeTestV4
from .capy import CapyPuzzle
from .tiktok import TikTokCaptcha
from .base import CaptchaType

__all__ = (
    'ImageCaptcha',
    'TextCaptcha',
    'RecaptchaV2',
    'RecaptchaV3',
    'HCaptcha',
    'FunCaptcha',
    'KeyCaptcha',
    'GeeTest',
    'GeeTestV4',
    'CapyPuzzle',
    'TikTokCaptcha',
    'CaptchaType'
)
