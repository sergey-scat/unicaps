# -*- coding: UTF-8 -*-
"""
Base CAPTCHA stuff
"""

import enum
import importlib
from abc import ABC
from dataclasses import dataclass, fields, MISSING
from typing import Dict


class CaptchaType(enum.Enum):
    """ Captcha type enumeration """

    IMAGE = "ImageCaptcha"
    RECAPTCHAV2 = "RecaptchaV2"
    RECAPTCHAV3 = "RecaptchaV3"
    TEXT = "TextCaptcha"
    FUNCAPTCHA = "FunCaptcha"
    GEETEST = "GeeTest"
    GEETESTV4 = "GeeTestV4"
    HCAPTCHA = "HCaptcha"
    KEYCAPTCHA = "KeyCaptcha"
    CAPY = "CapyPuzzle"
    TIKTOK = "TikTokCaptcha"


@dataclass
class BaseCaptcha(ABC):
    """ Base class for any CAPTCHA """

    @classmethod
    def get_type(cls) -> CaptchaType:
        """ Return CaptchaType """

        return CaptchaType(cls.__name__)

    @classmethod
    def get_solution_class(cls) -> 'BaseCaptchaSolution':
        """ Return appropriate solution class """

        return getattr(importlib.import_module(cls.__module__), cls.__name__ + "Solution")

    def get_optional_data(self, **kwargs) -> Dict:
        """
        Return a dict with all optional fields requested (that are not None)
        as a dict with given names.

        :return: :dict:Dictionary of optional not None fields with given names and those values
        :rtype: dict
        """

        result = {}

        if not kwargs:
            # get all optional params
            kwargs = {
                field.name: (field.name, None) for field in fields(self)
                if field.default is not MISSING
            }

        for opt_field in kwargs:
            opt_field_value = getattr(self, opt_field)
            field_name, converter = kwargs[opt_field]
            if opt_field_value is not None:
                if callable(converter):
                    opt_field_value = converter(opt_field_value)
                result[field_name] = opt_field_value
        return result


@dataclass
class BaseCaptchaSolution(ABC):
    """ Base class for any CAPTCHA solution """

    @classmethod
    def get_type(cls) -> CaptchaType:
        """ Returns CaptchaType """

        return CaptchaType(cls.__name__.split("Solution", maxsplit=1)[0])

    @classmethod
    def get_captcha_class(cls) -> BaseCaptcha:
        """ Returns appropriate solution class """

        return getattr(
            importlib.import_module(cls.__module__),
            cls.__name__.split("Solution", maxsplit=1)[0]
        )

    def __str__(self):
        return '\n'.join(str(getattr(self, field.name)) for field in fields(self))
