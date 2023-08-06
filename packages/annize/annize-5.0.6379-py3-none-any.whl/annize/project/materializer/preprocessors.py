# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import itertools
import typing as t

import annize.data
import annize.project


def resolve_appendtonodes(nodes: t.Iterable[annize.project.Node]) -> t.Iterable[annize.project.Node]:
    referencetuples = []
    def plan_references(node: t.Optional[annize.project.Node], childnodes: t.Iterable[annize.project.Node]) -> None:
        if isinstance(node, annize.project.ArgumentNode) and node.append_to:
            pkey = node.name = (node.name or annize.data.UniqueId().long_str)
            referencetuples.append((pkey, node.append_to))
        for childnode in childnodes:
            plan_references(childnode, childnode.children)
    for fnode in nodes:
        plan_references(None, [fnode])
    unresolved_referencetuples = list(referencetuples)
    def create_references(node: t.Optional[annize.project.Node]) -> None:
        if isinstance(node, annize.project.ArgumentNode):
            for referencetuple in referencetuples:
                originname, appendttoname = referencetuple
                if node.name == appendttoname:
                    keyrefnode = annize.project.ReferenceNode()
                    keyrefnode.reference_key = originname
                    keyrefnode.on_unresolvable = annize.project.ReferenceNode.OnUnresolvableAction.SKIP
                    node.append_child(keyrefnode)
                    if referencetuple in unresolved_referencetuples:
                        unresolved_referencetuples.remove(referencetuple)
        for childnode in node.children:
            create_references(childnode)
    for fnode in nodes:
        create_references(fnode)
    if unresolved_referencetuples:
        raise annize.project.UnresolvableReferenceError(unresolved_referencetuples[0][1])
    return nodes


def normalize_blockscopes(nodes: t.Iterable[annize.project.Node]) -> t.Iterable[annize.project.Node]:
    def with_synthetic_blocks(fnodes: t.Iterable[annize.project.Node],
                              scope: annize.project.ScopableBlockNode.Scope,
                              _nodes: t.Iterable[annize.project.Node] = None):
        if _nodes is None:
            return with_synthetic_blocks(fnodes, scope, fnodes)
        for node in _nodes:
            fnodes = with_synthetic_blocks(fnodes, scope, node.children)
            if isinstance(node, annize.project.ScopableBlockNode) and node.scope == scope:
                if len(tuple(node.children)) > 0:
                    raise annize.project.MaterializerError(f"The node '{node}' must not have children")
                if (not node.parent) or (not isinstance(node.parent, annize.project.FileNode)):
                    raise annize.project.MaterializerError(f"The node '{node}' must be on top level of a file")
                blockclone = node.clone(with_children=False)
                node.parent.remove_child(node)
                blockclone.scope = annize.project.ScopableBlockNode.Scope.BLOCK
                for fnode in fnodes:
                    blockclone.append_child(fnode)
                fnodes = [blockclone]
        return fnodes
    nnodes = list(itertools.chain.from_iterable(
        [with_synthetic_blocks([fnode], annize.project.ScopableBlockNode.Scope.FILE) for fnode in nodes]))
    return with_synthetic_blocks(nnodes, annize.project.ScopableBlockNode.Scope.PROJECT)
