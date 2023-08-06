# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import abc
import typing as t

import annize.features.documentation.common as documentation
import annize.fs.temp
import annize.i18n

if t.TYPE_CHECKING:
    import annize.features.documentation.sphinx.common as documentationsphinx  # pylint: disable=unused-import  ## TODO


_outputgenerators = []


def register_output_generator(outputgenerator):
    _outputgenerators.append(outputgenerator)
    return outputgenerator


def find_output_generator_for_outputspec(outputspec):
    for outputgenerator in _outputgenerators:
        if outputgenerator.is_compatible_for(outputspec):
            return outputgenerator(outputspec)
    return None


class OutputGenerator(abc.ABC):
    """
    Base class for documentation output specifications. See :py:func:`render`.
    """

    def __init__(self, outputspec):
        super().__init__()
        self.__outputspec = outputspec

    @property
    def outputspec(self) -> documentation.OutputSpec:
        return self.__outputspec

    @classmethod
    @abc.abstractmethod
    def is_compatible_for(cls, outputspec: documentation.OutputSpec) -> bool:
        pass

    @abc.abstractmethod
    def formatname(self) -> str:
        """
        Returns the Sphinx format name.
        """

    def prepare_generate(self, geninfo: "documentationsphinx.Document.GenerateInfo") -> None:
        pass

    def postproc(self, preresult: annize.fs.FsEntry) -> annize.fs.FsEntry:
        return preresult

    def multilanguage_frame(self, document: "documentationsphinx.Document"
                            ) -> documentation._DocumentGenerateAllLanguagesResult:
        resultdir = annize.fs.temp.fresh_temp_dir().owned()
        entrypathsforlanguages = {}
        for language in document.available_languages():
            variantresult = document.generate(self.outputspec, language=language)
            languagefilename = language
            if variantresult.file.is_file():
                nampcs = variantresult.file.basename().split(".")
                if len(nampcs) > 1:
                    languagefilename = f"{languagefilename}.{nampcs[-1]}"
            variantdir = resultdir.child_by_relative_path(languagefilename)
            variantresult.file.owned().move_to(variantdir.path())
            langentrypath = language
            if variantresult.entry_path:
                langentrypath += f"/{variantresult.entry_path}"
            entrypathsforlanguages[language] = langentrypath
        return documentation._DocumentGenerateAllLanguagesResult(resultdir.disowned(), "",
                                                                 entrypathsforlanguages)
