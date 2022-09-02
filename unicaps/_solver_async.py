"""
AsyncCaptchaSolver class
"""
import io
import pathlib
from typing import Union

from .captcha import (
    ImageCaptcha, TextCaptcha, RecaptchaV2, RecaptchaV3, HCaptcha, FunCaptcha, KeyCaptcha, GeeTest,
    GeeTestV4, CapyPuzzle, TikTokCaptcha
)
from ._captcha.base import BaseCaptcha  # type: ignore
from ._service.base import AsyncSolvedCaptcha, AsyncCaptchaTask
from ._solver import CaptchaSolver


class AsyncCaptchaSolver(CaptchaSolver):
    """Main captcha solver :class:`AsyncCaptchaSolver <AsyncCaptchaSolver>` object.

    :param service_name: captcha solving service to use (enum CaptchaSolvingService or str).
    :param api_key: API key to access the solving service.
    """

    async def _solve_captcha_async(self, captcha_class, *args, **kwargs):
        proxy = kwargs.pop('proxy') if 'proxy' in kwargs else None
        user_agent = kwargs.pop('user_agent') if 'user_agent' in kwargs else None
        cookies = kwargs.pop('cookies') if 'cookies' in kwargs else None

        return await self._service.solve_captcha_async(
            captcha_class(*args, **kwargs),
            proxy=proxy,
            user_agent=user_agent,
            cookies=cookies
        )

    async def solve_image_captcha(self,  # type: ignore
                                  image: Union[bytes, io.RawIOBase, io.BufferedIOBase,
                                               pathlib.Path],
                                  **kwargs) -> AsyncSolvedCaptcha:  # type: ignore
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
        :return: :class:`AsyncSolvedCaptcha <AsyncSolvedCaptcha>` object
        :rtype: unicaps.AsyncSolvedCaptcha
        """

        return await self._solve_captcha_async(ImageCaptcha, image, **kwargs)

    async def solve_text_captcha(self, text: str, **kwargs) -> AsyncSolvedCaptcha:  # type: ignore
        r"""Solves text CAPTCHA.

        :param text: String with text captcha task.
        :param alphabet: (optional) Alphabet used in the CAPTCHA.
        :param language: (optional) Language.
        :return: :class:`AsyncSolvedCaptcha <AsyncSolvedCaptcha>` object
        :rtype: unicaps.AsyncSolvedCaptcha
        """
        return await self._solve_captcha_async(TextCaptcha, text, **kwargs)

    async def solve_recaptcha_v2(self, site_key: str, page_url: str,  # type: ignore
                                 **kwargs) -> AsyncSolvedCaptcha:
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
        :return: :class:`AsyncSolvedCaptcha <AsyncSolvedCaptcha>` object
        :rtype: unicaps.AsyncSolvedCaptcha
        """
        return await self._solve_captcha_async(RecaptchaV2, site_key, page_url, **kwargs)

    async def solve_recaptcha_v3(self, site_key: str, page_url: str,  # type: ignore
                                 **kwargs) -> AsyncSolvedCaptcha:
        r"""Solves reCAPTCHA v3.

        :param site_key: Value of "render" parameter.
        :param page_url: Full URL of the page with CAPTCHA.
        :param is_enterprise: (optional) reCAPTCHA Enterprise flag.
        :param action: (optional) Widget action value.
        :param min_score: (optional) Filters a worker with corresponding score.
        :param api_domain: (optional) Domain used to load the captcha: google.com or recaptcha.net.
        :param proxy: (optional) Proxy to use while solving the CAPTCHA.
        :param user_agent: (optional) User-Agent to use while solving the CAPTCHA.
        :param cookies: (optional) Cookies to use while solving the CAPTCHA.
        :return: :class:`AsyncSolvedCaptcha <AsyncSolvedCaptcha>` object
        :rtype: unicaps.AsyncSolvedCaptcha
        """
        return await self._solve_captcha_async(RecaptchaV3, site_key, page_url, **kwargs)

    async def solve_hcaptcha(self, site_key: str, page_url: str,  # type: ignore
                             **kwargs) -> AsyncSolvedCaptcha:
        r"""Solves hCaptcha.

        :param site_key: hCaptcha website key.
        :param page_url: Full URL of the page with CAPTCHA.
        :param is_invisible: (optional) Invisible hCaptcha flag (default: False).
        :param api_domain: (optional) API domain: hcaptcha.com or js.hcaptcha.com.
        :param proxy: (optional) Proxy to use while solving the CAPTCHA.
        :param user_agent: (optional) User-Agent to use while solving the CAPTCHA.
        :param cookies: (optional) Cookies to use while solving the CAPTCHA.
        :return: :class:`AsyncSolvedCaptcha <AsyncSolvedCaptcha>` object
        :rtype: unicaps.AsyncSolvedCaptcha
        """
        return await self._solve_captcha_async(HCaptcha, site_key, page_url, **kwargs)

    async def solve_funcaptcha(self, public_key: str, page_url: str,  # type: ignore
                               **kwargs) -> AsyncSolvedCaptcha:
        r"""Solves FunCaptcha.

        :param public_key: FunCaptcha public key.
        :param page_url: Full URL of the page with CAPTCHA.
        :param service_url: (optional) Service URL.
        :param no_js: (optional) Disable JavaScript.
        :param blob: (optional) The "blob" value of CAPTCHA.
        :param proxy: (optional) Proxy to use while solving the CAPTCHA.
        :param user_agent: (optional) User-Agent to use while solving the CAPTCHA.
        :param cookies: (optional) Cookies to use while solving the CAPTCHA.
        :return: :class:`AsyncSolvedCaptcha <AsyncSolvedCaptcha>` object
        :rtype: unicaps.AsyncSolvedCaptcha
        """
        return await self._solve_captcha_async(FunCaptcha, public_key, page_url, **kwargs)

    async def solve_keycaptcha(self, page_url: str, user_id: str, session_id: str,   # type: ignore
                               ws_sign: str, ws_sign2: str, **kwargs) -> AsyncSolvedCaptcha:
        r"""Solves KeyCaptcha.

        :param page_url: Full URL of the page with CAPTCHA.
        :param user_id: Value of "s_s_c_user_id" parameter.
        :param session_id: Value of "s_s_c_session_id" parameter.
        :param ws_sign: Value of "s_s_c_web_server_sign" parameter.
        :param ws_sign2: Value of "s_s_c_web_server_sign2" parameter.
        :return: :class:`AsyncSolvedCaptcha <AsyncSolvedCaptcha>` object
        :rtype: unicaps.AsyncSolvedCaptcha
        """
        return await self._solve_captcha_async(
            KeyCaptcha, page_url, user_id, session_id, ws_sign, ws_sign2, **kwargs
        )

    async def solve_geetest(self, page_url: str, gt_key: str, challenge: str,  # type: ignore
                            **kwargs) -> AsyncSolvedCaptcha:
        r"""Solves GeeTest.

        :param page_url: Full URL of the page with CAPTCHA.
        :param gt_key: Public website key (static).
        :param challenge: Dynamic challenge key.
        :param api_server: (optional) API domain
        :return: :class:`AsyncSolvedCaptcha <AsyncSolvedCaptcha>` object
        :rtype: unicaps.AsyncSolvedCaptcha
        """
        return await self._solve_captcha_async(GeeTest, page_url, gt_key, challenge, **kwargs)

    async def solve_geetest_v4(self, page_url: str, captcha_id: str,  # type: ignore
                               **kwargs) -> AsyncSolvedCaptcha:
        r"""Solves GeeTestV4.

        :param page_url: Full URL of the page with CAPTCHA.
        :param captcha_id: Value of captcha_id parameter you found on target website.
        :return: :class:`AsyncSolvedCaptcha <AsyncSolvedCaptcha>` object
        :rtype: unicaps.AsyncSolvedCaptcha
        """
        return await self._solve_captcha_async(GeeTestV4, page_url, captcha_id, **kwargs)

    async def solve_capy_puzzle(self, site_key: str, page_url: str,  # type: ignore
                                **kwargs) -> AsyncSolvedCaptcha:
        r"""Solves Capy.

        :param site_key: Public website key (static).
        :param page_url: Full URL of the page with CAPTCHA.
        :param api_server: (optional) The domain part of script URL you found on page.
        :param proxy: (optional) Proxy to use while solving the CAPTCHA.
        :param user_agent: (optional) User-Agent to use while solving the CAPTCHA.
        :param cookies: (optional) Cookies to use while solving the CAPTCHA.
        :return: :class:`AsyncSolvedCaptcha <AsyncSolvedCaptcha>` object
        :rtype: unicaps.AsyncSolvedCaptcha
        """
        return await self._solve_captcha_async(CapyPuzzle, site_key, page_url, **kwargs)

    async def solve_tiktok(self, page_url: str, **kwargs) -> AsyncSolvedCaptcha:  # type: ignore
        r"""Solves TikTokCaptcha.

        :param page_url: Full URL of the page with CAPTCHA.
        :param aid: (optional) The aid parameter value for the page.
        :param host: (optional) The host parameter value for the page.
        :param proxy: (optional) Proxy to use while solving the CAPTCHA.
        :param user_agent: (optional) User-Agent to use while solving the CAPTCHA.
        :param cookies: (optional) Cookies to use while solving the CAPTCHA.
        :return: :class:`AsyncSolvedCaptcha <AsyncSolvedCaptcha>` object
        :rtype: unicaps.AsyncSolvedCaptcha
        """
        return await self._solve_captcha_async(TikTokCaptcha, page_url, **kwargs)

    async def create_task(self, captcha: BaseCaptcha) -> AsyncCaptchaTask:  # type: ignore
        """Create task to solve CAPTCHA

        :param captcha: Captcha to solve.
        :return: :class:`AsyncCaptchaTask <AsyncCaptchaTask>` object
        :rtype: unicaps.AsyncCaptchaTask
        """
        return await self._service.create_task_async(captcha)

    async def get_balance(self) -> float:  # type: ignore
        """Get account balance

        :return: :float:Balance amount
        :rtype: float
        """
        return await self._service.get_balance_async()

    async def get_status(self) -> bool:  # type: ignore
        """Get service status

        :return: :bool:Service status
        :rtype: bool
        """
        return await self._service.get_status_async()

    async def close(self) -> None:  # type: ignore
        """Close all connections"""
        await self._service.close_async()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()
