# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import subprocess
import typing as t

import annize.callconv
import annize.data
import annize.features.licensing
import annize.fs.temp


class Package(annize.fs.AdHocFsEntry):

    def _initialize(self):
        name = self.__packagename or annize.features.base.project_name()
        sauxversion = f"-{self.__version}" if self.__version else ""
        sauxnamepostfix = f"-{self.__packagenamepostfix}" if self.__packagenamepostfix else ""
        pkgroot = f"{name}{sauxversion}{sauxnamepostfix}"
        with self.__source.temp_clone(basename=pkgroot) as tarsrc:
            if self.__documentation:
                self.__documentation.copy_to(tarsrc.owned().path(), path_is_parent=True)
            license = self.__license or annize.features.licensing.project_licenses()[0]  # TODO
            tarsrc.owned().child_by_relative_path("LICENSE").write_file(license.text)
            resultdir = annize.fs.temp.fresh_temp_dir().owned()
            result = resultdir.child_by_relative_path(f"{pkgroot}.tgz")
            # TODO use "tarfile" module instead
            subprocess.check_call(["tar", "cfz", result.path(), pkgroot], cwd=tarsrc.parent().readable_path())
            return result.disowned()

    @annize.callconv.parameter_from_childnodes("source")
    @annize.callconv.parameter_from_childnodes("version")
    @annize.callconv.parameter_from_childnodes("license")
    @annize.callconv.parameter_from_childnodes("artifactstore")
    def __init__(self, *, packagename: t.Optional[str] = None, packagenamepostfix: t.Optional[str] = None,
                 source: annize.fs.FsEntry, version: annize.data.Version = None,
                 license: annize.features.licensing.License = None,
                 documentation: annize.fs.FsEntry = None):
        super().__init__()
        self.__packagename = packagename
        self.__packagenamepostfix = packagenamepostfix
        self.__source = source
        self.__version = version
        self.__license = license
        self.__documentation = documentation
