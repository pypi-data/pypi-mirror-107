# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import typing as t

import annize.callconv
import annize.context
import annize.data


class RunTests:

    def __init__(self, **b):  # TODO selective (some tests only)
        pass

    def __call__(self, *args, **kwargs):
        for test in annize.context.objects_by_type(Test):
            test.run()


class Test:

    def run(self):
        raise NotImplementedError()


class TestGroup(Test):

    @annize.callconv.parameter_from_childnodes("tests")
    def __init__(self, *, tests: t.List[Test]):
        self.__tests = tests

    def run(self):
        for test in self.__tests:
            test.run()
