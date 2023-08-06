# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import hashlib
import typing as t

import annize.callconv
import annize.features.base
import annize.features.dependencies.common
import annize.features.distributables.common
import annize.features.documentation.sphinx.rst
import annize.features.homepage.common
import annize.fs
import annize.i18n


class Section(annize.features.homepage.common.HomepageSection):

    @annize.callconv.parameter_from_childnodes("distributables")
    def __init__(self, *, distributables: t.List[annize.features.distributables.common.Group],
                 dependencies: t.List[annize.features.dependencies.common.Dependency],
                 head=annize.i18n.TrStr.tr("an_HP_Head_Download"), sortindex=40_000):
        super().__init__(head=head, sortindex=sortindex)  # TODO i18n
        self.__distributables = distributables
        self.__dependencies = dependencies

    def __generate_packagelist(self, info: annize.features.homepage.common.HomepageSection._GenerateInfo):
        content = ""
        lblfile = annize.i18n.tr("an_HP_DL_File")
        lblreleasetime = annize.i18n.tr("an_HP_DL_Releasetime")
        lblsha256sum = annize.i18n.tr("an_HP_DL_Sha256sum")
        lblsize = annize.i18n.tr("an_HP_DL_Size")
        info.customarg = []  # TODO now we do that once per language (as its called in _generate())
        for dlgroup in self.__distributables:
            groupcontent = f".. rubric:: {dlgroup.title}\n\n{dlgroup.description}\n\n"
            for dlfile in dlgroup.get_files():
                info.customarg.append(dlfile)
                ctime = dlfile.created_time().strftime('%Y-%m-%d %H:%M')
                fhash = filehash(dlfile.readable_path())
                ssize = friendly_filesize(dlfile.filesize())
                groupcontent += (f".. rst-class:: downloadblock\n\n"
                                 f":{lblfile}: `{dlfile.basename()} <{info.document_root_url}{dlfile.basename()}>`_\n"
                                 f":{lblreleasetime}: {ctime}\n"
                                 f":{lblsha256sum}: :samp:`{fhash}`\n"
                                 f":{lblsize}: {ssize}\n\n")
            content += groupcontent
        return content

    def preproc_generate(self, info):  # TODO weird
        for dlgroup in self.__distributables:
            for dlfile in dlgroup.get_files():
                dlfile.basename()  # TODO weird

    def postproc_generate(self, info):  # TODO inconsistent method naming ("_")
        dlfiles: t.List[annize.fs.FsEntry] = info.customarg
        for dlfile in dlfiles:
            dlfile.owned().move_to(info.document_root_directory.child_by_relative_path(dlfile.basename()).path())

    def _generate(self, info):  # TODO make package generation in "en" culture context ?!
        projectname = annize.features.base.pretty_project_name()
        product = self.Product()
        depslist = annize.features.dependencies.common.dependencies_to_rst_text(self.__dependencies)
        packagelist = self.__generate_packagelist(info)
        if packagelist:
            pkghead = annize.i18n.tr("an_HP_DL_PackagesAvailable")
            if depslist:
                thereqs = annize.i18n.tr("an_HP_DL_TheReqs")
                dependenciesref = f":ref:`{thereqs}<hp_downl_deps>`"
                pkghead += " " + annize.i18n.tr("an_HP_DL_CheckReqs").format(**locals())
            product.append_rst(pkghead)
            product.append_rst(packagelist)
        if depslist:
            product.append_rst(annize.features.documentation.sphinx.rst.RstGenerator.heading(
                annize.i18n.tr("an_HP_DL_Deps"), sub=True, anchor="hp_downl_deps"))
            product.append_rst(annize.i18n.tr("an_HP_DL_Uses3rdParty").format(**locals()))
            product.append_rst(depslist)
        return product


def friendly_filesize(isize: int) -> str:
    ssize = annize.i18n.tr("an_HP_DL_FriendlySize_B")
    for nssize in [
        annize.i18n.tr("an_HP_DL_FriendlySize_kB"),
        annize.i18n.tr("an_HP_DL_FriendlySize_MB"),
        annize.i18n.tr("an_HP_DL_FriendlySize_GB"),
        annize.i18n.tr("an_HP_DL_FriendlySize_TB"),
        annize.i18n.tr("an_HP_DL_FriendlySize_PB"),
        annize.i18n.tr("an_HP_DL_FriendlySize_EB"),
        annize.i18n.tr("an_HP_DL_FriendlySize_ZB"),
        annize.i18n.tr("an_HP_DL_FriendlySize_YB")
    ]:
        if isize > 1024:
            isize = isize / 1024.0
            ssize = nssize
        else:
            break
    return f"{isize:.1f} {ssize}"  #  TODO i18n


def filehash(filepath: str) -> str:
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while True:
            block = f.read(1024 ** 2)
            if block == b"":
                break
            hasher.update(block or b"")
    return hasher.hexdigest()


# TODO noh packagestore
