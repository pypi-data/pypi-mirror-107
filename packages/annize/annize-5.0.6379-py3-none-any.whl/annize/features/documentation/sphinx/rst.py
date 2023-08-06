# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import typing as t

import annize.callconv
import annize.features.documentation.sphinx.common
import annize.fs


#TODO

class RstGenerator:#TODO
    """
    Generator for some documentation source parts.
    """

    @staticmethod
    def heading(text: str, *, variant: str = "=", sub: bool = False, anchor: t.Optional[str] = None) -> str:#TODO i18n typing
        #TODO refactor that mess (large module name; unclear usage of variant/sub)
        """
        Generates documentation source for a section heading.
        """
        text = str(text)
        hrule = (variant * len(text))
        return "\n\n" + (f".. _{anchor}:\n\n" if anchor else "") + ("" if sub else f"{hrule}\n") \
               + f"{text}\n{hrule}\n\n"
