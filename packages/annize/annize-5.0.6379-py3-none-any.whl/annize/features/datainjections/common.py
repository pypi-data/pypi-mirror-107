# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import annize.callconv
import annize.fs.temp


class Injection(annize.fs.AdHocFsEntry):

    def _initialize(self):
        result = annize.fs.temp.fresh_temp_dir()
        self.inject(result)
        return result

    def inject(self, destination: annize.fs.FsEntry):
        raise NotImplementedError()


class Inject:

    @annize.callconv.parameter_from_childnodes("destination")
    @annize.callconv.parameter_from_childnodes("injection")
    def __init__(self, *, injection: Injection, destination: annize.fs.FsEntry):
        self.__injection = injection
        self.__destination = destination

    def __call__(self):
        destination = annize.fs.fsentry_by_path(self.__destination.readable_path(), is_ownable=True)  # TODO weird
        self.__injection.inject(destination.owned())
