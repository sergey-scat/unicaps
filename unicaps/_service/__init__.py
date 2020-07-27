# -*- coding: UTF-8 -*-
"""
Certain services related stuff
"""

import enum
# pylint: disable=import-self
from . import anti_captcha, cptch_net, rucaptcha, twocaptcha


class CaptchaSolvingService(enum.Enum):
    """ CAPTCHA solving service enumeration """

    ANTI_CAPTCHA = "anti-captcha.com"
    CPTCH_NET = "cptch.net"
    RUCAPTCHA = "rucaptcha.com"
    TWOCAPTCHA = "2captcha.com"


# supported CAPTCHA solving services
SOLVING_SERVICE = {
    CaptchaSolvingService.ANTI_CAPTCHA: anti_captcha,
    CaptchaSolvingService.CPTCH_NET: cptch_net,
    CaptchaSolvingService.RUCAPTCHA: rucaptcha,
    CaptchaSolvingService.TWOCAPTCHA: twocaptcha
}
