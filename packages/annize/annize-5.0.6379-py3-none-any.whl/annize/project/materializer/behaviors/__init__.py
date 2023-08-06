# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import abc
import typing as t

import annize.project.materializer.core


class Behavior(abc.ABC):

    @abc.abstractmethod
    def node_context(self, nodemat: annize.project.materializer.core.NodeMaterialization) -> t.ContextManager:
        pass

    def stop_materialization_here_and_try_again(self) -> None:
        raise annize.project.materializer.core.TryAgain()
