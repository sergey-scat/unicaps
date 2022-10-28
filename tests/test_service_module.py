# -*- coding: UTF-8 -*-
"""
Service module tests
"""

import importlib
import inspect
from copy import deepcopy
from unittest import mock

import pytest

from unicaps._captcha import CaptchaType
from unicaps._service import SOLVING_SERVICE

from data.data import (BASE_TASK_REQUEST_DATA, INPUT_TEST_DATA_FOR_TASK_PREPARE_FUNC,
                       OUTPUT_TEST_DATA_FOR_TASK_PREPARE_FUNC,
                       INPUT_TEST_LIST_FOR_TASK_PARSE_RESPONSE_FUNC,
                       INPUT_TEST_DATA_FOR_TASK_PARSE_RESPONSE_FUNC,
                       OUTPUT_TEST_DATA_FOR_TASK_PARSE_RESPONSE_FUNC,
                       INPUT_TEST_DATA_FOR_TASK_PARSE_RESPONSE_FUNC_WITH_EXC,
                       OUTPUT_TEST_DATA_FOR_TASK_PARSE_RESPONSE_FUNC_WITH_EXC)
from _helpers import dict_update

# dict of captcha services with lists of supported captchas
SERVICE_MODULES_FOR_TEST = {
    'anti_captcha': (CaptchaType.IMAGE, CaptchaType.RECAPTCHAV2, CaptchaType.RECAPTCHAV3,
                     CaptchaType.FUNCAPTCHA, CaptchaType.GEETEST, CaptchaType.GEETESTV4,
                     CaptchaType.HCAPTCHA),
    'twocaptcha': (CaptchaType.IMAGE, CaptchaType.TEXT, CaptchaType.RECAPTCHAV2,
                   CaptchaType.RECAPTCHAV3, CaptchaType.FUNCAPTCHA, CaptchaType.KEYCAPTCHA,
                   CaptchaType.GEETEST, CaptchaType.GEETESTV4, CaptchaType.HCAPTCHA,
                   CaptchaType.CAPY, CaptchaType.TIKTOK),
    'rucaptcha': (CaptchaType.IMAGE, CaptchaType.TEXT, CaptchaType.RECAPTCHAV2,
                  CaptchaType.RECAPTCHAV3, CaptchaType.FUNCAPTCHA, CaptchaType.KEYCAPTCHA,
                  CaptchaType.GEETEST, CaptchaType.GEETESTV4, CaptchaType.HCAPTCHA,
                  CaptchaType.CAPY, CaptchaType.TIKTOK),
    'azcaptcha': (CaptchaType.IMAGE, CaptchaType.RECAPTCHAV2, CaptchaType.RECAPTCHAV3,
                  CaptchaType.HCAPTCHA, CaptchaType.FUNCAPTCHA),
    'cptch_net': (CaptchaType.IMAGE, CaptchaType.RECAPTCHAV2, CaptchaType.RECAPTCHAV3),
    'deathbycaptcha': (CaptchaType.IMAGE, CaptchaType.RECAPTCHAV2, CaptchaType.RECAPTCHAV3,
                       CaptchaType.HCAPTCHA, CaptchaType.FUNCAPTCHA)
}
BASE_REQUESTS = ('GetBalance', 'GetStatus', 'ReportGood', 'ReportBad')
TASK_REQUEST_PREPARE_PARAMS = ('self', 'captcha', 'proxy', 'user_agent', 'cookies')
SOLUTION_REQUEST_PREPARE_PARAMS = ('self', 'task')
REQUEST_PARSE_RESPONSE_PARAMS = ('self', 'response')


@pytest.fixture(scope="module", params=SERVICE_MODULES_FOR_TEST)
def service_module(request):
    return importlib.import_module('unicaps._service.' + request.param)


@pytest.fixture(scope="module")
def service_instance(service_module):
    return getattr(service_module, "Service")("test")


@pytest.fixture(scope="module")
def json_response_obj():
    def get_obj(ret_value):
        obj = mock.Mock()
        obj.json = lambda: ret_value
        return obj
    return get_obj


def check_if_class_is_present(module, class_name, is_not=False):
    if is_not:
        assert not hasattr(module, class_name), \
               f'{class_name} is found in service module {module.__name__}'
    else:
        assert hasattr(module, class_name), \
               f'{class_name} is not found in service module {module.__name__}'


def is_captcha_supported(service_module, captcha_type):
    module_name = service_module.__name__.split('.')[-1]
    if captcha_type in SERVICE_MODULES_FOR_TEST[module_name]:
        return True
    return False


def get_request(service_module, captcha_type, req_type='Request'):
    request_name = captcha_type.value + req_type
    return request_name, getattr(service_module, request_name)


def test_if_service_class_is_present(service_module):
    """ Checks if Service() class is declared in the module """

    check_if_class_is_present(service_module, 'Service')


@pytest.mark.parametrize("req", BASE_REQUESTS)
def test_if_base_request_is_present(service_module, req):
    """ Checks if all of the base requests are present in the module file """

    check_if_class_is_present(service_module, req + 'Request')


@pytest.mark.parametrize("captcha_type", CaptchaType)
def test_if_task_request_is_present(service_module, captcha_type):
    """ Checks if all of the task requests are present in the module file """

    check_if_class_is_present(
        service_module,
        captcha_type.value + 'TaskRequest',
        not is_captcha_supported(service_module, captcha_type)
    )


@pytest.mark.parametrize("captcha_type", CaptchaType)
def test_if_solution_request_is_present(service_module, captcha_type):
    """ Checks if all of the solution requests are present in the module file """

    check_if_class_is_present(
        service_module,
        captcha_type.value + 'SolutionRequest',
        not is_captcha_supported(service_module, captcha_type)
    )


@pytest.mark.parametrize("req", BASE_REQUESTS)
def test_base_request_signature_of_prepare_func(service_module, req):
    """ Checks signature of the <captcha>TaskRequest.prepare() function """

    request_name = req + 'Request'
    request_class = getattr(service_module, request_name)

    if req in ('ReportGood', 'ReportBad'):
        standard = ('self', 'solved_captcha')
    else:
        standard = ('self',)

    params = tuple(inspect.signature(request_class.prepare).parameters)
    assert params == standard, \
           f"Incorrect signature of {request_name}.prepare() func: {', '.join(params)}"


@pytest.mark.parametrize("captcha_type", CaptchaType)
def test_task_request_signature_of_prepare_func(service_module, captcha_type):
    """ Checks signature of the <captcha>TaskRequest.prepare() function """

    if is_captcha_supported(service_module, captcha_type):
        request_name, request_class = get_request(service_module, captcha_type, 'TaskRequest')

        params = tuple(inspect.signature(request_class.prepare).parameters)
        assert params == TASK_REQUEST_PREPARE_PARAMS, \
               f"Incorrect signature of {request_name}.prepare() func: {', '.join(params)}"


@pytest.mark.parametrize("captcha_type", CaptchaType)
def test_solution_request_signature_of_prepare_func(service_module, captcha_type):
    """ Checks signature of the <captcha>TaskRequest.prepare() function """

    if is_captcha_supported(service_module, captcha_type):
        request_name, request_class = get_request(service_module, captcha_type, 'SolutionRequest')

        params = tuple(inspect.signature(request_class.prepare).parameters)
        assert params == SOLUTION_REQUEST_PREPARE_PARAMS, \
               f"Incorrect signature of {request_name}.prepare() func: {', '.join(params)}"


@pytest.mark.parametrize("req", BASE_REQUESTS)
def test_base_request_signature_of_parse_response_func(service_module, req):
    """ Checks signature of the <captcha>TaskRequest.prepare() function """

    request_name = req + 'Request'
    request_class = getattr(service_module, request_name)

    params = tuple(inspect.signature(request_class.parse_response).parameters)
    assert params == REQUEST_PARSE_RESPONSE_PARAMS, \
           f"Incorrect signature of {request_name}.prepare() func: {', '.join(params)}"


@pytest.mark.parametrize("captcha_type, req_type",
                         [(t, r) for t in CaptchaType for r in ('TaskRequest', 'SolutionRequest')])
def test_captcha_request_signature_of_parse_response_func(service_module, captcha_type, req_type):
    """
    Checks signature of the <captcha>TaskRequest.parse_response() and
    <captcha>SolutionRequest.parse_response() functions.
    """

    if not is_captcha_supported(service_module, captcha_type):
        pytest.skip("CAPTCHA is not supported!")

    request_name, request_class = get_request(service_module, captcha_type, req_type)
    params = tuple(inspect.signature(request_class.parse_response).parameters)
    assert params == REQUEST_PARSE_RESPONSE_PARAMS, \
           f"Incorrect signature of {request_name}.parse_response() func: {', '.join(params)}"


@pytest.mark.parametrize("test_id,input_data", INPUT_TEST_DATA_FOR_TASK_PREPARE_FUNC.items())
def test_task_request_return_value_of_prepare_func(service_module, test_id, input_data):
    service_type = {v: k for k, v in SOLVING_SERVICE.items()}[service_module]
    captcha_type = input_data[0].get_type()

    if not is_captcha_supported(service_module, captcha_type):
        pytest.skip("CAPTCHA is not supported!")

    request_name, request_class = get_request(service_module, captcha_type, 'TaskRequest')

    # service instance
    service = service_module.Service('test')

    # request instance
    request_instance = request_class(service)
    result_dict = request_instance.prepare(*input_data)

    standard_result = deepcopy(BASE_TASK_REQUEST_DATA[service_type])
    dict_update(standard_result, OUTPUT_TEST_DATA_FOR_TASK_PREPARE_FUNC[service_type][test_id])

    assert result_dict == standard_result


@pytest.mark.parametrize("test_id,captcha_type",
                         INPUT_TEST_LIST_FOR_TASK_PARSE_RESPONSE_FUNC.items())
def test_task_request_return_value_of_parse_response_func(service_module, test_id, captcha_type):
    service_type = {v: k for k, v in SOLVING_SERVICE.items()}[service_module]

    if not is_captcha_supported(service_module, captcha_type):
        pytest.skip("CAPTCHA is not supported!")

    request_name, request_class = get_request(service_module, captcha_type, 'TaskRequest')

    # service instance
    service = service_module.Service('test')

    input_data = INPUT_TEST_DATA_FOR_TASK_PARSE_RESPONSE_FUNC[service_type][test_id]

    # request instance
    request_instance = request_class(service)
    result_dict = request_instance.parse_response(input_data)

    standard_result = deepcopy(OUTPUT_TEST_DATA_FOR_TASK_PARSE_RESPONSE_FUNC[service_type][test_id])
    assert result_dict == standard_result


@pytest.mark.parametrize("test_id,captcha_type,exc_type",
                         [(i, c, e) for i, e in
                          OUTPUT_TEST_DATA_FOR_TASK_PARSE_RESPONSE_FUNC_WITH_EXC.items()
                          for c in CaptchaType])
def test_task_request_exception_of_parse_response_func(service_module, test_id, captcha_type,
                                                       exc_type):
    service_type = {v: k for k, v in SOLVING_SERVICE.items()}[service_module]

    if not is_captcha_supported(service_module, captcha_type):
        pytest.skip("CAPTCHA is not supported!")

    request_name, request_class = get_request(service_module, captcha_type, 'TaskRequest')

    # service instance
    service = service_module.Service('test')

    # get input data, skip test
    input_data = INPUT_TEST_DATA_FOR_TASK_PARSE_RESPONSE_FUNC_WITH_EXC[service_type][test_id]
    if not input_data:
        pytest.skip("The service doesn't support the testing exception!")

    # request instance
    request_instance = request_class(service)

    expected_exception = (
        OUTPUT_TEST_DATA_FOR_TASK_PARSE_RESPONSE_FUNC_WITH_EXC[test_id]
    )
    with pytest.raises(expected_exception):
        request_instance.parse_response(input_data)
