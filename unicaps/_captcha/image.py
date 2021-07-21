# -*- coding: UTF-8 -*-
"""
Image CAPTCHA
"""

import base64
import imghdr
import io
import pathlib
from dataclasses import dataclass
from typing import Union, Optional

from .base import BaseCaptcha, BaseCaptchaSolution
from ..common import CaptchaAlphabet, CaptchaCharType, WorkerLanguage
from ..exceptions import BadInputDataError


@dataclass
class ImageCaptcha(BaseCaptcha):
    """ Image CAPTCHA """

    image: Union[bytes, io.RawIOBase, io.BufferedIOBase, pathlib.Path]
    char_type: Optional[CaptchaCharType] = None
    is_phrase: Optional[bool] = None
    is_case_sensitive: Optional[bool] = None
    is_math: Optional[bool] = None
    min_len: Optional[int] = None
    max_len: Optional[int] = None
    alphabet: Optional[CaptchaAlphabet] = None
    language: Optional[WorkerLanguage] = None
    comment: Optional[str] = None

    def __post_init__(self):
        assert isinstance(self.image, (bytes, io.RawIOBase, io.BufferedIOBase, pathlib.Path))
        assert self.char_type is None or isinstance(self.char_type, CaptchaCharType)
        assert self.is_phrase is None or isinstance(self.is_phrase, bool)
        assert self.is_case_sensitive is None or isinstance(self.is_case_sensitive, bool)
        assert self.is_math is None or isinstance(self.is_math, bool)
        assert self.min_len is None or (isinstance(self.min_len, int) and self.min_len > 0)
        assert self.max_len is None or (isinstance(self.max_len, int) and self.max_len > 0)
        assert self.alphabet is None or isinstance(self.alphabet, CaptchaAlphabet)
        assert self.language is None or isinstance(self.language, WorkerLanguage)
        self._image_bytes = None
        self.get_image_bytes()

    def get_image_bytes(self) -> bytes:
        """ Bytes image """

        if self._image_bytes is None:
            if isinstance(self.image, bytes):
                self._image_bytes = self.image  # type: ignore
            elif isinstance(self.image, (io.RawIOBase, io.BufferedIOBase)):
                self._image_bytes = self.image.read()
            elif isinstance(self.image, pathlib.Path):
                self._image_bytes = self.image.read_bytes()

            # check image type
            self.get_image_type()

        return self._image_bytes

    def get_image_base64(self) -> bytes:
        """ BASE64 image """

        return base64.b64encode(self.get_image_bytes())

    def get_image_type(self) -> str:
        """ Get type of image file/data """

        image_type = imghdr.what(None, h=self._image_bytes)

        if not image_type:
            raise BadInputDataError("Unable to recognize image type!")
        return image_type


@dataclass
class ImageCaptchaSolution(BaseCaptchaSolution):
    """ Image CAPTCHA solution """

    text: str
