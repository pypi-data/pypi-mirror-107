# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import contextlib

import annize.project.materializer.behaviors
import annize.project.materializer.core


class BasketBehavior(annize.project.materializer.behaviors.Behavior):

    @contextlib.contextmanager
    def node_context(self, nodemat):
        yield
        if nodemat.has_result:
            newresult = []
            for resultitem in nodemat.result:
                if getattr(resultitem, "_is_annize_basket", False) \
                        or isinstance(resultitem, annize.data.Basket):
                    newresult += resultitem
                else:
                    newresult.append(resultitem)
            nodemat.set_materialized_result(newresult)
