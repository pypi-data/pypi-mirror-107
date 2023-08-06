# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import datetime

import annize.callconv
import annize.features.changelog.common
import annize.features.documentation.sphinx.rst
import annize.features.homepage.common
import annize.i18n


class Section(annize.features.homepage.common.HomepageSection):

    @annize.callconv.parameter_from_childnodes("changelog")
    def __init__(self, *, changelog: annize.features.changelog.common.Changelog = None,
                 head=annize.i18n.TrStr.tr("an_HP_Head_Changelog"), sortindex=60_000):
        super().__init__(head=head, sortindex=sortindex)  # TODO i18n
        self.__changelog = changelog

    def _generate(self, info):
        changelog = self.__changelog or annize.features.changelog.common.default_changelog()
        if changelog:
            entries = changelog.entries
            entries.sort(key=lambda e: (e.time, e.version))
            entries.reverse()
            if len(entries) > 0:
                result = self.Product()
                now = datetime.datetime.now()
                for ientry, entry in enumerate(entries):
                    if (ientry > 0) and entry.time and (now - entry.time > datetime.timedelta(days=365)):
                        break
                    result.append_rst("") # TODO
                    entryhead = []
                    if entry.time:
                        entryhead.append(str(entry.time.date()))  # TODO i18n
                    if entry.version:
                        entryhead.append(str(entry.version))
                    if len(entryhead) == 0:
                        raise Exception("TODO")
                    result.append_rst(annize.features.documentation.sphinx.rst.RstGenerator.heading(
                        ", ".join(entryhead), sub=True))
                    for entryitem in entry.items:
                        result.append_rst("- " + str(entryitem.text).strip().replace("\n", "  \n"))
                return result
        return None
