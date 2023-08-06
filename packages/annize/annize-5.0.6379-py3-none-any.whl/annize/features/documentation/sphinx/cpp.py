# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import annize.features.documentation.sphinx.doxygencompat


class CppApiReferenceLanguage(annize.features.documentation.sphinx.doxygencompat.DoxygenSupportedApiReferenceLanguage):
    """
    C++ language support for api references.
    """

    def __init__(self, **kwargs):
        super().__init__(file_patterns="*.c *.cc *.cxx *.cpp *.c++ *.ii *.ixx *.ipp *.i++ *.inl *.idl *.ddl *.h *.hh"
                                       " *.hxx *.hpp *.h++", **kwargs)
