# -*- coding: UTF-8 -*-
"""
Certain services related stuff
"""

import enum
# pylint: disable=import-self
from . import (
    anti_captcha, azcaptcha, captcha_guru, cptch_net, deathbycaptcha, rucaptcha, twocaptcha
)


class CaptchaSolvingService(enum.Enum):
    """ CAPTCHA solving service enumeration """

    ANTI_CAPTCHA = "anti-captcha.com"
    AZCAPTCHA = "azcaptcha.com"
    CAPTCHA_GURU = "captcha.guru"
    CPTCH_NET = "cptch.net"
    DEATHBYCAPTCHA = "deathbycaptcha.com"
    RUCAPTCHA = "rucaptcha.com"
    TWOCAPTCHA = "2captcha.com"


# supported CAPTCHA solving services
SOLVING_SERVICE = {
    CaptchaSolvingService.ANTI_CAPTCHA: anti_captcha,
    CaptchaSolvingService.AZCAPTCHA: azcaptcha,
    CaptchaSolvingService.CAPTCHA_GURU: captcha_guru,
    CaptchaSolvingService.CPTCH_NET: cptch_net,
    CaptchaSolvingService.DEATHBYCAPTCHA: deathbycaptcha,
    CaptchaSolvingService.RUCAPTCHA: rucaptcha,
    CaptchaSolvingService.TWOCAPTCHA: twocaptcha
}
