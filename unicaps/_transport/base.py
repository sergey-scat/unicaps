# -*- coding: UTF-8 -*-
"""
Base transport stuff
"""

from abc import ABC, abstractmethod
from typing import Optional, Any


class BaseRequest(ABC):
    """ Base request class """

    def __init__(self, service):
        # solving service instance
        self._service = service
        # source request data (not None if a request in process)
        self.source_data = None

    @abstractmethod
    def prepare(self, **kwargs) -> dict:
        """ Prepare request data """
        self.source_data = kwargs
        return {}

    @abstractmethod
    def parse_response(self, response: Any) -> dict:
        """ Parse response """
        if self.source_data is None:
            raise RuntimeError('The Request.prepare() method must be called first!')
        return {}

    def process_response(self, response: Any) -> dict:
        """ Parse response and clean source request data """
        response = self.parse_response(response)
        self.source_data = None
        return response


class BaseTransport(ABC):  # pylint: disable=too-few-public-methods
    """ Base transport class """

    def __init__(self, settings: Optional[dict] = None):
        self.settings = settings or {}

    @abstractmethod
    def _make_request(self, request_data: dict) -> Any:
        """ Abstract method to make a request """

    @abstractmethod
    async def _make_request_async(self, request_data: dict) -> Any:
        """ Abstract method to make a request """

    def make_request(self, request: BaseRequest, *args) -> dict:
        """ Makes a request to the service """
        response = self._make_request(request.prepare(*args))
        return request.process_response(response)

    async def make_request_async(self, request: BaseRequest, *args) -> dict:
        """ Makes a request to the service """
        response = await self._make_request_async(request.prepare(*args))
        return request.process_response(response)

    @abstractmethod
    def close(self):
        """ Close connections """

    @abstractmethod
    async def close_async(self):
        """ Close connections (async) """
