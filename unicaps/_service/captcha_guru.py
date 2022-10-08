"""
captcha.guru service
"""

# pylint: disable=unused-import
from .twocaptcha import (
    Service as Service2Captcha, GetBalanceRequest, GetStatusRequest,
    ReportGoodRequest, ReportBadRequest,
    ImageCaptchaTaskRequest, ImageCaptchaSolutionRequest,
    RecaptchaV2TaskRequest, RecaptchaV2SolutionRequest,
    RecaptchaV3TaskRequest, RecaptchaV3SolutionRequest,
    HCaptchaTaskRequest, HCaptchaSolutionRequest,
    GeeTestTaskRequest, GeeTestSolutionRequest
)

__all__ = [
    'Service', 'GetBalanceRequest', 'GetStatusRequest',
    'ReportGoodRequest', 'ReportBadRequest',
    'ImageCaptchaTaskRequest', 'ImageCaptchaSolutionRequest',
    'RecaptchaV2TaskRequest', 'RecaptchaV2SolutionRequest',
    'RecaptchaV3TaskRequest', 'RecaptchaV3SolutionRequest',
    'HCaptchaTaskRequest', 'HCaptchaSolutionRequest',
    'GeeTestTaskRequest', 'GeeTestSolutionRequest'
]


class Service(Service2Captcha):
    """ Main service class for captcha.guru """

    BASE_URL = 'http://api.captcha.guru'


def _decorator(cls):
    """ Decorator for *TaskRequest class """

    # pylint: disable=missing-function-docstring
    class Wrapper:
        """ A wrapper for *TaskRequest class """
        def __init__(self, *args, **kwargs):
            # print(f"__init__() called with args: {args} and kwargs: {kwargs}")
            self.decorated_obj = cls(*args, **kwargs)

        def prepare(self, *args, **kwargs):
            result = self.decorated_obj.prepare(*args, **kwargs)
            if 'data' in result:
                result['params'] = result['data']
                del result['data']
                result['method'] = 'GET'

                if 'soft_id' in result['params']:
                    del result['params']['soft_id']
                    result['params']['softguru'] = '127872'

            return result

        def parse_response(self, *args, **kwargs):
            return self.decorated_obj.parse_response(*args, **kwargs)

        def process_response(self, *args, **kwargs):
            return self.decorated_obj.process_response(*args, **kwargs)

    return Wrapper


ImageCaptchaTaskRequest = _decorator(ImageCaptchaTaskRequest)  # type: ignore
RecaptchaV2TaskRequest = _decorator(RecaptchaV2TaskRequest)  # type: ignore
RecaptchaV3TaskRequest = _decorator(RecaptchaV3TaskRequest)  # type: ignore
HCaptchaTaskRequest = _decorator(HCaptchaTaskRequest)  # type: ignore
GeeTestTaskRequest = _decorator(GeeTestTaskRequest)  # type: ignore
