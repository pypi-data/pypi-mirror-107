# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import typing as t

import annize.callconv
import annize.context
import annize.data
import annize.fs
import annize.i18n


class File(annize.fs.FsEntry):#TODO needed

    def __init__(self):
        super().__init__()


class PackageStore:

    def store_package(self, fsentries: t.Iterable[annize.fs.FsEntry], *, name: str) -> None:
        raise NotImplementedError()

    def get_package(self, *, name: str) -> t.Optional[t.Iterable[annize.fs.FsEntry]]:
        raise NotImplementedError()

    #TODO weird
    def get_package_history(self, *, name: str, limit: int = 3) -> t.Iterable[t.Iterable[annize.fs.FsEntry]]:
        raise NotImplementedError()


class Group:

    @annize.callconv.parameter_from_childnodes("files",
                                               if_typehint_matches=False, if_passing=annize.callconv.always_true)
    @annize.callconv.parameter_from_childnodes("packagestore")
    def __init__(self, *, title: str, files: t.List[annize.fs.FsEntry], description: str = "",
                 packagestore: PackageStore = None):
        self.__title = title
        self.__files = files
        self.__description = description
        self.__packagestore = packagestore

    @property
    def title(self) -> str:
        return annize.i18n.tr_if_trstr(self.__title)

    def get_files(self) -> t.List[annize.fs.FsEntry]:
        try:
            for file in self.__files:
                file.readable_path()
        except Exception:  # TODO logging
            frompkgstore = self.__get_files_from_packagestore()
            if frompkgstore is not None:
                return list(frompkgstore)
            raise
        self.__store_files_to_packagestore()
        return self.__files

    @property
    def description(self) -> str:
        return annize.i18n.tr_if_trstr(self.__description)

    @property
    def packagestore(self) -> t.Optional[PackageStore]:
        return self.__packagestore

    def __get_files_from_packagestore(self) -> t.Iterable[annize.fs.FsEntry]:
        if self.__packagestore:
            # TODO user interaction
            return self.__packagestore.get_package(name=self.__getname())

    def __store_files_to_packagestore(self) -> None:
        if self.__packagestore:
            self.__packagestore.store_package(self.__files, name=self.__getname())  #TODO pattern=annize.featur.... weg

    def __getname(self) -> str:
        myname = annize.context.object_name(self)
        if not annize.context.is_friendly_name(myname):  # TODO rename is_friendly_name to "is_stable_name" ?!
            raise Exception("TODO")
        return myname
