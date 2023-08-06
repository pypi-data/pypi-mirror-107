# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import dataclasses
import typing as t

import annize.callconv
import annize.context
import annize.features.base
import annize.features.dependencies.common
import annize.features.documentation.common
import annize.features.documentation.sphinx.output.html
import annize.features.documentation.sphinx.rst
import annize.features.distributables.common
import annize.features.mediagalleries
import annize.fs
import annize.fs.temp
import annize.i18n


class HomepageSection:

    @dataclasses.dataclass
    class _GenerateInfo:
        culture: annize.i18n.Culture
        customarg: t.Optional[object]
        document_root_url: str
        document_variant_directory: annize.fs.FsEntry
        document_variant_url: str

    @dataclasses.dataclass
    class _PrePostprocGenerateInfo:
        document_root_directory: annize.fs.FsEntry
        document_root_url: str
        customarg: t.Optional[object]

    class Product:

        def __init__(self, *, rst_text: str = "", media_files: t.List[annize.fs.FsEntry] = ()):
            self.__rst_text = rst_text or ""
            self.__media_files = list(media_files or ())

        @property
        def rst_text(self) -> str:
            return self.__rst_text

        @property
        def media_files(self) -> t.List[annize.fs.FsEntry]:
            return self.__media_files

        def append_rst(self, rst_text) -> None:
            self.__rst_text += rst_text + "\n\n"

        def attach_media_file(self, file: annize.fs.FsEntry) -> None:
            self.__media_files.append(file)

    def __init__(self, *, head: str, sortindex: int = 0):#TODO i18n types
        self.__head = head#TODO api not perfect for i18n
        self.__sortindex = sortindex

    def _generate(self, info: _GenerateInfo) -> t.Union[Product, str]:     #TODO  t.Union[Product, str]] -> only Product  ?!
        raise NotImplementedError()#TODO NotImplementedError vs abc.abstractclass   -> streamline

    @property
    def head(self):
        return annize.i18n.tr_if_trstr(self.__head)

    @property
    def sortindex(self):
        return self.__sortindex

    def preproc_generate(self, info: _PrePostprocGenerateInfo) -> None:
        pass

    def postproc_generate(self, info: _PrePostprocGenerateInfo) -> None:
        pass

    def generate(self, info: _GenerateInfo) -> t.Optional[Product]:
        product = self._generate(info)
        if isinstance(product, str):
            product = HomepageSection.Product(rst_text=product)
        return product


class Homepage:

    @annize.callconv.parameter_from_childnodes("sections")
    def __init__(self, *, title: t.Optional[str] = None, short_desc: t.Optional[str] = None,
                 sections: t.List[HomepageSection], languages: str = "?"):
        # TODO languages="?" ?!
        self.__title = title
        self.__short_desc = short_desc
        self.__sections = sections
        self.__languages = [la for la in [la.strip() for la in languages.split(" ")] if la]

    @property
    def languages(self) -> t.List[str]:
        return self.__languages

    @property
    def sections(self) -> t.List[HomepageSection]:
        return self.__sections

    @property
    def title(self) -> str:
        return self.__title or annize.features.base.pretty_project_name()

    @property
    def short_desc(self) -> str:
        return self.__short_desc or annize.features.base.summary()

    def _append_section(self, section: HomepageSection) -> None:
        self.__sections.append(section)

    @staticmethod
    def __generate_postpreproc(*, customargs: t.Dict, is_pre: bool,
                               document_root_directory: annize.fs.FsEntry, document_root_url: str):
        for section, customarg in customargs.items():
            prepostprocinfo = HomepageSection._PrePostprocGenerateInfo(
                customarg=customarg, document_root_directory=document_root_directory,
                document_root_url=document_root_url)
            prepostprocgenerate = section.preproc_generate if is_pre else section.postproc_generate
            prepostprocgenerate(prepostprocinfo)
            customargs[section] = prepostprocinfo.customarg

    @staticmethod
    def __generate_section(section, *, customargs: t.Dict, culture: annize.i18n.Culture,
                           document_root_directory: annize.fs.FsEntry, document_root_url: str,
                           document_variant_directory: annize.fs.FsEntry):
        document_variant_directory.mkdir()
        generateinfo = HomepageSection._GenerateInfo(
            culture=culture, customarg=customargs[section],
            document_root_url=document_root_url, document_variant_url="",
            document_variant_directory=document_variant_directory)
        sectioncontent = section.generate(generateinfo)
        if sectioncontent is not None:
            customargs[section] = generateinfo.customarg
            rstheading = annize.features.documentation.sphinx.rst.RstGenerator.heading(section.head,
                                                                                       variant="^", sub=True,
                                                                                       anchor="TODO sctn.key")
            return f"{rstheading}\n{sectioncontent.rst_text}\n\n"
        return ""

    def generate(self):
        variants = []
        sections = sorted(self.sections, key=lambda x: x.sortindex)
        result = annize.fs.temp.fresh_temp_dir(annize.context.object_name(self)).owned()
        customargs = {section: None for section in sections}
        document_root_url = "../"  # TODO nicer?! more robust?!
        self.__generate_postpreproc(customargs=customargs, is_pre=True,
                                    document_root_directory=result,
                                    document_root_url=document_root_url)
        rmcustomargs = set()
        for language in self.__languages:
            document_variant_directory = result.child_by_relative_path(language)
            with annize.i18n.get_culture(language):
                page = annize.features.documentation.sphinx.rst.RstGenerator.heading("Welcome!")#TODO noh i18n
                for section in sections:
                    pcont = self.__generate_section(section, customargs=customargs,
                                                    culture=annize.i18n.get_culture(language),
                                                    document_root_directory=result, document_root_url=document_root_url,
                                                    document_variant_directory=document_variant_directory)
                    if not pcont:
                        rmcustomargs.add(section)
                    page += pcont
                fpage = annize.fs.temp.TempFileByContent(content=page, filename="index.rst")
                variants.append(annize.features.documentation.sphinx.common.RstDocumentVariant(language=language,
                                                                                               source=fpage))
        for rmcustomarg in rmcustomargs:
            customargs.pop(rmcustomarg)
        doc = annize.features.documentation.sphinx.common.RstDocument(variants=variants)
        outputspec = annize.features.documentation.sphinx.output.html.HtmlOutputSpec(title=self.title,
                                                                                     short_desc=self.short_desc,
                                                                                     is_homepage=True)
        doc.generate_all_languages(outputspec).file.owned().move_to(result.path(), merge=True)
        self.__generate_postpreproc(customargs=customargs, is_pre=False,
                                    document_root_directory=result,
                                    document_root_url=document_root_url)
        return result.disowned()


class SimpleProjectHomepage(Homepage):

    @annize.callconv.parameter_from_childnodes("changelog")
    @annize.callconv.parameter_from_childnodes("dependencies")
    @annize.callconv.parameter_from_childnodes("distributables")
    @annize.callconv.parameter_from_childnodes("documentation")
    @annize.callconv.parameter_from_childnodes("mediagalleries")
    def __init__(self, *, changelog: annize.features.changelog.common.Changelog = None,
                 dependencies: t.List[annize.features.dependencies.common.Dependency],
                 distributables: t.List[annize.features.distributables.common.Group],
                 documentation: t.List[annize.features.documentation.common.Document],
                 imprint: str = None,  # TODO i18n typing
                 mediagalleries: t.List[annize.features.mediagalleries.Gallery], **kwargs):
        import annize.features.homepage.sections.about
        import annize.features.homepage.sections.changelog
        import annize.features.homepage.sections.documentation
        import annize.features.homepage.sections.download
        import annize.features.homepage.sections.gallery
        import annize.features.homepage.sections.imprint
        import annize.features.homepage.sections.license
        sections = annize.features.homepage.sections
        super().__init__(**kwargs)
        self._append_section(sections.about.Section())
        self._append_section(sections.changelog.Section(changelog=changelog))
        self._append_section(sections.documentation.Section(documentation=documentation))
        self._append_section(sections.download.Section(distributables=distributables, dependencies=dependencies))
        self._append_section(sections.gallery.Section(mediagalleries=mediagalleries))
        self._append_section(sections.imprint.Section(imprint=imprint))
        self._append_section(sections.license.Section())


class GeneratedHomepage(annize.fs.AdHocFsEntry):

    @annize.callconv.parameter_from_childnodes("homepage")
    def __init__(self, *, homepage: Homepage):
        super().__init__()
        self.__homepage = homepage

    def _initialize(self):
        return self.__homepage.generate()


class PinoHomepageAuxInfo(HomepageSection):  # TODO move to pinoprivate

    def __init__(self):
        super().__init__(head="")

    def preproc_generate(self, info):
        info.document_root_directory.child_by_relative_path("__project_name").write_file(annize.features.base.pretty_project_name())

    def _generate(self, info):
        info.document_variant_directory.child_by_relative_path("__summary").write_file(annize.features.base.summary())
        info.document_variant_directory.child_by_relative_path("__long_description").write_file(annize.features.base.long_description())


# TODO noh :       import locale; locale.setlocale(locale.LC_ALL, '')   ?!  see http://pythondialog.sourceforge.net/
