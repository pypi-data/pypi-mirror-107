# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import os
import subprocess

import annize.features.base
import annize.features.testing.common


class Test(annize.features.testing.common.Test):

    def __init__(self, *, testdir: str, src: str):
        super().__init__()
        self.__src = src  # TODO use FsEntry instead
        self.__testdir = testdir  # TODO use FsEntry instead

    def run(self):
        project_directory = annize.features.base.project_directory()
        # TODO zz
        os.environ["PYTHONPATH"] = os.environ.get("PYTHONPATH", "") +\
                                   f':{os.path.dirname(f"{project_directory}/{self.__testdir}")}'
        # TODO zz see the mess in anise4
        subprocess.check_call(["pytest", f"{project_directory}/{self.__testdir}"],
                              cwd=f"{project_directory}/{self.__src}")
