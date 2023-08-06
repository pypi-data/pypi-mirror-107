# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import contextlib

import annize.context
import annize.project.materializer.behaviors
import annize.project.materializer.core


class BlockBehavior(annize.project.materializer.behaviors.Behavior):

    @contextlib.contextmanager
    def node_context(self, nodemat):
        yield
        if isinstance(nodemat.node, (annize.project.BlockNode, annize.project.FileNode)):
            nodemat.set_materialized_result(nodemat.get_materialized_children())
