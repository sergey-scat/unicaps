# -*- coding: UTF-8 -*-
"""
Transport and requests for HTTP protocol
"""

from json.decoder import JSONDecodeError
from typing import Optional, Dict

import requests
from urllib3.util.retry import Retry  # type:ignore

from .base import BaseTransport, BaseRequest  # type: ignore
from ..exceptions import NetworkError, ServiceError  # type: ignore
from ..__version__ import __version__  # type: ignore


HTTP_RETRY_MAX_COUNT = 5  # max retry count in case of http(s) errors
HTTP_RETRY_BACKOFF_FACTOR = 0.5  # backoff factor for Retry
HTTP_RETRY_STATUS_FORCELIST = {500, 502, 503, 504}  # status forcelist for Retry


class StandardHTTPTransport(BaseTransport):  # pylint: disable=too-few-public-methods
    """ Standard HTTP Transport """

    def __init__(self, settings: Optional[Dict] = None):
        super().__init__(settings)
        self._settings.setdefault('max_retries', HTTP_RETRY_MAX_COUNT)
        self._settings.setdefault('handle_http_errors', True)

        self.session = requests.Session()
        self.session.mount(
            'http://',
            requests.adapters.HTTPAdapter(
                max_retries=Retry(
                    total=self._settings['max_retries'],
                    backoff_factor=HTTP_RETRY_BACKOFF_FACTOR,
                    status_forcelist=HTTP_RETRY_STATUS_FORCELIST
                )
            )
        )
        self.session.mount(
            'https://',
            requests.adapters.HTTPAdapter(
                max_retries=Retry(
                    total=self._settings['max_retries'],
                    backoff_factor=HTTP_RETRY_BACKOFF_FACTOR,
                    status_forcelist=HTTP_RETRY_STATUS_FORCELIST
                )
            )
        )

    def _make_request(self, request_data: Dict) -> requests.Response:
        if 'headers' not in request_data:
            request_data['headers'] = {}

        if 'User-Agent' not in request_data['headers']:
            request_data['headers']['User-Agent'] = 'python-unicaps/%s' % __version__

        try:
            response = self.session.request(**request_data)
        except requests.ConnectionError as exc:
            raise NetworkError('ConnectionError') from exc
        except requests.Timeout as exc:
            raise NetworkError('Timeout') from exc

        if self._settings['handle_http_errors']:
            try:
                response.raise_for_status()
            except requests.HTTPError as exc:
                raise NetworkError('HTTPError') from exc

        return response


class HTTPRequestJSON(BaseRequest):
    """ HTTP Request that returns JSON response """

    def prepare(self) -> Dict:
        """ Prepares request """

        request = super().prepare()
        request.update(
            dict(headers={'Accept': 'application/json',
                          'Content-Type': 'application/json'})
        )
        return request

    def parse_response(self, response: requests.Response) -> Dict:  # pylint: disable=no-self-use
        """ Parses response """

        try:
            return response.json()
        except JSONDecodeError as exc:
            raise ServiceError("Unable to parse response from the server: bad JSON") from exc
