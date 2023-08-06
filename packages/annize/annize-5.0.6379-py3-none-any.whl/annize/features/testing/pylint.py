# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import subprocess

import annize.callconv
import annize.features.testing.common
import annize.fs


class Test(annize.features.testing.common.Test):

    @annize.callconv.parameter_from_childnodes("src")
    def __init__(self, *, src: annize.fs.FsEntry):
        super().__init__()
        self.__src = src

    def run(self):
        srcpath = self.__src.readable_path()
        subprocess.check_call(["pylint", srcpath], cwd=srcpath)
