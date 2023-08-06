# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import annize.features.base
import annize.features.homepage.common
import annize.i18n


class Section(annize.features.homepage.common.HomepageSection):

    def __init__(self, *, imprint: str, head=annize.i18n.TrStr.tr("an_HP_Head_Imprint"), sortindex=70_000):
        super().__init__(head=head, sortindex=sortindex)  # TODO i18n
        self.__imprint = imprint

    def _generate(self, info):
        imprint = annize.features.base.imprint() if (self.__imprint is None) else self.__imprint
        return annize.i18n.tr_if_trstr(imprint) or None
