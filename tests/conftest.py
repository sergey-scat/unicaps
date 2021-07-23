# -*- coding: UTF-8 -*-

import enum
import importlib
import os.path
import random
import string
import sys

from pytest import fixture

cd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, cd)
from unicaps._captcha import CaptchaType


@fixture()
def services():
    pass


@fixture()
def captcha_service():
    pass


def gen_random_word(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def get_random_value(field):
    cls = getattr(field.type, '__args__', [field.type])[0]

    if cls is str:
        return gen_random_word(10)
    elif cls is bytes:
        return gen_random_word(32).encode('utf-8')
    elif cls is int:
        return random.randint(1, 255)
    elif cls is bool:
        return bool(random.randint(0, 1))
    # elif cls.__base__ is enum.Enum:
    elif issubclass(cls, enum.Enum):
        return getattr(cls, cls._member_names_[0])

    return cls()


@fixture(scope="module", params=CaptchaType)
def captcha_class(request):
    captcha_package = importlib.import_module('unicaps.captcha')
    return getattr(captcha_package, request.param.value)


@fixture(scope="module")
def captcha_instance(captcha_class):
    # return random_dataclass_init(captcha_class)
    params = captcha_class.__dataclass_fields__.copy()
    for name, field in params.items():
        params[name] = get_random_value(field)

        # for ImageCaptcha
        if name == 'image':
            params[name] = params[name][:6] + b'Exif' + params[name][10:]

    return captcha_class(**params)
