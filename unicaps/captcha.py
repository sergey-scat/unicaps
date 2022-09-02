# -*- coding: UTF-8 -*-
"""
Supported CAPTCHAs
~~~~~~~~~~~~~~~~~~
"""

# pylint: disable=unused-import,import-error
from ._captcha import (ImageCaptcha, TextCaptcha, RecaptchaV2, RecaptchaV3, HCaptcha, FunCaptcha,
                       KeyCaptcha, GeeTest, GeeTestV4, CapyPuzzle, TikTokCaptcha, CaptchaType)

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
