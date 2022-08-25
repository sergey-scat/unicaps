# -*- coding: UTF-8 -*-

from unicaps._captcha import CaptchaType
from unicaps._captcha.base import BaseCaptcha, BaseCaptchaSolution


def test_captcha_class_base(captcha_class):
    """
    Checks base class of Captcha class.
    """
    assert issubclass(captcha_class, BaseCaptcha)


def test_captcha_class_get_type(captcha_class):
    """
    Checks get_type() function of Captcha class.
    """
    assert isinstance(captcha_class.get_type(), CaptchaType)


def test_captcha_class_get_solution_class(captcha_class):
    """
    Checks get_solution_class() function of Captcha class.
    """
    assert issubclass(captcha_class.get_solution_class(), BaseCaptchaSolution)


def test_captcha_class_get_optional_data(captcha_instance):
    """
    Checks get_optional_data() function of Captcha class.
    """
    assert isinstance(captcha_instance.get_optional_data(), dict)


def test_captchasolution_class_get_type(captcha_class):
    """
    Checks get_type() function of CaptchaSolution class.
    """
    assert captcha_class.get_type() is captcha_class.get_solution_class().get_type()


def test_captchasolution_class_get_captcha_class(captcha_class):
    """
    Checks get_type() function of CaptchaSolution class.
    """
    assert captcha_class is captcha_class.get_solution_class().get_captcha_class()


def test_captchasolution_obj_get_string(captcha_class):
    """
    Checks get_type() function of CaptchaSolution class.
    """
    solution_class = captcha_class.get_solution_class()

    dc_fields = solution_class.__dataclass_fields__
    field_values = []
    for i, field in enumerate(dc_fields.values(), start=1):
        if field.type == str:
            value = f'test{i}'
        elif field.type == dict:
            value = {f'test{i}': f'test{i}'}
        else:
            value = None

        field_values.append(value)

    solution_obj = solution_class(*field_values)

    assert str(solution_obj) == '\n'.join(str(v) for v in field_values)
