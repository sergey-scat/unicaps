# -*- coding: UTF-8 -*-
"""
2captcha.com service
"""

import json

from .base import HTTPService
from .._transport.http_transport import HTTPRequestJSON  # type: ignore
from .. import exceptions
from .._captcha import CaptchaType
from ..common import CaptchaAlphabet

__all__ = [
    'Service', 'GetBalanceRequest', 'GetStatusRequest',
    'ReportGoodRequest', 'ReportBadRequest',
    'ImageCaptchaTaskRequest', 'ImageCaptchaSolutionRequest',
    'RecaptchaV2TaskRequest', 'RecaptchaV2SolutionRequest',
    'RecaptchaV3TaskRequest', 'RecaptchaV3SolutionRequest',
    'TextCaptchaTaskRequest', 'TextCaptchaSolutionRequest',
    'FunCaptchaTaskRequest', 'FunCaptchaSolutionRequest',
    'KeyCaptchaTaskRequest', 'KeyCaptchaSolutionRequest',
    'GeeTestTaskRequest', 'GeeTestSolutionRequest',
    'HCaptchaTaskRequest', 'HCaptchaSolutionRequest',
    'CapyTaskRequest', 'CapySolutionRequest'
]


class Service(HTTPService):
    """ Main service class for 2captcha """

    BASE_URL = 'https://2captcha.com'

    def _post_init(self):
        """ Init settings """

        for captcha_type in self._settings:
            self._settings[captcha_type].polling_interval = 5
            self._settings[captcha_type].solution_timeout = 180
            if captcha_type in (CaptchaType.RECAPTCHAV2, CaptchaType.HCAPTCHA):
                self._settings[captcha_type].polling_delay = 20
                self._settings[captcha_type].solution_timeout = 300
            elif captcha_type in (CaptchaType.RECAPTCHAV3,):
                self._settings[captcha_type].polling_delay = 15
            else:
                self._settings[captcha_type].polling_delay = 5


class Request(HTTPRequestJSON):
    """ Common Request class for 2captcha """

    def parse_response(self, response) -> dict:
        """ Parse response and checks for errors """

        response_data = super().parse_response(response)

        if response_data.pop("status") == 1:
            return response_data

        ###############
        # handle errors
        ###############
        error = response_data["request"]
        error_text = response_data.get("error_text", "")
        error_msg = "{}: {}".format(error, error_text)

        if error == 'CAPCHA_NOT_READY':  # pylint: disable=no-else-raise
            raise exceptions.SolutionNotReadyYet()
        elif error in ('ERROR_WRONG_USER_KEY', 'ERROR_KEY_DOES_NOT_EXIST', 'ERROR_IP_NOT_ALLOWED',
                       'IP_BANNED'):
            raise exceptions.AccessDeniedError(error_msg)
        elif error in ('ERROR_ZERO_BALANCE',):
            raise exceptions.LowBalanceError(error_msg)
        elif error in ('ERROR_NO_SLOT_AVAILABLE',):
            # If server returns ERROR_NO_SLOT_AVAILABLE make a 5 seconds timeout before sending
            # next request.
            # time.sleep(5)
            raise exceptions.ServiceTooBusy(error_msg)
        elif error in ('MAX_USER_TURN',) or error.startswith('ERROR:'):
            raise exceptions.TooManyRequestsError(error_msg)
        elif error in ('ERROR_WRONG_ID_FORMAT', 'ERROR_WRONG_CAPTCHA_ID'):
            raise exceptions.MalformedRequestError(error_msg)
        elif error in ('ERROR_ZERO_CAPTCHA_FILESIZE', 'ERROR_TOO_BIG_CAPTCHA_FILESIZE',
                       'ERROR_WRONG_FILE_EXTENSION', 'ERROR_IMAGE_TYPE_NOT_SUPPORTED',
                       'ERROR_UPLOAD', 'ERROR_PAGEURL', 'ERROR_BAD_TOKEN_OR_PAGEURL',
                       'ERROR_GOOGLEKEY', 'ERROR_BAD_PARAMETERS', 'ERROR_TOKEN_EXPIRED',
                       'ERROR_EMPTY_ACTION'):
            raise exceptions.BadInputDataError(error_msg)
        elif error in ('ERROR_CAPTCHAIMAGE_BLOCKED', 'ERROR_CAPTCHA_UNSOLVABLE',
                       'ERROR_BAD_DUPLICATES'):
            raise exceptions.UnableToSolveError(error_msg)
        elif error in ('ERROR_BAD_PROXY', 'ERROR_PROXY_CONNECTION_FAILED'):
            raise exceptions.ProxyError(error_msg)

        raise exceptions.ServiceError(error_msg)


class InRequest(Request):
    """ Request class for requests to /in.php """

    def prepare(self) -> dict:
        """ Prepare request """

        request = super().prepare()
        request.update(
            dict(
                method="POST",
                url=self._service.BASE_URL + "/in.php",
                data=dict(
                    key=self._service.api_key,
                    json=1,
                    soft_id=2738
                )
            )
        )
        return request


class ResRequest(Request):
    """ Request class for requests to /res.php """

    def prepare(self) -> dict:
        """ Prepare request """

        request = super().prepare()
        request.update(
            dict(
                method="GET",
                url=self._service.BASE_URL + "/res.php",
                params=dict(
                    key=self._service.api_key,
                    json=1
                )
            )
        )
        return request


class GetBalanceRequest(ResRequest):
    """ GetBalance Request class """

    def prepare(self) -> dict:
        """ Prepare request """

        request = super().prepare()
        request["params"].update(dict(action="getbalance"))
        return request

    def parse_response(self, response) -> dict:
        """ Parse response and return balance """

        return {'balance': float(super().parse_response(response)["request"])}


class GetStatusRequest(GetBalanceRequest):
    """ GetStatus Request class """

    def parse_response(self, response) -> dict:
        """ Parse response and return status """

        try:
            return super().parse_response(response)
        except exceptions.UnicapsException:
            return {}


class ReportGoodRequest(ResRequest):
    """ ReportGood Request class """

    # pylint: disable=arguments-differ
    def prepare(self, solved_captcha) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare()
        request["params"].update(
            dict(
                action="reportgood",
                id=solved_captcha.captcha_id
            )
        )
        return request


class ReportBadRequest(ResRequest):
    """ ReportBad Request class """

    # pylint: disable=arguments-differ
    def prepare(self, solved_captcha) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare()
        request["params"].update(
            dict(
                action="reportbad",
                id=solved_captcha.captcha_id
            )
        )
        return request


class TaskRequest(InRequest):
    """ Common Task Request class """

    # pylint: disable=arguments-differ,unused-argument
    def prepare(self, captcha=None, proxy=None, user_agent=None, cookies=None):
        request = super().prepare()

        if proxy:
            request['data'].update(
                dict(
                    proxy=proxy.get_string(),
                    proxytype=proxy.proxy_type.value.upper()
                )
            )

        if cookies:
            request['data']['cookies'] = ';'.join([f'{k}:{v}' for k, v in cookies.items()])

        if user_agent:
            request['data']['userAgent'] = user_agent

        return request

    def parse_response(self, response) -> dict:
        """ Parse response and return task_id """

        response_data = super().parse_response(response)

        return dict(
            task_id=response_data.pop("request"),
            extra=response_data
        )


class SolutionRequest(ResRequest):
    """ Common Solution Request class """

    # pylint: disable=arguments-differ
    def prepare(self, task) -> dict:  # type: ignore
        """ Prepare request """

        # save task
        self._task = task

        request = super().prepare()
        request["params"].update(
            dict(action="get2", id=task.task_id)
        )
        return request

    def parse_response(self, response) -> dict:
        """ Parse response and return solution and cost """

        response_data = super().parse_response(response)

        solution_data = response_data.pop("request")
        solution_class = self._task.captcha.get_solution_class()
        if self._task.captcha.get_type() in (CaptchaType.GEETEST, CaptchaType.CAPY):
            try:
                solution_dict = json.loads(solution_data)
            except json.JSONDecodeError as exc:
                raise exceptions.ServiceError('Got unrecognized data from the service!') from exc

            solution = solution_class(**solution_dict)
        elif self._task.captcha.get_type() in (CaptchaType.TIKTOK,):
            solution = solution_class(
                dict(
                    [key_value.split(':') for key_value in solution_data.split(';')]
                )
            )
        else:
            solution = solution_class(solution_data)

        return dict(
            solution=solution,
            cost=response_data.pop("price"),
            extra=response_data
        )


class ImageCaptchaTaskRequest(TaskRequest):
    """ ImageCaptchaTask Request class """

    # pylint: disable=arguments-differ,unused-argument,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare()

        # add required params
        request['data'].update(
            dict(
                method="base64",
                body=captcha.get_image_base64().decode('ascii')
            )
        )

        # add optional params
        request['data'].update(
            captcha.get_optional_data(
                is_phrase=('phrase', lambda v: int(bool(v))),
                is_case_sensitive=('regsense', lambda v: int(bool(v))),
                char_type=('numeric', lambda v: v.value),
                is_math=('calc', lambda v: int(bool(v))),
                min_len=('min_len', None),
                max_len=('max_len', None),
                alphabet=('language',
                          lambda v: {CaptchaAlphabet.CYRILLIC: 1,
                                     CaptchaAlphabet.LATIN: 2}.get(v, 0)),
                language=('lang', lambda v: v.value),
                comment=('textinstructions', None),
            )
        )

        return request


class ImageCaptchaSolutionRequest(SolutionRequest):
    """ Image CAPTCHA solution request """


class RecaptchaV2TaskRequest(TaskRequest):
    """ reCAPTCHA v2 task request """

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare(
            proxy=proxy,
            user_agent=user_agent,
            cookies=cookies
        )
        request['data'].update(
            dict(
                method="userrecaptcha",
                googlekey=captcha.site_key,
                pageurl=captcha.page_url,
                invisible=int(captcha.is_invisible)
            )
        )

        # add optional params
        request['data'].update(
            captcha.get_optional_data(
                data_s=('data-s', None),
            )
        )

        # check if enterprise captcha
        if captcha.is_enterprise:
            request['data']['enterprise'] = 1

        return request


class RecaptchaV2SolutionRequest(SolutionRequest):
    """ reCAPTCHA v2 solution request """


class RecaptchaV3TaskRequest(TaskRequest):
    """ reCAPTCHA v3 task request """

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare(proxy=proxy)
        request['data'].update(
            dict(
                method="userrecaptcha",
                version="v3",
                googlekey=captcha.site_key,
                pageurl=captcha.page_url
            )
        )

        # add optional params
        request['data'].update(
            captcha.get_optional_data(
                action=('action', None),
                min_score=('min_score', None),
            )
        )

        # check if enterprise captcha
        if captcha.is_enterprise:
            request['data']['enterprise'] = 1

        return request


class RecaptchaV3SolutionRequest(SolutionRequest):
    """ reCAPTCHA v3 solution request """


class TextCaptchaTaskRequest(TaskRequest):
    """ TextCaptcha task request """

    # pylint: disable=arguments-differ,unused-argument,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare()
        request['data'].update(
            dict(
                textcaptcha=captcha.text
            )
        )

        # add optional params
        request['data'].update(
            captcha.get_optional_data(
                alphabet=('language',
                          lambda v: {CaptchaAlphabet.CYRILLIC: 1,
                                     CaptchaAlphabet.LATIN: 2}.get(v, 0)),
                language=('lang', lambda v: v.value)
            )
        )

        return request


class TextCaptchaSolutionRequest(SolutionRequest):
    """ TextCaptcha solution request """


class FunCaptchaTaskRequest(TaskRequest):
    """ FunCaptcha task request """

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare(proxy=proxy, user_agent=user_agent)
        request['data'].update(
            dict(
                method="funcaptcha",
                publickey=captcha.public_key,
                pageurl=captcha.page_url
            )
        )

        # add optional params
        request['data'].update(
            captcha.get_optional_data(
                service_url=('surl', None),
                no_js=('nojs', None)
            )
        )

        return request


class FunCaptchaSolutionRequest(SolutionRequest):
    """ FunCaptcha solution request """


class KeyCaptchaTaskRequest(TaskRequest):
    """ KeyCaptcha task request """

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare()
        request['data'].update(
            dict(
                method="keycaptcha",
                s_s_c_user_id=captcha.user_id,
                s_s_c_session_id=captcha.session_id,
                s_s_c_web_server_sign=captcha.ws_sign,
                s_s_c_web_server_sign2=captcha.ws_sign2,
                pageurl=captcha.page_url
            )
        )

        return request


class KeyCaptchaSolutionRequest(SolutionRequest):
    """ KeyCaptcha solution request """


class GeeTestTaskRequest(TaskRequest):
    """ KeyCaptcha task request """

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare()
        request['data'].update(
            dict(
                method="geetest",
                gt=captcha.gt_key,
                challenge=captcha.challenge,
                pageurl=captcha.page_url
            )
        )

        # add optional params
        request['data'].update(
            captcha.get_optional_data(
                api_server=('api_server', None)
            )
        )

        return request


class GeeTestSolutionRequest(SolutionRequest):
    """ KeyCaptcha solution request """


class HCaptchaTaskRequest(TaskRequest):
    """ HCaptcha task request """

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare(proxy=proxy)
        request['data'].update(
            dict(
                method="hcaptcha",
                sitekey=captcha.site_key,
                pageurl=captcha.page_url
            )
        )

        return request


class HCaptchaSolutionRequest(SolutionRequest):
    """ HCaptcha solution request """


class CapyTaskRequest(TaskRequest):
    """ Capy task request """

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare(proxy=proxy)
        request['data'].update(
            dict(
                method="capy",
                captchakey=captcha.site_key,
                pageurl=captcha.page_url
            )
        )

        # add optional params
        request['data'].update(
            captcha.get_optional_data(
                api_server=('api_server', None)
            )
        )

        return request


class CapySolutionRequest(SolutionRequest):
    """ Capy solution request """


class TikTokCaptchaTaskRequest(TaskRequest):
    """ TikTokCaptcha task request """

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare(proxy=proxy, cookies=cookies)
        request['data'].update(
            dict(
                method="tiktok",
                pageurl=captcha.page_url
            )
        )

        return request


class TikTokCaptchaSolutionRequest(SolutionRequest):
    """ TikTokCaptcha solution request """
