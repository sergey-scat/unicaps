# -*- coding: UTF-8 -*-
"""
anti-captcha.com service
"""

from .base import HTTPService
from .._transport.http_transport import HTTPRequestJSON  # type: ignore
from .. import exceptions
from .._captcha import CaptchaType
from ..common import WorkerLanguage

__all__ = [
    'Service', 'GetBalanceRequest', 'GetStatusRequest',
    'ReportGoodRequest', 'ReportBadRequest',
    'ImageCaptchaTaskRequest', 'ImageCaptchaSolutionRequest',
    'RecaptchaV2TaskRequest', 'RecaptchaV2SolutionRequest',
    'RecaptchaV3TaskRequest', 'RecaptchaV3SolutionRequest',
    'FunCaptchaTaskRequest', 'FunCaptchaSolutionRequest',
    'GeeTestTaskRequest', 'GeeTestSolutionRequest',
    'HCaptchaTaskRequest', 'HCaptchaSolutionRequest',
]


class Service(HTTPService):
    """ Main service class for anti-captcha """

    BASE_URL = 'https://api.anti-captcha.com'

    def _post_init(self):
        """ Init settings """

        for captcha_type in self._settings:
            self._settings[captcha_type].polling_interval = 2

            if captcha_type in (CaptchaType.IMAGE,):
                self._settings[captcha_type].polling_delay = 5
                self._settings[captcha_type].solution_timeout = 90
            else:
                self._settings[captcha_type].polling_delay = 10
                self._settings[captcha_type].solution_timeout = 300


class Request(HTTPRequestJSON):
    """ Common Request class for anti-captcha """

    def prepare(self) -> dict:
        """ Prepares request """

        request = super().prepare()
        request.update(
            dict(
                method="POST",
                json=dict(clientKey=self._service.api_key)
            )
        )
        return request

    def parse_response(self, response) -> dict:
        """ Parses response and checks for errors """

        response_data = super().parse_response(response)

        error_id = response_data.pop("errorId")
        if error_id == 0:
            return response_data

        ###############
        # handle errors
        ###############
        error_code = response_data.get("errorCode", f'ERROR {error_id}')
        error_text = response_data.get("errorDescription", "")
        error_msg = "{}: {}".format(error_code, error_text)

        # pylint: disable=no-else-raise
        if error_code in ('ERROR_WRONG_USER_KEY', 'ERROR_KEY_DOES_NOT_EXIST',
                          'ERROR_IP_NOT_ALLOWED', 'ERROR_IP_BLOCKED'):
            raise exceptions.AccessDeniedError(error_msg)
        elif error_code in ('ERROR_ZERO_BALANCE',):
            raise exceptions.LowBalanceError(error_msg)
        elif error_code in ('ERROR_NO_SLOT_AVAILABLE',):
            raise exceptions.ServiceTooBusy(error_msg)
        elif error_code in ('ERROR_NO_SUCH_METHOD', 'ERROR_NO_SUCH_CAPCHA_ID', 'ERROR_TASK_ABSENT',
                            'ERROR_TASK_NOT_SUPPORTED', 'ERROR_FUNCAPTCHA_NOT_ALLOWED'):
            raise exceptions.MalformedRequestError(error_msg)
        elif error_code in ('ERROR_ZERO_CAPTCHA_FILESIZE', 'ERROR_TOO_BIG_CAPTCHA_FILESIZE',
                            'ERROR_WRONG_FILE_EXTENSION', 'ERROR_IMAGE_TYPE_NOT_SUPPORTED',
                            'ERROR_UPLOAD', 'ERROR_PAGEURL', 'ERROR_BAD_TOKEN_OR_PAGEURL',
                            'ERROR_GOOGLEKEY', 'ERROR_EMPTY_COMMENT',
                            'ERROR_INCORRECT_SESSION_DATA', 'ERROR_RECAPTCHA_INVALID_SITEKEY',
                            'ERROR_RECAPTCHA_INVALID_DOMAIN', 'ERROR_RECAPTCHA_OLD_BROWSER',
                            'ERROR_TOKEN_EXPIRED', 'ERROR_INVISIBLE_RECAPTCHA'):
            raise exceptions.BadInputDataError(error_msg)
        elif error_code in ('ERROR_CAPTCHAIMAGE_BLOCKED', 'ERROR_CAPTCHA_UNSOLVABLE',
                            'ERROR_BAD_DUPLICATES', 'ERROR_RECAPTCHA_TIMEOUT',
                            'ERROR_FAILED_LOADING_WIDGET'):
            raise exceptions.UnableToSolveError(error_msg)
        elif error_code in ('ERROR_PROXY_CONNECT_REFUSED', 'ERROR_PROXY_CONNECT_TIMEOUT',
                            'ERROR_PROXY_READ_TIMEOUT', 'ERROR_PROXY_BANNED',
                            'ERROR_PROXY_TRANSPARENT', 'ERROR_PROXY_HAS_NO_IMAGE_SUPPORT',
                            'ERROR_PROXY_INCOMPATIBLE_HTTP_VERSION', 'ERROR_PROXY_NOT_AUTHORISED'):
            raise exceptions.ProxyError(error_msg)

        raise exceptions.ServiceError(error_msg)


class GetBalanceRequest(Request):
    """ GetBalance Request class """

    def prepare(self) -> dict:
        """ Prepares request """

        request = super().prepare()
        request.update(dict(url=self._service.BASE_URL + "/getBalance"))

        return request

    def parse_response(self, response) -> dict:
        """ Parses response and returns task_id """

        return dict(balance=float(super().parse_response(response)['balance']))


class GetStatusRequest(GetBalanceRequest):
    """ GetStatus Request class """

    def parse_response(self, response) -> dict:
        """ Parses response and returns task_id """

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


class ReportBadRequest(Request):
    """ ReportBad Request class """

    # pylint: disable=arguments-differ
    def prepare(self, solved_captcha) -> dict:  # type: ignore
        """ Prepares request """

        request = super().prepare()

        captcha_type = solved_captcha.task.captcha.get_type()

        if captcha_type == CaptchaType.IMAGE:
            uri = "/reportIncorrectImageCaptcha"
        elif captcha_type in (CaptchaType.RECAPTCHAV2, CaptchaType.RECAPTCHAV3):
            uri = "/reportIncorrectRecaptcha"
        else:
            raise exceptions.UnicapsException(
                f"Report for bad {captcha_type.value} is not supported!"
            )

        request.update(dict(url=self._service.BASE_URL + uri))
        request["json"].update(dict(taskId=int(solved_captcha.captcha_id)))
        return request


class TaskRequest(Request):
    """ Request class for requests to /createTask """

    # pylint: disable=arguments-differ,unused-argument
    def prepare(self, captcha=None, proxy=None, user_agent=None, cookies=None) -> dict:
        """ Prepares request """

        request = super().prepare()
        request.update(dict(url=self._service.BASE_URL + "/createTask"))
        request["json"].update(
            dict(
                task=dict(),
                softId=940
            )
        )

        # add proxy
        if proxy:
            request["json"]["task"].update(
                dict(
                    proxyType=proxy.proxy_type.value,
                    proxyAddress=proxy.address,
                    proxyPort=proxy.port
                )
            )

            if proxy.login:
                request["json"]["task"].update(
                    dict(
                        proxyLogin=proxy.login,
                        proxyPassword=proxy.password
                    )
                )

        if user_agent:
            request["json"]["task"]["userAgent"] = user_agent

        if cookies:
            request["json"]["task"]["cookies"] = '; '.join(f'{k}={v}'for k, v in cookies.items())

        return request

    def parse_response(self, response) -> dict:
        """ Parses response and returns task_id """

        response_data = super().parse_response(response)

        return {"task_id": response_data.pop("taskId"),
                "extra": response_data}


class SolutionRequest(Request):
    """ Request class for requests to /getTaskResult """

    # pylint: disable=arguments-differ
    def prepare(self, task) -> dict:  # type: ignore
        """ Prepares request """

        # save task
        self._task = task

        request = super().prepare()
        request.update(dict(url=self._service.BASE_URL + "/getTaskResult"))
        request["json"].update(dict(taskId=str(task.task_id)))

        return request

    def parse_response(self, response) -> dict:
        """ Parses response and returns solution and cost """

        response_data = super().parse_response(response)

        if response_data["status"] != "ready":
            raise exceptions.SolutionNotReadyYet()

        solution_data = response_data["solution"]
        solution_class = self._task.captcha.get_solution_class()
        captcha_type = self._task.captcha.get_type()
        args = []
        kwargs = {}
        if captcha_type in (CaptchaType.IMAGE,):
            args.append(solution_data.pop('text'))
        elif captcha_type in (CaptchaType.RECAPTCHAV2, CaptchaType.RECAPTCHAV3,
                              CaptchaType.HCAPTCHA):
            args.append(solution_data.pop('gRecaptchaResponse'))
        elif captcha_type in (CaptchaType.FUNCAPTCHA,):
            args.append(solution_data.pop('token'))
        elif captcha_type in (CaptchaType.GEETEST,):
            kwargs.update(solution_data)
        else:
            kwargs.update(solution_data)

        solution = solution_class(*args, **kwargs)

        return dict(
            solution=solution,
            cost=response_data.pop("cost"),
            extra=response_data
        )


class ImageCaptchaTaskRequest(TaskRequest):
    """ ImageCaptchaTask Request class """

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepares request """

        request = super().prepare()

        task_data = dict(
            type="ImageToTextTask",
            body=captcha.get_image_base64().decode('ascii')
        )
        task_data.update(
            captcha.get_optional_data(
                is_case_sensitive=('case', None),
                is_phrase=('phrase', None),
                is_math=('math', None),
                char_type=('numeric', lambda v: v.value if v.value in (1, 2) else None),
                min_len=('minLength', None),
                max_len=('maxLength', None),
                comment=('comment', None)
            )
        )
        request['json']['task'].update(task_data)

        # set workers pool language
        if captcha.language:
            request['json']['languagePool'] = (
                'rn' if captcha.language == WorkerLanguage.RUSSIAN else 'en'
            )

        return request


class ImageCaptchaSolutionRequest(SolutionRequest):
    """ Image CAPTCHA solution request """

    #def parse_response(self, response) -> dict:
        #""" Parses response and returns solution and cost """

        #response_data = super().parse_response(response)

        #return dict(
            #solution=response_data["solution"].pop("text"),
            #cost=response_data.pop("cost"),
            #extra=response_data
        #)


class RecaptchaV2TaskRequest(TaskRequest):
    """ reCAPTCHA v2 task Request class """

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepares request """

        if proxy:
            kwargs = dict(captcha=captcha, proxy=proxy, user_agent=user_agent, cookies=cookies)
            task_type = "NoCaptchaTask"
        else:
            kwargs = dict(captcha=captcha)
            task_type = "NoCaptchaTaskProxyless"

        request = super().prepare(**kwargs)
        request['json']['task'].update(
            dict(
                type=task_type,
                websiteURL=captcha.page_url,
                websiteKey=captcha.site_key,
                isInvisible=captcha.is_invisible
            )
        )
        # set optional data if any
        request['json']['task'].update(
            captcha.get_optional_data(
                data_s=('recaptchaDataSValue', None)
            )
        )

        return request


class RecaptchaV2SolutionRequest(SolutionRequest):
    """ reCAPTCHA v2 solution request """

    #def parse_response(self, response) -> dict:
        #""" Parses response and returns solution and cost """

        #response_data = super().parse_response(response)

        #return dict(
            #solution=response_data["solution"].pop("gRecaptchaResponse"),
            #cost=response_data.pop("cost"),
            #extra=response_data
        #)


class RecaptchaV3TaskRequest(TaskRequest):
    """ reCAPTCHA v3 task Request class """

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepares request """

        request = super().prepare()
        request['json']['task'].update(
            dict(
                type="RecaptchaV3TaskProxyless",
                websiteURL=captcha.page_url,
                websiteKey=captcha.site_key,
                # minScore=captcha.min_score,
                # pageAction=captcha.action
            )
        )
        # set optional data if any
        request['json']['task'].update(
            captcha.get_optional_data(
                min_score=('minScore', None),
                action=('pageAction', None),
            )
        )

        return request


class RecaptchaV3SolutionRequest(SolutionRequest):
    """ reCAPTCHA v3 solution request """

    #def parse_response(self, response) -> dict:
        #""" Parses response and returns solution and cost """

        #response_data = super().parse_response(response)

        #return dict(
            #solution=response_data["solution"].pop("gRecaptchaResponse"),
            #cost=response_data.pop("cost"),
            #extra=response_data
        #)


class FunCaptchaTaskRequest(TaskRequest):
    """ FunCaptcha task Request class """

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepares request """

        if proxy:
            kwargs = dict(captcha=captcha, proxy=proxy, user_agent=user_agent, cookies=cookies)
            task_type = "FunCaptchaTask"
        else:
            kwargs = dict(captcha=captcha)
            task_type = "FunCaptchaTaskProxyless"

        request = super().prepare(**kwargs)
        request['json']['task'].update(
            dict(
                type=task_type,
                websiteURL=captcha.page_url,
                websitePublicKey=captcha.public_key
            )
        )
        # set optional data if any
        request['json']['task'].update(
            captcha.get_optional_data(
                service_url=('funcaptchaApiJSSubdomain', None),
            )
        )

        return request


class FunCaptchaSolutionRequest(SolutionRequest):
    """ FunCaptcha solution request """

    #def parse_response(self, response) -> dict:
        #""" Parses response and returns solution and cost """

        #response_data = super().parse_response(response)

        #return dict(
            #solution=response_data["solution"].pop("token"),
            #cost=response_data.pop("cost"),
            #extra=response_data
        #)


class GeeTestTaskRequest(TaskRequest):
    """ GeeTest task Request class """

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepares request """

        if proxy:
            kwargs = dict(captcha=captcha, proxy=proxy, user_agent=user_agent, cookies=cookies)
            task_type = "GeeTestTask"
        else:
            kwargs = dict(captcha=captcha)
            task_type = "GeeTestTaskProxyless"

        request = super().prepare(**kwargs)
        request['json']['task'].update(
            dict(
                type=task_type,
                websiteURL=captcha.page_url,
                gt=captcha.gt_key,
                challenge=captcha.challenge,
                geetestApiServerSubdomain=captcha.api_server
            )
        )

        return request


class GeeTestSolutionRequest(SolutionRequest):
    """ GeeTest solution request """

    #def parse_response(self, response) -> dict:
        #""" Parses response and returns solution and cost """

        #response_data = super().parse_response(response)

        #return dict(
            #solution=response_data["solution"].pop("challenge"),
            #cost=response_data.pop("cost"),
            #extra=response_data
        #)


class HCaptchaTaskRequest(TaskRequest):
    """ hCaptcha task Request class """

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepares request """

        if proxy:
            kwargs = dict(captcha=captcha, proxy=proxy, user_agent=user_agent, cookies=cookies)
            task_type = "HCaptchaTask"
        else:
            kwargs = dict(captcha=captcha)
            task_type = "HCaptchaTaskProxyless"

        request = super().prepare(**kwargs)
        request['json']['task'].update(
            dict(
                type=task_type,
                websiteURL=captcha.page_url,
                websiteKey=captcha.site_key
            )
        )

        return request


class HCaptchaSolutionRequest(SolutionRequest):
    """ hCaptcha solution request """

    #def parse_response(self, response) -> dict:
        #""" Parses response and returns solution and cost """

        #response_data = super().parse_response(response)

        #return dict(
            #solution=response_data["solution"].pop("gRecaptchaResponse"),
            #cost=response_data.pop("cost"),
            #extra=response_data
        #)
