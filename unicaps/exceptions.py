# -*- coding: UTF-8 -*-
"""
unicaps.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains the set of Unicaps' exceptions.
"""


class UnicapsException(Exception):
    """Main exception class"""


class SolutionNotReadyYet(UnicapsException):
    """CAPTCHA solving in progress"""


class ServiceError(UnicapsException):
    """Main service-related exception class"""


class CaptchaError(UnicapsException):
    """CAPTCHA-related exception"""


class NetworkError(UnicapsException):
    """
    Network Connection Error
    Service returned 5xx status code
    """


class ProxyError(UnicapsException):
    """
    Bad proxy
    """


class AccessDeniedError(ServiceError):
    """
    Wrong API key
    IP banned
    IP not allowed
    """


class LowBalanceError(ServiceError):
    """
    Low balance
    """


class ServiceTooBusy(ServiceError):
    """
    No available slots
    """


class SolutionWaitTimeout(ServiceError):
    """
    Didn't receive solution within N minutes
    """


class TooManyRequestsError(ServiceError):
    """
    Exceeded request limit
    """


class MalformedRequestError(ServiceError):
    """
    Exceeded request limit
    """


class BadInputDataError(CaptchaError):
    """
    Not supported image file
    Empty file
    Image file is too big
    Bad captcha data (eg, wrong googlekey, bad page URL, etc.)
    """


class UnableToSolveError(CaptchaError):
    """
    Captcha unsolvable
    """
