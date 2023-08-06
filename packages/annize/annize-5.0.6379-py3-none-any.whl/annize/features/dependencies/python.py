# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import annize.callconv
import annize.features.dependencies.common


class Python(annize.features.dependencies.common.Dependency):

    @annize.callconv.parameter_from_childnodes("kind")
    def __init__(self, *, version: str, kind: annize.features.dependencies.common.Kind = None):
        super().__init__(kind=kind, label=f"Python {version}", icon="python")
