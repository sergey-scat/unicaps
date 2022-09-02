# -*- coding: UTF-8 -*-
"""
CaptchaSolver tests
"""
from unittest.mock import Mock

import pytest
from unicaps import CaptchaSolver, CaptchaSolvingService
from unicaps.captcha import CaptchaType

API_KEY = 'TEST_API_KEY'


@pytest.fixture(scope="module")
def captcha_solver():
    return CaptchaSolver('2captcha.com', API_KEY)


@pytest.fixture()
def mocked_captcha_solver(captcha_solver, monkeypatch):
    monkeypatch.setattr(captcha_solver, '_service', Mock())
    return captcha_solver


def test_solver_init():
    service = CaptchaSolvingService.ANTI_CAPTCHA
    solver = CaptchaSolver(service, API_KEY)

    assert solver.service_name == service
    assert solver.api_key == API_KEY


def test_solver_init_from_string():
    solver = CaptchaSolver('2captcha.com', API_KEY)

    assert solver.service_name == CaptchaSolvingService.TWOCAPTCHA
    assert solver.api_key == API_KEY


def test_solver_bad_init():
    with pytest.raises(ValueError):
        CaptchaSolver('2captcha', API_KEY)


def test_solver_bad_init2():
    with pytest.raises(ValueError):
        CaptchaSolver(b'2captcha.com', API_KEY)


# @pytest.mark.parametrize("captcha_type", CaptchaType)
def test_call_solve_func(mocked_captcha_solver, captcha_instance):
    mapping = {
        CaptchaType.IMAGE: 'image_captcha',
        CaptchaType.TEXT: 'text_captcha',
        CaptchaType.RECAPTCHAV2: 'recaptcha_v2',
        CaptchaType.RECAPTCHAV3: 'recaptcha_v3',
        CaptchaType.HCAPTCHA: 'hcaptcha',
        CaptchaType.FUNCAPTCHA: 'funcaptcha',
        CaptchaType.KEYCAPTCHA: 'keycaptcha',
        CaptchaType.GEETEST: 'geetest',
        CaptchaType.CAPY: 'capy_puzzle',
        CaptchaType.TIKTOK: 'tiktok',
        CaptchaType.GEETESTV4: 'geetest_v4'
    }

    func = getattr(mocked_captcha_solver, f'solve_{mapping[captcha_instance.get_type()]}')
    func(
        **{k: v for k, v in captcha_instance.__dict__.items() if not k.startswith('_')}
    )
