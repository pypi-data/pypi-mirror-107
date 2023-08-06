# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import contextlib
import typing as t

import annize.context
import annize.project.materializer.behaviors
import annize.project.materializer.core


class ReferenceBehavior(annize.project.materializer.behaviors.Behavior):

    def __init__(self, rootblock):
        super().__init__()
        self.__rootblock = rootblock
        self.__is_retry_useful = False

    @contextlib.contextmanager
    def resolver_node_context(self, nodemat):
        yield
        if isinstance(nodemat.node, annize.project.ReferenceNode):
            obj = annize.context.object_by_name(nodemat.node.reference_key, self)
            if obj == self:
                raise annize.project.UnresolvableReferenceError(nodemat.node.reference_key)
            nodemat.set_materialized_result([obj])

    @contextlib.contextmanager
    def detect_retry_useful_node_context(self, nodemat):
        had_result = nodemat.has_result
        yield
        if (not had_result) and nodemat.has_result:
            self.__is_retry_useful = True

    @contextlib.contextmanager
    def retry_node_context(self, nodemat):
        try:
            yield
        except annize.project.UnresolvableReferenceError:
            if nodemat.node != self.__rootblock or not self.__is_retry_useful:
                raise
            self.__is_retry_useful = False
            self.stop_materialization_here_and_try_again()

    @contextlib.contextmanager
    def node_context(self, nodemat):
        with self.detect_retry_useful_node_context(nodemat):
            with self.retry_node_context(nodemat):
                with self.resolver_node_context(nodemat):
                    yield


class SkipUnresolvableReferenceBehavior(annize.project.materializer.behaviors.Behavior):

    def __init__(self, rootblock):
        super().__init__()
        self.__rootblock = rootblock

    @contextlib.contextmanager
    def node_context(self, nodemat):
        try:
            yield
        except annize.project.UnresolvableReferenceError:
            if nodemat.node != self.__rootblock:
                raise
            do_rerun = False
            for unresolvable_reference in self.__unresolvable_references(nodemat):
                if unresolvable_reference.on_unresolvable == annize.project.ReferenceNode.OnUnresolvableAction.SKIP:
                    if self.__reference_is_hopeless(unresolvable_reference, rootnodemat=nodemat):
                        unresolvable_reference.parent.remove_child(unresolvable_reference)
                        do_rerun = True
            if not do_rerun:
                raise
            self.stop_materialization_here_and_try_again()

    @staticmethod
    def __unresolvable_references(rootnodemat) -> t.List[annize.project.ReferenceNode]:
        result = []
        nodes = [rootnodemat.node]
        while nodes:
            node = nodes.pop()
            for childnode in node.children:
                nodes.append(childnode)
            if isinstance(node, annize.project.ReferenceNode):
                refnodemat = rootnodemat.try_get_materialization_for_node(node)
                if refnodemat and not refnodemat.has_result:
                    result.append(node)
        return result

    @classmethod
    def __reference_is_hopeless(cls, refnode: annize.project.ReferenceNode, *, rootnodemat) -> bool:
        for node in cls.__nodes_by_name(refnode.reference_key, rootnode=rootnodemat.node):
            if not cls.__node_is_hopeless(node, rootnodemat):
                return False
        return True

    @classmethod
    def __node_is_hopeless(cls, node: annize.project.Node, rootnodemat) -> bool:
        while node:
            if rootnodemat.try_get_materialization_for_node(node).has_result:
                return True
            node = node.parent
        return False

    @staticmethod
    def __nodes_by_name(name: str, *, rootnode: annize.project.Node) -> t.List[annize.project.Node]:
        result = []
        nodes = [rootnode]
        while nodes:
            node = nodes.pop()
            for childnode in node.children:
                nodes.append(childnode)
            if isinstance(node, annize.project.ArgumentNode) and node.name == name:
                result.append(node)
        return result
