# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import annize.features.base
import annize.features.homepage.common
import annize.i18n


class Section(annize.features.homepage.common.HomepageSection):

    def __init__(self, *, head=annize.i18n.TrStr.tr("an_HP_Head_About"), sortindex=10_000):
        super().__init__(head=head, sortindex=sortindex)  # TODO i18n

    def _generate(self, info): # TODO ", language" needed ?!
        return annize.features.base.long_description() or None
