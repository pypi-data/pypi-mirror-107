# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import typing as t

import annize.callconv


class Task:

    @annize.callconv.parameter_from_childnodes("innertasks")
    def __init__(self, *, innertasks: t.List[object]):#TODO t.List[t.Any]
        self.__innertasks = innertasks

    def __call__(self, *args, **kwargs):
        for innertask in self.__innertasks:
            innertask(*args, **kwargs)
