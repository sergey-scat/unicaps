# -*- coding: UTF-8 -*-
"""
CaptchaSolver class
"""
import io
import pathlib
from typing import Union

from .captcha import (
    ImageCaptcha, TextCaptcha, RecaptchaV2, RecaptchaV3, HCaptcha, FunCaptcha, KeyCaptcha, GeeTest,
    GeeTestV4, CapyPuzzle, TikTokCaptcha
)
from ._captcha.base import BaseCaptcha  # type: ignore
from ._service import CaptchaSolvingService, SOLVING_SERVICE
from ._service.base import SolvedCaptcha, CaptchaTask


class CaptchaSolver:
    """Main captcha solver :class:`CaptchaSolver <CaptchaSolver>` object.

    :param service_name: captcha solving service to use (enum CaptchaSolvingService or str).
    :param api_key: API key to access the solving service.
    """

    def __init__(self, service_name: Union[CaptchaSolvingService, str], api_key: str):
        # check service_name
        if isinstance(service_name, CaptchaSolvingService):
            self.service_name = service_name
        elif isinstance(service_name, str):
            try:
                self.service_name = CaptchaSolvingService(service_name)
            except ValueError as exc:
                raise ValueError(
                    f"'{service_name}' is not a valid CaptchaSolvingService. "
                    "Please use one of the following values: " + ', '.join(
                        [f"'{i.value}'" for i in CaptchaSolvingService]
                    )
                ) from exc
        else:
            raise ValueError(
                '"service_name" param must be an instance of str or CaptchaSolvingService!'
            )

        self.api_key = api_key
        self._service = SOLVING_SERVICE[self.service_name].Service(api_key)  # type: ignore

    def _solve_captcha(self, captcha_class, *args, **kwargs):
        proxy = kwargs.pop('proxy') if 'proxy' in kwargs else None
        user_agent = kwargs.pop('user_agent') if 'user_agent' in kwargs else None
        cookies = kwargs.pop('cookies') if 'cookies' in kwargs else None

        return self._service.solve_captcha(
            captcha_class(*args, **kwargs),
            proxy=proxy,
            user_agent=user_agent,
            cookies=cookies
        )

    def solve_image_captcha(self,
                            image: Union[bytes, io.RawIOBase, io.BufferedIOBase, pathlib.Path],
                            **kwargs) -> SolvedCaptcha:
        r"""Solves image CAPTCHA.

        :param image: binary file, bytes or pathlib.Path object containing image with CAPTCHA
        :param char_type: (optional) Character type.
        :param is_phrase: (optional) Boolean. True if CAPTCHA contains more than one word.
        :param is_case_sensitive: (optional) Boolean.
        :param is_math: (optional) Boolean. True if CAPTCHA requires calculation.
        :param min_len: (optional) Integer. Minimum length of the CAPTCHA's text.
        :param max_len: (optional) Integer. Maximum length of the CAPTCHA's text.
        :param alphabet: (optional) Alphabet used in the CAPTCHA.
        :param language: (optional) Language.
        :param comment: (optional) String. Text instructions for worker.
        :return: :class:`SolvedCaptcha <SolvedCaptcha>` object
        :rtype: unicaps.SolvedCaptcha
        """

        return self._solve_captcha(ImageCaptcha, image, **kwargs)

    def solve_text_captcha(self, text: str, **kwargs) -> SolvedCaptcha:
        r"""Solves text CAPTCHA.

        :param text: String with text captcha task.
        :param alphabet: (optional) Alphabet used in the CAPTCHA.
        :param language: (optional) Language.
        :return: :class:`SolvedCaptcha <SolvedCaptcha>` object
        :rtype: unicaps.SolvedCaptcha
        """
        return self._solve_captcha(TextCaptcha, text, **kwargs)

    def solve_recaptcha_v2(self, site_key: str, page_url: str, **kwargs) -> SolvedCaptcha:
        r"""Solves reCAPTCHA v2.

        :param site_key: Value of "data-sitekey" (or "k") parameter.
        :param page_url: Full URL of the page with CAPTCHA.
        :param is_invisible: (optional) Invisible reCAPTCHA flag.
        :param is_enterprise: (optional) reCAPTCHA Enterprise flag.
        :param data_s: (optional) Value of "data-s" parameter.
        :param api_domain: (optional) Domain used to load the captcha: google.com or recaptcha.net.
        :param proxy: (optional) Proxy to use while solving the CAPTCHA.
        :param user_agent: (optional) User-Agent to use while solving the CAPTCHA.
        :param cookies: (optional) Cookies to use while solving the CAPTCHA.
        :return: :class:`SolvedCaptcha <SolvedCaptcha>` object
        :rtype: unicaps.SolvedCaptcha
        """
        return self._solve_captcha(RecaptchaV2, site_key, page_url, **kwargs)

    def solve_recaptcha_v3(self, site_key: str, page_url: str, **kwargs) -> SolvedCaptcha:
        r"""Solves reCAPTCHA v3.

        :param site_key: Value of "render" parameter.
        :param page_url: Full URL of the page with CAPTCHA.
        :param is_enterprise: (optional) reCAPTCHA Enterprise flag (default: False).
        :param action: (optional) Widget action value.
        :param min_score: (optional) Filters a worker with corresponding score.
        :param api_domain: (optional) Domain used to load the captcha: google.com or recaptcha.net.
        :param proxy: (optional) Proxy to use while solving the CAPTCHA.
        :param user_agent: (optional) User-Agent to use while solving the CAPTCHA.
        :param cookies: (optional) Cookies to use while solving the CAPTCHA.
        :return: :class:`SolvedCaptcha <SolvedCaptcha>` object
        :rtype: unicaps.SolvedCaptcha
        """
        return self._solve_captcha(RecaptchaV3, site_key, page_url, **kwargs)

    def solve_hcaptcha(self, site_key: str, page_url: str, **kwargs) -> SolvedCaptcha:
        r"""Solves hCaptcha.

        :param site_key: hCaptcha website key.
        :param page_url: Full URL of the page with CAPTCHA.
        :param is_invisible: (optional) Invisible hCaptcha flag (default: False).
        :param api_domain: (optional) API domain: hcaptcha.com or js.hcaptcha.com.
        :param proxy: (optional) Proxy to use while solving the CAPTCHA.
        :param user_agent: (optional) User-Agent to use while solving the CAPTCHA.
        :param cookies: (optional) Cookies to use while solving the CAPTCHA.
        :return: :class:`SolvedCaptcha <SolvedCaptcha>` object
        :rtype: unicaps.SolvedCaptcha
        """
        return self._solve_captcha(HCaptcha, site_key, page_url, **kwargs)

    def solve_funcaptcha(self, public_key: str, page_url: str, **kwargs) -> SolvedCaptcha:
        r"""Solves FunCaptcha.

        :param public_key: FunCaptcha public key.
        :param page_url: Full URL of the page with CAPTCHA.
        :param service_url: (optional) Service URL.
        :param no_js: (optional) Disable JavaScript.
        :param blob: (optional) The "blob" value of CAPTCHA.
        :param proxy: (optional) Proxy to use while solving the CAPTCHA.
        :param user_agent: (optional) User-Agent to use while solving the CAPTCHA.
        :param cookies: (optional) Cookies to use while solving the CAPTCHA.
        :return: :class:`SolvedCaptcha <SolvedCaptcha>` object
        :rtype: unicaps.SolvedCaptcha
        """
        return self._solve_captcha(FunCaptcha, public_key, page_url, **kwargs)

    def solve_keycaptcha(self, page_url: str, user_id: str, session_id: str, ws_sign: str,
                         ws_sign2: str, **kwargs) -> SolvedCaptcha:
        r"""Solves KeyCaptcha.

        :param page_url: Full URL of the page with CAPTCHA.
        :param user_id: Value of "s_s_c_user_id" parameter.
        :param session_id: Value of "s_s_c_session_id" parameter.
        :param ws_sign: Value of "s_s_c_web_server_sign" parameter.
        :param ws_sign2: Value of "s_s_c_web_server_sign2" parameter.
        :return: :class:`SolvedCaptcha <SolvedCaptcha>` object
        :rtype: unicaps.SolvedCaptcha
        """
        return self._solve_captcha(
            KeyCaptcha, page_url, user_id, session_id, ws_sign, ws_sign2, **kwargs
        )

    def solve_geetest(self, page_url: str, gt_key: str, challenge: str,
                      **kwargs) -> SolvedCaptcha:
        r"""Solves GeeTest.

        :param page_url: Full URL of the page with CAPTCHA.
        :param gt_key: Public website key (static).
        :param challenge: Dynamic challenge key.
        :param api_server: (optional) API domain
        :return: :class:`SolvedCaptcha <SolvedCaptcha>` object
        :rtype: unicaps.SolvedCaptcha
        """
        return self._solve_captcha(GeeTest, page_url, gt_key, challenge, **kwargs)

    def solve_geetest_v4(self, page_url: str, captcha_id: str, **kwargs) -> SolvedCaptcha:
        r"""Solves GeeTestV4.

        :param page_url: Full URL of the page with CAPTCHA.
        :param captcha_id: Value of captcha_id parameter you found on target website.
        :return: :class:`SolvedCaptcha <SolvedCaptcha>` object
        :rtype: unicaps.SolvedCaptcha
        """
        return self._solve_captcha(GeeTestV4, page_url, captcha_id, **kwargs)

    def solve_capy_puzzle(self, site_key: str, page_url: str, **kwargs) -> SolvedCaptcha:
        r"""Solves Capy Puzzle CAPTCHA.

        :param site_key: Public website key (static).
        :param page_url: Full URL of the page with CAPTCHA.
        :param api_server: (optional) The domain part of script URL you found on page.
        :param proxy: (optional) Proxy to use while solving the CAPTCHA.
        :param user_agent: (optional) User-Agent to use while solving the CAPTCHA.
        :param cookies: (optional) Cookies to use while solving the CAPTCHA.
        :return: :class:`SolvedCaptcha <SolvedCaptcha>` object
        :rtype: unicaps.SolvedCaptcha
        """
        return self._solve_captcha(CapyPuzzle, site_key, page_url, **kwargs)

    def solve_tiktok(self, page_url: str, **kwargs) -> SolvedCaptcha:
        r"""Solves TikTokCaptcha.

        :param page_url: Full URL of the page with CAPTCHA.
        :param aid: (optional) The aid parameter value for the page.
        :param host: (optional) The host parameter value for the page.
        :param proxy: (optional) Proxy to use while solving the CAPTCHA.
        :param user_agent: (optional) User-Agent to use while solving the CAPTCHA.
        :param cookies: (optional) Cookies to use while solving the CAPTCHA.
        :return: :class:`SolvedCaptcha <SolvedCaptcha>` object
        :rtype: unicaps.SolvedCaptcha
        """
        return self._solve_captcha(TikTokCaptcha, page_url, **kwargs)

    def create_task(self, captcha: BaseCaptcha) -> CaptchaTask:
        """Create task to solve CAPTCHA

        :param captcha: Captcha to solve.
        :return: :class:`CaptchaTask <CaptchaTask>` object
        :rtype: unicaps.CaptchaTask
        """
        return self._service.create_task(captcha)

    def get_balance(self) -> float:
        """Get account balance

        :return: :float:Balance amount
        :rtype: float
        """
        return self._service.get_balance()

    def get_status(self) -> bool:
        """Get service status

        :return: :bool:Service status
        :rtype: bool
        """
        return self._service.get_status()

    def close(self) -> None:
        """Close all connections"""
        self._service.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
