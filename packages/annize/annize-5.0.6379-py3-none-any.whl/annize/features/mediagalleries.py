# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import typing as t

import annize.i18n
import annize.callconv
import annize.fs


class Gallery:

    class Item:

        def __init__(self, file, description):
            self.__file = file
            self.__description = description

        @property
        def file(self) -> annize.fs.FsEntry:
            return self.__file

        @property
        def description(self) -> str:#TODO i18n typing
            return self.__description

    @annize.callconv.parameter_from_childnodes("source")
    def __init__(self, *, source: annize.fs.FsEntry, title: str = ""): # TODO i18n typing
        self.__source = source
        self.__title = title

    @property
    def items(self) -> t.List[Item]:
        result = []
        # TODO
        for itemfile in self.__source.children():
            if not itemfile.basename().endswith(".png"):#TODO weg
                continue
            result.append(self.Item(itemfile, self._description_for_mediafile(itemfile)))
        return result

    @property
    def title(self) -> str: # TODO i18n typing
        return self.__title

    def _description_for_mediafile(self, itemfile: annize.fs.FsEntry) -> str:#TODO i18n typing
        variants = {}
        txtfiles = [tfl for tfl in itemfile.parent().children() if tfl.basename().endswith(".txt")]
        for varfile in [tfl for tfl in txtfiles if tfl.basename().startswith(f"{itemfile.basename()}.")]:
            varname = varfile.basename()[len(itemfile.basename())+1:-4]
            variants[varname] = varfile.read_file().decode().strip()
        otxtfile = itemfile.parent().child_by_relative_path(f"{itemfile.basename()}.txt")
        if otxtfile.exists():
            variants["?"] = otxtfile.read_file().decode()
        return annize.i18n.IndependentTrStr(**variants)
