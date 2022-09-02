# -*- coding: UTF-8 -*-
"""
Base service stuff
"""

import asyncio
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from inspect import getmodule
from timeit import default_timer as timer
from typing import Dict, Optional, Tuple

from .._transport.http_transport import StandardHTTPTransport  # type: ignore
from .._captcha import CaptchaType
from .._captcha.base import BaseCaptcha, BaseCaptchaSolution
from .._misc.proxy import ProxyServer
from ..exceptions import UnicapsException, SolutionWaitTimeout, SolutionNotReadyYet


class BaseService(ABC):
    """ Base class for all services """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self._transport = self._init_transport()
        self._module = getmodule(self)
        self._settings = {captcha_type: Settings() for captcha_type in self.supported_captchas}
        self._post_init()

    @abstractmethod
    def _init_transport(self):
        pass

    def _post_init(self):
        pass

    def _make_request(self, request_class, *args):
        request_class = request_class + "Request"
        if not hasattr(self._module, request_class):
            raise UnicapsException(f"{request_class} is not supported by the current service!")

        request = getattr(self._module, request_class)(self)
        return self._transport.make_request(request, *args)

    async def _make_request_async(self, request_class, *args):
        request_class = request_class + "Request"
        if not hasattr(self._module, request_class):
            raise UnicapsException(f"{request_class} is not supported by the current service!")

        request = getattr(self._module, request_class)(self)
        return await self._transport.make_request_async(request, *args)

    @property
    def supported_captchas(self) -> Tuple[CaptchaType, ...]:
        """ List of supported captchas """

        captchas = []
        for captcha_type in CaptchaType:
            if hasattr(self._module, captcha_type.value + "TaskRequest"):
                captchas.append(captcha_type)
        return tuple(captchas)

    @property
    def settings(self) -> Dict[CaptchaType, 'Settings']:
        """ Service settings """

        return self._settings

    def solve_captcha(self, captcha: BaseCaptcha, proxy: Optional[ProxyServer] = None,
                      user_agent: Optional[str] = None,
                      cookies: Optional[Dict[str, str]] = None) -> 'SolvedCaptcha':
        """ Solves captcha and returns SolvedCaptcha object """

        start_time = datetime.now()
        task = self.create_task(captcha, proxy, user_agent, cookies)
        solution, cost, extra = self.wait_for_solution(task)
        end_time = datetime.now()

        return SolvedCaptcha(task, solution, start_time, end_time,
                             cost=cost, extra=extra)

    async def solve_captcha_async(self, captcha: BaseCaptcha, proxy: Optional[ProxyServer] = None,
                                  user_agent: Optional[str] = None,
                                  cookies: Optional[Dict[str, str]] = None) -> 'AsyncSolvedCaptcha':
        """ Solves captcha and returns SolvedCaptcha object (async) """

        start_time = datetime.now()
        task = await self.create_task_async(captcha, proxy, user_agent, cookies)
        solution, cost, extra = await self.wait_for_solution_async(task)
        end_time = datetime.now()

        return AsyncSolvedCaptcha(task, solution, start_time, end_time,
                                  cost=cost, extra=extra)

    def create_task(self, captcha: BaseCaptcha, proxy: Optional[ProxyServer] = None,
                    user_agent: Optional[str] = None,
                    cookies: Optional[Dict[str, str]] = None) -> 'CaptchaTask':
        """ Creates task for solving a CAPTCHA """

        captcha_type = captcha.get_type()

        if captcha_type not in self.supported_captchas:
            raise UnicapsException(f"{captcha_type} is not supported by the current service!")

        result = self._make_request(
            f"{captcha_type.value}Task", captcha, proxy, user_agent, cookies
        )
        task_id = str(result["task_id"])

        return CaptchaTask(self, captcha, task_id, result.get("extra"))

    async def create_task_async(self, captcha: BaseCaptcha, proxy: Optional[ProxyServer] = None,
                                user_agent: Optional[str] = None,
                                cookies: Optional[Dict[str, str]] = None) -> 'AsyncCaptchaTask':
        """ Creates CAPTCHA solving task (async) """

        captcha_type = captcha.get_type()

        if captcha_type not in self.supported_captchas:
            raise UnicapsException(f"{captcha_type} is not supported by the current service!")

        result = await self._make_request_async(
            f"{captcha_type.value}Task", captcha, proxy, user_agent, cookies
        )
        task_id = str(result["task_id"])

        return AsyncCaptchaTask(self, captcha, task_id, result.get("extra"))

    def get_task_result(self, task: 'CaptchaTask') -> Tuple[BaseCaptchaSolution,
                                                            Optional[float], Dict]:
        """ Returns CAPTCHA solution """

        result = self._make_request(f"{task.captcha.get_type().value}Solution", task)

        return (
            result['solution'],  # type: ignore
            float(result['cost']) if result.get('cost') else None,
            result.get("extra") or {}
        )

    async def get_task_result_async(self, task: 'CaptchaTask') -> Tuple[BaseCaptchaSolution,
                                                                        Optional[float], Dict]:
        """ Returns CAPTCHA solution """

        result = await self._make_request_async(f"{task.captcha.get_type().value}Solution", task)

        return (
            result['solution'],  # type: ignore
            float(result['cost']) if result.get('cost') else None,
            result.get("extra") or {}
        )

    def wait_for_solution(self, task) -> Tuple[BaseCaptchaSolution, Optional[float], Dict]:
        """ Wait for CAPTCHA solution """

        settings = self._settings[task.captcha.get_type()]

        start_time = timer()
        time.sleep(settings.polling_delay)
        while True:
            if timer() - start_time > settings.solution_timeout:
                raise SolutionWaitTimeout(
                    f"Couldn't receive a solution in {settings.solution_timeout} seconds!"
                )

            try:
                return task.get_result()
            except SolutionNotReadyYet:
                time.sleep(settings.polling_interval)

    async def wait_for_solution_async(self, task) -> Tuple[BaseCaptchaSolution,
                                                           Optional[float], Dict]:
        """ Wait for CAPTCHA solution """

        settings = self._settings[task.captcha.get_type()]

        start_time = timer()
        await asyncio.sleep(settings.polling_delay)
        while True:
            if timer() - start_time > settings.solution_timeout:
                raise SolutionWaitTimeout(
                    f"Couldn't receive a solution in {settings.solution_timeout} seconds!"
                )

            try:
                return await task.get_result()
            except SolutionNotReadyYet:
                await asyncio.sleep(settings.polling_interval)

    def get_balance(self):
        """ Get account balance """

        balance = self._make_request("GetBalance").get('balance')
        if balance is not None:
            balance = float(balance)
        return balance

    async def get_balance_async(self):
        """ Get account balance """

        response = await self._make_request_async("GetBalance")
        balance = response.get('balance')
        if balance is not None:
            balance = float(balance)
        return balance

    def get_status(self) -> bool:
        """ Get service status """

        return bool(self._make_request("GetStatus"))

    async def get_status_async(self) -> bool:
        """ Get service status """

        return bool(await self._make_request_async("GetStatus"))

    def report_good(self, solved_captcha: 'SolvedCaptcha', raise_exc: bool = False) -> bool:
        """ Report good CAPTCHA """

        result = False
        try:
            result = self._make_request("ReportGood", solved_captcha)
        except UnicapsException:
            if raise_exc:
                raise
        return bool(result)

    async def report_good_async(self, solved_captcha: 'SolvedCaptcha',
                                raise_exc: bool = False) -> bool:
        """ Report good CAPTCHA """

        result = False
        try:
            result = await self._make_request_async("ReportGood", solved_captcha)
        except UnicapsException:
            if raise_exc:
                raise
        return bool(result)

    def report_bad(self, solved_captcha: 'SolvedCaptcha', raise_exc: bool = False) -> bool:
        """ Report bad CAPTCHA """

        result = False
        try:
            result = self._make_request("ReportBad", solved_captcha)
        except UnicapsException:
            if raise_exc:
                raise
        return bool(result)

    async def report_bad_async(self, solved_captcha: 'SolvedCaptcha',
                               raise_exc: bool = False) -> bool:
        """ Report bad CAPTCHA """

        result = False
        try:
            result = await self._make_request_async("ReportBad", solved_captcha)
        except UnicapsException:
            if raise_exc:
                raise
        return bool(result)

    @abstractmethod
    def close(self):
        """ Close connections """

    @abstractmethod
    async def close_async(self):
        """ Close connections (async) """


class HTTPService(BaseService):
    """ Standard HTTP Service """

    def _init_transport(self):
        return StandardHTTPTransport()

    def close(self):
        """ Close connections """
        self._transport.close()

    async def close_async(self):
        """ Close connections (async) """
        await self._transport.close_async()


@dataclass
class Settings:
    """ Service settings """

    polling_delay: int = 5  # seconds before starting to check for sollution
    polling_interval: int = 2  # seconds between checks
    solution_timeout: int = 300  # seconds is solution timeout


class CaptchaTask:
    """ Task for CAPTCHA solving """

    def __init__(self, service, captcha: BaseCaptcha, task_id: str, extra: Dict = None):
        self._service = service
        self._captcha = captcha
        self._task_id = task_id
        self._extra = extra or {}
        self._result = None

    @property
    def task_id(self) -> str:
        """ Task ID """
        return self._task_id

    @property
    def captcha(self) -> BaseCaptcha:
        """ Source CAPTCHA """
        return self._captcha

    @property
    def extra(self) -> Dict:
        """ Task extra data """
        return self._extra

    def get_result(self) -> Optional[BaseCaptchaSolution]:
        """ Gets solution """
        if self._result is None:
            self._result = self._service.get_task_result(self)
        return self._result

    def is_done(self) -> bool:
        """ Checks if solution is ready """
        return bool(self._result)

    def wait(self) -> BaseCaptchaSolution:
        """ Waits for solution """
        return self._service.wait_for_solution(self)


class AsyncCaptchaTask(CaptchaTask):
    """ Task for CAPTCHA solving """

    async def get_result(self) -> Optional[BaseCaptchaSolution]:  # type: ignore
        """ Gets solution """
        if self._result is None:
            self._result = await self._service.get_task_result_async(self)
        return self._result

    async def wait(self) -> BaseCaptchaSolution:  # type: ignore
        """ Waits for solution """
        return await self._service.wait_for_solution_async(self)


class SolvedCaptcha:
    """ Solved CAPTCHA object """

    def __init__(self, task: CaptchaTask, solution: BaseCaptchaSolution, start_time: datetime,
                 end_time: datetime, cost: Optional[float] = None, cookies: Optional[dict] = None,
                 extra: dict = None):
        if not task.is_done():
            raise UnicapsException("CAPTCHA is not solved yet!")

        self._task = task
        self._solution = solution
        self._start_time = start_time
        self._end_time = end_time
        self._cost = cost
        self._cookies = cookies or {}
        self._extra = extra or {}

    @property
    def captcha_id(self) -> str:
        """ CAPTCHA ID (usually it's the same as task ID) """
        return self._task.task_id

    @property
    def task(self) -> CaptchaTask:
        """ Task for solving """
        return self._task

    @property
    def solution(self) -> BaseCaptchaSolution:
        """ CAPTCHA solution """
        return self._solution

    @property
    def start_time(self) -> datetime:
        """ Start solving at """
        return self._start_time

    @property
    def end_time(self) -> datetime:
        """ End solving at """
        return self._end_time

    @property
    def cost(self) -> Optional[float]:
        """ The cost of solved CAPTCHA """
        return self._cost

    @property
    def cookies(self) -> dict:
        """ Cookies """
        return self._cookies

    @property
    def extra(self) -> dict:
        """ Extra data from the service """
        return self._extra

    def report_good(self, raise_exc: bool = False) -> bool:
        """ Report good CAPTCHA """
        # pylint: disable=protected-access
        return self._task._service.report_good(self, raise_exc=raise_exc)

    def report_bad(self, raise_exc: bool = False) -> bool:
        """ Report bad CAPTCHA """
        # pylint: disable=protected-access
        return self._task._service.report_bad(self, raise_exc=raise_exc)


class AsyncSolvedCaptcha(SolvedCaptcha):
    """ Solved CAPTCHA object (async) """

    async def report_good(self, raise_exc: bool = False) -> bool:  # type: ignore
        """ Report good CAPTCHA """
        # pylint: disable=protected-access
        return await self._task._service.report_good_async(self, raise_exc=raise_exc)

    async def report_bad(self, raise_exc: bool = False) -> bool:  # type: ignore
        """ Report bad CAPTCHA """
        # pylint: disable=protected-access
        return await self._task._service.report_bad_async(self, raise_exc=raise_exc)
