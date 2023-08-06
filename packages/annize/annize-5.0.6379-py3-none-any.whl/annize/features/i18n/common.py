# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import typing as t

import annize.data
import annize.i18n


class ProjectDefinedTranslationProvider(annize.i18n.TranslationProvider):

    def __init__(self):
        self.__translations = {}

    def __translations_for_stringname(self, stringname: str) -> t.Dict[str, str]:
        result = self.__translations[stringname] = self.__translations.get(stringname) or {}
        return result

    def translate(self, stringname, *, culture):
        return self.__translations_for_stringname(stringname).get(culture.iso_639_1_lang_code)

    def add_translations(self, stringname: str, variants: t.Dict[str, str]) -> None:
        self.__translations_for_stringname(stringname).update(variants)


_translationprovider = ProjectDefinedTranslationProvider()

annize.i18n.add_translation_provider(_translationprovider, priority=-100_000) # TODO who unloads it?!


class String(annize.i18n.ProvidedTrStr):

    def __init__(self, *, stringname: t.Optional[str] = None, stringtr: t.Optional[str] = None, **variants: str):
        if stringtr:
            stringtr = stringtr.strip()
            if not stringtr.endswith(")"):
                raise Exception("TODO")
            istart = stringtr.find("(")
            if istart == -1:
                raise Exception("TODO")
            inrstr = stringtr[istart+1:-1].strip()
            if len(inrstr) < 3:
                raise Exception("TODO")
            if inrstr[0] != inrstr[-1]:
                raise Exception("TODO")
            stringname = inrstr[1:-1]
        if not stringname:
            stringname = annize.data.UniqueId().long_str
        super().__init__(stringname)
        if variants:
            _translationprovider.add_translations(stringname, variants)

# TODO
