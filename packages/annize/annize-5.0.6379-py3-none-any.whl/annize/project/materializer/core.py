# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import contextlib
import itertools
import logging
import typing as t

import annize.context
import annize.project

if t.TYPE_CHECKING:
    import annize.project.featureloader
    import annize.project.materializer.behaviors


_logger = logging.getLogger(__name__)

_Material = t.Optional[t.Any]

_Materialization = t.Tuple[annize.project.Node, t.List[_Material]]


class NodeMaterialization:

    def __init__(self, materializer: "ProjectMaterializer", node: annize.project.Node, store: t.Dict):
        self.__node = node
        self.__materializer = materializer
        self.__store = store
        self.__result = None

    @property
    def node(self) -> annize.project.Node:
        return self.__node

    def set_materialized_result(self, resultlist):
        self.__result = resultlist

    def get_materialized_children_tuples(self):
        return self.__materializer._materialize_hlp_childobjs(self.__node, self.__store)

    def get_materialized_children(self) -> t.Iterable[_Material]:
        return list(itertools.chain.from_iterable([x[1] for x in self.get_materialized_children_tuples()]))

    def try_get_materialization_for_node(self, node: annize.project.Node):
        return self.__store.get(node, None)

    @property
    def has_result(self):
        return self.__result is not None

    @property
    def result(self):
        if not self.has_result:
            raise RuntimeError("No result available")
        return self.__result


class ProjectMaterializer:

    def __init__(self, node: annize.project.Node, *,
                 behaviors: t.Iterable["annize.project.materializer.behaviors.Behavior"]):
        self.__node = node
        self.__behaviors = behaviors

    def __materialization_for_node(self, node: annize.project.Node, store: t.Dict) -> NodeMaterialization:
        result = store.get(node, None)
        if not result:
            result = store[node] = NodeMaterialization(self, node, store)
        return result

    def __materialize(self, node: annize.project.Node, store: t.Dict) -> t.List[_Material]:
        nodemat = self.__materialization_for_node(node, store)
        _logger.debug("Starting materialization of '%s'; nodemat.has_result=%r", node, nodemat.has_result)
        if not nodemat.has_result:
            with contextlib.ExitStack() as stack:
                for behavior in self.__behaviors:
                    stack.enter_context(behavior.node_context(nodemat))
        _logger.debug("Finalized materialization of '%s' to '%s'", node, nodemat.result)
        return nodemat.result

    def _materialize_hlp_childobjs(self, node: annize.project.Node, store: t.Dict) -> t.List[_Materialization]:
        _logger.debug("Starting materialization of the children of '%s'", node)
        result = []
        for icnode, cnode in enumerate(node.children):
            try:
                result.append((cnode, self.__materialize(cnode, store)))
            except Exception as ex:
                if getattr(ex, "retry_can_help", False):
                    _logger.debug("Got an %s during materialization of a child, but will now make dry runs for the"
                                  " remaining ones in order to help resolving stuff later.", type(ex).__name__)
                    for nodechild in node.children[icnode+1:]:
                        try:
                            self.__materialize(nodechild, store)
                        except Exception as ex2:
                            if not getattr(ex2, "retry_can_help", False):
                                raise
                raise
        _logger.debug("Finished materialization of the children of '%s' to %d items", node, len(result))
        return result

    def get_materialized(self) -> t.List[t.Optional[t.Any]]:
        materializationstore = {}
        while True:
            try:
                result = self.__materialize(self.__node, materializationstore)
                break
            except TryAgain:
                _logger.debug("Trying again from start now.")
        for obj in result:
            annize.context.current().mark_object_as_toplevel(obj)
        return result


class TryAgain(BaseException):
    pass
