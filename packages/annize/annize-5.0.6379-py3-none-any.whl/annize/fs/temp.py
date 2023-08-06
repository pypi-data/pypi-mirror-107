# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import atexit
import os
import tempfile
import typing as t

import annize.data
import annize.fs


class _TempDir(annize.fs.FsEntry):

    def __init__(self, dirname: t.Optional[str] = None, temprootpath: t.Optional[str] = None):
        super().__init__(is_ownable=True)
        self.__path = self.__outerpath = f"{temprootpath or tempfile.gettempdir()}/{annize.data.UniqueId()}"
        self.restrict_path(dirname or "_")
        self.owned().mkdir(exist_ok=False)
        atexit.register(self.__cleanup)

    def readable_path(self):
        return self.__path

    def restrict_path(self, path):
        self.__path = os.path.abspath(f"{self.__path}/{path}")

    def __cleanup(self):
        try:
            annize.fs.fsentry_by_path(self.__outerpath, is_ownable=True, is_owned=True).remove()
        except IOError:
            pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            return super().__exit__(exc_type, exc_val, exc_tb)
        finally:
            self.__cleanup()


class TempFileByContent(annize.fs.AdHocFsEntry):

    def __init__(self, *, content: t.AnyStr, filename: t.Optional[str] = "afile"):
        super().__init__()
        self.__content = content if isinstance(content, bytes) else (content or "").encode()
        self.__filename = filename

    def _initialize(self) -> annize.fs.FsEntry:
        result = _TempDir()
        with open(f"{result.owned().path()}/{self.__filename}", "wb") as f:
            f.write(self.__content)
        result.restrict_path(self.__filename)
        return result


def fresh_temp_dir(dirname: t.Optional[str] = None, *, temprootpath: t.Optional[str] = None) -> "_TempDir":
    return _TempDir(dirname, temprootpath)
