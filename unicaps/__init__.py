# -*- coding: UTF-8 -*-
"""
Unicaps package
~~~~~~~~~~~~~~~
"""

# pylint: disable=unused-import,import-error
from ._solver import CaptchaSolver
from ._solver_async import AsyncCaptchaSolver
from ._service import CaptchaSolvingService

__all__ = ('CaptchaSolver', 'AsyncCaptchaSolver', 'CaptchaSolvingService')
