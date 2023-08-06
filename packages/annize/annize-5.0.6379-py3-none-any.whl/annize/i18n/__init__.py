# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import os
import threading
import typing as t

import annize.aux

#TODO language subcodes


CultureSpec = t.Optional[t.Union["Culture", str]]


class TranslationProvider:

    def translate(self, stringname: str, *, culture: "Culture") -> str:
        raise NotImplementedError()


class GettextTranslationProvider(TranslationProvider):

    def __init__(self, mopath):
        self.__mopath = mopath
        self.__gettexttrs = {}

    def translate(self, stringname: str, *, culture: "Culture"):
        culture = get_culture(culture)
        import gettext # TODO
        gettexttr = self.__gettexttrs.get(culture.iso_639_1_lang_code, None)
        if not gettexttr:
            #TODO
            gettexttr = gettext.translation("annize", self.__mopath, languages=[culture.iso_639_1_lang_code])#TODO
            self.__gettexttrs[culture.iso_639_1_lang_code] = gettexttr
        return gettexttr.gettext(stringname)


_providers = []


def add_translation_provider(provider: TranslationProvider, *, priority: int = 0) -> None:
    _providers.append((priority, provider))
    _providers.sort(key=lambda prtup: prtup[0])


def translation_providers() -> t.List[TranslationProvider]:
    return [prtup[1] for prtup in _providers]


add_translation_provider(GettextTranslationProvider(annize.aux.mo_path), priority=100_000) #TODO


def tr(stringname: str, *, culture: CultureSpec = None) -> str:
    culture = get_culture(culture)
    for provider in translation_providers():
        result = provider.translate(stringname, culture=culture)
        if result is not None:
            return result
    raise TranslationUnavailableError(stringname, culture.english_lang_name)


class TrStr:

    @staticmethod
    def tr(stringname: str) -> "TrStr":
        return ProvidedTrStr(stringname)

    def translate(self, culture: CultureSpec = None) -> str:
        raise NotImplementedError()

    def format(self_, *args, **kwargs) -> "TrStr":
        if "self" in kwargs:
            kwargs.pop("self")  # TODO weg?!
        class MyTrStr(TrStr):
            def translate(self, culture=None):
                return self_.translate(culture).format(*args, **kwargs)
        return MyTrStr()

    def __str__(self):
        return self.translate()


class TODO(TrStr):

    def __init__(self, txt):
        self.__txt = txt

    def translate(self, culture: CultureSpec = None) -> str:
        return self.__txt


class IndependentTrStr(TrStr):  # TODO needed ?!

    def __init__(self, **variants: str):
        super().__init__()
        self.__variants = variants

    def translate(self, culture=None) -> str:
        #TODO
        culture = get_culture(culture)
        result = self.__variants.get(culture.iso_639_1_lang_code, None)
        if result is None:
            raise TranslationUnavailableError(repr(self), culture.english_lang_name)
        return result


class ProvidedTrStr(TrStr):

    def __init__(self, stringname: str):
        super().__init__()
        self.__stringname = stringname

    def translate(self, culture=None) -> str:
        return tr(self.__stringname, culture=culture)


#: Type annotation for something that can be either a :samp:`str` or a :py:class:`TrStr`.
TrStrOrStr = t.Union[str, TrStr]


def tr_if_trstr(txt: TrStrOrStr, culture: CultureSpec = None) -> str:  # TODO
    if (not txt) or isinstance(txt, str):
        return txt
    return txt.translate(culture=get_culture(culture))


class Culture:

    @staticmethod
    def get_from_iso_639_1_lang_code(iso_639_1_lang_code):
        import pycountry  # TODO
        language = pycountry.languages.get(alpha_2=iso_639_1_lang_code.upper())
        return Culture(language.name, iso_639_1_lang_code)

    def __init__(self, english_lang_name: str, iso_639_1_lang_code: str):
        self.__english_lang_name = english_lang_name
        self.__iso_639_1_lang_code = iso_639_1_lang_code.lower()

    @property
    def english_lang_name(self) -> str:
        return self.__english_lang_name

    @property
    def iso_639_1_lang_code(self) -> str:
        return self.__iso_639_1_lang_code

    def __enter__(self):
        _culturestack.stack = stack = getattr(_culturestack, "stack", [])
        stack.append(self)
        # TODO more and nicer
        os.environ["LANGUAGE"] = self.iso_639_1_lang_code
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        _culturestack.stack.pop()


def get_culture(culture: CultureSpec) -> t.Optional[Culture]:#TODO
    if culture is None:
        return current_culture()
    if isinstance(culture, str):
        culture = Culture.get_from_iso_639_1_lang_code(culture)
    return culture


# TODO xx xy noh global variables?!
_culturestack = threading.local()


def current_culture() -> Culture:  #  TODO store in Context instead ?!
    stack = getattr(_culturestack, "stack", None)
    if not stack:
        raise NoCurrentCultureError()
    return stack[-1]


def annize_user_interaction_culture() -> Culture:
    return get_culture(os.environ.get("LANGUAGE")[:2] or "en")#TODO


class NoCurrentCultureError(TypeError):

    def __init__(self):
        super().__init__("There is no current Annize i18n culture")


class TranslationUnavailableError(TypeError):

    def __init__(self, stringname: str, language: str):
        super().__init__(f"There is no translation for '{stringname}' in language '{language}'")


# TODO test
