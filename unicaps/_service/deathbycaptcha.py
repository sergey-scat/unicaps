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
            self.settings[captcha_type].polling_interval = 5
            self.settings[captcha_type].solution_timeout = 180

            if captcha_type in (CaptchaType.RECAPTCHAV2, CaptchaType.HCAPTCHA):
                self.settings[captcha_type].polling_delay = 15
                self.settings[captcha_type].solution_timeout = 200
            elif captcha_type in (CaptchaType.RECAPTCHAV3,):
                self.settings[captcha_type].polling_delay = 15


class Request(HTTPRequestJSON):
    """ Common Request class for deathbycaptcha """

    def parse_response(self, response) -> dict:
        """ Parse response and checks for errors """

        response_data = super().parse_response(response)

        status_code = response_data.pop('status')
        if status_code == 0:
            if 'text' in response_data.keys() and response_data['text'] not in ['', '?']:
                return response_data
            elif 'text' not in response_data or response.status_code == 303:
                return response_data

        ###############
        # handle errors
        ###############
        error_text = response_data.get('error', '')
        error_msg = f"{status_code}: {error_text}"

        if 'text' in response_data.keys():
            if response_data['text'] == '':
                error_text = 'CAPCHA_NOT_READY'
            elif response_data['text'] == '?':
                error_text = 'ERROR_CAPTCHA_UNSOLVABLE'

        if error_text == 'CAPCHA_NOT_READY':  # pylint: disable=no-else-raise
            raise exceptions.SolutionNotReadyYet()
        elif error_text in ('token authentication disabled', 'not-logged-in', 'banned'):
            raise exceptions.AccessDeniedError(error_msg)
        elif error_text in ('insufficient-funds',):
            raise exceptions.LowBalanceError(error_msg)
        elif error_text in ('service-overload',):
            raise exceptions.ServiceTooBusy(error_msg)
        elif error_text in ('upload-failed', 'invalid-captcha'):
            raise exceptions.MalformedRequestError(error_msg)
        elif error_text in ('ERROR_PAGEURL', 'Invalid base64-encoded CAPTCHA', 'Not a (CAPTCHA) image',
                            'Empty CAPTCHA image', 'ERROR_GOOGLEKEY', 'ERROR_PAGEURL',
                            'ERROR_PUBLICKEY', 'ERROR_SITEKEY', 'ERROR_ACTION', 'ERROR_MIN_SCORE',
                            'ERROR_MIN_SCORE_NOT_FLOAT'):
            raise exceptions.BadInputDataError(error_msg)
        elif error_text in 'ERROR_CAPTCHA_UNSOLVABLE':
            raise exceptions.UnableToSolveError(error_msg)
        elif error_text in ('ERROR_PROXYTYPE', 'ERROR_PROXY'):
            raise exceptions.ProxyError(error_msg)

        raise exceptions.ServiceError(error_msg)


class InRequest(Request):
    """ Request class for POST requests """

    def prepare(self, **kwargs) -> dict:
        """ Prepare request """

        request = super().prepare(**kwargs)
        request['headers'].pop('Content-Type')

        request.update(
            dict(
                method="POST",
                url=self._service.BASE_URL + "/captcha",
                data=dict(
                    authtoken=self._service.api_key
                )
            )
        )
        return request


class ResRequest(Request):
    """ Request class for GET requests """

    def prepare(self) -> dict:
        """ Prepare request """

        request = super().prepare()
        request.update(
            dict(
                method="GET",
                url=self._service.BASE_URL,
                params=dict(
                    authtoken=self._service.api_key
                )
            )
        )
        return request


class GetBalanceRequest(ResRequest):
    """ GetBalance Request class """

    def prepare(self) -> dict:
        """ Prepare request """

        request = super().prepare()
        return request

    def parse_response(self, response) -> dict:
        """ Parse response and return balance """

        return {'balance': float(super().parse_response(response)["balance"])}


class GetStatusRequest(ResRequest):
    """ GetStatus Request class """

    def prepare(self):
        request = super().prepare()
        request['url'] = self._service.BASE_URL + '/status'

        return request

    def parse_response(self, response) -> dict:
        """ Parse response and return status """

        try:
            return super().parse_response(response)
        except exceptions.UnicapsException:
            return {}


class ReportGoodRequest(Request):
    """ ReportGood Request class """

    # pylint: disable=arguments-differ
    def prepare(self, solved_captcha) -> dict:  # type: ignore
        """ Prepares request """

        raise exceptions.UnicapsException(
            "Report for good CAPTCHA is not supported by the current service!"
        )


class ReportBadRequest(InRequest):
    """ ReportBad Request class """

    # pylint: disable=arguments-differ
    def prepare(self, solved_captcha) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare(solved_captcha=solved_captcha)
        request['url'] = request['url'] + '/' + solved_captcha.captcha_id + '/report'

        return request


class TaskRequest(InRequest):
    """ Common Task Request class """

    # pylint: disable=arguments-differ,unused-argument
    def prepare(self, captcha, proxy, user_agent, cookies):
        """ Prepare a request """

        request = super().prepare(
            captcha=captcha,
            proxy=proxy,
            user_agent=user_agent,
            cookies=cookies
        )

        if proxy:
            request['data'].update(
                dict(
                    proxy=proxy.get_string(),
                    proxytype=proxy.proxy_type.value.upper()
                )
            )

        return request

    def parse_response(self, response) -> dict:
        """ Parse response and return captcha_id """

        response_data = super().parse_response(response)

        return dict(
            task_id=response_data.pop("captcha"),
            extra=response_data
        )


class SolutionRequest(ResRequest):
    """ Common Solution Request class """

    # pylint: disable=arguments-differ
    def prepare(self, task) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare()
        request['url'] = self._service.BASE_URL + '/captcha/' + task.task_id

        return request

    def parse_response(self, response) -> dict:
        """ Parse response and return solution and cost """

        response_data = super().parse_response(response)
        solution_data = response_data.pop("text")

        return dict(
            solution=solution_data
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
        opt_data = captcha.get_optional_data(data_s=('data-s', None))
        data_s = None
        if opt_data.keys():
            data_s = opt_data['data-s']

        data = {
            "googlekey": captcha.site_key,
            "pageurl": captcha.page_url
        }
        if data_s:
            data.update({"data-s": data_s})

        request['data'].update(
            dict(
                type=4,
                token_params=json.dumps(data)
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

        opt_data = captcha.get_optional_data(
            action=('action', None),
            min_score=('min_score', None)
        )
        action = None
        min_score = None
        if opt_data.keys():
            if 'action' in opt_data.keys():
                action = opt_data['action']
            if 'min_score' in opt_data.keys():
                min_score = opt_data['min_score']

        data = {
            "googlekey": captcha.site_key,
            "pageurl": captcha.page_url
        }
        if action:
            data.update({"action": action})
        if min_score:
            data.update({"min_score": min_score})

        request['data'].update(
            dict(
                type=5,
                token_params=json.dumps(data)
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

        request['data'].update(
            dict(
                type=6,
                funcaptcha_params=json.dumps({
                    "publickey": captcha.public_key,
                    "pageurl": captcha.page_url
                })
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

        request['data'].update(
            dict(
                type=7,
                hcaptcha_params=json.dumps({
                    "sitekey": captcha.site_key,
                    "pageurl": captcha.page_url
                })
            )
        )

        return request


class HCaptchaSolutionRequest(SolutionRequest):
    """ HCaptcha solution request """
