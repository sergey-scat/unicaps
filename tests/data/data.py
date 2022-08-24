# -*- coding: UTF-8 -*-
"""
Test data
"""

import base64
import os.path
import pathlib
from random import choice
from unittest import mock

from unicaps import CaptchaSolvingService, exceptions as exc
from unicaps.captcha import (
    CaptchaType, ImageCaptcha, RecaptchaV2, RecaptchaV3, FunCaptcha, TextCaptcha,
    KeyCaptcha, GeeTest, HCaptcha, CapyPuzzle, TikTokCaptcha
)
from unicaps.common import CaptchaAlphabet, CaptchaCharType, WorkerLanguage
from unicaps.proxy import ProxyServer
# from unicaps.__version__ import __version__ as VERSION

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

API_KEY = 'test'

IMAGE_FILE_PATH = os.path.join(CURRENT_DIR, 'image.jpg')
IMAGE_FILE_PATHLIB = pathlib.Path(IMAGE_FILE_PATH)
IMAGE_FILE_FILEOBJECT = open(IMAGE_FILE_PATH, 'rb')
IMAGE_FILE_BYTES = open(IMAGE_FILE_PATH, 'rb').read()
IMAGE_FILE_BASE64 = base64.b64encode(IMAGE_FILE_BYTES)
IMAGE_FILE_BASE64_STR = IMAGE_FILE_BASE64.decode('ascii')

PROXY_ADDRESS = 'http://login:password@proxy.com:8080'
PROXY_OBJ = ProxyServer(PROXY_ADDRESS)

COOKIES = {'cookie1': 'value1', 'cookie2': 'value2'}

INPUT_TEST_DATA_FOR_TASK_PREPARE_FUNC = {
    1: (ImageCaptcha(IMAGE_FILE_BYTES), None, None, None),
    2: (ImageCaptcha(IMAGE_FILE_PATHLIB), None, None, None),
    3: (ImageCaptcha(IMAGE_FILE_FILEOBJECT, is_phrase=True), None, None, None),
    4: (ImageCaptcha(IMAGE_FILE_BYTES, is_case_sensitive=True), None, None, None),
    5: (ImageCaptcha(IMAGE_FILE_BYTES, char_type=CaptchaCharType.ALPHA), None, None, None),
    6: (ImageCaptcha(IMAGE_FILE_BYTES, is_math=True), None, None, None),
    7: (ImageCaptcha(IMAGE_FILE_BYTES, min_len=1), None, None, None),
    8: (ImageCaptcha(IMAGE_FILE_BYTES, max_len=10), None, None, None),
    9: (ImageCaptcha(IMAGE_FILE_BYTES, alphabet=CaptchaAlphabet.LATIN), None, None, None),
    10: (ImageCaptcha(IMAGE_FILE_BYTES, language=WorkerLanguage.ENGLISH), None, None, None),
    11: (ImageCaptcha(IMAGE_FILE_BYTES, comment='test'), None, None, None),
    12: (RecaptchaV2('test1', 'test2'), None, None, None),
    13: (RecaptchaV2('test1', 'test2', is_invisible=True), None, None, None),
    14: (RecaptchaV2('test1', 'test2', data_s='test3'), None, None, None),
    15: (RecaptchaV3('test1', 'test2'), None, None, None),
    16: (RecaptchaV3('test1', 'test2', action='test3'), None, None, None),
    17: (RecaptchaV3('test1', 'test2', min_score=0.9), None, None, None),
    18: (FunCaptcha('test1', 'test2'), None, None, None),
    19: (FunCaptcha('test1', 'test2', service_url='test3'), None, None, None),
    20: (FunCaptcha('test1', 'test2', no_js=True), None, None, None),
    21: (TextCaptcha('test1'), None, None, None),
    22: (TextCaptcha('test1', alphabet=CaptchaAlphabet.LATIN), None, None, None),
    23: (TextCaptcha('test1', language=WorkerLanguage.ENGLISH), None, None, None),
    24: (KeyCaptcha('test1', 'test2', 'test3', 'test4', 'test5'), None, None, None),
    25: (GeeTest('test1', 'test2', 'test3'), None, None, None),
    26: (GeeTest('test1', 'test2', 'test3', api_server='test4'), None, None, None),
    27: (HCaptcha('test1', 'test2'), None, None, None),
    28: (CapyPuzzle('test1', 'test2', 'test3'), None, None, None),
    29: (TikTokCaptcha('test1',), None, None, COOKIES),
    30: (RecaptchaV2('test1', 'test2'), PROXY_OBJ, None, None),
    31: (RecaptchaV2('test1', 'test2'), PROXY_OBJ, 'User-Agent1', None),
    32: (RecaptchaV2('test1', 'test2'), PROXY_OBJ, 'User-Agent1', COOKIES),
    33: (RecaptchaV2('test1', 'test2', data_s="test3", is_enterprise=True), None, None, None),
    34: (RecaptchaV3('test1', 'test2', is_enterprise=True), None, None, None),
}

BASE_TASK_REQUEST_DATA = {
    CaptchaSolvingService.TWOCAPTCHA: dict(
        method='POST',
        url='https://2captcha.com/in.php',
        headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
        data=dict(key=API_KEY, json=1, soft_id=2738)
    ),
    CaptchaSolvingService.RUCAPTCHA: dict(
        method='POST',
        url='https://rucaptcha.com/in.php',
        headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
        data=dict(key=API_KEY, json=1, soft_id=2738)
    ),
    CaptchaSolvingService.ANTI_CAPTCHA: dict(
        method='POST',
        json=dict(clientKey=API_KEY, softId=940),
        headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
        url='https://api.anti-captcha.com/createTask'
    ),
    CaptchaSolvingService.AZCAPTCHA: dict(
        method='POST',
        url='http://azcaptcha.com/in.php',
        data=dict(key=API_KEY, json=1)
    ),
    CaptchaSolvingService.CPTCH_NET: dict(
        method='POST',
        url='https://cptch.net/in.php',
        data=dict(key=API_KEY, json=1, soft_id="164")
    ),
    # CaptchaSolvingService.DEATHBYCAPTCHA: dict(
    # authtoken=API_KEY,
    # version=f"Unicaps/Python v{VERSION}",
    # cmd="upload"
    # ),
}

OUTPUT_TEST_DATA_FOR_TASK_PREPARE_FUNC = {
    CaptchaSolvingService.TWOCAPTCHA: {
        1: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR)},
        2: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR)},
        3: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR, phrase=1)},
        4: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR, regsense=1)},
        5: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR, numeric=2)},
        6: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR, calc=1)},
        7: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR, min_len=1)},
        8: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR, max_len=10)},
        9: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR, language=2)},
        10: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR, lang='en')},
        11: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR, textinstructions='test')},
        12: {'data': dict(method='userrecaptcha', googlekey='test1', pageurl='test2', invisible=0)},
        13: {'data': dict(method='userrecaptcha', googlekey='test1', pageurl='test2', invisible=1)},
        14: {'data': {'method': 'userrecaptcha', 'googlekey': 'test1', 'pageurl': 'test2',
                      'invisible': 0, 'data-s': 'test3'}},
        15: {'data': dict(method='userrecaptcha', version='v3', googlekey='test1',
                          pageurl='test2')},
        16: {'data': dict(method='userrecaptcha', version='v3', googlekey='test1', pageurl='test2',
                          action='test3')},
        17: {'data': dict(method='userrecaptcha', version='v3', googlekey='test1', pageurl='test2',
                          min_score=0.9)},
        18: {'data': dict(method='funcaptcha', publickey='test1', pageurl='test2')},
        19: {'data': dict(method='funcaptcha', publickey='test1', pageurl='test2', surl='test3')},
        20: {'data': dict(method='funcaptcha', publickey='test1', pageurl='test2', nojs=1)},
        21: {'data': dict(textcaptcha='test1')},
        22: {'data': dict(textcaptcha='test1', language=2)},
        23: {'data': dict(textcaptcha='test1', lang='en')},
        24: {'data': dict(method='keycaptcha', pageurl='test1', s_s_c_user_id='test2',
                          s_s_c_session_id='test3', s_s_c_web_server_sign='test4',
                          s_s_c_web_server_sign2='test5')},
        25: {'data': dict(method='geetest', pageurl='test1', gt='test2', challenge='test3')},
        26: {'data': dict(method='geetest', pageurl='test1', gt='test2', challenge='test3',
                          api_server='test4')},
        27: {'data': dict(method='hcaptcha', sitekey='test1', pageurl='test2')},
        28: {'data': dict(method='capy', captchakey='test1', pageurl='test2', api_server='test3')},
        29: {'data': dict(method='tiktok', pageurl='test1',
                          cookies='cookie1:value1;cookie2:value2')},
        30: {'data': dict(method='userrecaptcha', googlekey='test1', pageurl='test2', invisible=0,
                          proxy=PROXY_ADDRESS.split('://')[1],
                          proxytype=PROXY_ADDRESS.split('://')[0].upper())},
        31: {'data': dict(method='userrecaptcha', googlekey='test1', pageurl='test2', invisible=0,
                          proxy=PROXY_ADDRESS.split('://')[1],
                          proxytype=PROXY_ADDRESS.split('://')[0].upper(),
                          userAgent='User-Agent1')},
        32: {'data': dict(method='userrecaptcha', googlekey='test1', pageurl='test2', invisible=0,
                          proxy=PROXY_ADDRESS.split('://')[1],
                          proxytype=PROXY_ADDRESS.split('://')[0].upper(),
                          userAgent='User-Agent1',
                          cookies='cookie1:value1;cookie2:value2')},
        33: {'data': {'method': 'userrecaptcha', 'googlekey': 'test1', 'pageurl': 'test2',
                      'invisible': 0, 'data-s': 'test3', 'enterprise': 1}},
        34: {'data': dict(method='userrecaptcha', version='v3', googlekey='test1', pageurl='test2',
                          enterprise=1)},
    },
    CaptchaSolvingService.ANTI_CAPTCHA: {
        1: {'json': dict(task=dict(type='ImageToTextTask', body=IMAGE_FILE_BASE64_STR))},
        2: {'json': dict(task=dict(type='ImageToTextTask', body=IMAGE_FILE_BASE64_STR))},
        3: {'json': dict(task=dict(type='ImageToTextTask', body=IMAGE_FILE_BASE64_STR,
                                   phrase=True))},
        4: {'json': dict(task=dict(type='ImageToTextTask', body=IMAGE_FILE_BASE64_STR, case=True))},
        5: {'json': dict(task=dict(type='ImageToTextTask', body=IMAGE_FILE_BASE64_STR, numeric=2))},
        6: {'json': dict(task=dict(type='ImageToTextTask', body=IMAGE_FILE_BASE64_STR, math=True))},
        7: {'json': dict(task=dict(type='ImageToTextTask', body=IMAGE_FILE_BASE64_STR,
                                   minLength=1))},
        8: {'json': dict(task=dict(type='ImageToTextTask', body=IMAGE_FILE_BASE64_STR,
                                   maxLength=10))},
        9: {'json': dict(task=dict(type='ImageToTextTask', body=IMAGE_FILE_BASE64_STR))},
        10: {'json': dict(task=dict(type='ImageToTextTask', body=IMAGE_FILE_BASE64_STR),
                          languagePool='en')},
        11: {'json': dict(task=dict(type='ImageToTextTask', body=IMAGE_FILE_BASE64_STR,
                                    comment='test'))},
        12: {'json': dict(task=dict(type='NoCaptchaTaskProxyless', websiteKey='test1',
                                    websiteURL='test2', isInvisible=False))},
        13: {'json': dict(task=dict(type='NoCaptchaTaskProxyless', websiteKey='test1',
                                    websiteURL='test2', isInvisible=True))},
        14: {'json': dict(task=dict(type='NoCaptchaTaskProxyless', websiteKey='test1',
                                    websiteURL='test2', isInvisible=False,
                                    recaptchaDataSValue='test3'))},
        15: {'json': dict(task=dict(type='RecaptchaV3TaskProxyless', websiteKey='test1',
                                    websiteURL='test2'))},
        16: {'json': dict(task=dict(type='RecaptchaV3TaskProxyless', websiteKey='test1',
                                    websiteURL='test2', pageAction='test3'))},
        17: {'json': dict(task=dict(type='RecaptchaV3TaskProxyless', websiteKey='test1',
                                    websiteURL='test2', minScore=0.9))},
        18: {'json': dict(task=dict(type='FunCaptchaTaskProxyless', websitePublicKey='test1',
                                    websiteURL='test2'))},
        19: {'json': dict(task=dict(type='FunCaptchaTaskProxyless', websitePublicKey='test1',
                                    websiteURL='test2', funcaptchaApiJSSubdomain='test3'))},
        20: {'json': dict(task=dict(type='FunCaptchaTaskProxyless', websitePublicKey='test1',
                                    websiteURL='test2'))},
        21: None,
        22: None,
        23: None,
        24: None,
        25: {'json': dict(task=dict(type='GeeTestTaskProxyless', websiteURL='test1',
                                    gt='test2', challenge='test3'))},
        26: {'json': dict(task=dict(type='GeeTestTaskProxyless', websiteURL='test1',
                                    gt='test2', challenge='test3',
                                    geetestApiServerSubdomain='test4'))},
        27: {'json': dict(task=dict(type='HCaptchaTaskProxyless', websiteKey='test1',
                                    websiteURL='test2'))},
        28: None,
        29: None,
        30: {'json': dict(task=dict(type='NoCaptchaTask', websiteKey='test1',
                                    websiteURL='test2', isInvisible=False,
                                    proxyType=PROXY_OBJ.proxy_type.value,
                                    proxyAddress=PROXY_OBJ.get_ip_address(),
                                    proxyPort=PROXY_OBJ.port,
                                    proxyLogin=PROXY_OBJ.login,
                                    proxyPassword=PROXY_OBJ.password))},
        31: {'json': dict(task=dict(type='NoCaptchaTask', websiteKey='test1',
                                    websiteURL='test2', isInvisible=False,
                                    proxyType=PROXY_OBJ.proxy_type.value,
                                    proxyAddress=PROXY_OBJ.get_ip_address(),
                                    proxyPort=PROXY_OBJ.port,
                                    proxyLogin=PROXY_OBJ.login,
                                    proxyPassword=PROXY_OBJ.password,
                                    userAgent='User-Agent1'))},
        32: {'json': dict(task=dict(type='NoCaptchaTask', websiteKey='test1',
                                    websiteURL='test2', isInvisible=False,
                                    proxyType=PROXY_OBJ.proxy_type.value,
                                    proxyAddress=PROXY_OBJ.get_ip_address(),
                                    proxyPort=PROXY_OBJ.port,
                                    proxyLogin=PROXY_OBJ.login,
                                    proxyPassword=PROXY_OBJ.password,
                                    userAgent='User-Agent1',
                                    cookies='cookie1=value1; cookie2=value2'))},
        33: {'json': dict(task=dict(type='RecaptchaV2EnterpriseTaskProxyless', websiteKey='test1',
                                    websiteURL='test2', isInvisible=False,
                                    enterprisePayload=dict(s='test3')))},
        34: {'json': dict(task=dict(type='RecaptchaV3TaskProxyless', websiteKey='test1',
                                    websiteURL='test2', isEnterprise=True))},
    },
    CaptchaSolvingService.AZCAPTCHA: {
        1: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR)},
        2: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR)},
        3: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR, phrase=1)},
        4: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR, regsense=1)},
        5: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR, numeric=2)},
        6: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR, calc=1)},
        7: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR, min_len=1)},
        8: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR, max_len=10)},
        9: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR, language=2)},
        10: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR, lang='en')},
        11: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR, textinstructions='test')},
        12: {'data': dict(method='userrecaptcha', googlekey='test1', pageurl='test2', invisible=0)},
        13: {'data': dict(method='userrecaptcha', googlekey='test1', pageurl='test2', invisible=1)},
        14: {'data': {'method': 'userrecaptcha', 'googlekey': 'test1', 'pageurl': 'test2',
                      'invisible': 0, 'data-s': 'test3'}},
        15: {'data': dict(method='userrecaptcha', version='v3', googlekey='test1',
                          pageurl='test2')},
        16: {'data': dict(method='userrecaptcha', version='v3', googlekey='test1', pageurl='test2',
                          action='test3')},
        17: {'data': dict(method='userrecaptcha', version='v3', googlekey='test1', pageurl='test2',
                          min_score=0.9)},
        18: None,
        19: None,
        20: None,
        21: None,
        22: None,
        23: None,
        24: None,
        25: None,
        26: None,
        27: None,
        28: None,
        29: None,
        30: {'data': dict(method='userrecaptcha', googlekey='test1', pageurl='test2', invisible=0,
                          proxy=PROXY_ADDRESS.split('://')[1],
                          proxytype=PROXY_ADDRESS.split('://')[0].upper())},
        31: {'data': dict(method='userrecaptcha', googlekey='test1', pageurl='test2', invisible=0,
                          proxy=PROXY_ADDRESS.split('://')[1],
                          proxytype=PROXY_ADDRESS.split('://')[0].upper(),
                          userAgent='User-Agent1')},
        32: {'data': dict(method='userrecaptcha', googlekey='test1', pageurl='test2', invisible=0,
                          proxy=PROXY_ADDRESS.split('://')[1],
                          proxytype=PROXY_ADDRESS.split('://')[0].upper(),
                          userAgent='User-Agent1',
                          cookies='cookie1:value1;cookie2:value2')},
        33: {'data': {'method': 'userrecaptcha', 'googlekey': 'test1', 'pageurl': 'test2',
                      'invisible': 0, 'data-s': 'test3'}},
        34: {'data': dict(method='userrecaptcha', version='v3', googlekey='test1',
                          pageurl='test2')},
    },
    CaptchaSolvingService.CPTCH_NET: {
        1: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR)},
        2: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR)},
        3: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR, phrase=1)},
        4: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR, regsense=1)},
        5: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR, numeric=2)},
        6: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR, calc=1)},
        7: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR, min_len=1)},
        8: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR, max_len=10)},
        9: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR, language=2)},
        10: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR, lang='en')},
        11: {'data': dict(method='base64', body=IMAGE_FILE_BASE64_STR, textinstructions='test')},
        12: {'data': dict(method='userrecaptcha', googlekey='test1', pageurl='test2', invisible=0)},
        13: {'data': dict(method='userrecaptcha', googlekey='test1', pageurl='test2', invisible=1)},
        14: {'data': {'method': 'userrecaptcha', 'googlekey': 'test1', 'pageurl': 'test2',
                      'invisible': 0}},
        15: {'data': dict(method='userrecaptcha', version='v3', googlekey='test1',
                          pageurl='test2')},
        16: {'data': dict(method='userrecaptcha', version='v3', googlekey='test1', pageurl='test2',
                          action='test3')},
        17: {'data': dict(method='userrecaptcha', version='v3', googlekey='test1', pageurl='test2',
                          min_score=0.9)},
        18: None,
        19: None,
        20: None,
        21: None,
        22: None,
        23: None,
        24: None,
        25: None,
        26: None,
        27: None,
        28: None,
        29: None,
        30: {'data': dict(method='userrecaptcha', googlekey='test1', pageurl='test2', invisible=0)},
        31: {'data': dict(method='userrecaptcha', googlekey='test1', pageurl='test2', invisible=0)},
        32: {'data': dict(method='userrecaptcha', googlekey='test1', pageurl='test2', invisible=0)},
        33: {'data': dict(method='userrecaptcha', googlekey='test1', pageurl='test2', invisible=0)},
        34: {'data': dict(method='userrecaptcha', version='v3', googlekey='test1',
                          pageurl='test2')},
    },
    # CaptchaSolvingService.DEATHBYCAPTCHA: {
    # 1: None,
    # 2: None,
    # 3: None,
    # 4: None,
    # 5: None,
    # 6: None,
    # 7: None,
    # 8: None,
    # 9: None,
    # 10: None,
    # 11: None,
    # 12: {'type': 4, 'token_params': json.dumps(dict(googlekey='test1', pageurl='test2'))},
    # 13: {'type': 4, 'token_params': json.dumps(dict(googlekey='test1', pageurl='test2'))},
    # 14: {'type': 4, 'token_params': json.dumps(dict(googlekey='test1', pageurl='test2'))},
    # 15: None,
    # 16: None,
    # 17: None,
    # 18: None,
    # 19: None,
    # 20: None,
    # 21: None,
    # 22: None,
    # 23: None,
    # 24: None,
    # 25: None,
    # 26: None,
    # 27: None,
    # 28: None,
    # 29: None,
    # 30: {'type': 4, 'token_params': json.dumps(dict(googlekey='test1', pageurl='test2'))},
    # 31: {'type': 4, 'token_params': json.dumps(dict(googlekey='test1', pageurl='test2'))},
    # 32: {'type': 4, 'token_params': json.dumps(dict(googlekey='test1', pageurl='test2'))},
    # },
}
OUTPUT_TEST_DATA_FOR_TASK_PREPARE_FUNC[CaptchaSolvingService.RUCAPTCHA] = (
    OUTPUT_TEST_DATA_FOR_TASK_PREPARE_FUNC[CaptchaSolvingService.TWOCAPTCHA]
)


def get_http_resp_obj(ret_value):
    obj = mock.Mock()
    obj.json = lambda: ret_value.copy()
    return obj


INPUT_TEST_LIST_FOR_TASK_PARSE_RESPONSE_FUNC = {
    1: CaptchaType.IMAGE,
    2: CaptchaType.RECAPTCHAV2,
    3: CaptchaType.RECAPTCHAV3,
    4: CaptchaType.TEXT,
    5: CaptchaType.FUNCAPTCHA,
    6: CaptchaType.KEYCAPTCHA,
    7: CaptchaType.GEETEST,
    8: CaptchaType.HCAPTCHA,
    9: CaptchaType.CAPY,
    10: CaptchaType.TIKTOK,
}

INPUT_TEST_DATA_FOR_TASK_PARSE_RESPONSE_FUNC = {
    CaptchaSolvingService.TWOCAPTCHA: {
        1: get_http_resp_obj(dict(status=1, request='1234567890')),
        2: get_http_resp_obj(dict(status=1, request='1234567890')),
        3: get_http_resp_obj(dict(status=1, request='1234567890')),
        4: get_http_resp_obj(dict(status=1, request='1234567890')),
        5: get_http_resp_obj(dict(status=1, request='1234567890')),
        6: get_http_resp_obj(dict(status=1, request='1234567890')),
        7: get_http_resp_obj(dict(status=1, request='1234567890')),
        8: get_http_resp_obj(dict(status=1, request='1234567890')),
        9: get_http_resp_obj(dict(status=1, request='1234567890')),
        10: get_http_resp_obj(dict(status=1, request='1234567890')),
    },
    CaptchaSolvingService.ANTI_CAPTCHA: {
        1: get_http_resp_obj(dict(errorId=0, taskId='1234567890')),
        2: get_http_resp_obj(dict(errorId=0, taskId='1234567890')),
        3: get_http_resp_obj(dict(errorId=0, taskId='1234567890')),
        4: None,
        5: get_http_resp_obj(dict(errorId=0, taskId='1234567890')),
        6: None,
        7: get_http_resp_obj(dict(errorId=0, taskId='1234567890')),
        8: get_http_resp_obj(dict(errorId=0, taskId='1234567890')),
        9: None,
        10: None,
    },
    CaptchaSolvingService.AZCAPTCHA: {
        1: get_http_resp_obj(dict(status=1, request='1234567890')),
        2: get_http_resp_obj(dict(status=1, request='1234567890')),
        3: get_http_resp_obj(dict(status=1, request='1234567890')),
        4: None,
        5: None,
        6: None,
        7: None,
        8: None,
        9: None,
        10: None,
    },
    CaptchaSolvingService.CPTCH_NET: {
        1: get_http_resp_obj(dict(status=1, request='1234567890')),
        2: get_http_resp_obj(dict(status=1, request='1234567890')),
        3: get_http_resp_obj(dict(status=1, request='1234567890')),
        4: None,
        5: None,
        6: None,
        7: None,
        8: None,
        9: None,
        10: None,
    },
    # CaptchaSolvingService.DEATHBYCAPTCHA: {
    # 1: None,
    # 2: json.dumps(dict(captcha='1234567890')),
    # 3: None,
    # 4: None,
    # 5: None,
    # 6: None,
    # 7: None,
    # 8: None,
    # 9: None,
    # 10: None,
    # },
}
INPUT_TEST_DATA_FOR_TASK_PARSE_RESPONSE_FUNC[CaptchaSolvingService.RUCAPTCHA] = (
    INPUT_TEST_DATA_FOR_TASK_PARSE_RESPONSE_FUNC[CaptchaSolvingService.TWOCAPTCHA]
)

OUTPUT_TEST_DATA_FOR_TASK_PARSE_RESPONSE_FUNC = {
    CaptchaSolvingService.TWOCAPTCHA: {
        1: dict(task_id='1234567890', extra={}),
        2: dict(task_id='1234567890', extra={}),
        3: dict(task_id='1234567890', extra={}),
        4: dict(task_id='1234567890', extra={}),
        5: dict(task_id='1234567890', extra={}),
        6: dict(task_id='1234567890', extra={}),
        7: dict(task_id='1234567890', extra={}),
        8: dict(task_id='1234567890', extra={}),
        9: dict(task_id='1234567890', extra={}),
        10: dict(task_id='1234567890', extra={}),
    },
    CaptchaSolvingService.ANTI_CAPTCHA: {
        1: dict(task_id='1234567890', extra={}),
        2: dict(task_id='1234567890', extra={}),
        3: dict(task_id='1234567890', extra={}),
        4: None,
        5: dict(task_id='1234567890', extra={}),
        6: None,
        7: dict(task_id='1234567890', extra={}),
        8: dict(task_id='1234567890', extra={}),
        9: None,
        10: None,
    },
    CaptchaSolvingService.AZCAPTCHA: {
        1: dict(task_id='1234567890', extra={}),
        2: dict(task_id='1234567890', extra={}),
        3: dict(task_id='1234567890', extra={}),
        4: None,
        5: None,
        6: None,
        7: None,
        8: None,
        9: None,
        10: None,
    },
    CaptchaSolvingService.CPTCH_NET: {
        1: dict(task_id='1234567890', extra={}),
        2: dict(task_id='1234567890', extra={}),
        3: dict(task_id='1234567890', extra={}),
        4: None,
        5: None,
        6: None,
        7: None,
        8: None,
        9: None,
        10: None,
    },
    # CaptchaSolvingService.DEATHBYCAPTCHA: {
    # 1: None,
    # 2: dict(task_id='1234567890', extra={}),
    # 3: None,
    # 4: None,
    # 5: None,
    # 6: None,
    # 7: None,
    # 8: None,
    # 9: None,
    # 10: None,
    # },
}
OUTPUT_TEST_DATA_FOR_TASK_PARSE_RESPONSE_FUNC[CaptchaSolvingService.RUCAPTCHA] = (
    OUTPUT_TEST_DATA_FOR_TASK_PARSE_RESPONSE_FUNC[CaptchaSolvingService.TWOCAPTCHA]
)


OUTPUT_TEST_DATA_FOR_TASK_PARSE_RESPONSE_FUNC_WITH_EXC = {
    1: exc.ServiceError,
    2: exc.AccessDeniedError,
    3: exc.LowBalanceError,
    4: exc.ServiceTooBusy,
    5: exc.TooManyRequestsError,
    6: exc.MalformedRequestError,
    7: exc.BadInputDataError,
    8: exc.UnableToSolveError,
    9: exc.ProxyError
}

INPUT_TEST_DATA_FOR_TASK_PARSE_RESPONSE_FUNC_WITH_EXC = {
    CaptchaSolvingService.TWOCAPTCHA: {
        1: get_http_resp_obj(dict(status=0, request=choice(
            ['REPORT_NOT_RECORDED', 'ERROR_IP_ADDRES']))),
        2: get_http_resp_obj(dict(status=0, request=choice(
            ['ERROR_WRONG_USER_KEY', 'ERROR_KEY_DOES_NOT_EXIST', 'ERROR_IP_NOT_ALLOWED',
             'IP_BANNED']))),
        3: get_http_resp_obj(dict(status=0, request='ERROR_ZERO_BALANCE')),
        4: get_http_resp_obj(dict(status=0, request='ERROR_NO_SLOT_AVAILABLE')),
        5: get_http_resp_obj(dict(status=0, request=choice(
            ['MAX_USER_TURN', 'ERROR: 1001', 'ERROR: 1005']))),
        6: get_http_resp_obj(dict(status=0, request=choice(
            ['ERROR_WRONG_ID_FORMAT', 'ERROR_WRONG_CAPTCHA_ID']))),
        7: get_http_resp_obj(dict(status=0, request=choice(
            'ERROR_UPLOAD ERROR_ZERO_CAPTCHA_FILESIZE ERROR_TOO_BIG_CAPTCHA_FILESIZE '
            'ERROR_WRONG_FILE_EXTENSION ERROR_IMAGE_TYPE_NOT_SUPPORTED ERROR_PAGEURL '
            'ERROR_BAD_TOKEN_OR_PAGEURL ERROR_GOOGLEKEY ERROR_BAD_PARAMETERS '
            'ERROR_TOKEN_EXPIRED ERROR_EMPTY_ACTION'.split()))),
        8: get_http_resp_obj(dict(status=0, request=choice(
            'ERROR_CAPTCHAIMAGE_BLOCKED ERROR_CAPTCHA_UNSOLVABLE ERROR_BAD_DUPLICATES'.split()))),
        9: get_http_resp_obj(dict(status=0, request=choice(
            ['ERROR_BAD_PROXY', 'ERROR_PROXY_CONNECTION_FAILED']))),
    },
    CaptchaSolvingService.ANTI_CAPTCHA: {
        1: get_http_resp_obj(dict(errorId=2, errorCode='UNKNOWN_ERROR')),
        2: get_http_resp_obj(dict(errorId=3, errorCode=choice(
            ['ERROR_KEY_DOES_NOT_EXIST', 'ERROR_IP_NOT_ALLOWED', 'ERROR_IP_BLOCKED']))),
        3: get_http_resp_obj(dict(errorId=4, errorCode='ERROR_ZERO_BALANCE')),
        4: get_http_resp_obj(dict(errorId=4, errorCode='ERROR_NO_SLOT_AVAILABLE')),
        5: None,
        6: get_http_resp_obj(dict(errorId=4, errorCode=choice(
            'ERROR_NO_SUCH_METHOD ERROR_NO_SUCH_CAPCHA_ID ERROR_TASK_ABSENT '
            'ERROR_TASK_NOT_SUPPORTED ERROR_FUNCAPTCHA_NOT_ALLOWED'.split()))),
        7: get_http_resp_obj(dict(errorId=4, errorCode=choice(
            'ERROR_ZERO_CAPTCHA_FILESIZE ERROR_TOO_BIG_CAPTCHA_FILESIZE '
            'ERROR_IMAGE_TYPE_NOT_SUPPORTED ERROR_EMPTY_COMMENT ERROR_INCORRECT_SESSION_DATA '
            'ERROR_RECAPTCHA_INVALID_SITEKEY ERROR_RECAPTCHA_INVALID_DOMAIN '
            'ERROR_RECAPTCHA_OLD_BROWSER ERROR_TOKEN_EXPIRED ERROR_INVISIBLE_RECAPTCHA'.split()))),
        8: get_http_resp_obj(dict(errorId=4, errorCode=choice(
            'ERROR_CAPTCHA_UNSOLVABLE ERROR_BAD_DUPLICATES ERROR_RECAPTCHA_TIMEOUT '
            'ERROR_FAILED_LOADING_WIDGET'.split()))),
        9: get_http_resp_obj(dict(errorId=4, errorCode=choice(
            'ERROR_PROXY_CONNECT_REFUSED ERROR_PROXY_CONNECT_TIMEOUT ERROR_PROXY_READ_TIMEOUT '
            'ERROR_PROXY_BANNED ERROR_PROXY_TRANSPARENT ERROR_PROXY_HAS_NO_IMAGE_SUPPORT '
            'ERROR_PROXY_INCOMPATIBLE_HTTP_VERSION ERROR_PROXY_NOT_AUTHORISED'.split()))),
    },
    CaptchaSolvingService.CPTCH_NET: {
        1: get_http_resp_obj(dict(status=0, request='UNKNOWN_ERROR')),
        2: get_http_resp_obj(dict(status=0, request=choice(
            ['ERROR_WRONG_USER_KEY', 'ERROR_KEY_DOES_NOT_EXIST']))),
        3: get_http_resp_obj(dict(status=0, request='ERROR_ZERO_BALANCE')),
        4: None,
        5: None,
        6: get_http_resp_obj(dict(status=0, request='ERROR_WRONG_CAPTCHA_ID')),
        7: get_http_resp_obj(dict(status=0, request=choice(
            'ERROR_UPLOAD ERROR_ZERO_CAPTCHA_FILESIZE ERROR_TOO_BIG_CAPTCHA_FILESIZE '
            'ERROR_PAGEURL ERROR_GOOGLEKEY ERROR'.split()))),
        8: get_http_resp_obj(dict(status=0, request='ERROR_CAPTCHA_UNSOLVABLE')),
        9: None,
    },
    # CaptchaSolvingService.DEATHBYCAPTCHA: {
    # 1: None,
    # 2: json.dumps(dict(error=choice(
    # ['not-logged-in', 'invalid-credentials', 'banned']))),
    # 3: json.dumps(dict(error='insufficient-funds')),
    # 4: json.dumps(dict(error='service-overload')),
    # 5: None,
    # 6: None,
    # 7: json.dumps(dict(error='invalid-captcha')),
    # 8: None,
    # 9: None,
    # },
}
INPUT_TEST_DATA_FOR_TASK_PARSE_RESPONSE_FUNC_WITH_EXC[CaptchaSolvingService.RUCAPTCHA] = (
    INPUT_TEST_DATA_FOR_TASK_PARSE_RESPONSE_FUNC_WITH_EXC[CaptchaSolvingService.TWOCAPTCHA]
)
INPUT_TEST_DATA_FOR_TASK_PARSE_RESPONSE_FUNC_WITH_EXC[CaptchaSolvingService.AZCAPTCHA] = (
    INPUT_TEST_DATA_FOR_TASK_PARSE_RESPONSE_FUNC_WITH_EXC[CaptchaSolvingService.TWOCAPTCHA]
)
