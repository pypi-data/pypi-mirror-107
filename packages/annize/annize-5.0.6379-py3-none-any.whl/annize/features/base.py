# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import datetime
import os
import typing as t

import annize.callconv
import annize.context
import annize.data
import annize.engine
import annize.fs
import annize.features.files
import annize.i18n


TrStrOrStr = annize.i18n.TrStrOrStr


class Data:

    def __init__(self, *, project_name: TrStrOrStr = None, pretty_project_name: TrStrOrStr = None,
                 summary: TrStrOrStr = None, long_description: TrStrOrStr = None, homepage_url: TrStrOrStr = None,
                 imprint: TrStrOrStr = None, project_directory: str = None):
        self.__project_name = project_name  # TODO whitelist allowed characters
        self.__pretty_project_name = pretty_project_name
        self.__summary = summary
        self.__long_description = long_description
        self.__homepage_url = homepage_url
        self.__imprint = imprint
        self.__project_directory = project_directory

    @property
    def project_name(self) -> TrStrOrStr:
        return self.__project_name

    @property
    def pretty_project_name(self) -> TrStrOrStr:
        return self.__pretty_project_name

    @property
    def summary(self) -> TrStrOrStr:
        return self.__summary

    @property
    def long_description(self) -> TrStrOrStr:
        return self.__long_description

    @property
    def homepage_url(self) -> TrStrOrStr:
        return self.__homepage_url

    @property
    def imprint(self) -> TrStrOrStr:
        return self.__imprint

    @property
    def project_directory(self) -> str:
        return self.__project_directory


class BrandColor(annize.data.Color):
    pass


class DateTime(datetime.datetime):

    def __new__(cls, *, iso: str = None):
        return datetime.datetime.fromisoformat(iso)


class Keywords:

    def __init__(self, *, from_string: str = "", split_by: str = " ", keywords: t.List[str] = ()):
        self.__from_string = from_string
        self.__split_by = split_by
        self.__keywords = keywords

    @property
    def keywords(self) -> t.List[str]:
        result = []
        for keyword in [*self.__keywords, *self.__from_string.split(self.__split_by)]:
            if keyword and (keyword not in result):
                result.append(keyword)
        return result


class Keyword(Keywords):

    def __init__(self, text: str):
        super().__init__(keywords=[text])


def project_keywords() -> Keywords:
    allkeywords = []
    for keywords in annize.context.objects_by_type(Keywords):
        for keyword in keywords.keywords:
            if keyword not in allkeywords:
                allkeywords.append(keyword)
    return Keywords(keywords=allkeywords)


class Basket(annize.data.Basket):  # TODO have it directly in annize namespace?!

    @annize.callconv.parameter_from_childnodes("objects")
    def __init__(self, *, objects: t.List[object]):
        super().__init__(objects)


class FirstOf(annize.data.Basket): # TODO have it directly in annize namespace?!

    @annize.callconv.parameter_from_childnodes("objects")
    def __init__(self, *, objects: t.List[object]):
        super().__init__(objects[:1])


def brand_color(*, none_on_undefined: bool = False) -> annize.data.Color:
    for obj in annize.context.objects_by_type(BrandColor):
        return obj
    return None if none_on_undefined else annize.data.Color(red=0.3, green=0.3, blue=0.3)


def _get_data(key: str, defaultvalue: t.Optional[t.Any]) -> t.Optional[t.Any]:
    result = defaultvalue
    for obj in annize.context.objects_by_type(Data):
        value = getattr(obj, key)
        if value:
            result = value
            break
    return annize.i18n.tr_if_trstr(result)


def project_name() -> str:
    return _get_data("project_name", "")


def pretty_project_name() -> str:
    return _get_data("pretty_project_name", project_name())


def summary() -> str:
    return _get_data("summary", "")


def long_description() -> str:
    return _get_data("long_description", "")


def homepage_url() -> str:
    return _get_data("homepage_url", "")


def imprint() -> str:
    return _get_data("imprint", "")


def project_directory() -> str:
    annize_config_rootpath = annize.context.object_by_name(_ANNIZE_CONFIG_ROOTPATH)
    projectfiles_subdir = os.path.dirname(annize_config_rootpath)
    result = _get_data("project_directory", None)
    if not result:
        result = annize.engine.guess_project_root_directory(annize_config_rootpath)
    if not os.path.isabs(result):
        result = f"{projectfiles_subdir}/{result}"
    result = os.path.abspath(result)
    return result


_ANNIZE_CONFIG_ROOTPATH = annize.data.UniqueId("annize_config_rootpath").processonly_long_str  # TODO unify such variable names
