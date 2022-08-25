# -*- coding: UTF-8 -*-
"""
Transport and requests for HTTP protocol
"""

from json.decoder import JSONDecodeError
from typing import Optional, Dict

import httpx

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

        default_headers = {
            'User-Agent': f'python-unicaps/{__version__}'
        }

        self.session = httpx.Client(
            headers=default_headers,
            timeout=httpx.Timeout(timeout=30)
        )

    def _make_request(self, request_data: Dict) -> httpx.Response:
        if 'headers' not in request_data:
            request_data['headers'] = {}

        try:
            response = self.session.request(**request_data)
        except httpx.TimeoutException as exc:
            raise NetworkError('Timeout') from exc
        except httpx.RequestError as exc:
            raise NetworkError('RequestError') from exc

        if self._settings['handle_http_errors']:
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as exc:
                raise NetworkError('HTTPStatusError') from exc

        return response

    def close(self):
        """ Close connections """
        self.session.close()


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

    def parse_response(self, response: httpx.Response) -> Dict:
        """ Parses response """

        try:
            return response.json()
        except JSONDecodeError as exc:
            raise ServiceError("Unable to parse response from the server: bad JSON") from exc
