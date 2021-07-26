# -*- coding: UTF-8 -*-
"""
Base transport stuff
"""

from abc import ABC, abstractmethod
from typing import Optional, Any


class BaseRequest(ABC):
    """ Base request class """

    def __init__(self, service):
        self._service = service

    @abstractmethod
    def prepare(self) -> dict:
        """ Prepare request data """
        return {}

    @abstractmethod
    def parse_response(self, response: Any) -> dict:
        """ Parse response """
        return {}


class BaseTransport(ABC):  # pylint: disable=too-few-public-methods
    """ Base transport class """

    def __init__(self, settings: Optional[dict] = None):
        self._settings = settings or {}

    @abstractmethod
    def _make_request(self, request_data: dict) -> Any:
        """ Abstract method to make a request """

    def make_request(self, request: BaseRequest, *args) -> dict:
        """ Makes a request to the service """

        return request.parse_response(
            self._make_request(request.prepare(*args))
        )
