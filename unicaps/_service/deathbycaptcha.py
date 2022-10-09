# -*- coding: UTF-8 -*-
"""
deathbycaptcha.com service
"""
import json

from .base import HTTPService
from .._transport.http_transport import HTTPRequestJSON  # type: ignore
from .. import exceptions
from .._captcha import CaptchaType

__all__ = [
    'Service', 'GetBalanceRequest', 'GetStatusRequest',
    'ReportGoodRequest', 'ReportBadRequest',
    'ImageCaptchaTaskRequest', 'ImageCaptchaSolutionRequest',
    'RecaptchaV2TaskRequest', 'RecaptchaV2SolutionRequest',
    'RecaptchaV3TaskRequest', 'RecaptchaV3SolutionRequest',
    'FunCaptchaTaskRequest', 'FunCaptchaSolutionRequest',
    'HCaptchaTaskRequest', 'HCaptchaSolutionRequest'
]


class Service(HTTPService):
    """ Main service class for deathbycaptcha """

    BASE_URL = 'http://api.dbcapi.me/api'

    def _post_init(self):
        """ Init settings """
        self._transport.settings['handle_http_errors'] = False

        for captcha_type in self.settings:
            self.settings[captcha_type].polling_delay = 5
            self.settings[captcha_type].polling_interval = 2
            self.settings[captcha_type].solution_timeout = 180

            if captcha_type in (CaptchaType.RECAPTCHAV2, CaptchaType.HCAPTCHA):
                self.settings[captcha_type].polling_delay = 15
                self.settings[captcha_type].solution_timeout = 200
            elif captcha_type in (CaptchaType.RECAPTCHAV3,):
                self.settings[captcha_type].polling_delay = 15


class Request(HTTPRequestJSON):
    """ Common Request class for deathbycaptcha """

    def prepare(self, **kwargs) -> dict:
        """ Prepare the request """

        request = super().prepare(**kwargs)
        request['headers'].pop('Content-Type')

        method = kwargs.get('method', 'GET')
        data_or_params = 'data' if method == 'POST' else 'params'

        request.update({
            'method': kwargs.get('method', 'GET'),
            'url': self._service.BASE_URL + kwargs.get('url', ''),
            data_or_params: dict(
                authtoken=self._service.api_key
            ),
            # 'follow_redirects': True
        })
        return request

    def parse_response(self, response) -> dict:
        """ Parse response and check for errors """

        response_data = super().parse_response(response)

        status = response_data.get('status')
        if (response.status_code == 303 or response.is_success) and status == 0:
            response_data.pop('status')
            return response_data

        #################
        # handle errors #
        #################
        if response_data.get('error'):
            error_text = response_data['error']
        elif response.is_error:
            error_text = f'[{response.status_code} {response.reason_phrase}]'
        else:
            error_text = 'Unknown error'

        error_msg = f"{status}: {error_text}"

        if error_text in ('token authentication disabled', 'not-logged-in', 'banned'):
            raise exceptions.AccessDeniedError(error_msg)
        if error_text in ('insufficient-funds',):
            raise exceptions.LowBalanceError(error_msg)
        if error_text in ('service-overload',):
            raise exceptions.ServiceTooBusy(error_msg)
        if error_text in ('upload-failed', 'invalid-captcha'):
            raise exceptions.MalformedRequestError(error_msg)
        if error_text in ('ERROR_PAGEURL', 'Invalid base64-encoded CAPTCHA',
                          'Not a (CAPTCHA) image', 'Empty CAPTCHA image', 'ERROR_GOOGLEKEY',
                          'ERROR_PAGEURL', 'ERROR_PUBLICKEY', 'ERROR_SITEKEY', 'ERROR_ACTION',
                          'ERROR_MIN_SCORE', 'ERROR_MIN_SCORE_NOT_FLOAT'):
            raise exceptions.BadInputDataError(error_msg)
        if error_text in ('ERROR_PROXYTYPE', 'ERROR_PROXY'):
            raise exceptions.ProxyError(error_msg)

        raise exceptions.ServiceError(error_msg)


class PostRequest(Request):
    """ Request class for POST requests """

    def prepare(self, **kwargs) -> dict:
        """ Prepare request """
        return super().prepare(method="POST", **kwargs)


class GetRequest(Request):
    """ Request class for GET requests """

    def prepare(self, **kwargs) -> dict:
        """ Prepare request """
        return super().prepare(method="GET", **kwargs)


class GetBalanceRequest(GetRequest):
    """ GetBalance Request class """

    def prepare(self) -> dict:
        """ Prepare request """
        return super().prepare(url='')

    def parse_response(self, response) -> dict:
        """ Parse response and return balance """
        return {
            'balance': float(super().parse_response(response)["balance"]) / 100
        }


class GetStatusRequest(GetRequest):
    """ GetStatus Request class """

    def prepare(self):
        """ Prepare request """
        return super().prepare(url='/status')

    def parse_response(self, response) -> dict:
        """ Parse response and return status """
        try:
            response_data = super().parse_response(response)
            if response_data.get('is_service_overloaded'):
                return {}
            return response_data
        except exceptions.UnicapsException:
            return {}


class ReportGoodRequest(PostRequest):
    """ ReportGood Request class """

    # pylint: disable=arguments-differ
    def prepare(self, solved_captcha) -> dict:  # type: ignore
        """ Prepares request """
        raise exceptions.UnicapsException(
            "Report for good CAPTCHA is not supported by the current service!"
        )


class ReportBadRequest(PostRequest):
    """ ReportBad Request class """

    # pylint: disable=arguments-differ
    def prepare(self, solved_captcha) -> dict:  # type: ignore
        """ Prepare request """
        return super().prepare(
            url=f'/captcha/{solved_captcha.captcha_id}/report',
            solved_captcha=solved_captcha
        )


class TaskRequest(PostRequest):
    """ Common Task Request class """

    # pylint: disable=arguments-differ,unused-argument
    def prepare(self, captcha, proxy, user_agent, cookies):
        """ Prepare a request """

        request = super().prepare(
            url='/captcha',
            captcha=captcha,
            proxy=proxy,
            user_agent=user_agent,
            cookies=cookies
        )

        return request

    def parse_response(self, response) -> dict:
        """ Parse response and return captcha_id """

        response_data = super().parse_response(response)

        # raise the BadInputDataError if CAPTCHA is not correct
        if not response_data.pop('is_correct'):
            raise exceptions.BadInputDataError('is_correct=false')

        if 'text' in response_data:
            response_data.pop('text')

        return dict(
            task_id=response_data.pop("captcha"),
            extra=response_data
        )


class SolutionRequest(GetRequest):
    """ Common Solution Request class """

    # pylint: disable=arguments-differ
    def prepare(self, task) -> dict:  # type: ignore
        """ Prepare request """
        return super().prepare(url=f'/captcha/{task.task_id}', task=task)

    def parse_response(self, response) -> dict:
        """ Parse response and return solution and cost """

        response_data = super().parse_response(response)

        # raise the UnableToSolveError if CAPTCHA is not correct
        if not response_data.pop('is_correct'):
            raise exceptions.UnableToSolveError('is_correct=false')

        # the empty text field means that solving is in progress
        text = response_data.pop("text")
        if not text:
            raise exceptions.SolutionNotReadyYet()

        # get solution class and prepare a solution object
        solution_class = self.source_data['task'].captcha.get_solution_class()
        solution = solution_class(text)

        response_data.pop("captcha")

        return dict(
            solution=solution,
            extra=response_data
        )


class ImageCaptchaTaskRequest(TaskRequest):
    """ ImageCaptchaTask Request class """

    # pylint: disable=arguments-differ,unused-argument,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare(
            captcha=captcha,
            proxy=proxy,
            user_agent=user_agent,
            cookies=cookies
        )

        # add required params
        request['data'].update(dict(
            captchafile='base64:' + captcha.get_image_base64().decode('ascii')
        ))
        return request


class ImageCaptchaSolutionRequest(SolutionRequest):
    """ Image CAPTCHA solution request """


class RecaptchaV2TaskRequest(TaskRequest):
    """ reCAPTCHA v2 task request """

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare(
            captcha=captcha,
            proxy=proxy,
            user_agent=user_agent,
            cookies=cookies
        )

        data = {
            "googlekey": captcha.site_key,
            "pageurl": captcha.page_url
        }
        data.update(
            captcha.get_optional_data(
                data_s=('data-s', None),
            )
        )

        request['data'].update(
            dict(
                type=4,
                token_params=_dumps(data, proxy)
            )
        )

        return request


class RecaptchaV2SolutionRequest(SolutionRequest):
    """ reCAPTCHA v2 solution request """


class RecaptchaV3TaskRequest(TaskRequest):
    """ reCAPTCHA v3 task request """

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare(
            captcha=captcha,
            proxy=proxy,
            user_agent=user_agent,
            cookies=cookies
        )

        data = {
            "googlekey": captcha.site_key,
            "pageurl": captcha.page_url
        }

        data.update(
            captcha.get_optional_data(
                action=('action', None),
                min_score=('min_score', None),
            )
        )

        request['data'].update(
            dict(
                type=5,
                token_params=_dumps(data, proxy)
            )
        )

        return request


class RecaptchaV3SolutionRequest(SolutionRequest):
    """ reCAPTCHA v3 solution request """


class FunCaptchaTaskRequest(TaskRequest):
    """ FunCaptcha task request """

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare(
            captcha=captcha,
            proxy=proxy,
            user_agent=user_agent,
            cookies=cookies
        )

        data = {
            "publickey": captcha.public_key,
            "pageurl": captcha.page_url
        }

        request['data'].update(
            dict(
                type=6,
                funcaptcha_params=_dumps(data, proxy)
            )
        )

        return request


class FunCaptchaSolutionRequest(SolutionRequest):
    """ FunCaptcha solution request """


class HCaptchaTaskRequest(TaskRequest):
    """ HCaptcha task request """

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare(
            captcha=captcha,
            proxy=proxy,
            user_agent=user_agent,
            cookies=cookies
        )

        data = {
            "sitekey": captcha.site_key,
            "pageurl": captcha.page_url
        }

        request['data'].update(
            dict(
                type=7,
                hcaptcha_params=_dumps(data, proxy)
            )
        )

        return request


class HCaptchaSolutionRequest(SolutionRequest):
    """ HCaptcha solution request """


def _dumps(data, proxy):
    if proxy:
        data.update(
            dict(
                proxy=proxy.get_string(including_type=True),
                proxytype=proxy.proxy_type.value.upper()
            )
        )
    return json.dumps(data)
