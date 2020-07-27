# -*- coding: UTF-8 -*-
"""
CAPTCHA common stuff
"""

import enum


class CaptchaAlphabet(enum.Enum):
    """ Alphabet used in the CAPTCHA """

    LATIN = 'latin'
    CYRILLIC = 'cyrillic'


class CaptchaCharType(enum.Enum):
    """ Character types used in CAPTCHA """

    NUMERIC = 1
    ALPHA = 2
    ALPHA_OR_NUMERIC = 3
    ALPHANUMERIC = 4


class WorkerLanguage(enum.Enum):
    """ Worker's language to solve the CAPTCHA """

    ENGLISH = 'en'
    RUSSIAN = 'ru'
    SPANISH = 'es'
    PORTUGUESE = 'pt'
    UKRAINIAN = 'uk'
    VIETNAMESE = 'vi'
    FRENCH = 'fr'
    INDONESIAN = 'id'
    ARAB = 'ar'
    JAPANESE = 'ja'
    TURKISH = 'tr'
    GERMAN = 'de'
    CHINESE = 'zh'
    # PHILIPPINE = 'fil'
    POLISH = 'pl'
    THAI = 'th'
    ITALIAN = 'it'
    DUTCH = 'nl'
    SLOVAK = 'sk'
    BULGARIAN = 'bg'
    ROMANIAN = 'ro'
    HUNGARIAN = 'hu'
    KOREAN = 'ko'
    CZECH = 'cs'
    AZERBAIJANI = 'az'
    PERSIAN = 'fa'
    BENGALI = 'bn'
    GREEK = 'el'
    LITHUANIAN = 'lt'
    LATVIAN = 'lv'
    SWEDISH = 'sv'
    SERBIAN = 'sr'
    CROATIAN = 'hr'
    HEBREW = 'he'
    HINDI = 'hi'
    NORWEGIAN = 'nb'
    SLOVENIAN = 'sl'
    DANISH = 'da'
    UZBEK = 'uz'
    FINNISH = 'fi'
    CATALAN = 'ca'
    GEORGIAN = 'ka'
    MALAY = 'ms'
    TELUGU = 'te'
    ESTONIAN = 'et'
    MALAYALAM = 'ml'
    BELORUSSIAN = 'be'
    KAZAKH = 'kk'
    MARATHI = 'mr'
    NEPALI = 'ne'
    BURMESE = 'my'
    BOSNIAN = 'bs'
    ARMENIAN = 'hy'
    MACEDONIAN = 'mk'
    PUNJABI = 'pa'
