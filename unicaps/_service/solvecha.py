# -*- coding: UTF-8 -*-
"""
solvecha.com service
"""

from .base import HTTPService
from .._transport.http_transport import HTTPRequestJSON, StandardHTTPTransport  # type: ignore
from .. import exceptions

__all__ = [
    'Service', 'GetBalanceRequest', 'GetStatusRequest',
    'ReportGoodRequest', 'ReportBadRequest',
    'ImageCaptchaTaskRequest', 'ImageCaptchaSolutionRequest',
]


class Service(HTTPService):
    """ Main service class for solvecha.com (image CAPTCHAs only) """

    BASE_URL = 'https://api.solvecha.com'

    def _init_transport(self):
        # the API answers errors with a 4xx status and a JSON body,
        # so the response is parsed by the Request classes
        return StandardHTTPTransport({'handle_http_errors': False})

    def _post_init(self):
        """ Init settings """

        for captcha_type in self.settings:
            self.settings[captcha_type].polling_delay = 2
            self.settings[captcha_type].polling_interval = 2
            self.settings[captcha_type].solution_timeout = 90


class Request(HTTPRequestJSON):
    """ Common Request class for solvecha.com """

    def prepare(self, **kwargs) -> dict:
        """ Prepares request """

        request = super().prepare(**kwargs)
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

        error_id = response_data.pop("errorId", 0)
        if error_id == 0:
            return response_data

        # ############# #
        # handle errors #
        # ############# #
        error_code = response_data.get("errorCode") or f'ERROR {error_id}'
        error_text = response_data.get("errorDescription", "")
        error_msg = f"{error_code}: {error_text}"

        # pylint: disable=no-else-raise
        if error_code in ('ERROR_KEY_DENIED_ACCESS',):
            raise exceptions.AccessDeniedError(error_msg)
        elif error_code in ('ERROR_ZERO_BALANCE',):
            raise exceptions.LowBalanceError(error_msg)
        elif error_code in ('ERROR_RATE_LIMIT',):
            raise exceptions.TooManyRequestsError(error_msg)
        elif error_code in ('ERROR_NO_SUCH_METHOD', 'ERROR_TASK_NOT_SUPPORTED'):
            raise exceptions.MalformedRequestError(error_msg)
        elif error_code in ('ERROR_INVALID_TASK_DATA',):
            raise exceptions.BadInputDataError(error_msg)
        elif error_code in ('ERROR_CAPTCHA_UNSOLVABLE',):
            raise exceptions.UnableToSolveError(error_msg)

        raise exceptions.ServiceError(error_msg)


class GetBalanceRequest(Request):
    """ GetBalance Request class """

    def prepare(self) -> dict:   # type: ignore
        """ Prepares request """

        request = super().prepare()
        request.update(dict(url=self._service.BASE_URL + "/getBalance"))

        return request

    def parse_response(self, response) -> dict:
        """ Parses response and returns the prepaid balance """

        return dict(balance=float(super().parse_response(response)['balance']))


class GetStatusRequest(GetBalanceRequest):
    """ GetStatus Request class """

    def parse_response(self, response) -> dict:
        """ Parses response and returns balance or an empty dict """

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

        raise exceptions.UnicapsException(
            "Report for bad CAPTCHA is not supported by the current service!"
        )


class TaskRequest(Request):
    """ Request class for requests to /createTask """

    # pylint: disable=arguments-differ,unused-argument
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepare a request """

        request = super().prepare(
            captcha=captcha,
            proxy=proxy,
            user_agent=user_agent,
            cookies=cookies
        )

        request.update(dict(url=self._service.BASE_URL + "/createTask"))
        request["json"].update(dict(task={}))

        return request

    def parse_response(self, response) -> dict:
        """ Parses response and returns task_id """

        response_data = super().parse_response(response)

        # the solution may already be in this response, it is fetched by /getTaskResult
        return {"task_id": response_data.pop("taskId"),
                "extra": {}}


class SolutionRequest(Request):
    """ Request class for requests to /getTaskResult """

    # pylint: disable=arguments-differ
    def prepare(self, task) -> dict:  # type: ignore
        """ Prepare a request """

        request = super().prepare(task=task)
        request.update(dict(url=self._service.BASE_URL + "/getTaskResult"))
        request["json"].update(dict(taskId=str(task.task_id)))

        return request

    def parse_response(self, response) -> dict:
        """ Parses response and returns solution and cost """

        response_data = super().parse_response(response)

        if response_data["status"] != "ready":
            raise exceptions.SolutionNotReadyYet()

        solution_class = self.source_data['task'].captcha.get_solution_class()
        solution = solution_class(response_data["solution"]["text"])

        return dict(
            solution=solution,
            cost=response_data.get("cost"),
            extra={}
        )


class ImageCaptchaTaskRequest(TaskRequest):
    """ ImageCaptchaTask Request class """

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepare a request """

        request = super().prepare(
            captcha=captcha,
            proxy=None,
            user_agent=None,
            cookies=None
        )
        request['json']['task'].update(
            dict(
                type="ImageToTextTask",
                body=captcha.get_image_base64().decode('ascii')
            )
        )

        return request


class ImageCaptchaSolutionRequest(SolutionRequest):
    """ Image CAPTCHA solution request """
