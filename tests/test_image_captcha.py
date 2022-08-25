# -*- coding: UTF-8 -*-

import base64
import os.path
import pathlib

import pytest
from unicaps.captcha import ImageCaptcha
from unicaps.exceptions import BadInputDataError

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
IMAGE_FILE = os.path.join(DATA_DIR, 'image.jpg')


@pytest.fixture
def image_path():
    return pathlib.Path(IMAGE_FILE)


@pytest.fixture
def image_bytes():
    return open(IMAGE_FILE, 'rb').read()


@pytest.fixture
def image_base64(image_bytes):
    return base64.b64encode(image_bytes)


def test_image_from_path(image_path, image_bytes):
    """ Pathlib input test"""
    captcha = ImageCaptcha(image=image_path)
    assert image_bytes == captcha.get_image_bytes()


def test_image_from_binary(image_bytes):
    """ Binary input test"""
    captcha = ImageCaptcha(image=image_bytes)
    assert image_bytes == captcha.get_image_bytes()


def test_not_an_image():
    """ Not an image input test """
    with pytest.raises(TypeError):
        ImageCaptcha(image='wrong_image')


def test_bad_image():
    """ Bad image input test """
    with pytest.raises(BadInputDataError):
        ImageCaptcha(image=b'bad_image_data')
