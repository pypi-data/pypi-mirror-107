# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import contextlib
import inspect

import annize.context
import annize.data
import annize.project.materializer.behaviors
import annize.project.materializer.core
import annize.project.featureloader


class ArgumentBehavior(annize.project.materializer.behaviors.Behavior):

    def __init__(self, callfct, *, featureloader: annize.project.featureloader.FeatureLoader):
        # TODO xx remove those params from Materializer itself TODO typehints
        self.__featureloader = featureloader
        self.__callfct = callfct

    @contextlib.contextmanager
    def node_context(self, nodemat):
        yield
        if isinstance(nodemat.node, annize.project.CallableNode):
            args, kwargs = list(), dict()
            for childnode, childarguments in nodemat.get_materialized_children_tuples():
                if len(childarguments) > 0:
                    if isinstance(childnode, annize.project.ArgumentNode) and childnode.arg_name:
                        kwargs[childnode.arg_name] = childarguments[0]
                    else:
                        args += childarguments
            featuremodule = self.__featureloader.load_feature(nodemat.node.feature)
            if not featuremodule:
                raise annize.project.FeatureUnavailableError(nodemat.node.feature)
            try:
                clss = getattr(featuremodule, nodemat.node.callee)
            except AttributeError as ex:
                raise annize.project.MaterializerError(
                    f"No item '{nodemat.node.callee}' in feature module '{nodemat.node.feature}'") from ex
            clssspec = inspect.getfullargspec(clss)
            if len(clssspec.args) > 1 or clssspec.varargs:
                raise annize.project.MaterializerError(f"Callable '{nodemat.node.callee}' in '{nodemat.node.feature}'"
                                                       f" has position arguments, which is not allowed")
            try:
                value = self.__callfct(clss, args, kwargs)
            except TypeError as ex:
                raise annize.project.MaterializerError(f"Unable to construct"
                                                       f" '{nodemat.node.feature}.{nodemat.node.callee}', {ex}") from ex
        elif isinstance(nodemat.node, annize.project.ScalarValueNode):
            value = nodemat.node.value
        else:
            return
        if nodemat.node.name:
            annize.context.set_object_name(value, nodemat.node.name)
        nodemat.set_materialized_result([value])
        annize.context.add_object(value)
