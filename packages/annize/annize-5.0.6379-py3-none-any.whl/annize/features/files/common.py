# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import re
import typing as t

import annize.callconv
import annize.features.base
import annize.fs.temp


class FsEntry(annize.fs.AdHocFsEntry):  # TODO what is it for?!

    @annize.callconv.parameter_from_childnodes("root")
    def __init__(self, *, root: annize.fs.FsEntry = None, path: str = None):
        super().__init__()
        self.__root = root or ProjectDir()
        self.__relative_path = path

    @property
    def root(self) -> annize.fs.FsEntry:
        return self.__root

    @property
    def relative_path(self) -> str:
        return self.__relative_path

    def _initialize(self):
        return self.root.child_by_relative_path(self.relative_path)


class File(FsEntry):
    pass


class Exclude:

    def __init__(self, *, by_path_pattern: str = None, by_path: str = None,
                 by_name_pattern: str = None, by_name: str = None):  # TODO inverse, and/or, ...
        self.__by_path_pattern = re.compile(by_path_pattern) if by_path_pattern else None
        self.__by_path = by_path
        self.__by_name_pattern = re.compile(by_name_pattern) if by_name_pattern else None
        self.__by_name = by_name

    @staticmethod
    def __does_exclude(text: str, by_text: str, by_pattern: re.Pattern) -> bool:
        return (by_text == text) or (by_pattern and by_pattern.fullmatch(text))

    def does_exclude(self, relative_path: str, source: annize.fs.FsEntry, destination: annize.fs.FsEntry) -> bool:
        return self.__does_exclude(relative_path, self.__by_path, self.__by_path_pattern) \
               or self.__does_exclude(source.basename(), self.__by_name, self.__by_name_pattern)


class DirPart:

    @annize.callconv.parameter_from_childnodes("excludes")
    @annize.callconv.parameter_from_childnodes("root")
    def __init__(self, *, excludes: t.Iterable[Exclude] = None, root: annize.fs.FsEntry = None,
                 source_path: str = None, destination_path: str = None, path: str = None,
                 destination_is_parent: bool = False):
        self.__excludes = excludes or ()
        if path is not None:
            if (source_path is not None) or (destination_path is not None):
                raise Exception("TODO")
            source_path = destination_path = path
        self.__root = root
        self.__source_path = source_path
        self.__destination_path = destination_path
        self.__destination_is_parent = destination_is_parent

    @property
    def excludes(self) -> t.Iterable[Exclude]:
        return self.__excludes

    @property
    def root(self) -> t.Optional[annize.fs.FsEntry]:
        return self.__root

    @property
    def path(self) -> str:
        return self.__source_path

    @property
    def destination_path(self) -> str:
        return self.__destination_path

    @property
    def destination_is_parent(self) -> bool:
        return self.__destination_is_parent


class Dir(FsEntry):

    @annize.callconv.parameter_from_childnodes("excludes")
    @annize.callconv.parameter_from_childnodes("parts")
    def __init__(self, *, excludes: t.Iterable[Exclude], parts: t.Iterable[DirPart],
                 root: annize.fs.FsEntry = None, path: str = None, name: str = None):  # TODO xx temp ?! cleanup?!
        super().__init__(root=root, path=path)
        self.__excludes = excludes
        self.__parts = parts
        self.__name = name

    @classmethod
    def __transfer_predicate_and(cls, *predicates: annize.fs._TransferPredicate) -> annize.fs._TransferPredicate:
        def pred(relpath, srcf, destf):
            for predicate in predicates:
                if not predicate(relpath, srcf, destf):
                    return False
            return True
        return pred

    @classmethod
    def __transfer_predicate_for_exclude(cls, exclude: Exclude) -> annize.fs._TransferPredicate:
        def pred(relpath, srcf, destf):
            return not exclude.does_exclude(relpath, srcf, destf)
        return pred

    @classmethod
    def __transfer_predicate_for_excludes(cls, excludes: t.Iterable[Exclude]) -> annize.fs._TransferPredicate:
        def result(*_):
            return True
        for exclude in excludes:
            result = cls.__transfer_predicate_and(result, cls.__transfer_predicate_for_exclude(exclude))
        return result

    def _initialize(self):
        result = annize.fs.temp.fresh_temp_dir(dirname=self.__name).owned()
        if not self.__parts and not self.__excludes: # TODO nicer (keep original path if possible)
            return self.root.child_by_relative_path(self.relative_path)
        parts = list(self.__parts)
        if self.relative_path is not None:
            parts.append(DirPart(root=self.root, path=self.relative_path))
        for part in parts:
            transfer_predicate = self.__transfer_predicate_for_excludes(list(self.__excludes) + list(part.excludes))
            partsrc = part.root or self.root
            if part.path:
                partsrc = partsrc.child_by_relative_path(part.path)
            partdest = result
            if part.destination_path:
                partdest = partdest.child_by_relative_path(part.destination_path)
            partsrc.copy_to(partdest.path(), merge=True, transfer_predicate=transfer_predicate,
                            path_is_parent=part.destination_is_parent)
        return result.disowned()  # TODO maybe better unownable?! or depending on if we have a friendly_name?!


class ProjectDir(annize.fs.AdHocFsEntry):#TODO rename  ...Directory ?! as MachineRootDirectory

    def _initialize(self):
        return annize.fs.fsentry_by_path(annize.features.base.project_directory(), is_ownable=False)  # TODO is_ownable=False ?! nicer?!


class MachineRootDirectory(annize.fs.AdHocFsEntry):

    def _initialize(self):
        return annize.fs.fsentry_by_path("/", is_ownable=False)  # TODO is_ownable=False ?! nicer?!
