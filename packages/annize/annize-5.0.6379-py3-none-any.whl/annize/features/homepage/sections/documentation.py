# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import typing as t

import annize.callconv
import annize.context
import annize.features.homepage.common
import annize.i18n


class Section(annize.features.homepage.common.HomepageSection):

    @annize.callconv.parameter_from_childnodes("documentation")
    def __init__(self, *, documentation: t.List[annize.features.documentation.common.Document],
                 head=annize.i18n.TrStr.tr("an_HP_Head_Documentation"), sortindex=30_000):
        super().__init__(head=head, sortindex=sortindex)  # TODO i18n
        self.__documentation = documentation

    def preproc_generate(self, info):
        info.customarg = {}
        for document in self.__documentation:
            documentdirname = annize.context.object_name(document)
            outputspec = annize.features.documentation.common.HtmlOutputSpec(title=document.title)  # TODO document.title
            genres = document.generate_all_languages(outputspec)
            genres.file.owned().move_to(info.document_root_directory.child_by_relative_path(documentdirname).path())
            info.customarg[document] = f"{info.document_root_url}{documentdirname}/index.html"

    def _generate(self, info):
        if len(self.__documentation) > 0:
            content = annize.i18n.tr("an_HP_Doc_DocsAvailable") + "\n\n"
            for document in self.__documentation:
                generateddocumenturl = info.customarg[document]
                content += f"`{document.title} <{generateddocumenturl}>`_\n\n"  # TODO document.title
            return content
        return None

# TODO show last three versions via packagestore
