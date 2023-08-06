# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import contextlib

import annize.project.materializer.behaviors
import annize.project.materializer.core


class FeatureUnavailableBehavior(annize.project.materializer.behaviors.Behavior):

    def __init__(self):
        self.__skipnode_featureignorelist = []

    @contextlib.contextmanager
    def __context_skipnode_featureignorelist(self, node):
        self.__skipnode_featureignorelist.append(node.feature)
        try:
            yield
        finally:
            self.__skipnode_featureignorelist.remove(node.feature)

    @contextlib.contextmanager
    def __context_catchexceptions(self, nodemat, featureignorelist):
        try:
            yield
        except annize.project.FeatureUnavailableError as ex:
            if ex.featurename in featureignorelist:
                nodemat.set_materialized_result([])
            else:
                raise

    @contextlib.contextmanager
    def node_context(self, nodemat):
        with contextlib.ExitStack() as contexts:
            if isinstance(nodemat.node, annize.project.CallableNode):
                contexts.enter_context(self.__context_catchexceptions(nodemat, self.__skipnode_featureignorelist))
            elif isinstance(nodemat.node, annize.project.OnFeatureUnavailableNode):
                if nodemat.node.do == annize.project.OnFeatureUnavailableNode.Action.SKIP_NODE:
                    contexts.enter_context(self.__context_skipnode_featureignorelist(nodemat.node))
                elif nodemat.node.do == annize.project.OnFeatureUnavailableNode.Action.SKIP_BLOCK:
                    contexts.enter_context(self.__context_catchexceptions(nodemat, [nodemat.node.feature]))
                else:
                    raise annize.project.MaterializerError(f"Invalid 'do' for '{nodemat.node}'")
            yield
