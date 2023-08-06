# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import typing as t

import annize.callconv
import annize.context
import annize.features.documentation.sphinx.rst
import annize.features.homepage.common
import annize.features.mediagalleries
import annize.i18n


class Section(annize.features.homepage.common.HomepageSection):

    @annize.callconv.parameter_from_childnodes("mediagalleries")
    def __init__(self, *, head=annize.i18n.TrStr.tr("an_HP_Head_Gallery"), sortindex=50_000,
                 mediagalleries: t.List[annize.features.mediagalleries.Gallery]):
        super().__init__(head=head, sortindex=sortindex)  # TODO i18n
        self.__mediagalleries = mediagalleries

    def preproc_generate(self, info):
        info.customarg = {}
        for gallery in self.__mediagalleries:
            gallerydirname = annize.context.object_name(gallery)
            gallerydir = info.document_root_directory.child_by_relative_path(gallerydirname)
            gallerydir.mkdir()
            info.customarg[gallery] = galleryitems = []
            for item in gallery.items:
                itemfile = gallerydir.child_by_relative_path(item.file.basename())
                item.file.owned().move_to(itemfile.path())
                galleryitems.append((item, f"{info.document_root_url}{gallerydirname}/{itemfile.basename()}"))

    def _generate(self, info):
        if len(self.__mediagalleries) > 0:
            result = self.Product()
            for mediagallery in self.__mediagalleries:
                if mediagallery.title:
                    result.append_rst(annize.features.documentation.sphinx.rst.RstGenerator.heading(mediagallery.title,
                                                                                                    variant="~"))
                galleryrst = ".. rst-class:: annizedoc-mediagallery\n\n"
                for item, itemurl in info.customarg[mediagallery]:
                    mtitle = str(item.description).replace("\n", " ").replace('"', "''")
                    mediatype = "image"  # TODO
                    galleryrst += f" `{mtitle} <{itemurl}#{mediatype}>`__\n"
                result.append_rst(galleryrst)
            return result
        return None
