# Copyright (C) 2019 Majormode.  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import re


# Define the conversion table of ISO 639-2 code to its equivalent ISO
# 639-3 code.  The complete list can be found on Summer Institute of
# Linguistics (SIL) International's Web site located at:
# http://www-01.sil.org/iso639-3/codes.asp
ISO_639_2_TO_ISO_639_3 = {
   'aa':'aar', 'ab':'abk', 'af':'afr', 'ak':'aka', 'am':'amh',
   'ar':'ara', 'an':'arg', 'as':'asm', 'av':'ava', 'ae':'ave',
   'ay':'aym', 'az':'aze', 'ba':'bak', 'bm':'bam', 'be':'bel',
   'bn':'ben', 'bi':'bis', 'bo':'bod', 'bs':'bos', 'br':'bre',
   'bg':'bul', 'ca':'cat', 'cs':'ces', 'ch':'cha', 'ce':'che',
   'cu':'chu', 'cv':'chv', 'kw':'cor', 'co':'cos', 'cr':'cre',
   'cy':'cym', 'da':'dan', 'de':'deu', 'dv':'div', 'dz':'dzo',
   'el':'ell', 'en':'eng', 'eo':'epo', 'et':'est', 'eu':'eus',
   'ee':'ewe', 'fo':'fao', 'fa':'fas', 'fj':'fij', 'fi':'fin',
   'fr':'fra', 'fy':'fry', 'ff':'ful', 'gd':'gla', 'ga':'gle',
   'gl':'glg', 'gv':'glv', 'gn':'grn', 'gu':'guj', 'ht':'hat',
   'ha':'hau', 'sh':'hbs', 'he':'heb', 'hz':'her', 'hi':'hin',
   'ho':'hmo', 'hr':'hrv', 'hu':'hun', 'hy':'hye', 'ig':'ibo',
   'io':'ido', 'ii':'iii', 'iu':'iku', 'ie':'ile', 'ia':'ina',
   'id':'ind', 'ik':'ipk', 'is':'isl', 'it':'ita', 'jv':'jav',
   'ja':'jpn', 'kl':'kal', 'kn':'kan', 'ks':'kas', 'ka':'kat',
   'kr':'kau', 'kk':'kaz', 'km':'khm', 'ki':'kik', 'rw':'kin',
   'ky':'kir', 'kv':'kom', 'kg':'kon', 'ko':'kor', 'kj':'kua',
   'ku':'kur', 'lo':'lao', 'la':'lat', 'lv':'lav', 'li':'lim',
   'ln':'lin', 'lt':'lit', 'lb':'ltz', 'lu':'lub', 'lg':'lug',
   'mh':'mah', 'ml':'mal', 'mr':'mar', 'mk':'mkd', 'mg':'mlg',
   'mt':'mlt', 'mn':'mon', 'mi':'mri', 'ms':'msa', 'my':'mya',
   'na':'nau', 'nv':'nav', 'nr':'nbl', 'nd':'nde', 'ng':'ndo',
   'ne':'nep', 'nl':'nld', 'nn':'nno', 'nb':'nob', 'no':'nor',
   'ny':'nya', 'oc':'oci', 'oj':'oji', 'or':'ori', 'om':'orm',
   'os':'oss', 'pa':'pan', 'pi':'pli', 'pl':'pol', 'pt':'por',
   'ps':'pus', 'qu':'que', 'rm':'roh', 'ro':'ron', 'rn':'run',
   'ru':'rus', 'sg':'sag', 'sa':'san', 'si':'sin', 'sk':'slk',
   'sl':'slv', 'se':'sme', 'sm':'smo', 'sn':'sna', 'sd':'snd',
   'so':'som', 'st':'sot', 'es':'spa', 'sq':'sqi', 'sc':'srd',
   'sr':'srp', 'ss':'ssw', 'su':'sun', 'sw':'swa', 'sv':'swe',
   'ty':'tah', 'ta':'tam', 'tt':'tat', 'te':'tel', 'tg':'tgk',
   'tl':'tgl', 'th':'tha', 'ti':'tir', 'to':'ton', 'tn':'tsn',
   'ts':'tso', 'tk':'tuk', 'tr':'tur', 'tw':'twi', 'ug':'uig',
   'uk':'ukr', 'ur':'urd', 'uz':'uzb', 've':'ven', 'vi':'vie',
   'vo':'vol', 'wa':'wln', 'wo':'wol', 'xh':'xho', 'yi':'yid',
   'yo':'yor', 'za':'zha', 'zh':'zho', 'zu':'zul'
}

REGEX_PATTERN_LANGUAGE_CODE = r'[a-z]{2,3}'
REGEX_PATTERN_COUNTRY_CODE = r'[A-Z]{2}'
REGEX_PATTERN_LOCALE = r'(([a-z]{2,3})-([A-Z]{2})$)|([a-z]{2,3}$)'
REGEX_PATTERN_JAVA_LOCALE = r'(([a-z]{2})-([A-Z]{2})$)|([a-z]{2}$)'
REGEX_PATTERN_PERMISSIVE_LOCALE = r'(([a-z]{2,3})[-_]([A-Za-z]{2})$)|([a-z]{2,3}$)'

REGEX_LOCALE = re.compile(REGEX_PATTERN_LOCALE)
REGEX_JAVA_LOCALE = re.compile(REGEX_PATTERN_JAVA_LOCALE)
REGEX_PERMISSIVE_LOCALE = re.compile(REGEX_PATTERN_PERMISSIVE_LOCALE)


class Locale:
    """
    Represent a locale that corresponds to a tag respecting RFC 4646.

    Some computational tasks require information about the current user
    context to be able to process data—particularly when formatting output
    for presentation to the user or when interpreting input.  A locale
    object provides a repository for that information.  An operation that
    requires a locale object to perform its task is called locale-
    sensitive.

    A locale is not a language; it’s a set of conventions for handling
    written language text and various units (for example, date and time
    formats, currency used, and the decimal separator).

    Conceptually, a locale identifies a specific user community—a group of
    users who have similar cultural and linguistic expectations for human-
    computer interaction (and the kinds of data they process). A locale’s
    identifier is a label for a given set of settings.  For example, “en”
    (representing “English”) is an identifier for a linguistic (and to
    some extent cultural) locale that includes (among others) Australia,
    Great Britain, and the United States.  There are also specific
    regional locales for Australian English, British English, U.S.
    English, and so on.

    When data are displayed to a user it should be formatted according to
    the conventions of the user’s native country, region, or culture.
    Conversely, when users enter data, they may do so according to their
    own customs or preferences.  Locale objects are used to provide
    information required to localize the presentation or interpretation of
    data.  This information can include decimal separators, date formats,
    and units of measurement, as well as language and region information.

    Locales are arranged in a hierarchy. At the root is the system locale,
    which provides default values for all settings. Below the root
    hierarchy are language locales.  These encapsulate settings for
    language groups, such as English, German and Chinese (using
    identifiers “en”, “de”, and “zh”).  Normal locales specify a language
    in a particular region (for example “en-GB”, “de-AT”, and “zh-SG”).

    A locale is expressed by a ISO 639-3 alpha-3 code element, optionally
    followed by a dash character `-` and a ISO 3166-1 alpha-2 code.  For
    example: "eng" (which denotes a standard English), "eng-US" (which
    denotes an American English).
    """
    class MalformedLocaleException(Exception):
        """
        Indicate that a string doesn't comply with the valid expression of a
        locale.
        """
        pass

    def __eq__(self, other):
        """
        Compare the current locale object to another passed to the comparison
        method.  The two locale objects must have the same language, and the
        same country or no country defined for both locale objects.


        :param other: a `Locale` object to compare with the current locale
            object.


        :return: `True` if the given locale corresponds to the current
            locale; `False` otherwise.
        """
        return self.language_code == other.language_code and \
            self.country_code == other.country_code

    def __hash__(self):
        """
        Return an integer corresponding to the hash of this locale object.
        Two objects which compare equal have the same hash value.


        :return: an integer corresponding to the hash of this object.
        """
        if not hasattr(self, '__hash'):
            encoded_locale = self.language_code if self.country_code is None \
                else f'{self.language_code}{self.country_code}'

            self.__hash = sum(
                [(ord(c) - ord('a') if ord(c) >= ord('a') else ord(c) - ord('A')) * 52**i
                    for i, c in enumerate(encoded_locale)])

        return self.__hash

    def __init__(self, language_code, country_code=None):
        """
        Build an object `Locale` providing a ISO 639-3 alpha-3 code (or
        alpha-2 code), and optionally a ISO 3166-1 alpha-2 code.


        :param language_code: a ISO 639-3 alpha-3 code (or alpha-2 code; which
            will be automatically converted to its equivalent ISO 639-3
            alpha-3 code).

        :param country_code: a ISO 3166-1 alpha-2 code.
        """
        self.language_code = language_code if len(language_code) == 3 \
            else ISO_639_2_TO_ISO_639_3[language_code]
        self.country_code = country_code

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.to_string()

    @staticmethod
    def from_string(locale, strict=True):
        """
        Return an object `Locale` corresponding to the string representation
        of a locale.


        :param locale: a string representation of a locale, i.e., a ISO 639-3
           alpha-3 code (or alpha-2 code), optionally followed by a dash
           character `-` and a ISO 3166-1 alpha-2 code.

        :param strict: indicate whether the string representation of a locale
            has to be strictly compliant with RFC 4646, or whether a Java-style
            locale (character `_` instead of `-`) is accepted.


        :return: a `Locale` object.
        """
        language_code, country_code = Locale.decompose_locale(locale, strict)
        return Locale(language_code, country_code)

    def is_similar(self, other):
        """
        Indicate whether the current locale object is similar to another
        passed to the comparison method.  Two locale objects are said similar
        if they have at least the same language, but not necessarily the same
        country.


        :param other: a `Locale` object to compare with the current locale
            object.


        :return: `True` if the given locale is similar to the current
            locale; `False` otherwise.
        """
        return self.language_code == other.language_code

    def to_http_string(self):
        """
        Return the string representation of the locale compatible with the
        HTTP header `Accept-Language` as specified in `RFC 7231
        <https://tools.ietf.org/html/rfc7231#section-5.3.5>_`

        The Accept-Language request HTTP header advertises which languages the
        client is able to understand, and which locale variant is preferred.


        :return: a string representation of this locale compatible with HTTP
            request, i.e., a ISO 639-3 alpha-2, optionally followed by a dash
            character `-` and a ISO 3166-1 alpha-2 code.
        """
        return self.language_code[:2] if self.country_code is None \
            else f'{self.language_code[:2]}-{self.country_code}'

    def to_string(self):
        """
        Return a string representation of this object `Locale`.


        :return: a string representation of a locale, i.e., a ISO 639-3
             alpha-3 code (or alpha-2 code), optionally followed by a dash
            character `-` and a ISO 3166-1 alpha-2 code.
        """
        return Locale.compose_locale(self.language_code, self.country_code)

    @staticmethod
    def decompose_locale(locale, strict=True):
        """
        Return the decomposition of the specified locale into a language code
        and a country code.


        :param locale: a string representation of a locale, i.e., a ISO 639-3
            alpha-3 code (or alpha-2 code), optionally followed by a dash
            character `-` and a ISO 3166-1 alpha-2 code.  If `None` passed,
            the function returns the default locale, i.e., standard English
            `('eng', None)`.

        :param strict: indicate whether the string representation of a locale
            has to be strictly compliant with RFC 4646, or whether a Java-
            style locale (character `_` instead of `-`) is accepted.


        :return: a tuple `(language_code, country_code)`, where the first
                 code represents a ISO 639-3 alpha-3 code (or alpha-2 code),
                 and the second code a ISO 3166-1 alpha-2 code.
        """
        if locale is None:
            return 'eng', None

        match = REGEX_LOCALE.match(locale)
        if match is None:
            if strict:
                raise Locale.MalformedLocaleException()

            match = REGEX_PERMISSIVE_LOCALE.match(locale)
            if match is None:
                raise Locale.MalformedLocaleException()

        _, locale_language_code, locale_country_code, language_code = match.groups()

        return (locale_language_code, locale_country_code.upper()) if language_code is None \
            else (language_code, None)

    @staticmethod
    def compose_locale(language_code, country_code=None):
        """
        Return the string representation of the locale specified with a ISO
        639-3 alpha-3 code (or alpha-2 code), optionally followed by a dash
        character `-` and a ISO 3166-1 alpha-2 code.


        :param language_code: a ISO 639-3 alpha-3 code (or alpha-2 code).

        :param country_code: a ISO 3166-1 alpha-2 code.


        :return: a string representing a locale.
        """
        return language_code if country_code is None else f'{language_code}-{country_code}'


DEFAULT_LOCALE = Locale('eng')
