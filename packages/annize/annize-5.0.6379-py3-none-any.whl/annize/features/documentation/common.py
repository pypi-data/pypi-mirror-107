# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import abc
import typing as t

import annize.callconv
import annize.fs.temp


class _DocumentGenerateResult:

    def __init__(self, file: annize.fs.FsEntry, entry_path: str):
        self.__file = file
        self.__entry_path = entry_path

    @property
    def file(self) -> annize.fs.FsEntry:
        return self.__file

    @property
    def entry_path(self) -> str:
        return self.__entry_path

    def _set_entry_path(self, entry_path: str) -> None:
        self.__entry_path = entry_path


class _DocumentGenerateAllLanguagesResult(_DocumentGenerateResult):

    def __init__(self, file: annize.fs.FsEntry, entry_path: str, entry_paths_for_languages: t.Dict[str, str]):
        super().__init__(file, entry_path)
        self.__entrypathsforlanguages = entry_paths_for_languages

    def entry_path_for_language(self, language: str) -> str:
        return self.__entrypathsforlanguages[language]

    @property
    def languages(self) -> t.List[str]:
        return list(self.__entrypathsforlanguages.keys())


class Document(abc.ABC):

    @abc.abstractmethod
    def available_languages(self) -> t.List[str]:
        pass

    @abc.abstractmethod
    def generate(self, outputspec, *, language: str = "?") -> _DocumentGenerateResult:  # TODO put "language" to "outputspec" ?!
        pass

    @abc.abstractmethod
    def generate_all_languages(self, outputspec) -> _DocumentGenerateAllLanguagesResult:
        pass


class OutputSpec(abc.ABC):
    """
    Base class for documentation output specifications. See :py:func:`render`.
    """


class HtmlOutputSpec(OutputSpec):
    """
    HTML documentation output.
    """

    def __init__(self, *, is_homepage: bool = False, title: t.Optional[str] = None):
        """
        :param is_homepage: If to render output for a homepage with slight different stylings and behavior.
        :param title: The html title. TODO higher level thing here?!
        """
        super().__init__()
        self.__is_homepage = is_homepage
        self.__title = title

    @property
    def is_homepage(self):
        return self.__is_homepage

    @property
    def title(self):
        return self.__title


class PdfOutputSpec(OutputSpec):
    """
    PDF documentation output.
    """


class PlaintextOutputSpec(OutputSpec):
    """
    Plaintext documentation output.
    """


class GeneratedDocument(annize.fs.AdHocFsEntry):

    @annize.callconv.parameter_from_childnodes("document")
    @annize.callconv.parameter_from_childnodes("outputspec")
    def __init__(self, *, document: Document, outputspec: OutputSpec, language: str = None, filename: str = None):
        super().__init__()
        self.__document = document
        self.__outputspec = outputspec
        self.__language = language
        self.__filename = filename

    def _initialize(self):
        if self.__language:
            result = self.__document.generate(self.__outputspec, language=self.__language).file
        else:
            result = self.__document.generate_all_languages(self.__outputspec).file
        if self.__filename:
            oresult = result.owned()
            result = annize.fs.temp.fresh_temp_dir().child_by_relative_path(self.__filename)
            oresult.move_to(result.owned().path())
        return result
