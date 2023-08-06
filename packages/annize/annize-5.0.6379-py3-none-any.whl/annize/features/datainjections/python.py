# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import annize.callconv
import annize.data
import annize.features.base
import annize.features.datainjections.common
import annize.fs


class Injection(annize.features.datainjections.common.Injection):

    @annize.callconv.parameter_from_childnodes("version")
    def __init__(self, *, filename: str = "_project_infos.py", version: annize.data.Version = None):
        super().__init__()
        self.__filename = filename
        self.__version = version

    def inject(self, destination: annize.fs.FsEntry):
        pieces = [
            ("homepage_url", annize.features.base.homepage_url()),
            ("version", str(self.__version))
        ]
        content = ""
        for piecekey, piecevalue in pieces:
            if piecevalue is not None:
                content += f"{piecekey} = {repr(piecevalue)}\n"
        destination.child_by_relative_path(self.__filename).write_file(content)
