# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

"""
Materializing of Annize projects into a working structure.
"""

import typing as t

import annize.callconv
import annize.project.featureloader
import annize.project.materializer.core

if t.TYPE_CHECKING:
    import annize.project


def materialize(
        nodes: t.Iterable["annize.project.FileNode"], *,
        featureloader: t.Optional[annize.project.featureloader.FeatureLoader] = None) -> t.List[t.Optional[t.Any]]:
    import annize.project.materializer.behaviors.argument as argument
    import annize.project.materializer.behaviors.basket as basket
    import annize.project.materializer.behaviors.block as block
    import annize.project.materializer.behaviors.featureunavailable as featureunavailable
    import annize.project.materializer.behaviors.reference as reference
    import annize.project.materializer.preprocessors as preprocessors
    featureloader = featureloader or annize.project.featureloader.DefaultFeatureLoader()
    nodes = [node.clone() for node in nodes]
    for preprocessor in [preprocessors.resolve_appendtonodes, preprocessors.normalize_blockscopes]:
        nodes = preprocessor(nodes)
    rootblock = annize.project.BlockNode()
    for node in nodes:
        rootblock.append_child(node)
    return annize.project.materializer.core.ProjectMaterializer(
        rootblock, behaviors=[
            basket.BasketBehavior(),
            featureunavailable.FeatureUnavailableBehavior(),
            reference.SkipUnresolvableReferenceBehavior(rootblock),
            reference.ReferenceBehavior(rootblock),
            block.BlockBehavior(),
            argument.ArgumentBehavior(annize.callconv.call, featureloader=featureloader)
        ]).get_materialized()
